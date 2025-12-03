# Manual Técnico - Algoritmos · Búsquedas y Grafos

**Versión:** 1.0
**Última actualización:** Diciembre 2025
**Lenguaje:** Python 3.13+

---

## Tabla de Contenidos

1. [Descripción General](#descripción-general)
2. [Requisitos y Dependencias](#requisitos-y-dependencias)
3. [Instalación](#instalación)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Arquitectura](#arquitectura)
6. [Guía de Uso](#guía-de-uso)
7. [Componentes Principales](#componentes-principales)
8. [Algoritmos Implementados](#algoritmos-implementados)
9. [Modelos de Datos](#modelos-de-datos)
10. [Sistema de Vistas](#sistema-de-vistas)
11. [Patrones de Diseño](#patrones-de-diseño)
12. [API de Modelos](#api-de-modelos)
13. [Persistencia de Datos](#persistencia-de-datos)
14. [Troubleshooting](#troubleshooting)
15. [Contribuciones](#contribuciones)

---

## Descripción General

**CC2** es una aplicación educativa interactiva que implementa algoritmos fundamentales de ciencias de la computación, con especial énfasis en:

- **Búsquedas Internas:** Lineal, Binaria, Hash, Árboles Digitales, Residuos, Huffman
- **Búsquedas Externas:** Secuencial, Binaria, Hash, Dinámicas, Índices
- **Teoría de Grafos:** Operaciones algebraicas, matrices, circuitos, árboles de expansión
- **Algoritmos Avanzados:** Kruskal, Prim, Floyd-Warshall, análisis de centros y medianas

La aplicación proporciona:
- **Interfaz gráfica interactiva** (CustomTkinter)
- **Visualización de estructuras** (Matplotlib + NetworkX)
- **Ejecución paso a paso** de algoritmos
- **Persistencia de datos** (JSON)
- **Validación robusta** de entrada

### Objetivos Educativos

✓ Comprensión visual de cómo funcionan los algoritmos
✓ Análisis comparativo entre diferentes estrategias
✓ Manipulación interactiva de estructuras de datos
✓ Aplicación de teoría de grafos en casos reales

---

## Requisitos y Dependencias

### Versión de Python

```
Python ≥ 3.13
```

### Dependencias Externas

| Librería | Versión | Descripción |
|----------|---------|-------------|
| **customtkinter** | ≥5.2.2 | Framework GUI moderno con soporte para temas |
| **networkx** | ≥3.0 | Análisis, algoritmos y visualización de grafos |
| **matplotlib** | ≥3.0 | Visualización de gráficos y estructuras |

### Librerías Estándar Utilizadas

- `tkinter` - GUI base (incluido en Python)
- `json` - Serialización y persistencia
- `dataclasses` - Estructuras de datos
- `typing` - Type hints
- `math` - Operaciones matemáticas
- `random` - Generación de números aleatorios
- `bisect` - Búsqueda e inserción binaria ordenada
- `heapq` - Colas de prioridad (para Huffman)
- `itertools` - Combinaciones y permutaciones

### Requisitos del Sistema

- **OS:** Windows, macOS, Linux
- **RAM:** Mínimo 4GB (recomendado 8GB)
- **Disco:** 150MB (incluyendo dependencias)
- **Display:** 1920x1080 recomendado (soporta escalado)

---

## Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/ByJ4Xx/CC2.git
cd CC2
```

### 2. Crear Entorno Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
# Usando pip
pip install customtkinter networkx matplotlib

# O usando requirements.txt si existe
pip install -r requirements.txt
```

### 4. Ejecutar la Aplicación

```bash
# Desde el directorio raíz del proyecto
python main.py
```

**Nota:** La primera ejecución puede tomar más tiempo debido a la compilación de módulos.

---

## Estructura del Proyecto

```
CC2/
├── main.py                          # Punto de entrada
├── app.py                           # Aplicación principal (GUI)
├── pyproject.toml                   # Configuración del proyecto
├── PLAN.md                          # Plan de desarrollo
├── README.md                        # Documentación general
├── MANUAL_TECNICO.md               # Este archivo
│
├── models/                          # Lógica de negocios (algoritmos)
│   ├── __init__.py
│   ├── linear.py                   # Búsqueda lineal (estructura interna)
│   ├── binary.py                   # Búsqueda binaria (estructura interna)
│   ├── hash.py                     # Funciones hash y resolución de colisiones
│   ├── digital.py                  # Árbol digital (búsqueda por bits)
│   ├── residue.py                  # Árbol de residuos
│   ├── residue_multiple.py         # Árbol de residuos múltiples
│   ├── huffman.py                  # Árbol de Huffman (compresión)
│   ├── external.py                 # Base para búsquedas externas
│   ├── external_hash.py            # Hash externo
│   ├── dynamic_total.py            # Arrays dinámicos con expansión
│   ├── graph_theory.py             # Matrices y circuitos de grafos
│   ├── graph_operations.py         # Operaciones algebraicas de grafos
│   └── spanning_trees.py           # Árboles de expansión (MST)
│
├── ui/                              # Componentes de interfaz reutilizables
│   ├── __init__.py
│   ├── sidebar.py                  # Barra lateral colapsable
│   └── header.py                   # Barra de título y selector de tema
│
├── views/                           # Vistas específicas de cada funcionalidad
│   ├── __init__.py
│   ├── base.py                     # Clase base para todas las vistas
│   ├── welcome.py                  # Página de bienvenida
│   │
│   ├── lineal.py                   # Vista: Búsqueda Lineal
│   ├── binaria.py                  # Vista: Búsqueda Binaria
│   ├── hash_view.py                # Vista: Funciones Hash
│   ├── digital.py                  # Vista: Árbol Digital
│   ├── residue.py                  # Vista: Árbol de Residuos
│   ├── residue_multiple.py         # Vista: Árbol de Residuos Múltiples
│   ├── huffman.py                  # Vista: Árbol de Huffman
│   │
│   ├── external_base.py            # Clase base para vistas externas
│   ├── external_sequential.py      # Vista: Búsqueda Secuencial Externa
│   ├── external_binary.py          # Vista: Búsqueda Binaria Externa
│   ├── external_dynamic.py         # Vista: Estructuras Dinámicas
│   ├── external_hash.py            # Vista: Hash Externo
│   ├── external_index_new.py       # Vista: Índices Externos
│   │
│   ├── graph_operations_view.py    # Vista: Operaciones de Grafos
│   ├── graph_theory_view.py        # Vista: Matrices y Circuitos
│   └── spanning_trees_view.py      # Vista: Árboles de Expansión
│
├── tests/                           # Tests unitarios
│   ├── test_directed_matrices.py
│   ├── test_circuits_with_reverse.py
│   └── test_reverse_edge_circuit.py
│
└── .git/                            # Control de versiones

```

---

## Arquitectura

### Patrón MVC

La aplicación sigue el patrón **Model-View-Controller**:

```
┌─────────────────────┐
│    Models/          │
│    (Lógica pura)    │
└──────────┬──────────┘
           │
           │ Datos
           ↓
┌─────────────────────┐      ┌──────────────────┐
│    Views/           │←────→│   UI Components  │
│    (Presentación)   │      │   (Sidebar, etc) │
└─────────────────────┘      └──────────────────┘
           ↑
           │ Eventos
           │
┌─────────────────────┐
│    App (Controller) │
└─────────────────────┘
```

### Layout de Interfaz

```
┌──────────────────────────────────────────────────┐
│              Header (HeaderBar)                  │
│    Título dinámico + Selector de Tema            │
├──────────┬───────────────────────────────────────┤
│          │                                       │
│ Sidebar  │     Contenido Dinámico               │
│          │     (Diferentes vistas)               │
│          │                                       │
│  (260px) │     (Flexible)                        │
│          │                                       │
└──────────┴───────────────────────────────────────┘
```

### Flujo de Control

```
1. Usuario abre aplicación
   ↓
2. main.py → app.py → App.__init__()
   ↓
3. GUI se carga (Sidebar + Header + Welcome)
   ↓
4. Usuario navega (click en Sidebar)
   ↓
5. Sidebar.on_select() → App.handle_select()
   ↓
6. App construye clave: "sección:item"
   ↓
7. App.show_content(clave) carga vista correspondiente
   ↓
8. Vista interactúa con modelo (insert, find, etc)
   ↓
9. Vista actualiza UI con resultados
```

---

## Guía de Uso

### Inicio Rápido

```python
# 1. Ejecutar aplicación
python main.py

# 2. Navegar usando el Sidebar (panel izquierdo)
# Búsquedas → Internas → Búsqueda Lineal

# 3. Configurar estructura
# - Tamaño: 10^3
# - Longitud: 4 dígitos
# - Clic en "Crear"

# 4. Insertar datos
# - Ingresar clave: 1234
# - Clic en "Insertar"

# 5. Buscar
# - Ingresar clave: 1234
# - Clic en "Buscar"

# 6. Ver resultados en visualización
```

### Búsqueda Lineal (Ejemplo Completo)

```
1. Navegar a: Búsquedas → Internas → Lineal
2. Seleccionar: Capacidad = 10^3, Longitud = 4
3. Clic: "Crear estructura"
   ✓ LinearStructure(1000, 4) instanciada

4. Panel "Operaciones":
   - Ingresar: 5678
   - Clic: "Insertar"
   ✓ Elemento añadido a posición ordenada

5. Panel "Búsqueda paso a paso":
   - Ingresar: 5678
   - Clic: "Iniciar búsqueda"
   - Ver pasos de búsqueda lineal

6. Generar datos (opcional):
   - Ingresar: 50 (cantidad)
   - Clic: "Generar aleatorios"
   ✓ 50 claves insertadas automáticamente

7. Persistencia:
   - Clic: "Guardar estructura"
   - Seleccionar ubicación y nombre
   ✓ Guardado en JSON

8. Recuperar:
   - Clic: "Cargar estructura"
   - Seleccionar archivo JSON
   ✓ Estructura restaurada
```

### Comparar Dos Algoritmos

```
Scenario: Comparar búsqueda lineal vs. binaria

1. Abrir dos navegadores o pestañas
2. En uno: Lineal (con 1000 elementos)
3. En otro: Binaria (con 1000 elementos)
4. Insertar mismos datos en ambas
5. Buscar mismo elemento
6. Comparar tiempo y pasos mostrados
7. Observar diferencia: O(n) vs. O(log n)
```

### Análisis de Grafos

```
1. Navegar a: Grafos → Árboles a partir de Grafos
2. Crear vértices: A, B, C, D
3. Crear aristas con pesos:
   - e1: A-B (peso: 1)
   - e2: B-C (peso: 2)
   - e3: C-D (peso: 3)
   - e4: D-A (peso: 4)
   - e5: A-C (peso: 2)

4. Clic: "Generar Árbol Mínimo (MST)"
   ✓ Se calcula MST usando Kruskal
   ✓ Se visualiza árbol en panel "Grafo"

5. Clic: "Ver 3 Grafos"
   ✓ Se muestran:
     - Original (todas las aristas)
     - MST (árbol mínimo)
     - Complemento (aristas faltantes)

6. Clic: "Identificar Ramas y Cuerdas"
   ✓ Ramas: aristas del MST (n-1)
   ✓ Cuerdas: aristas del complemento

7. Clic: "Ejecutar Floyd-Warshall"
   ✓ Se calcula matriz de distancias
   ✓ Se muestra en tabla
   ✓ Se muestran excentricidades

8. Clic: "Hallar Mediana"
   ✓ Se resalta vértice(s) de mediana
   ✓ Se muestra suma de distancias
```

---

## Componentes Principales

### 1. App (app.py)

**Rol:** Controlador principal y contenedor de GUI

```python
class App(ctk.CTk):
    def __init__(self):
        # Inicializa ventana
        # Crea sidebar, header y contenedor
        # Carga vista inicial (welcome)

    def handle_select(self, section, item):
        # Maneja navegación
        # Construye clave: "section:item"
        # Carga vista correspondiente

    def show_content(self, key):
        # Oculta vista anterior
        # Instancia nueva vista
        # Actualiza header

    def on_closing(self):
        # Limpia recursos
        # Cierra figuras matplotlib
        # Cierra aplicación
```

**Atributos principales:**
- `contents: Dict` - Mapeo de rutas a vistas
- `current_content: BaseContent` - Vista actual
- `sidebar: CollapsibleSidebar` - Panel de navegación
- `header: HeaderBar` - Barra de título

### 2. CollapsibleSidebar (ui/sidebar.py)

**Rol:** Navegación jerárquica colapsable

```python
class CollapsibleSidebar(ctk.CTkFrame):
    def __init__(self, parent, on_select_callback):
        # Crea botones de sección
        # Crea submenús expandibles
        # Configura animación de colapso

    def toggle_collapsed(self):
        # Alterna entre expandido/colapsado
        # Anima cambio de ancho (56px ↔ 260px)

    def on_select(self, section, item):
        # Dispara callback con selección
        # Resalta botón seleccionado
```

**Estructura jerárquica:**
```
├── Búsquedas
│   ├── Internas
│   │   ├── Lineal
│   │   ├── Binaria
│   │   ├── Hash
│   │   ├── Digital
│   │   ├── Residuo
│   │   ├── Residuo Múltiple
│   │   └── Huffman
│   └── Externas
│       ├── Secuencial
│       ├── Binaria
│       ├── Dinámicas
│       ├── Índices
│       └── Hash
│
└── Grafos
    ├── Operaciones
    ├── Matrices
    └── Árboles
```

### 3. HeaderBar (ui/header.py)

**Rol:** Barra de título y selector de tema

```python
class HeaderBar(ctk.CTkFrame):
    def __init__(self, parent):
        # Crea label de título
        # Crea dropdown de tema
        # Configura tema inicial

    def update_title(self, new_title):
        # Actualiza título dinámicamente

    def set_theme(self, theme):
        # Cambia tema global
        # Opciones: "System", "Light", "Dark"
```

### 4. BaseContent (views/base.py)

**Rol:** Clase base para todas las vistas

```python
class BaseContent(ctk.CTkFrame):
    title = "Título por defecto"  # Clase variable

    def __init__(self, parent):
        super().__init__(parent)
        # Frame contenedor con padding estándar

    # Métodos para sobrescribir:
    # - setup_ui(): Crea interfaz
    # - on_focus(): Se ejecuta al mostrar vista
    # - cleanup(): Limpia antes de cambiar vista
```

---

## Algoritmos Implementados

### Búsquedas Internas

#### 1. Búsqueda Lineal (O(n))

```python
# Implementación conceptual
def find(self, key):
    for i, value in enumerate(self.items):
        if value == key:
            return i
    return -1
```

- **Complejidad:** O(n) en peor caso
- **Ventajas:** Simple, sin requisitos de orden
- **Desventajas:** Lento para datos grandes
- **Mejor caso:** O(1) cuando está al inicio
- **Peor caso:** O(n) cuando está al final o no existe

#### 2. Búsqueda Binaria (O(log n))

```python
# Implementación conceptual
def find(self, key):
    left, right = 0, len(self.items) - 1
    while left <= right:
        mid = (left + right) // 2
        if self.items[mid] == key:
            return mid
        elif self.items[mid] < key:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

- **Complejidad:** O(log n) garantizado
- **Requisitos:** Datos deben estar ordenados
- **Ventajas:** Muy rápida incluso con millones de elementos
- **Desventajas:** Requiere mantener orden en inserciones

#### 3. Funciones Hash

**Cuadrado (Square):**
```
h(x) = tomar dígitos centrales de x²
Ejemplo: x = 123
  x² = 15129
  h(x) = 51 (dígitos centrales)
```

**Modular:**
```
h(x) = x mod m
Ejemplo: x = 123, m = 100
  h(x) = 23
```

**Plegamiento (Folding):**
```
h(x) = suma de partes de x
Ejemplo: x = 12345, partes = [12, 34, 5]
  h(x) = 12 + 34 + 5 = 51
```

**Truncamiento (Truncation):**
```
h(x) = seleccionar dígitos específicos
Ejemplo: x = 123456, posiciones = [1, 3]
  h(x) = 24 (dígitos en posiciones 1 y 3)
```

**Resolución de Colisiones:**

| Método | Fórmula | Descripción |
|--------|---------|-------------|
| Secuencial | h(x,i) = (h + i) mod m | Prueba h, h+1, h+2, ... |
| Doble | h(x,i) = (h + 2i) mod m | Prueba h, h+2, h+4, ... |
| Cuadrado | h(x,i) = (h + i²) mod m | Prueba h, h+1, h+4, h+9, ... |
| Anidados | Múltiples buckets | Cada celda contiene lista |
| Encadenamiento | Listas ligadas | Cada colisión crea nodo en lista |

#### 4. Árbol Digital (Digital Tree)

- Búsqueda por código binario de 5 bits
- Cada letra A-Z tiene código binario único
- Navega el árbol según bits
- Tiempo: O(5) = O(1) para letras

#### 5. Árbol de Residuos (Residue Tree)

- Manejo de colisiones con nodos auxiliares
- Cuando hay colisión, crea nodo auxiliar
- Reconstruye árbol con menos de 5 niveles

#### 6. Árbol de Huffman (Huffman Tree)

```python
# Construcción conceptual
def build_huffman_tree(text):
    # 1. Contar frecuencias
    freq = Counter(text)

    # 2. Crear heap de nodos
    heap = [HuffNode(char, count) for char, count in freq.items()]
    heapify(heap)

    # 3. Construir árbol
    while len(heap) > 1:
        left = heappop(heap)
        right = heappop(heap)
        parent = HuffNode(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        heappush(heap, parent)

    return heap[0]  # Raíz del árbol
```

- **Compresión sin pérdida**
- **Códigos de longitud variable:**
  - Caracteres frecuentes: códigos cortos
  - Caracteres raros: códigos largos
- **Eficiencia:** Comprime típicamente 30-40% de texto

### Búsquedas Externas

#### 1. Búsqueda Secuencial Externa

```
Datos: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Bloques (tamaño 3):
  Bloque 0: [1, 2, 3]
  Bloque 1: [4, 5, 6]
  Bloque 2: [7, 8, 9]
  Bloque 3: [10, -, -]

Búsqueda de 7:
  1. Leer Bloque 0: 1, 2, 3 (no está)
  2. Leer Bloque 1: 4, 5, 6 (no está)
  3. Leer Bloque 2: 7, 8, 9 (¡ENCONTRADO!)

Complejidad: O(ceil(n/b)) lecturas de bloque
```

#### 2. Búsqueda Binaria Externa

```
Aplica búsqueda binaria a bloques, luego lineal dentro
Complejidad: O(log(n/b)) lecturas de bloque
```

#### 3. Arrays Dinámicos

```
DO (Densidad de Ocupación) = (elementos / capacidad) * 100

Expansión automática cuando DO > 65%:
  1. Calcular nueva capacidad = actual + sqrt(actual)
  2. Copiar elementos a nueva estructura
  3. Reorganizar en bloques

Ejemplo:
  Capacidad: 100, Elementos: 67 (DO = 67%)
  Expansión: Nueva capacidad = 100 + 10 = 110
```

### Teoría de Grafos

#### 1. Matriz de Incidencia (Vértices × Aristas)

**No dirigido:**
```
    e1  e2  e3
A [  1   0   1 ]
B [  1   1   0 ]
C [  0   1   1 ]

1 = vértice incidente a arista
0 = no incidente
```

**Dirigido (convención: 1=sale, -1=entra):**
```
    e1  e2  e3
A [ -1   0   1 ]  (sale por e3, entra por e1)
B [  1  -1   0 ]  (entra por e1, sale por e2)
C [  0   1  -1 ]  (sale por e2, entra por e3)
```

#### 2. Matriz de Adyacencia (Vértices × Vértices)

```
  A  B  C
A [0  1  1]
B [1  0  1]
C [1  1  0]

1 = existe arista
0 = no existe arista

Dirigido:
  A  B  C
A [0  1  0]  (A→B existe, A→C no)
B [0  0  1]  (B→C existe)
C [1  0  0]  (C→A existe)
```

#### 3. Circuitos Fundamentales

```
Para cada arista no en MST:
  1. Agregar arista al MST
  2. Se forma un ciclo
  3. Registrar ciclo como circuito fundamental

Número de circuitos = m - (n-1)
donde m = aristas, n = vértices
```

#### 4. Conjuntos de Corte Fundamentales

```
Para cada arista en MST:
  1. Eliminar arista del MST
  2. Se separan dos componentes
  3. Encontrar mínimo número de aristas para reconectar
  4. Ese conjunto es el corte fundamental
```

### Algoritmos de Árboles de Expansión

#### 1. Algoritmo de Kruskal (O(e log e))

```python
def kruskal(graph):
    edges = sorted(graph.edges, key=lambda x: x.weight)
    uf = UnionFind(graph.vertices)
    mst = []

    for edge in edges:
        if uf.find(edge.u) != uf.find(edge.v):
            mst.append(edge)
            uf.union(edge.u, edge.v)
            if len(mst) == len(graph.vertices) - 1:
                break

    return mst
```

- **Greedy:** Selecciona arista mínima que no crea ciclo
- **Complejidad:** O(e log e) por ordenamiento
- **Mejor para:** Grafos dispersos

#### 2. Algoritmo de Prim (O(v²) o O(e log v))

```python
def prim(graph, start):
    visited = set([start])
    edges = [e for e in graph.edges if e.u == start]
    mst = []

    while len(visited) < len(graph.vertices):
        # Seleccionar arista mínima
        edge = min(edges, key=lambda x: x.weight)
        mst.append(edge)
        visited.add(edge.v)

        # Agregar nuevas aristas
        for e in graph.edges:
            if e.u in visited and e.v not in visited:
                edges.append(e)

        edges.remove(edge)

    return mst
```

- **Greedy:** Expande desde vértice inicial
- **Complejidad:** O(v²) versión simple
- **Mejor para:** Grafos densos

#### 3. Floyd-Warshall (O(v³))

```python
def floyd_warshall(graph):
    dist = inicializar_distancias(graph)

    for k in range(len(graph.vertices)):
        for i in range(len(graph.vertices)):
            for j in range(len(graph.vertices)):
                dist[i][j] = min(
                    dist[i][j],
                    dist[i][k] + dist[k][j]
                )

    return dist
```

- **Calcula:** Distancias entre TODOS los pares
- **Complejidad:** O(v³) garantizado
- **Produce:**
  - Matriz de distancias mínimas
  - Excentricidades (max distancia desde vértice)
  - Radio (min excentricidad)
  - Diámetro (max excentricidad)

#### 4. Centro del Árbol

```python
# Método: Eliminación recursiva de hojas
def find_center(tree):
    while len(tree.vertices) > 2:
        # Encontrar hojas (incidencia = 1)
        leaves = [v for v in tree.vertices
                  if degree[v] == 1]

        # Eliminar todas las hojas
        for leaf in leaves:
            tree.remove_vertex(leaf)

    return tree.vertices  # Vértices restantes
```

- **Centro:** Vértice(s) con excentricidad mínima
- **Puede haber 1 o 2 centros (bicentro)**
- **Aplicación:** Ubicación óptima de recursos

#### 5. Mediana del Grafo

```python
def find_median(graph):
    distances = floyd_warshall(graph)
    min_sum = float('inf')
    medians = []

    for i, vertex in enumerate(graph.vertices):
        distance_sum = sum(distances[i])
        if distance_sum < min_sum:
            min_sum = distance_sum
            medians = [vertex]
        elif distance_sum == min_sum:
            medians.append(vertex)

    return medians, min_sum
```

- **Mediana:** Vértice(s) que minimizan suma de distancias
- **Aplicación:** Ubicación óptima minimizando distancia total
- **Diferencia:** Centro vs Mediana
  - Centro: minimiza distancia máxima
  - Mediana: minimiza distancia total

#### 6. Distancia entre Árboles de Expansión

```python
def tree_distance(tree1, tree2):
    # Fórmula: (|Unión| - |Intersección|) / 2
    union = tree1.union(tree2)
    intersection = tree1.intersection(tree2)

    distance = (len(union) - len(intersection)) / 2

    return distance
```

- **Mide:** Cuántas aristas difieren entre dos árboles
- **Rango:** 0 (idénticos) hasta (n-1) (totalmente diferentes)
- **Aplicación:** Comparación de distintos MST

---

## Modelos de Datos

### Búsquedas Internas

#### LinearStructure / BinaryStructure

```python
@dataclass
class LinearStructure:
    capacity: int  # Potencia de 10 (100, 1000, 10000)
    key_length: int  # 1-9 dígitos
    items: List[int] = field(default_factory=list)

    def insert(self, value: int) -> int:
        """Inserta elemento manteniendo orden"""
        if len(self.items) >= self.capacity:
            raise ValueError("Estructura llena")

        # Usar bisect para mantener orden
        bisect.insort(self.items, value)
        return len(self.items) - 1

    def find(self, value: int) -> int:
        """Búsqueda (lineal en LinearStructure, binaria en BinaryStructure)"""
        try:
            return self.items.index(value)
        except ValueError:
            return -1

    def to_json(self) -> str:
        """Serializar a JSON"""
        return json.dumps({
            'tipo': 'lineal',
            'capacidad': self.capacity,
            'longitud_clave': self.key_length,
            'datos': self.items
        })

    @classmethod
    def from_json(cls, json_str: str):
        """Deserializar desde JSON"""
        data = json.loads(json_str)
        obj = cls(data['capacidad'], data['longitud_clave'])
        obj.items = data['datos']
        return obj
```

#### HashStructure

```python
@dataclass
class HashStructure:
    capacity: int
    key_length: int
    hash_func: str  # 'cuadrado', 'modular', 'plegamiento', 'truncamiento'
    collision: str  # 'secuencial', 'doble', 'cuadrado', 'anidados', 'encadenamiento'
    table: List[Any] = field(default_factory=list)
    trunc_positions: Optional[List[int]] = None
    folding_op: Optional[str] = None

    def insert(self, value: int) -> Tuple[int, Optional[int], int]:
        """
        Inserta con resolución de colisiones
        Retorna: (posición_final, posición_colisión, intentos)
        """
        if len(self.table) == 0:
            self.table = [None] * self.capacity

        h = self._hash_function(value)
        collision_pos = None
        attempts = 0

        for i in range(self.capacity):
            pos = self._collision_strategy(h, value, i)
            attempts += 1

            if self.table[pos] is None or self.table[pos] == "DELETED":
                self.table[pos] = value
                return (pos, collision_pos, attempts)

            if collision_pos is None and self.table[pos] != value:
                collision_pos = pos

        raise ValueError("Tabla hash llena")
```

### Grafos

#### WeightedGraph

```python
class WeightedGraph:
    def __init__(self,
                 vertices: Optional[Set[str]] = None,
                 is_directed: bool = False,
                 has_weights: bool = True):
        self.vertices: Set[str] = vertices or set()
        self.edges: Dict[str, Tuple[str, str, float]] = {}
        self.is_directed = is_directed
        self.has_weights = has_weights

    def add_vertex(self, vertex: str) -> bool:
        """Agrega vértice"""
        if vertex in self.vertices:
            return False
        self.vertices.add(vertex)
        return True

    def add_edge(self,
                 edge_name: str,
                 v1: str,
                 v2: str,
                 weight: float = 1.0) -> bool:
        """Agrega arista"""
        if edge_name in self.edges:
            return False
        if v1 not in self.vertices or v2 not in self.vertices:
            return False

        self.edges[edge_name] = (v1, v2, weight)
        return True

    def minimum_spanning_tree(self, algorithm: str = "kruskal") -> Dict:
        """
        Calcula MST
        Retorna: {'success': bool, 'edge_names': List, 'total_weight': float}
        """
        # Implementación Kruskal o Prim
        pass

    def floyd_warshall(self) -> Dict:
        """
        Calcula distancias entre todos los pares
        Retorna: matriz de distancias, excentricidades, radio, diámetro
        """
        pass

    def is_tree(self, edge_names: Set[str]) -> bool:
        """
        Verifica si un conjunto de aristas forma árbol válido
        - n-1 aristas (donde n = vértices)
        - Conexo
        - Sin ciclos
        """
        pass

    def tree_distance(self, tree1: Set[str], tree2: Set[str]) -> Dict:
        """
        Distancia = (|Unión| - |Intersección|) / 2
        """
        pass
```

---

## Sistema de Vistas

### Mapeo de Vistas

```python
contents = {
    # Welcome
    "welcome": WelcomeContent,

    # Búsquedas Internas
    "internas:lineal": LinealContent,
    "internas:binaria": BinariaContent,
    "internas:hash": HashContent,
    "internas:digital": DigitalContent,
    "internas:residuo": ResidueContent,
    "internas:residuo_multiple": ResidueMultipleContent,
    "internas:huffman": HuffmanContent,

    # Búsquedas Externas
    "externas:secuencial": ExternalSequentialContent,
    "externas:binaria": ExternalBinaryContent,
    "externas:dinamicas": ExternalDynamicContent,
    "externas:indices": ExternalIndexNewView,
    "externas:hash": ExternalHashView,

    # Grafos
    "grafos:operaciones": GraphOperationsContent,
    "grafos:teoria": GraphTheoryContent,
    "grafos:arboles": SpanningTreesContent,
}
```

### Estructura Común de Vistas Internas

```
┌─ Configuración
│  ├─ Tamaño (potencia de 10)
│  ├─ Longitud de clave
│  └─ [Crear]

├─ Operaciones
│  ├─ Clave: [_____]
│  ├─ [Insertar] [Buscar] [Eliminar]
│  └─ [Información]

├─ Búsqueda paso a paso
│  ├─ Clave: [_____]
│  ├─ [Iniciar] [Paso] [Auto] [Pausar]
│  └─ (Visualización de pasos)

├─ Generación
│  ├─ Cantidad: [__]
│  └─ [Generar aleatorios]

└─ I/O
   ├─ [Guardar]
   └─ [Cargar]
```

### Estructura Común de Vistas de Grafos

```
Panel Izquierdo (Controles):
├─ Propiedades
├─ Crear vértices/aristas
├─ Eliminar/Modificar
├─ Operaciones algorítmicas
└─ Guardar/Cargar

Panel Derecho (Resultados):
├─ Canvas (visualización del grafo)
├─ Tabs (diferentes vistas)
└─ Tabla de resultados
```

---

## Patrones de Diseño

### 1. MVC (Model-View-Controller)

```
Model (models/)
  ↓ Proporciona datos
View (views/)
  ↓ Muestra e interactúa
Controller (app.py)
  ↓ Coordina eventos
```

### 2. Inheritance

```python
# Base para todas las vistas
class BaseContent(ctk.CTkFrame):
    title = "Título"
    def setup_ui(self): pass

# Implementación específica
class LinealContent(BaseContent):
    title = "Búsqueda Lineal"
    def setup_ui(self):
        # Crear interfaz específica
        pass
```

### 3. Strategy Pattern

**Hash:** Diferentes funciones hash intercambiables

```python
hash_strategies = {
    'cuadrado': self._h_square,
    'modular': self._h_modular,
    'plegamiento': self._h_folding,
    'truncamiento': self._h_truncate
}

# Usar:
h_func = hash_strategies[self.hash_func]
hash_value = h_func(key)
```

**Colisiones:** Diferentes estrategias de resolución

```python
collision_strategies = {
    'secuencial': lambda h, i: (h + i) % m,
    'doble': lambda h, i: (h + 2*i) % m,
    'cuadrado': lambda h, i: (h + i**2) % m,
}
```

### 4. Factory Pattern

```python
# En app.py
def show_content(self, key):
    ViewClass = self.contents[key]  # Factory
    self.current_content = ViewClass(self.content_container)
    self.current_content.pack(fill="both", expand=True)
```

### 5. Observer Pattern

```python
# Sidebar notifica a App sobre navegación
sidebar.set_on_select(app.handle_select)

# Button notifica vista sobre clic
button.configure(command=view.on_insertar)
```

### 6. Singleton Pattern

```python
# Una sola instancia de App
if __name__ == "__main__":
    app = App()  # Única instancia
    app.mainloop()
```

---

## API de Modelos

### LinearStructure / BinaryStructure

```python
# Crear
structure = LinearStructure(1000, 4)

# Insertar
try:
    idx = structure.insert(1234)
    print(f"Insertado en índice {idx}")
except ValueError as e:
    print(f"Error: {e}")

# Buscar
idx = structure.find(1234)
if idx >= 0:
    print(f"Encontrado en índice {idx}")
else:
    print("No encontrado")

# Eliminar
try:
    structure.delete(1234)
except ValueError as e:
    print(f"Error: {e}")

# Generar aleatorios
count = structure.generate_random(50)
print(f"Generados {count} elementos")

# Persistencia
json_str = structure.to_json()
new_structure = LinearStructure.from_json(json_str)
```

### HashStructure

```python
# Crear
h = HashStructure(
    capacity=100,
    key_length=3,
    hash_func='modular',
    collision='secuencial'
)

# Insertar
pos, collision_pos, attempts = h.insert(123)
print(f"Insertado en {pos}, intentos: {attempts}")

# Buscar
pos = h.find(123)

# Datos en bucket (encadenamiento)
items = h.bucket_items(pos)

# Generar tabla con datos
h.generate_random(20)
```

### WeightedGraph

```python
# Crear grafo
g = WeightedGraph(is_directed=False, has_weights=True)

# Agregar vértices
g.add_vertex("A")
g.add_vertex("B")
g.add_vertex("C")

# Agregar aristas
g.add_edge("e1", "A", "B", 1.0)
g.add_edge("e2", "B", "C", 2.0)

# MST
mst = g.minimum_spanning_tree("kruskal")
print(f"Peso MST: {mst['total_weight']}")

# Floyd-Warshall
fw = g.floyd_warshall()
print(f"Diámetro: {fw['diameter']}")
print(f"Radio: {fw['radius']}")

# Centro
center = g.find_tree_center()
print(f"Centro: {center['center_vertices']}")

# Mediana
median = g.find_median()
print(f"Mediana: {median['median_vertices']}")

# Distancia entre árboles
dist = g.tree_distance(tree1, tree2)
print(f"Distancia: {dist['distance']}")
```

### GraphTheory

```python
# Crear
gt = GraphTheory(is_directed=False)

# Agregar elementos
gt.add_vertex("A")
gt.add_edge("e1", "A", "B", 1.0)

# Matrices
adj_matrix = gt.vertex_adjacency_matrix()
inc_matrix = gt.vertex_incidence_matrix()
circuit_matrix = gt.fundamental_cycles()

# Circuitos
circuits = gt.find_all_cycles()
fundamental_circuits = gt.fundamental_cycles(mst_edges)

# Cortes
cut_sets = gt.find_fundamental_cut_sets(mst_edges)
```

---

## Persistencia de Datos

### Formato JSON

#### LinearStructure

```json
{
  "tipo": "lineal",
  "capacidad": 1000,
  "longitud_clave": 4,
  "datos": [1111, 1234, 2345, 3456, ...]
}
```

#### HashStructure

```json
{
  "tipo": "hash",
  "capacidad": 100,
  "longitud_clave": 3,
  "hash_func": "modular",
  "colision": "secuencial",
  "trunc_positions": null,
  "folding_op": null,
  "tabla": [123, null, 456, "DELETED", ...]
}
```

#### WeightedGraph

```json
{
  "vertices": ["A", "B", "C", "D"],
  "edges": {
    "e1": {"v1": "A", "v2": "B", "weight": 1.0},
    "e2": {"v1": "B", "v2": "C", "weight": 2.0},
    "e3": {"v1": "C", "v2": "D", "weight": 3.0},
    "e4": {"v1": "D", "v2": "A", "weight": 4.0}
  },
  "is_directed": false,
  "has_weights": true
}
```

### Guardado Manual

```python
# Guardar
with open("mi_estructura.json", "w") as f:
    f.write(structure.to_json())

# Cargar
with open("mi_estructura.json", "r") as f:
    structure = LinearStructure.from_json(f.read())
```

### Desde Interfaz

```python
# En vista:
from tkinter import filedialog

# Guardar
filename = filedialog.asksaveasfilename(
    defaultextension=".json",
    filetypes=[("JSON files", "*.json")]
)
if filename:
    with open(filename, "w") as f:
        f.write(self.structure.to_json())

# Cargar
filename = filedialog.askopenfilename(
    filetypes=[("JSON files", "*.json")]
)
if filename:
    with open(filename, "r") as f:
        self.structure = LinearStructure.from_json(f.read())
```

---

## Troubleshooting

### Problemas Comunes

#### 1. "ImportError: No module named 'customtkinter'"

**Solución:**
```bash
pip install customtkinter
```

#### 2. "ImportError: No module named 'networkx'"

**Solución:**
```bash
pip install networkx matplotlib
```

#### 3. Interfaz se ve pixelada o mal escalada

**Causa:** DPI scaling en Windows
**Solución:**
```python
# En app.py, antes de crear App:
import ctk
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
```

#### 4. Aplicación responde lentamente

**Causas posibles:**
- Generar muchos datos aleatorios
- Grafo muy grande (100+ vértices)
- Floyd-Warshall en grafo denso

**Soluciones:**
- Usar números más pequeños
- Simplificar grafo
- Usar búsqueda binaria en lugar de lineal

#### 5. "Estructura llena" en búsquedas

**Causa:** Intentar insertar más elementos que capacidad
**Solución:** Crear estructura con capacidad mayor

```python
# Cambiar de 10^2 (100) a 10^3 (1000)
structure = LinearStructure(1000, 4)
```

#### 6. Error al cargar grafo desde JSON

**Verificar:**
- Formato JSON válido
- Vértices referenciados existen
- Pesos son números

**Arreglarlo:**
```bash
# Validar JSON
python -m json.tool archivo.json
```

#### 7. Visualización de grafo en blanco

**Causa:** Grafo sin aristas o desconectado
**Solución:** Agregar más aristas o verificar conectividad

```python
if not graph.is_connected():
    print("Grafo desconectado - agregue más aristas")
```

### Debugging

#### Activar logs

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# En vista:
logger.debug(f"Insertando: {value}")
logger.info(f"Estructura llenada al {pct}%")
logger.error("Error crítico")
```

#### Inspeccionar estructura

```python
# Ver contenido actual
print(f"Elementos: {structure.items}")
print(f"Capacidad: {structure.capacity}")
print(f"Ocupación: {len(structure.items) / structure.capacity * 100:.1f}%")

# Grafo
print(f"Vértices: {graph.vertices}")
print(f"Aristas: {graph.edges}")
print(f"¿Conexo? {graph.is_connected()}")
```

---

## Contribuciones

### Estructura para Contribuidores

1. **Crear rama desde master**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Hacer cambios en models/**
   - Implementar algoritmo nuevo
   - Agregar métodos a clase existente

3. **Crear vista correspondiente en views/**
   - Heredar de `BaseContent`
   - Implementar `setup_ui()`
   - Agregar manejo de errores

4. **Actualizar app.py**
   - Agregar mapeo en `self.contents`
   - Agregar opción en sidebar

5. **Tests**
   - Crear tests en `tests/`
   - Ejecutar: `python -m pytest`

6. **Commit y Push**
   ```bash
   git add .
   git commit -m "Agregar: [descripción clara]"
   git push origin feature/nueva-funcionalidad
   ```

7. **Pull Request**
   - Describir cambios
   - Referenciar issues si aplica

### Guía de Estilo

**Python (PEP 8):**
```python
# Nombres claros
def find_maximum_spanning_tree(graph: WeightedGraph) -> Dict:
    """Descripción con docstring completo."""
    pass

# Type hints
def insert(self, value: int) -> bool:
    """Inserta valor, retorna True si se insertó."""
    pass

# Comentarios para lógica compleja
# Algoritmo: Kruskal con Union-Find
```

**Commits:**
```
Mensaje: "Agregar/Arreglar/Refactorizar: [descripción corta]"

Ejemplo:
  ✓ "Agregar: función is_tree() para verificación de árboles válidos"
  ✓ "Arreglar: error de desbordamiento en inserción hash"
  ✗ "fix bug" (poco descriptivo)
```

---

## Referencias y Recursos

### Librerías Utilizadas

- [CustomTkinter Documentation](https://github.com/TomSchimansky/CustomTkinter)
- [NetworkX Documentation](https://networkx.org/documentation/)
- [Matplotlib Documentation](https://matplotlib.org/)

### Algoritmos

- Kruskal MST: https://en.wikipedia.org/wiki/Kruskal%27s_algorithm
- Prim's Algorithm: https://en.wikipedia.org/wiki/Prim%27s_algorithm
- Floyd-Warshall: https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
- Huffman Coding: https://en.wikipedia.org/wiki/Huffman_coding

### Teoría de Grafos

- Graph Matrices: https://en.wikipedia.org/wiki/Incidence_matrix
- Fundamental Cycles: https://en.wikipedia.org/wiki/Cycle_basis
- Cut Sets: https://en.wikipedia.org/wiki/Cut_(graph_theory)

---

## Información de Soporte

**Problemas:** Reportar en GitHub Issues
**Sugerencias:** Crear GitHub Discussions
**Cambios Documentados:** Ver CHANGELOG.md (si existe)

---

**Última actualización:** Diciembre 2025
**Versión:** 1.0
**Estado:** Estable
