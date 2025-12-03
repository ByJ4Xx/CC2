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
    Soporta grafos dirigidos o no dirigidos con vértices y aristas nombradas
    Opcionalmente permite asignar pesos a las aristas
    """
    vertices: Set[str] = field(default_factory=set)
    edges: Dict[str, Tuple[str, str, Optional[float]]] = field(default_factory=dict)  # nombre -> (v1, v2, weight)
    is_directed: bool = False
    has_weights: bool = False

    def __post_init__(self):
        """Valida que las aristas tengan vértices válidos"""
        for edge_name, edge_data in list(self.edges.items()):
            if isinstance(edge_data, tuple) and len(edge_data) >= 2:
                v1, v2 = edge_data[0], edge_data[1]
                if v1 not in self.vertices or v2 not in self.vertices:
                    # Agregar vértices automáticamente si no existen
                    self.vertices.add(v1)
                    self.vertices.add(v2)

    def add_vertex(self, vertex: str) -> None:
        """Agrega un vértice al grafo"""
        self.vertices.add(vertex)

    def remove_vertex(self, vertex: str) -> bool:
        """Elimina un vértice y todas sus aristas asociadas"""
        if vertex not in self.vertices:
            return False
        self.vertices.discard(vertex)
        # Eliminar aristas que contienen este vértice
        edges_to_remove = [name for name, edge_data in self.edges.items()
                          if edge_data[0] == vertex or edge_data[1] == vertex]
        for edge_name in edges_to_remove:
            del self.edges[edge_name]
        return True

    def add_edge(self, edge_name: str, v1: str, v2: str, weight: Optional[float] = None) -> bool:
        """Agrega una arista entre dos vértices"""
        if v1 not in self.vertices or v2 not in self.vertices:
            return False
        if weight is not None:
            self.edges[edge_name] = (v1, v2, weight)
        else:
            self.edges[edge_name] = (v1, v2, 1.0)
        return True

    def remove_edge(self, edge_name: str) -> bool:
        """Elimina una arista por nombre"""
        if edge_name in self.edges:
            del self.edges[edge_name]
            return True
        return False

    def modify_edge(self, edge_name: str, v1: str, v2: str, weight: Optional[float] = None) -> bool:
        """Modifica una arista existente"""
        if edge_name not in self.edges:
            return False
        if v1 not in self.vertices or v2 not in self.vertices:
            return False
        if weight is not None:
            self.edges[edge_name] = (v1, v2, weight)
        else:
            self.edges[edge_name] = (v1, v2, 1.0)
        return True

    def _to_networkx(self):
        """Convierte el grafo a formato NetworkX"""
        if self.is_directed:
            G = nx.DiGraph()
        else:
            G = nx.Graph()

        G.add_nodes_from(self.vertices)
        for edge_name, edge_data in self.edges.items():
            v1, v2 = edge_data[0], edge_data[1]
            weight = edge_data[2] if len(edge_data) > 2 else 1.0
            G.add_edge(v1, v2, name=edge_name, weight=weight)
        return G

    # ==================== MATRICES ====================

    def vertex_adjacency_matrix(self) -> Tuple[np.ndarray, List[str]]:
        """
        Matriz de adyacencia de vértices
        Para grafos NO dirigidos: M[i][j] = número de aristas entre vértice i y vértice j (simétrica)
        Para grafos DIRIGIDOS: M[i][j] = número de aristas desde vértice i hacia vértice j
        """
        vertices_list = sorted(list(self.vertices))
        n = len(vertices_list)
        matrix = np.zeros((n, n), dtype=int)

        vertex_to_idx = {v: i for i, v in enumerate(vertices_list)}

        for edge_data in self.edges.values():
            v1, v2 = edge_data[0], edge_data[1]
            i = vertex_to_idx[v1]
            j = vertex_to_idx[v2]
            if self.is_directed:
                # Solo desde v1 hacia v2
                matrix[i][j] += 1
            else:
                # Bidireccional
                matrix[i][j] += 1
                matrix[j][i] += 1

        return matrix, vertices_list

    def edge_adjacency_matrix(self) -> Tuple[np.ndarray, List[str]]:
        """
        Matriz de adyacencia de aristas
        M[i][j] = 1 si las aristas i y j comparten un vértice, 0 en caso contrario
        (Mismo para dirigidos y no dirigidos)
        """
        edges_list = sorted(list(self.edges.keys()))
        n = len(edges_list)
        matrix = np.zeros((n, n), dtype=int)

        for i, edge1 in enumerate(edges_list):
            edge_data1 = self.edges[edge1]
            v1_set = {edge_data1[0], edge_data1[1]}
            for j, edge2 in enumerate(edges_list):
                if i != j:
                    edge_data2 = self.edges[edge2]
                    v2_set = {edge_data2[0], edge_data2[1]}
                    if v1_set & v2_set:  # Intersección no vacía
                        matrix[i][j] = 1

        return matrix, edges_list

    def vertex_incidence_matrix(self) -> Tuple[np.ndarray, List[str], List[str]]:
        """
        Matriz de incidencia vértice-arista
        Para grafos NO dirigidos: M[i][j] = 1 si el vértice i es incidente a la arista j
        Para grafos DIRIGIDOS:
            - M[i][j] = 1 si la arista sale del vértice i (vértice es la cola)
            - M[i][j] = -1 si la arista entra al vértice i (vértice es la cabeza)
            - M[i][j] = 0 en caso contrario
        """
        vertices_list = sorted(list(self.vertices))
        edges_list = sorted(list(self.edges.keys()))

        n_vertices = len(vertices_list)
        n_edges = len(edges_list)
        matrix = np.zeros((n_vertices, n_edges), dtype=int)

        vertex_to_idx = {v: i for i, v in enumerate(vertices_list)}

        for j, edge_name in enumerate(edges_list):
            edge_data = self.edges[edge_name]
            v1, v2 = edge_data[0], edge_data[1]
            i1 = vertex_to_idx[v1]
            i2 = vertex_to_idx[v2]

            if self.is_directed:
                # Para grafos dirigidos: v1 es la cola (sale=1), v2 es la cabeza (entra=-1)
                matrix[i1][j] = 1   # Arista sale de v1
                matrix[i2][j] = -1  # Arista entra a v2
            else:
                # Para grafos no dirigidos: ambos vértices son incidentes (1)
                matrix[i1][j] = 1
                if v1 != v2:  # No contar loops dos veces
                    matrix[i2][j] = 1

        return matrix, vertices_list, edges_list

    def edge_incidence_matrix(self) -> Tuple[np.ndarray, List[str], List[str]]:
        """
        Matriz de incidencia arista-vértice (transpuesta de vertex_incidence)
        Para grafos NO dirigidos: M[i][j] = 1 si la arista i es incidente al vértice j
        Para grafos DIRIGIDOS:
            - M[i][j] = 1 si la arista i sale del vértice j (vértice es la cola)
            - M[i][j] = -1 si la arista i entra al vértice j (vértice es la cabeza)
            - M[i][j] = 0 en caso contrario
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

        Para grafos DIRIGIDOS: También retorna información de dirección
        - edge_directions: dict con edge_name -> 1 (dirección correcta) o -1 (dirección opuesta)
        """
        cycles = self.find_all_cycles()
        circuits = []

        for i, cycle in enumerate(cycles):
            # Encontrar las aristas del circuito
            circuit_edges = []
            edge_directions = {}  # Para grafos dirigidos

            for j in range(len(cycle)):
                v1 = cycle[j]
                v2 = cycle[(j + 1) % len(cycle)]

                # Buscar la arista entre v1 y v2
                for edge_name, edge_data in self.edges.items():
                    e_v1, e_v2 = edge_data[0], edge_data[1]
                    if self.is_directed:
                        # Para dirigidos: buscar arista exacta en la dirección del ciclo
                        if e_v1 == v1 and e_v2 == v2:
                            circuit_edges.append(edge_name)
                            edge_directions[edge_name] = 1
                            break
                        elif e_v1 == v2 and e_v2 == v1:
                            # La arista existe pero en dirección opuesta
                            circuit_edges.append(edge_name)
                            edge_directions[edge_name] = -1
                            break
                    else:
                        # Para no dirigidos: buscar en ambas direcciones
                        if (e_v1 == v1 and e_v2 == v2) or (e_v1 == v2 and e_v2 == v1):
                            circuit_edges.append(edge_name)
                            edge_directions[edge_name] = 1
                            break

            circuit_data = {
                "id": i + 1,
                "vertices": cycle,
                "edges": circuit_edges,
                "length": len(cycle)
            }

            # Agregar información de dirección para grafos dirigidos
            if self.is_directed:
                circuit_data["edge_directions"] = edge_directions

            circuits.append(circuit_data)

        return circuits

    def fundamental_cycles(self, spanning_tree_edges: Optional[Set[str]] = None) -> List[Dict]:
        """
        Encuentra los ciclos fundamentales respecto a un árbol generador
        Si no se proporciona árbol, se calcula uno usando DFS

        Para grafos DIRIGIDOS: Retorna también edge_directions con información de dirección
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
            edge_data = self.edges[chord_name]
            v1, v2 = edge_data[0], edge_data[1]

            # Crear subgrafo solo con aristas del árbol
            tree_graph = nx.Graph()
            tree_graph.add_nodes_from(G.nodes())
            for edge_name in spanning_tree_edges:
                edge_data = self.edges[edge_name]
                e_v1, e_v2 = edge_data[0], edge_data[1]
                tree_graph.add_edge(e_v1, e_v2, name=edge_name)

            try:
                # Encontrar camino en el árbol entre v1 y v2
                path = nx.shortest_path(tree_graph, v1, v2)

                # Construir lista de aristas del camino con dirección
                path_edges = []
                edge_directions = {}
                for i in range(len(path) - 1):
                    for edge_name in spanning_tree_edges:
                        edge_data = self.edges[edge_name]
                        e_v1, e_v2 = edge_data[0], edge_data[1]
                        if e_v1 == path[i] and e_v2 == path[i+1]:
                            path_edges.append(edge_name)
                            edge_directions[edge_name] = 1
                            break
                        elif e_v1 == path[i+1] and e_v2 == path[i]:
                            path_edges.append(edge_name)
                            edge_directions[edge_name] = -1
                            break

                # El ciclo fundamental es el camino + la cuerda
                cycle_data = {
                    "chord": chord_name,
                    "vertices": path,
                    "tree_edges": path_edges,
                    "all_edges": path_edges + [chord_name],
                    "length": len(path)
                }

                # Agregar dirección de la cuerda si es dirigido
                if self.is_directed:
                    edge_directions[chord_name] = 1  # La cuerda siempre se cuenta en su dirección original
                    cycle_data["edge_directions"] = edge_directions

                fundamental.append(cycle_data)
            except nx.NetworkXNoPath:
                continue

        return fundamental

    # ==================== CONJUNTOS DE CORTE ====================

    def find_cut_sets(self) -> List[Dict]:
        """
        Encuentra conjuntos de corte (edge cuts) mínimos del grafo.
        Un conjunto de corte es un conjunto mínimo de aristas cuya remoción
        desconecta el grafo o aumenta el número de componentes conexas.

        Para grafos DIRIGIDOS: Se trata el grafo como no dirigido para encontrar cortes
        """
        from itertools import combinations

        G = self._to_networkx()

        if not nx.is_connected(G):
            return {
                "success": False,
                "error": "El grafo no es conexo",
                "cut_sets": []
            }

        cut_sets = []
        edge_names_list = list(self.edges.keys())

        # Buscar puentes (aristas cuya remoción desconecta el grafo)
        bridges = list(nx.bridges(G))
        bridge_names = []
        for bridge in bridges:
            # Encontrar el nombre de la arista
            for edge_name, edge_data in self.edges.items():
                v1, v2 = edge_data[0], edge_data[1]
                if (v1, v2) == bridge or (v2, v1) == bridge:
                    bridge_names.append(edge_name)
                    cut_sets.append({
                        "edges": [edge_name],
                        "size": 1,
                        "type": "bridge",
                        "cardinality": 1
                    })
                    break

        # Buscar conjuntos de corte de mayor cardinalidad
        if len(edge_names_list) <= 15:  # Solo para grafos pequeños
            # Buscar por cardinalidad: primero de tamaño 2, luego 3, etc.
            for size in range(2, len(edge_names_list)):
                found_any = False

                for combination in combinations(edge_names_list, size):
                    # Crear grafo de prueba sin estas aristas
                    G_test = nx.Graph()
                    G_test.add_nodes_from(self.vertices)

                    for edge_name, edge_data in self.edges.items():
                        if edge_name not in combination:
                            v1, v2 = edge_data[0], edge_data[1]
                            G_test.add_edge(v1, v2)

                    # Verificar si es un conjunto de corte
                    if not nx.is_connected(G_test):
                        # Verificar que no es superset de otro conjunto de corte
                        is_minimal = True
                        for cut_set in cut_sets:
                            if set(cut_set["edges"]).issubset(set(combination)):
                                is_minimal = False
                                break

                        # Verificar que no es duplicado
                        is_duplicate = any(
                            set(cs["edges"]) == set(combination) for cs in cut_sets
                        )

                        if is_minimal and not is_duplicate:
                            cut_sets.append({
                                "edges": list(combination),
                                "size": len(combination),
                                "type": "cut_set",
                                "cardinality": size
                            })
                            found_any = True

                # Si no encontramos conjuntos de este tamaño, no buscar tamaños mayores
                if not found_any:
                    break

        return {
            "success": True,
            "cut_sets": cut_sets,
            "num_cut_sets": len(cut_sets),
            "bridges": len(bridges)
        }

    def fundamental_cut_sets(self, spanning_tree_edges: Optional[Set[str]] = None) -> List[Dict]:
        """
        Encuentra los conjuntos de corte fundamentales respecto a un árbol generador
        Para cada arista del árbol, su conjunto de corte fundamental es el conjunto
        de aristas cuya eliminación desconecta el grafo en dos componentes

        Para grafos DIRIGIDOS: Se trata el grafo como no dirigido para encontrar cortes
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
            edge_data = self.edges[tree_edge_name]
            v1, v2 = edge_data[0], edge_data[1]

            # Remover la arista del árbol para obtener dos componentes
            temp_tree = nx.Graph()
            temp_tree.add_nodes_from(G.nodes())

            for edge_name in spanning_tree_edges:
                if edge_name != tree_edge_name:
                    edge_data = self.edges[edge_name]
                    e_v1, e_v2 = edge_data[0], edge_data[1]
                    temp_tree.add_edge(e_v1, e_v2)

            # Encontrar las dos componentes
            components = list(nx.connected_components(temp_tree))

            if len(components) == 2:
                comp1, comp2 = components

                # Encontrar todas las aristas que cruzan entre las componentes
                cut_edges = [tree_edge_name]  # Incluir la arista del árbol

                for edge_name, edge_data in self.edges.items():
                    if edge_name != tree_edge_name:
                        e_v1, e_v2 = edge_data[0], edge_data[1]
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
        edges_dict = {}
        for name, edge_data in self.edges.items():
            v1, v2 = edge_data[0], edge_data[1]
            weight = edge_data[2] if len(edge_data) > 2 else 1.0
            edges_dict[name] = [v1, v2, weight]

        return {
            "vertices": sorted(list(self.vertices)),
            "edges": edges_dict,
            "is_directed": self.is_directed,
            "has_weights": self.has_weights
        }

    def to_json(self) -> str:
        """Exporta el grafo a JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> GraphTheory:
        """Crea un grafo desde un diccionario"""
        graph = cls(
            vertices=set(data["vertices"]),
            is_directed=data.get("is_directed", False),
            has_weights=data.get("has_weights", False)
        )
        for name, edge_info in data["edges"].items():
            if isinstance(edge_info, (list, tuple)) and len(edge_info) >= 2:
                v1, v2 = edge_info[0], edge_info[1]
                weight = edge_info[2] if len(edge_info) > 2 else 1.0
                graph.add_edge(name, v1, v2, weight)
        return graph

    @classmethod
    def from_json(cls, json_str: str) -> GraphTheory:
        """Importa un grafo desde JSON"""
        data = json.loads(json_str)
        return cls.from_dict(data)
