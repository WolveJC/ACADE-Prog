#include <iostream>
#include <stack>
#include <string>
#include <fstream>
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
        cout << "Nombre: " << nombre << ", edad: " << edad << endl;
    }
};

void fichero(stack<Persona>& pila) {
    ofstream archivo("Personas.txt");
    if (archivo.is_open()) {
        stack<Persona> copia = pila;
        while (!copia.empty()) {
            Persona p = copia.top();
            archivo << p.getNombre() << "," << p.getEdad() << endl; // Corrección aquí
            copia.pop();
        }
        archivo.close();
        cout << "Datos guardados en personas.txt" << endl;
    } else {
        cout << "No se pudo generar el archivo" << endl;
    }
}

int main() {
    stack<Persona> pila;
    int cantidad;

    cout << "¿Cuantas personas deseas ingresar? ";
    cin >> cantidad;

    for (int i = 0; i < cantidad; ++i) {
        string nombre;
        int edad;

        cout << "Ingrese el nombre de la persona " << (i + 1) << ": ";
        cin >> nombre;
        cout << "Ingrese la edad de " << nombre << ": ";
        cin >> edad;

        pila.push(Persona(nombre, edad));
    }
    cout << "Personas guardadas en pila: " << endl;
    stack<Persona> copia = pila;
    while (!copia.empty()) {
        copia.top().mostrarinfo();
        copia.pop();
    }
    fichero(pila);

    return 0;
}