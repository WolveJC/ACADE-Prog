# Proyecto: Pila de Personas con Factorial 👤

![C++ Badge](https://img.shields.io/badge/Language-C++-blue.svg)
![Structure](https://img.shields.io/badge/Data_Structure-Stack_(LIFO)-purple.svg)
![Status](https://img.shields.io/badge/Status-Educational-green.svg)
![Platform](https://img.shields.io/badge/Platform-Console-lightgrey.svg)
![Purpose](https://img.shields.io/badge/Purpose-Factorial%20Calculation%20%26%20Data%20Storage-orange.svg)

## 📌 Descripción
Este programa en C++ permite registrar personas y almacenarlas en una **pila**.  
Cada persona tiene:
- Nombre y apellido
- Edad
- Altura
- Número asignado
- Factorial del número asignado

El sistema:
- Calcula el factorial del número ingresado.
- Almacena los datos en una pila.
- Al vaciar la pila, muestra los datos en consola y los guarda en un archivo `.txt`.

---

## ⚙️ Requisitos
- Lenguaje: C++ (versión 11 o superior recomendada)
- Librerías estándar: `<iostream>`, `<fstream>`, `<stdlib.h>`

---

## 🚀 Compilación y ejecución
```bash
g++ personas.cpp -o personas
./personas
```

---

## 🧩 Estructura del código

`struct per`
- `nom`: nombre
- `ap`: apellido
- `age`: edad
- `alt`: altura
- `numper`: número asignado
- `numfact`: factorial del número asignado

`struct Cont`
- Nodo que almacena una persona
- Puntero foll al siguiente nodo (para pila)

**Funciones principales**
- `int facto(int n)`
  Calcula el factorial de un número.
- `sozoPhill(...)`
  Inserta una persona en la pila.
- `hakaiPhill(...)`
  Extrae personas de la pila, muestra datos y los guarda en archivo.

`int main()`
- Solicita datos de varias personas.
- Calcula el factorial del número ingresado.
- Inserta personas en la pila.
- Al finalizar, pide nombre de archivo y guarda los datos.

---

## 🧪 Ejemplo de uso

**Entrada (usuario)**
```
Ingrese nombre de la persona:
Juan
Ingrese apellido de la persona:
Pérez
Ingrese edad de la persona:
25
Ingrese altura de la persona:
1.75
Ingrese numero para la persona:
5
Debe ingresar más datos? (s/n):
n
Ingrese el nombre con el que desea guardar el archivo:
personas
```

**Salida en consola**
```
Nombre: Juan Pérez
Apellido: Pérez
Edad: 25
Altura: 1.75
Numero asignado: 5
Numero factorial: 120
¿Sacar siguiente dato? (s/n)
```

**Archivo generado (personas.txt)**
```
Nombre: Juan
Apellido: Pérez
Edad: 25
Altura: 1.75m
Numero asignado: 5
Numero factorial: 120
```

---

## 📌 Notas
- Usar std::stack en lugar de punteros manuales.  
- Validar entradas (edad positiva, altura razonable, número factorial no excesivo).  
- Usar long long para factorial y evitar overflow.  
- Evitar system("cls") por ser dependiente de Windows.  
- Guardar en modo ios::app para no sobrescribir archivos previos.  
- Modularizar en clases para mayor claridad.
- Este programa es un buen ejemplo de estructuras dinámicas (pila) implementadas manualmente.  
- Demuestra el uso de punteros y memoria dinámica en C++.  
- Puede servir como base para sistemas más grandes de gestión de datos.  
- En aplicaciones reales se recomienda usar estructuras estándar `(std::stack)` y manejo de excepciones.  
