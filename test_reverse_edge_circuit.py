# -*- coding: utf-8 -*-
"""
Script de prueba: crear un ciclo que usa una arista en direccion inversa
Para que esto suceda, necesitamos un grafo donde haya aristas que van
en ambas direcciones entre vertices
"""
import sys
sys.path.insert(0, 'models')

from graph_theory import GraphTheory

# Crear un grafo dirigido
graph = GraphTheory(is_directed=True)

# Agregar vertices
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')

# Crear un ciclo donde una arista va "al revés"
# A->B, B->C, C->A (ciclo normal)
# Pero tambien agregar A->C (para crear mas opciones de ciclos)
graph.add_edge('ab', 'A', 'B')  # A->B
graph.add_edge('bc', 'B', 'C')  # B->C
graph.add_edge('ca', 'C', 'A')  # C->A (completa ciclo ABC)
graph.add_edge('ac', 'A', 'C')  # A->C (crea camino alternativo)

print("=" * 70)
print("PRUEBA: MATRIZ DE INCIDENCIA Y CIRCUITOS COMPLEJOS")
print("=" * 70)

print("\nGrafo dirigido:")
print("  Aristas: A->B, B->C, C->A, A->C")

print("\n1. MATRIZ DE INCIDENCIA VERTICE-ARISTA")
print("   (1=sale, -1=entra, 0=no incidente)")
matrix, vertices, edges = graph.vertex_incidence_matrix()
print(f"\nVertices: {vertices}")
print(f"Aristas: {edges}\n")
print("Matriz:")
print(matrix)

print("\nExplicacion por vertices:")
print("  A: 1 en ab (sale a B), 1 en ac (sale a C), -1 en ca (entra desde C)")
print("  B: -1 en ab (entra de A), 1 en bc (sale a C)")
print("  C: -1 en bc (entra de B), -1 en ac (entra de A), 1 en ca (sale a A)")

print("\n" + "=" * 70)
print("2. CIRCUITOS ENCONTRADOS")
print("-" * 70)

circuits = graph.find_circuits()
print(f"\nCircuitos encontrados: {len(circuits)}\n")

for i, circuit in enumerate(circuits):
    print(f"Circuito {circuit['id']}:")
    print(f"  Vertices: {' -> '.join(circuit['vertices'])}")
    print(f"  Aristas: {circuit['edges']}")
    if 'edge_directions' in circuit:
        print(f"  Orientacion en el circuito:")
        for edge, direction in circuit['edge_directions'].items():
            status = "correcta (1)" if direction == 1 else "opuesta (-1)"
            print(f"    {edge}: {status}")
    print()

print("=" * 70)
print("CONCLUSIONES:")
print("=" * 70)
print("\n- La matriz de incidencia muestra:")
print("  * 1 cuando la arista SALE del vertice")
print("  * -1 cuando la arista ENTRA al vertice")
print("  * 0 cuando no hay incidencia")
print("\n- En los circuitos:")
print("  * 1 indica que la arista va en la direccion del ciclo")
print("  * -1 indicaria que va en la direccion inversa (si la hubiera)")
print("\n" + "=" * 70)
