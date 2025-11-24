# Proyecto: Cuenta Bancaria 💳

## 📌 Descripción
Este programa en C++ implementa una clase `CuentaBancaria` que permite:
- Crear una cuenta con titular, número de cuenta y saldo inicial.
- Realizar depósitos.
- Realizar retiros con validación de fondos.
- Mostrar información de la cuenta.

---

## ⚙️ Requisitos
- Lenguaje: C++ (versión 11 o superior recomendada)
- Librerías estándar: `<iostream>`, `<string>`

---

## 🚀 Compilación y ejecución
```bash
g++ cuenta.cpp -o cuenta
./cuenta
```

---

## 🧩 Estructura del código

`class CuentaBancaria`
- **Atributos privados:**
  - `titular`: nombre del titular de la cuenta.
  - `numeroCuenta`: número identificador de la cuenta.
  - `saldo`: saldo actual.

- **Constructor:**
  - Inicializa titular, número de cuenta y saldo inicial.

- **Métodos:**
  - `depositar(double monto)`: añade dinero al saldo si el monto es válido.
  - `retirar(double monto)`: descuenta dinero si hay fondos suficientes.
  - `mostrarInformacionCuenta()`: imprime los datos de la cuenta.

`int main()`
- Crea una cuenta bancaria.
- Muestra información inicial.
- Realiza operaciones de depósito y retiro.
- Muestra información final.

---

## 🧪 Ejemplo de uso

**Salida esperada**
```
Información inicial de la cuenta:
Titular de la cuenta: Juan Pérez
Número de cuenta: 123456789
Saldo: $1000

Realizando un depósito de $500...
Depósito exitoso. Nuevo saldo: $1500

Intentando retirar $2000...
Fondos insuficientes o monto inválido.

Retirando $300...
Retiro exitoso. Nuevo saldo: $1200

Información final de la cuenta:
Titular de la cuenta: Juan Pérez
Número de cuenta: 123456789
Saldo: $1200
```

---

## 📌 Notas
- Añadir validación para saldo inicial (no permitir valores negativos).  
- Usar iomanip para mostrar el saldo con dos decimales.  
- Implementar métodos get y set para mayor encapsulación.  
- Manejar múltiples cuentas en un vector o lista.  
- Añadir autenticación o PIN para operaciones seguras.  
- Este programa es un ejemplo básico de POO en C++.  
- Demuestra encapsulación (atributos privados), constructores y métodos públicos.  
- Puede servir como base para sistemas más complejos de gestión bancaria.  
- En aplicaciones reales se requeriría manejo de errores más robusto, persistencia en base de datos y seguridad.  