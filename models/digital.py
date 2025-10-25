from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Tuple


@dataclass
class DigitalNode:
    id: int
    value: Optional[str] = None
    left: Optional['DigitalNode'] = None
    right: Optional['DigitalNode'] = None


class DigitalTree:
    """Árbol digital simple que inserta letras siguiendo la lógica descrita:
    - El primer elemento insertado se convierte en la raíz.
    - Para cada letra se recorre su código bit a bit. Si en la dirección indicada
      no existe hijo se crea un nodo y se coloca la letra allí (se detiene)
    - Si existe, se sigue con el siguiente bit.
    """

    CODE_TABLE = {
        'A': '00001', 'B': '00010', 'C': '00011', 'D': '00100', 'E': '00101',
        'F': '00110', 'G': '00111', 'H': '01000', 'I': '01001', 'J': '01010',
        'K': '01011', 'L': '01100', 'M': '01101', 'N': '01110', 'O': '01111',
        'P': '10000', 'Q': '10001', 'R': '10010', 'S': '10011', 'T': '10100',
        'U': '10101', 'V': '10110', 'W': '10111', 'X': '11000', 'Y': '11001',
        'Z': '11010',
    }

    def __init__(self):
        self.root: Optional[DigitalNode] = None
        self._next_id = 1
        self._insertion_order: List[str] = []

    def _new_node(self, value: Optional[str] = None) -> DigitalNode:
        node = DigitalNode(self._next_id, value)
        self._next_id += 1
        return node

    def insert(self, letter: str) -> List[int]:
        letter = letter.upper()
        if letter not in self.CODE_TABLE:
            raise ValueError("Sólo letras A-Z permitidas")
        if letter in self._insertion_order:
            raise ValueError("La letra ya fue insertada")

        code = self.CODE_TABLE[letter]
        if self.root is None:
            self.root = self._new_node(letter)
            self._insertion_order.append(letter)
            return [self.root.id]

        path_ids: List[int] = []
        node = self.root
        path_ids.append(node.id)

        # Recorremos dígito a dígito; si falta hijo en la dirección indicada,
        # creamos y colocamos la letra allí (no es necesario agotar todos los bits)
        for bit in code:
            if bit == '0':
                if node.left is None:
                    node.left = self._new_node(letter)
                    path_ids.append(node.left.id)
                    self._insertion_order.append(letter)
                    return path_ids
                else:
                    node = node.left
                    path_ids.append(node.id)
            else:
                if node.right is None:
                    node.right = self._new_node(letter)
                    path_ids.append(node.right.id)
                    self._insertion_order.append(letter)
                    return path_ids
                else:
                    node = node.right
                    path_ids.append(node.id)

        # Si consumimos todos los bits y llegamos a un nodo ya existente, y si
        # el nodo no tiene valor, lo asignamos. Si ya tiene valor, tratamos como
        # duplicado.
        if node.value is None:
            node.value = letter
            self._insertion_order.append(letter)
            return path_ids

        raise ValueError("No se pudo insertar la letra (posición ocupada)")

    def find(self, letter: str) -> List[int]:
        letter = letter.upper()
        found_path: List[int] = []
        if self.root is None:
            return found_path

        # Búsqueda por recorrido completo: localizamos el nodo con el valor
        # y devolvemos la ruta desde la raíz hasta él (IDs)
        path: List[DigitalNode] = []

        def dfs(node: Optional[DigitalNode]) -> bool:
            if node is None:
                return False
            path.append(node)
            if node.value == letter:
                return True
            if dfs(node.left):
                return True
            if dfs(node.right):
                return True
            path.pop()
            return False

        if dfs(self.root):
            return [n.id for n in path]
        return []

    def delete(self, letter: str) -> bool:
        letter = letter.upper()
        if letter not in self._insertion_order:
            raise ValueError("La letra no existe en el árbol")
        # Removemos de la lista de inserción y reconstruimos el árbol
        self._insertion_order = [x for x in self._insertion_order if x != letter]
        self._rebuild()
        return True

    def _rebuild(self):
        # Reiniciar árbol e insertar en el mismo orden de llegada
        self.root = None
        self._next_id = 1
        order = list(self._insertion_order)
        self._insertion_order = []
        for letter in order:
            self.insert(letter)

    def to_list(self) -> List[Tuple[int, Optional[str], Optional[int], Optional[int]]]:
        """Devuelve lista de nodos: (id, value, left_id, right_id) para visualización."""
        res: List[Tuple[int, Optional[str], Optional[int], Optional[int]]] = []

        def dfs(node: Optional[DigitalNode]):
            if node is None:
                return
            left_id = node.left.id if node.left else None
            right_id = node.right.id if node.right else None
            res.append((node.id, node.value, left_id, right_id))
            dfs(node.left)
            dfs(node.right)

        dfs(self.root)
        return res
