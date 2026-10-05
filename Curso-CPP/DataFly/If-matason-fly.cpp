#include <iostream>
#include <fstream>
using namespace std;

struct Fly {
    int code;   // Código del vuelo
    float km;   // Kilómetros recorridos
    int num;    // Número de pasajeros
};

// Genera archivo con el recorrido del vuelo con más pasajeros
void reciboPasajeros(float km) {
    string filename;
    cout << "Ingrese el nombre para guardar el archivo del vuelo con más pasajeros: ";
    cin >> filename;
    filename += ".txt";

    ofstream recibo(filename);
    if (!recibo) {
        cout << "* ERROR GENERANDO RECIBO *" << endl;
        return;
    }
    recibo << "El vuelo con más pasajeros recorrió: " << km << " km" << endl;
    cout << "Archivo generado: " << filename << endl;
}

// Genera archivo con el código del vuelo con mayor recorrido
void reciboKilometros(int code) {
    string filename;
    cout << "Ingrese el nombre para guardar el archivo del vuelo con mayor recorrido: ";
    cin >> filename;
    filename += ".txt";

    ofstream recibo(filename);
    if (!recibo) {
        cout << "* ERROR GENERANDO RECIBO *" << endl;
        return;
    }
    recibo << "El vuelo con mayor recorrido tiene el código: " << code << endl;
    cout << "Archivo generado: " << filename << endl;
}

int main() {
    const int N = 5; // número de vuelos
    Fly vuelos[N];

    // Entrada de datos
    for (int i = 0; i < N; i++) {
        cout << "Ingrese código del vuelo " << i+1 << ": ";
        cin >> vuelos[i].code;
        cout << "Ingrese número de pasajeros del vuelo " << i+1 << ": ";
        cin >> vuelos[i].num;
        cout << "Ingrese kilómetros del vuelo " << i+1 << ": ";
        cin >> vuelos[i].km;
    }

    // Buscar vuelo con mayor recorrido
    int idxMaxKm = 0;
    for (int i = 1; i < N; i++) {
        if (vuelos[i].km > vuelos[idxMaxKm].km) {
            idxMaxKm = i;
        }
    }
    reciboKilometros(vuelos[idxMaxKm].code);

    // Buscar vuelo con mayor número de pasajeros
    int idxMaxPasajeros = 0;
    for (int i = 1; i < N; i++) {
        if (vuelos[i].num > vuelos[idxMaxPasajeros].num) {
            idxMaxPasajeros = i;
        }
    }
    reciboPasajeros(vuelos[idxMaxPasajeros].km);

    return 0;
}