from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Tuple
import json
import random


def _is_power_of_10(n: int) -> bool:
    if n <= 0:
        return False
    while n % 10 == 0:
        n //= 10
    return n == 1


TOMBSTONE = object()


@dataclass
class Node:
    value: int
    next: Optional["Node"] = None


@dataclass
class HashStructure:
    capacity: int
    key_length: int
    hash_func: str  # 'cuadrado' | 'modular' | 'plegamiento' | 'truncamiento'
    collision: str  # 'secuencial' | 'doble' | 'cuadrado' | 'anidados' | 'encadenamiento'
    table: List[Any] = field(default_factory=list)
    trunc_positions: Optional[List[int]] = None
    folding_op: Optional[str] = None  # 'suma' or 'multiplicacion'

    def __post_init__(self):
        if not isinstance(self.capacity, int) or self.capacity <= 0:
            raise ValueError("Capacidad inválida")
        if self.capacity > 10000 or not _is_power_of_10(self.capacity):
            raise ValueError("La capacidad debe ser potencia de 10 y ≤ 10000")
        if not (1 <= int(self.key_length) <= 9):
            raise ValueError("Longitud de clave inválida (1-9)")
        self.hash_func = self.hash_func.lower()
        self.collision = self.collision.lower()
        if self.hash_func not in {"cuadrado", "modular", "plegamiento", "truncamiento"}:
            raise ValueError("Función hash no soportada")
        if self.collision not in {"secuencial", "doble", "cuadrado", "anidados", "encadenamiento"}:
            raise ValueError("Estrategia de colisión no soportada")
        # Init table
        if not self.table:
            if self.collision == "anidados":
                self.table = [[] for _ in range(self.capacity)]
            else:
                self.table = [None] * self.capacity
        else:
            # Normalize table length
            if len(self.table) != self.capacity:
                raise ValueError("La tabla cargada no coincide con la capacidad")

        # Default folding_op
        if self.hash_func == "plegamiento":
            if self.folding_op is None:
                self.folding_op = "suma"
            if self.folding_op not in ("suma", "multiplicacion"):
                raise ValueError("Operación de plegamiento inválida")

    @property
    def size(self) -> int:
        if self.collision == "anidados":
            return sum(len(x) for x in self.table if isinstance(x, list))
        if self.collision == "encadenamiento":
            total = 0
            for head in self.table:
                node = head
                while isinstance(node, Node):
                    total += 1
                    node = node.next
            return total
        return sum(1 for x in self.table if isinstance(x, int))

    def _valid_key(self, value: int) -> bool:
        return isinstance(value, int) and len(str(abs(value))) == int(self.key_length)

    def _h_square(self, value: int) -> int:
        n = len(str(self.capacity - 1))  # digits of capacity - 1 equals exponent n
        sq = value * value
        s = str(sq)
        if len(s) < n:
            s = s.zfill(n)
        start = (len(s) - n) // 2  # central block; if odd, picks middle-left as start
        block = s[start:start + n]
        return int(block) % self.capacity

    def _h_modular(self, value: int) -> int:
        return value % self.capacity

    def _h_folding(self, value: int) -> int:
        # chunk size determined by digits needed for index
        n = len(str(self.capacity - 1))
        if n == 0:
            n = 1
        s = str(abs(value))
        pad = (-len(s)) % n
        if pad:
            s = s.zfill(len(s) + pad)

        if self.folding_op == "multiplicacion":
            total = 1
            for i in range(0, len(s), n):
                total *= int(s[i:i + n])
        else:
            total = 0
            for i in range(0, len(s), n):
                total += int(s[i:i + n])

        return total % self.capacity

    def _h_truncate(self, value: int) -> int:
        s = str(abs(value)).zfill(self.key_length)
        # If trunc_positions provided, pick those indices (0-based left->right)
        if self.trunc_positions:
            try:
                selected = ''.join(s[pos] for pos in self.trunc_positions)
            except Exception:
                raise ValueError("Posiciones de truncamiento inválidas")
            return int(selected) % self.capacity

        # Default: take last m digits where m = digits for capacity-1
        m = len(str(self.capacity - 1))
        if m == 0:
            m = 1
        return int(s[-m:]) % self.capacity

    def _hash(self, value: int) -> int:
        if self.hash_func == "cuadrado":
            return self._h_square(value)
        if self.hash_func == "modular":
            return self._h_modular(value)
        if self.hash_func == "plegamiento":
            return self._h_folding(value)
        if self.hash_func == "truncamiento":
            return self._h_truncate(value)
        raise ValueError("Función hash no soportada")

    def _index_at(self, h: int, value: int, i: int) -> int:
        if i == 0:
            return h
        if self.collision == "secuencial":
            return (h + i)
        if self.collision == "doble":
            # Avanza de 2 en 2: equivalente a ((hash + 1) mod tamaño) + 1
            # usando índices 0-based en la tabla.
            return (h + 2 * i) % self.capacity
        if self.collision == "cuadrado":
            return (h + i * i) % self.capacity
        raise ValueError("Estrategia de colisión no soportada")

    def find(self, value: int) -> int:
        if not self._valid_key(value):
            return -1
        h = self._hash(value)
        # Nuevas estrategias: solo consulta (no inserta)
        
        if self.collision == "anidados":
            bucket = self.table[h]
            if isinstance(bucket, list) and value in bucket:
                return h + 1
            return -1
        if self.collision == "encadenamiento":
            node = self.table[h]
            while isinstance(node, Node):
                if node.value == value:
                    return h + 1
                node = node.next
            return -1
        for i in range(self.capacity):
            idx = self._index_at(h, value, i)
            slot = self.table[idx]
            if slot is None:
                return -1
            if isinstance(slot, int) and slot == value:
                return idx + 1
        return -1

    def insert(self, value: int) -> Tuple[int, Optional[int], int]:
        if self.collision not in {"anidados", "encadenamiento"} and self.size >= self.capacity:
            raise ValueError("La estructura está llena")
        if not self._valid_key(value):
            raise ValueError("La clave no cumple la longitud configurada")
        if self.find(value) != -1:
            raise ValueError("La clave ya existe (duplicada)")

        h = self._hash(value)
        # Nuevas estrategias: insertar en bucket
        if self.collision == "anidados":
            bucket = self.table[h]
            if not isinstance(bucket, list):
                bucket = []
                self.table[h] = bucket
            first_collision_index = (h if len(bucket) > 0 else None)
            bucket.append(value)
            return h + 1, (first_collision_index + 1) if first_collision_index is not None else None, 1

        if self.collision == "encadenamiento":
            head = self.table[h]
            if isinstance(head, Node):
                # Append at tail to preserve insertion order
                node = head
                while isinstance(node.next, Node):
                    node = node.next
                node.next = Node(value)
                return h + 1, h + 1, 1
            else:
                self.table[h] = Node(value)
                return h + 1, None, 1

        first_collision_index: Optional[int] = None
        for i in range(self.capacity):
            idx = self._index_at(h, value, i)
            slot = self.table[idx]
            if slot is None or slot is TOMBSTONE:
                self.table[idx] = value
                attempts = i + 1
                return idx + 1, (first_collision_index + 1) if first_collision_index is not None else None, attempts
            if first_collision_index is None:
                first_collision_index = idx
        raise ValueError("No se encontró espacio libre (tabla llena)")

    def delete(self, value: int) -> int:
        idx = self.find(value)
        if idx == -1:
            raise ValueError("La clave no existe")
        real_idx = idx - 1
        if self.collision == "anidados":
            bucket = self.table[real_idx]
            if isinstance(bucket, list):
                try:
                    bucket.remove(value)
                except ValueError:
                    pass
            return idx
        if self.collision == "encadenamiento":
            prev: Optional[Node] = None
            node = self.table[real_idx]
            while isinstance(node, Node):
                if node.value == value:
                    if prev is None:
                        self.table[real_idx] = node.next
                    else:
                        prev.next = node.next
                    return idx
                prev, node = node, node.next
            return idx
        self.table[real_idx] = TOMBSTONE
        return idx

    # Random generation avoiding duplicates
    def generate_random(self, count: int) -> int:
        if count <= 0:
            return 0
        remaining_capacity = self.capacity - self.size
        if remaining_capacity <= 0:
            return 0
        to_add = min(count, remaining_capacity)
        k = int(self.key_length)
        min_val = 0 if k == 1 else 10 ** (k - 1)
        max_val = 10 ** k - 1
        added = 0
        while added < to_add:
            v = random.randint(min_val, max_val)
            if self.find(v) != -1:
                continue
            try:
                self.insert(v)
                added += 1
            except Exception:
                # If insertion fails due to clustering, try another number
                pass
        return added

    # Serialization
    def to_dict(self) -> Dict[str, Any]:
        datos: List[Any] = []
        if self.collision in {"anidados", "encadenamiento"}:
            for x in self.table:
                if self.collision == "anidados":
                    datos.append(list(x) if isinstance(x, list) else [])
                else:
                    arr: List[int] = []
                    node = x
                    while isinstance(node, Node):
                        arr.append(node.value)
                        node = node.next
                    datos.append(arr)
        else:
            for x in self.table:
                if x is None:
                    datos.append(None)
                elif x is TOMBSTONE:
                    datos.append({"t": 1})
                else:
                    datos.append(x)
        return {
            "tipo": "hash",
            "capacidad": self.capacity,
            "longitud_clave": int(self.key_length),
            "hash_func": self.hash_func,
            "colision": self.collision,
            "trunc_positions": self.trunc_positions,
            "folding_op": self.folding_op,
            "datos": datos,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "HashStructure":
        if not isinstance(data, dict) or data.get("tipo") != "hash":
            raise ValueError("Archivo incompatible: 'tipo' debe ser 'hash'")
        capacidad = data.get("capacidad")
        klen = data.get("longitud_clave")
        hname = data.get("hash_func")
        cname = data.get("colision")
        datos = data.get("datos")
        # Soporte de nuevas estrategias al cargar
        if cname in {"anidados", "encadenamiento"}:
            if not isinstance(datos, list) or len(datos) != capacidad:
                raise ValueError("Estructura de datos invǭlida en archivo")
            if cname == "anidados":
                table_ai: List[List[int]] = []
                for x in datos:
                    if x is None:
                        table_ai.append([])
                    elif isinstance(x, list):
                        bucket: List[int] = []
                        for v in x:
                            if not isinstance(v, int) or len(str(abs(v))) != klen:
                                raise ValueError("Clave con longitud no compatible")
                            bucket.append(v)
                        table_ai.append(bucket)
                    else:
                        raise ValueError("Elemento de datos invǭlido en archivo")
                return HashStructure(capacidad, klen, hname, cname, table_ai,
                                     trunc_positions=data.get("trunc_positions"),
                                     folding_op=data.get("folding_op"))
            else:
                table_ch: List[Optional[Node]] = []
                for x in datos:
                    if x is None:
                        table_ch.append(None)
                    elif isinstance(x, list):
                        head: Optional[Node] = None
                        for v in reversed(x):
                            if not isinstance(v, int) or len(str(abs(v))) != klen:
                                raise ValueError("Clave con longitud no compatible")
                            head = Node(v, head)
                        table_ch.append(head)
                    else:
                        raise ValueError("Elemento de datos invǭlido en archivo")
                return HashStructure(capacidad, klen, hname, cname, table_ch,
                                     trunc_positions=data.get("trunc_positions"),
                                     folding_op=data.get("folding_op"))
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError("Capacidad inválida en archivo")
        if capacidad > 10000 or not _is_power_of_10(capacidad):
            raise ValueError("Capacidad debe ser potencia de 10 y ≤ 10000")
        if not isinstance(klen, int) or not (1 <= klen <= 9):
            raise ValueError("Longitud de clave inválida en archivo")
        if hname not in {"cuadrado", "modular", "plegamiento", "truncamiento"}:
            raise ValueError("Función hash inválida en archivo")
        if cname not in {"secuencial", "doble", "cuadrado", "anidados", "encadenamiento"}:
            raise ValueError("Colisión inválida en archivo")
        if not isinstance(datos, list) or len(datos) != capacidad:
            raise ValueError("Estructura de datos inválida en archivo")
        table: List[Optional[int]] = [None] * capacidad
        for i, x in enumerate(datos):
            if x is None:
                table[i] = None
            elif isinstance(x, dict) and x.get("t") == 1:
                table[i] = TOMBSTONE  # type: ignore[assignment]
            elif isinstance(x, int):
                if len(str(abs(x))) != klen:
                    raise ValueError("Clave con longitud no compatible")
                table[i] = x
            else:
                raise ValueError("Elemento de datos inválido en archivo")
        return HashStructure(capacidad, klen, hname, cname, table,
                     trunc_positions=data.get("trunc_positions"),
                     folding_op=data.get("folding_op"))

    # Utilidad para visualizacin/preview
    def bucket_items(self, index: int) -> List[int]:
        if not (0 <= index < self.capacity):
            return []
        if self.collision == "anidados":
            bucket = self.table[index]
            return list(bucket) if isinstance(bucket, list) else []
        if self.collision == "encadenamiento":
            arr: List[int] = []
            node = self.table[index]
            while isinstance(node, Node):
                arr.append(node.value)
                node = node.next
            return arr
        x = self.table[index]
        return [x] if isinstance(x, int) else []
