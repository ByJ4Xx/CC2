from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Tuple


@dataclass
class ResidueNode:
    id: int
    value: Optional[str] = None  # None for aux/internal nodes
    left: Optional['ResidueNode'] = None
    right: Optional['ResidueNode'] = None


class ResidueTree:
    CODE_TABLE = {
        'A': '00001', 'B': '00010', 'C': '00011', 'D': '00100', 'E': '00101',
        'F': '00110', 'G': '00111', 'H': '01000', 'I': '01001', 'J': '01010',
        'K': '01011', 'L': '01100', 'M': '01101', 'N': '01110', 'O': '01111',
        'P': '10000', 'Q': '10001', 'R': '10010', 'S': '10011', 'T': '10100',
        'U': '10101', 'V': '10110', 'W': '10111', 'X': '11000', 'Y': '11001',
        'Z': '11010',
    }

    def __init__(self):
        # Root is an internal node (aux) that does not store a value
        self.root: ResidueNode = self._new_node(None)
        self._next_id = 2  # root already consumed id=1
        self._insertion_order: List[str] = []

    def _new_node(self, value: Optional[str] = None) -> ResidueNode:
        # If _next_id not yet set (during __init__), handle root specially
        try:
            nid = getattr(self, "_next_id")
        except AttributeError:
            nid = 1
        node = ResidueNode(nid, value)
        # ensure _next_id increases
        if hasattr(self, "_next_id"):
            self._next_id += 1
        else:
            self._next_id = nid + 1
        return node

    def insert(self, letter: str) -> List[int]:
        letter = letter.upper()
        if letter not in self.CODE_TABLE:
            raise ValueError("Sólo letras A-Z permitidas")
        if letter in self._insertion_order:
            raise ValueError("La letra ya fue insertada")

        code = self.CODE_TABLE[letter]
        path_ids: List[int] = [self.root.id]
        # recursive helper to insert starting at node with bit index
        def insert_from(node: ResidueNode, idx: int, letter: str) -> List[int]:
            # if we've consumed all bits, try to place here
            if idx >= len(code):
                # if node is aux (value None) and has no value, assign
                if node.value is None and node.left is None and node.right is None:
                    node.value = letter
                    return [node.id]
                # otherwise treat as collision and create aux under this node
                # create a new aux node and reinsert
            bit = code[idx]
            if bit == '0':
                child = node.left
                if child is None:
                    leaf = self._new_node(letter)
                    leaf.value = letter
                    node.left = leaf
                    return [leaf.id]
                if child.value is not None:
                    # collision: convert child into aux node
                    existing_letter = child.value
                    # replace child with aux node
                    aux = self._new_node(None)
                    node.left = aux
                    # reinsert existing and new into aux starting from next bit
                    existing_code = self.CODE_TABLE[existing_letter]
                    path_aux = []
                    # reinsert existing_letter into aux
                    def reinstate(cur: ResidueNode, start_idx: int, letter_e: str):
                        if start_idx >= len(existing_code):
                            # place at current aux if empty
                            if cur.value is None and cur.left is None and cur.right is None:
                                cur.value = letter_e
                                return [cur.id]
                            else:
                                # create a leaf under left by default
                                leaf = self._new_node(letter_e)
                                leaf.value = letter_e
                                cur.left = leaf
                                return [leaf.id]
                        b = existing_code[start_idx]
                        if b == '0':
                            if cur.left is None:
                                leaf = self._new_node(existing_letter)
                                leaf.value = existing_letter
                                cur.left = leaf
                                return [cur.id, leaf.id]
                            else:
                                cur = cur.left
                                res = reinstate(cur, start_idx + 1, letter_e)
                                return [cur.id] + res if res else [cur.id]
                        else:
                            if cur.right is None:
                                leaf = self._new_node(existing_letter)
                                leaf.value = existing_letter
                                cur.right = leaf
                                return [cur.id, leaf.id]
                            else:
                                cur = cur.right
                                res = reinstate(cur, start_idx + 1, letter_e)
                                return [cur.id] + res if res else [cur.id]

                    # insert existing
                    _ = reinstate(aux, idx + 1, existing_letter)
                    # now insert the new letter into aux using same logic
                    # reuse insert_from behavior by calling insert_from on aux
                    inserted = insert_from(aux, idx + 1, letter)
                    return [aux.id] + inserted
                else:
                    # child is aux/internal
                    res = insert_from(child, idx + 1, letter)
                    return [child.id] + res
            else:
                # bit == '1'
                child = node.right
                if child is None:
                    leaf = self._new_node(letter)
                    leaf.value = letter
                    node.right = leaf
                    return [leaf.id]
                if child.value is not None:
                    existing_letter = child.value
                    aux = self._new_node(None)
                    node.right = aux
                    existing_code = self.CODE_TABLE[existing_letter]

                    def reinstate(cur: ResidueNode, start_idx: int, letter_e: str):
                        if start_idx >= len(existing_code):
                            if cur.value is None and cur.left is None and cur.right is None:
                                cur.value = letter_e
                                return [cur.id]
                            else:
                                leaf = self._new_node(letter_e)
                                leaf.value = letter_e
                                cur.left = leaf
                                return [leaf.id]
                        b = existing_code[start_idx]
                        if b == '0':
                            if cur.left is None:
                                leaf = self._new_node(existing_letter)
                                leaf.value = existing_letter
                                cur.left = leaf
                                return [cur.id, leaf.id]
                            else:
                                cur = cur.left
                                res = reinstate(cur, start_idx + 1, letter_e)
                                return [cur.id] + res if res else [cur.id]
                        else:
                            if cur.right is None:
                                leaf = self._new_node(existing_letter)
                                leaf.value = existing_letter
                                cur.right = leaf
                                return [cur.id, leaf.id]
                            else:
                                cur = cur.right
                                res = reinstate(cur, start_idx + 1, letter_e)
                                return [cur.id] + res if res else [cur.id]

                    _ = reinstate(aux, idx + 1, existing_letter)
                    inserted = insert_from(aux, idx + 1, letter)
                    return [aux.id] + inserted
                else:
                    res = insert_from(child, idx + 1, letter)
                    return [child.id] + res

        result = insert_from(self.root, 0, letter)
        self._insertion_order.append(letter)
        return [self.root.id] + result

    def find(self, letter: str) -> List[int]:
        letter = letter.upper()
        path: List[ResidueNode] = []

        def dfs(node: Optional[ResidueNode]) -> bool:
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
        self._insertion_order = [x for x in self._insertion_order if x != letter]
        self._rebuild()
        return True

    def _rebuild(self):
        # recreate empty root
        self._next_id = 1
        self.root = self._new_node(None)
        self._insertion_order, order = [], list(self._insertion_order)
        for letter in order:
            self.insert(letter)

    def to_list(self) -> List[Tuple[int, Optional[str], Optional[int], Optional[int]]]:
        res: List[Tuple[int, Optional[str], Optional[int], Optional[int]]] = []

        def dfs(node: Optional[ResidueNode]):
            if node is None:
                return
            left_id = node.left.id if node.left else None
            right_id = node.right.id if node.right else None
            res.append((node.id, node.value, left_id, right_id))
            dfs(node.left)
            dfs(node.right)

        dfs(self.root)
        return res
