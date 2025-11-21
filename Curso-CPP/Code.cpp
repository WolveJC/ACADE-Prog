#include <iostream>
#include <fstream>
#include <string>
using namespace std;

struct Estudiante {
    string nombre;
    int edad;
    int ci;
    int nota;
};

struct Nodo {
    Estudiante estu;
    Nodo* siguiente;
};

void ingresarPila(Nodo*& pila, const Estudiante& estu) {
    Nodo* nuevo = new Nodo();
    nuevo->estu = estu;
    nuevo->siguiente = pila;
    pila = nuevo;
    cout << "Estudiante agregado a la pila.\n";
}

bool sacarPila(Nodo*& pila, Estudiante& estu) {
    if (pila == nullptr) return false;
    Nodo* aux = pila;
    estu = aux->estu;
    pila = aux->siguiente;
    delete aux;
    return true;
}

int main() {
    Nodo* pila = nullptr;
    Estudiante estu;
    string rep;
    string nombreArchivo;

    cout << "Ingrese nombre del archivo de salida (con extensión, ej. estudiantes.txt): ";
    cin >> nombreArchivo;
    ofstream archivo(nombreArchivo, ios::app);
    if (!archivo) {
        cerr << "Error al abrir archivo.\n";
        return 1;
    }

    do {
        cout << "Ingrese el nombre del alumno: ";
        cin >> estu.nombre;
        cout << "Ingrese la edad del alumno: ";
        cin >> estu.edad;
        while (estu.edad <= 0) {
            cout << "Edad inválida. Ingrese nuevamente: ";
            cin >> estu.edad;
        }
        cout << "Ingrese la cédula del alumno: ";
        cin >> estu.ci;
        cout << "Ingrese la calificación del alumno (0-20): ";
        cin >> estu.nota;
        while (estu.nota < 0 || estu.nota > 20) {
            cout << "Nota inválida. Ingrese nuevamente (0-20): ";
            cin >> estu.nota;
        }

        ingresarPila(pila, estu);

        cout << "¿Desea agregar más alumnos al sistema? (s/n): ";
        cin >> rep;
    } while (rep == "s");

    cout << "\n--- Extrayendo estudiantes de la pila ---\n";
    while (sacarPila(pila, estu)) {
        cout << "Nombre: " << estu.nombre << endl;
        cout << "Edad: " << estu.edad << endl;
        cout << "Cédula: " << estu.ci << endl;
        cout << "Calificación: " << estu.nota << endl;
        cout << "-----------\n";

        archivo << "Nombre: " << estu.nombre << endl;
        archivo << "Edad: " << estu.edad << endl;
        archivo << "Cédula: " << estu.ci << endl;
        archivo << "Calificación: " << estu.nota << endl;
        archivo << "-----------\n";
    }

    archivo.close();
    cout << "Datos guardados en " << nombreArchivo << endl;
    return 0;
}