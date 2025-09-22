from __future__ import annotations

from dataclasses import dataclass, field
import bisect
import json
import math
import random
from typing import Any, Dict, List, Optional


def _is_power_of_10(n: int) -> bool:
    if n <= 0:
        return False
    while n % 10 == 0:
        n //= 10
    return n == 1


@dataclass
class SearchResult:
    index: int
    block: int
    offset: int
    found: bool

    @classmethod
    def not_found(cls, block: int = -1) -> "SearchResult":
        return cls(-1, block, -1, False)


@dataclass
class ExternalStructureBase:
    capacity: int
    key_length: int
    items: List[int] = field(default_factory=list)
    type_name: str = "externa"

    def __post_init__(self):
        if not isinstance(self.capacity, int) or self.capacity <= 0:
            raise ValueError("Capacidad inválida")
        if self.capacity > 10000 or not _is_power_of_10(self.capacity):
            raise ValueError("La capacidad debe ser potencia de 10 y ≤ 10000")
        if not (1 <= int(self.key_length) <= 9):
            raise ValueError("Longitud de clave inválida (1-9)")
        # Normalizar datos iniciales
        cleaned: List[int] = []
        seen = set()
        for value in sorted(self.items):
            if not isinstance(value, int):
                raise ValueError("Los datos deben ser enteros")
            if len(str(abs(value))) != int(self.key_length):
                raise ValueError("Clave con longitud no compatible")
            if value in seen:
                raise ValueError("Claves duplicadas no permitidas")
            cleaned.append(value)
            seen.add(value)
        if len(cleaned) > self.capacity:
            raise ValueError("'datos' excede la capacidad")
        self.items = cleaned

    # Propiedades de bloques
    @property
    def block_size(self) -> int:
        return max(1, math.isqrt(self.capacity))

    @property
    def block_count(self) -> int:
        size = self.block_size
        return (self.capacity + size - 1) // size

    # Utilidades internas
    def _valid_key(self, value: int) -> bool:
        return isinstance(value, int) and len(str(abs(value))) == int(self.key_length)

    def locate_index(self, index: int) -> tuple[int, int]:
        if index < 0 or index >= len(self.items):
            raise ValueError("Índice fuera de rango")
        block = index // self.block_size
        offset = index % self.block_size
        return block, offset

    def get_blocks(self, fill: bool = True) -> List[List[Optional[int]]]:
        blocks: List[List[Optional[int]]] = []
        size = self.block_size
        for b in range(self.block_count):
            start = b * size
            end = min(start + size, len(self.items))
            if start >= len(self.items):
                block: List[Optional[int]] = []
            else:
                block = list(self.items[start:end])
            if fill and len(block) < size:
                block.extend([None] * (size - len(block)))
            blocks.append(block)
        return blocks

    def get_block_base(self, block_index: int) -> Optional[int]:
        size = self.block_size
        start = block_index * size
        end = min(start + size, len(self.items))
        if start >= len(self.items) or end == 0:
            return None
        return self.items[end - 1]

    def get_block_bases(self) -> List[Optional[int]]:
        return [self.get_block_base(i) for i in range(self.block_count)]

    # Operaciones básicas comunes
    @property
    def is_full(self) -> bool:
        return len(self.items) >= self.capacity

    def insert(self, value: int) -> int:
        if self.is_full:
            raise ValueError("La estructura está llena")
        if not self._valid_key(value):
            raise ValueError("La clave no cumple la longitud configurada")
        idx = bisect.bisect_left(self.items, value)
        if idx < len(self.items) and self.items[idx] == value:
            raise ValueError("La clave ya existe (duplicada)")
        self.items.insert(idx, value)
        return idx

    def delete(self, value: int) -> int:
        idx = bisect.bisect_left(self.items, value)
        if idx == len(self.items) or self.items[idx] != value:
            raise ValueError("La clave no existe")
        self.items.pop(idx)
        return idx

    # Serialización
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": self.type_name,
            "capacidad": self.capacity,
            "longitud_clave": int(self.key_length),
            "datos": list(self.items),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExternalStructureBase":
        if not isinstance(data, dict) or data.get("tipo") != cls.type_name:
            raise ValueError(f"Archivo incompatible: 'tipo' debe ser '{cls.type_name}'")
        capacidad = data.get("capacidad")
        klen = data.get("longitud_clave")
        datos = data.get("datos")
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError("Capacidad inválida en archivo")
        if capacidad > 10000 or not _is_power_of_10(capacidad):
            raise ValueError("Capacidad debe ser potencia de 10 y ≤ 10000")
        if not isinstance(klen, int) or not (1 <= klen <= 9):
            raise ValueError("Longitud de clave inválida en archivo")
        if not isinstance(datos, list):
            raise ValueError("Estructura de datos inválida en archivo")
        for value in datos:
            if not isinstance(value, int):
                raise ValueError("Los datos deben ser enteros")
            if len(str(abs(value))) != klen:
                raise ValueError("Clave con longitud no compatible")
        return cls(capacidad, klen, list(datos))

    def generate_random(self, count: int) -> int:
        if count <= 0:
            return 0
        remaining_capacity = self.capacity - len(self.items)
        if remaining_capacity <= 0:
            return 0
        to_add = min(count, remaining_capacity)
        k = int(self.key_length)
        min_val = 0 if k == 1 else 10 ** (k - 1)
        max_val = 10 ** k - 1
        existing = set(self.items)
        added_vals: List[int] = []
        while len(added_vals) < to_add:
            v = random.randint(min_val, max_val)
            if v in existing:
                continue
            existing.add(v)
            added_vals.append(v)
        self.items.extend(added_vals)
        self.items.sort()
        return len(added_vals)

    # Métodos de búsqueda (a implementar en subclases)
    def find(self, value: int) -> SearchResult:  # pragma: no cover - abstract
        raise NotImplementedError


class ExternalSequentialStructure(ExternalStructureBase):
    type_name = "externa_secuencial"

    def _find_block_sequential(self, value: int) -> Optional[int]:
        bases = self.get_block_bases()
        last_valid_block = -1
        for i, base in enumerate(bases):
            if base is None:
                break
            last_valid_block = i
            if value <= base:
                return i
        if last_valid_block != -1:
            return last_valid_block
        return None

    def find(self, value: int) -> SearchResult:
        if not self._valid_key(value):
            return SearchResult.not_found()
        block = self._find_block_sequential(value)
        if block is None:
            return SearchResult.not_found()
        size = self.block_size
        start = block * size
        end = min(start + size, len(self.items))
        for offset, idx in enumerate(range(start, end)):
            if self.items[idx] == value:
                return SearchResult(idx, block, offset, True)
        return SearchResult.not_found(block)


class ExternalBinaryStructure(ExternalStructureBase):
    type_name = "externa_binaria"

    def _find_block_binary(self, value: int) -> Optional[int]:
        bases = []
        indices = []
        for i, base in enumerate(self.get_block_bases()):
            if base is None:
                break
            bases.append(base)
            indices.append(i)
        if not bases:
            return None
        pos = bisect.bisect_left(bases, value)
        if pos >= len(indices):
            return None
        return indices[pos]

    def find(self, value: int) -> SearchResult:
        if not self._valid_key(value):
            return SearchResult.not_found()
        block = self._find_block_binary(value)
        if block is None:
            return SearchResult.not_found()
        size = self.block_size
        start = block * size
        end = min(start + size, len(self.items))
        block_slice = self.items[start:end]
        pos = bisect.bisect_left(block_slice, value)
        if pos < len(block_slice) and block_slice[pos] == value:
            return SearchResult(start + pos, block, pos, True)
        return SearchResult.not_found(block)
