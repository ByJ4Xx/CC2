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
    Grafo para árboles de expansión
    Soporta grafos dirigidos/no dirigidos, con o sin pesos
    """
    vertices: Set[str] = field(default_factory=set)
    edges: Dict[str, Tuple[str, str, float]] = field(default_factory=dict)  # nombre -> (v1, v2, peso)
    is_directed: bool = False  # True para grafos dirigidos
    has_weights: bool = True   # True para grafos con pesos, False para no ponderados

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

    def remove_vertex(self, vertex: str) -> bool:
        """Elimina un vértice y todas sus aristas asociadas"""
        if vertex not in self.vertices:
            return False

        self.vertices.discard(vertex)
        # Eliminar todas las aristas que contienen este vértice
        edges_to_remove = [
            name for name, (v1, v2, weight) in self.edges.items()
            if v1 == vertex or v2 == vertex
        ]
        for edge_name in edges_to_remove:
            del self.edges[edge_name]
        return True

    def edit_edge(self, edge_name: str, new_weight: float) -> bool:
        """Modifica el peso de una arista existente"""
        if edge_name not in self.edges:
            return False
        v1, v2, _ = self.edges[edge_name]
        self.edges[edge_name] = (v1, v2, new_weight)
        return True

    def get_graph_info(self) -> Dict:
        """Retorna información completa del grafo"""
        total_weight = sum(w for _, _, w in self.edges.values())

        # Calcular grado de cada vértice
        degrees = {}
        for vertex in self.vertices:
            degree = 0
            for _, (v1, v2, _) in self.edges.items():
                if self.is_directed:
                    if v1 == vertex:
                        degree += 1  # Grado de salida
                else:
                    if v1 == vertex or v2 == vertex:
                        degree += 1
            degrees[vertex] = degree

        return {
            "num_vertices": len(self.vertices),
            "num_edges": len(self.edges),
            "is_directed": self.is_directed,
            "has_weights": self.has_weights,
            "is_connected": self.is_connected(),
            "total_weight": total_weight,
            "degrees": degrees,
            "vertices": sorted(list(self.vertices)),
            "edges": [
                {
                    "name": name,
                    "v1": v1,
                    "v2": v2,
                    "weight": weight
                }
                for name, (v1, v2, weight) in sorted(self.edges.items())
            ]
        }

    def _to_networkx(self) -> nx.Graph:
        """Convierte el grafo a formato NetworkX"""
        G = nx.Graph()
        G.add_nodes_from(self.vertices)
        for edge_name, (v1, v2, weight) in self.edges.items():
            G.add_edge(v1, v2, name=edge_name, weight=weight)
        return G

    def get_complement_graph(self) -> 'WeightedGraph':
        """
        Calcula el complemento del grafo
        Retorna un nuevo grafo con las aristas que no existen en el original
        """
        complement = WeightedGraph(
            is_directed=self.is_directed,
            has_weights=self.has_weights
        )
        complement.vertices = self.vertices.copy()

        # Obtener todas las aristas posibles
        vertices_list = sorted(list(self.vertices))
        existing_edges = set()

        # Guardar pares de vértices que ya tienen arista
        for v1, v2, _ in self.edges.values():
            edge_pair = tuple(sorted([v1, v2]))
            existing_edges.add(edge_pair)

        # Agregar aristas que NO existen en el grafo original
        edge_counter = 1
        for i, v1 in enumerate(vertices_list):
            for v2 in vertices_list[i + 1:]:
                edge_pair = tuple(sorted([v1, v2]))
                if edge_pair not in existing_edges:
                    complement.add_edge(f"c{edge_counter}", v1, v2, weight=1.0)
                    edge_counter += 1

        return complement

    def get_mst_complement(self, mst_edges: Set[str]) -> 'WeightedGraph':
        """
        Calcula el complemento del MST dentro del grafo original
        Retorna un nuevo grafo con las aristas del original que NO están en el MST

        Fórmula: Original = MST + Complemento del MST

        Args:
            mst_edges: Conjunto de nombres de aristas que forman el MST

        Returns:
            WeightedGraph con las aristas restantes (Original - MST)
        """
        complement = WeightedGraph(
            is_directed=self.is_directed,
            has_weights=self.has_weights
        )
        complement.vertices = self.vertices.copy()

        # Agregar todas las aristas del grafo original que NO están en el MST
        for edge_name, (v1, v2, weight) in self.edges.items():
            if edge_name not in mst_edges:
                complement.add_edge(edge_name, v1, v2, weight)

        return complement

    def get_subgraph(self, vertices_subset: Set[str]) -> 'WeightedGraph':
        """
        Crea un subgrafo con solo los vértices especificados y sus aristas
        """
        subgraph = WeightedGraph(
            is_directed=self.is_directed,
            has_weights=self.has_weights
        )
        subgraph.vertices = vertices_subset.copy()

        # Agregar solo las aristas cuyos vértices están en el subconjunto
        for edge_name, (v1, v2, weight) in self.edges.items():
            if v1 in vertices_subset and v2 in vertices_subset:
                subgraph.add_edge(edge_name, v1, v2, weight)

        return subgraph

    def find_tree_center(self, spanning_tree_edges: Optional[Set[str]] = None) -> Dict:
        """
        Encuentra el centro del grafo basándose en la tabla de excentricidades
        El centro está formado por el vértice (o vértices) con excentricidad mínima (radio)

        Args:
            spanning_tree_edges: No utilizado (parámetro por compatibilidad)

        Returns:
            Dict con información del centro
        """
        # Usar Floyd-Warshall para obtener excentricidades
        fw_result = self.floyd_warshall()

        if not fw_result["success"]:
            return {
                "success": False,
                "error": fw_result.get("error", "Error en Floyd-Warshall")
            }

        eccentricities = fw_result["eccentricities"]
        radius = fw_result["radius"]

        # El centro es el conjunto de vértices con excentricidad igual al radio
        center_vertices = sorted([v for v, ecc in eccentricities.items() if ecc == radius])

        # Verificar si es centro (1 vértice) o bicentro (2 vértices)
        is_bicentro = len(center_vertices) == 2
        is_connected_bicentro = False

        if is_bicentro:
            # Verificar si los dos vértices están conectados directamente
            v1, v2 = center_vertices[0], center_vertices[1]
            for edge_name, (edge_v1, edge_v2, _) in self.edges.items():
                if (edge_v1 == v1 and edge_v2 == v2) or (edge_v1 == v2 and edge_v2 == v1):
                    is_connected_bicentro = True
                    break

        return {
            "success": True,
            "center_vertices": center_vertices,
            "is_center": len(center_vertices) == 1,
            "is_bicentro": is_bicentro,
            "is_connected_bicentro": is_connected_bicentro,
            "num_centers": len(center_vertices),
            "radius": radius,
            "eccentricities": eccentricities
        }

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

    def is_tree(self, edge_names: Set[str]) -> bool:
        """
        Verifica si un conjunto de nombres de aristas forma un árbol válido.

        Un árbol válido debe:
        1. Tener exactamente n-1 aristas (donde n es el número de vértices)
        2. Ser conexo (todos los vértices conectados)
        3. No tener ciclos

        Args:
            edge_names: Conjunto de nombres de aristas a verificar

        Returns:
            True si forma un árbol válido, False en caso contrario
        """
        n = len(self.vertices)

        # Un árbol debe tener exactamente n-1 aristas
        if len(edge_names) != n - 1:
            return False

        # Crear grafo temporal con las aristas especificadas
        temp_graph = nx.Graph()
        temp_graph.add_nodes_from(self.vertices)

        for edge_name in edge_names:
            if edge_name not in self.edges:
                return False
            v1, v2, _ = self.edges[edge_name]
            temp_graph.add_edge(v1, v2)

        # Verificar que sea un árbol (conexo y sin ciclos)
        return nx.is_tree(temp_graph)

    def tree_distance(self, tree1: Set[str], tree2: Set[str]) -> Dict:
        """
        Calcula la distancia entre dos árboles de expansión usando la fórmula:
        Distancia = ((Unión - Intersección) / 2)

        Donde:
        - Unión: número de aristas que pertenecen a alguno de los dos árboles
        - Intersección: número de aristas comunes a ambos árboles
        - Distancia: número de aristas que difieren entre los dos árboles

        Args:
            tree1: Conjunto de nombres de aristas del primer árbol
            tree2: Conjunto de nombres de aristas del segundo árbol

        Returns:
            Diccionario con:
            - success: bool
            - tree1_edges: Aristas del primer árbol
            - tree2_edges: Aristas del segundo árbol
            - union: Aristas en alguno de los dos árboles
            - intersection: Aristas comunes
            - union_count: Número de aristas en la unión
            - intersection_count: Número de aristas en la intersección
            - distance: Distancia calculada
            - symmetric_difference: Aristas que difieren
            - error: Mensaje de error (si aplica)
        """
        # Verificar si ambos son árboles válidos
        if not self.is_tree(tree1):
            return {
                "success": False,
                "error": "El primer conjunto de aristas no forma un árbol válido"
            }

        if not self.is_tree(tree2):
            return {
                "success": False,
                "error": "El segundo conjunto de aristas no forma un árbol válido"
            }

        # Calcular unión e intersección
        union = tree1.union(tree2)
        intersection = tree1.intersection(tree2)
        symmetric_diff = tree1.symmetric_difference(tree2)

        # Calcular distancia usando la fórmula: (unión - intersección) / 2
        union_count = len(union)
        intersection_count = len(intersection)
        distance = (union_count - intersection_count) / 2

        return {
            "success": True,
            "tree1_edges": sorted(list(tree1)),
            "tree2_edges": sorted(list(tree2)),
            "union": sorted(list(union)),
            "intersection": sorted(list(intersection)),
            "symmetric_difference": sorted(list(symmetric_diff)),
            "union_count": union_count,
            "intersection_count": intersection_count,
            "symmetric_difference_count": len(symmetric_diff),
            "distance": distance,
            "is_identical": tree1 == tree2
        }

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

    # ==================== RAMAS Y CUERDAS ====================

    def identify_branches_and_chords(self, spanning_tree_edges: Optional[Set[str]] = None) -> Dict:
        """
        Identifica las ramas (aristas del árbol) y cuerdas (aristas del complemento)

        Args:
            spanning_tree_edges: Conjunto de nombres de aristas del árbol.
                                Si es None, se calcula el MST automáticamente.

        Returns:
            Dict con información de ramas y cuerdas
        """
        G = self._to_networkx()

        if not nx.is_connected(G):
            return {
                "success": False,
                "error": "El grafo no es conexo"
            }

        # Si no se proporciona árbol, calcular MST
        if spanning_tree_edges is None:
            mst_result = self.minimum_spanning_tree()
            if not mst_result["success"]:
                return mst_result
            spanning_tree_edges = set(mst_result["edge_names"])

        # Separar ramas y cuerdas
        branches = []
        chords = []

        for edge_name, (v1, v2, weight) in self.edges.items():
            edge_info = {
                "name": edge_name,
                "vertices": [v1, v2],
                "weight": weight
            }

            if edge_name in spanning_tree_edges:
                branches.append(edge_info)
            else:
                chords.append(edge_info)

        return {
            "success": True,
            "branches": branches,
            "chords": chords,
            "num_branches": len(branches),
            "num_chords": len(chords),
            "tree_edges": spanning_tree_edges
        }

    def find_cut_sets(self) -> Dict:
        """
        Encuentra los conjuntos de corte del grafo.
        Un conjunto de corte es un conjunto mínimo de aristas cuya remoción
        desconecta el grafo o aumenta el número de componentes conexas.

        Returns:
            Dict con los conjuntos de corte encontrados
        """
        from itertools import combinations

        G = self._to_networkx()

        if not nx.is_connected(G):
            return {
                "success": False,
                "error": "El grafo no es conexo"
            }

        cut_sets = []
        edge_names_list = list(self.edges.keys())

        # Buscar puentes (aristas cuya remoción desconecta el grafo)
        bridges = list(nx.bridges(G))
        bridge_names = []
        for bridge in bridges:
            # Encontrar el nombre de la arista
            for edge_name, (v1, v2, _) in self.edges.items():
                if (v1, v2) == bridge or (v2, v1) == bridge:
                    bridge_names.append(edge_name)
                    cut_sets.append({
                        "edges": [edge_name],
                        "vertices": [v1, v2],
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

                    for edge_name, (v1, v2, weight) in self.edges.items():
                        if edge_name not in combination:
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
                            # Obtener vértices involucrados
                            vertices_involved = set()
                            for edge_name in combination:
                                v1, v2, _ = self.edges[edge_name]
                                vertices_involved.add(v1)
                                vertices_involved.add(v2)

                            cut_sets.append({
                                "edges": list(combination),
                                "vertices": sorted(list(vertices_involved)),
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

    def find_fundamental_cycles(self, spanning_tree_edges: Optional[Set[str]] = None) -> Dict:
        """
        Encuentra todos los ciclos fundamentales del grafo.
        Un ciclo fundamental es un ciclo que contiene exactamente una cuerda (arista no en el árbol).

        Args:
            spanning_tree_edges: Conjunto de nombres de aristas del árbol.
                                Si es None, se calcula el MST automáticamente.

        Returns:
            Dict con los ciclos fundamentales encontrados
        """
        G = self._to_networkx()

        if not nx.is_connected(G):
            return {
                "success": False,
                "error": "El grafo no es conexo"
            }

        # Si no se proporciona árbol, calcular MST
        if spanning_tree_edges is None:
            mst_result = self.minimum_spanning_tree()
            if not mst_result["success"]:
                return mst_result
            spanning_tree_edges = set(mst_result["edge_names"])

        # Identificar cuerdas (aristas no en el árbol)
        all_edges = set(self.edges.keys())
        chords = all_edges - spanning_tree_edges

        # Para cada cuerda, encontrar el ciclo fundamental
        fundamental_cycles = []

        for chord_name in chords:
            v1_chord, v2_chord, _ = self.edges[chord_name]

            # Crear grafo del árbol (solo ramas)
            tree_graph = nx.Graph()
            tree_graph.add_nodes_from(self.vertices)

            for edge_name in spanning_tree_edges:
                v1, v2, _ = self.edges[edge_name]
                tree_graph.add_edge(v1, v2)

            # Encontrar camino en el árbol entre los vértices de la cuerda
            try:
                path_in_tree = nx.shortest_path(tree_graph, v1_chord, v2_chord)
            except nx.NetworkXNoPath:
                continue

            # El ciclo fundamental = camino en árbol + cuerda
            cycle_edges = []

            # Agregar aristas del camino
            for i in range(len(path_in_tree) - 1):
                u, v = path_in_tree[i], path_in_tree[i + 1]
                # Encontrar el nombre de la arista
                for edge_name in spanning_tree_edges:
                    e_v1, e_v2, _ = self.edges[edge_name]
                    if (e_v1 == u and e_v2 == v) or (e_v1 == v and e_v2 == u):
                        cycle_edges.append(edge_name)
                        break

            # Agregar la cuerda
            cycle_edges.append(chord_name)

            # Obtener vértices del ciclo
            cycle_vertices = set()
            for edge_name in cycle_edges:
                v1, v2, _ = self.edges[edge_name]
                cycle_vertices.add(v1)
                cycle_vertices.add(v2)

            fundamental_cycles.append({
                "edges": cycle_edges,
                "vertices": sorted(list(cycle_vertices)),
                "chord": chord_name,
                "num_edges": len(cycle_edges)
            })

        return {
            "success": True,
            "fundamental_cycles": fundamental_cycles,
            "num_cycles": len(fundamental_cycles),
            "tree_edges": spanning_tree_edges
        }

    def find_fundamental_cut_sets(self, spanning_tree_edges: Optional[Set[str]] = None) -> Dict:
        """
        Encuentra los conjuntos de corte fundamentales del grafo.
        Un conjunto de corte fundamental contiene exactamente una rama (arista del árbol).

        Args:
            spanning_tree_edges: Conjunto de nombres de aristas del árbol.
                                Si es None, se calcula el MST automáticamente.

        Returns:
            Dict con los conjuntos de corte fundamentales encontrados
        """
        G = self._to_networkx()

        if not nx.is_connected(G):
            return {
                "success": False,
                "error": "El grafo no es conexo"
            }

        # Si no se proporciona árbol, calcular MST
        if spanning_tree_edges is None:
            mst_result = self.minimum_spanning_tree()
            if not mst_result["success"]:
                return mst_result
            spanning_tree_edges = set(mst_result["edge_names"])

        fundamental_cut_sets = []

        # Para cada rama, encontrar el conjunto de corte fundamental
        for branch_name in spanning_tree_edges:
            v1_branch, v2_branch, _ = self.edges[branch_name]

            # Crear grafo del árbol sin esta rama
            tree_graph = nx.Graph()
            tree_graph.add_nodes_from(self.vertices)

            for edge_name in spanning_tree_edges:
                if edge_name != branch_name:
                    v1, v2, _ = self.edges[edge_name]
                    tree_graph.add_edge(v1, v2)

            # Encontrar componentes conexas del árbol sin esta rama
            tree_components = list(nx.connected_components(tree_graph))

            if len(tree_components) != 2:
                continue

            # Encontrar aristas del grafo original que cruzan entre las dos componentes
            comp1, comp2 = tree_components[0], tree_components[1]
            cut_edges = []

            for edge_name, (u, v, _) in self.edges.items():
                if (u in comp1 and v in comp2) or (u in comp2 and v in comp1):
                    cut_edges.append(edge_name)

            # Obtener vértices del conjunto de corte
            cut_vertices = set()
            for edge_name in cut_edges:
                v1, v2, _ = self.edges[edge_name]
                cut_vertices.add(v1)
                cut_vertices.add(v2)

            fundamental_cut_sets.append({
                "edges": sorted(cut_edges),
                "vertices": sorted(list(cut_vertices)),
                "branch": branch_name,
                "num_edges": len(cut_edges)
            })

        return {
            "success": True,
            "fundamental_cut_sets": fundamental_cut_sets,
            "num_cut_sets": len(fundamental_cut_sets),
            "tree_edges": spanning_tree_edges
        }

    # ==================== ALGORITMO DE FLOYD-WARSHALL ====================

    def floyd_warshall(self) -> Dict:
        """
        Implementa el algoritmo de Floyd-Warshall para encontrar
        caminos más cortos entre todos los pares de vértices.

        Returns:
            Dict con matrices de distancias y caminos
        """
        vertices_list = sorted(list(self.vertices))
        n = len(vertices_list)

        if n == 0:
            return {
                "success": False,
                "error": "El grafo está vacío"
            }

        # Inicializar matriz de distancias con infinito
        INF = float('inf')
        dist = [[INF for _ in range(n)] for _ in range(n)]
        next_vertex = [[None for _ in range(n)] for _ in range(n)]

        # Mapeo de vértice a índice
        vertex_to_idx = {v: i for i, v in enumerate(vertices_list)}

        # Distancia de un vértice a sí mismo es 0
        for i in range(n):
            dist[i][i] = 0
            next_vertex[i][i] = i

        # Inicializar con las aristas existentes
        for edge_name, (v1, v2, weight) in self.edges.items():
            i = vertex_to_idx[v1]
            j = vertex_to_idx[v2]
            dist[i][j] = weight
            dist[j][i] = weight
            next_vertex[i][j] = j
            next_vertex[j][i] = i

        # Algoritmo de Floyd-Warshall
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        next_vertex[i][j] = next_vertex[i][k]

        # Construir caminos
        def reconstruct_path(i: int, j: int) -> List[str]:
            """Reconstruye el camino de i a j"""
            if next_vertex[i][j] is None:
                return []

            path = [vertices_list[i]]
            while i != j:
                i = next_vertex[i][j]
                path.append(vertices_list[i])
            return path

        # Calcular excentricidades, radio y diámetro
        eccentricities = {}
        for i, v in enumerate(vertices_list):
            max_dist = max(dist[i][j] for j in range(n) if dist[i][j] != INF)
            eccentricities[v] = max_dist if max_dist != INF else None

        valid_eccentricities = [e for e in eccentricities.values() if e is not None and e != INF]
        radius = min(valid_eccentricities) if valid_eccentricities else None
        diameter = max(valid_eccentricities) if valid_eccentricities else None

        return {
            "success": True,
            "vertices": vertices_list,
            "distance_matrix": dist,
            "next_matrix": next_vertex,
            "eccentricities": eccentricities,
            "radius": radius,
            "diameter": diameter,
            "reconstruct_path": reconstruct_path
        }

    # ==================== MEDIANA DEL GRAFO ====================

    def find_median(self) -> Dict:
        """
        Encuentra la mediana del grafo usando Floyd-Warshall
        La mediana es el vértice (o vértices) que minimiza la suma de distancias
        a todos los demás vértices (excluyendo la distancia a sí mismo)

        Returns:
            Dict con vértices medianos y suma mínima de distancias
        """
        # Usar Floyd-Warshall para obtener la tabla de distancias
        fw_result = self.floyd_warshall()

        if not fw_result["success"]:
            return {
                "success": False,
                "error": fw_result.get("error", "Error en Floyd-Warshall")
            }

        vertices_list = fw_result["vertices"]
        distance_matrix = fw_result["distance_matrix"]
        vertex_to_idx = {v: i for i, v in enumerate(vertices_list)}

        distance_sums = {}
        INF = float('inf')

        # Para cada vértice, sumar las distancias a todos los demás
        # (excluyendo la distancia a sí mismo, que es 0)
        for i, v in enumerate(vertices_list):
            total_distance = 0
            for j in range(len(vertices_list)):
                if i != j:  # No incluir la distancia a sí mismo
                    dist = distance_matrix[i][j]
                    if dist != INF:
                        total_distance += dist
                    else:
                        # Si no hay camino, el grafo no es conexo
                        return {
                            "success": False,
                            "error": "El grafo no es conexo"
                        }
            distance_sums[v] = total_distance

        # Encontrar mínimo
        min_sum = min(distance_sums.values()) if distance_sums else 0

        # Mediana: vértices con suma mínima
        median_vertices = [v for v, s in distance_sums.items() if s == min_sum]

        return {
            "success": True,
            "median_vertices": sorted(median_vertices),
            "min_distance_sum": min_sum,
            "distance_sums": distance_sums,
            "num_medians": len(median_vertices)
        }

    # ==================== TABLA DE ANÁLISIS ====================

    def get_analysis_table(self) -> Dict:
        """
        Genera tabla completa de análisis del grafo con:
        - Excentricidades
        - Radio y diámetro
        - Distancias desde cada vértice
        - Centro y centroide

        Returns:
            Dict con toda la información para la tabla interactiva
        """
        if not self.is_connected():
            return {
                "success": False,
                "error": "El grafo debe ser conexo para el análisis completo"
            }

        vertices_list = sorted(list(self.vertices))
        G = self._to_networkx()

        # Calcular matriz de distancias usando Floyd-Warshall
        floyd_result = self.floyd_warshall()
        if not floyd_result["success"]:
            return floyd_result

        # Calcular centro
        center_result = self.graph_center()

        # Calcular centroide
        centroid_result = self.graph_centroid()

        # Construir tabla de análisis por vértice
        vertex_analysis = {}
        for i, vertex in enumerate(vertices_list):
            distances = {}
            for j, other_vertex in enumerate(vertices_list):
                distances[other_vertex] = floyd_result["distance_matrix"][i][j]

            vertex_analysis[vertex] = {
                "eccentricity": floyd_result["eccentricities"][vertex],
                "distances": distances,
                "sum_distances": centroid_result["distance_sums"][vertex],
                "is_center": vertex in center_result["center_vertices"],
                "is_centroid": vertex in centroid_result["centroid_vertices"]
            }

        return {
            "success": True,
            "vertices": vertices_list,
            "vertex_analysis": vertex_analysis,
            "radius": floyd_result["radius"],
            "diameter": floyd_result["diameter"],
            "center_vertices": center_result["center_vertices"],
            "centroid_vertices": centroid_result["centroid_vertices"],
            "distance_matrix": floyd_result["distance_matrix"]
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
            },
            "is_directed": self.is_directed,
            "has_weights": self.has_weights
        }

    def to_json(self) -> str:
        """Exporta el grafo a JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: dict) -> WeightedGraph:
        """Crea un grafo desde un diccionario"""
        graph = cls(
            vertices=set(data["vertices"]),
            is_directed=data.get("is_directed", False),
            has_weights=data.get("has_weights", True)
        )
        for name, edge_data in data["edges"].items():
            graph.add_edge(name, edge_data["v1"], edge_data["v2"], edge_data["weight"])
        return graph

    @classmethod
    def from_json(cls, json_str: str) -> WeightedGraph:
        """Importa un grafo desde JSON"""
        data = json.loads(json_str)
        return cls.from_dict(data)
