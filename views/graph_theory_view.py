"""
Vista de Teoría de Grafos
Interfaz para circuitos, conjuntos de corte y matrices
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
from graph_theory import GraphTheory


class GraphTheoryContent(ctk.CTkFrame):
    """Contenido para teoría de grafos - Matrices"""

    title = "Matrices"

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.graph = GraphTheory()
        self.graph_pos = None  # Posición fija del grafo

        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.grid_columnconfigure(0, weight=0, minsize=250)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Panel izquierdo: controles
        self.create_controls_panel()

        # Panel derecho: visualización y resultados
        self.create_visualization_panel()

    def create_controls_panel(self):
        """Crea el panel de controles"""
        controls = ctk.CTkScrollableFrame(self, corner_radius=10)
        controls.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        # ===== CONSTRUCCIÓN DEL GRAFO =====
        self.create_section(controls, "🔨 Datos del Grafo")

        ctk.CTkLabel(controls, text="Vértice:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.vertex_entry = ctk.CTkEntry(controls, placeholder_text="Nombre del vértice")
        self.vertex_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="➕ Agregar Vértice",
            command=self.add_vertex,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(controls, text="Arista:", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        self.edge_name_entry = ctk.CTkEntry(controls, placeholder_text="Nombre (ej: e1)")
        self.edge_name_entry.pack(fill="x", padx=10, pady=5)

        # Lista desplegable para Vértice 1
        ctk.CTkLabel(controls, text="Vértice 1:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.edge_v1_var = ctk.StringVar(value="")
        self.edge_v1_combo = ctk.CTkComboBox(
            controls,
            variable=self.edge_v1_var,
            values=[]
        )
        self.edge_v1_combo.pack(fill="x", padx=10, pady=5)

        # Lista desplegable para Vértice 2
        ctk.CTkLabel(controls, text="Vértice 2:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.edge_v2_var = ctk.StringVar(value="")
        self.edge_v2_combo = ctk.CTkComboBox(
            controls,
            variable=self.edge_v2_var,
            values=[]
        )
        self.edge_v2_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="➕ Agregar Arista",
            command=self.add_edge,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=5)

        # ===== MATRICES =====
        self.create_section(controls, "📊 Matrices Fundamentales")

        # Matriz de Incidencia
        ctk.CTkButton(
            controls,
            text="Matriz de Incidencia (V-A)",
            command=self.show_vertex_incidence,
            fg_color="#16a085",
            hover_color="#138f7a"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Matriz de Incidencia (A-V)",
            command=self.show_edge_incidence,
            fg_color="#16a085",
            hover_color="#138f7a"
        ).pack(fill="x", padx=10, pady=5)

        # Matriz de Adyacencia
        self.create_section(controls, "🔗 Matriz de Adyacencia")

        ctk.CTkButton(
            controls,
            text="Vértices",
            command=self.show_vertex_adjacency,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Aristas",
            command=self.show_edge_adjacency,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=5)

        # Matriz de Conjuntos de Corte
        self.create_section(controls, "✂️ Matriz de Conjuntos de Corte")

        ctk.CTkButton(
            controls,
            text="Conjuntos de Corte",
            command=self.find_cut_sets,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Conjuntos de Corte Fundamentales",
            command=self.find_fundamental_cuts,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(fill="x", padx=10, pady=5)

        # Matriz de Circuitos
        self.create_section(controls, "🔄 Matriz de Circuitos")

        ctk.CTkButton(
            controls,
            text="Encontrar Circuitos",
            command=self.find_circuits,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Circuitos Fundamentales",
            command=self.find_fundamental_cycles,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(fill="x", padx=10, pady=5)

        # ===== UTILIDADES =====
        self.create_section(controls, "🔧 Utilidades")

        ctk.CTkButton(
            controls,
            text="💾 Guardar Grafo",
            command=self.save_graph,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="📂 Cargar Grafo",
            command=self.load_graph,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="🗑️ Limpiar Todo",
            command=self.clear_all,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(fill="x", padx=10, pady=5)

    def create_visualization_panel(self):
        """Crea el panel de visualización"""
        viz_frame = ctk.CTkFrame(self, corner_radius=10)
        viz_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        viz_frame.grid_rowconfigure(1, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)

        # Título
        self.viz_title = ctk.CTkLabel(
            viz_frame,
            text="📊 Grafo",
            font=("Segoe UI", 16, "bold")
        )
        self.viz_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        # Notebook con tabs
        self.notebook = ctk.CTkTabview(viz_frame)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # Tab de visualización
        self.tab_graph = self.notebook.add("Grafo")

        # Canvas de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6), facecolor='#2b2b2b')
        self.ax.set_facecolor('#2b2b2b')
        self.canvas = FigureCanvasTkAgg(self.fig, self.tab_graph)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Tab de resultados
        self.tab_results = self.notebook.add("Resultados")
        self.results_text = ctk.CTkTextbox(self.tab_results, font=("Consolas", 11))
        self.results_text.pack(fill="both", expand=True, padx=10, pady=10)

        self.draw_graph()

    def create_section(self, parent, title):
        """Crea un título de sección"""
        label = ctk.CTkLabel(
            parent,
            text=title,
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        )
        label.pack(fill="x", padx=10, pady=(15, 5))

    # ==================== CONSTRUCCIÓN ====================

    def add_vertex(self):
        """Agrega un vértice al grafo"""
        vertex = self.vertex_entry.get().strip()
        if not vertex:
            messagebox.showwarning("Advertencia", "Ingresa un nombre de vértice")
            return

        if vertex in self.graph.vertices:
            messagebox.showwarning("Advertencia", f"El vértice '{vertex}' ya existe")
            return

        self.graph.add_vertex(vertex)
        self.vertex_entry.delete(0, 'end')

        # Actualizar las listas desplegables de vértices
        vertices_list = sorted(list(self.graph.vertices))
        self.edge_v1_combo.configure(values=vertices_list)
        self.edge_v2_combo.configure(values=vertices_list)

        self.draw_graph()
        self.show_status(f"✓ Vértice '{vertex}' agregado")

    def add_edge(self):
        """Agrega una arista al grafo"""
        edge_name = self.edge_name_entry.get().strip()
        v1 = self.edge_v1_var.get().strip()
        v2 = self.edge_v2_var.get().strip()

        if not edge_name or not v1 or not v2:
            messagebox.showwarning("Advertencia", "Completa todos los campos")
            return

        if edge_name in self.graph.edges:
            messagebox.showwarning("Advertencia", f"La arista '{edge_name}' ya existe")
            return

        if not self.graph.add_edge(edge_name, v1, v2):
            messagebox.showerror("Error", "Verifica que los vértices existan")
            return

        self.edge_name_entry.delete(0, 'end')
        self.edge_v1_var.set("")
        self.edge_v2_var.set("")
        self.draw_graph()
        self.show_status(f"✓ Arista '{edge_name}' agregada")

    # ==================== CIRCUITOS ====================

    def find_circuits(self):
        """Encuentra todos los circuitos del grafo"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        circuits = self.graph.find_circuits()

        if len(circuits) == 0:
            result = "No se encontraron circuitos (el grafo es acíclico o un árbol)\n"
        else:
            result = f"CIRCUITOS ENCONTRADOS: {len(circuits)}\n\n"
            for circuit in circuits:
                result += f"Circuito {circuit['id']}:\n"
                result += f"  Vértices: {' → '.join(circuit['vertices'])} → {circuit['vertices'][0]}\n"
                result += f"  Aristas: {', '.join(circuit['edges'])}\n"
                result += f"  Longitud: {circuit['length']}\n\n"

        self.show_results(result)
        self.notebook.set("Resultados")

    def find_fundamental_cycles(self):
        """Encuentra circuitos fundamentales"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        fundamental = self.graph.fundamental_cycles()

        if len(fundamental) == 0:
            result = "No se encontraron circuitos fundamentales\n"
        else:
            result = f"CIRCUITOS FUNDAMENTALES: {len(fundamental)}\n\n"
            for i, cycle in enumerate(fundamental, 1):
                result += f"Circuito Fundamental {i}:\n"
                result += f"  Cuerda: {cycle['chord']}\n"
                result += f"  Camino en árbol: {' → '.join(cycle['vertices'])}\n"
                result += f"  Aristas del árbol: {', '.join(cycle['tree_edges'])}\n"
                result += f"  Todas las aristas: {', '.join(cycle['all_edges'])}\n"
                result += f"  Longitud: {cycle['length']}\n\n"

        self.show_results(result)
        self.notebook.set("Resultados")

    # ==================== CONJUNTOS DE CORTE ====================

    def find_cut_sets(self):
        """Encuentra conjuntos de corte"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        cut_sets = self.graph.find_cut_sets()

        if len(cut_sets) == 0:
            result = "No se encontraron conjuntos de corte o el grafo no es conexo\n"
        else:
            result = f"CONJUNTOS DE CORTE: {len(cut_sets)}\n\n"
            for i, cut in enumerate(cut_sets, 1):
                result += f"Conjunto de Corte {i}:\n"
                result += f"  Aristas: {', '.join(cut['edges'])}\n"
                result += f"  Tamaño: {cut['size']}\n"
                result += f"  Partición 1: {{{', '.join(cut['partitions'][0])}}}\n"
                result += f"  Partición 2: {{{', '.join(cut['partitions'][1])}}}\n\n"

        self.show_results(result)
        self.notebook.set("Resultados")

    def find_fundamental_cuts(self):
        """Encuentra conjuntos de corte fundamentales"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        fundamental_cuts = self.graph.fundamental_cut_sets()

        if len(fundamental_cuts) == 0:
            result = "No se encontraron conjuntos de corte fundamentales\n"
        else:
            result = f"CONJUNTOS DE CORTE FUNDAMENTALES: {len(fundamental_cuts)}\n\n"
            for i, cut in enumerate(fundamental_cuts, 1):
                result += f"Conjunto de Corte Fundamental {i}:\n"
                result += f"  Arista del árbol: {cut['tree_edge']}\n"
                result += f"  Todas las aristas del corte: {', '.join(cut['cut_edges'])}\n"
                result += f"  Tamaño: {cut['size']}\n"
                result += f"  Partición 1: {{{', '.join(cut['partitions'][0])}}}\n"
                result += f"  Partición 2: {{{', '.join(cut['partitions'][1])}}}\n\n"

        self.show_results(result)
        self.notebook.set("Resultados")

    # ==================== MATRICES ====================

    def show_vertex_adjacency(self):
        """Muestra matriz de adyacencia de vértices"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        matrix, vertices = self.graph.vertex_adjacency_matrix()

        result = "MATRIZ DE ADYACENCIA DE VÉRTICES\n\n"
        result += "M[i][j] = número de aristas entre vértice i y vértice j\n\n"

        # Encabezado
        result += "     " + "  ".join(f"{v:>3}" for v in vertices) + "\n"
        result += "   " + "-" * (4 * len(vertices) + 2) + "\n"

        # Filas
        for i, v in enumerate(vertices):
            result += f"{v:>3} |"
            for j in range(len(vertices)):
                result += f"{matrix[i][j]:>3} "
            result += "\n"

        self.show_results(result)
        self.notebook.set("Resultados")

    def show_edge_adjacency(self):
        """Muestra matriz de adyacencia de aristas"""
        if len(self.graph.edges) == 0:
            messagebox.showwarning("Advertencia", "El grafo no tiene aristas")
            return

        matrix, edges = self.graph.edge_adjacency_matrix()

        result = "MATRIZ DE ADYACENCIA DE ARISTAS\n\n"
        result += "M[i][j] = 1 si las aristas comparten un vértice, 0 en caso contrario\n\n"

        # Encabezado
        result += "     " + "  ".join(f"{e:>3}" for e in edges) + "\n"
        result += "   " + "-" * (4 * len(edges) + 2) + "\n"

        # Filas
        for i, e in enumerate(edges):
            result += f"{e:>3} |"
            for j in range(len(edges)):
                result += f"{matrix[i][j]:>3} "
            result += "\n"

        self.show_results(result)
        self.notebook.set("Resultados")

    def show_vertex_incidence(self):
        """Muestra matriz de incidencia vértice-arista"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        matrix, vertices, edges = self.graph.vertex_incidence_matrix()

        result = "MATRIZ DE INCIDENCIA VÉRTICE-ARISTA\n\n"
        result += "M[i][j] = 1 si el vértice i es incidente a la arista j\n\n"

        # Encabezado
        result += "     " + "  ".join(f"{e:>3}" for e in edges) + "\n"
        result += "   " + "-" * (4 * len(edges) + 2) + "\n"

        # Filas
        for i, v in enumerate(vertices):
            result += f"{v:>3} |"
            for j in range(len(edges)):
                result += f"{matrix[i][j]:>3} "
            result += "\n"

        self.show_results(result)
        self.notebook.set("Resultados")

    def show_edge_incidence(self):
        """Muestra matriz de incidencia arista-vértice"""
        if len(self.graph.edges) == 0:
            messagebox.showwarning("Advertencia", "El grafo no tiene aristas")
            return

        matrix, edges, vertices = self.graph.edge_incidence_matrix()

        result = "MATRIZ DE INCIDENCIA ARISTA-VÉRTICE\n\n"
        result += "M[i][j] = 1 si la arista i es incidente al vértice j\n\n"

        # Encabezado
        result += "     " + "  ".join(f"{v:>3}" for v in vertices) + "\n"
        result += "   " + "-" * (4 * len(vertices) + 2) + "\n"

        # Filas
        for i, e in enumerate(edges):
            result += f"{e:>3} |"
            for j in range(len(vertices)):
                result += f"{matrix[i][j]:>3} "
            result += "\n"

        self.show_results(result)
        self.notebook.set("Resultados")

    # ==================== VISUALIZACIÓN ====================

    def draw_graph(self):
        """Dibuja el grafo con posición fija"""
        self.ax.clear()

        if len(self.graph.vertices) == 0:
            self.ax.text(
                0.5, 0.5,
                'Agrega vértices y aristas\npara visualizar el grafo',
                ha='center', va='center',
                fontsize=14, color='#95a5a6',
                transform=self.ax.transAxes
            )
            self.ax.axis('off')
            self.canvas.draw()
            self.graph_pos = None  # Resetear posición
            return

        G = nx.Graph()
        G.add_nodes_from(self.graph.vertices)

        edge_labels = {}
        for edge_name, (v1, v2) in self.graph.edges.items():
            G.add_edge(v1, v2)
            edge_labels[(v1, v2)] = edge_name

        # Calcular o reutilizar posición del grafo
        current_vertices = set(self.graph.vertices)

        if self.graph_pos is None:
            # Primera vez o después de limpiar
            self.graph_pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        else:
            # Verificar si hay cambios en vértices
            stored_vertices = set(self.graph_pos.keys())

            if current_vertices != stored_vertices:
                new_vertices = current_vertices - stored_vertices
                removed_vertices = stored_vertices - current_vertices

                if new_vertices:
                    # Calcular posición para nuevos vértices
                    temp_pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
                    for v in new_vertices:
                        self.graph_pos[v] = temp_pos[v]

                if removed_vertices:
                    # Eliminar vértices que ya no existen
                    for v in removed_vertices:
                        del self.graph_pos[v]

        pos = self.graph_pos

        nx.draw_networkx_nodes(
            G, pos, ax=self.ax,
            node_color='#3498db',
            node_size=800,
            alpha=0.9
        )

        nx.draw_networkx_edges(
            G, pos, ax=self.ax,
            edge_color='#95a5a6',
            width=2,
            alpha=0.6
        )

        nx.draw_networkx_labels(
            G, pos, ax=self.ax,
            font_size=12,
            font_weight='bold',
            font_color='white'
        )

        nx.draw_networkx_edge_labels(
            G, pos, edge_labels, ax=self.ax,
            font_size=9,
            font_color='#ecf0f1'
        )

        self.ax.set_title(
            f"Vértices: {len(self.graph.vertices)}, Aristas: {len(self.graph.edges)}",
            color='white',
            fontsize=14,
            fontweight='bold'
        )
        self.ax.axis('off')
        self.canvas.draw()

    def show_results(self, text: str):
        """Muestra resultados en el panel de texto"""
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", text)

    def show_status(self, message: str):
        """Muestra mensaje de estado"""
        self.viz_title.configure(text=f"📊 {message}")
        self.after(3000, lambda: self.viz_title.configure(text="📊 Grafo"))

    # ==================== PERSISTENCIA ====================

    def save_graph(self):
        """Guarda el grafo en un archivo"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.graph.to_json())
                messagebox.showinfo("Éxito", "Grafo guardado exitosamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")

    def load_graph(self):
        """Carga un grafo desde un archivo"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    self.graph = GraphTheory.from_json(f.read())
                self.draw_graph()
                messagebox.showinfo("Éxito", "Grafo cargado exitosamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar: {str(e)}")

    def clear_all(self):
        """Limpia todo"""
        if messagebox.askyesno("Confirmar", "¿Limpiar todo el grafo?"):
            self.graph = GraphTheory()
            self.graph_pos = None  # Resetear posición del grafo
            self.draw_graph()
            self.results_text.delete("1.0", "end")
            self.show_status("✓ Grafo limpiado")
