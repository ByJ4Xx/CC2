from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Tuple
import json
import math

@dataclass
class ExternalHashStructure:
    num_records: int
    key_length: int
    hash_func: str  # 'cuadrado' | 'modular' | 'plegamiento' | 'truncamiento' | 'conversion_base'
    base: Optional[int] = None  # Only for conversion_base (2-9)
    trunc_positions: Optional[List[int]] = None  # Indices to pick for truncation (0-based left->right)
    folding_op: Optional[str] = None  # 'suma' or 'multiplicacion' for plegamiento
    
    # Calculated attributes
    num_blocks: int = field(init=False)
    records_per_block: int = field(init=False)
    
    # Structures: List of blocks, where each block is a list of records (int or None)
    main_structure: List[List[Optional[int]]] = field(default_factory=list)
    collision_structure: List[List[Optional[int]]] = field(default_factory=list)

    def __post_init__(self):
        if self.num_records <= 0:
            raise ValueError("El número de registros debe ser mayor a 0")
        
        # B = |sqrt(n)|
        self.num_blocks = int(math.sqrt(self.num_records))
        if self.num_blocks == 0: 
            self.num_blocks = 1
            
        # Records per block = |n/B|
        self.records_per_block = int(self.num_records / self.num_blocks)
        if self.records_per_block == 0:
            self.records_per_block = 1

        # Validate base for conversion_base
        if self.hash_func == "conversion_base":
            if self.base is None or not (2 <= self.base <= 9):
                raise ValueError("Base inválida para conversión de base (debe ser 2-9)")

        # Validate folding_op for plegamiento
        if self.hash_func == "plegamiento":
            if self.folding_op is None:
                # default to suma
                self.folding_op = "suma"
            if self.folding_op not in ("suma", "multiplicacion"):
                raise ValueError("Operación de plegamiento inválida")

        # Initialize structures if empty
        if not self.main_structure:
            self.main_structure = [[None] * self.records_per_block for _ in range(self.num_blocks)]
        if not self.collision_structure:
            self.collision_structure = [[None] * self.records_per_block for _ in range(self.num_blocks)]

    def _valid_key(self, value: int) -> bool:
        return isinstance(value, int) and len(str(abs(value))) == int(self.key_length)

    # --- Hash Functions ---
    def _h_square(self, value: int) -> int:
        n = len(str(self.num_blocks - 1))
        sq = value * value
        s = str(sq)
        if len(s) < n:
            s = s.zfill(n)
        start = (len(s) - n) // 2
        block = s[start:start + n]
        return int(block) % self.num_blocks

    def _h_modular(self, value: int) -> int:
        return value % self.num_blocks

    def _h_folding(self, value: int) -> int:
        # chunk size determined by digits needed for block index
        n = len(str(self.num_blocks - 1))
        if n == 0:
            n = 1
        s = str(abs(value))
        # pad s to multiple of n
        pad = (-len(s)) % n
        if pad:
            s = s.zfill(len(s) + pad)

        if self.folding_op == "multiplicacion":
            total = 1
            for i in range(0, len(s), n):
                chunk = int(s[i:i + n])
                total *= chunk
        else:
            total = 0
            for i in range(0, len(s), n):
                total += int(s[i:i + n])

        return total

    def _h_truncate(self, value: int) -> int:
        s = str(abs(value)).zfill(self.key_length)
        # If trunc_positions provided, pick those indices (0-based left->right)
        if self.trunc_positions:
            try:
                selected = ''.join(s[pos] for pos in self.trunc_positions)
            except Exception:
                raise ValueError("Posiciones de truncamiento inválidas")
            return int(selected)

        # Default: take last m digits where m = digits for block index
        m = len(str(self.num_blocks - 1))
        if m == 0:
            m = 1
        return int(s[-m:])

    def _h_base_conversion(self, value: int) -> int:
        # K is key, G is base.
        # Example: K=2538, G=9.
        # 2*9^3 + 5*9^2 + 3*9^1 + 8*9^0 = 1998
        # Result -> 98 (This implies modulo or taking last digits to fit address space)
        # Given the context of hash functions mapping to an address space (num_blocks),
        # we will use modulo num_blocks.
        
        s_val = str(abs(value))
        n = len(s_val)
        total = 0
        # Interpret the decimal digits as coefficients for the polynomial in base G
        # Note: The user example treats '2538' as digits 2, 5, 3, 8.
        # This is technically interpreting the decimal number string as if it were in base 10,
        # but using the digits as coefficients for powers of G.
        
        for i, char in enumerate(s_val):
            digit = int(char)
            exponent = n - 1 - i
            total += digit * (self.base ** exponent)
            
        return total

    def _hash(self, value: int) -> int:
        if self.hash_func == "cuadrado":
            return self._h_square(value)
        if self.hash_func == "modular":
            return self._h_modular(value)
        if self.hash_func == "plegamiento":
            return self._h_folding(value)
        if self.hash_func == "truncamiento":
            return self._h_truncate(value)
        if self.hash_func == "conversion_base":
            return self._h_base_conversion(value)
        raise ValueError("Función hash no soportada")

    # --- Operations ---
    def insert(self, value: int) -> Tuple[int, str, int]:
        """
        Returns: (block_index, structure_type, record_index)
        structure_type: 'main' or 'collision'
        """
        if not self._valid_key(value):
            raise ValueError(f"La clave debe tener {self.key_length} dígitos")
        
        # Check for duplicates
        if self.search(value):
            raise ValueError("La clave ya existe")

        h = self._hash(value) % self.num_blocks
        
        # Try Main Structure
        block = self.main_structure[h]
        for i, slot in enumerate(block):
            if slot is None:
                block[i] = value
                return h, "main", i
        
        # Try Collision Structure
        col_block = self.collision_structure[h]
        for i, slot in enumerate(col_block):
            if slot is None:
                col_block[i] = value
                return h, "collision", i
                
        raise ValueError("Bloque y área de colisión llenos")

    def search(self, value: int) -> Optional[Tuple[int, str, int]]:
        if not self._valid_key(value):
            return None
            
        h = self._hash(value) % self.num_blocks
        
        # Check Main
        block = self.main_structure[h]
        for i, slot in enumerate(block):
            if slot == value:
                return h, "main", i
                
        # Check Collision
        col_block = self.collision_structure[h]
        for i, slot in enumerate(col_block):
            if slot == value:
                return h, "collision", i
                
        return None

    def delete(self, value: int) -> bool:
        found = self.search(value)
        if not found:
            raise ValueError("Clave no encontrada")
            
        h, struct_type, idx = found
        if struct_type == "main":
            self.main_structure[h][idx] = None
        else:
            self.collision_structure[h][idx] = None
        return True

    # --- Serialization ---
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": "external_hash",
            "num_records": self.num_records,
            "key_length": self.key_length,
            "hash_func": self.hash_func,
            "base": self.base,
            "trunc_positions": self.trunc_positions,
            "folding_op": self.folding_op,
            "main_structure": self.main_structure,
            "collision_structure": self.collision_structure
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "ExternalHashStructure":
        if data.get("tipo") != "external_hash":
            raise ValueError("Tipo de archivo inválido")
            
        obj = ExternalHashStructure(
            num_records=data["num_records"],
            key_length=data["key_length"],
            hash_func=data["hash_func"],
            base=data.get("base"),
            trunc_positions=data.get("trunc_positions"),
            folding_op=data.get("folding_op")
        )
        obj.main_structure = data["main_structure"]
        obj.collision_structure = data["collision_structure"]
        return obj

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
