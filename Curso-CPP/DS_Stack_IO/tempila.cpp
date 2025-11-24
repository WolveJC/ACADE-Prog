#include <iostream>
#include <fstream>
#include <string>
using namespace std;

struct Tiempo {
    int semanas, dias, horas;
    long long segundos;
};

struct Persona {
    string nom, curso;
    int ci;
};

struct Nodo {
    Persona per;
    Tiempo tem;
    Nodo* siguiente;
};

void calcularSegundos(Tiempo& t) {
    int diasTotales = t.semanas * 7 + t.dias;
    int horasTotales = diasTotales * 24 + t.horas;
    t.segundos = static_cast<long long>(horasTotales) * 3600;
}

void ingresarPila(Nodo*& pila, const Persona& p, const Tiempo& t) {
    Nodo* nuevo = new Nodo();
    nuevo->per = p;
    nuevo->tem = t;
    nuevo->siguiente = pila;
    pila = nuevo;
    cout << "Estudiante agregado a la pila.\n";
}

bool sacarPila(Nodo*& pila, Persona& p, Tiempo& t) {
    if (pila == nullptr) return false;
    Nodo* aux = pila;
    p = aux->per;
    t = aux->tem;
    pila = aux->siguiente;
    delete aux;
    return true;
}

int main() {
    Persona per;
    Tiempo tem;
    Nodo* pila = nullptr;
    string nombreArchivo;

    cout << "Bienvenido\n";
    cout << "Ingrese su nombre: ";
    getline(cin, per.nom);
    cout << "Ingrese su cédula: ";
    cin >> per.ci;
    cout << "Ingrese la materia que desea cursar: ";
    cin >> per.curso;
    cout << "Ingrese cuántas semanas cursará: ";
    cin >> tem.semanas;
    while (tem.semanas < 0) { cout << "Valor inválido. Ingrese semanas >= 0: "; cin >> tem.semanas; }
    cout << "Ingrese los días adicionales: ";
    cin >> tem.dias;
    while (tem.dias < 0) { cout << "Valor inválido. Ingrese días >= 0: "; cin >> tem.dias; }
    cout << "Ingrese las horas adicionales: ";
    cin >> tem.horas;
    while (tem.horas < 0) { cout << "Valor inválido. Ingrese horas >= 0: "; cin >> tem.horas; }

    calcularSegundos(tem);
    ingresarPila(pila, per, tem);

    cout << "Ingrese el nombre del archivo de salida (ej. curso.txt): ";
    cin >> nombreArchivo;
    ofstream archivo(nombreArchivo);
    if (!archivo) {
        cerr << "Error al abrir archivo.\n";
        return 1;
    }

    cout << "\n--- Extrayendo datos de la pila ---\n";
    while (sacarPila(pila, per, tem)) {
        cout << "Nombre: " << per.nom << endl;
        cout << "Cédula: " << per.ci << endl;
        cout << "Curso: " << per.curso << endl;
        cout << "Semanas: " << tem.semanas << endl;
        cout << "Días: " << tem.dias << endl;
        cout << "Horas: " << tem.horas << endl;
        cout << "Tiempo total en segundos: " << tem.segundos << endl;
        cout << "-----------\n";

        archivo << "Nombre: " << per.nom << endl;
        archivo << "Cédula: " << per.ci << endl;
        archivo << "Curso: " << per.curso << endl;
        archivo << "Semanas: " << tem.semanas << endl;
        archivo << "Días: " << tem.dias << endl;
        archivo << "Horas: " << tem.horas << endl;
        archivo << "Tiempo total en segundos: " << tem.segundos << endl;
        archivo << "-----------\n";
    }

    archivo.close();
    cout << "Datos guardados en " << nombreArchivo << endl;
    return 0;
}