# Proyecto: Registro de Vuelos ✈️

## 📌 Descripción
Este programa en C++ permite registrar información de varios vuelos (código, kilómetros recorridos y número de pasajeros).  
Luego determina:
- El vuelo con **mayor recorrido en kilómetros**.
- El vuelo con **mayor número de pasajeros**.  

Genera archivos `.txt` con los resultados.

---

## ⚙️ Requisitos
- Lenguaje: C++ (versión 11 o superior recomendada)
- Librerías estándar: `<iostream>`, `<fstream>`

---

## 🚀 Compilación y ejecución
```bash
g++ vuelos.cpp -o vuelos
./vuelos
```

---

## 🧩 Estructura del código

`struct Fly`
Estructura que almacena los datos de cada vuelo:
- code: código identificador del vuelo.
- km: kilómetros recorridos.
- num: número de pasajeros.

`void reciboPasajeros(float km)`
- Genera un archivo .txt con el recorrido en kilómetros del vuelo que tuvo más pasajeros.
- Parámetro: km → kilómetros recorridos por ese vuelo.

`void reciboKilometros(int code)`
- Genera un archivo .txt con el código del vuelo que recorrió más kilómetros.
- Parámetro: code → código del vuelo con mayor recorrido.

`int main()`
- Solicita datos de 5 vuelos (código, pasajeros, kilómetros).
- Determina el vuelo con mayor recorrido en kilómetros.
- Determina el vuelo con mayor número de pasajeros.
- Llama a las funciones para generar los archivos de recibo.

## 🧪 Ejemplo de uso

**Entrada:**
```
Ingrese código del vuelo 1: 101
Ingrese número de pasajeros del vuelo 1: 120
Ingrese kilómetros del vuelo 1: 500
...
```

**Salida en consola:**
```
Archivo generado: mayorRecorrido.txt
Archivo generado: masPasajeros.txt
```

**Archivos creados:**
- `mayorRecorrido.txt` → contiene el código del vuelo con mayor recorrido.  
- `masPasajeros.txt` → contiene los kilómetros recorridos por el vuelo con más pasajeros.  

---

## 📌 Notas
- El programa actualmente procesa 5 vuelos. Puede ampliarse modificando la constante N.  
- Los archivos generados se guardan en el mismo directorio donde se ejecuta el programa.  
- Se recomienda validar entradas para evitar errores (ej. pasajeros negativos).  
