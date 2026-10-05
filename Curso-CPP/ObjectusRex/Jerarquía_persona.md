# Proyecto: Sistema de Personas, Trabajadores y Estudiantes 👥

![C++ Badge](https://img.shields.io/badge/Language-C++-blue.svg)
![Status](https://img.shields.io/badge/Status-Educational-green.svg)
![Platform](https://img.shields.io/badge/Platform-Console-lightgrey.svg)
![Concepts](https://img.shields.io/badge/Concepts-OOP%20%7C%20Inheritance%20%7C%20Polymorphism-orange.svg)

## 📌 Descripción
Este programa en C++ implementa un sistema orientado a objetos para representar diferentes tipos de personas:
- **Persona**: atributos básicos (nombre, apellido, cédula, edad).
- **Trabajador**: hereda de persona, añade puesto y salario.
- **Estudiante (stu)**: hereda de persona, añade curso, notas y promedio.
- **Universitario (uni)**: hereda de estudiante, añade carrera y título.

El programa demuestra **herencia, polimorfismo y encapsulamiento** en C++.

---

## ⚙️ Requisitos
- Lenguaje: C++ (versión 11 o superior recomendada)
- Librerías estándar: `<iostream>`

---

## 🚀 Compilación y ejecución
```bash
g++ personas.cpp -o personas
./personas
```

---

## 🧩 Estructura del código

`class persona`
- **Atributos privados:** `nom, ap, ci, age`.
- **Métodos:**
  - `ter_setpersona(...)`: asigna valores a los atributos.
  - `tergetnom()`, `tergetap()`, `tergetci()`, `tergetage()`: devuelven los atributos.
  - `show_pipol()`: imprime la información de la persona.

`class trabajador : public persona`
- **Atributos privados:** `puesto, salario`.
- **Métodos:**
  - `ter_setjob(...)`: asigna datos de persona + puesto y salario.
  - `tergetpuesto(), tergetsalario()`: devuelven atributos.
  - `show_job()`: imprime datos de persona y del trabajador.

`class stu : public persona`
- **Atributos privados:** `curso, nota1, nota2, nota3, prom`.
- **Métodos:**
  - `ter_setestu(...)`: asigna datos de persona + curso y notas.
  - `set_promedio(...)`: calcula el promedio de las notas.
  - `tergetcuerso(), tergetprom()`: devuelven atributos.
  - `show_estu()`: imprime datos de persona y del estudiante.

`class uni : public stu`
- **Atributos privados:** `carear, title`.
- **Métodos:**
  - `ter_setuni(...)`: asigna datos de persona + estudiante + carrera y título.
  - `tergetcarear(), tergettitle()`: devuelven atributos.
  - `show_unity()`: imprime datos de persona, estudiante y universitario.

`int main()`
- Crea objetos dinámicos de trabajador, stu y uni.
- Asigna valores con los métodos set.
- Muestra la información con los métodos show.
- Libera memoria con delete.

---

## 🧪 Ejemplo de uso

**Entrada (en código)**
```cpp
trabajador* emp = new trabajador();
emp->ter_setjob("Mario", "Garcia", 4567233, 34, "Obrero", 130);

stu* estudiante = new stu();
estudiante->ter_setestu("Adol", "Cristin", 30665344, 18, "Castellano", 16, 13, 14);

uni* estUni = new uni();
estUni->ter_setuni("Juan", "Pérez", 12345678, 20, "Ingeniería", 18, 17, 19, "Ingeniería de Sistemas", "Licenciado");
```

**Salida esperada**
```
-Empleado-
Nombre: Mario
Apellido: Garcia
Cedula de identidad: 4567233
Edad: 34
Cargo: Obrero
Salario: 130Bs.

-Estudiante-
Nombre: Adol
Apellido: Cristin
Cedula de identidad: 30665344
Edad: 18
Curso: Castellano
Notas: 16/13/14
Promedio: 14.3333

-Estudiante universitario
Nombre: Juan
Apellido: Pérez
Cedula de identidad: 12345678
Edad: 20
Curso: Ingeniería
Notas: 18/17/19
Promedio: 18
Carreara: Ingeniería de Sistemas
Grado de formación: Licenciado
```

---

## 📌 Notas
- Se utiliza herencia múltiple en niveles: persona → stu → uni.
- Se demuestra polimorfismo con show_pipol() y sus extensiones en las clases derivadas.
- El uso de new y delete muestra gestión manual de memoria, aunque puede adaptarse a objetos automáticos.