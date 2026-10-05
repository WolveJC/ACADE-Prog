#include <iostream>
#include <string>
using namespace std;

class Persona {
private:
    string nombre;
    int edad;

public:
    // Método set para asignar el nombre
    void setNombre(string nuevoNombre) {
        if (!nuevoNombre.empty()) {
            nombre = nuevoNombre;
        } else {
            cout << "Error: El nombre no puede estar vacío." << endl;
        }
    }

    // Método get para obtener el nombre
    string getNombre() {
        return nombre;
    }

    // Método set para asignar la edad
    void setEdad(int nuevaEdad) {
        if (nuevaEdad > 0) {
            edad = nuevaEdad;
        } else {
            cout << "Error: La edad debe ser mayor a 0." << endl;
        }
    }

    // Método get para obtener la edad
    int getEdad() {
        return edad;
    }

    // Método para mostrar información de la persona
    void mostrarInformacion() {
        cout << "Nombre: " << nombre << ", Edad: " << edad << endl;
    }
};

int main() {
    Persona persona;
    string nombre;
    int edad;

    // Solicitar al usuario que ingrese los datos
    cout << "Ingrese el nombre de la persona: ";
    getline(cin, nombre); // Leer una línea completa para el nombre
    persona.setNombre(nombre); // Usar el método set para asignar el nombre

    cout << "Ingrese la edad de la persona: ";
    cin >> edad; // Leer la edad
    persona.setEdad(edad); // Usar el método set para asignar la edad

    // Mostrar la información ingresada
    cout << "\nInformación ingresada:" << endl;
    persona.mostrarInformacion();

    return 0;
}