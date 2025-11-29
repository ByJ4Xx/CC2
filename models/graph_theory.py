"""
Módulo de Teoría de Grafos
Implementa conceptos fundamentales de teoría de grafos:
- Circuitos y circuitos fundamentales
- Conjuntos de corte y conjuntos de corte fundamentales
- Matrices de incidencia y adyacencia (vértices y aristas)
- Análisis de caminos y ciclos
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
import json
import networkx as nx
import numpy as np


@dataclass
class GraphTheory:
    """
    Clase para análisis de teoría de grafos
    Soporta grafos no dirigidos con vértices y aristas nombradas
    """
    vertices: Set[str] = field(default_factory=set)
    edges: Dict[str, Tuple[str, str]] = field(default_factory=dict)  # nombre -> (v1, v2)

    def __post_init__(self):
        """Valida que las aristas tengan vértices válidos"""
        for edge_name, (v1, v2) in list(self.edges.items()):
            if v1 not in self.vertices or v2 not in self.vertices:
                # Agregar vértices automáticamente si no existen
                self.vertices.add(v1)
                self.vertices.add(v2)

    def add_vertex(self, vertex: str) -> None:
        """Agrega un vértice al grafo"""
        self.vertices.add(vertex)

    def add_edge(self, edge_name: str, v1: str, v2: str) -> bool:
        """Agrega una arista entre dos vértices"""
        if v1 not in self.vertices or v2 not in self.vertices:
            return False
        self.edges[edge_name] = (v1, v2)
        return True

    def remove_edge(self, edge_name: str) -> bool:
        """Elimina una arista por nombre"""
        if edge_name in self.edges:
            del self.edges[edge_name]
            return True
        return False

    def _to_networkx(self) -> nx.Graph:
        """Convierte el grafo a formato NetworkX"""
        G = nx.Graph()
        G.add_nodes_from(self.vertices)
        for edge_name, (v1, v2) in self.edges.items():
            G.add_edge(v1, v2, name=edge_name)
        return G

    # ==================== MATRICES ====================

    def vertex_adjacency_matrix(self) -> Tuple[np.ndarray, List[str]]:
        """
        Matriz de adyacencia de vértices
        M[i][j] = número de aristas entre vértice i y vértice j
        """
        vertices_list = sorted(list(self.vertices))
        n = len(vertices_list)
        matrix = np.zeros((n, n), dtype=int)

        vertex_to_idx = {v: i for i, v in enumerate(vertices_list)}

        for v1, v2 in self.edges.values():
            i = vertex_to_idx[v1]
            j = vertex_to_idx[v2]
            matrix[i][j] += 1
            matrix[j][i] += 1

        return matrix, vertices_list

    def edge_adjacency_matrix(self) -> Tuple[np.ndarray, List[str]]:
        """
        Matriz de adyacencia de aristas
        M[i][j] = 1 si las aristas i y j comparten un vértice, 0 en caso contrario
        """
        edges_list = sorted(list(self.edges.keys()))
        n = len(edges_list)
        matrix = np.zeros((n, n), dtype=int)

        for i, edge1 in enumerate(edges_list):
            v1_set = set(self.edges[edge1])
            for j, edge2 in enumerate(edges_list):
                if i != j:
                    v2_set = set(self.edges[edge2])
                    if v1_set & v2_set:  # Intersección no vacía
                        matrix[i][j] = 1

        return matrix, edges_list

    def vertex_incidence_matrix(self) -> Tuple[np.ndarray, List[str], List[str]]:
        """
        Matriz de incidencia vértice-arista
        M[i][j] = 1 si el vértice i es incidente a la arista j, 0 en caso contrario
        """
        vertices_list = sorted(list(self.vertices))
        edges_list = sorted(list(self.edges.keys()))

        n_vertices = len(vertices_list)
        n_edges = len(edges_list)
        matrix = np.zeros((n_vertices, n_edges), dtype=int)

        vertex_to_idx = {v: i for i, v in enumerate(vertices_list)}

        for j, edge_name in enumerate(edges_list):
            v1, v2 = self.edges[edge_name]
            i1 = vertex_to_idx[v1]
            i2 = vertex_to_idx[v2]
            matrix[i1][j] = 1
            matrix[i2][j] = 1

        return matrix, vertices_list, edges_list

    def edge_incidence_matrix(self) -> Tuple[np.ndarray, List[str], List[str]]:
        """
        Matriz de incidencia arista-vértice (transpuesta de vertex_incidence)
        M[i][j] = 1 si la arista i es incidente al vértice j, 0 en caso contrario
        """
        vertex_matrix, vertices_list, edges_list = self.vertex_incidence_matrix()
        return vertex_matrix.T, edges_list, vertices_list

    # ==================== CIRCUITOS ====================

    def find_all_cycles(self) -> List[List[str]]:
        """
        Encuentra todos los ciclos simples en el grafo
        Retorna lista de ciclos como listas de vértices
        """
        G = self._to_networkx()
        try:
            cycles = list(nx.simple_cycles(G.to_directed()))
            # Convertir a ciclos no dirigidos únicos
            unique_cycles = []
            seen = set()
            for cycle in cycles:
                # Normalizar el ciclo (empezar desde el menor vértice)
                min_idx = cycle.index(min(cycle))
                normalized = tuple(cycle[min_idx:] + cycle[:min_idx])
                reversed_normalized = tuple(reversed(normalized))

                if normalized not in seen and reversed_normalized not in seen:
                    seen.add(normalized)
                    unique_cycles.append(list(normalized))

            return unique_cycles
        except:
            # Para grafos no dirigidos, usar cycle_basis
            cycles = nx.cycle_basis(G)
            return cycles

    def find_circuits(self) -> List[Dict]:
        """
        Encuentra todos los circuitos (ciclos) en el grafo
        Retorna información detallada de cada circuito
        """
        cycles = self.find_all_cycles()
        circuits = []

        for i, cycle in enumerate(cycles):
            # Encontrar las aristas del circuito
            circuit_edges = []
            for j in range(len(cycle)):
                v1 = cycle[j]
                v2 = cycle[(j + 1) % len(cycle)]

                # Buscar la arista entre v1 y v2
                for edge_name, (e_v1, e_v2) in self.edges.items():
                    if (e_v1 == v1 and e_v2 == v2) or (e_v1 == v2 and e_v2 == v1):
                        circuit_edges.append(edge_name)
                        break

            circuits.append({
                "id": i + 1,
                "vertices": cycle,
                "edges": circuit_edges,
                "length": len(cycle)
            })

        return circuits

    def fundamental_cycles(self, spanning_tree_edges: Optional[Set[str]] = None) -> List[Dict]:
        """
        Encuentra los ciclos fundamentales respecto a un árbol generador
        Si no se proporciona árbol, se calcula uno usando DFS
        """
        G = self._to_networkx()

        # Si no se proporciona árbol generador, calcular uno
        if spanning_tree_edges is None:
            if not nx.is_connected(G):
                return []
            tree = nx.minimum_spanning_tree(G)
            spanning_tree_edges = set()
            for u, v, data in tree.edges(data=True):
                edge_name = data.get('name', f"{u}-{v}")
                spanning_tree_edges.add(edge_name)

        # Aristas no incluidas en el árbol (cuerdas)
        chord_edges = set(self.edges.keys()) - spanning_tree_edges

        fundamental = []

        # Para cada cuerda, encontrar el ciclo fundamental
        for chord_name in chord_edges:
            v1, v2 = self.edges[chord_name]

            # Crear subgrafo solo con aristas del árbol
            tree_graph = nx.Graph()
            tree_graph.add_nodes_from(G.nodes())
            for edge_name in spanning_tree_edges:
                e_v1, e_v2 = self.edges[edge_name]
                tree_graph.add_edge(e_v1, e_v2, name=edge_name)

            try:
                # Encontrar camino en el árbol entre v1 y v2
                path = nx.shortest_path(tree_graph, v1, v2)

                # Construir lista de aristas del camino
                path_edges = []
                for i in range(len(path) - 1):
                    for edge_name in spanning_tree_edges:
                        e_v1, e_v2 = self.edges[edge_name]
                        if (e_v1 == path[i] and e_v2 == path[i+1]) or \
                           (e_v1 == path[i+1] and e_v2 == path[i]):
                            path_edges.append(edge_name)
                            break

                # El ciclo fundamental es el camino + la cuerda
                fundamental.append({
                    "chord": chord_name,
                    "vertices": path,
                    "tree_edges": path_edges,
                    "all_edges": path_edges + [chord_name],
                    "length": len(path)
                })
            except nx.NetworkXNoPath:
                continue

        return fundamental

    # ==================== CONJUNTOS DE CORTE ====================

    def find_cut_sets(self) -> List[Dict]:
        """
        Encuentra conjuntos de corte (edge cuts) mínimos
        Un conjunto de corte es un conjunto de aristas cuya eliminación desconecta el grafo
        """
        G = self._to_networkx()

        if not nx.is_connected(G):
            return []

        cut_sets = []

        # Encontrar todos los cortes mínimos entre pares de vértices
        vertices_list = list(G.nodes())
        seen_cuts = set()

        for i, source in enumerate(vertices_list):
            for target in vertices_list[i+1:]:
                # Encontrar corte mínimo entre source y target
                cut_value, partition = nx.minimum_cut(G, source, target)

                reachable, non_reachable = partition

                # Encontrar las aristas del corte
                cut_edges = []
                for edge_name, (v1, v2) in self.edges.items():
                    if (v1 in reachable and v2 in non_reachable) or \
                       (v1 in non_reachable and v2 in reachable):
                        cut_edges.append(edge_name)

                # Normalizar el conjunto de aristas para evitar duplicados
                normalized_cut = tuple(sorted(cut_edges))

                if normalized_cut not in seen_cuts and len(cut_edges) > 0:
                    seen_cuts.add(normalized_cut)
                    cut_sets.append({
                        "edges": cut_edges,
                        "size": len(cut_edges),
                        "partitions": [sorted(list(reachable)), sorted(list(non_reachable))]
                    })

        # Ordenar por tamaño
        cut_sets.sort(key=lambda x: x["size"])

        return cut_sets

    def fundamental_cut_sets(self, spanning_tree_edges: Optional[Set[str]] = None) -> List[Dict]:
        """
        Encuentra los conjuntos de corte fundamentales respecto a un árbol generador
        Para cada arista del árbol, su conjunto de corte fundamental es el conjunto
        de aristas cuya eliminación desconecta el grafo en dos componentes
        """
        G = self._to_networkx()

        if not nx.is_connected(G):
            return []

        # Si no se proporciona árbol generador, calcular uno
        if spanning_tree_edges is None:
            tree = nx.minimum_spanning_tree(G)
            spanning_tree_edges = set()
            for u, v, data in tree.edges(data=True):
                edge_name = data.get('name', f"{u}-{v}")
                spanning_tree_edges.add(edge_name)

        fundamental_cuts = []

        # Para cada arista del árbol
        for tree_edge_name in spanning_tree_edges:
            v1, v2 = self.edges[tree_edge_name]

            # Remover la arista del árbol para obtener dos componentes
            temp_tree = nx.Graph()
            temp_tree.add_nodes_from(G.nodes())

            for edge_name in spanning_tree_edges:
                if edge_name != tree_edge_name:
                    e_v1, e_v2 = self.edges[edge_name]
                    temp_tree.add_edge(e_v1, e_v2)

            # Encontrar las dos componentes
            components = list(nx.connected_components(temp_tree))

            if len(components) == 2:
                comp1, comp2 = components

                # Encontrar todas las aristas que cruzan entre las componentes
                cut_edges = [tree_edge_name]  # Incluir la arista del árbol

                for edge_name, (e_v1, e_v2) in self.edges.items():
                    if edge_name != tree_edge_name:
                        if (e_v1 in comp1 and e_v2 in comp2) or \
                           (e_v1 in comp2 and e_v2 in comp1):
                            cut_edges.append(edge_name)

                fundamental_cuts.append({
                    "tree_edge": tree_edge_name,
                    "cut_edges": cut_edges,
                    "size": len(cut_edges),
                    "partitions": [sorted(list(comp1)), sorted(list(comp2))]
                })

        return fundamental_cuts

    # ==================== CAMINOS Y CONECTIVIDAD ====================

    def is_connected(self) -> bool:
        """Verifica si el grafo es conexo"""
        G = self._to_networkx()
        return nx.is_connected(G)

    def shortest_path(self, v1: str, v2: str) -> Optional[List[str]]:
        """Encuentra el camino más corto entre dos vértices"""
        G = self._to_networkx()
        try:
            return nx.shortest_path(G, v1, v2)
        except nx.NetworkXNoPath:
            return None

    def graph_diameter(self) -> Optional[int]:
        """Calcula el diámetro del grafo (mayor distancia entre dos vértices)"""
        G = self._to_networkx()
        if not nx.is_connected(G):
            return None
        return nx.diameter(G)

    # ==================== PERSISTENCIA ====================

    def to_dict(self) -> dict:
        """Convierte el grafo a diccionario"""
        return {
            "vertices": sorted(list(self.vertices)),
            "edges": {name: [v1, v2] for name, (v1, v2) in self.edges.items()}
        }

    def to_json(self) -> str:
        """Exporta el grafo a JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> GraphTheory:
        """Crea un grafo desde un diccionario"""
        graph = cls(vertices=set(data["vertices"]))
        for name, (v1, v2) in data["edges"].items():
            graph.add_edge(name, v1, v2)
        return graph

    @classmethod
    def from_json(cls, json_str: str) -> GraphTheory:
        """Importa un grafo desde JSON"""
        data = json.loads(json_str)
        return cls.from_dict(data)
