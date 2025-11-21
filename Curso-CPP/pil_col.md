# Proyecto: Gestión de Estudiantes con Pila y Cola 🎓

## 📌 Descripción
Este programa en C++ permite registrar estudiantes y almacenarlos en dos estructuras:
- **Pila (stack)** → último en entrar, primero en salir.
- **Cola (queue)** → primero en entrar, primero en salir.

Cada estudiante tiene:
- Nombre y apellido
- Edad
- Nacionalidad
- Curso
- Promedio de tres notas (ponderado: 30%, 30%, 40%)

El sistema determina si el estudiante aprueba (≥10) o reprueba.

---

## ⚙️ Requisitos
- Lenguaje: C++ (versión 11 o superior recomendada)
- Librerías estándar: `<iostream>`, `<stdlib.h>`

---

## 🚀 Compilación y ejecución
```bash
g++ estudiantes.cpp -o estudiantes
./estudiantes
```

---

## 🧩 Estructura del código

`struct per`
- `nom`: nombre
- `ap`: apellido
- `age`: edad
- `contry`: nacionalidad

`struct estudiante`
- `pipol`: datos personales (per)
- `cur`: curso
- `prom`: promedio de notas

`struct Cont`
- Nodo que almacena un estudiante
- Puntero foll al siguiente nodo (para pila o cola)

**Funciones principales** 
- `float prom(float, float, float)`
  Calcula promedio ponderado de tres notas.
- `bool aprob(estudiante)`
  Retorna true si el promedio ≥ 10.
- `sozoPhill(...) / hakaiPhill(...)`
  Insertar y extraer estudiantes de la pila.
- `sozoCoil(...) / hakaiCoil(...)`
  Insertar y extraer estudiantes de la cola.

`int main()`
- Muestra menú principal:
  1. Ingresar y sacar pila
  2. Ingresar y sacar cola
  3. Salir
- Permite ingresar múltiples estudiantes.
- Al finalizar, muestra y vacía la pila o cola.

---

## 🧪 Ejemplo de uso

**Entrada (usuario)**

`MENU
1. Ingresar y Sacar pila
2. Ingresar y Sacar cola
3. Salir
Seleccione opción: 1
Ingrese nombre de la persona:
Juan
Ingrese apellido de la persona:
Pérez
Ingrese nacionalidad de la persona:
Venezolana
Ingrese edad de la persona:
20
Ingrese el curso del estudiante:
Matemáticas
Ingrese la nota 1:
12
Ingrese nota 2:
14
Ingrese nota 3:
15
El estudiante aprobo
¿Ingresar más datos? (s/n):
n`

**Salida en consola**

`Estudiantes en la pila:
Nombre y Apellido: Juan Pérez
Edad: 20
Nacionalidad: Venezolana
Curso: Matemáticas
Promedio: 13.9 - Aprobado`

---

## 📌 Notas
- Usar std::stack y std::queue en lugar de punteros manuales.  
- Validar entradas (notas entre 0–20, edad positiva).  
- Evitar system("cls") por ser dependiente de Windows.  
- Modularizar en clases (GestorEstudiantes).  
- Estandarizar nombres de funciones y variables.  
- Este programa es un buen ejemplo de estructuras dinámicas (pila y cola) implementadas manualmente.  
- Demuestra el uso de punteros y memoria dinámica en C++.  
- Puede servir como base para sistemas más grandes de gestión académica.  
- En aplicaciones reales se recomienda usar estructuras estándar `(std::stack, std::queue)` y manejo de excepciones.  
