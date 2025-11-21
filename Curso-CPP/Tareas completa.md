# Proyecto: Gestor de Tareas 📝

## 📌 Descripción
Este programa en C++ implementa un gestor de tareas simple que clasifica las tareas en:
- **Urgentes** → almacenadas en una **pila** (stack).
- **Normales** → almacenadas en una **cola** (queue).

Permite:
- Agregar tareas.
- Mostrar tareas.
- Guardar tareas en un archivo (`tareas.txt`).
- Cargar tareas desde el archivo.

---

## ⚙️ Requisitos
- Lenguaje: C++ (versión 11 o superior recomendada)
- Librerías estándar: `<iostream>`, `<fstream>`, `<stack>`, `<queue>`, `<string>`

---

## 🚀 Compilación y ejecución
```bash
g++ tareas.cpp -o tareas
./tareas
```

---

## 🧩 Estructura del código

`struct Tarea`
- descripcion: texto de la tarea.
- urgente: booleano (true = urgente, false = normal).

**Funciones principales**
- `agregarTarea(stack<Tarea>&, queue<Tarea>&)`
  Solicita descripción y urgencia, agrega la tarea a la pila o cola.

- `mostrarTareas(const stack<Tarea>&, const queue<Tarea>&)`
  Muestra todas las tareas urgentes y normales.

- `guardarTareas(const stack<Tarea>&, const queue<Tarea>&)`
  Guarda las tareas en tareas.txt (1 = urgente, 0 = normal).

- `cargarTareas(stack<Tarea>&, queue<Tarea>&)`
  Carga las tareas desde tareas.txt.

`int main()`
- Inicializa pila y cola.
- Carga tareas desde archivo.
- Muestra menú interactivo:
  1. Agregar tarea  
  2. Mostrar tareas  
  3. Guardar tareas  
  4. Salir  

---

## 🧪 Ejemplo de uso

**Entrada (usuario)**
`
1. Agregar tarea
Descripción de la tarea: Comprar pan
¿Es urgente? (1: Sí, 0: No): 0
`

**Salida en consola**
`
Tareas Normales:
- Comprar pan
`

Archivo generado (tareas.txt)
`
0 Comprar pan
`

---

## 📌 Notas:
- Validar entrada de urgencia (solo 0 o 1).  
- Usar `cin.ignore(numeric_limits<streamsize>::max(), '\n')`; para limpiar buffer.  
- Añadir numeración al mostrar tareas.  
- Implementar clase `GestorTareas` para encapsular lógica.  
- Guardar en modo `ios::app` para no sobrescribir tareas previas.
- **Estructura de datos:** el uso de pila y cola es un buen ejemplo para diferenciar prioridades. La pila refleja urgencias inmediatas (última tarea agregada es la primera en atenderse), mientras que la cola refleja tareas normales en orden de llegada.  
- **Persistencia:** actualmente el programa guarda en texto plano. Para proyectos más grandes, podría usarse un formato estructurado como JSON o CSV.  
- **Escalabilidad:** el programa funciona bien para pocas tareas, pero si se manejan cientos, convendría optimizar la carga/guardado y añadir búsqueda o filtrado.  
- **Interfaz de usuario:** la interacción es por consola. Una mejora futura sería implementar una interfaz gráfica o web.  
- **Buenas prácticas:** encapsular en clases, usar `std::vector` para mayor flexibilidad, y aplicar manejo de excepciones `(try/catch)` para robustez.  
- Extensiones posibles:  
  - Marcar tareas como completadas.  
  - Añadir fechas límite.  
  - Prioridades múltiples (no solo urgente/normal).  
  - Exportar reportes de tareas.  
