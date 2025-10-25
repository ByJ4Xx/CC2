import customtkinter as ctk
from .base import BaseContent
from models.residue import ResidueTree
import networkx as nx
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk


class ResidueContent(BaseContent):
    title = "Árbol por Residuos"

    def __init__(self, master):
        super().__init__(master)

        self.tree = ResidueTree()

        # Layout: main graph area (left) + action sidebar (right)
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=0)
        self.body.grid_rowconfigure(0, weight=1)

        # Area del grafo (matplotlib)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.body)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=0, sticky='nsew', padx=(0, 12))

        # Barra lateral de acciones
        self.side = ctk.CTkFrame(self.body, width=260)
        self.side.grid(row=0, column=1, sticky='ns', padx=(0, 0))
        self.side.grid_propagate(False)
        self.side.columnconfigure(0, weight=1)

        ctk.CTkLabel(self.side, text="Acciones", font=("", 14, "bold")).grid(row=0, column=0, padx=12, pady=12, sticky='w')

        # Input letra
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

        # Estado / mensajes
        self.status = ctk.CTkLabel(self.side, text="", wraplength=220, anchor='w', justify='left')
        self.status.grid(row=7, column=0, padx=12, pady=(8, 12), sticky='w')

        # Inicial draw
        self._init_done = True
        self._draw()

    def _nodes_positions(self, root):
        positions = {}
        x = 0

        def dfs(node, depth=0):
            nonlocal x
            if node is None:
                return
            dfs(node.left, depth + 1)
            positions[node.id] = (x, -depth)
            x += 1
            dfs(node.right, depth + 1)

        dfs(root, 0)
        return positions

    def _draw_graph(self, highlight_path_ids=None):
        self.ax.cla()
        nodes = self.tree.to_list()
        G = nx.DiGraph()
        id_to_label = {}
        root_id = getattr(self.tree.root, "id", None)
        for nid, val, left_id, right_id in nodes:
            if nid == root_id:
                label = "Raiz"
            elif val is None:
                label = "aux"
            else:
                label = val
            id_to_label[nid] = label
            G.add_node(nid)
            if left_id is not None:
                G.add_edge(nid, left_id)
            if right_id is not None:
                G.add_edge(nid, right_id)

        positions = self._nodes_positions(self.tree.root)

        for u, v in G.edges():
            x1, y1 = positions.get(u, (0, 0))
            x2, y2 = positions.get(v, (0, 0))
            color = 'red' if highlight_path_ids and u in highlight_path_ids and v in highlight_path_ids else 'black'
            self.ax.plot([x1, x2], [y1, y2], color=color, zorder=1)

        for nid, label in id_to_label.items():
            x1, y1 = positions.get(nid, (0, 0))
            is_high = highlight_path_ids and nid in highlight_path_ids
            if is_high:
                color = 'orange'
            else:
                if nid == root_id:
                    color = 'gold'
                elif label == 'aux':
                    color = 'lightgreen'
                else:
                    color = 'lightblue'
            self.ax.scatter([x1], [y1], s=600, c=color, zorder=2)
            self.ax.text(x1, y1, label, ha='center', va='center', zorder=3)

        self.ax.set_axis_off()
        self.fig.tight_layout()
        self.canvas.draw()

    def _draw(self, highlight_path_ids=None, **kwargs):
        if not getattr(self, "_init_done", False):
            return
        return self._draw_graph(highlight_path_ids)

    def on_insert(self):
        letter = (self.letter_entry.get() or '').strip()
        if not letter or len(letter) != 1 or not letter.isalpha():
            self.status.configure(text="Ingrese una única letra (a-z)")
            return
        try:
            path = self.tree.insert(letter)
            self.status.configure(text=f"Insertado '{letter.upper()}' en nodo(s): {path}")
            # clear input after successful insert
            try:
                self.letter_entry.delete(0, 'end')
            except Exception:
                self.letter_entry.configure(text='')
            self._draw()
        except Exception as e:
            self.status.configure(text=str(e))

    def on_search(self):
        letter = (self.letter_entry.get() or '').strip()
        if not letter or len(letter) != 1 or not letter.isalpha():
            self.status.configure(text="Ingrese una única letra (a-z) para buscar")
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
            self.status.configure(text="Ingrese una única letra (a-z) para eliminar")
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
        for k, v in sorted(ResidueTree.CODE_TABLE.items()):
            txt.insert('end', f"{k}\t{v}\n")
        txt.configure(state='disabled')
