#include <iostream>
#include <vector>
#include <string>
using namespace std;

// Definición de la clase Producto
class Producto {
private:
    string nombre;
    int cantidad;
    double precio;

public:
    // Constructor
    Producto(string nombre, int cantidad, double precio) {
        this->nombre = nombre;
        this->cantidad = cantidad;
        this->precio = precio;
    }

    // Métodos para obtener información
    string getNombre() {
        return nombre;
    }

    int getCantidad() {
        return cantidad;
    }

    double getPrecio() {
        return precio;
    }

    // Método para actualizar la cantidad
    void actualizarCantidad(int nuevaCantidad) {
        cantidad = nuevaCantidad;
    }

    // Mostrar información del producto
    void mostrarInformacion() {
        cout << "Producto: " << nombre << endl;
        cout << "Cantidad: " << cantidad << endl;
        cout << "Precio: $" << precio << endl;
    }
};

// Función para mostrar el menú principal
void mostrarMenu() {
    cout << "\n=== Menú ===" << endl;
    cout << "1. Agregar producto" << endl;
    cout << "2. Mostrar inventario" << endl;
    cout << "3. Actualizar cantidad de un producto" << endl;
    cout << "4. Salir" << endl;
    cout << "Seleccione una opción: ";
}

int main() {
    vector<Producto> inventario; // Lista de productos
    int opcion;

    do {
        mostrarMenu();
        cin >> opcion;

        switch (opcion) {
            case 1: {
                // Agregar un producto
                string nombre;
                int cantidad;
                double precio;

                cout << "\nIngrese el nombre del producto: ";
                cin >> nombre;
                cout << "Ingrese la cantidad: ";
                cin >> cantidad;
                cout << "Ingrese el precio: ";
                cin >> precio;

                Producto nuevoProducto(nombre, cantidad, precio);
                inventario.push_back(nuevoProducto);
                cout << "Producto agregado exitosamente." << endl;
                break;
            }

            case 2: {
                // Mostrar el inventario
                cout << "\n=== Inventario ===" << endl;
                for (size_t i = 0; i < inventario.size(); ++i) {
                    cout << "Producto " << i + 1 << ":" << endl;
                    inventario[i].mostrarInformacion();
                    cout << "------------------" << endl;
                }
                break;
            }

            case 3: {
                // Actualizar cantidad de un producto
                string nombre;
                int nuevaCantidad;

                cout << "\nIngrese el nombre del producto a actualizar: ";
                cin >> nombre;

                bool encontrado = false;
                for (size_t i = 0; i < inventario.size(); ++i) {
                    if (inventario[i].getNombre() == nombre) {
                        cout << "Ingrese la nueva cantidad: ";
                        cin >> nuevaCantidad;
                        inventario[i].actualizarCantidad(nuevaCantidad);
                        cout << "Cantidad actualizada exitosamente." << endl;
                        encontrado = true;
                        break;
                    }
                }

                if (!encontrado) {
                    cout << "Producto no encontrado en el inventario." << endl;
                }
                break;
            }

            case 4:
                cout << "Saliendo del programa..." << endl;
                break;

            default:
                cout << "Opción inválida. Intente de nuevo." << endl;
                break;
        }
    } while (opcion != 4);

    return 0;
}