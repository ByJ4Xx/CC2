# Plan de Implementación: Árboles de Expansión Mejorado

## Objetivo
Implementar un sistema completo de análisis de árboles de expansión que incluya:
- Edición de grafos (eliminar/modificar vértices y aristas)
- Carga de grafos desde la sección de matrices
- Análisis de árbol mínimo y complemento con 3 visualizaciones
- Cálculo del centro del grafo
- Algoritmo de Floyd con tabla interactiva

---

## Estructura

### 1. Mejoras a `models/spanning_trees.py`

#### 1.1 Agregar métodos a `WeightedGraph`:

**Métodos para edición:**
- `remove_vertex(vertex: str)` - Elimina vértice y sus aristas
- `remove_edge(edge_name: str)` - Elimina una arista por nombre
- `edit_edge(edge_name: str, new_weight: float)` - Modifica el peso de una arista
- `get_graph_info()` - Retorna información completa del grafo

**Métodos para complemento:**
- `get_complement_graph()` - Retorna un nuevo WeightedGraph con el complemento
- `minimum_spanning_tree_with_complement()` - Calcula MST y retorna (mst_edges, complement_edges)

**Métodos para centro mejorado:**
- `find_tree_center()` - Encuentra el centro del árbol eliminando hojas recursivamente
- `find_bicentro()` - Detecta si hay bicentro

**Soporte para grafos dirigidos y sin pesos:**
- Agregar campos: `is_directed`, `has_weights`
- Ajustar Floyd-Warshall para grafos no ponderados
- Mantener compatibilidad con grafos ponderados

---

### 2. Mejoras a `views/spanning_trees_view.py`

#### 2.1 Panel de controles actualizado:
- **Sección 0.5: Editor de Grafo**
  - Botón "Eliminar Vértice" (con dropdown de vértices)
  - Botón "Eliminar Arista" (con dropdown de aristas)
  - Botón "Modificar Arista" (popup con selector y nuevo peso)
  - Botón "Ver Información del Grafo"
  - Botón "Cargar desde Matrices" (diálogo para seleccionar grafo guardado)

#### 2.2 Visualización mejorada:
- **Tab en notebook para 3 grafos:**
  - Tab "Original" - Grafo original
  - Tab "MST" - Árbol mínimo
  - Tab "Complemento" - Grafo complemento
  - Tab "Ramas/Cuerdas" - Grafo original con ramas y cuerdas resaltadas

#### 2.3 Mejora de la tabla de análisis:
- Agregar columnas/información:
  - `Radio` - Excentricidad mínima (destacado)
  - `Diámetro` - Excentricidad máxima (destacado)
  - `Centro` - Vértices con excentricidad = radio (color especial)
  - `Mediana` - Vértices con suma mínima (color especial)
  - Mostrar subgrafo de la mediana

#### 2.4 Métodos nuevos en vista:
- `draw_multiple_graphs(original, mst, complement)` - Dibuja 3 grafos lado a lado
- `draw_graph_with_tree_structure(mst_edges, branches, chords)` - Dibuja con colores
- `show_graph_info()` - Muestra información en ventana
- `show_median_subgraph()` - Visualiza el subgrafo de la mediana
- `load_graph_from_matrices()` - Diálogo para cargar grafo externo

---

### 3. Integración con `models/graph_operations.py`

**Nueva clase o método:**
- `GraphData` → Convertir a `WeightedGraph`
- Permitir que el usuario cargue un grafo de matrix operations
- Guardar grafos para reutilizar entre secciones

---

## Flujo de Usuario

### Flujo 1: Crear grafo y analizar
1. Usuario agrega vértices y aristas (ponderadas, dirigidas o no)
2. Opcionalmente edita/elimina elementos
3. Calcula MST → ve 3 grafos (original, MST, complemento)
4. Identifica ramas y cuerdas → resaltadas en color
5. Calcula centro → resaltado en grafo
6. Ejecuta Floyd → ve tabla con análisis completo

### Flujo 2: Cargar desde matrices
1. Usuario crea grafo en sección "Operaciones de Grafos"
2. Guarda el grafo
3. En "Árboles de Expansión", clic en "Cargar desde Matrices"
4. Selecciona grafo guardado → Se carga automáticamente
5. Continúa con análisis

---

## Detalles Técnicos

### Cambios en `WeightedGraph`:

```python
# Nuevos campos
is_directed: bool = False
has_weights: bool = True

# Nuevos métodos
def remove_vertex(vertex: str) -> bool
def remove_edge(edge_name: str) -> bool
def edit_edge(edge_name: str, new_weight: float) -> bool
def get_graph_info() -> Dict
def get_complement_graph() -> 'WeightedGraph'
def find_tree_center() -> Dict
def get_subgraph(vertices: Set[str]) -> 'WeightedGraph'
```

### Cambios en `SpanningTreesContent`:

```python
# Nueva interfaz
self.tabs_graphs = {
    "original": Canvas,
    "mst": Canvas,
    "complement": Canvas,
    "branches_chords": Canvas
}

# Métodos nuevos
def delete_vertex()
def delete_edge()
def edit_edge()
def load_from_matrices()
def show_three_graphs()
def draw_median_subgraph()
```

---

## Prioridad de implementación

1. **Fase 1**: Métodos básicos en `WeightedGraph` (eliminar, editar, información)
2. **Fase 2**: Interfaz de edición en vista
3. **Fase 3**: Múltiples grafos (original, MST, complemento)
4. **Fase 4**: Mejora de tabla Floyd con información de radio/diámetro/mediana
5. **Fase 5**: Carga desde matrices
6. **Fase 6**: Visualización de mediana y optimizaciones

---

## Notas importantes

- Mantener compatibilidad con grafos ponderados y no dirigidos
- Los grafos de matrices pueden tener diferentes características (dirigidos, sin pesos)
- Floyd-Warshall debe adaptarse para grafos no ponderados
- Centro: algoritmo de eliminación de hojas (incidencia 1)
- Mediana: suma mínima de distancias a todos los demás vértices
