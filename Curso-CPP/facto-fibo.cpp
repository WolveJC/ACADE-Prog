#include <iostream>
#include <string>
#include <stack>
#include <limits>
using namespace std;

class Calculadora {
public:
    long long factorial(int n) {
        if (n < 0) return -1;
        long long resultado = 1;
        for (int i = 1; i <= n; ++i) {
            resultado *= i;
        }
        return resultado;
    }

    void fibonacci(int n) {
        if (n < 0) {
            cout << "Numero no valido." << endl;
            return;
        }
        int a = 0, b = 1;
        cout << "Serie Fibonacci hasta " << n << ": ";
        for (int i = 0; i < n; ++i) {
            cout << a << " ";
            int next = a + b;
            a = b;
            b = next;
        }
        return serie;
    }

    bool numeroMagico(int n) {
        while (n >= 10) {
            int sum = 0;
            while (n > 0) {
                sum += n % 10;
                n /= 10;
            }
            n = sum;
        }
        return n == 1;
    }
};

struct Usuario {
    string name;
    int numero;
    string resultado; // Nuevo campo para guardar el resultado
};

int main() {
    Calculadora cal;
    stack<Usuario> historial;
    string usu;
    int op;

    cout << "Ingrese su nombre: ";
    cin >> usu;

    do {
        cout << "\n--- Menu ---\n";
        cout << "1. Calcular factorial de un numero\n";
        cout << "2. Mostrar la serie Fibonacci hasta un numero\n";
        cout << "3. Verificar si un numero es magico\n";
        cout << "4. Mostrar numeros guardados\n";
        cout << "5. Salir\n";
        cout << "Seleccione una opción: ";
        cin >> op;

        Usuario cu;
        cu.name = usu;

        switch (op) {
            case 1:
                cout << "Ingresa un numero: " << endl;
                cin >> cu.numero;
                long long fact = cal.factorial(cu.numero);
                if (fact != -1) {
                    cout << "El factorial de " << cu.numero << " es " << fact << endl;
                } else {
                    cout << "El factorial no esta definido para estos numeros negativos" << endl;
                }
                historial.push(cu);
                break;
            case 2:
                cout << "Ingrese un numero: " << endl;
                cin >> cu.numero;
                cal.fibonacci(cu.numero);
                in.push(cu);
                break;
            case 3:
                cout << "Ingrese un numero:" << endl;
                cin >> cu.numero;
                if (cal.numeromagico(cu.numero)) {
                    cout << cu.numero << " es un numero magico." << endl;
                } else {
                    cout << cu.numero << " no es un numero magico." << endl;
                }
                in.push(cu);
                break;
            case 4:
                cout << "Numeros guardados: " << endl;
                if (in.empty()) {
                    cout << "No hay nada" << endl;
                } else {
                    stack<Usuario> temp = historial;
                    while (!temp.empty()) {
                        Usuario u = temp.top();
                        cout << "Usuario: " << u.name << ", Numero: " << u.numero << endl;
                        temp.pop();
                    }
                }
                break;
            case 5:
                cout << "Saliendo...\n";
                break;

            default:
                cout << "Opción no válida.\n";
        }
    } while (op != 5);

    return 0;
}