# -*- coding: utf-8 -*-
"""
Script de prueba para verificar circuitos con aristas en direccion opuesta
"""
import sys
sys.path.insert(0, 'models')

from graph_theory import GraphTheory

# Crear un grafo dirigido con ciclo que requiere arista inversa
graph = GraphTheory(is_directed=True)

# Agregar vertices
graph.add_vertex('A')
graph.add_vertex('B')
graph.add_vertex('C')

# Agregar aristas: A->B, B->C, A->C (sin C->A, forzara usar C->A inversa)
graph.add_edge('a1', 'A', 'B')  # A->B
graph.add_edge('a2', 'B', 'C')  # B->C
graph.add_edge('a3', 'A', 'C')  # A->C

print("=" * 70)
print("PRUEBA: CIRCUITOS CON ARISTAS EN DIRECCION OPUESTA")
print("=" * 70)

print("\nGrafo dirigido: A -> B, B -> C, A -> C")
print("\nBuscando ciclos...")

circuits = graph.find_circuits()
print(f"\nCircuitos encontrados: {len(circuits)}\n")

for circuit in circuits:
    print(f"Circuito {circuit['id']}:")
    print(f"  Vertices: {circuit['vertices']}")
    print(f"  Aristas: {circuit['edges']}")
    if 'edge_directions' in circuit:
        print(f"  Direcciones:")
        for edge, direction in circuit['edge_directions'].items():
            dir_str = "correcta (1)" if direction == 1 else "opuesta (-1)"
            print(f"    {edge}: {direction} ({dir_str})")
    print()

# Ahora probar con un grafo que si tiene el ciclo completo
print("\n" + "=" * 70)
print("COMPARACION: CICLO COMPLETO")
print("=" * 70)

graph2 = GraphTheory(is_directed=True)
graph2.add_vertex('A')
graph2.add_vertex('B')
graph2.add_vertex('C')

# A->B->C->A (ciclo completo)
graph2.add_edge('e1', 'A', 'B')
graph2.add_edge('e2', 'B', 'C')
graph2.add_edge('e3', 'C', 'A')

print("\nGrafo dirigido: A -> B -> C -> A")
print("\nBuscando ciclos...")

circuits2 = graph2.find_circuits()
print(f"\nCircuitos encontrados: {len(circuits2)}\n")

for circuit in circuits2:
    print(f"Circuito {circuit['id']}:")
    print(f"  Vertices: {circuit['vertices']}")
    print(f"  Aristas: {circuit['edges']}")
    if 'edge_directions' in circuit:
        print(f"  Direcciones:")
        for edge, direction in circuit['edge_directions'].items():
            dir_str = "correcta (1)" if direction == 1 else "opuesta (-1)"
            print(f"    {edge}: {direction} ({dir_str})")
    print()

print("=" * 70)
print("PRUEBA COMPLETADA")
print("=" * 70)
