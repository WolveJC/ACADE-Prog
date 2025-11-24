#include <iostream>
#include <fstream>
#include <string>
using namespace std;

struct Registro {
    string nombre;
    string curso;
    int ci;
};

// Función que calcula duración total del curso
void resolver(int semanas, int diasExtra, int horasExtra) {
    int diasTotales = semanas * 7 + diasExtra;
    int horasTotales = diasTotales * 24 + horasExtra;
    long long segundosTotales = static_cast<long long>(horasTotales) * 3600;

    cout << "\n--- Duración del curso ---\n";
    cout << "Días totales: " << diasTotales << endl;
    cout << "Horas totales: " << horasTotales << endl;
    cout << "Segundos totales: " << segundosTotales << endl;
}

int main() {
    Registro log;
    int semanas, diasExtra, horasExtra;
    string nombreArchivo;
    int opcionExt;

    cout << "Bienvenido usuario\n";
    cout << "Por favor ingresa tu nombre: ";
    getline(cin, log.nombre);

    cout << "Hola " << log.nombre << ", ingresa tu número de cédula: ";
    cin >> log.ci;
    cin.ignore();

    cout << log.nombre << ", ¿Qué curso estás cursando?: ";
    getline(cin, log.curso);

    cout << "¿Cuántas semanas dura el curso?: ";
    cin >> semanas;
    while (semanas < 0) {
        cout << "Valor inválido. Ingrese semanas >= 0: ";
        cin >> semanas;
    }

    cout << "¿Cuántos días extra tiene además de las semanas?: ";
    cin >> diasExtra;
    while (diasExtra < 0) {
        cout << "Valor inválido. Ingrese días >= 0: ";
        cin >> diasExtra;
    }

    cout << "¿Cuántas horas extra tiene además de los días extra?: ";
    cin >> horasExtra;
    while (horasExtra < 0) {
        cout << "Valor inválido. Ingrese horas >= 0: ";
        cin >> horasExtra;
    }

    cout << "Nombre para el archivo: ";
    cin >> nombreArchivo;

    cout << "Seleccione una extensión para el archivo:\n";
    cout << "1. Texto (.txt)\n";
    cout << "2. Registro (.log)\n";
    cout << "3. Documento (.doc)\n";
    cin >> opcionExt;

    string extension;
    switch (opcionExt) {
        case 1: extension = ".txt"; break;
        case 2: extension = ".log"; break;
        case 3: extension = ".doc"; break;
        default: extension = ".txt"; cout << "Opción inválida, se usará .txt\n"; break;
    }

    string archivoFinal = nombreArchivo + extension;
    ofstream file(archivoFinal);
    if (!file) {
        cerr << "Error abriendo el archivo\n";
        return 1;
    }

    file << "Nombre: " << log.nombre << "\n";
    file << "Cédula: " << log.ci << "\n";
    file << "Curso: " << log.curso << "\n";
    file.close();

    cout << "Datos guardados en " << archivoFinal << endl;

    resolver(semanas, diasExtra, horasExtra);

    return 0;
}