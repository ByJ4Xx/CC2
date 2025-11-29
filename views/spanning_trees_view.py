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

        # ===== CONSTRUCCIÓN =====
        self.create_section(controls, "🔨 Construcción del Grafo")

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

        self.edge_v1_entry = ctk.CTkEntry(controls, placeholder_text="Vértice 1")
        self.edge_v1_entry.pack(fill="x", padx=10, pady=5)

        self.edge_v2_entry = ctk.CTkEntry(controls, placeholder_text="Vértice 2")
        self.edge_v2_entry.pack(fill="x", padx=10, pady=5)

        self.edge_weight_entry = ctk.CTkEntry(controls, placeholder_text="Peso (ej: 5)")
        self.edge_weight_entry.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="➕ Agregar Arista",
            command=self.add_edge,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=5)

        # ===== ÁRBOLES GENERADORES =====
        self.create_section(controls, "🌳 Árboles Generadores")

        ctk.CTkButton(
            controls,
            text="MST - Kruskal",
            command=lambda: self.calculate_mst("kruskal"),
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="MST - Prim",
            command=lambda: self.calculate_mst("prim"),
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Árbol Generador Máximo",
            command=self.calculate_maximum_tree,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(fill="x", padx=10, pady=5)

        # ===== CENTRO Y CENTROIDE =====
        self.create_section(controls, "🎯 Centro y Centroide")

        ctk.CTkButton(
            controls,
            text="Calcular Centro",
            command=self.calculate_center,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Calcular Centroide",
            command=self.calculate_centroid,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(fill="x", padx=10, pady=5)

        # ===== DISTANCIAS ENTRE ÁRBOLES =====
        self.create_section(controls, "📏 Distancia entre Árboles")

        ctk.CTkLabel(
            controls,
            text="⚠️ Genera todos los árboles\n(lento para grafos grandes)",
            font=("Segoe UI", 10),
            text_color="#e74c3c"
        ).pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls,
            text="Calcular Distancias",
            command=self.calculate_tree_distances,
            fg_color="#16a085",
            hover_color="#138f7a"
        ).pack(fill="x", padx=10, pady=5)

        # ===== UTILIDADES =====
        self.create_section(controls, "🔧 Utilidades")

        ctk.CTkButton(
            controls,
            text="ℹ️ Info del Grafo",
            command=self.show_graph_info,
            fg_color="#34495e",
            hover_color="#2c3e50"
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
        self.draw_graph()
        self.show_status(f"✓ Vértice '{vertex}' agregado")

    def add_edge(self):
        """Agrega una arista ponderada al grafo"""
        edge_name = self.edge_name_entry.get().strip()
        v1 = self.edge_v1_entry.get().strip()
        v2 = self.edge_v2_entry.get().strip()
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
        self.edge_v1_entry.delete(0, 'end')
        self.edge_v2_entry.delete(0, 'end')
        self.edge_weight_entry.delete(0, 'end')
        self.draw_graph()
        self.show_status(f"✓ Arista '{edge_name}' agregada")

    # ==================== ÁRBOLES GENERADORES ====================

    def calculate_mst(self, algorithm: str):
        """Calcula el árbol generador mínimo"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        result = self.graph.minimum_spanning_tree(algorithm)

        if not result["success"]:
            messagebox.showerror("Error", result["error"])
            return

        # Guardar árbol actual
        self.current_tree = set(result["edge_names"])

        output = f"ÁRBOL GENERADOR MÍNIMO ({algorithm.upper()})\n\n"
        output += f"Peso total: {result['total_weight']:.2f}\n"
        output += f"Número de aristas: {result['num_edges']}\n\n"
        output += "Aristas del árbol:\n"

        for edge in result["tree_edges"]:
            v1, v2 = edge["vertices"]
            output += f"  {edge['name']}: {v1} - {v2} (peso: {edge['weight']:.2f})\n"

        self.show_results(output)
        self.draw_graph(highlight_edges=self.current_tree)
        self.notebook.set("Resultados")

    def calculate_maximum_tree(self):
        """Calcula el árbol generador máximo"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        result = self.graph.maximum_spanning_tree()

        if not result["success"]:
            messagebox.showerror("Error", result["error"])
            return

        # Guardar árbol actual
        self.current_tree = set(result["edge_names"])

        output = "ÁRBOL GENERADOR MÁXIMO\n\n"
        output += f"Peso total: {result['total_weight']:.2f}\n"
        output += f"Número de aristas: {result['num_edges']}\n\n"
        output += "Aristas del árbol:\n"

        for edge in result["tree_edges"]:
            v1, v2 = edge["vertices"]
            output += f"  {edge['name']}: {v1} - {v2} (peso: {edge['weight']:.2f})\n"

        self.show_results(output)
        self.draw_graph(highlight_edges=self.current_tree)
        self.notebook.set("Resultados")

    # ==================== CENTRO Y CENTROIDE ====================

    def calculate_center(self):
        """Calcula el centro del grafo"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        result = self.graph.graph_center()

        if not result["success"]:
            messagebox.showerror("Error", result["error"])
            return

        output = "CENTRO DEL GRAFO\n\n"

        if result["num_centers"] == 1:
            output += f"Centro: {result['center_vertices'][0]}\n\n"
        else:
            output += f"Centros: {', '.join(result['center_vertices'])}\n\n"

        output += f"Radio: {result['radius']}\n"
        output += f"Diámetro: {result['diameter']}\n\n"
        output += "Excentricidades:\n"

        for vertex, ecc in result["eccentricity"].items():
            marker = " ⭐" if vertex in result["center_vertices"] else ""
            output += f"  {vertex}: {ecc}{marker}\n"

        self.show_results(output)
        self.draw_graph(highlight_vertices=set(result["center_vertices"]))
        self.notebook.set("Resultados")

    def calculate_centroid(self):
        """Calcula el centroide del grafo"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        result = self.graph.graph_centroid()

        if not result["success"]:
            messagebox.showerror("Error", result["error"])
            return

        output = "CENTROIDE DEL GRAFO\n\n"

        if result["num_centroids"] == 1:
            output += f"Centroide: {result['centroid_vertices'][0]}\n\n"
        else:
            output += f"Centroides: {', '.join(result['centroid_vertices'])}\n\n"

        output += f"Suma mínima de distancias: {result['min_distance_sum']}\n\n"
        output += "Suma de distancias por vértice:\n"

        for vertex, dist_sum in result["distance_sums"].items():
            marker = " ⭐" if vertex in result["centroid_vertices"] else ""
            output += f"  {vertex}: {dist_sum}{marker}\n"

        self.show_results(output)
        self.draw_graph(highlight_vertices=set(result["centroid_vertices"]))
        self.notebook.set("Resultados")

    # ==================== DISTANCIAS ENTRE ÁRBOLES ====================

    def calculate_tree_distances(self):
        """Calcula distancias entre todos los árboles de expansión"""
        if len(self.graph.vertices) == 0:
            messagebox.showwarning("Advertencia", "El grafo está vacío")
            return

        if not self.graph.is_connected():
            messagebox.showerror("Error", "El grafo debe ser conexo")
            return

        # Advertencia
        if len(self.graph.edges) > 12:
            if not messagebox.askyesno(
                "Advertencia",
                "El grafo tiene muchas aristas.\n"
                "Generar todos los árboles puede ser muy lento.\n"
                "¿Continuar?"
            ):
                return

        self.show_status("Calculando árboles... (puede tardar)")
        self.update()

        result = self.graph.all_tree_distances()

        if not result["success"]:
            messagebox.showerror("Error", result["error"])
            self.show_status("Error en cálculo")
            return

        output = "DISTANCIAS ENTRE ÁRBOLES DE EXPANSIÓN\n\n"
        output += f"Árboles de expansión encontrados: {result['num_trees']}\n"
        output += f"Pares de árboles: {result['num_pairs']}\n"
        output += f"Distancia mínima: {result['min_distance']}\n"
        output += f"Distancia máxima: {result['max_distance']}\n\n"

        if result["num_pairs"] <= 50:
            output += "Distancias entre pares:\n"
            for dist_info in result["distances"]:
                output += f"\nÁrbol {dist_info['tree1_id']} ↔ Árbol {dist_info['tree2_id']}: "
                output += f"distancia = {dist_info['distance']}\n"
                output += f"  Árbol {dist_info['tree1_id']}: {{{', '.join(dist_info['tree1_edges'])}}}\n"
                output += f"  Árbol {dist_info['tree2_id']}: {{{', '.join(dist_info['tree2_edges'])}}}\n"
        else:
            output += "\n(Mostrando primeros 50 pares)\n"
            for dist_info in result["distances"][:50]:
                output += f"Árbol {dist_info['tree1_id']} ↔ Árbol {dist_info['tree2_id']}: "
                output += f"{dist_info['distance']}\n"

        self.show_results(output)
        self.notebook.set("Resultados")
        self.show_status(f"✓ {result['num_trees']} árboles encontrados")

    # ==================== INFO Y UTILIDADES ====================

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

    def draw_graph(self, highlight_edges=None, highlight_vertices=None):
        """Dibuja el grafo ponderado"""
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
            return

        G = nx.Graph()
        G.add_nodes_from(self.graph.vertices)

        edge_labels = {}
        for edge_name, (v1, v2, weight) in self.graph.edges.items():
            G.add_edge(v1, v2, name=edge_name, weight=weight)
            edge_labels[(v1, v2)] = f"{edge_name}\n({weight:.1f})"

        pos = nx.spring_layout(G, k=2, iterations=50)

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
        if highlight_edges:
            # Dibujar aristas no destacadas
            normal_edges = []
            highlight_edges_list = []

            for u, v, data in G.edges(data=True):
                if data.get('name') in highlight_edges:
                    highlight_edges_list.append((u, v))
                else:
                    normal_edges.append((u, v))

            if normal_edges:
                nx.draw_networkx_edges(
                    G, pos, ax=self.ax,
                    edgelist=normal_edges,
                    edge_color='#95a5a6',
                    width=1.5,
                    alpha=0.3
                )

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
            font_color='#ecf0f1'
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
                messagebox.showinfo("Éxito", "Grafo cargado exitosamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar: {str(e)}")

    def clear_all(self):
        """Limpia todo"""
        if messagebox.askyesno("Confirmar", "¿Limpiar todo el grafo?"):
            self.graph = WeightedGraph()
            self.current_tree = None
            self.draw_graph()
            self.results_text.delete("1.0", "end")
            self.show_status("✓ Grafo limpiado")
