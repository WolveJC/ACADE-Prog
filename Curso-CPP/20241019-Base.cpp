#include <iostream>
#include <fstream>
#include <string>
using namespace std;

// -------------------- Struct base para pila/cola --------------------
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

// -------------------- Ejemplo if y for --------------------
void ejemploIfFor() {
    cout << "\nEjemplo IF y FOR:\n";
    for (int i = 1; i <= 5; i++) {
        if (i % 2 == 0) {
            cout << i << " es par\n";
        } else {
            cout << i << " es impar\n";
        }
    }
}

// -------------------- Lista enlazada --------------------
struct NodoLista {
    int dato;
    NodoLista* sig;
};

void ejemploLista() {
    cout << "\nEjemplo Lista Enlazada:\n";
    NodoLista* head = nullptr;
    // Insertar 3 nodos
    for (int i = 1; i <= 3; i++) {
        NodoLista* nuevo = new NodoLista();
        nuevo->dato = i * 10;
        nuevo->sig = head;
        head = nuevo;
    }
    // Recorrer lista
    NodoLista* temp = head;
    while (temp != nullptr) {
        cout << "Nodo lista: " << temp->dato << endl;
        temp = temp->sig;
    }
}

// -------------------- Árbol binario --------------------
struct NodoArbol {
    int dato;
    NodoArbol* izq;
    NodoArbol* der;
};

NodoArbol* insertarArbol(NodoArbol* raiz, int valor) {
    if (raiz == nullptr) {
        NodoArbol* nuevo = new NodoArbol();
        nuevo->dato = valor;
        nuevo->izq = nuevo->der = nullptr;
        return nuevo;
    }
    if (valor < raiz->dato) raiz->izq = insertarArbol(raiz->izq, valor);
    else raiz->der = insertarArbol(raiz->der, valor);
    return raiz;
}

void recorrerArbol(NodoArbol* raiz) {
    if (raiz != nullptr) {
        recorrerArbol(raiz->izq);
        cout << "Nodo árbol: " << raiz->dato << endl;
        recorrerArbol(raiz->der);
    }
}

void ejemploArbol() {
    cout << "\nEjemplo Árbol Binario:\n";
    NodoArbol* raiz = nullptr;
    raiz = insertarArbol(raiz, 50);
    raiz = insertarArbol(raiz, 30);
    raiz = insertarArbol(raiz, 70);
    recorrerArbol(raiz);
}

// -------------------- Clase básica --------------------
class ClaseBasica {
private:
    int valor; // encapsulado privado
public:
    ClaseBasica(int v) { // constructor
        valor = v;
        cout << "Constructor llamado con valor " << valor << endl;
    }
    ~ClaseBasica() { // destructor
        cout << "Destructor llamado\n";
    }
    void mostrar() { // método público
        cout << "Valor: " << valor << endl;
    }
};

void ejemploClase() {
    cout << "\nEjemplo Clase Básica:\n";
    ClaseBasica obj(42);
    obj.mostrar();
}

// -------------------- Guardar archivo --------------------
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

// -------------------- Menú rotativo --------------------
int main() {
    int op;
    char res;
    do {
        cout << "\n--- MENU ---\n";
        cout << "1. Ingresar y sacar pila\n";
        cout << "2. Ingresar y sacar cola\n";
        cout << "3. Guardar archivo\n";
        cout << "4. Ejemplo IF y FOR\n";
        cout << "5. Ejemplo Lista Enlazada\n";
        cout << "6. Ejemplo Árbol Binario\n";
        cout << "7. Ejemplo Clase Básica\n";
        cout << "8. Salir\n";
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
                ejemploIfFor();
                break;
            case 5:
                ejemploLista();
                break;
            case 6:
                ejemploArbol();
                break;
            case 7:
                ejemploClase();
                break;
            case 8:
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