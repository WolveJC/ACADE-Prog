#include <iostream>
#include <stack>
#include <string>
#include <fstream>
#include <limits> // Necesario para limpiar el búfer

using namespace std;

class Persona {
private:
    string nombre;
    int edad;
public:
    Persona(string n, int e) {
        nombre = n;
        edad = e;
    }
    void setNombre(string n) {
        nombre = n;
    }
    void setEdad(int e) {
        edad = e;
    }
    string getNombre() const {
        return nombre;
    }
    int getEdad() const {
        return edad;
    }
    void mostrarinfo() const {
        cout << "Nombre: " << nombre << ", Edad: " << edad << endl;
    }
};

void fichero(stack<Persona>& pila) {
    ofstream archivo("Personas.txt");
    if (archivo.is_open()) {
        stack<Persona> copia = pila;
        while (!copia.empty()) {
            Persona p = copia.top();
            archivo << p.getNombre() << "," << p.getEdad() << endl;
            copia.pop();
        }
        archivo.close();
        cout << "\n[Exito] Datos guardados en Personas.txt" << endl;
    } else {
        cout << "\n[Error] No se pudo generar el archivo." << endl;
    }
}

int main() {
    stack<Persona> pila;
    int cantidad;

    cout << "¿Cuantas personas deseas ingresar? ";
    while (!(cin >> cantidad) || cantidad <= 0) {
        cout << "Por favor, ingrese un numero valido mayor a 0: ";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }

    // Limpiar el salto de línea pendiente en el búfer después de leer la cantidad
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    for (int i = 0; i < cantidad; ++i) {
        string nombre;
        int edad;

        cout << "\nIngrese el nombre completo de la persona " << (i + 1) << ": ";
        getline(cin, nombre); // Permite espacios en el nombre (ej. Juan Perez)

        cout << "Ingrese la edad de " << nombre << ": ";
        while (!(cin >> edad) || edad < 0) {
            cout << "Edad invalida. Ingrese una edad correcta: ";
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
        }

        // Limpiar el búfer después de leer la edad numérica
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        pila.push(Persona(nombre, edad));
    }

    cout << "\n--- Personas guardadas en la pila ---" << endl;
    stack<Persona> copia = pila;
    while (!copia.empty()) {
        copia.top().mostrarinfo();
        copia.pop();
    }

    // Guardar en archivo de texto
    fichero(pila);

    return 0;
}
