#include <iostream>
#include <cmath>   // <math.h> también funciona, pero <cmath> es más estándar
using namespace std;

// Prototipos de funciones
void fun1(int a, int n);
void fun2(int c);

int main()
{
    int a, n, c;

    cout << "Introduce el número para realizar la potencia: ";
    cin >> a;
    cout << "Introduce el exponente: ";
    cin >> n;

    fun1(a, n);  // llamada a pow

    cout << "Introduce un número para calcular su raíz cuadrada: ";
    cin >> c;

    fun2(c);     // llamada a sqrt

    return 0;
}

// Función para potencia
void fun1(int a, int n)
{
    int pot = pow(a, n);
    cout << "El resultado de " << a << "^" << n << " es: " << pot << endl;
}

// Función para raíz cuadrada
void fun2(int c)
{
    double rad = sqrt(c);
    cout << "La raíz cuadrada de " << c << " es: " << rad << endl;
}