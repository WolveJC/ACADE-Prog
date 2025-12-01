#include <iostream>
#include <fstream>
#include <stdlib.h>
using namespace std;

struct per {
    string nom;
    string ap;
    int age;
    float alt;
    int numper;
    int numfact;
};

struct Cont {
    per pipol;   // ahora el miembro se llama pipol
    Cont *foll;
};

per pipol;
Cont *phill = NULL;

// Crear pila
void sozoPhill(Cont *&phill, per p) {
    Cont *novo_dono = new Cont();
    novo_dono->pipol = p; // Rellenar dato
    novo_dono->foll = phill;
    phill = novo_dono;
    cout << "Datos cargados" << endl;
}

// Sacar pila
void hakaiPhill(Cont *&phill, per &p, string filename) {
    char r;
    if (phill == NULL) {
        cout << "La pila está vacía." << endl;
        return;
    }
    fstream arch;
    arch.open(filename.c_str(), ios::out);
    if (arch.fail()) {
        cout << "* ERROR GENERANDO ARCHIVO *" << endl;
        return;
    }

    while (phill != NULL) {
        cout << "Nombre: " << phill->pipol.nom << " " << phill->pipol.ap << endl;
        cout << "Apellido: " << phill->pipol.ap << endl;
        cout << "Edad: " << phill->pipol.age << endl;
        cout << "Altura: " << phill->pipol.alt << endl;
        cout << "Numero asignado: " << phill->pipol.numper << endl;
        cout << "Numero factorial: " << phill->pipol.numfact << endl;

        // Guardar en archivo
        arch << "Nombre: " << phill->pipol.nom << endl;
        arch << "Apellido: " << phill->pipol.ap << endl;
        arch << "Edad: " << phill->pipol.age << endl;
        arch << "Altura: " << phill->pipol.alt << "m" << endl;
        arch << "Numero asignado: " << phill->pipol.numper << endl;
        arch << "Numero factorial: " << phill->pipol.numfact << endl;

        Cont *axil = phill;
        phill = phill->foll;
        delete axil;

        cout << "¿Sacar siguiente dato? (s/n)" << endl;
        cin >> r;
        if (r == 'n') {
            break;
        }
    }
    arch.close();
}

// Función para calcular el factorial
int facto(int n) {
    if (n < 0) return -1;
    int fact = 1;
    for (int a = 1; a <= n; a++) {
        fact *= a;
    }
    return fact;
}

int main() {
    char res;
    do {
        cout << "Ingrese nombre de la persona: " << endl;
        cin >> pipol.nom;
        cout << "Ingrese apellido de la persona: " << endl;
        cin >> pipol.ap;
        cout << "Ingrese edad de la persona: " << endl;
        cin >> pipol.age;
        cout << "Ingrese altura de la persona: " << endl;
        cin >> pipol.alt;
        cout << "Ingrese numero para la persona: " << endl;
        cin >> pipol.numper;
        pipol.numfact = facto(pipol.numper);

        sozoPhill(phill, pipol);
        cout << "Debe ingresar más datos? (s/n)" << endl;
        cin >> res;
        cout << string(20, '\n'); // limpiar pantalla portable
    } while (res == 's');

    string filename;
    string ext = ".txt";
    cout << "Ingrese el nombre con el que desea guardar el archivo: " << endl;
    cin >> filename;
    filename += ext;
    hakaiPhill(phill, pipol, filename);
    return 0;
}