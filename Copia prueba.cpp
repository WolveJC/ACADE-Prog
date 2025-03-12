#include <iostream>
#include <fstream>
#include <stack>
#include <queue>
#include <string>

using namespace std;

struct Producto {
    string nombre;
    int cantidad;
    float precio;
    bool disponible; // true si está disponible, false si está en espera
};

// Funciones
void agregarProducto(stack<Producto>& pila, queue<Producto>& cola);
void mostrarProductos(const stack<Producto>& pila, const queue<Producto>& cola);
void guardarProductos(const stack<Producto>& pila, const queue<Producto>& cola);

int main() {
    stack<Producto> pilaProductos;
    queue<Producto> colaProductos;

    int opcion;
    do {
        cout << "1. Agregar producto\n";
        cout << "2. Mostrar productos\n";
        cout << "3. Guardar productos\n";
        cout << "4. Salir\n";
        cout << "Seleccione una opción: ";
        cin >> opcion;

        switch (opcion) {
            case 1:
                agregarProducto(pilaProductos, colaProductos);
                break;
            case 2:
                mostrarProductos(pilaProductos, colaProductos);
                break;
            case 3:
                guardarProductos(pilaProductos, colaProductos);
                break;
            case 4:
                cout << "Saliendo del programa...\n";
                break;
            default:
                cout << "Opción no válida. Intente de nuevo.\n";
        }
    } while (opcion != 4);

    return 0;
}

void agregarProducto(stack<Producto>& pila, queue<Producto>& cola) {
    Producto nuevoProducto;
    cout << "Nombre del producto: ";
    cin.ignore(); // Limpiar el buffer
    getline(cin, nuevoProducto.nombre);
    cout << "Cantidad del producto: ";
    cin >> nuevoProducto.cantidad;
    cout << "Precio del producto: ";
    cin >> nuevoProducto.precio;
    cout << "¿Está disponible? (1: Sí, 0: No): ";
    cin >> nuevoProducto.disponible;

    if (nuevoProducto.disponible) {
        cola.push(nuevoProducto);
    } else {
        pila.push(nuevoProducto);
    }
}

void mostrarProductos(const stack<Producto>& pila, const queue<Producto>& cola) {
    cout << "\nProductos en Espera:\n";
    stack<Producto> pilaTemporal = pila; // Copia de la pila para mostrar
    while (!pilaTemporal.empty()) {
        Producto p = pilaTemporal.top();
        cout << "- " << p.nombre << ", Cantidad: " << p.cantidad << ", Precio: $" << p.precio << endl;
        pilaTemporal.pop();
    }

    cout << "\nProductos Disponibles:\n";
    queue<Producto> colaTemporal = cola; // Copia de la cola para mostrar
    while (!colaTemporal.empty()) {
        Producto p = colaTemporal.front();
        cout << "- " << p.nombre << ", Cantidad: " << p.cantidad << ", Precio: $" << p.precio << endl;
        colaTemporal.pop();
    }
    cout << endl;
}

void guardarProductos(const stack<Producto>& pila, const queue<Producto>& cola) {
    ofstream archivo("productos.txt");
    if (!archivo) {
        cerr << "Error al abrir el archivo para guardar.\n";
        return;
    }

    // Guardar productos en espera
    stack<Producto> pilaTemporal = pila;
    while (!pilaTemporal.empty()) {
        Producto p = pilaTemporal.top();
        archivo << "0 " << p.nombre << " " << p.cantidad << " " << p.precio << endl; // 0 para en espera
        pilaTemporal.pop();
    }

    // Guardar productos disponibles
    queue<Producto> colaTemporal = cola;
    while (!colaTemporal.empty()) {
        Producto p = colaTemporal.front();
        archivo << "1 " << p.nombre << " " << p.cantidad << " " << p.precio << endl; // 1 para disponible
        colaTemporal.pop();
    }

    archivo.close();
    cout << "Productos guardados exitosamente.\n";
}