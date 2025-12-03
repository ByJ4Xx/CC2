"""
Vista de Operaciones con Grafos
Interfaz gráfica para operaciones algebraicas de teoría de grafos
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from typing import Optional, List, Dict
import sys
import os

# Importar el modelo
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'models'))
from graph_operations import GraphOperationsManager, GraphData, Edge


class GraphOperationsContent(ctk.CTkFrame):
    """Contenido principal para operaciones con grafos"""

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")

        self.manager = GraphOperationsManager()
        self.current_graph: Optional[GraphData] = None
        self.selected_graphs: List[GraphData] = []  # Para operaciones binarias
        self.graph_positions: Dict[int, Dict] = {}  # Almacenar posiciones de cada grafo

        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Dividir en tres columnas
        self.grid_columnconfigure(0, weight=0, minsize=200)  # Lista de grafos
        self.grid_columnconfigure(1, weight=1)  # Visualización
        self.grid_columnconfigure(2, weight=0, minsize=300)  # Controles
        self.grid_rowconfigure(0, weight=1)
        
        # ========== COLUMNA IZQUIERDA: Lista de Grafos ==========
        self.create_graphs_list()
        
        # ========== COLUMNA CENTRAL: Visualización ==========
        self.create_visualization_area()
        
        # ========== COLUMNA DERECHA: Controles ==========
        self.create_controls_area()
    
    def create_graphs_list(self):
        """Crea el panel de lista de grafos"""
        list_frame = ctk.CTkFrame(self, corner_radius=10)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        list_frame.grid_rowconfigure(1, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            list_frame,
            text="📚 Grafos",
            font=("Segoe UI", 16, "bold")
        )
        title.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        # Frame con scrollbar
        self.graphs_listbox = ctk.CTkScrollableFrame(list_frame, fg_color="transparent")
        self.graphs_listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Botones de gestión
        buttons_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        buttons_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            buttons_frame,
            text="➕ Nuevo Grafo",
            command=self.create_new_graph,
            fg_color="#2ecc71",
            hover_color="#27ae60"
        ).pack(fill="x", pady=2)
        
        ctk.CTkButton(
            buttons_frame,
            text="🗑️ Borrar Seleccionado",
            command=self.delete_selected_graph,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(fill="x", pady=2)
        
        ctk.CTkButton(
            buttons_frame,
            text="ℹ️ Info del Grafo",
            command=self.show_graph_info,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", pady=2)
        
        # Botones de archivo
        file_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        file_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        ctk.CTkButton(
            file_frame,
            text="💾 Guardar Todo",
            command=self.save_all_graphs,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(fill="x", pady=2)
        
        ctk.CTkButton(
            file_frame,
            text="📂 Cargar Todo",
            command=self.load_all_graphs,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        ).pack(fill="x", pady=2)
        
        ctk.CTkButton(
            file_frame,
            text="🗑️ Limpiar Todo",
            command=self.clear_all_graphs,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        ).pack(fill="x", pady=2)
    
    def create_visualization_area(self):
        """Crea el área de visualización del grafo"""
        viz_frame = ctk.CTkFrame(self, corner_radius=10)
        viz_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=0)
        viz_frame.grid_rowconfigure(1, weight=1)
        viz_frame.grid_columnconfigure(0, weight=1)
        
        # Título
        self.viz_title = ctk.CTkLabel(
            viz_frame,
            text="📊 Visualización del Grafo",
            font=("Segoe UI", 16, "bold")
        )
        self.viz_title.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Canvas de matplotlib
        self.fig, self.ax = plt.subplots(figsize=(8, 6), facecolor='#2b2b2b')
        self.ax.set_facecolor('#2b2b2b')
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        self.draw_empty_graph()
    
    def create_controls_area(self):
        """Crea el área de controles"""
        controls_frame = ctk.CTkScrollableFrame(self, corner_radius=10)
        controls_frame.grid(row=0, column=2, sticky="nsew", padx=(10, 0), pady=0)
        
        # ===== SECCIÓN: Agregar Vértice =====
        self.create_section(controls_frame, "➕ Agregar Vértice")
        
        self.vertex_entry = ctk.CTkEntry(controls_frame, placeholder_text="Nombre del vértice")
        self.vertex_entry.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            controls_frame,
            text="Agregar Vértice",
            command=self.add_vertex
        ).pack(fill="x", padx=10, pady=5)
        
        # ===== SECCIÓN: Agregar Arista =====
        self.create_section(controls_frame, "🔗 Agregar Arista")

        self.edge_name_entry = ctk.CTkEntry(controls_frame, placeholder_text="Nombre de la arista")
        self.edge_name_entry.pack(fill="x", padx=10, pady=5)

        # Lista desplegable para Vértice 1
        ctk.CTkLabel(controls_frame, text="Vértice 1:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.edge_v1_var = ctk.StringVar(value="")
        self.edge_v1_combo = ctk.CTkComboBox(
            controls_frame,
            variable=self.edge_v1_var,
            values=[]
        )
        self.edge_v1_combo.pack(fill="x", padx=10, pady=5)

        # Lista desplegable para Vértice 2
        ctk.CTkLabel(controls_frame, text="Vértice 2:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.edge_v2_var = ctk.StringVar(value="")
        self.edge_v2_combo = ctk.CTkComboBox(
            controls_frame,
            variable=self.edge_v2_var,
            values=[]
        )
        self.edge_v2_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls_frame,
            text="Agregar Arista",
            command=self.add_edge
        ).pack(fill="x", padx=10, pady=5)

        # ===== SECCIÓN: Eliminar Vértice =====
        self.create_section(controls_frame, "❌ Eliminar Vértice")

        ctk.CTkLabel(controls_frame, text="Vértice a eliminar:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.delete_vertex_var = ctk.StringVar(value="")
        self.delete_vertex_combo = ctk.CTkComboBox(
            controls_frame,
            variable=self.delete_vertex_var,
            values=[]
        )
        self.delete_vertex_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls_frame,
            text="Eliminar Vértice",
            command=self.delete_vertex,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(fill="x", padx=10, pady=5)

        # ===== SECCIÓN: Eliminar Arista =====
        self.create_section(controls_frame, "❌ Eliminar Arista")

        ctk.CTkLabel(controls_frame, text="Arista a eliminar:", anchor="w").pack(fill="x", padx=10, pady=(5, 0))
        self.delete_edge_var = ctk.StringVar(value="")
        self.delete_edge_combo = ctk.CTkComboBox(
            controls_frame,
            variable=self.delete_edge_var,
            values=[]
        )
        self.delete_edge_combo.pack(fill="x", padx=10, pady=5)

        ctk.CTkButton(
            controls_frame,
            text="Eliminar Arista",
            command=self.delete_edge,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        ).pack(fill="x", padx=10, pady=5)

        # ===== SECCIÓN: Operaciones Unarias =====
        self.create_section(controls_frame, "🔄 Operaciones Unarias (1 grafo)")
        
        ctk.CTkButton(
            controls_frame,
            text="Complemento (G')",
            command=self.do_complement,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(fill="x", padx=10, pady=2)
        
        ctk.CTkButton(
            controls_frame,
            text="Fusión de Vértices",
            command=self.do_vertex_fusion,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(fill="x", padx=10, pady=2)
        
        ctk.CTkButton(
            controls_frame,
            text="Contracción de Arista",
            command=self.do_edge_contraction,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(fill="x", padx=10, pady=2)

        ctk.CTkButton(
            controls_frame,
            text="Grafo Línea L(G)",
            command=self.do_line_graph,
            fg_color="#e67e22",
            hover_color="#d35400"
        ).pack(fill="x", padx=10, pady=2)

        # ===== SECCIÓN: Operaciones Binarias =====
        self.create_section(controls_frame, "⚡ Operaciones Binarias (2+ grafos)")
        
        self.selection_label = ctk.CTkLabel(
            controls_frame,
            text="Grafos seleccionados: 0",
            font=("Segoe UI", 11)
        )
        self.selection_label.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            controls_frame,
            text="Unión (G1 ∪ G2)",
            command=self.do_union,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=2)
        
        ctk.CTkButton(
            controls_frame,
            text="Intersección (G1 ∩ G2)",
            command=self.do_intersection,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=2)
        
        ctk.CTkButton(
            controls_frame,
            text="Suma Anillo (G1 ⊕ G2)",
            command=self.do_ring_sum,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=2)
        
        ctk.CTkButton(
            controls_frame,
            text="Suma (G1 + G2)",
            command=self.do_sum,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=2)
        
        ctk.CTkButton(
            controls_frame,
            text="Producto Cartesiano (G1 × G2)",
            command=self.do_cartesian_product,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=2)
        
        ctk.CTkButton(
            controls_frame,
            text="Producto Tensorial (G1 ⊗ G2)",
            command=self.do_tensor_product,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=2)
        
        ctk.CTkButton(
            controls_frame,
            text="Composición (G1 ∘ G2)",
            command=self.do_composition,
            fg_color="#3498db",
            hover_color="#2980b9"
        ).pack(fill="x", padx=10, pady=2)
    
    def create_section(self, parent, title):
        """Crea un título de sección"""
        label = ctk.CTkLabel(
            parent,
            text=title,
            font=("Segoe UI", 14, "bold"),
            anchor="w"
        )
        label.pack(fill="x", padx=10, pady=(15, 5))
    
    # ==================== GESTIÓN DE GRAFOS ====================
    
    def create_new_graph(self):
        """Crea un nuevo grafo"""
        graph = self.manager.create_graph()
        self.current_graph = graph

        # Limpiar los comboboxes (grafo nuevo está vacío)
        self.edge_v1_combo.configure(values=[])
        self.edge_v2_combo.configure(values=[])

        self.refresh_graphs_list()
        self.draw_graph(graph)
        self.show_status(f"✓ Grafo G{graph.number} creado", "success")
    
    def delete_selected_graph(self):
        """Elimina el grafo seleccionado"""
        if self.current_graph is None:
            self.show_status("⚠️ Selecciona un grafo primero", "warning")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Eliminar G{self.current_graph.number}?"):
            number = self.current_graph.number
            self.manager.delete_graph(number)
            self.current_graph = None
            self.refresh_graphs_list()
            self.draw_empty_graph()
            self.show_status(f"✓ Grafo G{number} eliminado", "success")
    
    def select_graph(self, graph: GraphData):
        """Selecciona un grafo para trabajar con él"""
        self.current_graph = graph

        # Actualizar los comboboxes con los vértices del grafo seleccionado
        vertices_list = sorted(list(graph.vertices))
        self.edge_v1_combo.configure(values=vertices_list)
        self.edge_v2_combo.configure(values=vertices_list)
        self.delete_vertex_combo.configure(values=vertices_list)

        # Actualizar combobox de aristas
        edges_list = sorted([e.name for e in graph.edges])
        self.delete_edge_combo.configure(values=edges_list)

        self.draw_graph(graph)
        self.show_status(f"✓ G{graph.number} seleccionado", "success")
    
    def toggle_graph_selection(self, graph: GraphData):
        """Alterna la selección de un grafo para operaciones binarias"""
        if graph in self.selected_graphs:
            self.selected_graphs.remove(graph)
        else:
            self.selected_graphs.append(graph)
        
        self.refresh_graphs_list()
        self.selection_label.configure(text=f"Grafos seleccionados: {len(self.selected_graphs)}")
    
    def refresh_graphs_list(self):
        """Actualiza la lista visual de grafos"""
        # Limpiar lista actual
        for widget in self.graphs_listbox.winfo_children():
            widget.destroy()
        
        # Agregar cada grafo
        for graph in self.manager.get_all_graphs():
            self.create_graph_item(self.graphs_listbox, graph)
    
    def create_graph_item(self, parent, graph: GraphData):
        """Crea un item de grafo en la lista"""
        # Frame del item
        item_frame = ctk.CTkFrame(parent, corner_radius=8)
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # Color según si es resultado
        if graph.is_result:
            item_frame.configure(fg_color="#e67e22")
        
        # Checkbox para selección múltiple
        is_selected = graph in self.selected_graphs
        checkbox = ctk.CTkCheckBox(
            item_frame,
            text="",
            command=lambda: self.toggle_graph_selection(graph),
            width=20
        )
        checkbox.pack(side="left", padx=5)
        if is_selected:
            checkbox.select()
        
        # Información del grafo
        info = ctk.CTkLabel(
            item_frame,
            text=f"{graph.get_display_name()}\n|S|={len(graph.vertices)} |A|={len(graph.edges)}",
            font=("Segoe UI", 11),
            anchor="w"
        )
        info.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        
        # Botón de selección
        btn = ctk.CTkButton(
            item_frame,
            text="Ver",
            width=50,
            command=lambda: self.select_graph(graph)
        )
        btn.pack(side="right", padx=5)
    
    def show_graph_info(self):
        """Muestra información detallada del grafo actual"""
        if self.current_graph is None:
            self.show_status("⚠️ Selecciona un grafo primero", "warning")
            return
        
        g = self.current_graph
        
        vertices_str = ", ".join(sorted(g.vertices)) if g.vertices else "∅"
        edges_str = "\n".join([
            f"{e.name}: {{{e.get_vertices_list()[0]}, {e.get_vertices_list()[1]}}}"
            for e in sorted(g.edges, key=lambda x: x.name)
        ]) if g.edges else "∅"

        display_name = g.get_display_name()
        info = f"""INFORMACIÓN DEL GRAFO {display_name}

Conjunto de Vértices S:
{vertices_str}

Conjunto de Aristas A:
{edges_str}

Cardinalidades:
|S| = {len(g.vertices)}
|A| = {len(g.edges)}

Tipo: {"Resultado de operación" if g.is_result else "Grafo base"}
{"Expresión: " + g.expression if g.expression else ""}
"""

        # Crear ventana de información
        info_window = ctk.CTkToplevel(self)
        info_window.title(f"Información de {display_name}")
        info_window.geometry("500x400")
        
        text = ctk.CTkTextbox(info_window, font=("Consolas", 11))
        text.pack(fill="both", expand=True, padx=10, pady=10)
        text.insert("1.0", info)
        text.configure(state="disabled")
    
    # ==================== OPERACIONES DE CONSTRUCCIÓN ====================
    
    def add_vertex(self):
        """Agrega un vértice al grafo actual"""
        if self.current_graph is None:
            self.show_status("⚠️ Crea o selecciona un grafo primero", "warning")
            return
        
        vertex = self.vertex_entry.get().strip()
        if not vertex:
            self.show_status("⚠️ Ingresa un nombre de vértice", "warning")
            return
        
        if vertex in self.current_graph.vertices:
            self.show_status(f"⚠️ El vértice '{vertex}' ya existe", "warning")
            return
        
        self.current_graph.add_vertex(vertex)
        self.vertex_entry.delete(0, 'end')

        # Actualizar las listas desplegables de vértices
        vertices_list = sorted(list(self.current_graph.vertices))
        self.edge_v1_combo.configure(values=vertices_list)
        self.edge_v2_combo.configure(values=vertices_list)
        self.delete_vertex_combo.configure(values=vertices_list)

        self.draw_graph(self.current_graph)
        self.refresh_graphs_list()
        self.show_status(f"✓ Vértice '{vertex}' agregado", "success")
    
    def add_edge(self):
        """Agrega una arista al grafo actual"""
        if self.current_graph is None:
            self.show_status("⚠️ Crea o selecciona un grafo primero", "warning")
            return

        edge_name = self.edge_name_entry.get().strip()
        v1 = self.edge_v1_var.get().strip()
        v2 = self.edge_v2_var.get().strip()

        if not edge_name or not v1 or not v2:
            self.show_status("⚠️ Completa todos los campos", "warning")
            return

        if not self.current_graph.add_edge(edge_name, v1, v2):
            self.show_status("❌ No se pudo agregar la arista. Verifica los vértices", "error")
            return

        self.edge_name_entry.delete(0, 'end')
        self.edge_v1_var.set("")
        self.edge_v2_var.set("")
        self.draw_graph(self.current_graph)
        self.refresh_graphs_list()
        self.show_status(f"✓ Arista '{edge_name}' agregada", "success")

    def delete_vertex(self):
        """Elimina un vértice del grafo actual"""
        if self.current_graph is None:
            self.show_status("⚠️ Crea o selecciona un grafo primero", "warning")
            return

        vertex = self.delete_vertex_var.get().strip()
        if not vertex:
            self.show_status("⚠️ Selecciona un vértice para eliminar", "warning")
            return

        self.current_graph.remove_vertex(vertex)
        self.delete_vertex_var.set("")

        # Actualizar comboboxes
        vertices_list = sorted(list(self.current_graph.vertices))
        self.edge_v1_combo.configure(values=vertices_list)
        self.edge_v2_combo.configure(values=vertices_list)
        self.delete_vertex_combo.configure(values=vertices_list)

        self.draw_graph(self.current_graph)
        self.refresh_graphs_list()
        self.show_status(f"✓ Vértice '{vertex}' eliminado", "success")

    def delete_edge(self):
        """Elimina una arista del grafo actual"""
        if self.current_graph is None:
            self.show_status("⚠️ Crea o selecciona un grafo primero", "warning")
            return

        edge_name = self.delete_edge_var.get().strip()
        if not edge_name:
            self.show_status("⚠️ Selecciona una arista para eliminar", "warning")
            return

        if self.current_graph.remove_edge(edge_name):
            self.delete_edge_var.set("")

            # Actualizar combobox
            edges_list = sorted([e.name for e in self.current_graph.edges])
            self.delete_edge_combo.configure(values=edges_list)

            self.draw_graph(self.current_graph)
            self.refresh_graphs_list()
            self.show_status(f"✓ Arista '{edge_name}' eliminada", "success")
        else:
            self.show_status(f"❌ No se pudo eliminar la arista", "error")

    # ==================== OPERACIONES UNARIAS ====================
    
    def do_complement(self):
        """Calcula el complemento del grafo actual"""
        if self.current_graph is None:
            self.show_status("⚠️ Selecciona un grafo primero", "warning")
            return
        
        result = self.manager.complement(self.current_graph)
        self.current_graph = result
        self.refresh_graphs_list()
        self.draw_graph(result)
        self.show_status(f"✓ Complemento calculado → {result.get_display_name()}", "success")
    
    def do_vertex_fusion(self):
        """Fusiona dos vértices del grafo actual"""
        if self.current_graph is None:
            self.show_status("⚠️ Selecciona un grafo primero", "warning")
            return
        
        if len(self.current_graph.vertices) < 2:
            self.show_status("⚠️ El grafo necesita al menos 2 vértices", "warning")
            return
        
        # Ventana de selección
        dialog = ctk.CTkToplevel(self)
        dialog.title("Fusión de Vértices")
        dialog.geometry("300x200")
        
        ctk.CTkLabel(dialog, text="Selecciona dos vértices para fusionar:").pack(pady=10)
        
        vertices = sorted(list(self.current_graph.vertices))
        
        v1_var = ctk.StringVar(value=vertices[0])
        v2_var = ctk.StringVar(value=vertices[1] if len(vertices) > 1 else vertices[0])
        
        ctk.CTkOptionMenu(dialog, variable=v1_var, values=vertices).pack(pady=5)
        ctk.CTkOptionMenu(dialog, variable=v2_var, values=vertices).pack(pady=5)
        
        def confirm():
            v1 = v1_var.get()
            v2 = v2_var.get()
            if v1 == v2:
                messagebox.showerror("Error", "Selecciona vértices diferentes")
                return
            
            result = self.manager.vertex_fusion(self.current_graph, v1, v2)
            self.current_graph = result
            self.refresh_graphs_list()
            self.draw_graph(result)
            self.show_status(f"✓ Vértices fusionados → {result.get_display_name()}", "success")
            dialog.destroy()
        
        ctk.CTkButton(dialog, text="Fusionar", command=confirm).pack(pady=10)
    
    def do_edge_contraction(self):
        """Contrae una arista del grafo actual"""
        if self.current_graph is None:
            self.show_status("⚠️ Selecciona un grafo primero", "warning")
            return

        if len(self.current_graph.edges) == 0:
            self.show_status("⚠️ El grafo no tiene aristas", "warning")
            return

        # Ventana de selección
        dialog = ctk.CTkToplevel(self)
        dialog.title("Contracción de Arista")
        dialog.geometry("300x150")

        ctk.CTkLabel(dialog, text="Selecciona una arista para contraer:").pack(pady=10)

        edges = [e.name for e in sorted(self.current_graph.edges, key=lambda x: x.name)]
        edge_var = ctk.StringVar(value=edges[0])

        ctk.CTkOptionMenu(dialog, variable=edge_var, values=edges).pack(pady=5)

        def confirm():
            edge_name = edge_var.get()
            result = self.manager.edge_contraction(self.current_graph, edge_name)
            if result is None:
                messagebox.showerror("Error", "No se pudo contraer la arista")
                return

            self.current_graph = result
            self.refresh_graphs_list()
            self.draw_graph(result)
            self.show_status(f"✓ Arista contraída → {result.get_display_name()}", "success")
            dialog.destroy()

        ctk.CTkButton(dialog, text="Contraer", command=confirm).pack(pady=10)

    def do_line_graph(self):
        """Calcula el grafo línea del grafo actual"""
        if self.current_graph is None:
            self.show_status("⚠️ Selecciona un grafo primero", "warning")
            return

        if len(self.current_graph.edges) == 0:
            self.show_status("⚠️ El grafo necesita al menos una arista", "warning")
            return

        result = self.manager.line_graph(self.current_graph)
        self.current_graph = result
        self.refresh_graphs_list()
        self.draw_graph(result)
        self.show_status(f"✓ Grafo línea calculado → {result.get_display_name()}", "success")
    
    # ==================== OPERACIONES BINARIAS ====================
    
    def do_union(self):
        """Unión de grafos"""
        if len(self.selected_graphs) < 2:
            self.show_status("⚠️ Selecciona al menos 2 grafos", "warning")
            return
        
        result = self.selected_graphs[0]
        for g in self.selected_graphs[1:]:
            result = self.manager.union(result, g)

        self.selected_graphs.clear()
        self.current_graph = result
        self.refresh_graphs_list()
        self.draw_graph(result)
        self.show_status(f"✓ Unión calculada → {result.get_display_name()}", "success")
    
    def do_intersection(self):
        """Intersección de grafos"""
        if len(self.selected_graphs) < 2:
            self.show_status("⚠️ Selecciona al menos 2 grafos", "warning")
            return
        
        result = self.selected_graphs[0]
        for g in self.selected_graphs[1:]:
            result = self.manager.intersection(result, g)

        self.selected_graphs.clear()
        self.current_graph = result
        self.refresh_graphs_list()
        self.draw_graph(result)
        self.show_status(f"✓ Intersección calculada → {result.get_display_name()}", "success")
    
    def do_ring_sum(self):
        """Suma anillo de grafos"""
        if len(self.selected_graphs) != 2:
            self.show_status("⚠️ Selecciona exactamente 2 grafos", "warning")
            return
        
        result = self.manager.ring_sum(self.selected_graphs[0], self.selected_graphs[1])
        self.selected_graphs.clear()
        self.current_graph = result
        self.refresh_graphs_list()
        self.draw_graph(result)
        self.show_status(f"✓ Suma anillo calculada → {result.get_display_name()}", "success")
    
    def do_sum(self):
        """Suma de grafos"""
        if len(self.selected_graphs) != 2:
            self.show_status("⚠️ Selecciona exactamente 2 grafos", "warning")
            return
        
        result = self.manager.graph_sum(self.selected_graphs[0], self.selected_graphs[1])
        self.selected_graphs.clear()
        self.current_graph = result
        self.refresh_graphs_list()
        self.draw_graph(result)
        self.show_status(f"✓ Suma calculada → {result.get_display_name()}", "success")
    
    def do_cartesian_product(self):
        """Producto cartesiano de grafos"""
        if len(self.selected_graphs) != 2:
            self.show_status("⚠️ Selecciona exactamente 2 grafos", "warning")
            return
        
        result = self.manager.cartesian_product(self.selected_graphs[0], self.selected_graphs[1])
        self.selected_graphs.clear()
        self.current_graph = result
        self.refresh_graphs_list()
        self.draw_graph(result)
        self.show_status(f"✓ Producto cartesiano calculado → {result.get_display_name()}", "success")
    
    def do_tensor_product(self):
        """Producto tensorial de grafos"""
        if len(self.selected_graphs) != 2:
            self.show_status("⚠️ Selecciona exactamente 2 grafos", "warning")
            return
        
        result = self.manager.tensor_product(self.selected_graphs[0], self.selected_graphs[1])
        self.selected_graphs.clear()
        self.current_graph = result
        self.refresh_graphs_list()
        self.draw_graph(result)
        self.show_status(f"✓ Producto tensorial calculado → {result.get_display_name()}", "success")
    
    def do_composition(self):
        """Composición de grafos"""
        if len(self.selected_graphs) != 2:
            self.show_status("⚠️ Selecciona exactamente 2 grafos", "warning")
            return
        
        result = self.manager.composition(self.selected_graphs[0], self.selected_graphs[1])
        self.selected_graphs.clear()
        self.current_graph = result
        self.refresh_graphs_list()
        self.draw_graph(result)
        self.show_status(f"✓ Composición calculada → {result.get_display_name()}", "success")
    
    # ==================== PERSISTENCIA ====================
    
    def save_all_graphs(self):
        """Guarda todos los grafos en un archivo"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.manager.save_to_file(filename):
                self.show_status("✓ Grafos guardados exitosamente", "success")
            else:
                self.show_status("❌ Error al guardar grafos", "error")
    
    def load_all_graphs(self):
        """Carga todos los grafos desde un archivo"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            if self.manager.load_from_file(filename):
                self.current_graph = None
                self.selected_graphs.clear()
                self.refresh_graphs_list()
                self.draw_empty_graph()
                self.show_status("✓ Grafos cargados exitosamente", "success")
            else:
                self.show_status("❌ Error al cargar grafos", "error")
    
    def clear_all_graphs(self):
        """Elimina todos los grafos"""
        if messagebox.askyesno("Confirmar", "¿Eliminar todos los grafos?"):
            self.manager.clear_all()
            self.current_graph = None
            self.selected_graphs.clear()
            self.refresh_graphs_list()
            self.draw_empty_graph()
            self.show_status("✓ Todos los grafos eliminados", "success")
    
    # ==================== VISUALIZACIÓN ====================
    
    def draw_graph(self, graph: GraphData):
        """Dibuja un grafo usando NetworkX y Matplotlib"""
        self.ax.clear()

        if len(graph.vertices) == 0:
            self.draw_empty_graph()
            return

        # Crear grafo de NetworkX
        G = nx.Graph()

        # Agregar vértices
        for v in graph.vertices:
            G.add_node(v)

        # Agregar aristas con etiquetas
        edge_labels = {}
        for edge in graph.edges:
            vertices = edge.get_vertices_list()
            if len(vertices) >= 2:
                G.add_edge(vertices[0], vertices[1])
                edge_labels[(vertices[0], vertices[1])] = edge.name

        # Usar posiciones guardadas o generar nuevas
        # Validar que todas las posiciones existan para todos los vértices
        if graph.number in self.graph_positions:
            saved_pos = self.graph_positions[graph.number]
            # Si el número de vértices cambió, regenerar posiciones preservando las existentes
            if len(saved_pos) == len(G.nodes()):
                pos = saved_pos
            else:
                # Generar nuevas posiciones pero mantener los vértices existentes si es posible
                pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
                # Intentar preservar posiciones de vértices existentes
                for node in saved_pos:
                    if node in pos:
                        pos[node] = saved_pos[node]
                self.graph_positions[graph.number] = pos
        else:
            pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
            self.graph_positions[graph.number] = pos

        # Dibujar
        nx.draw_networkx_nodes(
            G, pos, ax=self.ax,
            node_color='#3498db' if not graph.is_result else '#e67e22',
            node_size=800,
            alpha=0.9
        )

        # Dibujar aristas con curvas para evitar sobreposición
        nx.draw_networkx_edges(
            G, pos, ax=self.ax,
            edge_color='#95a5a6',
            width=2,
            alpha=0.6,
            connectionstyle="arc3,rad=0.1"
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
            font_color='black'
        )

        self.ax.set_title(
            f"{graph.get_display_name()} - |S|={len(graph.vertices)}, |A|={len(graph.edges)}",
            color='white',
            fontsize=14,
            fontweight='bold'
        )

        # Configurar límites de los ejes para que todos los nodos sean visibles
        if pos:
            x_coords = [p[0] for p in pos.values()]
            y_coords = [p[1] for p in pos.values()]
            margin = 0.2
            x_margin = (max(x_coords) - min(x_coords)) * margin if x_coords else 0.5
            y_margin = (max(y_coords) - min(y_coords)) * margin if y_coords else 0.5

            self.ax.set_xlim(min(x_coords) - x_margin if x_coords else -1, max(x_coords) + x_margin if x_coords else 1)
            self.ax.set_ylim(min(y_coords) - y_margin if y_coords else -1, max(y_coords) + y_margin if y_coords else 1)

        self.ax.axis('off')

        self.canvas.draw()
    
    def draw_empty_graph(self):
        """Dibuja un grafo vacío"""
        self.ax.clear()
        self.ax.text(
            0.5, 0.5,
            'Selecciona o crea un grafo\npara visualizarlo',
            ha='center', va='center',
            fontsize=14,
            color='#95a5a6',
            transform=self.ax.transAxes
        )
        self.ax.axis('off')
        self.canvas.draw()
    
    def show_status(self, message: str, status_type: str = "info"):
        """Muestra un mensaje de estado"""
        self.viz_title.configure(text=f"📊 {message}")
        
        # Restaurar título después de 3 segundos
        self.after(3000, lambda: self.viz_title.configure(text="📊 Visualización del Grafo"))


# ==================== EJECUCIÓN STANDALONE ====================

if __name__ == "__main__":
    # Crear ventana standalone para pruebas
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("Operaciones con Grafos - Prueba Standalone")
    root.geometry("1400x800")
    
    content = GraphOperationsContent(root)
    content.pack(fill="both", expand=True, padx=10, pady=10)
    
    root.mainloop()
