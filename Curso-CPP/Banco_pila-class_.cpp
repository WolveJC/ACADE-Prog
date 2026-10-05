#include <iostream>
#include <string>
#include <stack>
#include <fstream>
using namespace std;

class Persona {
public:
    string nombre;
    string apellido;
    int edad;
    int cedula;
    int telefono;

    Persona() {} // Constructor por defecto

    Persona(string nom, string ape, int _edad, int ci, int tel) {
        nombre = nom;
        apellido = ape;
        edad = _edad;
        cedula = ci;
        telefono = tel;
    }
};

class Banco {
private:
    stack<Persona> personas;

public:
    void registrarPersona() {
        string nombre, apellido;
        int edad, cedula, telefono;

        cin.ignore(numeric_limits<streamsize>::max(), '\n'); // limpiar buffer
        cout << "Ingrese el Nombre: ";
        getline(cin, nombre);
        cout << "Ingrese el Apellido: ";
        getline(cin, apellido);
        cout << "Ingrese la edad: ";
        cin >> edad;
        while (edad <= 0) {
            cout << "Edad inválida. Ingrese nuevamente: ";
            cin >> edad;
        }
        cout << "Ingrese la cédula: ";
        cin >> cedula;
        cout << "Ingrese el número de teléfono: ";
        cin >> telefono;

        Persona nueva(nombre, apellido, edad, cedula, telefono);
        personas.push(nueva);
        cout << "Persona registrada.\n";
    }

    void mostrarPersonas() {
        if (personas.empty()) {
            cout << "No hay personas registradas.\n";
            return;
        }
        stack<Persona> temp = personas;
        cout << "\n--- Personas registradas ---\n";
        while (!temp.empty()) {
            Persona p = temp.top();
            cout << "Nombre: " << p.nombre
                 << ", Apellido: " << p.apellido
                 << ", Edad: " << p.edad
                 << ", Cédula: " << p.cedula
                 << ", Teléfono: " << p.telefono << "\n";
            temp.pop();
        }
    }

    void guardarEnArchivo(const string& nombreArchivo) {
        ofstream archivo(nombreArchivo);
        if (!archivo) {
            cerr << "Error al abrir archivo.\n";
            return;
        }
        stack<Persona> temp = personas;
        while (!temp.empty()) {
            Persona p = temp.top();
            archivo << p.nombre << " " << p.apellido << " "
                    << p.edad << " " << p.cedula << " " << p.telefono << "\n";
            temp.pop();
        }
        archivo.close();
        cout << "Datos guardados en " << nombreArchivo << endl;
    }
};

int main() {
    Banco banco;
    int op;

    do {
        cout << "\n--- Menu ---\n";
        cout << "1. Registrar persona\n";
        cout << "2. Mostrar personas registradas\n";
        cout << "3. Guardar en archivo\n";
        cout << "4. Salir\n";
        cout << "Seleccione una opción: ";
        cin >> op;

        switch (op) {
            case 1:
                banco.registrarPersona();
                break;
            case 2:
                banco.mostrarPersonas();
                break;
            case 3: {
                string archivo;
                cout << "Ingrese nombre del archivo (ej. banco.txt): ";
                cin >> archivo;
                banco.guardarEnArchivo(archivo);
                break;
            }
            case 4:
                cout << "Saliendo...\n";
                break;
            default:
                cout << "Opción inválida.\n";
        }
    } while (op != 4);

    return 0;
}