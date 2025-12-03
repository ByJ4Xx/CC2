from __future__ import annotations

from typing import List, Dict, Any


class DynamicTotalArray:
    """Dynamic array with total expansion behavior.

    columns: number of columns (cubetas)
    records: number of records per column (rows)
    do_threshold: expansion threshold (percent, 65-85)
    do_reduction_threshold: reduction threshold (percent, 85-110)
    """

    def __init__(self, columns: int = 2, records: int = 2, do_threshold: int = 75, do_reduction_threshold: int = 85):
        if columns < 1 or records < 1:
            raise ValueError("columns and records must be >= 1")
        # Validate DO ranges: expansion DO in [65,85], reduction DO in [85,110]
        do_threshold = int(do_threshold)
        do_reduction_threshold = int(do_reduction_threshold)
        if not (65 <= do_threshold <= 85):
            raise ValueError("DO de expansión debe estar entre 65 y 85")
        if not (85 <= do_reduction_threshold <= 110):
            raise ValueError("DO de reducción debe estar entre 85 y 110")
        if do_reduction_threshold <= do_threshold:
            raise ValueError("DO de reducción debe ser mayor que DO de expansión")

        self.columns = int(columns)
        self.records = int(records)
        self.do_threshold = do_threshold
        self.do_reduction_threshold = do_reduction_threshold
        # insertion_order stores ALL inserted keys in chronological order (including collisions)
        self.insertion_order = []
        # columns lists (each column holds keys that currently belong to the structure)
        self.cols = [[] for _ in range(self.columns)]

    def clear(self):
        self.insertion_order = []
        self.cols = [[] for _ in range(self.columns)]

    def _rebuild(self):
        """Rebuild active columns from the full insertion order.

        Keys that cannot fit into their target column (because the column
        already has 'records' items) will remain as collisions (i.e., not
        included in self.cols). This preserves insertion order and ensures
        collisions don't increase DO until expansion allows them to be placed.
        """
        self.cols = [[] for _ in range(self.columns)]
        for k in self.insertion_order:
            col = k % self.columns
            if len(self.cols[col]) < self.records:
                self.cols[col].append(k)

    def insert(self, key: int) -> Dict[str, Any]:
        key = int(key)
        # disallow duplicates globally
        if key in self.insertion_order:
            raise ValueError("Clave duplicada no permitida")
        # record insertion order (keeps collisions too)
        self.insertion_order.append(key)
        col = key % self.columns
        inserted = False
        # try to place into the target column if there's room
        if len(self.cols[col]) < self.records:
            self.cols[col].append(key)
            inserted = True

        # occupied is the number of items actually in the structure (not collisions)
        occupied = sum(len(c) for c in self.cols)
        total_capacity = self.columns * self.records
        
        # DO para expansión: elementos / (columnas × registros) × 100
        do_expansion = (occupied / total_capacity) * 100 if total_capacity > 0 else 0.0
        
        # DO para reducción: elementos / columnas × 100
        do_reduction = (occupied / self.columns) * 100 if self.columns > 0 else 0.0

        # Expansión necesaria si DO_expansión >= umbral_expansión
        expansion_needed = do_expansion >= self.do_threshold

        return {
            "expansion_needed": expansion_needed, 
            "do_expansion": do_expansion,
            "do_reduction": do_reduction,
            "occupied": occupied, 
            "columns": self.columns, 
            "collision": not inserted
        }

    def expand(self) -> Dict[str, Any]:
        """Perform the expansion (double columns) and rebuild from insertion_order."""
        self.columns *= 2
        self._rebuild()
        occupied = sum(len(c) for c in self.cols)
        total_capacity = self.columns * self.records
        do_expansion = (occupied / total_capacity) * 100 if total_capacity > 0 else 0.0
        do_reduction = (occupied / self.columns) * 100 if self.columns > 0 else 0.0
        return {
            "expanded": True, 
            "columns": self.columns, 
            "do_expansion": do_expansion,
            "do_reduction": do_reduction,
            "occupied": occupied
        }

    def expand_partial(self) -> Dict[str, Any]:
        """Increase columns by half (columns += columns//2) and rebuild.

        Requires columns to be even to have an exact half; if odd, integer division used.
        """
        add = max(1, self.columns // 2)
        self.columns = self.columns + add
        self._rebuild()
        occupied = sum(len(c) for c in self.cols)
        total_capacity = self.columns * self.records
        do_expansion = (occupied / total_capacity) * 100 if total_capacity > 0 else 0.0
        do_reduction = (occupied / self.columns) * 100 if self.columns > 0 else 0.0
        return {
            "expanded": True, 
            "columns": self.columns, 
            "do_expansion": do_expansion,
            "do_reduction": do_reduction,
            "occupied": occupied
        }

    def find(self, key: int) -> Dict[str, Any]:
        key = int(key)
        # Only search within active columns (collisions are not searchable)
        col = key % self.columns
        positions = [i for i, v in enumerate(self.cols[col]) if v == key]
        if positions:
            return {"found": True, "column": col, "positions": positions}
        return {"found": False}

    def delete(self, key: int) -> Dict[str, Any]:
        key = int(key)
        # deletion only allowed for keys currently in structure (not collisions)
        col = key % self.columns
        if key not in self.cols[col]:
            raise ValueError("La clave no existe en la estructura (puede estar en colisión)")

        # remove first occurrence from both cols and insertion_order
        removed = False
        # remove from cols
        for i, v in enumerate(self.cols[col]):
            if v == key:
                del self.cols[col][i]
                removed = True
                break

        # remove first occurrence in insertion_order
        for i, v in enumerate(self.insertion_order):
            if v == key:
                del self.insertion_order[i]
                break

        # after deletion, try to rebuild to compact structure (some collisions may now fit)
        self._rebuild()

        occupied = sum(len(c) for c in self.cols)
        total_capacity = self.columns * self.records
        
        # DO para expansión
        do_expansion = (occupied / total_capacity) * 100 if total_capacity > 0 else 0.0
        
        # DO para reducción
        do_reduction = (occupied / self.columns) * 100 if self.columns > 0 else 0.0

        # Reducir si DO_reducción < DO_reducción_umbral Y columnas > 1
        should_reduce = False
        if do_reduction < self.do_reduction_threshold and self.columns > 1:
            should_reduce = True

        return {
            "removed": removed, 
            "should_reduce": should_reduce, 
            "do_expansion": do_expansion,
            "do_reduction": do_reduction,
            "occupied": occupied, 
            "columns": self.columns
        }

    def reduce(self) -> Dict[str, Any]:
        """Perform reduction (halve columns) and rebuild.

        Returns information about the new state.
        """
        self.columns = max(1, self.columns // 2)
        self._rebuild()
        occupied = sum(len(c) for c in self.cols)
        total_capacity = self.columns * self.records
        do_expansion = (occupied / total_capacity) * 100 if total_capacity > 0 else 0.0
        do_reduction = (occupied / self.columns) * 100 if self.columns > 0 else 0.0
        return {
            "reduced": True, 
            "columns": self.columns, 
            "do_expansion": do_expansion,
            "do_reduction": do_reduction,
            "occupied": occupied
        }

    def current_do_expansion(self) -> float:
        """Return current DO for expansion (occupied / total_capacity * 100)."""
        occupied = sum(len(c) for c in self.cols)
        total_capacity = self.columns * self.records
        return (occupied / total_capacity) * 100 if total_capacity > 0 else 0.0

    def current_do_reduction(self) -> float:
        """Return current DO for reduction (occupied / columns * 100)."""
        occupied = sum(len(c) for c in self.cols)
        return (occupied / self.columns) * 100 if self.columns > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tipo": "dynamic_total",
            "columns": self.columns,
            "records": self.records,
            "do_threshold": self.do_threshold,
            "do_reduction_threshold": self.do_reduction_threshold,
            "insertion_order": list(self.insertion_order),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DynamicTotalArray":
        if not isinstance(data, dict) or data.get("tipo") != "dynamic_total":
            raise ValueError("Archivo incompatible: 'tipo' debe ser 'dynamic_total'")
        cols = int(data.get("columns", 2))
        rec = int(data.get("records", 2))
        do = int(data.get("do_threshold", 80))
        dore = int(data.get("do_reduction_threshold", 75))
        arr = cls(cols, rec, do, dore)
        for k in data.get("insertion_order", []):
            arr.insertion_order.append(int(k))
        arr._rebuild()
        return arr

    def snapshot(self) -> Dict[str, Any]:
        # compute collisions per target column (keys in insertion_order but not in cols)
        collisions: List[List[int]] = [[] for _ in range(self.columns)]
        cols_set = [list(c) for c in self.cols]
        # create a flat set membership check per column
        for k in self.insertion_order:
            col = k % self.columns
            if k not in self.cols[col]:
                collisions[col].append(k)

        return {"cols": [list(c) for c in self.cols], "collisions": collisions, "columns": self.columns, "records": self.records}
