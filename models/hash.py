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
class HashStructure:
    capacity: int
    key_length: int
    hash_func: str  # 'cuadrado' | 'modular' | 'plegamiento' | 'truncamiento'
    collision: str  # 'secuencial' | 'doble' | 'cuadrado'
    table: List[Optional[int]] = field(default_factory=list)

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
        if self.collision not in {"secuencial", "doble", "cuadrado"}:
            raise ValueError("Estrategia de colisión no soportada")
        # Init table
        if not self.table:
            self.table = [None] * self.capacity
        else:
            # Normalize table length
            if len(self.table) != self.capacity:
                raise ValueError("La tabla cargada no coincide con la capacidad")

    @property
    def size(self) -> int:
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
        n = len(str(self.capacity - 1))
        s = str(abs(value)).zfill(n)
        total = 0
        for i in range(0, len(s), n):
            total += int(s[i:i + n])
        return total % self.capacity

    def _h_truncate(self, value: int) -> int:
        n = len(str(self.capacity - 1))
        s = str(abs(value)).zfill(n)
        return int(s[-n:]) % self.capacity

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
        for i in range(self.capacity):
            idx = self._index_at(h, value, i)
            slot = self.table[idx]
            if slot is None:
                return -1
            if isinstance(slot, int) and slot == value:
                return idx
            # if tombstone, continue probing
        return -1

    def insert(self, value: int) -> Tuple[int, Optional[int], int]:
        if self.size >= self.capacity:
            raise ValueError("La estructura está llena")
        if not self._valid_key(value):
            raise ValueError("La clave no cumple la longitud configurada")
        if self.find(value) != -1:
            raise ValueError("La clave ya existe (duplicada)")

        h = self._hash(value)
        first_collision_index: Optional[int] = None
        for i in range(self.capacity):
            idx = self._index_at(h, value, i)
            slot = self.table[idx]
            if slot is None or slot is TOMBSTONE:
                self.table[idx] = value
                attempts = i + 1
                return idx, first_collision_index, attempts
            if first_collision_index is None:
                first_collision_index = idx
        raise ValueError("No se encontró espacio libre (tabla llena)")

    def delete(self, value: int) -> int:
        idx = self.find(value)
        if idx == -1:
            raise ValueError("La clave no existe")
        self.table[idx] = TOMBSTONE
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
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValueError("Capacidad inválida en archivo")
        if capacidad > 10000 or not _is_power_of_10(capacidad):
            raise ValueError("Capacidad debe ser potencia de 10 y ≤ 10000")
        if not isinstance(klen, int) or not (1 <= klen <= 9):
            raise ValueError("Longitud de clave inválida en archivo")
        if hname not in {"cuadrado", "modular", "plegamiento", "truncamiento"}:
            raise ValueError("Función hash inválida en archivo")
        if cname not in {"secuencial", "doble", "cuadrado"}:
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
        return HashStructure(capacidad, klen, hname, cname, table)
