#include <iostream>
#include <string>

using namespace std;

struct Productos {
    string nomp;
    int cod;
    float pre;
    int exis;
};

struct Persona {
    char nom[45];
    char ape[45];
    int cedula;
    int tel;
    double credito;
};

int main() {
    int cant;
    int op = 0;

    // Arreglo de tamaño 4 para usar los índices 1, 2 y 3 de forma segura
    Productos merca[4]; 

    // 1. Registro inicial de los 3 productos
    for (int i = 1; i <= 3; i++) {
        cout << "--- Producto " << i << " ---" << endl;
        cout << "Nombre del producto: ";
        cin >> merca[i].nomp;
        
        cout << "Codigo del producto: ";
        cin >> merca[i].cod;
        
        cout << "Precio del producto: ";
        cin >> merca[i].pre;
        
        cout << "Existencia inicial: ";
        cin >> merca[i].exis;
        cout << endl;
    }

    // 2. Registro inicial del cliente
    Persona cliente;
    cout << "--- Datos del Cliente ---" << endl;
    cout << "Nombre de la persona: ";
    cin >> cliente.nom;
    cout << "Apellido de la persona: ";
    cin >> cliente.ape;
    cout << "Cedula de la persona: ";
    cin >> cliente.cedula;
    cout << "Telefono de la persona: ";
    cin >> cliente.tel;
    cout << "Credito disponible de la persona: ";
    cin >> cliente.credito;
    cout << endl;

    // 3. Ciclo principal del sistema (Menú interactivo)
    while (op != 4) {
        cout << "\n===========================" << endl;
        cout << "BIENVENIDO - MENU PRINCIPAL" << endl;
        cout << "Credito disponible: " << cliente.credito << endl;
        cout << "Elige una opcion de producto:" << endl;
        cout << "1. " << merca[1].nomp << " | Precio: " << merca[1].pre << " | Stock: " << merca[1].exis << endl;
        cout << "2. " << merca[2].nomp << " | Precio: " << merca[2].pre << " | Stock: " << merca[2].exis << endl;
        cout << "3. " << merca[3].nomp << " | Precio: " << merca[3].pre << " | Stock: " << merca[3].exis << endl;
        cout << "4. Salir del sistema" << endl;
        cout << "Opcion: ";
        cin >> op;

        if (op >= 1 && op <= 3) {
            int idx = op; // Índice del producto seleccionado
            
            cout << "\n--- Producto Seleccionado: " << merca[idx].nomp << " ---" << endl;
            cout << "Disponibles en stock: " << merca[idx].exis << endl; 
            cout << "Precio unitario: " << merca[idx].pre << endl;
            cout << "¿Cuanto desea adquirir? (Ingrese 0 para cancelar y volver al menu): ";
            cin >> cant;

            // Si el usuario introduce 0, cancela y regresa al menú
            if (cant == 0) {
                cout << "Operacion cancelada. Regresando al menu..." << endl;
            } 
            else if (cant < 0) {
                cout << "Error: No puede ingresar cantidades negativas." << endl;
            } 
            else {
                double total = cant * merca[idx].pre;

                // Validar existencias
                if (cant > merca[idx].exis) {
                    cout << "¡Error! No hay suficiente existencia. Stock actual: " << merca[idx].exis << endl;
                }
                // Validar crédito
                else if (total > cliente.credito) {
                    cout << "¡Error! El cliente no posee suficiente crédito." << endl;
                    cout << "Total de la compra: " << total << " | Crédito disponible: " << cliente.credito << endl;
                } 
                // Transacción exitosa
                else {
                    merca[idx].exis -= cant;
                    cliente.credito -= total;

                    cout << "\n¡Compra realizada con exito!" << endl;
                    cout << "Se descontaron " << total << " de credito." << endl;
                    cout << "Nuevo credito restante: " << cliente.credito << endl;
                }
            }
        } 
        else if (op == 4) {
            cout << "\nSaliendo del sistema. ¡Gracias por usar el programa!" << endl;
        } 
        else {
            cout << "\nOpcion invalida. Intente de nuevo." << endl;
        }
    }

    return 0;
}
