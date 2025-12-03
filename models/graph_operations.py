"""
Módulo de Operaciones con Grafos
Implementa operaciones algebraicas formales de teoría de grafos

Operaciones Unarias:
- Complemento
- Fusión de vértices
- Contracción de arista

Operaciones Binarias:
- Unión
- Intersección
- Suma anillo (diferencia simétrica)
- Suma
- Producto cartesiano
- Producto tensorial
- Composición
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
import json


@dataclass
class Edge:
    """Representa una arista con nombre y vértices"""
    name: str
    vertices: frozenset  # Usamos frozenset para que sea hashable
    
    def __init__(self, name: str, v1: str, v2: str):
        self.name = name
        self.vertices = frozenset([v1, v2])
    
    def __hash__(self):
        return hash((self.name, self.vertices))
    
    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.name == other.name and self.vertices == other.vertices
    
    def get_vertices_list(self) -> List[str]:
        """Retorna los vértices como lista ordenada"""
        return sorted(list(self.vertices))
    
    def contains_vertex(self, vertex: str) -> bool:
        """Verifica si la arista contiene el vértice dado"""
        return vertex in self.vertices
    
    def to_dict(self) -> dict:
        """Convierte la arista a diccionario"""
        return {
            "name": self.name,
            "vertices": self.get_vertices_list()
        }


@dataclass
class GraphData:
    """
    Representa un grafo con nomenclatura académica
    G_n = (S_n, A_n) donde:
    - S_n es el conjunto de vértices
    - A_n es el conjunto de aristas
    """
    number: int  # Número del grafo (G1, G2, G3, ...)
    vertices: Set[str] = field(default_factory=set)
    edges: Set[Edge] = field(default_factory=set)
    is_result: bool = False  # Marca si es resultado de una operación
    
    def add_vertex(self, vertex: str) -> None:
        """Agrega un vértice al grafo"""
        self.vertices.add(vertex)
    
    def remove_vertex(self, vertex: str) -> None:
        """
        Elimina un vértice y todas las aristas que lo contienen
        """
        self.vertices.discard(vertex)
        # Eliminar aristas que contienen este vértice
        self.edges = {e for e in self.edges if not e.contains_vertex(vertex)}
    
    def add_edge(self, edge_name: str, v1: str, v2: str) -> bool:
        """
        Agrega una arista entre dos vértices
        Retorna True si se agregó exitosamente
        """
        if v1 not in self.vertices or v2 not in self.vertices:
            return False
        
        edge = Edge(edge_name, v1, v2)
        self.edges.add(edge)
        return True
    
    def remove_edge(self, edge_name: str) -> bool:
        """Elimina una arista por nombre"""
        for edge in self.edges:
            if edge.name == edge_name:
                self.edges.remove(edge)
                return True
        return False
    
    def get_edge_by_name(self, edge_name: str) -> Optional[Edge]:
        """Busca una arista por nombre"""
        for edge in self.edges:
            if edge.name == edge_name:
                return edge
        return None
    
    def get_edges_with_vertex(self, vertex: str) -> Set[Edge]:
        """Retorna todas las aristas que contienen el vértice dado"""
        return {e for e in self.edges if e.contains_vertex(vertex)}
    
    def to_dict(self) -> dict:
        """Convierte el grafo a diccionario"""
        return {
            "number": self.number,
            "vertices": sorted(list(self.vertices)),
            "edges": [e.to_dict() for e in self.edges],
            "is_result": self.is_result
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> GraphData:
        """Crea un grafo desde un diccionario"""
        graph = cls(
            number=data["number"],
            vertices=set(data["vertices"]),
            is_result=data.get("is_result", False)
        )
        
        for edge_data in data["edges"]:
            v_list = edge_data["vertices"]
            if len(v_list) >= 2:
                edge = Edge(edge_data["name"], v_list[0], v_list[1])
                graph.edges.add(edge)
        
        return graph
    
    def __str__(self) -> str:
        return f"G{self.number}: |S|={len(self.vertices)}, |A|={len(self.edges)}"


class GraphOperationsManager:
    """
    Gestor de múltiples grafos y operaciones entre ellos
    """
    
    def __init__(self):
        self.graphs: Dict[int, GraphData] = {}
        self.next_number = 1
    
    def create_graph(self) -> GraphData:
        """Crea un nuevo grafo con numeración automática"""
        graph = GraphData(number=self.next_number)
        self.graphs[self.next_number] = graph
        self.next_number += 1
        return graph
    
    def delete_graph(self, number: int) -> bool:
        """Elimina un grafo por su número"""
        if number in self.graphs:
            del self.graphs[number]
            return True
        return False
    
    def get_graph(self, number: int) -> Optional[GraphData]:
        """Obtiene un grafo por su número"""
        return self.graphs.get(number)
    
    def get_all_graphs(self) -> List[GraphData]:
        """Retorna todos los grafos ordenados por número"""
        return [self.graphs[n] for n in sorted(self.graphs.keys())]
    
    def clear_all(self) -> None:
        """Elimina todos los grafos"""
        self.graphs.clear()
        self.next_number = 1
    
    # ==================== OPERACIONES UNARIAS ====================
    
    def complement(self, g: GraphData) -> GraphData:
        """
        Calcula el complemento de un grafo
        G' tiene las mismas vértices pero las aristas complementarias
        """
        result = GraphData(number=self.next_number, is_result=True)
        result.vertices = g.vertices.copy()
        
        # Obtener todas las aristas posibles
        vertices_list = sorted(list(g.vertices))
        edge_counter = 1
        
        for i, v1 in enumerate(vertices_list):
            for v2 in vertices_list[i+1:]:
                # Verificar si esta arista existe en el grafo original
                exists = False
                for edge in g.edges:
                    if edge.vertices == frozenset([v1, v2]):
                        exists = True
                        break
                
                # Si no existe, agregarla al complemento
                if not exists:
                    edge = Edge(f"e{edge_counter}", v1, v2)
                    result.edges.add(edge)
                    edge_counter += 1
        
        self.graphs[self.next_number] = result
        self.next_number += 1
        return result
    
    def vertex_fusion(self, g: GraphData, v1: str, v2: str) -> GraphData:
        """
        Fusiona dos vértices en uno solo
        El nuevo vértice se llama v1v2 (concatenación)
        Las aristas entre v1 y v2 se eliminan (loops)
        Las demás aristas se actualizan al nuevo vértice
        """
        result = GraphData(number=self.next_number, is_result=True)
        
        # Nuevo nombre del vértice fusionado
        new_vertex = f"{v1}{v2}"
        
        # Copiar vértices excepto v1 y v2, agregar el fusionado
        result.vertices = (g.vertices - {v1, v2}) | {new_vertex}
        
        # Procesar aristas
        for edge in g.edges:
            vertices = edge.get_vertices_list()
            
            # Si la arista es entre v1 y v2, se elimina (loop)
            if set(vertices) == {v1, v2}:
                continue
            
            # Reemplazar v1 o v2 por el nuevo vértice
            new_vertices = []
            for v in vertices:
                if v == v1 or v == v2:
                    new_vertices.append(new_vertex)
                else:
                    new_vertices.append(v)
            
            # Crear nueva arista
            if len(new_vertices) >= 2:
                new_edge = Edge(edge.name, new_vertices[0], new_vertices[1])
                result.edges.add(new_edge)
        
        self.graphs[self.next_number] = result
        self.next_number += 1
        return result
    
    def edge_contraction(self, g: GraphData, edge_name: str) -> GraphData:
        """
        Contracción de una arista: elimina la arista y fusiona sus vértices
        Es equivalente a fusión de vértices después de identificar la arista
        """
        edge = g.get_edge_by_name(edge_name)
        if edge is None:
            return None

        vertices = edge.get_vertices_list()
        if len(vertices) < 2:
            return None

        # Primero remover la arista, luego fusionar vértices
        temp_graph = GraphData(number=g.number)
        temp_graph.vertices = g.vertices.copy()
        temp_graph.edges = g.edges.copy()
        temp_graph.remove_edge(edge_name)

        return self.vertex_fusion(temp_graph, vertices[0], vertices[1])

    def line_graph(self, g: GraphData) -> GraphData:
        """
        Grafo línea L(G): Operación unaria que genera un nuevo grafo donde:
        - Cada arista de G se convierte en un vértice de L(G)
        - Dos vértices en L(G) están conectados si sus aristas correspondientes
          comparten un vértice en G

        Ejemplo: Si G tiene aristas a,b,c donde a=(u,v) y b=(v,w),
        entonces L(G) tiene vértices a,b,c donde existe arista entre a-b
        """
        result = GraphData(number=self.next_number, is_result=True)

        # Convertir cada arista de G en un vértice de L(G)
        edges_list = list(g.edges)
        for i, edge in enumerate(edges_list):
            result.vertices.add(edge.name)

        # Crear aristas en L(G) entre vértices que comparten una arista en G
        edge_counter = 1
        for i, edge1 in enumerate(edges_list):
            for edge2 in edges_list[i+1:]:
                # Verificar si las aristas comparten un vértice
                if edge1.vertices & edge2.vertices:  # Intersección no vacía
                    new_edge = Edge(f"l{edge_counter}", edge1.name, edge2.name)
                    result.edges.add(new_edge)
                    edge_counter += 1

        self.graphs[self.next_number] = result
        self.next_number += 1
        return result
    
    # ==================== OPERACIONES BINARIAS ====================
    
    def union(self, g1: GraphData, g2: GraphData) -> GraphData:
        """
        Unión de dos grafos: G1 ∪ G2
        S3 = S1 ∪ S2
        A3 = A1 ∪ A2
        """
        result = GraphData(number=self.next_number, is_result=True)
        result.vertices = g1.vertices | g2.vertices
        result.edges = g1.edges | g2.edges
        
        self.graphs[self.next_number] = result
        self.next_number += 1
        return result
    
    def intersection(self, g1: GraphData, g2: GraphData) -> GraphData:
        """
        Intersección de dos grafos: G1 ∩ G2
        S3 = S1 ∩ S2
        A3 = A1 ∩ A2 (solo aristas cuyos vértices están en S3)
        """
        result = GraphData(number=self.next_number, is_result=True)
        result.vertices = g1.vertices & g2.vertices
        
        # Solo aristas que están en ambos y cuyos vértices están en la intersección
        for edge in g1.edges & g2.edges:
            if edge.vertices.issubset(result.vertices):
                result.edges.add(edge)
        
        self.graphs[self.next_number] = result
        self.next_number += 1
        return result
    
    def ring_sum(self, g1: GraphData, g2: GraphData) -> GraphData:
        """
        Suma anillo (diferencia simétrica): G1 ⊕ G2
        S3 = S1 ∪ S2
        A3 = (A1 ∪ A2) - (A1 ∩ A2)
        """
        result = GraphData(number=self.next_number, is_result=True)
        result.vertices = g1.vertices | g2.vertices
        result.edges = (g1.edges | g2.edges) - (g1.edges & g2.edges)
        
        self.graphs[self.next_number] = result
        self.next_number += 1
        return result
    
    def graph_sum(self, g1: GraphData, g2: GraphData) -> GraphData:
        """
        Suma de grafos: G1 + G2
        Une ambos grafos y agrega aristas entre todos los vértices de G1 y G2
        """
        result = GraphData(number=self.next_number, is_result=True)
        result.vertices = g1.vertices | g2.vertices
        result.edges = g1.edges | g2.edges
        
        # Agregar aristas entre todos los vértices de G1 y G2
        edge_counter = len(result.edges) + 1
        for v1 in g1.vertices:
            for v2 in g2.vertices:
                edge = Edge(f"s{edge_counter}", v1, v2)
                result.edges.add(edge)
                edge_counter += 1
        
        self.graphs[self.next_number] = result
        self.next_number += 1
        return result
    
    def cartesian_product(self, g1: GraphData, g2: GraphData) -> GraphData:
        """
        Producto cartesiano: G1 × G2
        Vértices: (u, v) para todo u en S1, v en S2
        Aristas: ((u1,v), (u2,v)) si (u1,u2) en A1
                 ((u,v1), (u,v2)) si (v1,v2) en A2
        """
        result = GraphData(number=self.next_number, is_result=True)
        
        # Crear vértices (u,v)
        for u in g1.vertices:
            for v in g2.vertices:
                result.vertices.add(f"({u},{v})")
        
        edge_counter = 1
        
        # Aristas tipo 1: ((u1,v), (u2,v)) si (u1,u2) en A1
        for edge in g1.edges:
            vertices = edge.get_vertices_list()
            if len(vertices) >= 2:
                u1, u2 = vertices[0], vertices[1]
                for v in g2.vertices:
                    new_edge = Edge(f"c{edge_counter}", f"({u1},{v})", f"({u2},{v})")
                    result.edges.add(new_edge)
                    edge_counter += 1
        
        # Aristas tipo 2: ((u,v1), (u,v2)) si (v1,v2) en A2
        for edge in g2.edges:
            vertices = edge.get_vertices_list()
            if len(vertices) >= 2:
                v1, v2 = vertices[0], vertices[1]
                for u in g1.vertices:
                    new_edge = Edge(f"c{edge_counter}", f"({u},{v1})", f"({u},{v2})")
                    result.edges.add(new_edge)
                    edge_counter += 1
        
        self.graphs[self.next_number] = result
        self.next_number += 1
        return result
    
    def tensor_product(self, g1: GraphData, g2: GraphData) -> GraphData:
        """
        Producto tensorial: G1 ⊗ G2
        Vértices: (u, v) para todo u en S1, v en S2
        Aristas: ((u1,v1), (u2,v2)) si (u1,u2) en A1 Y (v1,v2) en A2
        """
        result = GraphData(number=self.next_number, is_result=True)
        
        # Crear vértices (u,v)
        for u in g1.vertices:
            for v in g2.vertices:
                result.vertices.add(f"({u},{v})")
        
        edge_counter = 1
        
        # Crear aristas solo si existen en ambos grafos
        for edge1 in g1.edges:
            v1_list = edge1.get_vertices_list()
            if len(v1_list) < 2:
                continue
            u1, u2 = v1_list[0], v1_list[1]
            
            for edge2 in g2.edges:
                v2_list = edge2.get_vertices_list()
                if len(v2_list) < 2:
                    continue
                v1, v2 = v2_list[0], v2_list[1]
                
                new_edge = Edge(f"t{edge_counter}", f"({u1},{v1})", f"({u2},{v2})")
                result.edges.add(new_edge)
                edge_counter += 1
        
        self.graphs[self.next_number] = result
        self.next_number += 1
        return result
    
    def composition(self, g1: GraphData, g2: GraphData) -> GraphData:
        """
        Composición de grafos: G1 ∘ G2
        Vértices: (u, v) para todo u en S1, v en S2
        Aristas: 
        - ((u1,v1), (u2,v2)) si (u1,u2) en A1
        - ((u,v1), (u,v2)) si (v1,v2) en A2
        """
        result = GraphData(number=self.next_number, is_result=True)
        
        # Crear vértices (u,v)
        for u in g1.vertices:
            for v in g2.vertices:
                result.vertices.add(f"({u},{v})")
        
        edge_counter = 1
        
        # Tipo 1: Si existe arista en G1
        for edge1 in g1.edges:
            vertices = edge1.get_vertices_list()
            if len(vertices) >= 2:
                u1, u2 = vertices[0], vertices[1]
                for v1 in g2.vertices:
                    for v2 in g2.vertices:
                        new_edge = Edge(f"o{edge_counter}", f"({u1},{v1})", f"({u2},{v2})")
                        result.edges.add(new_edge)
                        edge_counter += 1
        
        # Tipo 2: Si existe arista en G2 (mismo vértice en G1)
        for u in g1.vertices:
            for edge2 in g2.edges:
                vertices = edge2.get_vertices_list()
                if len(vertices) >= 2:
                    v1, v2 = vertices[0], vertices[1]
                    new_edge = Edge(f"o{edge_counter}", f"({u},{v1})", f"({u},{v2})")
                    result.edges.add(new_edge)
                    edge_counter += 1
        
        self.graphs[self.next_number] = result
        self.next_number += 1
        return result
    
    # ==================== PERSISTENCIA ====================
    
    def to_json(self) -> str:
        """Exporta todos los grafos a JSON"""
        data = {
            "next_number": self.next_number,
            "graphs": [g.to_dict() for g in self.get_all_graphs()]
        }
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def from_json(self, json_str: str) -> bool:
        """Importa grafos desde JSON"""
        try:
            data = json.loads(json_str)
            self.clear_all()
            self.next_number = data.get("next_number", 1)
            
            for graph_data in data.get("graphs", []):
                graph = GraphData.from_dict(graph_data)
                self.graphs[graph.number] = graph
            
            return True
        except Exception as e:
            print(f"Error al cargar JSON: {e}")
            return False
    
    def save_to_file(self, filename: str) -> bool:
        """Guarda los grafos en un archivo JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.to_json())
            return True
        except Exception as e:
            print(f"Error al guardar archivo: {e}")
            return False
    
    def load_from_file(self, filename: str) -> bool:
        """Carga los grafos desde un archivo JSON"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return self.from_json(f.read())
        except Exception as e:
            print(f"Error al cargar archivo: {e}")
            return False
