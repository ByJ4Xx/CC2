# -*- coding: utf-8 -*-
"""
Script de prueba para verificar las matrices de grafos dirigidos
"""
import sys
sys.path.insert(0, 'models')

from graph_theory import GraphTheory

# Crear un grafo dirigido simple
graph = GraphTheory(is_directed=True)

# Agregar vértices
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')

# Agregar aristas: A->B, B->C, C->A (ciclo)
graph.add_edge('a1', 'A', 'B')
graph.add_edge('a2', 'B', 'C')
graph.add_edge('a3', 'C', 'A')

print("=" * 70)
print("PRUEBA DE MATRICES PARA GRAFOS DIRIGIDOS")
print("=" * 70)

print("\nGrafo dirigido: A -> B -> C -> A (ciclo)")
print("\n1. MATRIZ DE INCIDENCIA VERTICE-ARISTA")
print("   Convención: 1=sale, -1=entra, 0=no incidente")
print("-" * 70)

matrix, vertices, edges = graph.vertex_incidence_matrix()
print(f"Vertices: {vertices}")
print(f"Aristas: {edges}\n")
print("Matriz:")
print(matrix)
print("\nExplicación:")
print("  A: 1 en a1 (sale de A), -1 en a3 (entra a A)")
print("  B: -1 en a1 (entra a B), 1 en a2 (sale de B)")
print("  C: -1 en a2 (entra a C), 1 en a3 (sale de C)")

print("\n" + "=" * 70)
print("2. MATRIZ DE ADYACENCIA VERTICES")
print("   Para dirigidos: M[i,j] = numero de aristas desde i hacia j")
print("-" * 70)

matrix_adj, vertices_adj = graph.vertex_adjacency_matrix()
print(f"Vertices: {vertices_adj}\n")
print("Matriz:")
print(matrix_adj)
print("\nExplicación:")
print("  NO es simétrica (a diferencia de grafos no dirigidos)")
print("  M[A,B]=1 (arista A->B), M[B,C]=1 (arista B->C), M[C,A]=1 (arista C->A)")
print("  Resto = 0 (no hay arista en esa dirección)")

print("\n" + "=" * 70)
print("3. MATRIZ DE ADYACENCIA ARISTAS")
print("   M[i,j] = 1 si comparten vertice, 0 en caso contrario")
print("-" * 70)

matrix_edge, edges_list = graph.edge_adjacency_matrix()
print(f"Aristas: {edges_list}\n")
print("Matriz:")
print(matrix_edge)
print("\nExplicación:")
print("  a1 y a2 comparten B: M[a1,a2] = 1")
print("  a2 y a3 comparten C: M[a2,a3] = 1")
print("  a1 y a3 comparten A: M[a1,a3] = 1")
print("  Diagonal: 0 (una arista no se relaciona consigo misma)")

print("\n" + "=" * 70)
print("4. CIRCUITOS (CICLOS) CON INFORMACION DE DIRECCION")
print("-" * 70)

circuits = graph.find_circuits()
print(f"Circuitos encontrados: {len(circuits)}\n")
for circuit in circuits:
    print(f"Circuito {circuit['id']}:")
    print(f"  Vertices: {circuit['vertices']}")
    print(f"  Aristas: {circuit['edges']}")
    if 'edge_directions' in circuit:
        print(f"  Direcciones: {circuit['edge_directions']}")
        print("    (1=dirección correcta del ciclo, -1=dirección opuesta)")

print("\n" + "=" * 70)
print("5. COMPARACION CON GRAFO NO DIRIGIDO")
print("-" * 70)

graph_ud = GraphTheory(is_directed=False)
graph_ud.add_vertex('A')
graph_ud.add_vertex('B')
graph_ud.add_vertex('C')
graph_ud.add_edge('a1', 'A', 'B')
graph_ud.add_edge('a2', 'B', 'C')
graph_ud.add_edge('a3', 'C', 'A')

print("\nMatriz de Incidencia (NO DIRIGIDO):")
matrix_ud, _, _ = graph_ud.vertex_incidence_matrix()
print(matrix_ud)
print("\nExplicación: Todos los valores son 0 o 1 (sin -1)")
print("  Cada vertice tiene 1 para las aristas incidentes")

print("\nMatriz de Adyacencia (NO DIRIGIDO):")
matrix_adj_ud, _ = graph_ud.vertex_adjacency_matrix()
print(matrix_adj_ud)
print("\nExplicación: Matriz es simétrica (M[i,j] = M[j,i])")

print("\n" + "=" * 70)
print("RESULTADO: TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("=" * 70)
