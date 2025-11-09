import json
import math
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from typing import Optional

from models.external_index import MainFile, PrimaryIndex, SecondaryIndex, MultiLevelIndex


class ExternalIndexView(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # model
        self.main: Optional[MainFile] = None
        self.index = None
        self.multilevel = None

        # UI state
        self.r_var = tk.StringVar(value="1000")
        self.B_var = tk.StringVar(value="4096")
        self.lr_var = tk.StringVar(value="64")
        self.insert_var = tk.StringVar()
        self.type_var = tk.StringVar(value="Primario")
        self.option_map = {"Primario": "primary", "Secundario": "secondary", "Multinivel Primario": "multi_primary", "Multinivel Secundario": "multi_secondary"}

        # build UI
        self._build_controls()
        self._build_canvas()

        self.status_var = tk.StringVar(value="Estructura no creada")
        ctk.CTkLabel(self, textvariable=self.status_var, anchor="w").pack(side="top", fill="x", padx=8)

    def _build_controls(self):
        cfg = ctk.CTkFrame(self)
        cfg.pack(side="top", fill="x", padx=8, pady=8)

        ctk.CTkLabel(cfg, text="r:").pack(side="left", padx=4)
        ctk.CTkEntry(cfg, textvariable=self.r_var, width=80).pack(side="left", padx=4)
        ctk.CTkLabel(cfg, text="B:").pack(side="left", padx=4)
        ctk.CTkEntry(cfg, textvariable=self.B_var, width=80).pack(side="left", padx=4)
        ctk.CTkLabel(cfg, text="lr:").pack(side="left", padx=4)
        ctk.CTkEntry(cfg, textvariable=self.lr_var, width=80).pack(side="left", padx=4)

        self.type_menu = ctk.CTkOptionMenu(cfg, values=list(self.option_map.keys()), variable=self.type_var)
        self.type_menu.pack(side="left", padx=8)

        ctk.CTkButton(cfg, text="Crear", command=self.on_create).pack(side="left", padx=8)
        ctk.CTkButton(cfg, text="Borrar", command=self.on_clear).pack(side="left", padx=8)

        ops = ctk.CTkFrame(self)
        ops.pack(side="top", fill="x", padx=8, pady=4)
        ctk.CTkLabel(ops, text="Clave:").pack(side="left", padx=4)
        ctk.CTkEntry(ops, textvariable=self.insert_var, width=160).pack(side="left", padx=4)
        ctk.CTkButton(ops, text="Insertar", command=self._do_insert).pack(side="left", padx=6)
        ctk.CTkButton(ops, text="Eliminar", command=self._do_delete).pack(side="left", padx=6)
        ctk.CTkButton(ops, text="Buscar", command=self._do_search).pack(side="left", padx=6)
        ctk.CTkButton(ops, text="Guardar", command=self.on_save).pack(side="left", padx=6)
        ctk.CTkButton(ops, text="Abrir", command=self.on_load).pack(side="left", padx=6)

    def _build_canvas(self):
        canvas_frame = ctk.CTkFrame(self)
        canvas_frame.pack(side="top", fill="both", expand=True, padx=8, pady=8)

        inner = tk.Frame(canvas_frame)
        inner.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(inner, bg="#111111", highlightthickness=0)
        self.vscroll = tk.Scrollbar(inner, orient="vertical", command=self.canvas.yview)
        self.hscroll = tk.Scrollbar(inner, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vscroll.set, xscrollcommand=self.hscroll.set)
        self.vscroll.pack(side="right", fill="y")
        self.hscroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mousewheel)

    def _on_mousewheel(self, event):
        try:
            delta = int(-1 * (event.delta / 120))
            self.canvas.yview_scroll(delta, "units")
        except Exception:
            pass

    def _on_shift_mousewheel(self, event):
        try:
            delta = int(-1 * (event.delta / 120))
            self.canvas.xview_scroll(delta, "units")
        except Exception:
            pass

    def on_create(self):
        try:
            r = int(self.r_var.get())
            B = int(self.B_var.get())
            lr = int(self.lr_var.get())
        except ValueError:
            messagebox.showerror("Error", "r, B y lr deben ser enteros positivos")
            return

        if self.main is not None:
            messagebox.showinfo("Info", "Debe borrar la estructura actual antes de crear una nueva")
            return

        try:
            self.main = MainFile(r=r, B=B, lr=lr, ordered=True)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.main = None
            return

        sel = self.option_map.get(self.type_var.get(), "primary")
        self.index = None
        self.multilevel = None

        if sel == "primary":
            self.index = PrimaryIndex(self.main)
            self.index.build()
        elif sel == "secondary":
            self.index = SecondaryIndex(self.main)
            self.index.build()
        elif sel == "multi_primary":
            base = PrimaryIndex(self.main)
            base.build()
            self.multilevel = MultiLevelIndex(base)
            self.multilevel.build()
            self.index = base
        elif sel == "multi_secondary":
            base = SecondaryIndex(self.main)
            base.build()
            self.multilevel = MultiLevelIndex(base)
            self.multilevel.build()
            self.index = base

        self.status_var.set(f"Estructura creada: {sel}")
        self._draw_structure()

    def _do_search(self):
        if self.main is None:
            messagebox.showinfo("Info", "Cree la estructura primero")
            return
        raw = self.insert_var.get()
        if not raw:
            return
        try:
            key = int(raw)
        except Exception:
            key = raw
        result = {"found": False}
        path = None
        if self.multilevel:
            result = self.multilevel.search(key, self.main)
            path = result.get("path")
        elif isinstance(self.index, PrimaryIndex):
            result = self.index.search(key)
        elif isinstance(self.index, SecondaryIndex):
            result = self.index.search(key)

        self._draw_structure(highlight=result.get("record_index"), path=path)
        if result.get("found"):
            messagebox.showinfo("Resultado", f"Encontrado en índice de registro {result.get('record_index')}")
        else:
            messagebox.showinfo("Resultado", "No encontrado")

    def on_save(self):
        if self.main is None:
            messagebox.showinfo("Info", "No hay estructura para guardar")
            return
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if not path:
            return
        data = {
            "params": {"r": self.main.r, "B": self.main.B, "lr": self.main.lr},
            "records": list(self.main.records),
            "index_type": self.option_map.get(self.type_var.get(), "primary"),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        self.status_var.set(f"Estructura guardada en {path}")

    def on_load(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not path:
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        params = data.get("params") or {}
        records = data.get("records") or []
        itype = data.get("index_type", "primary")

        if self.main is not None:
            messagebox.showinfo("Info", "Borre la estructura actual antes de cargar otra")
            return

        try:
            self.main = MainFile(r=params.get("r", len(records)), B=params.get("B", 4096), lr=params.get("lr", 64), ordered=True)
        except Exception as e:
            messagebox.showerror("Error al cargar", str(e))
            return

        for rec in records:
            try:
                key = int(rec)
            except Exception:
                key = rec
            self.main.insert(key)

        self.type_var.set(next((k for k, v in self.option_map.items() if v == itype), list(self.option_map.keys())[0]))

        if itype == "primary":
            self.index = PrimaryIndex(self.main)
            self.index.build()
        elif itype == "secondary":
            self.index = SecondaryIndex(self.main)
            self.index.build()
        elif itype == "multi_primary":
            base = PrimaryIndex(self.main)
            base.build()
            self.multilevel = MultiLevelIndex(base)
            self.multilevel.build()
            self.index = base
        elif itype == "multi_secondary":
            base = SecondaryIndex(self.main)
            base.build()
            self.multilevel = MultiLevelIndex(base)
            self.multilevel.build()
            self.index = base

        self.status_var.set(f"Estructura cargada desde {path}")
        self._draw_structure()

    def _do_insert(self):
        if self.main is None:
            messagebox.showinfo("Info", "Cree la estructura primero")
            return
        raw = self.insert_var.get()
        if not raw:
            return
        try:
            key = int(raw)
        except Exception:
            key = raw
        try:
            self.main.insert(key)
        except Exception as e:
            messagebox.showerror("Insert error", str(e))
            return
        if isinstance(self.index, PrimaryIndex) or isinstance(self.index, SecondaryIndex):
            self.index.build()
        if self.multilevel:
            self.multilevel.build()
        self.insert_var.set("")
        self._draw_structure()

    def _do_delete(self):
        if self.main is None:
            messagebox.showinfo("Info", "Cree la estructura primero")
            return
        raw = self.insert_var.get()
        if not raw:
            return
        try:
            key = int(raw)
        except Exception:
            key = raw
        deleted = self.main.delete(key)
        if not deleted:
            messagebox.showinfo("Eliminar", "Clave no encontrada")
            return
        if isinstance(self.index, PrimaryIndex) or isinstance(self.index, SecondaryIndex):
            self.index.build()
        if self.multilevel:
            self.multilevel.build()
        self.insert_var.set("")
        self._draw_structure()

    def on_clear(self):
        self.main = None
        self.index = None
        self.multilevel = None
        self.canvas.delete("all")
        self.status_var.set("Estructura no creada")

    def _draw_structure(self, highlight: int | None = None, path=None):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 400

        if not self.main:
            self.canvas.create_text(w / 2, h / 2, text="Sin estructura", fill="white", font=("Arial", 14))
            return

        margin = 20
        main_w = int(w * 0.5)
        main_h = h - 2 * margin
        main_x = w - main_w - margin
        main_y = margin

        b = max(1, self.main.b)
        rows = b
        block_h = max(24, main_h // rows)
        block_w = main_w - 2 * margin

        self.canvas.create_text(main_x + block_w / 2 + margin, main_y - 10, text="Estructura principal", fill="white")

        for i in range(b):
            y0 = main_y + i * block_h
            y1 = y0 + block_h - 4
            x0 = main_x + margin
            x1 = x0 + block_w
            color = "#1E3A8A" if highlight is None or highlight is None else "#083344"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#222222", outline="#AAAAAA")
            block = self.main.get_block(i)
            label = f"B{i}: " + ",".join(str(k) for k in block[:4])
            self.canvas.create_text(x0 + 6, y0 + (block_h // 2), text=label, anchor="w", fill="white", font=("Arial", 9))

        # Index area left of main
        margin = 20
        idx_area_x0 = margin
        idx_area_x1 = main_x - 2 * margin
        idx_area_w = max(200, idx_area_x1 - idx_area_x0)
        y_start = main_y

        if self.multilevel:
            bfri = getattr(self.multilevel, "bfri", None)
            base_index = self.multilevel.base_index
            if isinstance(base_index, PrimaryIndex):
                bi = math.ceil(self.main.b / bfri) if bfri and bfri > 0 else 1
            elif isinstance(base_index, SecondaryIndex):
                bi = math.ceil(self.main.r / bfri) if bfri and bfri > 0 else 1
            else:
                bi = 1

            levels_counts = [max(1, bi)]
            while True:
                prev = levels_counts[-1]
                nxt = math.ceil(prev / bfri) if bfri and bfri > 0 else 1
                levels_counts.append(max(1, nxt))
                if nxt <= 1:
                    break

            levels_entries = list(self.multilevel.levels)
            while len(levels_entries) < len(levels_counts):
                levels_entries.append([])

            num_columns = len(levels_counts)
            col_w = idx_area_w / num_columns

            for col_idx in range(num_columns - 1, -1, -1):
                level_idx = col_idx
                level_entries = levels_entries[level_idx] if level_idx < len(levels_entries) else []
                num_blocks = levels_counts[level_idx]
                label = f"L{level_idx + 1}"
                col_x = idx_area_x0 + (num_columns - 1 - col_idx) * col_w
                # determine how many blocks the next lower level has (what this block points to)
                if level_idx > 0:
                    lower_total_blocks = levels_counts[level_idx - 1]
                else:
                    lower_total_blocks = self.main.b
                self._draw_index_level(level_entries, col_x, y_start, int(col_w - 8), block_h, bfri=bfri, level_label=label, num_blocks=num_blocks, lower_total_blocks=lower_total_blocks)
            content_right = idx_area_x0 + num_columns * col_w
        elif self.index:
            entries = getattr(self.index, "entries", [])
            bfri = getattr(self.index, "bfri", None)
            if isinstance(self.index, PrimaryIndex):
                bi = math.ceil(self.main.b / bfri) if bfri and bfri > 0 else 1
            elif isinstance(self.index, SecondaryIndex):
                bi = math.ceil(self.main.r / bfri) if bfri and bfri > 0 else 1
            else:
                bi = max(1, math.ceil(len(entries) / bfri) if bfri and bfri > 0 else 1)
            col_x = idx_area_x0
            self._draw_index_level(entries, col_x, y_start, int(idx_area_w - 8), block_h, bfri=bfri, level_label="L1", num_blocks=bi, lower_total_blocks=self.main.b)
            content_right = idx_area_x0 + idx_area_w

        content_bottom = max(main_y + b * (block_h + 0), y_start) + 40
        content_right = max(content_right, main_x + main_w)
        try:
            self.canvas.configure(scrollregion=(0, 0, content_right + 40, content_bottom))
        except Exception:
            pass

        # highlight
        if highlight is not None:
            rec = highlight
            block_num = rec // self.main.bfr
            y0 = main_y + block_num * block_h
            x0 = main_x + margin
            x1 = x0 + block_w
            self.canvas.create_rectangle(x0, y0, x1, y0 + block_h - 4, outline="#FFD54F", width=3)

        if path:
            for lvl, entry in path:
                key, ptr = entry
                y = main_y + (lvl * (block_h + 12)) + 8
                ix = idx_area_x0 + idx_area_w
                iy = y
                mx = main_x + margin
                my = main_y + ptr * block_h + block_h / 2
                self.canvas.create_line(ix, iy, mx, my, fill="#8AFFC1", arrow="last", width=2)

    def _draw_index_level(self, entries, x, y, w, h, bfri: Optional[int] = None, level_label: Optional[str] = None, num_blocks: Optional[int] = None, lower_total_blocks: Optional[int] = None):
        if bfri is None:
            bfri = getattr(self.index, "bfri", None) or getattr(self.multilevel, "bfri", None)

        num_entries = len(entries) if entries else 0
        if num_blocks is None:
            if bfri and bfri > 0:
                num_blocks = max(1, math.ceil(num_entries / bfri))
            else:
                num_blocks = max(1, num_entries)

        block_h = max(24, h)
        block_w = w - 8

        if level_label:
            self.canvas.create_text(x + 6, y - 10, text=level_label, anchor="w", fill="#E2E8F0")

        for bi in range(num_blocks):
            bx0 = x + 4
            by0 = y + bi * (block_h + 8)
            bx1 = bx0 + block_w
            by1 = by0 + block_h
            self.canvas.create_rectangle(bx0, by0, bx1, by1, fill="#14213D", outline="#888")

            if bfri and bfri > 0:
                bstart = bi * bfri
                bend = min(bstart + bfri, num_entries)
            else:
                bstart = bi
                bend = min(bstart + 1, num_entries)

            # Only show pointer range to lower-level blocks, per user request.
            if bfri and lower_total_blocks is not None:
                tgt_start = bi * bfri
                tgt_end = min((bi + 1) * bfri - 1, lower_total_blocks - 1)
                label = f"B{bi}: B{tgt_start}-B{tgt_end}"
            else:
                label = f"B{bi}: —"

            self.canvas.create_text(bx0 + 6, by0 + block_h / 2, text=label, anchor="w", fill="white", font=("Arial", 9))


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.geometry("1000x600")
    view = ExternalIndexView(root)
    view.pack(fill="both", expand=True)
    root.mainloop()
