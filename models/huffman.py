from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple
import heapq


@dataclass
class HuffNode:
    id: int
    freq: int
    char: Optional[str] = None
    left: Optional['HuffNode'] = None
    right: Optional['HuffNode'] = None


class HuffmanTree:
    def __init__(self):
        self._next_id = 1
        self.root: Optional[HuffNode] = None
        self.codes: Dict[str, str] = {}
        self._text = ""

    def clear(self):
        self._next_id = 1
        self.root = None
        self.codes = {}
        self._text = ""

    def _new_node(self, freq: int, char: Optional[str] = None) -> HuffNode:
        node = HuffNode(self._next_id, freq, char)
        self._next_id += 1
        return node

    def build_from_text(self, text: str):
        """Build the Huffman tree from the given text (letters only)."""
        text = text.upper()
        if not text:
            raise ValueError("Texto vacío")
        # frequency table
        freq: Dict[str, int] = {}
        for ch in text:
            freq[ch] = freq.get(ch, 0) + 1

        # priority queue of tuples (freq, id, node)
        pq: List[Tuple[int, int, HuffNode]] = []
        for ch, f in freq.items():
            n = self._new_node(f, ch)
            heapq.heappush(pq, (f, n.id, n))

        if not pq:
            raise ValueError("No hay caracteres para construir el árbol")

        # special case: single unique char
        if len(pq) == 1:
            f, _id, node = heapq.heappop(pq)
            self.root = node
            self.codes = {node.char: "0"}
            self._text = text
            return self.codes

        while len(pq) > 1:
            f1, id1, n1 = heapq.heappop(pq)
            f2, id2, n2 = heapq.heappop(pq)
            parent = self._new_node(f1 + f2, None)
            parent.left = n1
            parent.right = n2
            heapq.heappush(pq, (parent.freq, parent.id, parent))

        _, _, root = heapq.heappop(pq)
        self.root = root

        # generate codes
        self.codes = {}

        def gen_codes(node: Optional[HuffNode], prefix: str):
            if node is None:
                return
            if node.char is not None:
                # leaf
                self.codes[node.char] = prefix or "0"
                return
            gen_codes(node.left, prefix + "0")
            gen_codes(node.right, prefix + "1")

        gen_codes(self.root, "")
        self._text = text
        return self.codes

    def to_list(self) -> List[Tuple[int, Optional[str], Optional[int], Optional[int]]]:
        """Return list of nodes for visualization: (id, label, left_id, right_id)
        label: for leaves -> 'A\n3' (char and freq), for internal -> str(freq)
        """
        res: List[Tuple[int, Optional[str], Optional[int], Optional[int]]] = []

        def dfs(node: Optional[HuffNode]):
            if node is None:
                return
            left_id = node.left.id if node.left else None
            right_id = node.right.id if node.right else None
            if node.char is not None:
                label = f"{node.char}\n{node.freq}"
            else:
                label = str(node.freq)
            res.append((node.id, label, left_id, right_id))
            if node.left:
                dfs(node.left)
            if node.right:
                dfs(node.right)

        dfs(self.root)
        return res

    def to_dict(self) -> dict:
        return {"tipo": "huffman", "text": self._text}

    @classmethod
    def from_dict(cls, data: dict) -> "HuffmanTree":
        if not isinstance(data, dict) or data.get("tipo") != "huffman":
            raise ValueError("Archivo incompatible: 'tipo' debe ser 'huffman'")
        text = data.get("text", "")
        t = cls()
        if text:
            t.build_from_text(text)
        return t

    def find_code(self, ch: str) -> Optional[str]:
        return self.codes.get(ch.upper())

    def find(self, letter: str) -> List[int]:
        """Return path of node ids from root to the leaf for letter (uppercase)."""
        letter = letter.upper()
        path: List[HuffNode] = []

        def dfs(node: Optional[HuffNode]) -> bool:
            if node is None:
                return False
            path.append(node)
            if node.char == letter:
                return True
            if node.left and dfs(node.left):
                return True
            if node.right and dfs(node.right):
                return True
            path.pop()
            return False

        if self.root and dfs(self.root):
            return [n.id for n in path]
        return []

    def delete(self, letter: str) -> bool:
        """Remove all occurrences of letter from the original text and rebuild tree.
        Returns True if deleted; raises ValueError if letter not present.
        """
        if not self._text:
            raise ValueError("Árbol vacío")
        letter = letter.upper()
        if letter not in self._text:
            raise ValueError("La letra no existe en el árbol")
        # remove all occurrences
        new_text = ''.join(ch for ch in self._text if ch != letter)
        self.clear()
        if new_text:
            self.build_from_text(new_text)
        return True
