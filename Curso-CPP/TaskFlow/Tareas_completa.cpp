#include <iostream>
#include <fstream>
#include <stack>
#include <queue>
#include <string>

using namespace std;

struct Tarea {
    string descripcion;
    bool urgente; // true si es urgente, false si es normal
};

// Funciones
void agregarTarea(stack<Tarea>& pila, queue<Tarea>& cola);
void mostrarTareas(const stack<Tarea>& pila, const queue<Tarea>& cola);
void guardarTareas(const stack<Tarea>& pila, const queue<Tarea>& cola);
void cargarTareas(stack<Tarea>& pila, queue<Tarea>& cola);

int main() {
    stack<Tarea> pilaTareas;
    queue<Tarea> colaTareas;
    cargarTareas(pilaTareas, colaTareas);

    int opcion;
    do {
        cout << "1. Agregar tarea\n";
        cout << "2. Mostrar tareas\n";
        cout << "3. Guardar tareas\n";
        cout << "4. Salir\n";
        cout << "Seleccione una opción: ";
        cin >> opcion;

        switch (opcion) {
            case 1:
                agregarTarea(pilaTareas, colaTareas);
                break;
            case 2:
                mostrarTareas(pilaTareas, colaTareas);
                break;
            case 3:
                guardarTareas(pilaTareas, colaTareas);
                break;
            case 4:
                cout << "Saliendo del programa...\n";
                break;
            default:
                cout << "Opción no válida. Intente de nuevo.\n";
        }
    } while (opcion != 4);

    return 0;
}

void agregarTarea(stack<Tarea>& pila, queue<Tarea>& cola) {
    Tarea nuevaTarea;
    cout << "Descripción de la tarea: ";
    cin.ignore(); // Limpiar el buffer
    getline(cin, nuevaTarea.descripcion);
    cout << "¿Es urgente? (1: Sí, 0: No): ";
    cin >> nuevaTarea.urgente;

    if (nuevaTarea.urgente) {
        pila.push(nuevaTarea);
    } else {
        cola.push(nuevaTarea);
    }
}

void mostrarTareas(const stack<Tarea>& pila, const queue<Tarea>& cola) {
    cout << "\nTareas Urgentes:\n";
    stack<Tarea> pilaTemporal = pila; // Copia de la pila para mostrar
    while (!pilaTemporal.empty()) {
        cout << "- " << pilaTemporal.top().descripcion << endl;
        pilaTemporal.pop();
    }

    cout << "\nTareas Normales:\n";
    queue<Tarea> colaTemporal = cola; // Copia de la cola para mostrar
    while (!colaTemporal.empty()) {
        cout << "- " << colaTemporal.front().descripcion << endl;
        colaTemporal.pop();
    }
    cout << endl;
}

void guardarTareas(const stack<Tarea>& pila, const queue<Tarea>& cola) {
    ofstream archivo("tareas.txt");
    if (!archivo) {
        cerr << "Error al abrir el archivo para guardar.\n";
        return;
    }

    // Guardar tareas urgentes
    stack<Tarea> pilaTemporal = pila;
    while (!pilaTemporal.empty()) {
        archivo << "1 " << pilaTemporal.top().descripcion << endl; // 1 para urgente
        pilaTemporal.pop();
    }

    // Guardar tareas normales
    queue<Tarea> colaTemporal = cola;
    while (!colaTemporal.empty()) {
        archivo << "0 " << colaTemporal.front().descripcion << endl; // 0 para normal
        colaTemporal.pop();
    }

    archivo.close();
    cout << "Tareas guardadas exitosamente.\n";
}

void cargarTareas(stack<Tarea>& pila, queue<Tarea>& cola) {
    ifstream archivo("tareas.txt");
    if (!archivo) {
        cerr << "No se pudo abrir el archivo para cargar.\n";
        return;
    }

    Tarea tarea;
    int tipo;
    while (archivo >> tipo) {
        archivo.ignore(); // Limpiar el buffer
        getline(archivo, tarea.descripcion);
                if (tipo == 1) {
            tarea.urgente = true;
            pila.push(tarea); // Agregar a la pila si es urgente
        } else {
            tarea.urgente = false;
            cola.push(tarea); // Agregar a la cola si es normal
        }
    }

    archivo.close();
    cout << "Tareas cargadas exitosamente.\n";
}
