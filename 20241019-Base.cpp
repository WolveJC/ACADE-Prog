#include  <iostream>
#include <fstream>
#include <stdlib.h>
using namespace std;

struct Cont{
int dat;
Cont *foll;
};

Cont *phill= NULL;
Cont *front=NULL;
Cont *end=NULL;

//Crear pila, puntero y dirección + el dato para rellenar
void sozoPhill(Cont *&phill , int dato){
	Cont *novo_dono= new Cont();
	novo_dono->dat=dato; //Rellenar dato
	novo_dono->foll=phill;
	phill=novo_dono;
}

//Sacar pila, puntero y dirección + dirección del dato rellenado
void hakaiPhill(Cont *&phill, int &dat){
	if (phill == NULL) {
        cout << "La pila está vacía." << endl;
        return;
    }
    cout << "Datos:" << endl;
    while (phill != NULL) {
        cout << "" << phill->dat << endl;
        Cont *axil = phill;
        stutu= axil->stu;
        phill = phill->foll;
        delete axil;
    }
}

//Cola vacía
bool VoidCoil(Cont *front){
	if (front == NULL){
		return true;
	}
	else{
		return false;
	}
}

//Crear cola, puntero con dirección para el comienzo y final de la cola + su dato a rellenar
void sozoCoil(Cont *&front, Cont *&end, struct stu) {
    Cont *novo_dono = new Cont();
    novo_dono->stu = stu;
    novo_dono->foll = NULL;
    if (VoidCoil(front)) {
        front = novo_dono;
    } else {
        end->foll = novo_dono;
    }
    end = novo_dono;
}


//Sacar cola, puntero con dirección para el comienzo y final de la cola + dirección del dato rellenado
void hakaiCoil(Cont *&front, Cont *&end, &dat) {
   if (VoidCoil(front)) {
        cout << "La cola está vacía." << endl;
        return;
    }
    cout << "Datos:" << endl;
    while (!VoidCoil(front)) {
        cout << "" << front->dat<< endl;
        stutu= axil->stu;
        front = front->foll;
        if (front == NULL) {
            end = NULL;
        }
        delete axil;
    }
	
}

//Función Archivo
void save_arch(){
    string filename;
    string ext;
    fstream arch;
    ext=".txt";
    cout << "Ingrese el nombre con el que desea guardar el archivo: " << endl;
    cin >> filename;
    filename+=ext;
    arch.open(filename.c_str(),ios::out);
    if (arch.fail()) {
        cout << "* ERROR GENERARANDO RECIBO *" << endl;
    }
    arch << "/n " << endl;
    cout << "Archivo Generado" << endl;
    arch.close();
}
//Menú rotativo
int main (){
	char opc, res;
    int op;
        do {
        cout << "MENU" << endl;
        cout << "1. Ingresar y Sacar pila" << endl;
        cout << "2. Ingresar y Sacar cola" << endl;
        cout << "3. Salir" << endl;
        cin >> op;
        switch (op) {
            case 1:
                do {
                	cout << "Ingresar datos" << endl;
                	sozo
                    cout << "¿Ingresar mas datos? (s/n): " << endl;
                    cin >> opc;
                    system ("cls");
                } while (opc == 's');
                hakai
                break;
            case 2:
                do {
                	cout << "Ingresar datos" << endl;
                	sozo
                    cout << "¿Ingresar mas datos? (s/n): " << endl;
                    cin >> opc;
                    system ("cls");
                } while (opc == 's');
                hakai
                break;
            case 3:
                cout << "Saliendo..." << endl;
                return 0;
            default:
                cout << "Opción no válida. Intente de nuevo." << endl;
                break;
        }
        cout << "¿Desea regresar al menu? (s/n): " << endl;
        cin >> res;
        system ("cls");
    } while (res == 's');
	return 0;
}
