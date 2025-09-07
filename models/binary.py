from __future__ import annotations

from dataclasses import dataclass, field
import json
import bisect
import random
from typing import List, Dict, Any


def _is_power_of_10(n: int) -> bool:
    if n <= 0:
        return False
    while n % 10 == 0:
        n //= 10
    return n == 1


@dataclass
class BinaryStructure:
    capacity: int
    key_length: int
    items: List[int] = field(default_factory=list)  # always sorted ascending

    def __post_init__(self):
        if not isinstance(self.capacity, int) or self.capacity <= 0:
            raise ValueError("Capacidad inválida")
        if self.capacity > 10000 or not _is_power_of_10(self.capacity):
            raise ValueError("La capacidad debe ser potencia de 10 y ≤ 10000")
        if not (1 <= int(self.key_length) <= 9):
            raise ValueError("Longitud de clave inválida (1-9)")
        # Ensure items sorted and valid
        self.items.sort()
        last = None
        for x in self.items:
            if not isinstance(x, int):
                raise ValueError("Los datos deben ser enteros")
            if len(str(abs(x))) != int(self.key_length):
                raise ValueError("Clave con longitud no compatible")
            if last is not None and x == last:
                raise ValueError("Datos duplicados no permitidos")
            last = x
        if len(self.items) > self.capacity:
            raise ValueError("'datos' excede la capacidad")

    @property
    def is_full(self) -> bool:
        return len(self.items) >= self.capacity

    def _valid_key(self, value: int) -> bool:
        return isinstance(value, int) and len(str(abs(value))) == int(self.key_length)

    def insert(self, value: int) -> int:
        if self.is_full:
            raise ValueError("La estructura está llena")
        if not self._valid_key(value):
            raise ValueError("La clave no cumple la longitud configurada")
        i = bisect.bisect_left(self.items, value)
        if i < len(self.items) and self.items[i] == value:
            raise ValueError("La clave ya existe (duplicada)")
        self.items.insert(i, value)
        return i

    def find(self, value: int) -> int:
        i = bisect.bisect_left(self.items, value)
        if i != len(self.items) and self.items[i] == value:
            return i
        return -1

    def delete(self, value: int) -> int:
        i = bisect.bisect_left(self.items, value)
        if i == len(self.items) or self.items[i] != value:
            raise ValueError("La clave no existe")
        self.items.pop(i)
        return i

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": "binaria",
            "capacidad": self.capacity,
            "longitud_clave": int(self.key_length),
            "datos": list(self.items),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "BinaryStructure":
        if not isinstance(data, dict) or data.get("tipo") != "binaria":
            raise ValueError("Archivo incompatible: 'tipo' debe ser 'binaria'")
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
        # Validate and sort
        items = []
        seen = set()
        for x in datos:
            if not isinstance(x, int):
                raise ValueError("Los datos deben ser enteros")
            if len(str(abs(x))) != klen:
                raise ValueError("Clave con longitud no compatible")
            if x in seen:
                raise ValueError("Claves duplicadas en archivo")
            seen.add(x)
            items.append(x)
        items.sort()
        if len(items) > capacidad:
            raise ValueError("'datos' excede la capacidad")
        return BinaryStructure(capacidad, klen, items)

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
        added_vals = []
        while len(added_vals) < to_add:
            v = random.randint(min_val, max_val)
            if v in existing:
                continue
            existing.add(v)
            added_vals.append(v)
        # Merge and sort
        self.items.extend(added_vals)
        self.items.sort()
        return len(added_vals)

