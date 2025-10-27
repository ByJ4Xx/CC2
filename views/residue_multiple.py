import customtkinter as ctk
from .base import BaseContent
from models.residue_multiple import ResidueMultipleTree
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import filedialog as fd
import json


class ResidueMultipleContent(BaseContent):
    title = "Árbol Residuo Múltiple"

    def __init__(self, master):
        super().__init__(master)

        self.tree = ResidueMultipleTree()

        # Layout: main graph area (left) + action sidebar (right)
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=0)
        self.body.grid_rowconfigure(0, weight=1)

        # Area del grafo (matplotlib)
        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.body)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky='nsew', padx=(0, 12))

        # Barra lateral de acciones
        self.side = ctk.CTkFrame(self.body, width=300)
        self.side.grid(row=0, column=1, sticky='ns', padx=(0, 0))
        self.side.grid_propagate(False)
        self.side.columnconfigure(0, weight=1)

        ctk.CTkLabel(self.side, text="Acciones", font=("", 14, "bold")).grid(row=0, column=0, padx=12, pady=12, sticky='w')

        ctk.CTkLabel(self.side, text="Letra (a-z):").grid(row=1, column=0, padx=12, pady=(4, 0), sticky='w')
        self.letter_entry = ctk.CTkEntry(self.side)
        self.letter_entry.grid(row=2, column=0, padx=12, pady=(4, 8), sticky='ew')

        self.insert_btn = ctk.CTkButton(self.side, text="Insertar", command=self.on_insert)
        self.insert_btn.grid(row=3, column=0, padx=12, pady=6, sticky='ew')

        self.search_btn = ctk.CTkButton(self.side, text="Buscar", command=self.on_search)
        self.search_btn.grid(row=4, column=0, padx=12, pady=6, sticky='ew')

        self.delete_btn = ctk.CTkButton(self.side, text="Eliminar", command=self.on_delete)
        self.delete_btn.grid(row=5, column=0, padx=12, pady=6, sticky='ew')

        self.show_table_btn = ctk.CTkButton(self.side, text="Mostrar tabla de códigos", command=self.show_table)
        self.show_table_btn.grid(row=6, column=0, padx=12, pady=(18, 6), sticky='ew')

        # Estado
        self.status = ctk.CTkLabel(self.side, text="", wraplength=260, anchor='w', justify='left')
        self.status.grid(row=7, column=0, padx=12, pady=(8, 12), sticky='w')

        # Save / Load / Clear
        self.save_btn = ctk.CTkButton(self.side, text="Guardar (.json)", command=self.on_save)
        self.save_btn.grid(row=8, column=0, padx=12, pady=(6, 4), sticky='ew')

        self.load_btn = ctk.CTkButton(self.side, text="Cargar (.json)", command=self.on_load)
        self.load_btn.grid(row=9, column=0, padx=12, pady=4, sticky='ew')

        self.clear_btn = ctk.CTkButton(self.side, text="Limpiar", fg_color="#b00020", hover_color="#c62828", command=self.on_clear)
        self.clear_btn.grid(row=10, column=0, padx=12, pady=(12, 6), sticky='ew')

        self._init_done = True
        self._draw()

    def _nodes_positions(self, root):
        # Compute subtree widths and depths, then place leaves left-to-right
        positions = {}

        def compute(node, depth=0):
            # returns width of this subtree and sets temporary attributes
            if node is None:
                return 0
            node._depth = depth
            if not node.children:
                node._width = 1
                return 1
            widths = []
            for k in sorted(node.children.keys()):
                w = compute(node.children[k], depth + 1)
                widths.append(w)
            node._width = sum(widths) if widths else 1
            return node._width

        compute(root)

        x_counter = 0

        def place(node):
            nonlocal x_counter
            if not node.children:
                positions[node.id] = (x_counter, -getattr(node, '_depth', 0))
                x_counter += 1
                return
            # place children first
            for k in sorted(node.children.keys()):
                place(node.children[k])
            # center this node over its children
            child_xs = [positions[node.children[k].id][0] for k in sorted(node.children.keys())]
            if child_xs:
                positions[node.id] = (sum(child_xs) / len(child_xs), -getattr(node, '_depth', 0))
            else:
                positions[node.id] = (x_counter, -getattr(node, '_depth', 0))

        place(root)

        # normalize x positions to center the whole tree around x=0 (prettier plotting)
        xs = [p[0] for p in positions.values()] if positions else [0]
        min_x, max_x = min(xs), max(xs)
        mid = (min_x + max_x) / 2
        for nid in list(positions.keys()):
            x, y = positions[nid]
            positions[nid] = (x - mid, y)

        # cleanup temp attrs (optional)
        def cleanup(node):
            if node is None:
                return
            for c in node.children.values():
                cleanup(c)
            for attr in ('_width', '_depth'):
                if hasattr(node, attr):
                    delattr(node, attr)

        cleanup(root)
        return positions

    def _draw_graph(self, highlight_path_ids=None):
        self.ax.cla()
        nodes = self.tree.to_list()
        G = nx.DiGraph()
        id_to_label = {}
        edges = []  # tuples (u, v, label)
        for nid, val, mapping in nodes:
            if nid == self.tree.root.id:
                label = 'Raiz'
            elif val is None:
                label = 'aux'
            else:
                label = val
            id_to_label[nid] = label
            G.add_node(nid)
            for k, cid in mapping.items():
                edges.append((nid, cid, k))

        positions = self._nodes_positions(self.tree.root)

        # draw edges with labels
        for u, v, lab in edges:
            x1, y1 = positions.get(u, (0, 0))
            x2, y2 = positions.get(v, (0, 0))
            self.ax.plot([x1, x2], [y1, y2], color='black', zorder=1)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            self.ax.text(mx, my, lab, color='black', fontsize=8, zorder=3)

        # draw nodes
        for nid, label in id_to_label.items():
            x1, y1 = positions.get(nid, (0, 0))
            if label == 'Raiz':
                color = 'gold'
            elif label == 'aux':
                color = 'lightgreen'
            else:
                color = 'lightblue'
            if highlight_path_ids and nid in highlight_path_ids:
                color = 'orange'
            self.ax.scatter([x1], [y1], s=500, c=color, zorder=2)
            self.ax.text(x1, y1, label, ha='center', va='center', zorder=4)

        self.ax.set_axis_off()
        self.fig.tight_layout()
        self.canvas.draw()

    def _draw(self, highlight_path_ids=None, **kwargs):
        if not getattr(self, '_init_done', False):
            return
        return self._draw_graph(highlight_path_ids)

    def on_insert(self):
        letter = (self.letter_entry.get() or '').strip()
        if not letter or len(letter) != 1 or not letter.isalpha():
            self.status.configure(text='Ingrese una única letra (a-z)')
            return
        try:
            path = self.tree.insert(letter)
            self.status.configure(text=f"Insertado '{letter.upper()}' en nodo(s): {path}")
            try:
                self.letter_entry.delete(0, 'end')
            except Exception:
                pass
            self._draw()
        except Exception as e:
            self.status.configure(text=str(e))

    def on_search(self):
        letter = (self.letter_entry.get() or '').strip()
        if not letter or len(letter) != 1 or not letter.isalpha():
            self.status.configure(text='Ingrese una única letra (a-z) para buscar')
            return
        path = self.tree.find(letter)
        if not path:
            self.status.configure(text=f"No se encontró '{letter.upper()}'")
            self._draw()
        else:
            self.status.configure(text=f"Ruta a '{letter.upper()}': {path}")
            self._draw(highlight_path_ids=set(path))

    def on_delete(self):
        letter = (self.letter_entry.get() or '').strip()
        if not letter or len(letter) != 1 or not letter.isalpha():
            self.status.configure(text='Ingrese una única letra (a-z) para eliminar')
            return
        try:
            self.tree.delete(letter)
            self.status.configure(text=f"Eliminado '{letter.upper()}' y rearmado el árbol")
            self._draw()
        except Exception as e:
            self.status.configure(text=str(e))

    def show_table(self):
        top = tk.Toplevel(self)
        top.title("Tabla de Código Binario")
        top.geometry("520x400")
        txt = tk.Text(top, wrap='none')
        txt.pack(fill='both', expand=True)
        txt.insert('1.0', "Letra\tCódigo\n")
        for k, v in sorted(ResidueMultipleTree.CODE_TABLE.items()):
            txt.insert('end', f"{k}\t{v}\n")
        txt.configure(state='disabled')

    def on_save(self):
        path = fd.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files', '*.json')])
        if not path:
            return
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.tree.to_dict(), f, ensure_ascii=False, indent=2)
            self.status.configure(text=f"Guardado en {path}")
        except Exception as e:
            self.status.configure(text=f"Error guardando: {e}")

    def on_load(self):
        path = fd.askopenfilename(filetypes=[('JSON files', '*.json')])
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            new_tree = ResidueMultipleTree.from_dict(data)
            self.tree = new_tree
            self.status.configure(text=f"Cargado desde {path}")
            self._draw()
        except Exception as e:
            self.status.configure(text=f"Error cargando: {e}")

    def on_clear(self):
        try:
            self.tree.clear()
            self.status.configure(text='Árbol limpiado')
            self._draw()
        except Exception as e:
            self.status.configure(text=str(e))
