from __future__ import annotations

from dataclasses import dataclass, field
import json
import math
import random
from typing import List, Dict, Any


def _is_power_of_10(n: int) -> bool:
    if n <= 0:
        return False
    while n % 10 == 0:
        n //= 10
    return n == 1


@dataclass
class LinearStructure:
    capacity: int
    key_length: int
    items: List[int] = field(default_factory=list)

    def __post_init__(self):
        if not isinstance(self.capacity, int) or self.capacity <= 0:
            raise ValueError("Capacidad inválida")
        if self.capacity > 10000 or not _is_power_of_10(self.capacity):
            raise ValueError("La capacidad debe ser potencia de 10 y ≤ 10000")
        if not (1 <= int(self.key_length) <= 9):
            raise ValueError("Longitud de clave inválida (1-9)")

    # Operaciones básicas
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
        if value in self.items:
            raise ValueError("La clave ya existe (duplicada)")
        self.items.append(value)
        return len(self.items) - 1

    def find(self, value: int) -> int:
        for i, v in enumerate(self.items):
            if v == value:
                return i
        return -1

    def delete(self, value: int) -> int:
        idx = self.find(value)
        if idx == -1:
            raise ValueError("La clave no existe")
        self.items.pop(idx)
        return idx

    # Serialización
    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": "lineal",
            "capacidad": self.capacity,
            "longitud_clave": int(self.key_length),
            "datos": list(self.items),
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "LinearStructure":
        if not isinstance(data, dict) or data.get("tipo") != "lineal":
            raise ValueError("Archivo incompatible: 'tipo' debe ser 'lineal'")
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
        vistos = set()
        for x in datos:
            if not isinstance(x, int):
                raise ValueError("Los datos deben ser enteros")
            if len(str(abs(x))) != klen:
                raise ValueError("Clave con longitud no compatible")
            if x in vistos:
                raise ValueError("Claves duplicadas en archivo")
            vistos.add(x)
        if len(datos) > capacidad:
            raise ValueError("'datos' excede la capacidad")
        return LinearStructure(capacidad, klen, list(datos))

    # Generación aleatoria
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
        added = 0
        # Use random sampling with rejection to avoid duplicates
        while added < to_add:
            val = random.randint(min_val, max_val)
            if val in existing:
                continue
            self.items.append(val)
            existing.add(val)
            added += 1
        return added

