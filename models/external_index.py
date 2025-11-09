"""External indexing structures (logic only).

Provides:
- MainFile: stores records, computes bfr and blocks
- PrimaryIndex: sparse index (one entry per main-file block) mapping first-key -> block
- SecondaryIndex: dense index (one entry per record) mapping key -> record_address
- MultiLevelIndex: builds extra index levels on top of a base index until a single-block level

Assumptions / decisions made:
- Records are simple integer-like keys (comparable). Each record is stored as a key (payload optional).
- No duplicates are allowed by default (Sin repetición).
- By default inserts must be in non-decreasing order (En orden). This can be disabled by passing ordered=False.
- Index record length (lri) is fixed at 15 bytes as described.
- Binary searches are used on index levels. For primary (sparse) we use the largest index key <= target to locate the block, then binary search inside the block.

This module focuses on logic and is GUI-agnostic. It exposes methods to build indexes and perform searches.
"""

from __future__ import annotations

import math
from bisect import bisect_left, bisect_right
from typing import Any, List, Optional, Tuple, Dict


class MainFile:
    """Represents the main data file split into blocks.

    Attributes:
        r: desired number of records (capacity)
        B: block size in bytes
        lr: record length in bytes
        bfr: records per block (floor(B/lr))
        b: number of blocks (ceil(r/bfr))
        records: list of keys (insertion order)
        ordered: if True, insertions must be non-decreasing (En orden)
    """

    def __init__(self, r: int, B: int, lr: int, ordered: bool = True):
        if r <= 0:
            raise ValueError("r must be positive")
        if B <= 0 or lr <= 0:
            raise ValueError("B and lr must be positive")

        self.r = int(r)
        self.B = int(B)
        self.lr = int(lr)
        self.bfr = self.B // self.lr
        if self.bfr <= 0:
            raise ValueError("Block factor bfr = floor(B/lr) evaluates to 0; increase B or reduce lr")

        # number of blocks required to store r records
        self.b = math.ceil(self.r / self.bfr)
        self.records: List[Any] = []  # store just the key (payload optional)
        self.ordered = bool(ordered)

    def insert(self, key: Any) -> None:
        """Insert a key into the main file.

        Raises ValueError on duplicates or if ordering requirement is violated.
        """
        if key in self.records:
            raise ValueError("duplicate keys are not allowed")
        if self.ordered and self.records and key < self.records[-1]:
            raise ValueError("insertion order violated: keys must be non-decreasing when ordered=True")
        if len(self.records) >= self.r:
            raise OverflowError("cannot insert: main file at capacity r")
        self.records.append(key)

    def delete(self, key: Any) -> bool:
        """Delete a key from the main file. Returns True if deleted, False if not found."""
        try:
            self.records.remove(key)
            return True
        except ValueError:
            return False

    def num_records(self) -> int:
        return len(self.records)

    def get_block_for_record_index(self, rec_index: int) -> int:
        return rec_index // self.bfr

    def get_block(self, block_num: int) -> List[Any]:
        if block_num < 0 or block_num >= self.b:
            raise IndexError("block number out of range")
        start = block_num * self.bfr
        end = min(start + self.bfr, len(self.records))
        return self.records[start:end]

    def find_in_block(self, block_num: int, key: Any) -> Optional[int]:
        """Binary search for key inside specified block. Returns record index within main file or None."""
        block = self.get_block(block_num)
        if not block:
            return None
        i = bisect_left(block, key)
        if i < len(block) and block[i] == key:
            # convert local index to global record index
            global_index = block_num * self.bfr + i
            return global_index
        return None


class PrimaryIndex:
    """Sparse primary index: one entry per main-file block, pointing to that block's first key.

    Index record length (lri) is fixed to 15 bytes. bfri = floor(B / lri)
    bi = ceil(b / bfri)
    """

    LRI = 15

    def __init__(self, main: MainFile):
        self.main = main
        self.lri = self.LRI
        self.bfri = main.B // self.lri
        if self.bfri <= 0:
            raise ValueError("bfri (index block factor) is zero: increase B or lri")
        self.entries: List[Tuple[Any, int]] = []  # list of (first_key_in_block, block_num)
        self.bi = 0

    def build(self) -> None:
        """Build the sparse index from the main file.

        Creates an entry for every main-file block that has at least one record. The entry key
        is the first key in the block and the pointer is the block number.
        """
        self.entries = []
        # number of main blocks is main.b; iterate over actual existing blocks
        for block_num in range(self.main.b):
            block = self.main.get_block(block_num)
            if block:
                self.entries.append((block[0], block_num))
        # number of index blocks
        num_index_entries = len(self.entries)
        self.bi = math.ceil(num_index_entries / self.bfri) if num_index_entries > 0 else 0

    def search(self, key: Any) -> Dict[str, Any]:
        """Search for key using the primary index.

        Returns dict with:
            found: bool
            record_index: optional global record index in main file
            block_scanned: block number in main file
            index_entry: index entry used (key, block_num)
        """
        if not self.entries:
            return {"found": False}

        # find rightmost index entry with entry_key <= key
        keys = [e[0] for e in self.entries]
        i = bisect_right(keys, key) - 1
        if i < 0:
            # key is smaller than first index key -> we scan first block
            index_entry = self.entries[0]
        else:
            index_entry = self.entries[i]

        _, block_num = index_entry
        rec_index = self.main.find_in_block(block_num, key)
        return {
            "found": rec_index is not None,
            "record_index": rec_index,
            "block_scanned": block_num,
            "index_entry": index_entry,
        }

    def snapshot(self) -> Dict[str, Any]:
        return {"entries": list(self.entries), "bfri": self.bfri, "bi": self.bi}


class SecondaryIndex:
    """Dense secondary index: one index entry per record mapping key -> record_index.

    For simplicity we assume the secondary key is the record key itself (unique). The index
    is dense (r entries). bfri = floor(B/lri) with lri fixed at 15 (same as primary).
    """

    LRI = 15

    def __init__(self, main: MainFile):
        self.main = main
        self.lri = self.LRI
        self.bfri = main.B // self.lri
        if self.bfri <= 0:
            raise ValueError("bfri (index block factor) is zero: increase B or lri")
        self.entries: List[Tuple[Any, int]] = []  # list of (key, record_index)
        self.bi = 0

    def build(self) -> None:
        self.entries = [(k, i) for i, k in enumerate(self.main.records)]
        num_entries = len(self.entries)
        self.bi = math.ceil(num_entries / self.bfri) if num_entries > 0 else 0

    def search(self, key: Any) -> Dict[str, Any]:
        """Binary search exact match on the dense index. Returns record_index if found."""
        if not self.entries:
            return {"found": False}
        keys = [e[0] for e in self.entries]
        i = bisect_left(keys, key)
        if i < len(keys) and keys[i] == key:
            return {"found": True, "record_index": self.entries[i][1], "index_pos": i}
        return {"found": False}

    def snapshot(self) -> Dict[str, Any]:
        return {"entries": list(self.entries), "bfri": self.bfri, "bi": self.bi}


class MultiLevelIndex:
    """Builds multiple index levels on top of a base index until the number of index blocks is 1.

    The top level indexes the level below using the same record size (lri=15), and bfri computed
    the same way. Each level stores entries of (key, pointer_block_num) where pointer_block_num
    points to a block in the lower level (or the main file for the leaf).
    """

    def __init__(self, base_index: Any):
        self.base_index = base_index
        # bfri is taken from base index
        self.lri = base_index.lri
        self.bfri = base_index.bfri
        # levels list: level 0 is the base_index entries represented as (key, pointer)
        # higher levels are built on top of the previous level
        self.levels: List[List[Tuple[Any, int]]] = []

    def build(self) -> None:
        # start with base index entries as list of (key, pointer_block)
        if isinstance(self.base_index, PrimaryIndex):
            base_entries = list(self.base_index.entries)
        elif isinstance(self.base_index, SecondaryIndex):
            # map (key, record_index) to pointer being record_index // bfr (block within main)
            base_entries = [(k, idx // self.base_index.main.bfr) for k, idx in self.base_index.entries]
        else:
            raise TypeError("unsupported base index type for multilevel construction")

        if not base_entries:
            self.levels = []
            return

        self.levels = [base_entries]

        # iteratively build higher level: always create the next-level index that points to
        # blocks of the previous level; stop after creating a level that fits in a single block.
        while True:
            prev = self.levels[-1]
            num_prev_entries = len(prev)
            num_blocks_prev = max(1, math.ceil(num_prev_entries / self.bfri))

            # build next level entries: one entry per block in prev, pointing to that block
            next_entries: List[Tuple[Any, int]] = []
            for block_num in range(num_blocks_prev):
                start = block_num * self.bfri
                if start < num_prev_entries:
                    entry_key = prev[start][0]
                else:
                    # reuse last key as placeholder so the index remains ordered
                    entry_key = prev[-1][0]
                next_entries.append((entry_key, block_num))

            self.levels.append(next_entries)

            # if this newly created level fits in one block, stop
            if num_blocks_prev <= 1:
                break

    def search(self, key: Any, main_file: MainFile) -> Dict[str, Any]:
        """Search through multilevel index down to main file. Returns dict with details.

        Algorithm: start at highest level, binary-search keys to find pointer (block_num) into
        the next-lower level, then repeat until reaching base-level where pointer points to
        main-file block(s). Finally search inside the main-file block.
        """
        if not self.levels:
            return {"found": False}

        current_level_idx = len(self.levels) - 1
        pointer_block = None
        path = []

        while current_level_idx >= 0:
            level = self.levels[current_level_idx]
            keys = [e[0] for e in level]
            i = bisect_right(keys, key) - 1
            if i < 0:
                entry = level[0]
            else:
                entry = level[i]
            path.append((current_level_idx, entry))
            pointer_block = entry[1]
            # move to lower level (one down)
            current_level_idx -= 1

        # now pointer_block identifies a block in the base-level that points to main-file blocks
        # Depending on base_index type, pointer interpretation differs:
        if isinstance(self.base_index, PrimaryIndex):
            # pointer_block is the main-file block number
            rec_index = main_file.find_in_block(pointer_block, key)
            return {"found": rec_index is not None, "record_index": rec_index, "path": path}
        elif isinstance(self.base_index, SecondaryIndex):
            # base level entries are mapped to main-file blocks as (key, record_index // bfr)
            # pointer_block is a block number in main file; search inside
            rec_index = main_file.find_in_block(pointer_block, key)
            return {"found": rec_index is not None, "record_index": rec_index, "path": path}
        else:
            return {"found": False}

    def snapshot(self) -> Dict[str, Any]:
        return {"levels": [list(l) for l in self.levels], "bfri": self.bfri}


if __name__ == "__main__":
    # simple demo
    mf = MainFile(r=50, B=4096, lr=100, ordered=True)
    for k in range(1, 31):
        mf.insert(k)

    pidx = PrimaryIndex(mf)
    pidx.build()
    print("Primary index entries:", len(pidx.entries), "bfri:", pidx.bfri, "bi:", pidx.bi)

    sidx = SecondaryIndex(mf)
    sidx.build()
    print("Secondary index entries:", len(sidx.entries), "bfri:", sidx.bfri, "bi:", sidx.bi)

    m = MultiLevelIndex(pidx)
    m.build()
    print("Multilevel levels:", len(m.levels))
