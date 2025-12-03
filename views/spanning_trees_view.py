"""
Vista de Árboles de Expansión
Interfaz para MST, centros y distancias entre árboles
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
from spanning_trees import WeightedGraph


class SpanningTreesContent(ctk.CTkFrame):
    """Contenido para árboles de expansión"""

    title = "Árboles de Expansión"

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.graph = WeightedGraph()
        self.current_tree = None  # Árbol actual para visualización
        self.graph_pos = None  # Posición fija del grafo para mantener la forma

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

        # ===== 0. OPCIONES DEL GRAFO =====
        self.create_section(controls, "⚙️ 0. Opciones del Grafo")

        # Checkbox para dirigido
        self.is_directed_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            controls,
            text="Grafo Dirigido",
            variable=self.is_directed_var,
            command=self.on_graph_option_changed
        ).pack(fill="x", padx=10, pady=5)

        # Checkbox para pesos
        self.has_weights_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            controls,
            text="Con Pesos",
            variable=self.has_weights_var,
            command=self.on_graph_option_changed
        ).pack(fill="x", padx=10, pady=5)

        # ===== 1. SE LE DEBEN PEDIR AL USUARIO LOS DATOS DEL GRAFO =====
        self.create_section(controls, "🔨 1. Datos del Grafo")

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

        ctk.CTkLabel(controls, text="Arista Ponderada:", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
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

        ctk.CTkLabel(controls, text="Peso:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.edge_weight_entry = ctk.CTkEntry(controls, placeholder_text="Peso (ej: 5)")
        self.edge_weight_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="➕ Agregar Arista",
            command=self.add_edge,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=5)

        # ===== 1.5 EDICIÓN DEL GRAFO =====
        self.create_section(controls, "✏️ 1.5 Edición del Grafo")

        ctk.CTkLabel(controls, text="Vértice a Eliminar:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.delete_vertex_var = ctk.StringVar(value="")
        self.delete_vertex_combo = ctk.CTkComboBox(
            controls,
            variable=self.delete_vertex_var,
            values=[]
        )
        self.delete_vertex_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="🗑️ Eliminar Vértice",
            command=self.delete_vertex,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(controls, text="Arista a Eliminar:", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        self.delete_edge_var = ctk.StringVar(value="")
        self.delete_edge_combo = ctk.CTkComboBox(
            controls,
            variable=self.delete_edge_var,
            values=[]
        )
        self.delete_edge_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="🗑️ Eliminar Arista",
            command=self.delete_edge,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(controls, text="Arista a Modificar:", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        self.edit_edge_var = ctk.StringVar(value="")
        self.edit_edge_combo = ctk.CTkComboBox(
            controls,
            variable=self.edit_edge_var,
            values=[]
        )
        self.edit_edge_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="📝 Modificar Arista",
            command=self.edit_edge,
            fg_color="#f39c12",
            hover_color="#e67e22"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="ℹ️ Ver Información del Grafo",
            command=self.show_graph_info,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(fill="x", padx=10, pady=5)

        # ===== 2. EN BASE A ESE GRAFO SE DEBE GENERAR EL ÁRBOL MÍNIMO Y EL COMPLEMENTO =====
        self.create_section(controls, "🌳 2. Árbol Mínimo y Complemento")

        ctk.CTkButton(
            controls,
            text="Generar Árbol Mínimo (MST)",
            command=lambda: self.calculate_mst("kruskal"),
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="📊 Ver 3 Grafos (Original, MST, Complemento)",
            command=self.show_three_graphs,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            controls,
            text="árbol + complemento = grafo",
            font=("Segoe UI", 10, "italic"),
            text_color="#95a5a6"
        ).pack(fill="x", padx=10, pady=(0, 5))

        # ===== 3. DEL ÁRBOL SE SACAN LAS RAMAS, DEL COMPLEMENTO SE SACAN LAS CUERDAS =====
        self.create_section(controls, "🌿 3. Ramas y Cuerdas")

        ctk.CTkButton(
            controls,
            text="Identificar Ramas y Cuerdas",
            command=self.identify_branches_chords,
            fg_color="#16a085",
            hover_color="#138f7a"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            controls,
            text="Ramas: aristas del árbol\nCuerdas: aristas del complemento",
            font=("Segoe UI", 9, "italic"),
            text_color="#95a5a6"
        ).pack(fill="x", padx=10, pady=(0, 5))

        # ===== 4. SEÑALAR EL CENTRO DEL ÁRBOL =====
        self.create_section(controls, "🎯 4. Centro del Árbol")

        ctk.CTkButton(
            controls,
            text="Calcular Centro",
            command=self.calculate_center,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(fill="x", padx=10, pady=5)

        # ===== 5. ALGORITMO DE FLOYD =====
        self.create_section(controls, "🔍 5. Algoritmo de Floyd")

        ctk.CTkButton(
            controls,
            text="Ejecutar Floyd-Warshall",
            command=self.run_floyd_warshall,
            fg_color="#c0392b",
            hover_color="#a93226"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            controls,
            text="Encuentra caminos más cortos",
            font=("Segoe UI", 9, "italic"),
            text_color="#95a5a6"
        ).pack(fill="x", padx=10, pady=(0, 5))

        ctk.CTkButton(
            controls,
            text="📍 Hallar Mediana",
            command=self.find_and_show_median,
            fg_color="#16a085",
            hover_color="#138f7a"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            controls,
            text="Vértices con suma mínima de distancias",
            font=("Segoe UI", 9, "italic"),
            text_color="#95a5a6"
        ).pack(fill="x", padx=10, pady=(0, 5))

        # ===== 6. MOSTRAR TABLA CON BOTONES =====
        self.create_section(controls, "📊 6. Tabla de Análisis")

        ctk.CTkButton(
            controls,
            text="Mostrar Tabla con Botones",
            command=self.show_analysis_table,
            fg_color="#c0392b",
            hover_color="#a93226"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            controls,
            text="Excentricidad, radio, distancias...",
            font=("Segoe UI", 9, "italic"),
            text_color="#95a5a6"
        ).pack(fill="x", padx=10, pady=(0, 5))

        # ===== UTILIDADES =====
        self.create_section(controls, "🔧 Utilidades")

        ctk.CTkButton(
            controls,
            text="📥 Cargar desde Matrices",
            command=self.load_from_matrices,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=5)

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
            text="📊 Grafo Ponderado",
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
        self.update_edit_dropdowns()

        self.draw_graph()
        self.show_status(f"✓ Vértice '{vertex}' agregado")

    def add_edge(self):
        """Agrega una arista ponderada al grafo"""
        edge_name = self.edge_name_entry.get().strip()
        v1 = self.edge_v1_var.get().strip()
        v2 = self.edge_v2_var.get().strip()
        weight_str = self.edge_weight_entry.get().strip()

        if not edge_name or not v1 or not v2 or not weight_str:
            messagebox.showwarning("Advertencia", "Completa todos los campos")
            return

        try:
            weight = float(weight_str)
        except ValueError:
            messagebox.showerror("Error", "El peso debe ser un número")
            return

        if edge_name in self.graph.edges:
            messagebox.showwarning("Advertencia", f"La arista '{edge_name}' ya existe")
            return

        if not self.graph.add_edge(edge_name, v1, v2, weight):
            messagebox.showerror("Error", "Verifica que los vértices existan")
            return

        self.edge_name_entry.delete(0, 'end')
        self.edge_v1_var.set("")
        self.edge_v2_var.set("")
        self.edge_weight_entry.delete(0, 'end')
        self.draw_graph()
        self.show_status(f"✓ Arista '{edge_name}' agregada")

    # ==================== OPCIONES DEL GRAFO ====================

    def on_graph_option_changed(self):
        """Actualiza las opciones del grafo cuando se cambian los checkboxes"""
        self.graph.is_directed = self.is_directed_var.get()
        self.graph.has_weights = self.has_weights_var.get()

    # ==================== EDICIÓN ====================

    def update_edit_dropdowns(self):
        """Actualiza las listas desplegables de edición"""
        vertices_list = sorted(list(self.graph.vertices))
        self.delete_vertex_combo.configure(values=vertices_list)

        edges_list = sorted(list(self.graph.edges.keys()))
        self.delete_edge_combo.configure(values=edges_list)
        self.edit_edge_combo.configure(values=edges_list)

    def delete_vertex(self):
        """Elimina un vértice"""
        vertex = self.delete_vertex_var.get().strip()
        if not vertex:
            messagebox.showwarning("Advertencia", "Selecciona un vértice para eliminar")
            return

        if vertex not in self.graph.vertices:
            messagebox.showwarning("Advertencia", f"El vértice '{vertex}' no existe")
            return

        if messagebox.askyesno("Confirmar", f"¿Eliminar vértice '{vertex}' y sus aristas?"):
            self.graph.remove_vertex(vertex)
            self.delete_vertex_var.set("")
            self.update_edit_dropdowns()
            self.edge_v1_combo.configure(values=sorted(list(self.graph.vertices)))
            self.edge_v2_combo.configure(values=sorted(list(self.graph.vertices)))
            self.draw_graph()
            self.show_status(f"✓ Vértice '{vertex}' eliminado")

    def delete_edge(self):
        """Elimina una arista"""
        edge_name = self.delete_edge_var.get().strip()
        if not edge_name:
            messagebox.showwarning("Advertencia", "Selecciona una arista para eliminar")
            return

        if edge_name not in self.graph.edges:
            messagebox.showwarning("Advertencia", f"La arista '{edge_name}' no existe")
            return

        if messagebox.askyesno("Confirmar", f"¿Eliminar arista '{edge_name}'?"):
            self.graph.remove_edge(edge_name)
            self.delete_edge_var.set("")
            self.update_edit_dropdowns()
            self.draw_graph()
            self.show_status(f"✓ Arista '{edge_name}' eliminada")

    def edit_edge(self):
        """Modifica el peso de una arista"""
        edge_name = self.edit_edge_var.get().strip()
        if not edge_name:
            messagebox.showwarning("Advertencia", "Selecciona una arista para modificar")
            return

        if edge_name not in self.graph.edges:
            messagebox.showwarning("Advertencia", f"La arista '{edge_name}' no existe")
            return

        # Crear ventana de diálogo
        edit_window = ctk.CTkToplevel(self)
        edit_window.title(f"Modificar Arista {edge_name}")
        edit_window.geometry("300x150")
        edit_window.resizable(False, False)

        v1, v2, current_weight = self.graph.edges[edge_name]

        ctk.CTkLabel(edit_window, text=f"Arista: {edge_name}").pack(pady=10, padx=10)
        ctk.CTkLabel(edit_window, text=f"Vértices: {v1} - {v2}").pack(pady=(0, 10), padx=10)

        ctk.CTkLabel(edit_window, text="Nuevo peso:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        weight_entry = ctk.CTkEntry(edit_window, placeholder_text=f"Actual: {current_weight}")
        weight_entry.pack(fill="x", padx=10, pady=5)

        def apply_changes():
            try:
                new_weight = float(weight_entry.get())
                self.graph.edit_edge(edge_name, new_weight)
                self.edit_edge_var.set("")
                self.draw_graph()
                self.show_status(f"✓ Arista '{edge_name}' modificada")
                edit_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "El peso debe ser un número")

        ctk.CTkButton(
            edit_window,
            text="Aplicar",
            command=apply_changes,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(fill="x", padx=10, pady=10)

    def show_graph_info(self):
        """Muestra información detallada del grafo"""
        if len(self.graph.vertices) == 0:
            messagebox.showinfo("Información", "El grafo está vacío")
            return

        info = self.graph.get_graph_info()

        output = "INFORMACIÓN DEL GRAFO\n"
        output += "=" * 50 + "\n\n"

        output += f"Vértices: {info['num_vertices']}\n"
        output += f"Aristas: {info['num_edges']}\n"
        output += f"Dirigido: {'Sí' if info['is_directed'] else 'No'}\n"
        output += f"Con Pesos: {'Sí' if info['has_weights'] else 'No'}\n"
        output += f"Conexo: {'Sí' if info['is_connected'] else 'No'}\n"
        output += f"Peso Total: {info['total_weight']:.2f}\n\n"

        output += "VÉRTICES:\n"
        output += ", ".join(info['vertices']) + "\n\n"

        output += "ARISTAS:\n"
        for edge in info['edges']:
            output += f"  {edge['name']}: {edge['v1']} - {edge['v2']}"
            if info['has_weights']:
                output += f" (peso: {edge['weight']:.2f})"
            output += "\n"

        output += "\nGRADO DE CADA VÉRTICE:\n"
        for vertex, degree in sorted(info['degrees'].items()):
            output += f"  {vertex}: {degree}\n"

        self.show_results(output)
        self.notebook.set("Resultados")

    # ==================== ÁRBOLES GENERADORES ====================

    def calculate_mst(self, algorithm: str):
        """Calcula el árbol generador mínimo y muestra el complemento"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        result = self.graph.minimum_spanning_tree(algorithm)

        if not result["success"]:
            messagebox.showerror("Error", result["error"])
            return

        # Guardar árbol actual
        self.current_tree = set(result["edge_names"])

        # Calcular complemento
        complement = self.graph.get_complement_graph()
        complement_edges = set(complement.edges.keys())

        output = f"ÁRBOL GENERADOR MÍNIMO ({algorithm.upper()})\n\n"
        output += f"Peso total del árbol: {result['total_weight']:.2f}\n"
        output += f"Número de aristas del árbol: {result['num_edges']}\n\n"
        output += "Aristas del árbol:\n"

        for edge in result["tree_edges"]:
            v1, v2 = edge["vertices"]
            output += f"  {edge['name']}: {v1} - {v2} (peso: {edge['weight']:.2f})\n"

        output += f"\n\nCOMPLEMENTO DEL GRAFO\n"
        output += f"Número de aristas del complemento: {len(complement_edges)}\n\n"
        output += "Aristas del complemento:\n"

        if complement_edges:
            for edge_name in sorted(complement_edges):
                v1, v2, weight = complement.edges[edge_name]
                output += f"  {edge_name}: {v1} - {v2}\n"
        else:
            output += "  (El complemento está vacío - el grafo original es completo)\n"

        output += f"\n\nFÓRMULA: Árbol + Complemento = Grafo Original\n"
        output += f"{result['num_edges']} + {len(complement_edges)} = {len(self.graph.edges)}\n"

        self.show_results(output)
        self.draw_graph(highlight_edges=self.current_tree)
        self.notebook.set("Resultados")

    def show_three_graphs(self):
        """Muestra 3 grafos en una ventana: Original, MST, Complemento del MST"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        # Calcular MST
        mst_result = self.graph.minimum_spanning_tree()
        if not mst_result["success"]:
            messagebox.showerror("Error", mst_result["error"])
            return

        # Crear un grafo con solo las aristas del MST
        mst_graph = WeightedGraph(
            is_directed=self.graph.is_directed,
            has_weights=self.graph.has_weights
        )
        mst_graph.vertices = self.graph.vertices.copy()

        # Agregar solo las aristas del MST
        for edge_name in mst_result["edge_names"]:
            if edge_name in self.graph.edges:
                v1, v2, weight = self.graph.edges[edge_name]
                mst_graph.add_edge(edge_name, v1, v2, weight)

        # Obtener el complemento del MST (aristas que no están en el MST)
        complement = mst_graph.get_complement_graph()

        # Crear ventana
        window = ctk.CTkToplevel(self)
        window.title("Visualización de Grafos: Original, MST, Complemento")
        window.geometry("1400x600")

        # Frame principal
        main_frame = ctk.CTkFrame(window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        # Función auxiliar para crear cada subfigura
        def create_graph_display(parent, title, graph_obj, highlight_edges=None):
            frame = ctk.CTkFrame(parent, fg_color="#f0f0f0")
            frame.pack(fill="both", expand=True, side="left", padx=5, pady=5)

            # Título
            ctk.CTkLabel(
                frame,
                text=title,
                font=("Segoe UI", 12, "bold"),
                text_color="#000000"
            ).pack(pady=10)

            # Información
            info_text = f"Vértices: {len(graph_obj.vertices)}\nAristas: {len(graph_obj.edges)}"
            ctk.CTkLabel(
                frame,
                text=info_text,
                font=("Segoe UI", 10),
                text_color="#333333"
            ).pack(pady=5)

            # Canvas de matplotlib
            fig, ax = plt.subplots(figsize=(4.5, 5), facecolor='#f0f0f0')
            ax.set_facecolor('#f0f0f0')

            if len(graph_obj.vertices) > 0:
                G = nx.Graph()
                G.add_nodes_from(graph_obj.vertices)

                edge_labels = {}
                for edge_name, (v1, v2, weight) in graph_obj.edges.items():
                    G.add_edge(v1, v2, name=edge_name, weight=weight)
                    edge_labels[(v1, v2)] = f"{edge_name}"

                pos = nx.circular_layout(G)

                # Dibujar nodos
                nx.draw_networkx_nodes(
                    G, pos, ax=ax,
                    node_color='#3498db',
                    node_size=600,
                    alpha=0.9
                )

                # Dibujar aristas
                if highlight_edges:
                    normal_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('name') not in highlight_edges]
                    highlight_edges_list = [(u, v) for u, v, d in G.edges(data=True) if d.get('name') in highlight_edges]

                    if normal_edges:
                        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=normal_edges, edge_color='#95a5a6', width=1.5, alpha=0.3)
                    if highlight_edges_list:
                        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=highlight_edges_list, edge_color='#2ecc71', width=2.5, alpha=0.9)
                else:
                    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='#95a5a6', width=2, alpha=0.6)

                # Dibujar etiquetas
                nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold', font_color='white')

                ax.axis('off')

            canvas = FigureCanvasTkAgg(fig, frame)
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)

        # Crear 3 subfiguras
        create_graph_display(main_frame, "Grafo Original", self.graph)
        create_graph_display(main_frame, "Árbol Mínimo (MST)", mst_graph)
        create_graph_display(main_frame, "Complemento del MST", complement)

    # ==================== CENTRO Y CENTROIDE ====================

    def calculate_center(self):
        """Calcula el centro del grafo basándose en excentricidades"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo para calcular el centro")
            return

        result = self.graph.find_tree_center()

        if not result["success"]:
            messagebox.showerror("Error", result.get("error", "Error desconocido"))
            return

        output = "CENTRO DEL GRAFO (Basado en Excentricidades)\n"
        output += "=" * 50 + "\n\n"

        center_vertices = result["center_vertices"]
        radius = result["radius"]

        if result["is_center"]:
            output += f"✓ CENTRO: {center_vertices[0]}\n\n"
            output += "Tipo: CENTRO (1 vértice central)\n"
            output += "El grafo tiene un único vértice central\n\n"
        elif result["is_bicentro"]:
            output += f"✓ BICENTRO: {', '.join(center_vertices)}\n\n"
            output += "Tipo: BICENTRO (2 vértices centrales)\n"
            if result["is_connected_bicentro"]:
                output += f"Los vértices centrales están conectados por una arista\n\n"
            else:
                output += f"Los vértices centrales NO están conectados directamente\n\n"
        else:
            output += f"Centro: {', '.join(center_vertices)}\n\n"

        output += f"Número de vértices en el centro: {result['num_centers']}\n"
        output += f"Radio del grafo (excentricidad mínima): {radius}\n\n"

        output += "Excentricidades de cada vértice:\n"
        for vertex in sorted(result["eccentricities"].keys()):
            ecc = result["eccentricities"][vertex]
            marker = " ⭐ CENTRO" if vertex in center_vertices else ""
            output += f"  {vertex}: {ecc}{marker}\n"

        output += "\nAlgoritmo: Floyd-Warshall\n"
        output += "El centro es el conjunto de vértices con excentricidad igual al radio\n"

        self.show_results(output)
        self.notebook.set("Resultados")

        # Resaltar vértices del centro
        self.draw_graph(highlight_vertices=set(center_vertices))

    # ==================== RAMAS Y CUERDAS ====================

    def identify_branches_chords(self):
        """Identifica ramas del árbol y cuerdas del complemento"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        # Si ya hay un árbol calculado, usarlo; sino calcular MST
        tree_edges = self.current_tree if self.current_tree else None

        result = self.graph.identify_branches_and_chords(tree_edges)

        if not result["success"]:
            messagebox.showerror("Error", result["error"])
            return

        output = "RAMAS Y CUERDAS DEL GRAFO\n\n"

        output += f"RAMAS (Aristas del árbol): {result['num_branches']}\n"
        if result["branches"]:
            for branch in result["branches"]:
                v1, v2 = branch["vertices"]
                output += f"  {branch['name']}: {v1} - {v2} (peso: {branch['weight']:.2f})\n"
        else:
            output += "  (ninguna)\n"

        output += f"\nCUERDAS (Aristas del complemento): {result['num_chords']}\n"
        if result["chords"]:
            for chord in result["chords"]:
                v1, v2 = chord["vertices"]
                output += f"  {chord['name']}: {v1} - {v2} (peso: {chord['weight']:.2f})\n"
        else:
            output += "  (ninguna)\n"

        output += f"\nTotal de aristas: {result['num_branches'] + result['num_chords']}\n"

        self.show_results(output)

        # Actualizar árbol actual y visualizar
        self.current_tree = result["tree_edges"]

        # Preparar conjuntos de nombres de aristas para visualización
        branch_names = set(branch["name"] for branch in result["branches"])
        chord_names = set(chord["name"] for chord in result["chords"])

        self.draw_graph(branches=branch_names, chords=chord_names)
        self.notebook.set("Resultados")

    # ==================== ALGORITMO DE FLOYD-WARSHALL ====================

    def run_floyd_warshall(self):
        """Ejecuta el algoritmo de Floyd-Warshall"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        result = self.graph.floyd_warshall()

        if not result["success"]:
            messagebox.showerror("Error", result["error"])
            return

        vertices = result["vertices"]
        dist_matrix = result["distance_matrix"]

        output = "ALGORITMO DE FLOYD-WARSHALL\n\n"
        output += "Matriz de distancias más cortas:\n\n"

        # Encabezado
        output += "      " + "  ".join(f"{v:>6}" for v in vertices) + "\n"
        output += "    " + "-" * (8 * len(vertices)) + "\n"

        # Filas
        for i, v in enumerate(vertices):
            output += f"{v:>4} |"
            for j in range(len(vertices)):
                dist = dist_matrix[i][j]
                if dist == float('inf'):
                    output += "    ∞ "
                else:
                    output += f"{dist:>6.1f}"
            output += "\n"

        output += f"\nRadio del grafo: {result['radius']:.2f}\n"
        output += f"Diámetro del grafo: {result['diameter']:.2f}\n\n"

        output += "Excentricidades:\n"
        for v, ecc in result["eccentricities"].items():
            if ecc is not None:
                output += f"  {v}: {ecc:.2f}\n"

        self.show_results(output)
        self.notebook.set("Resultados")

    def find_and_show_median(self):
        """Encuentra la mediana del grafo y muestra información"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        result = self.graph.find_median()

        if not result["success"]:
            messagebox.showerror("Error", result["error"])
            return

        output = "MEDIANA DEL GRAFO\n"
        output += "=" * 50 + "\n\n"

        median_vertices = result["median_vertices"]
        if result["num_medians"] == 1:
            output += f"✓ Mediana: {median_vertices[0]}\n\n"
        else:
            output += f"✓ Medianas: {', '.join(median_vertices)}\n\n"

        output += f"Suma mínima de distancias: {result['min_distance_sum']:.2f}\n\n"

        output += "Suma de distancias por vértice:\n"
        for vertex in sorted(result["distance_sums"].keys()):
            dist_sum = result["distance_sums"][vertex]
            marker = " ⭐ MEDIANA" if vertex in median_vertices else ""
            output += f"  {vertex}: {dist_sum:.2f}{marker}\n"

        # Crear subgrafo de la mediana
        try:
            median_subgraph = self.graph.get_subgraph(set(median_vertices))
            output += f"\n\nSubgrafo de la mediana:\n"
            output += f"Vértices: {', '.join(sorted(list(median_subgraph.vertices)))}\n"
            output += f"Aristas: {len(median_subgraph.edges)}\n"
            if median_subgraph.edges:
                for edge_name, (v1, v2, weight) in sorted(median_subgraph.edges.items()):
                    output += f"  {edge_name}: {v1} - {v2}"
                    if self.graph.has_weights:
                        output += f" (peso: {weight:.2f})"
                    output += "\n"
        except:
            pass

        self.show_results(output)
        self.notebook.set("Resultados")

        # Resaltar vértices de la mediana
        self.draw_graph(highlight_vertices=set(median_vertices))

    def show_analysis_table(self):
        """Muestra tabla interactiva de análisis completo"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        result = self.graph.get_analysis_table()

        if not result["success"]:
            messagebox.showerror("Error", result["error"])
            return

        # Crear ventana de tabla
        table_window = ctk.CTkToplevel(self)
        table_window.title("Tabla de Análisis del Grafo")
        table_window.geometry("1000x700")

        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(table_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Título
        title_frame = ctk.CTkFrame(main_frame, fg_color="#1a1a1a", corner_radius=0)
        title_frame.pack(fill="x", padx=0, pady=0)

        ctk.CTkLabel(
            title_frame,
            text="📊 ANÁLISIS COMPLETO DEL GRAFO",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=15, padx=20)

        # Información general en tabla formateada
        info_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b", corner_radius=10)
        info_frame.pack(fill="x", pady=10, padx=15)

        info_frame.grid_columnconfigure(0, weight=1)
        info_frame.grid_columnconfigure(1, weight=1)
        info_frame.grid_columnconfigure(2, weight=1)
        info_frame.grid_columnconfigure(3, weight=1)

        # Encabezados y datos
        stats = [
            ("Radio ⭐", f"{result['radius']:.2f}"),
            ("Diámetro 📏", f"{result['diameter']:.2f}"),
            ("Centro", ', '.join(result['center_vertices'])),
            ("Centroide", ', '.join(result['centroid_vertices']))
        ]

        for idx, (label, value) in enumerate(stats):
            col = idx % 4
            row = idx // 4

            ctk.CTkLabel(
                info_frame,
                text=label + ":",
                font=("Segoe UI", 11, "bold"),
                text_color="#95a5a6"
            ).grid(row=row*2, column=col, padx=15, pady=(10, 2), sticky="w")

            ctk.CTkLabel(
                info_frame,
                text=value,
                font=("Segoe UI", 12, "bold"),
                text_color="#ecf0f1"
            ).grid(row=row*2+1, column=col, padx=15, pady=(2, 10), sticky="w")

        # Separador
        separator = ctk.CTkFrame(main_frame, fg_color="#3a3a3a", height=1)
        separator.pack(fill="x", pady=15, padx=15)

        # Tabla de vértices con encabezado
        table_header_frame = ctk.CTkFrame(main_frame, fg_color="#1f1f1f", corner_radius=8)
        table_header_frame.pack(fill="x", pady=(10, 0), padx=15)

        table_header_frame.grid_columnconfigure(0, weight=1, minsize=80)
        table_header_frame.grid_columnconfigure(1, weight=1, minsize=100)
        table_header_frame.grid_columnconfigure(2, weight=1, minsize=120)
        table_header_frame.grid_columnconfigure(3, weight=2, minsize=200)
        table_header_frame.grid_columnconfigure(4, weight=1, minsize=150)

        headers = ["Vértice", "Excentricidad", "Suma Dist.", "Tipo", "Acciones"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                table_header_frame,
                text=header,
                font=("Segoe UI", 11, "bold"),
                text_color="#ecf0f1",
                fg_color="#2b2b2b",
                corner_radius=0
            ).grid(row=0, column=col, padx=10, pady=12, sticky="ew")

        # Tabla de vértices
        vertices = result["vertices"]
        vertex_analysis = result["vertex_analysis"]

        for idx, vertex in enumerate(vertices):
            data = vertex_analysis[vertex]

            # Alternar colores de fondo
            bg_color = "#2b2b2b" if idx % 2 == 0 else "#252525"

            row_frame = ctk.CTkFrame(main_frame, fg_color=bg_color, corner_radius=0)
            row_frame.pack(fill="x", padx=15, pady=1)

            row_frame.grid_columnconfigure(0, weight=1, minsize=80)
            row_frame.grid_columnconfigure(1, weight=1, minsize=100)
            row_frame.grid_columnconfigure(2, weight=1, minsize=120)
            row_frame.grid_columnconfigure(3, weight=2, minsize=200)
            row_frame.grid_columnconfigure(4, weight=1, minsize=150)

            # Vértice
            vertex_label = vertex
            if data["is_center"] or data["is_centroid"]:
                markers = []
                if data["is_center"]:
                    markers.append("★ CENTRO")
                if data["is_centroid"]:
                    markers.append("◆ CENTROIDE")
                vertex_label = f"{vertex} ({', '.join(markers)})"

            ctk.CTkLabel(
                row_frame,
                text=vertex_label,
                font=("Segoe UI", 11, "bold" if data["is_center"] or data["is_centroid"] else "normal"),
                text_color="#e67e22" if data["is_center"] or data["is_centroid"] else "#ecf0f1"
            ).grid(row=0, column=0, padx=10, pady=12, sticky="w")

            # Excentricidad
            ctk.CTkLabel(
                row_frame,
                text=f"{data['eccentricity']:.2f}",
                font=("Segoe UI", 11)
            ).grid(row=0, column=1, padx=10, pady=12, sticky="w")

            # Suma de distancias
            ctk.CTkLabel(
                row_frame,
                text=f"{data['sum_distances']:.2f}",
                font=("Segoe UI", 11)
            ).grid(row=0, column=2, padx=10, pady=12, sticky="w")

            # Tipo
            tipo_text = ""
            if data["is_center"] and data["is_centroid"]:
                tipo_text = "Centro y Centroide"
            elif data["is_center"]:
                tipo_text = "Centro"
            elif data["is_centroid"]:
                tipo_text = "Centroide"
            else:
                tipo_text = "Regular"

            ctk.CTkLabel(
                row_frame,
                text=tipo_text,
                font=("Segoe UI", 11)
            ).grid(row=0, column=3, padx=10, pady=12, sticky="w")

            # Acciones (botones)
            action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
            action_frame.grid(row=0, column=4, padx=10, pady=12, sticky="w")

            # Botón para mostrar distancias
            def show_distances(v=vertex, dists=data['distances']):
                dist_text = f"DISTANCIAS DESDE {v}:\n\n"
                for other_v in sorted(dists.keys()):
                    dist = dists[other_v]
                    if dist == 0:
                        dist_text += f"  {other_v}: 0\n"
                    elif dist == float('inf'):
                        dist_text += f"  {other_v}: ∞\n"
                    else:
                        dist_text += f"  {other_v}: {dist:.2f}\n"

                # Mostrar en ventana emergente
                dist_window = ctk.CTkToplevel(table_window)
                dist_window.title(f"Distancias desde {v}")
                dist_window.geometry("400x500")

                text_box = ctk.CTkTextbox(dist_window, font=("Consolas", 11))
                text_box.pack(fill="both", expand=True, padx=10, pady=10)
                text_box.insert("1.0", dist_text)
                text_box.configure(state="disabled")

            ctk.CTkButton(
                action_frame,
                text="Distancias",
                command=show_distances,
                width=90,
                height=28,
                font=("Segoe UI", 9),
                fg_color="#3498db",
                hover_color="#2980b9"
            ).pack(side="left", padx=2)

            # Botón para resaltar en grafo
            def highlight_vertex(v=vertex):
                self.draw_graph(highlight_vertices={v})
                table_window.lift()

            ctk.CTkButton(
                action_frame,
                text="Resaltar",
                command=highlight_vertex,
                width=80,
                height=28,
                font=("Segoe UI", 9),
                fg_color="#2ecc71",
                hover_color="#27ae60"
            ).pack(side="left", padx=2)

    # ==================== PERSISTENCIA ====================

    def show_graph_info(self):
        """Muestra información del grafo"""
        if len(self.graph.vertices) == 0:
            messagebox.showinfo("Info", "El grafo está vacío")
            return

        output = "INFORMACIÓN DEL GRAFO\n\n"
        output += f"Vértices: {len(self.graph.vertices)}\n"
        output += f"  {', '.join(sorted(self.graph.vertices))}\n\n"

        output += f"Aristas: {len(self.graph.edges)}\n"
        for edge_name, (v1, v2, weight) in sorted(self.graph.edges.items()):
            output += f"  {edge_name}: {v1} - {v2} (peso: {weight:.2f})\n"

        output += f"\nConexo: {'Sí' if self.graph.is_connected() else 'No'}\n"

        if self.graph.is_connected():
            # Calcular peso total
            total_weight = sum(w for _, _, w in self.graph.edges.values())
            output += f"Peso total de todas las aristas: {total_weight:.2f}\n"

        self.show_results(output)
        self.notebook.set("Resultados")

    # ==================== VISUALIZACIÓN ====================

    def draw_graph(self, highlight_edges=None, highlight_vertices=None, branches=None, chords=None):
        """Dibuja el grafo ponderado con posición fija

        Args:
            highlight_edges: conjunto de nombres de aristas a destacar (color verde)
            highlight_vertices: conjunto de vértices a destacar (color rojo)
            branches: conjunto de nombres de aristas que son ramas (color azul)
            chords: conjunto de nombres de aristas que son cuerdas (color naranja)
        """
        self.ax.clear()

        if len(self.graph.vertices) == 0:
            self.ax.text(
                0.5, 0.5,
                'Agrega vértices y aristas ponderadas\npara visualizar el grafo',
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
        for edge_name, (v1, v2, weight) in self.graph.edges.items():
            G.add_edge(v1, v2, name=edge_name, weight=weight)
            edge_labels[(v1, v2)] = f"{edge_name}\n({weight:.1f})"

        # Calcular o reutilizar posición del grafo
        # Si el conjunto de vértices cambió, recalcular
        current_vertices = set(self.graph.vertices)

        if self.graph_pos is None:
            # Primera vez o después de limpiar - usar layout circular para simetría
            self.graph_pos = nx.circular_layout(G)
        else:
            # Verificar si hay vértices nuevos o eliminados
            stored_vertices = set(self.graph_pos.keys())

            if current_vertices != stored_vertices:
                # Hay cambios en vértices - recalcular layout circular completo
                self.graph_pos = nx.circular_layout(G)

        pos = self.graph_pos

        # Colores de vértices
        node_colors = []
        for node in G.nodes():
            if highlight_vertices and node in highlight_vertices:
                node_colors.append('#e74c3c')  # Rojo para destacados
            else:
                node_colors.append('#3498db')  # Azul normal

        nx.draw_networkx_nodes(
            G, pos, ax=self.ax,
            node_color=node_colors,
            node_size=800,
            alpha=0.9
        )

        # Colores de aristas
        if branches or chords or highlight_edges:
            # Categorizar aristas
            branch_edges = []
            chord_edges = []
            highlight_edges_list = []
            normal_edges = []

            for u, v, data in G.edges(data=True):
                edge_name = data.get('name')

                if branches and edge_name in branches:
                    branch_edges.append((u, v))
                elif chords and edge_name in chords:
                    chord_edges.append((u, v))
                elif highlight_edges and edge_name in highlight_edges:
                    highlight_edges_list.append((u, v))
                else:
                    normal_edges.append((u, v))

            # Dibujar aristas normales (grises claros)
            if normal_edges:
                nx.draw_networkx_edges(
                    G, pos, ax=self.ax,
                    edgelist=normal_edges,
                    edge_color='#95a5a6',
                    width=1.5,
                    alpha=0.3
                )

            # Dibujar ramas (azul)
            if branch_edges:
                nx.draw_networkx_edges(
                    G, pos, ax=self.ax,
                    edgelist=branch_edges,
                    edge_color='#3498db',
                    width=3,
                    alpha=0.9
                )

            # Dibujar cuerdas (naranja)
            if chord_edges:
                nx.draw_networkx_edges(
                    G, pos, ax=self.ax,
                    edgelist=chord_edges,
                    edge_color='#e67e22',
                    width=3,
                    alpha=0.9
                )

            # Dibujar aristas destacadas (verde)
            if highlight_edges_list:
                nx.draw_networkx_edges(
                    G, pos, ax=self.ax,
                    edgelist=highlight_edges_list,
                    edge_color='#2ecc71',
                    width=3,
                    alpha=0.9
                )
        else:
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
            font_size=8,
            font_color='#000000'
        )

        title = f"Vértices: {len(self.graph.vertices)}, Aristas: {len(self.graph.edges)}"
        if self.graph.is_connected():
            title += " (Conexo)"

        self.ax.set_title(
            title,
            color='white',
            fontsize=14,
            fontweight='bold'
        )

        # Agregar leyenda si hay ramas o cuerdas
        if branches or chords:
            legend_text = "Leyenda: "
            if branches:
                legend_text += "🔵 Ramas (Azul)"
            if branches and chords:
                legend_text += " | "
            if chords:
                legend_text += "🟠 Cuerdas (Naranja)"

            self.ax.text(
                0.02, 0.98, legend_text,
                transform=self.ax.transAxes,
                fontsize=10,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='#2b2b2b', alpha=0.8, edgecolor='#95a5a6'),
                color='white'
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
        self.after(3000, lambda: self.viz_title.configure(text="📊 Grafo Ponderado"))

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
                    self.graph = WeightedGraph.from_json(f.read())
                self.current_tree = None
                self.draw_graph()
                self.update_edit_dropdowns()
                messagebox.showinfo("Éxito", "Grafo cargado exitosamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar: {str(e)}")

    def load_from_matrices(self):
        """Carga un grafo desde la sección de operaciones de matrices"""
        filename = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Cargar Grafo desde Matrices"
        )

        if not filename:
            return

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                import json
                data = json.load(f)

            # Convertir desde formato GraphData a WeightedGraph
            # El archivo puede contener múltiples grafos, usamos el primero
            if isinstance(data, dict) and "graphs" in data:
                graph_data = data["graphs"][0] if data.get("graphs") else None
            elif isinstance(data, dict):
                graph_data = data
            else:
                graph_data = None

            if not graph_data or not isinstance(graph_data, dict):
                messagebox.showerror("Error", "El archivo no contiene grafos válidos")
                return

            # Crear nuevo WeightedGraph
            self.graph = WeightedGraph()
            self.graph.vertices = set(graph_data.get("vertices", []))

            # Procesar aristas - manejar diferentes formatos
            edges = graph_data.get("edges", [])
            if isinstance(edges, list):
                for i, edge_item in enumerate(edges):
                    if isinstance(edge_item, dict):
                        # Formato: {"name": "e1", "vertices": ["a", "b"]}
                        edge_name = edge_item.get("name", f"e{i+1}")
                        vertices = edge_item.get("vertices", [])
                        if len(vertices) >= 2:
                            weight = 1.0
                            self.graph.add_edge(edge_name, vertices[0], vertices[1], weight)

            self.current_tree = None
            self.is_directed_var.set(graph_data.get("is_directed", False))
            self.has_weights_var.set(graph_data.get("has_weights", True))
            self.on_graph_option_changed()

            # Actualizar UI
            vertices_list = sorted(list(self.graph.vertices))
            self.edge_v1_combo.configure(values=vertices_list)
            self.edge_v2_combo.configure(values=vertices_list)
            self.update_edit_dropdowns()

            self.draw_graph()
            messagebox.showinfo(
                "Éxito",
                f"Grafo cargado:\n{len(self.graph.vertices)} vértices\n{len(self.graph.edges)} aristas"
            )

        except json.JSONDecodeError:
            messagebox.showerror("Error", "El archivo no es JSON válido")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar desde matrices:\n{str(e)}")

    def clear_all(self):
        """Limpia todo"""
        if messagebox.askyesno("Confirmar", "¿Limpiar todo el grafo?"):
            self.graph = WeightedGraph()
            self.current_tree = None
            self.graph_pos = None  # Resetear posición del grafo
            self.draw_graph()
            self.results_text.delete("1.0", "end")
            self.show_status("✓ Grafo limpiado")
