#include <iostream>
#include <queue>   // STL queue
#include <string>
using namespace std;

int main() {
    queue<char> cola;  // cola de caracteres
    int op;
    char dato;

    do {
        cout << "\n--- Menu ---\n";
        cout << "1. Insertar\n";
        cout << "2. Mostrar\n";
        cout << "3. Salir\n";
        cout << "Seleccione una opción: ";
        cin >> op;

        switch (op) {
            case 1:
                cout << "Ingresa un caracter: ";
                cin >> dato;
                cola.push(dato);  // insertar en la cola
                break;
            case 2:
                if (cola.empty()) {
                    cout << "La cola está vacía.\n";
                } else {
                    cout << "Mostrando elementos de la cola: ";
                    while (!cola.empty()) {
                        char x = cola.front();  // primer elemento
                        cola.pop();             // eliminarlo
                        if (!cola.empty()) {
                            cout << x << ", ";
                        } else {
                            cout << x << "." << endl;
                        }
                    }
                }
                break;
            case 3:
                cout << "Saliendo...\n";
                break;
            default:
                cout << "Opción inválida.\n";
        }
    } while (op != 3);

    return 0;
}