# 1. Introducción
Bienvenido al manual de usuario del aplicativo **Ciencias de la Computacion 2**. Este software ha sido diseñado como una herramienta educativa e interactiva para la visualización y gestión de estructuras de datos. La interfaz gráfica permite interactuar con diversos métodos de búsqueda interna y externa, así como con algoritmos de grafos.
## 1.1 Módulos del sistema 

El sistema cuenta con los siguientes apartados principales:
#### A. Búsquedas Internas

Estas operaciones se realizan sobre datos almacenados completamente en la memoria principal (RAM) del ordenador.

- **Lineal:** Método de búsqueda secuencial que recorre la estructura elemento por elemento hasta encontrar el dato deseado o llegar al final.
    
- **Binaria:** Algoritmo eficiente que divide repetidamente el intervalo de búsqueda a la mitad. Requiere que la estructura esté previamente ordenada.
    
- **Funciones Hash:** Utiliza fórmulas matemáticas para transformar una clave en una dirección de memoria.
    
    - _Funciones disponibles:_ Cuadrática, Módulo (Mod), Plegamiento y Truncamiento.
        
    - _Soluciones de colisiones:_ Secuencial, Cuadrática, Doble función hash, Arreglos anidados y Encadenamiento.
        
- **Árbol Digital:** Estructura en forma de árbol que utiliza los bits de la clave para determinar la ramificación y posición del nodo.
    
- **Árbol de Residuos:** Variante de árbol de búsqueda basada en operaciones aritméticas modulares (residuos) para la inserción de claves.
    
- **Árbol de Residuos Múltiples:** Extensión del árbol de residuos que permite manejar múltiples claves o ramificaciones más complejas basadas en aritmética modular.
    
- **Árbol de Huffman:** Algoritmo utilizado para la compresión de datos. Crea un árbol binario basado en la frecuencia de aparición de los caracteres en una cadena de texto.
#### B. Búsquedas Externas

Estas operaciones están diseñadas para manejar grandes volúmenes de datos que no caben en la memoria principal, almacenándolos en dispositivos secundarios (disco duro).

- **Lineal:** Adaptación de la búsqueda secuencial para archivos o bloques de datos externos.
    
- **Binaria:** Adaptación del método de división de intervalos para acceder a registros en archivos ordenados.
    
- **Funciones Hash:** Implementación avanzada que gestiona el almacenamiento de colisiones y el acceso a disco mediante nuevas funciones hash optimizadas para acceso externo.
    
- **Estructuras dinámicas:** Métodos que permiten que el archivo o estructura crezca y se reduzca según sea necesario sin degradar el rendimiento.
    
- **Índices:** Uso de tablas auxiliares para localizar rápidamente registros en un archivo principal sin necesidad de recorrerlo por completo.
# 2. Como Ejecutar la Aplicación

Para iniciar el programa, siga estos pasos sencillos:

1. **Conexión:** Inserte la memoria USB que contiene el sistema en su computadora.
    
2. **Ubicación:** Abra la carpeta de la unidad USB. En ella encontrará el Manual Técnico, este Manual de Usuario y el archivo ejecutable del programa.
    
3. **Inicio:** Haga doble clic sobre el archivo ejecutable (`.exe`).
# 3. Navegación Básica 
## Componentes de la interfaz
Al iniciar el programa, visualizará la siguiente interfaz principal

![[Pasted image 20251129163841.png]]

1. **Área de Trabajo Principal:** Sección central que se actualiza dinámicamente para mostrar las herramientas y visualizaciones de la operación seleccionada.
    
2. **Menú Lateral de Navegación:** Panel izquierdo que permite explorar las categorías (Búsquedas, Grafos) y seleccionar módulos específicos.
    
3. **Configuración de Apariencia:** Menú desplegable ubicado en la esquina superior.
    
    - **Cambio de Tema:** Por defecto, el programa inicia en modo claro. Puede cambiar a **"Oscuro"** o **"Sistema"** (detecta automáticamente la preferencia de su S.O.) haciendo clic en la flecha junto al botón.
        

### 3.2 Selección de una operación

El menú lateral organiza las funciones en dos categorías: **"Búsquedas"** y **"Grafos"**.

**Pasos para acceder a un módulo:**

1. Haga clic en la categoría deseada (ej. **Búsquedas**) para desplegar las subcategorías.
    
2. Seleccione el tipo de búsqueda (ej. **Internas**).
    
3. Haga clic sobre el nombre del algoritmo específico (ej. **Lineal**).
    

_Nota: Puede colapsar los menús haciendo clic nuevamente en el botón azul de la categoría._

Ejemplo visual de navegación:

![[Pasted image 20251129172806.png]]

### 3.3 Regresar o Cambiar de Módulo

El programa no requiere un botón de "Atrás". Utilice el **Menú Lateral** en cualquier momento para cambiar inmediatamente entre diferentes apartados o algoritmos.
# 4. Uso de los Módulos de Búsquedas Internas

A continuación, se detalla el funcionamiento de cada herramienta de búsqueda interna.

### 4.1 Búsqueda Lineal

Este módulo permite visualizar cómo funciona la búsqueda secuencial en una lista de datos.

Componentes de la Interfaz:

![[Pasted image 20251129194746.png]]

1. **Panel de Configuración:** Permite definir el tamaño de la estructura ($10^n$, donde el usuario elige $n$) y la longitud de la clave. Incluye botones para **Crear** y **Borrar** la estructura e indicadores de capacidad.
    
2. **Panel de Operaciones:** Campo de texto para ingresar una clave manual y botones para **Insertar**, **Buscar** o **Eliminar**.
    
3. **Generador Aleatorio:** Herramienta para insertar múltiples claves al azar rápidamente.
    
4. **Gestión de Archivos:** Opciones para **Guardar** el estado actual o **Cargar** una estructura previa.
    
5. **Simulación Paso a Paso:** Controles para ver la animación detallada del algoritmo de búsqueda.
    
6. **Registro de Eventos:** Texto informativo que confirma acciones.
    
7. **Vista Previa:** Representación visual de la estructura de datos.
    

**Guía de Uso:**

1. **Crear Estructura:** En el panel (1), seleccione el exponente $n$ para el tamaño y la longitud de la clave. Presione **Crear**. _Nota: Para cambiar estos parámetros posteriormente, deberá presionar "Borrar Estructura" y crear una nueva._
    
2. **Insertar Datos:**
    
    - _Manualmente:_ Escriba un valor en el panel (2) y pulse **Insertar**.
        
    - _Aleatoriamente:_ En el panel (3), elija la cantidad de datos y pulse el botón de generación para llenar la estructura rápidamente.
        
3. **Buscar Datos:** Ingrese la clave en el panel (2).
    
    - Pulse **Buscar** para una búsqueda instantánea (el elemento se resaltará en la Vista Previa).
        
    - Utilice el panel (5) **Paso a Paso** si desea ver cómo el algoritmo recorre cada posición secuencialmente.
        
4. **Eliminar:** Ingrese la clave en el panel (2) y pulse **Eliminar**.
    
5. **Guardar/Cargar:** Use el panel (4) para respaldar su trabajo actual.

## 4.3 Búsqueda Binaria

Este módulo ejemplifica el algoritmo de búsqueda por división de intervalos.
Componentes de la Interfaz:

![[Pasted image 20251129194746.png]]

1. **Panel de Configuración:** Permite definir el tamaño de la estructura ($10^n$, donde el usuario elige $n$) y la longitud de la clave. Incluye botones para **Crear** y **Borrar** la estructura e indicadores de capacidad.
    
2. **Panel de Operaciones:** Campo de texto para ingresar una clave manual y botones para **Insertar**, **Buscar** o **Eliminar**.
    
3. **Generador Aleatorio:** Herramienta para insertar múltiples claves al azar rápidamente.
    
4. **Gestión de Archivos:** Opciones para **Guardar** el estado actual o **Cargar** una estructura previa.
    
5. **Registro de Eventos:** Texto informativo que confirma acciones.
    
6. **Vista Previa:** Representación visual de la estructura de datos.
    

**Guía de Uso:**

1. **Crear Estructura:** En el panel (1), seleccione el exponente $n$ para el tamaño y la longitud de la clave. Presione **Crear**. _Nota: Para cambiar estos parámetros posteriormente, deberá presionar "Borrar Estructura" y crear una nueva._
    
2. **Insertar Datos:**
    
    - _Manualmente:_ Escriba un valor en el panel (2) y pulse **Insertar**.
        
    - _Aleatoriamente:_ En el panel (3), elija la cantidad de datos y pulse el botón de generación para llenar la estructura rápidamente.
        
3. **Buscar Datos:** Ingrese la clave en el panel (2).
    
    - Pulse **Buscar** para una búsqueda instantánea (el elemento se resaltará en la Vista Previa).
        
4. **Eliminar:** Ingrese la clave en el panel (2) y pulse **Eliminar**.
    
5. **Guardar/Cargar:** Use el panel (4) para respaldar su trabajo actual.
## 4.4 Búsqueda con funciones hash
Este módulo permite experimentar con el almacenamiento y recuperación de datos utilizando algoritmos de direccionamiento calculado y cómo el sistema resuelve conflictos cuando dos claves aspiran a ocupar la misma posición.

![[Pasted image 20251201120844.png]]

1. **Panel de Configuración de Estructura:** Este es el panel más importante del módulo. Contiene los controles necesarios para definir la lógica del algoritmo:
    
    - **Selector de Función Hash:** Menú desplegable para elegir el método de transformación de la clave: _Cuadrática, Función Mod (Módulo), Plegamiento_ o _Truncamiento_.
        
    - **Selector de Solución de Colisiones:** Menú para definir cómo actuar si una posición está ocupada: _Secuencial, Cuadrática, Doble función hash, Arreglos anidados_ o _Encadenamiento_.
        
    - **Parámetros de Tamaño:** Entrada numérica para definir la capacidad ($10^n$) y la longitud de la clave.
        
    - **Controles de Estado:** Botones **Crear** y **Borrar Estructura**, junto con un indicador de texto que muestra la capacidad total y el número de elementos ocupados actualmente.
        
    - _Nota:_ Las opciones de Función y Colisión se bloquean una vez creada la estructura.
        
2. **Panel de Operaciones:** Contiene una caja de texto para que el usuario introduzca una clave específica y los botones de comando para **Insertar**, **Buscar** o **Eliminar** dicha clave en la tabla.
    
3. **Generador Aleatorio:** Herramienta diseñada para pruebas de estrés. Permite al usuario especificar un número de claves aleatorias y generarlas masivamente para observar cómo se comporta la distribución de datos y la frecuencia de colisiones.
    
4. **Gestión de Archivos:** Botones para **Guardar** la estructura actual o **Cargar** una previamente almacenada.
    
5. **Registro de Eventos (Log):** Un área de texto informativo que reporta las acciones internas del sistema en tiempo real.
    
6. **Vista Previa:** Representación gráfica de la tabla Hash. Aquí podrá ver los índices, los valores almacenados y, en el caso del encadenamiento o arreglos anidados, las estructuras adicionales que se generan.
#### Guía de uso

1. **Configuración y Creación:**
    
    - Diríjase al **Panel 1**. Antes de cualquier otra acción, debe seleccionar la **Función Hash** y la **Solución de Colisiones** que desea probar.
        
    - Defina el tamaño de la estructura (seleccionando el valor de $n$ para $10^n$) y la longitud de la clave.
        
    - Haga clic en el botón **Crear**.
        
    - _Advertencia:_ Una vez creada la estructura, no podrá cambiar la función hash ni el método de colisión. Si desea probar una combinación diferente, deberá pulsar **Borrar Estructura** y configurar los parámetros nuevamente.
        
2. **Inserción de Datos:**
    
    - **Manual:** Escriba una clave en el **Panel 2** y presione **Insertar**. Observe en la **Vista Previa** dónde se coloca el dato.
        
    - **Aleatoria:** Si desea llenar la tabla rápidamente, vaya al **Panel 3**, ingrese la cantidad de claves deseadas y presione el botón de generación.
        
3. **Búsqueda de Datos:**
    
    - Ingrese la clave que desea localizar en la caja de texto del **Panel 2**.
        
    - Presione el botón **Buscar**.
        
    - El sistema resaltará la posición de la clave en la **Vista Previa**. Si la clave no existe, el **Registro de Eventos (5)** le informará que el dato no fue encontrado.
        
4. **Eliminación:**
    
    - Para borrar un dato, ingréselo en el **Panel 2** y presione **Eliminar**. El sistema liberará el espacio o actualizará los enlaces según el método de colisión seleccionado.
        
5. **Guardado y Carga:**
    
    - Utilice las opciones del **Panel 4** para guardar su trabajo.
        
    - _Importante:_ La función de guardar en este módulo es avanzada; no solo almacena los datos contenidos en la tabla, sino que también guarda la configuración específica (qué función hash y qué solución de colisiones se usó) para asegurar la integridad de la estructura al momento de cargarla nuevamente.
## 4.5 Búsqueda por Arboles (Digital, Residuo y Residuo Multiple)

A continuación, encontrara de manera detallada una explicación de los componentes de la interfaz grafica y como usarlos para poder generar arboles digitales, de residuo o de residuo multiple. 

**No se proporciona una explicación individual debido a que los 3 módulos comparten la misma interfaz**, por lo que el proceso para utilizarlos es identifico.

![[Pasted image 20251201121313.png]]

1. **Área de Visualización del Árbol:** Es el lienzo principal (sección 1) donde se dibuja el árbol dinámicamente. A medida que se insertan datos, los nodos y las ramas aparecen aquí, permitiendo al usuario seguir visualmente el camino que recorre el algoritmo bit a bit.
    
2. **Panel de Operaciones:** Ubicado en la sección 2, este panel permite la interacción directa con la estructura:
    
    - **Campo de Entrada:** Espacio para digitar la letra o carácter que se desea procesar.
        
    - **Botones de Acción:** Controles para **Insertar** un nuevo nodo, **Buscar** uno existente o **Eliminar** un carácter del árbol.
        
3. **Herramientas de Referencia y Registro:**
    
    - **Botón "Mostrar tabla de códigos":** Al presionar este botón (sección 3), se despliega una tabla auxiliar que muestra la información de cada letra junto con su representación en binario. Esta herramienta es vital para entender por qué el árbol toma cierta forma.
        
    - **Registro de Eventos (Log):** Un área de texto situada debajo de la tabla que informa al usuario sobre el estado de las operaciones (ej. _"Nodo 'A' insertado exitosamente"_).
        
4. **Gestión de la Estructura:** Tres botones dedicados (sección 4) para el manejo general del lienzo:
    
    - **Guardar:** Almacena el estado actual del árbol.
        
    - **Cargar:** Recupera un árbol previamente guardado.
        
    - **Limpiar:** Borra todo el contenido del área de visualización (sección 1) para iniciar desde cero sin cerrar el programa.
        

#### Guía de uso

El flujo de trabajo en este módulo está orientado a la enseñanza de la inserción basada en bits:

1. **Inserción de Nodos:**
    
    - Escriba una letra en el campo de texto del **Panel de Operaciones**.
        
    - Haga clic en **Insertar**.
        
    - Observe el **Área de Visualización**: Verá aparecer un nuevo nodo. La dirección que toma la rama (izquierda o derecha) depende de los bits del carácter.
        
2. **Análisis de la Estructura:**
    
    - Si tiene dudas sobre la ubicación de un nodo, pulse **"Mostrar tabla de códigos"**.
        
    - Compare la representación binaria de la letra con el camino trazado en el árbol. Por ejemplo, si el código empieza con '0', la rama irá hacia un lado; si empieza con '1', irá hacia el otro.
        
3. **Búsqueda y Eliminación:**
    
    - Para verificar la existencia de un dato, ingrese la letra y pulse **Buscar**. El sistema resaltará el nodo correspondiente en el gráfico.
        
    - Para borrar, ingrese la letra y pulse **Eliminar**. Observe cómo la estructura se reajusta si es necesario.
        
4. **Mantenimiento:**
    
    - Si desea reiniciar el ejercicio completamente, utilice el botón **Limpiar**.
        
    - Use **Guardar** y **Cargar** para preservar sus ejemplos educativos o sesiones de prueba.
## 4.6 Búsqueda por Arbol de Huffman

Este módulo ilustra el funcionamiento del algoritmo de Huffman. A diferencia de los árboles anteriores que se construyen nodo a nodo manualmente, este árbol se genera a partir de la frecuencia de aparición de caracteres en una cadena de texto completa.

![[Pasted image 20251201122703.png]]

- **1. Área de Visualización del Árbol:** El espacio principal donde se renderiza el árbol binario resultante tras el análisis de frecuencias. Las letras más frecuentes aparecerán más cerca de la raíz.
    
- **2. Panel de Generación (Frecuencia):**
    
    - **Campo de Texto:** Un espacio amplio donde el usuario debe ingresar una palabra o frase completa (ej. "MISSISSIPPI").
        
    - **Botón Generar:** El comando que inicia el cálculo de frecuencias y construye el árbol automáticamente basándose en la entrada.
        
- **3. Panel de Operaciones Individuales:**
    
    - Diseñado para interactuar con el árbol una vez creado. Contiene un campo para ingresar una letra individual y botones para **Buscar** esa letra en la estructura o **Eliminar** su nodo correspondiente.
        
- **4. Herramientas de Referencia y Registro:**
    
    - **Botón "Mostrar tabla de códigos":** En este contexto, la tabla es crucial, ya que muestra el **nuevo código binario comprimido** generado para cada carácter (longitud variable), en lugar del código ASCII estándar.
        
    - **Registro de Eventos (Log):** Texto informativo sobre las acciones realizadas.
        
- **5. Gestión de la Estructura:** Botones para **Guardar** el árbol generado, **Cargar** uno previo y **Limpiar** la visualización.
#### Guía de uso

El uso de este módulo difiere ligeramente de los demás debido al paso previo de generación:

1. **Generación del Árbol (Paso Obligatorio):**
    
    - Diríjase al **Panel de Generación (2)**.
        
    - Introduzca una palabra o frase en el campo de texto. Se recomienda usar palabras con letras repetidas para apreciar mejor el efecto de la frecuencia (ej. "BANANA").
        
    - Presione **Generar**. El sistema analizará el texto y dibujará el árbol en el área de visualización.
        
2. **Análisis de Compresión:**
    
    - Observe la posición de los nodos: Las letras que más se repiten en su palabra estarán ubicadas en la parte superior del árbol (códigos más cortos). Las letras menos frecuentes estarán en las ramas más profundas (códigos más largos).
        
    - Pulse **"Mostrar tabla de códigos"** para verificar la asignación de bits resultante y compararla con la longitud de un código estándar.
        
3. **Interacción con Nodos:**
    
    - Una vez generado el árbol, puede utilizar el **Panel de Operaciones Individuales (3)**.
        
    - Ingrese una letra específica contenida en su palabra y pulse **Buscar** para localizarla visualmente en la jerarquía.
        
    - Utilice **Eliminar** si desea remover un nodo específico del árbol generado.

4. **Persistencia:**

    - Utilice los botones de **Guardar** y **Cargar** para almacenar su árbol de Huffman.

Aqui se añade un componente adicional
 - 1. La sección donde se mostrara el arbol según el usuario vaya ingresando claves (letras)
- 2. (Aquí existe el espacio donde el usuario puede digitar la palabra y el boton generar. Se crea el arbol a aprtir de eso)
- 3. Aqui existe el espacio donde el usuario puede insertar una letra y los botones para decidir que se hace con esa letra: Buscar o eliminar.
- 4. Aquí existe un botón "Mostrar tabla de códigos" que al ser presionado muestra una tabla con la información de de cada letra en binario con la cual se esta basando el programa para hacer la inserción y debajo esta un pequeño apartado de texto que le informa al usuario de las acciones que se van realizando.
- 5. Existen 3 botones, el boton para guardar el arbol, el boton para cargar y el boton para limpiar la seccion 1 (donde se ve el arbol)

# 5. Uso de los Módulos de Grafos

A continuación, se detalla el funcionamiento de cada herramienta de grafos. Los grafos son estructuras que representan conexiones entre elementos. Piense en una red de ciudades (elementos) conectadas por carreteras (conexiones).

## 5.1 Operaciones de Grafos

Este módulo permite crear múltiples grafos y realizar operaciones entre ellos, como crear uniones, intersecciones y otras combinaciones que resultan en nuevos grafos.

**¿Qué es una Operación de Grafos?**

Una operación de grafos es una manera de combinar o modificar grafos. Por ejemplo:
- **Unión:** Juntar todas las conexiones de dos grafos en uno solo.
- **Intersección:** Mantener solo las conexiones que existen en ambos grafos.
- **Complemento:** Invertir las conexiones (las que existían ahora no existen y viceversa).

![[Pasted image operaciones grafos.png]]

1. **Panel de Creación de Grafos:** Ubicado en la sección izquierda, permite crear varios grafos (llamados G1, G2, G3, etc.). Cada grafo es independiente y contiene sus propios puntos (vértices) y conexiones (aristas).

2. **Controles de Vértices:** Campo de entrada para escribir el nombre de un punto (por ejemplo "A", "B", "Ciudad1"). Incluye botones para **Agregar Vértice** y **Eliminar Vértice**.

3. **Controles de Aristas (Conexiones):** Campos para definir una conexión entre dos puntos. Puede ingresar:
    - El nombre de la arista (por ejemplo "e1", "ruta1")
    - El primer punto (por ejemplo "A")
    - El segundo punto (por ejemplo "B")
    - El peso o valor de la conexión (opcional, puede ser 1 si no especifica)

4. **Panel de Operaciones:** Botones para realizar acciones entre grafos:
    - **Unión:** Combina todos los puntos y conexiones de dos grafos.
    - **Intersección:** Mantiene solo lo que existe en ambos grafos.
    - **Complemento:** Invierte las conexiones.
    - **Producto Cartesiano, Producto Tensorial:** Operaciones más avanzadas.

5. **Visualización:** Panel derecho donde se muestra el grafo dibujado. Verá los puntos como círculos y las conexiones como líneas entre ellos.

6. **Tabla de Resultados:** Área que muestra información detallada de los grafos y las operaciones realizadas.

#### Guía de Uso

1. **Crear un Grafo:**

    - En el panel izquierdo, ingrese el nombre de un punto en el campo de **Vértices** (por ejemplo "A").

    - Presione **Agregar Vértice**. El punto aparecerá en la visualización.

    - Repita el proceso para crear más puntos (B, C, D, etc.).

2. **Agregar Conexiones (Aristas):**

    - En los campos de **Aristas**, escriba:
        - Nombre de la conexión: "e1"
        - Primer punto: "A"
        - Segundo punto: "B"
        - Peso: "1" (o el valor que desee)

    - Presione **Agregar Arista**. Verá una línea conectando A y B en la visualización.

    - Repita para crear un grafo completo.

3. **Crear un Segundo Grafo:**

    - Repita los pasos anteriores para crear G2 con sus propios puntos y conexiones.

4. **Realizar Operaciones:**

    - Una vez tenga dos grafos, seleccione la operación deseada en el **Panel de Operaciones** (por ejemplo "Unión").

    - El sistema creará un nuevo grafo resultado y lo mostrará en la visualización.

    - Observe en la **Tabla de Resultados** los detalles de la nueva estructura.

5. **Guardar y Cargar:**

    - Use los botones de **Guardar** para almacenar sus grafos.

    - Use **Cargar** para recuperar grafos previamente guardados.

## 5.2 Matrices de Grafos (Teoría de Grafos)

Este módulo permite visualizar un grafo en forma de tablas matemáticas llamadas **matrices**. Las matrices son una forma especial de representar gráficamente cómo se conectan los puntos.

**¿Por qué Matrices?**

Las matrices permiten analizar matemáticamente las propiedades de un grafo. En lugar de ver solo el dibujo, verá tablas numéricas que revelan información oculta sobre la estructura.

![[Pasted image matrices.png]]

1. **Panel de Propiedades del Grafo:** Ubicado en la sección superior izquierda, permite elegir características del grafo:
    - **¿Es dirigido?** Si marca esta opción, las conexiones tienen dirección (van de A a B, no de B a A).
    - **¿Tiene pesos?** Si marca esta opción, cada conexión puede tener un valor numérico.

2. **Panel de Creación:** Espacio para ingresar vértices y aristas, similar al módulo anterior:
    - Campo de **Vértice** con botón **Agregar**.
    - Campos de **Arista** (nombre, punto origen, punto destino, peso) con botón **Agregar**.
    - Botones para **Eliminar Vértice** y **Eliminar Arista**.

3. **Botones de Matrices:** Panel con botones para visualizar diferentes tablas:
    - **Matriz de Adyacencia:** Muestra cuáles puntos están conectados directamente.
    - **Matriz de Incidencia:** Muestra cuáles puntos están involucrados en cada conexión.
    - **Circuitos:** Muestra todos los ciclos (bucles cerrados) que existen en el grafo.
    - **Conjuntos de Corte:** Muestra qué conexiones, si se eliminaran, desconectarían el grafo.

4. **Visualización del Grafo:** Panel derecho donde ve el dibujo del grafo con sus puntos y conexiones.

5. **Tabla de Resultados:** Área central que muestra la matriz seleccionada como una tabla numérica clara y legible.

#### Guía de Uso

1. **Configurar el Tipo de Grafo:**

    - En el **Panel de Propiedades**, marque o desmarque según necesite:
        - **Dirigido** si las conexiones tienen dirección.
        - **Con Pesos** si cada conexión tiene un valor.

2. **Crear el Grafo:**

    - Agregue vértices: ingrese nombres (A, B, C, ...) y presione **Agregar Vértice**.

    - Agregue aristas: ingrese el nombre, los dos puntos que conecta y opcionalmente el peso.

    - Presione **Agregar Arista**.

3. **Ver una Matriz:**

    - En el **Panel de Matrices**, presione el botón de la matriz que desea ver.

    - La tabla aparecerá en el área de **Tabla de Resultados**.

    - **Nota:** Las filas y columnas representan vértices. Un "1" o número significa que hay conexión; "0" significa que no hay.

4. **Interpretar los Resultados:**

    - **Matriz de Adyacencia:** Si ve un "1" en la fila A y columna B, significa que A está conectado a B.

    - **Matriz de Incidencia:** Si ve un "1" en la fila A y columna e1, significa que A participa en la conexión e1.

    - **Circuitos:** Si el botón está disponible, verá todos los ciclos (caminos que vuelven al punto de inicio).

5. **Guardar y Cargar:**

    - Use los botones de **Guardar** para almacenar el grafo y sus matrices.

    - Use **Cargar** para recuperar trabajo anterior.

## 5.3 Árboles de Expansión (Árboles a partir de Grafos)

Este módulo calcula **árboles de expansión mínimos** a partir de un grafo. Un árbol de expansión es un subconjunto especial del grafo que conecta todos los puntos usando el menor número de conexiones (y opcionalmente el menor peso total).

**¿Qué es un Árbol de Expansión?**

Imagine que tiene una ciudad con varias calles conectando diferentes barrios. Un árbol de expansión es la selección mínima de calles que aseguran que todos los barrios permanezcan conectados. El árbol de expansión **mínimo** es aquel que usa la menor distancia total.

![[Pasted image arbol expansion.png]]

1. **Panel de Configuración del Grafo:** Ubicado en la sección izquierda, permite:
    - Elegir si el grafo es **Dirigido** (conexiones con dirección) o no.
    - Elegir si tiene **Pesos** (valores en cada conexión).
    - Botones para crear, borrar y obtener información del grafo.

2. **Panel de Creación de Vértices y Aristas:** Espacio para construir el grafo:
    - Campo de **Vértice** con botón **Agregar Vértice**.
    - Campos de **Arista** (nombre, vértice 1, vértice 2, peso) con botón **Agregar Arista**.
    - Botones para **Eliminar** o **Modificar** vértices y aristas.

3. **Panel de Operaciones MST:** Botones para calcular el árbol mínimo:
    - **Generar Árbol Mínimo (Kruskal):** Algoritmo que selecciona conexiones en orden de peso (menor primero).
    - **Ver 3 Grafos:** Muestra simultáneamente el grafo original, el árbol mínimo y las conexiones no utilizadas.
    - **Identificar Ramas y Cuerdas:** Separa las conexiones usadas (ramas) de las no usadas (cuerdas).

4. **Panel de Análisis Avanzado:**
    - **Ejecutar Floyd-Warshall:** Calcula la distancia más corta entre todos los puntos.
    - **Calcular Centro:** Encuentra el punto más central del árbol.
    - **Hallar Mediana:** Encuentra el punto que minimiza las distancias totales.

5. **Panel de Distancia entre Árboles:**
    - **Cargar MST como Árbol 1:** Guarda el árbol actual como referencia.
    - **Cargar MST como Árbol 2:** Guarda un segundo árbol para comparar.
    - **Usar Prim para Árbol 2:** Genera un segundo árbol usando un algoritmo diferente.
    - **Calcular Distancia:** Compara los dos árboles y muestra cuántas conexiones diferente tienen.

6. **Visualización:** Panel derecho donde se dibuja:
    - El grafo original (con todas las conexiones).
    - El árbol mínimo (solo las conexiones necesarias).
    - El complemento (las conexiones no utilizadas).

7. **Tabla de Resultados:** Área que muestra matrices de distancias y análisis detallado.

#### Guía de Uso - Crear un Árbol de Expansión Mínimo

1. **Configurar el Grafo:**

    - En el **Panel de Configuración**, marque:
        - **Dirigido:** Solo si las conexiones tienen sentido único.
        - **Con Pesos:** Casi siempre (es lo normal en árboles mínimos).

2. **Crear el Grafo:**

    - Agregue vértices: ingrese nombres (A, B, C, D) y presione **Agregar Vértice**.

    - Agregue aristas: ingrese para cada conexión:
        - Nombre: "e1", "e2", etc.
        - Vértice 1: "A"
        - Vértice 2: "B"
        - Peso: "5" (o cualquier número)

    - Presione **Agregar Arista** para cada conexión.

3. **Generar el Árbol Mínimo:**

    - En el **Panel de Operaciones MST**, presione **Generar Árbol Mínimo (Kruskal)**.

    - El sistema calculará automáticamente el árbol y lo dibujará en la visualización.

    - Verá en pantalla qué conexiones se seleccionaron y el peso total.

4. **Visualizar los Tres Grafos:**

    - Presione **Ver 3 Grafos**.

    - Verá en pantalla:
        - **Arriba a la izquierda:** Su grafo original con todas las conexiones.
        - **Arriba a la derecha:** El árbol mínimo calculado (solo las conexiones necesarias).
        - **Abajo:** Las conexiones no utilizadas (complemento).

5. **Analizar Ramas y Cuerdas:**

    - Presione **Identificar Ramas y Cuerdas**.

    - **Ramas:** Las conexiones que forman el árbol mínimo.

    - **Cuerdas:** Las conexiones que no se usaron en el árbol.

6. **Ejecutar Floyd-Warshall (Distancias):**

    - Presione **Ejecutar Floyd-Warshall**.

    - Verá una tabla que muestra la distancia más corta entre cada par de puntos.

    - También se mostrarán:
        - **Diámetro:** La distancia máxima entre cualquier par de puntos.
        - **Radio:** La distancia máxima más pequeña que se puede lograr.

7. **Encontrar el Centro:**

    - Presione **Calcular Centro**.

    - El sistema resaltará el punto o puntos más centrales del árbol.

    - El centro es útil para ubicar recursos (como una estación de bomberos) de manera óptima.

8. **Encontrar la Mediana:**

    - Presione **Hallar Mediana**.

    - La mediana es el punto que minimiza la distancia total a todos los demás puntos.

    - Es diferente del centro e igualmente útil para ubicación óptima.

#### Guía de Uso - Comparar Dos Árboles de Expansión

Este proceso permite comparar diferentes maneras de crear el árbol mínimo usando distintos algoritmos.

1. **Crear el Primer Árbol:**

    - Siguiendo los pasos anteriores, cree un grafo y genere su árbol mínimo con Kruskal.

    - En el **Panel de Distancia entre Árboles**, presione **Cargar MST como Árbol 1**.

    - Verá un mensaje confirmando que el árbol se guardó como referencia.

2. **Generar el Segundo Árbol (Diferente):**

    - En el **Panel de Distancia entre Árboles**, presione **Usar Prim para Árbol 2**.

    - Esto genera un árbol mínimo usando un algoritmo diferente (Prim en lugar de Kruskal).

    - **Nota:** Ambos algoritmos generan árboles con el MISMO peso total, pero pueden usar diferentes conexiones.

3. **Calcular la Diferencia:**

    - Presione **Calcular Distancia**.

    - El sistema mostrará:
        - **Unión:** Todas las conexiones que usan los dos árboles.
        - **Intersección:** Las conexiones que ambos árboles comparten.
        - **Diferencia:** Las conexiones que uno tiene pero el otro no.
        - **Distancia:** Un número que indica cuán diferentes son los árboles.

4. **Interpretar los Resultados:**

    - Si la **Distancia es 0:** Los dos árboles son idénticos.

    - Si la **Distancia es mayor:** Los árboles usan diferentes conexiones (pero siguen teniendo el mismo peso total).

    - Esto demuestra que para un mismo grafo, pueden existir múltiples árboles mínimos válidos.

#### Tips y Consejos para Grafos

**Grafo Simple (para aprender):**
```
Vértices: A, B, C, D
Aristas:
  e1: A-B (peso 1)
  e2: B-C (peso 2)
  e3: C-D (peso 3)
  e4: D-A (peso 4)
  e5: A-C (peso 2)
```

**Esperado:** El árbol mínimo usará e1, e2, e3, e4 con peso total = 10.

**Grafo Más Complejo (para explorar):**

Agregue más puntos y más conexiones para ver cómo los algoritmos seleccionan automáticamente las mejores.

**Grafos Dirigidos:**

Si marca "Dirigido", debe recordar que las conexiones tienen dirección (A→B es diferente de B→A).

**Guardar Trabajo:**

Use los botones **Guardar** y **Cargar** para almacenar grafos interesantes que quiera reutilizar.