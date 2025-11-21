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
            cout << "Número no válido." << endl;
            return;
        }
        long long a = 0, b = 1;
        cout << "Serie Fibonacci hasta " << n << ": ";
        for (int i = 0; i < n; ++i) {
            cout << a << " ";
            long long next = a + b;
            a = b;
            b = next;
        }
        cout << endl;
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
};

int main() {
    Calculadora cal;
    stack<Usuario> historial;
    string usu;
    int op;

    cout << "Ingrese su nombre: ";
    cin >> usu;

    do {
        cout << "\n--- MENU ---\n";
        cout << "1. Calcular factorial\n";
        cout << "2. Mostrar serie Fibonacci\n";
        cout << "3. Verificar número mágico\n";
        cout << "4. Mostrar números guardados\n";
        cout << "5. Salir\n";
        cout << "Seleccione una opción: ";
        cin >> op;

        Usuario cu;
        cu.name = usu;

        switch (op) {
            case 1:
                cout << "Ingrese un número: ";
                cin >> cu.numero;
                {
                    long long fact = cal.factorial(cu.numero);
                    if (fact != -1)
                        cout << "El factorial de " << cu.numero << " es " << fact << endl;
                    else
                        cout << "El factorial no está definido para números negativos." << endl;
                }
                historial.push(cu);
                break;

            case 2:
                cout << "Ingrese un número: ";
                cin >> cu.numero;
                cal.fibonacci(cu.numero);
                historial.push(cu);
                break;

            case 3:
                cout << "Ingrese un número: ";
                cin >> cu.numero;
                if (cal.numeroMagico(cu.numero))
                    cout << cu.numero << " es un número mágico." << endl;
                else
                    cout << cu.numero << " no es un número mágico." << endl;
                historial.push(cu);
                break;

            case 4:
                cout << "Historial de números:\n";
                if (historial.empty()) {
                    cout << "No hay números guardados.\n";
                } else {
                    stack<Usuario> temp = historial;
                    while (!temp.empty()) {
                        Usuario u = temp.top();
                        cout << "Usuario: " << u.name << ", Número: " << u.numero << endl;
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