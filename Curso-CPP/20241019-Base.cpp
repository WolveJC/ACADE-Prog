#include <iostream>
#include <fstream>
#include <string>
using namespace std;

struct Cont {
    int dat;
    Cont* foll;
};

// Punteros globales para pila y cola
Cont* phill = nullptr;   // pila
Cont* front = nullptr;   // cola inicio
Cont* end = nullptr;     // cola fin

// Crear pila
void sozoPhill(Cont*& phill, int dato) {
    Cont* novo_dono = new Cont();
    novo_dono->dat = dato;
    novo_dono->foll = phill;
    phill = novo_dono;
}

// Sacar pila
void hakaiPhill(Cont*& phill) {
    while (phill != nullptr) {
        cout << "Dato pila: " << phill->dat << endl;
        Cont* axil = phill;
        phill = phill->foll;
        delete axil;
    }
}

// Cola vacía
bool VoidCoil(Cont* front) {
    return (front == nullptr);
}

// Crear cola
void sozoCoil(Cont*& front, Cont*& end, int dato) {
    Cont* novo_dono = new Cont();
    novo_dono->dat = dato;
    novo_dono->foll = nullptr;
    if (VoidCoil(front)) {
        front = novo_dono;
    } else {
        end->foll = novo_dono;
    }
    end = novo_dono;
}

// Sacar cola
void hakaiCoil(Cont*& front, Cont*& end) {
    while (!VoidCoil(front)) {
        cout << "Dato cola: " << front->dat << endl;
        Cont* axil = front;
        front = front->foll;
        if (front == nullptr) end = nullptr;
        delete axil;
    }
}

// Guardar archivo (esqueleto)
void save_arch() {
    string filename;
    fstream arch;
    cout << "Ingrese nombre de archivo: ";
    cin >> filename;
    filename += ".txt";
    arch.open(filename.c_str(), ios::out);
    if (!arch) {
        cout << "Error generando archivo\n";
    } else {
        arch << "Ejemplo de escritura\n";
        cout << "Archivo generado\n";
    }
    arch.close();
}

// Menú rotativo
int main() {
    int op;
    char res;
    do {
        cout << "\n--- MENU ---\n";
        cout << "1. Ingresar y sacar pila\n";
        cout << "2. Ingresar y sacar cola\n";
        cout << "3. Guardar archivo\n";
        cout << "4. Salir\n";
        cin >> op;
        switch (op) {
            case 1:
                sozoPhill(phill, 10);
                sozoPhill(phill, 20);
                hakaiPhill(phill);
                break;
            case 2:
                sozoCoil(front, end, 30);
                sozoCoil(front, end, 40);
                hakaiCoil(front, end);
                break;
            case 3:
                save_arch();
                break;
            case 4:
                cout << "Saliendo...\n";
                return 0;
            default:
                cout << "Opción no válida.\n";
        }
        cout << "¿Desea regresar al menú? (s/n): ";
        cin >> res;
    } while (res == 's');
    return 0;
}