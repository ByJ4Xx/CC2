from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Tuple, Dict


@dataclass
class RMNode:
    id: int
    value: Optional[str] = None  # None for aux/internal
    children: Dict[str, 'RMNode'] = None  # keys: '00','01','10','11' or '0','1'

    def __post_init__(self):
        if self.children is None:
            self.children = {}


class ResidueMultipleTree:
    CODE_TABLE = {
        'A': '00001', 'B': '00010', 'C': '00011', 'D': '00100', 'E': '00101',
        'F': '00110', 'G': '00111', 'H': '01000', 'I': '01001', 'J': '01010',
        'K': '01011', 'L': '01100', 'M': '01101', 'N': '01110', 'O': '01111',
        'P': '10000', 'Q': '10001', 'R': '10010', 'S': '10011', 'T': '10100',
        'U': '10101', 'V': '10110', 'W': '10111', 'X': '11000', 'Y': '11001',
        'Z': '11010',
    }

    def __init__(self):
        # root aux node
        self._next_id = 1
        self.root = self._new_node(None)
        self._insertion_order: List[str] = []

    def _new_node(self, value: Optional[str] = None) -> RMNode:
        node = RMNode(self._next_id, value)
        self._next_id += 1
        return node

    def clear(self):
        self._next_id = 1
        self.root = self._new_node(None)
        self._insertion_order = []

    def insert(self, letter: str) -> List[int]:
        letter = letter.upper()
        if letter not in self.CODE_TABLE:
            raise ValueError("Sólo letras A-Z permitidas")
        if letter in self._insertion_order:
            raise ValueError("La letra ya fue insertada")

        code = self.CODE_TABLE[letter]
        node = self.root
        path_ids = [node.id]
        idx = 0

        while idx < len(code):
            remaining = len(code) - idx
            # use two-bit chunks while possible
            if remaining >= 2:
                chunk = code[idx:idx+2]
                idx += 2
                # child keys for aux levels are two-bit strings
                child = node.children.get(chunk)
                if child is None:
                    # create aux node
                    aux = self._new_node(None)
                    node.children[chunk] = aux
                    node = aux
                    path_ids.append(node.id)
                    continue
                # if child is leaf (value not None) but we need to go deeper
                if child.value is not None:
                    # collision: replace child with aux and reinsert existing letter deeper
                    existing = child.value
                    aux = self._new_node(None)
                    node.children[chunk] = aux
                    # reinsert existing starting from current idx into aux
                    self._reinsert_into(aux, existing, idx)
                    node = aux
                    path_ids.append(node.id)
                    continue
                # otherwise descend
                node = child
                path_ids.append(node.id)
            else:
                # final single bit: '0' or '1' makes leaf under current node
                bit = code[idx]
                idx += 1
                child = node.children.get(bit)
                if child is None:
                    leaf = self._new_node(letter)
                    leaf.value = letter
                    node.children[bit] = leaf
                    path_ids.append(leaf.id)
                    self._insertion_order.append(letter)
                    return path_ids
                # if child exists and is aux, we may need to descend further (unlikely)
                if child.value is None:
                    # descend into aux and attempt to place as value if empty
                    node = child
                    path_ids.append(node.id)
                    # since no more bits, try to place here if empty
                    if node.children == {} and node.value is None:
                        node.value = letter
                        self._insertion_order.append(letter)
                        return path_ids
                    # otherwise, create leaf under default '0'
                    leaf = self._new_node(letter)
                    leaf.value = letter
                    node.children['0'] = leaf
                    path_ids.append(leaf.id)
                    self._insertion_order.append(letter)
                    return path_ids
                else:
                    # collision at final bit: existing leaf -> convert to aux and reinsert
                    existing = child.value
                    aux = self._new_node(None)
                    node.children[bit] = aux
                    # reinsert existing into aux at next position (no bits left => put under '0')
                    self._reinsert_into(aux, existing, len(self.CODE_TABLE[existing]))
                    # insert new letter as sibling under '0' if free
                    leaf = self._new_node(letter)
                    leaf.value = letter
                    aux.children['0'] = leaf
                    path_ids.append(aux.id)
                    path_ids.append(leaf.id)
                    self._insertion_order.append(letter)
                    return path_ids

        # if loop exits, we ended exactly at some aux node; place letter here if empty
        if node.value is None and node.children == {}:
            node.value = letter
            self._insertion_order.append(letter)
            return path_ids

        raise ValueError("No se pudo insertar la letra")

    def _reinsert_into(self, node: RMNode, letter: str, idx: int):
        # Helper to reinsert existing letter into aux node starting at bit index idx
        code = self.CODE_TABLE[letter]
        cur = node
        i = idx
        while i < len(code):
            remaining = len(code) - i
            if remaining >= 2:
                chunk = code[i:i+2]
                i += 2
                child = cur.children.get(chunk)
                if child is None:
                    # create aux or leaf depending on remaining bits
                    if i >= len(code):
                        leaf = self._new_node(letter)
                        leaf.value = letter
                        cur.children[chunk] = leaf
                        return
                    else:
                        aux = self._new_node(None)
                        cur.children[chunk] = aux
                        cur = aux
                        continue
                else:
                    if child.value is not None:
                        # deeper collision: convert to aux
                        existing = child.value
                        aux = self._new_node(None)
                        cur.children[chunk] = aux
                        cur = aux
                        # restart reinsertion for existing from current i
                        self._reinsert_into(cur, existing, i)
                        continue
                    else:
                        cur = child
                        continue
            else:
                bit = code[i]
                i += 1
                child = cur.children.get(bit)
                if child is None:
                    leaf = self._new_node(letter)
                    leaf.value = letter
                    cur.children[bit] = leaf
                    return
                if child.value is None:
                    cur = child
                    continue
                else:
                    # collision at final bit: convert to aux
                    existing = child.value
                    aux = self._new_node(None)
                    cur.children[bit] = aux
                    # put existing under '0'
                    leaf = self._new_node(existing)
                    leaf.value = existing
                    aux.children['0'] = leaf
                    # then place new letter under '1'
                    leaf2 = self._new_node(letter)
                    leaf2.value = letter
                    aux.children['1'] = leaf2
                    return

    def find(self, letter: str) -> List[int]:
        letter = letter.upper()
        path: List[RMNode] = []

        def dfs(node: Optional[RMNode]) -> bool:
            if node is None:
                return False
            path.append(node)
            if node.value == letter:
                return True
            for k in sorted(node.children.keys()):
                if dfs(node.children[k]):
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
        self._insertion_order = [x for x in self._insertion_order if x != letter]
        # rebuild by clearing and reinserting
        order = list(self._insertion_order)
        self.clear()
        for l in order:
            self.insert(l)
        return True

    def to_dict(self) -> dict:
        return {"tipo": "residuo_multiple", "insertion_order": list(self._insertion_order)}

    @classmethod
    def from_dict(cls, data: dict) -> "ResidueMultipleTree":
        if not isinstance(data, dict) or data.get("tipo") != "residuo_multiple":
            raise ValueError("Archivo incompatible: 'tipo' debe ser 'residuo_multiple'")
        order = data.get("insertion_order")
        if not isinstance(order, list):
            raise ValueError("insertion_order inválido en archivo")
        t = cls()
        for letter in order:
            t.insert(letter)
        return t

    def to_list(self) -> List[Tuple[int, Optional[str], Dict[str, int]]]:
        """Return list of nodes and mapping of child labels to child ids for visualization.
        Each entry: (id, value, {label: child_id, ...})
        """
        res: List[Tuple[int, Optional[str], Dict[str, int]]] = []

        def dfs(node: RMNode):
            mapping = {k: v.id for k, v in node.children.items()}
            res.append((node.id, node.value, mapping))
            for k in sorted(node.children.keys()):
                dfs(node.children[k])

        dfs(self.root)
        return res
