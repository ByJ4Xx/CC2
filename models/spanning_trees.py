"""
Módulo de Árboles de Expansión
Implementa algoritmos para:
- Árboles generadores mínimos (MST) y máximos
- Centro y centroide del grafo
- Distancia entre árboles de expansión
- Algoritmos de Kruskal y Prim
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
import json
import networkx as nx
import numpy as np


@dataclass
class WeightedGraph:
    """
    Grafo ponderado para árboles de expansión
    Soporta grafos no dirigidos con pesos en las aristas
    """
    vertices: Set[str] = field(default_factory=set)
    edges: Dict[str, Tuple[str, str, float]] = field(default_factory=dict)  # nombre -> (v1, v2, peso)

    def __post_init__(self):
        """Valida que las aristas tengan vértices válidos"""
        for edge_name, (v1, v2, weight) in list(self.edges.items()):
            if v1 not in self.vertices or v2 not in self.vertices:
                self.vertices.add(v1)
                self.vertices.add(v2)

    def add_vertex(self, vertex: str) -> None:
        """Agrega un vértice al grafo"""
        self.vertices.add(vertex)

    def add_edge(self, edge_name: str, v1: str, v2: str, weight: float = 1.0) -> bool:
        """Agrega una arista ponderada entre dos vértices"""
        if v1 not in self.vertices or v2 not in self.vertices:
            return False
        self.edges[edge_name] = (v1, v2, weight)
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
        for edge_name, (v1, v2, weight) in self.edges.items():
            G.add_edge(v1, v2, name=edge_name, weight=weight)
        return G

    # ==================== ÁRBOLES GENERADORES ====================

    def minimum_spanning_tree(self, algorithm: str = "kruskal") -> Dict:
        """
        Calcula el árbol generador mínimo (MST)

        Args:
            algorithm: "kruskal" o "prim"

        Returns:
            Dict con información del MST
        """
        G = self._to_networkx()

        if not nx.is_connected(G):
            return {
                "success": False,
                "error": "El grafo no es conexo",
                "tree_edges": [],
                "total_weight": 0
            }

        if algorithm == "kruskal":
            mst = nx.minimum_spanning_tree(G, algorithm="kruskal")
        else:  # prim
            mst = nx.minimum_spanning_tree(G, algorithm="prim")

        # Extraer información del MST
        tree_edges = []
        total_weight = 0

        for u, v, data in mst.edges(data=True):
            edge_name = data.get("name", f"{u}-{v}")
            weight = data.get("weight", 1.0)
            tree_edges.append({
                "name": edge_name,
                "vertices": [u, v],
                "weight": weight
            })
            total_weight += weight

        return {
            "success": True,
            "algorithm": algorithm,
            "tree_edges": tree_edges,
            "edge_names": [e["name"] for e in tree_edges],
            "total_weight": total_weight,
            "num_edges": len(tree_edges)
        }

    def maximum_spanning_tree(self) -> Dict:
        """
        Calcula el árbol generador máximo
        Invierte los pesos y calcula el MST
        """
        G = self._to_networkx()

        if not nx.is_connected(G):
            return {
                "success": False,
                "error": "El grafo no es conexo",
                "tree_edges": [],
                "total_weight": 0
            }

        # Crear grafo con pesos invertidos
        G_inverted = nx.Graph()
        G_inverted.add_nodes_from(G.nodes())

        max_weight = max([data.get("weight", 1.0) for _, _, data in G.edges(data=True)])

        for u, v, data in G.edges(data=True):
            inverted_weight = max_weight + 1 - data.get("weight", 1.0)
            G_inverted.add_edge(u, v,
                              name=data.get("name", f"{u}-{v}"),
                              weight=inverted_weight,
                              original_weight=data.get("weight", 1.0))

        # Calcular MST del grafo invertido
        mst = nx.minimum_spanning_tree(G_inverted)

        # Extraer información del árbol máximo
        tree_edges = []
        total_weight = 0

        for u, v, data in mst.edges(data=True):
            edge_name = data.get("name", f"{u}-{v}")
            weight = data.get("original_weight", 1.0)
            tree_edges.append({
                "name": edge_name,
                "vertices": [u, v],
                "weight": weight
            })
            total_weight += weight

        return {
            "success": True,
            "algorithm": "maximum",
            "tree_edges": tree_edges,
            "edge_names": [e["name"] for e in tree_edges],
            "total_weight": total_weight,
            "num_edges": len(tree_edges)
        }

    # ==================== CENTRO Y CENTROIDE ====================

    def graph_center(self) -> Dict:
        """
        Calcula el centro del grafo
        El centro es el conjunto de vértices con excentricidad mínima
        Excentricidad = máxima distancia desde un vértice a todos los demás
        """
        G = self._to_networkx()

        if not nx.is_connected(G):
            return {
                "success": False,
                "error": "El grafo no es conexo"
            }

        # Calcular excentricidades
        eccentricity = nx.eccentricity(G)

        # Encontrar excentricidad mínima (radio)
        radius = min(eccentricity.values())

        # Centro: vértices con excentricidad igual al radio
        center_vertices = [v for v, e in eccentricity.items() if e == radius]

        # Diámetro: excentricidad máxima
        diameter = max(eccentricity.values())

        return {
            "success": True,
            "center_vertices": sorted(center_vertices),
            "radius": radius,
            "diameter": diameter,
            "eccentricities": {v: e for v, e in sorted(eccentricity.items())},
            "num_centers": len(center_vertices)
        }

    def graph_centroid(self) -> Dict:
        """
        Calcula el centroide del grafo
        El centroide minimiza la suma de distancias a todos los demás vértices
        """
        G = self._to_networkx()

        if not nx.is_connected(G):
            return {
                "success": False,
                "error": "El grafo no es conexo"
            }

        vertices_list = list(G.nodes())

        # Calcular suma de distancias para cada vértice
        distance_sums = {}

        for v in vertices_list:
            shortest_paths = nx.single_source_shortest_path_length(G, v)
            distance_sums[v] = sum(shortest_paths.values())

        # Encontrar mínimo
        min_sum = min(distance_sums.values())

        # Centroide: vértices con suma mínima
        centroid_vertices = [v for v, s in distance_sums.items() if s == min_sum]

        return {
            "success": True,
            "centroid_vertices": sorted(centroid_vertices),
            "min_distance_sum": min_sum,
            "distance_sums": {v: s for v, s in sorted(distance_sums.items())},
            "num_centroids": len(centroid_vertices)
        }

    # ==================== DISTANCIA ENTRE ÁRBOLES ====================

    def all_spanning_trees(self) -> List[Set[str]]:
        """
        Genera todos los árboles de expansión del grafo
        ADVERTENCIA: Puede ser muy lento para grafos grandes
        """
        G = self._to_networkx()

        if not nx.is_connected(G):
            return []

        n = len(G.nodes())
        m = len(G.edges())

        # Si ya es un árbol
        if m == n - 1:
            edge_names = set()
            for u, v, data in G.edges(data=True):
                edge_names.add(data.get("name", f"{u}-{v}"))
            return [edge_names]

        # Generar todos los árboles de expansión
        spanning_trees = []

        def is_spanning_tree(edge_set):
            """Verifica si un conjunto de aristas forma un árbol de expansión"""
            if len(edge_set) != n - 1:
                return False

            temp_graph = nx.Graph()
            temp_graph.add_nodes_from(G.nodes())

            for edge_name in edge_set:
                if edge_name in self.edges:
                    v1, v2, _ = self.edges[edge_name]
                    temp_graph.add_edge(v1, v2)

            return nx.is_tree(temp_graph) and len(temp_graph.nodes()) == n

        # Generar todas las combinaciones posibles
        from itertools import combinations

        all_edges = list(self.edges.keys())

        for edge_combo in combinations(all_edges, n - 1):
            edge_set = set(edge_combo)
            if is_spanning_tree(edge_set):
                spanning_trees.append(edge_set)

        return spanning_trees

    def tree_distance(self, tree1: Set[str], tree2: Set[str]) -> int:
        """
        Calcula la distancia entre dos árboles de expansión
        Distancia = número de aristas que difieren
        """
        symmetric_diff = tree1.symmetric_difference(tree2)
        return len(symmetric_diff)

    def all_tree_distances(self) -> Dict:
        """
        Calcula distancias entre todos los pares de árboles de expansión
        """
        trees = self.all_spanning_trees()

        if len(trees) == 0:
            return {
                "success": False,
                "error": "No se encontraron árboles de expansión"
            }

        if len(trees) > 100:
            return {
                "success": False,
                "error": f"Demasiados árboles ({len(trees)}). Límite: 100"
            }

        distances = []

        for i in range(len(trees)):
            for j in range(i + 1, len(trees)):
                dist = self.tree_distance(trees[i], trees[j])
                distances.append({
                    "tree1_id": i + 1,
                    "tree2_id": j + 1,
                    "distance": dist,
                    "tree1_edges": sorted(list(trees[i])),
                    "tree2_edges": sorted(list(trees[j]))
                })

        # Ordenar por distancia
        distances.sort(key=lambda x: x["distance"])

        return {
            "success": True,
            "num_trees": len(trees),
            "num_pairs": len(distances),
            "distances": distances,
            "max_distance": max([d["distance"] for d in distances]) if distances else 0,
            "min_distance": min([d["distance"] for d in distances]) if distances else 0
        }

    # ==================== CAMINOS Y ANÁLISIS ====================

    def is_connected(self) -> bool:
        """Verifica si el grafo es conexo"""
        G = self._to_networkx()
        return nx.is_connected(G)

    def shortest_path_weighted(self, v1: str, v2: str) -> Optional[Dict]:
        """Encuentra el camino más corto ponderado entre dos vértices"""
        G = self._to_networkx()
        try:
            path = nx.shortest_path(G, v1, v2, weight="weight")
            length = nx.shortest_path_length(G, v1, v2, weight="weight")
            return {
                "path": path,
                "length": length,
                "num_edges": len(path) - 1
            }
        except nx.NetworkXNoPath:
            return None

    # ==================== PERSISTENCIA ====================

    def to_dict(self) -> dict:
        """Convierte el grafo a diccionario"""
        return {
            "vertices": sorted(list(self.vertices)),
            "edges": {
                name: {"v1": v1, "v2": v2, "weight": weight}
                for name, (v1, v2, weight) in self.edges.items()
            }
        }

    def to_json(self) -> str:
        """Exporta el grafo a JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> WeightedGraph:
        """Crea un grafo desde un diccionario"""
        graph = cls(vertices=set(data["vertices"]))
        for name, edge_data in data["edges"].items():
            graph.add_edge(name, edge_data["v1"], edge_data["v2"], edge_data["weight"])
        return graph

    @classmethod
    def from_json(cls, json_str: str) -> WeightedGraph:
        """Importa un grafo desde JSON"""
        data = json.loads(json_str)
        return cls.from_dict(data)
