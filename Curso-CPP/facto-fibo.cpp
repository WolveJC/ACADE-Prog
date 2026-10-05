#include <iostream>
#include <string>
#include <stack>
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

    string fibonacci(int n) {
        if (n < 0) return "Numero no valido.";
        int a = 0, b = 1;
        string serie;
        for (int i = 0; i < n; ++i) {
            serie += to_string(a) + " ";
            int next = a + b;
            a = b;
            b = next;
        }
        return serie;
    }

    bool numeromagico(int n) {
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
    stack<Usuario> in;
    string usu;
    int op;

    cout << "Ingrese su nombre: " << endl;
    cin >> usu;

    do {
        cout << "\n--- Menu ---\n";
        cout << "1. Calcular factorial de un numero\n";
        cout << "2. Mostrar la serie Fibonacci hasta un numero\n";
        cout << "3. Verificar si un numero es magico\n";
        cout << "4. Mostrar numeros y resultados guardados\n";
        cout << "5. Salir\n";
        cout << "Seleccione una opcion: " << endl;
        cin >> op;
        Usuario cu;
        cu.name = usu;

        switch (op) {
            case 1: {
                cout << "Ingresa un numero: " << endl;
                cin >> cu.numero;
                long long fact = cal.factorial(cu.numero);
                if (fact != -1) {
                    cu.resultado = "Factorial = " + to_string(fact);
                    cout << "El factorial de " << cu.numero << " es " << fact << endl;
                } else {
                    cu.resultado = "Factorial no definido (numero negativo)";
                    cout << "El factorial no esta definido para numeros negativos" << endl;
                }
                in.push(cu);
                break;
            }
            case 2: {
                cout << "Ingrese un numero: " << endl;
                cin >> cu.numero;
                cu.resultado = "Fibonacci = " + cal.fibonacci(cu.numero);
                cout << "Serie Fibonacci hasta " << cu.numero << ": " << cu.resultado << endl;
                in.push(cu);
                break;
            }
            case 3: {
                cout << "Ingrese un numero:" << endl;
                cin >> cu.numero;
                if (cal.numeromagico(cu.numero)) {
                    cu.resultado = "Es un numero magico";
                    cout << cu.numero << " es un numero magico." << endl;
                } else {
                    cu.resultado = "No es un numero magico";
                    cout << cu.numero << " no es un numero magico." << endl;
                }
                in.push(cu);
                break;
            }
            case 4: {
                cout << "Numeros y resultados guardados: " << endl;
                if (in.empty()) {
                    cout << "No hay nada" << endl;
                } else {
                    stack<Usuario> temp = in;
                    while (!temp.empty()) {
                        Usuario u = temp.top();
                        cout << "Usuario: " << u.name 
                             << ", Numero: " << u.numero 
                             << ", Resultado: " << u.resultado << endl;
                        temp.pop();
                    }
                }
                break;
            }
            case 5:
                cout << "Saliendo..." << endl;
                break;
            default:
                cout << "Opcion no valida" << endl;
        }
        cout << endl;

    } while (op != 5);

    return 0;
}