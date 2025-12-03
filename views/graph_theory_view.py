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
        self.grid_columnconfigure(0, weight=0, minsize=280)
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

        # ===== CONFIGURACIÓN DEL GRAFO =====
        self.create_section(controls, "⚙️ Propiedades del Grafo")

        ctk.CTkLabel(controls, text="Tipo de Grafo:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.directed_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            controls,
            text="Dirigido",
            variable=self.directed_var,
            command=self.toggle_directed
        ).pack(fill="x", padx=10, pady=5)

        self.weights_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            controls,
            text="Con Pesos",
            variable=self.weights_var,
            command=self.toggle_weights
        ).pack(fill="x", padx=10, pady=5)

        # ===== CONSTRUCCIÓN DEL GRAFO =====
        self.create_section(controls, "🔨 Vértices")

        ctk.CTkLabel(controls, text="Nombre:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.vertex_entry = ctk.CTkEntry(controls, placeholder_text="Ej: A, B, 1, 2...")
        self.vertex_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="➕ Agregar Vértice",
            command=self.add_vertex,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(controls, text="Eliminar:", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        self.vertex_combo = ctk.CTkComboBox(
            controls,
            values=[],
            state="readonly"
        )
        self.vertex_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="🗑️ Eliminar Vértice",
            command=self.remove_vertex,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        # ===== ARISTAS =====
        self.create_section(controls, "🔗 Aristas")

        ctk.CTkLabel(controls, text="Nombre:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.edge_name_entry = ctk.CTkEntry(controls, placeholder_text="Ej: e1, e2...")
        self.edge_name_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(controls, text="Vértice 1:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.edge_v1_var = ctk.StringVar(value="")
        self.edge_v1_combo = ctk.CTkComboBox(
            controls,
            variable=self.edge_v1_var,
            values=[],
            state="readonly"
        )
        self.edge_v1_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(controls, text="Vértice 2:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.edge_v2_var = ctk.StringVar(value="")
        self.edge_v2_combo = ctk.CTkComboBox(
            controls,
            variable=self.edge_v2_var,
            values=[],
            state="readonly"
        )
        self.edge_v2_combo.pack(fill="x", padx=10, pady=5)

        # Peso (si está habilitado)
        ctk.CTkLabel(controls, text="Peso:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.weight_entry = ctk.CTkEntry(controls, placeholder_text="1.0")
        self.weight_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="➕ Agregar Arista",
            command=self.add_edge,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(controls, text="Eliminar:", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        self.edge_combo = ctk.CTkComboBox(
            controls,
            values=[],
            state="readonly"
        )
        self.edge_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="🗑️ Eliminar Arista",
            command=self.remove_edge,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        # ===== MATRICES =====
        self.create_section(controls, "📊 Matrices Fundamentales")

        ctk.CTkButton(
            controls,
            text="Matriz de Incidencia (V-A)",
            command=self.show_vertex_incidence,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Matriz de Adyacencia (V)",
            command=self.show_vertex_adjacency,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Matriz de Adyacencia (A)",
            command=self.show_edge_adjacency,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        # ===== MATRICES AVANZADAS =====
        self.create_section(controls, "🔄 Circuitos y Cortes")

        ctk.CTkButton(
            controls,
            text="Todos los Circuitos",
            command=self.show_all_circuits_matrix,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Circuitos Fundamentales",
            command=self.show_circuit_matrix,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Todos los Conjuntos de Corte",
            command=self.show_all_cut_sets_matrix,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Conjuntos de Corte Fundamentales",
            command=self.show_fundamental_cut_matrix,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        # ===== INFORMACIÓN =====
        self.create_section(controls, "ℹ️ Información")

        ctk.CTkButton(
            controls,
            text="📋 Ver Información del Grafo",
            command=self.show_graph_info,
            fg_color="#3498db",
            hover_color="#2980b9",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        # ===== UTILIDADES =====
        self.create_section(controls, "🔧 Utilidades")

        ctk.CTkButton(
            controls,
            text="💾 Guardar Grafo",
            command=self.save_graph,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="📂 Cargar Grafo",
            command=self.load_graph,
            fg_color="#95a5a6",
            hover_color="#7f8c8d",
            text_color="#000000"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="🗑️ Limpiar Todo",
            command=self.clear_all,
            fg_color="#e74c3c",
            hover_color="#c0392b",
            text_color="#000000"
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

    # ==================== PROPIEDADES DEL GRAFO ====================

    def toggle_directed(self):
        """Cambia si el grafo es dirigido o no"""
        self.graph.is_directed = self.directed_var.get()
        self.draw_graph()

    def toggle_weights(self):
        """Cambia si el grafo tiene pesos"""
        self.graph.has_weights = self.weights_var.get()
        self.weight_entry.configure(state="normal" if self.weights_var.get() else "disabled")

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

        self.update_comboboxes()
        self.draw_graph()
        self.show_status(f"✓ Vértice '{vertex}' agregado")

    def remove_vertex(self):
        """Elimina un vértice"""
        vertex = self.vertex_combo.get()
        if not vertex:
            messagebox.showwarning("Advertencia", "Selecciona un vértice")
            return

        if self.graph.remove_vertex(vertex):
            self.update_comboboxes()
            self.draw_graph()
            self.show_status(f"✓ Vértice '{vertex}' eliminado")

    def add_edge(self):
        """Agrega una arista al grafo"""
        edge_name = self.edge_name_entry.get().strip()
        v1 = self.edge_v1_var.get().strip()
        v2 = self.edge_v2_var.get().strip()

        if not edge_name or not v1 or not v2:
            messagebox.showwarning("Advertencia", "Completa todos los campos obligatorios")
            return

        if edge_name in self.graph.edges:
            messagebox.showwarning("Advertencia", f"La arista '{edge_name}' ya existe")
            return

        weight = None
        if self.weights_var.get():
            try:
                weight = float(self.weight_entry.get() or "1.0")
            except ValueError:
                messagebox.showerror("Error", "El peso debe ser un número")
                return

        if not self.graph.add_edge(edge_name, v1, v2, weight):
            messagebox.showerror("Error", "Verifica que los vértices existan")
            return

        self.edge_name_entry.delete(0, 'end')
        self.weight_entry.delete(0, 'end')
        self.edge_v1_var.set("")
        self.edge_v2_var.set("")
        self.update_comboboxes()
        self.draw_graph()
        self.show_status(f"✓ Arista '{edge_name}' agregada")

    def remove_edge(self):
        """Elimina una arista"""
        edge = self.edge_combo.get()
        if not edge:
            messagebox.showwarning("Advertencia", "Selecciona una arista")
            return

        if self.graph.remove_edge(edge):
            self.update_comboboxes()
            self.draw_graph()
            self.show_status(f"✓ Arista '{edge}' eliminada")

    def update_comboboxes(self):
        """Actualiza los combobox con vértices y aristas"""
        vertices_list = sorted(list(self.graph.vertices))
        self.edge_v1_combo.configure(values=vertices_list)
        self.edge_v2_combo.configure(values=vertices_list)
        self.vertex_combo.configure(values=vertices_list)

        edges_list = sorted(list(self.graph.edges.keys()))
        self.edge_combo.configure(values=edges_list)

    # ==================== MATRICES ====================

    def show_vertex_adjacency(self):
        """Muestra matriz de adyacencia de vértices"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        matrix, vertices = self.graph.vertex_adjacency_matrix()
        self._show_matrix_window(
            "Matriz de Adyacencia de Vértices",
            matrix,
            vertices,
            vertices,
            "📊 MATRIZ DE ADYACENCIA DE VÉRTICES",
            "M[i][j] = número de aristas entre vértice i y vértice j"
        )

    def show_edge_adjacency(self):
        """Muestra matriz de adyacencia de aristas"""
        if len(self.graph.edges) == 0:
            messagebox.showwarning("Advertencia", "El grafo no tiene aristas")
            return

        matrix, edges = self.graph.edge_adjacency_matrix()
        self._show_matrix_window(
            "Matriz de Adyacencia de Aristas",
            matrix,
            edges,
            edges,
            "📊 MATRIZ DE ADYACENCIA DE ARISTAS",
            "M[i][j] = 1 si las aristas comparten un vértice, 0 en caso contrario"
        )

    def show_vertex_incidence(self):
        """Muestra matriz de incidencia vértice-arista"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        matrix, vertices, edges = self.graph.vertex_incidence_matrix()

        if self.graph.is_directed:
            desc = "Dirigido: 1=sale del vértice, -1=entra al vértice, 0=no incidente"
        else:
            desc = "No dirigido: 1=vértice incidente, 0=no incidente"

        self._show_matrix_window(
            "Matriz de Incidencia Vértice-Arista",
            matrix,
            vertices,
            edges,
            "📊 MATRIZ DE INCIDENCIA VÉRTICE-ARISTA",
            desc
        )

    def _show_matrix_window(self, title, matrix, row_labels, col_labels, header_title, header_desc):
        """Muestra una matriz en una ventana"""
        matrix_window = ctk.CTkToplevel(self)
        matrix_window.title(title)
        matrix_window.geometry("900x600")

        main_frame = ctk.CTkScrollableFrame(matrix_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Título
        title_frame = ctk.CTkFrame(main_frame, fg_color="#f0f0f0")
        title_frame.pack(fill="x", padx=0, pady=0)

        ctk.CTkLabel(
            title_frame,
            text=header_title,
            font=("Segoe UI", 16, "bold"),
            text_color="#000000"
        ).pack(pady=10, padx=20)

        ctk.CTkLabel(
            title_frame,
            text=header_desc,
            font=("Segoe UI", 10),
            text_color="#555555"
        ).pack(pady=(0, 10), padx=20)

        # Frame de tabla
        table_frame = ctk.CTkFrame(main_frame, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        n_cols = len(col_labels) + 1
        for col in range(n_cols):
            table_frame.grid_columnconfigure(col, minsize=60, weight=1)

        # Encabezado de columnas
        ctk.CTkLabel(table_frame, text="", font=("Segoe UI", 10, "bold"), text_color="#000000").grid(row=0, column=0, padx=5, pady=10)
        for col, label in enumerate(col_labels):
            ctk.CTkLabel(
                table_frame,
                text=label,
                font=("Segoe UI", 10, "bold"),
                text_color="#000000",
                fg_color="#ffffff"
            ).grid(row=0, column=col+1, padx=5, pady=10, sticky="ew")

        # Filas
        for i, row_label in enumerate(row_labels):
            ctk.CTkLabel(
                table_frame,
                text=row_label,
                font=("Segoe UI", 10, "bold"),
                text_color="#000000",
                fg_color="#ffffff"
            ).grid(row=i+1, column=0, padx=5, pady=10, sticky="ew")

            for j in range(len(col_labels)):
                value = matrix[i][j]
                bg_color = "#e8f4f8" if value != 0 else "white"
                ctk.CTkLabel(
                    table_frame,
                    text=str(int(value)),
                    font=("Segoe UI", 10),
                    text_color="#000000",
                    fg_color=bg_color
                ).grid(row=i+1, column=j+1, padx=5, pady=10, sticky="ew")

    def show_all_circuits_matrix(self):
        """Muestra matriz de todos los circuitos"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        circuits = self.graph.find_circuits()
        if not circuits:
            messagebox.showinfo("Info", "No se encontraron circuitos")
            return

        edges_list = sorted(list(self.graph.edges.keys()))
        fundamental = self.graph.fundamental_cycles() if self.graph.is_connected() else []
        fundamental_edges = {tuple(sorted(c.get("all_edges", []))) for c in fundamental}

        self._show_circuits_cut_sets_matrix(
            "Matriz de Circuitos",
            circuits,
            edges_list,
            fundamental_edges,
            "🔄 MATRIZ DE CIRCUITOS (TODOS)",
            "Azul claro = circuito fundamental | Blanco = circuito no fundamental"
        )

    def show_circuit_matrix(self):
        """Muestra matriz de circuitos fundamentales"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        fundamental = self.graph.fundamental_cycles()
        if not fundamental:
            messagebox.showinfo("Info", "No se encontraron circuitos fundamentales")
            return

        edges_list = sorted(list(self.graph.edges.keys()))
        circuits = [{"id": i+1, "edges": c.get("all_edges", [])} for i, c in enumerate(fundamental)]
        fundamental_edges = {tuple(sorted(c.get("all_edges", []))) for c in fundamental}

        self._show_circuits_cut_sets_matrix(
            "Matriz de Circuitos Fundamentales",
            circuits,
            edges_list,
            fundamental_edges,
            "🔄 MATRIZ DE CIRCUITOS FUNDAMENTALES",
            "Azul claro = arista en circuito fundamental"
        )

    def show_all_cut_sets_matrix(self):
        """Muestra matriz de todos los conjuntos de corte"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        cuts_result = self.graph.find_cut_sets()
        if not cuts_result.get("success", False):
            messagebox.showerror("Error", "No se encontraron conjuntos de corte")
            return

        cuts = cuts_result.get("cut_sets", [])
        fundamental = self.graph.fundamental_cut_sets()
        fundamental_edges = {tuple(sorted(c.get("cut_edges", []))) for c in fundamental}

        edges_list = sorted(list(self.graph.edges.keys()))
        cut_sets = [{"id": i+1, "edges": c.get("edges", [])} for i, c in enumerate(cuts)]

        self._show_circuits_cut_sets_matrix(
            "Matriz de Conjuntos de Corte",
            cut_sets,
            edges_list,
            fundamental_edges,
            "✂️ MATRIZ DE CONJUNTOS DE CORTE (TODOS)",
            "Azul claro = conjunto de corte fundamental | Blanco = conjunto de corte no fundamental"
        )

    def show_fundamental_cut_matrix(self):
        """Muestra matriz de conjuntos de corte fundamentales"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        fundamental = self.graph.fundamental_cut_sets()
        if not fundamental:
            messagebox.showinfo("Info", "No se encontraron conjuntos de corte fundamentales")
            return

        edges_list = sorted(list(self.graph.edges.keys()))
        cut_sets = [{"id": i+1, "edges": c.get("cut_edges", [])} for i, c in enumerate(fundamental)]
        fundamental_edges = {tuple(sorted(c.get("cut_edges", []))) for c in fundamental}

        self._show_circuits_cut_sets_matrix(
            "Matriz de Conjuntos de Corte Fundamentales",
            cut_sets,
            edges_list,
            fundamental_edges,
            "✂️ MATRIZ DE CONJUNTOS DE CORTE FUNDAMENTALES",
            "Azul claro = arista en conjunto de corte fundamental"
        )

    def _show_circuits_cut_sets_matrix(self, title, items, edges_list, fundamental_edges, header_title, header_desc):
        """Muestra una matriz de circuitos o conjuntos de corte"""
        matrix_window = ctk.CTkToplevel(self)
        matrix_window.title(title)
        matrix_window.geometry("1000x600")

        main_frame = ctk.CTkScrollableFrame(matrix_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Título
        title_frame = ctk.CTkFrame(main_frame, fg_color="#f0f0f0")
        title_frame.pack(fill="x", padx=0, pady=0)

        ctk.CTkLabel(
            title_frame,
            text=header_title,
            font=("Segoe UI", 16, "bold"),
            text_color="#000000"
        ).pack(pady=10, padx=20)

        ctk.CTkLabel(
            title_frame,
            text=header_desc,
            font=("Segoe UI", 10),
            text_color="#555555"
        ).pack(pady=(0, 10), padx=20)

        # Frame de tabla
        table_frame = ctk.CTkFrame(main_frame, fg_color="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=20)

        n_cols = len(edges_list) + 1
        for col in range(n_cols):
            table_frame.grid_columnconfigure(col, minsize=60, weight=1)

        # Encabezado de columnas
        ctk.CTkLabel(table_frame, text="", font=("Segoe UI", 10, "bold"), text_color="#000000", fg_color="white").grid(row=0, column=0, padx=5, pady=10)
        for col, edge in enumerate(edges_list):
            ctk.CTkLabel(
                table_frame,
                text=edge,
                font=("Segoe UI", 9, "bold"),
                text_color="#000000",
                fg_color="#ffffff"
            ).grid(row=0, column=col+1, padx=5, pady=10, sticky="ew")

        # Filas para cada item
        for i, item in enumerate(items):
            item_edges = set(item.get("edges", []))
            is_fundamental = tuple(sorted(item_edges)) in fundamental_edges
            # Obtener información de dirección para grafos dirigidos
            edge_directions = item.get("edge_directions", {})

            # Etiqueta de fila
            row_label = f"{['C', 'K'][i % 2]}{item.get('id', i+1)}"  # Alterna C y K
            ctk.CTkLabel(
                table_frame,
                text=row_label,
                font=("Segoe UI", 9, "bold"),
                text_color="#000000",
                fg_color="#ffffff"
            ).grid(row=i+1, column=0, padx=5, pady=10, sticky="ew")

            # Datos
            for j, edge in enumerate(edges_list):
                # Determinar el valor a mostrar
                if edge in item_edges:
                    # Si hay información de dirección, usarla; si no, mostrar 1
                    value = edge_directions.get(edge, 1)
                else:
                    value = 0

                # Determinar color de fondo según valor y tipo fundamental
                if value == 1 and is_fundamental:
                    bg_color = "#5dade2"
                elif value == 1:
                    bg_color = "#d4e8f0"
                elif value == -1 and is_fundamental:
                    bg_color = "#f39c12"  # Naranja para -1 fundamental
                elif value == -1:
                    bg_color = "#fadab9"  # Naranja claro para -1 no fundamental
                else:
                    bg_color = "white"

                ctk.CTkLabel(
                    table_frame,
                    text=str(value),
                    font=("Segoe UI", 10, "bold" if value != 0 else "normal"),
                    text_color="#000000",
                    fg_color=bg_color
                ).grid(row=i+1, column=j+1, padx=5, pady=10, sticky="ew")

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
            self.graph_pos = None
            return

        G = nx.DiGraph() if self.graph.is_directed else nx.Graph()
        G.add_nodes_from(self.graph.vertices)

        edge_labels = {}
        for edge_name, edge_data in self.graph.edges.items():
            v1, v2 = edge_data[0], edge_data[1]
            G.add_edge(v1, v2)
            edge_labels[(v1, v2)] = edge_name

        current_vertices = set(self.graph.vertices)

        if self.graph_pos is None:
            self.graph_pos = nx.circular_layout(G)
        else:
            stored_vertices = set(self.graph_pos.keys())
            if current_vertices != stored_vertices:
                self.graph_pos = nx.circular_layout(G)

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
            alpha=0.6,
            arrowsize=20 if self.graph.is_directed else 0,
            arrowstyle='->' if self.graph.is_directed else ''
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
            font_color='#000000'
        )

        graph_type = "Dirigido" if self.graph.is_directed else "No dirigido"
        weights_str = "con pesos" if self.graph.has_weights else "sin pesos"
        self.ax.set_title(
            f"{graph_type} {weights_str} | Vértices: {len(self.graph.vertices)}, Aristas: {len(self.graph.edges)}",
            color='white',
            fontsize=12,
            fontweight='bold'
        )
        self.ax.axis('off')
        self.canvas.draw()

    def show_status(self, message: str):
        """Muestra mensaje de estado"""
        self.viz_title.configure(text=f"📊 {message}")
        self.after(3000, lambda: self.viz_title.configure(text="📊 Grafo"))

    # ==================== INFORMACIÓN ====================

    def show_graph_info(self):
        """Muestra información del grafo actual"""
        if len(self.graph.vertices) == 0:
            messagebox.showinfo("Información", "El grafo está vacío")
            return

        graph_type = "Dirigido" if self.graph.is_directed else "No dirigido"
        weights_status = "Con pesos" if self.graph.has_weights else "Sin pesos"

        vertices_list = sorted(list(self.graph.vertices))
        edges_list = sorted(list(self.graph.edges.keys()))

        # Calcular información adicional
        is_connected = self.graph.is_connected()

        info_text = f"""
╔════════════════════════════════════════╗
║     INFORMACIÓN DEL GRAFO              ║
╚════════════════════════════════════════╝

📊 PROPIEDADES BÁSICAS:
  • Tipo: {graph_type}
  • Pesos: {weights_status}
  • Conexo: {"Sí" if is_connected else "No"}

📈 ESTADÍSTICAS:
  • Vértices: {len(self.graph.vertices)}
  • Aristas: {len(self.graph.edges)}

📍 VÉRTICES ({len(vertices_list)}):
{chr(10).join(f"    {i+1}. {v}" for i, v in enumerate(vertices_list))}

🔗 ARISTAS ({len(edges_list)}):
"""
        for i, edge_name in enumerate(edges_list, 1):
            edge_data = self.graph.edges[edge_name]
            v1, v2 = edge_data[0], edge_data[1]
            weight = edge_data[2] if len(edge_data) > 2 else 1.0

            if self.graph.is_directed:
                edge_str = f"{v1} → {v2}"
            else:
                edge_str = f"{v1} — {v2}"

            if self.graph.has_weights:
                info_text += f"    {i}. {edge_name}: {edge_str} (peso: {weight})\n"
            else:
                info_text += f"    {i}. {edge_name}: {edge_str}\n"

        info_text += "\n"

        # Crear ventana de información
        info_window = ctk.CTkToplevel(self)
        info_window.title("Información del Grafo")
        info_window.geometry("600x700")

        # Frame con scrollbar
        frame = ctk.CTkScrollableFrame(info_window, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Mostrar texto
        text_label = ctk.CTkLabel(
            frame,
            text=info_text,
            justify="left",
            font=("Consolas", 10),
            text_color="#000000"
        )
        text_label.pack(fill="both", expand=True, padx=10, pady=10)

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

                self.directed_var.set(self.graph.is_directed)
                self.weights_var.set(self.graph.has_weights)
                self.weight_entry.configure(state="normal" if self.weights_var.get() else "disabled")

                self.update_comboboxes()
                self.draw_graph()
                messagebox.showinfo("Éxito", "Grafo cargado exitosamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar: {str(e)}")

    def clear_all(self):
        """Limpia todo"""
        if messagebox.askyesno("Confirmar", "¿Limpiar todo el grafo?"):
            self.graph = GraphTheory()
            self.graph_pos = None
            self.directed_var.set(False)
            self.weights_var.set(False)
            self.weight_entry.configure(state="disabled")
            self.update_comboboxes()
            self.draw_graph()
            self.show_status("✓ Grafo limpiado")
