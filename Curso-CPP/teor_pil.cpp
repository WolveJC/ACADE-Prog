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
    per per;
    Cont *foll;
};

per pipol;
Cont *phill = NULL;

// Crear pila
void sozoPhill(Cont *&phill, per per) {
    Cont *novo_dono = new Cont();
    novo_dono->per = per; // Rellenar dato
    novo_dono->foll = phill;
    phill = novo_dono;
    cout << "Datos cargados" << endl;
}

// Sacar pila
void hakaiPhill(Cont *&phill, per &per, string filename) {
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
        cout << "Nombre: " << phill->per.nom << " " << phill->per.ap << endl;
        cout << "Apellido: " << phill->per.ap << endl;
        cout << "Edad: " << phill->per.age << endl;
        cout << "Altura: " << phill->per.alt << endl;
        cout << "Numero asignado: " << phill->per.numper << endl;
        cout << "Numero factorial: " << phill->per.numfact << endl;

        // Guardar en archivo
        arch << "Nombre: " << phill->per.nom << endl;
        arch << "Apellido: " << phill->per.ap << endl;
        arch << "Edad: " << phill->per.age << endl;
        arch << "Altura: " << phill->per.alt << "m" << endl;
        arch << "Numero asignado: " << phill->per.numper << endl;
        arch << "Numero factorial: " << phill->per.numfact << endl;

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
        system("cls");
    } while (res == 's');

    string filename;
    string ext = ".txt";
    cout << "Ingrese el nombre con el que desea guardar el archivo: " << endl;
    cin >> filename;
    filename += ext;
    hakaiPhill(phill, pipol, filename);
    return 0;
}
