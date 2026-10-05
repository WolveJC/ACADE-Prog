#include <iostream>
#include <string>
using namespace std;

struct per {
    string nom;
    string ap;
    int age;
    string contry;
};

struct estudiante {
    per pipol;
    string cur;
    float prom;
};

struct Cont {
    estudiante stu;
    Cont *foll;
};

float not_1, not_2, not_3;
estudiante stu;
Cont *phill = NULL;
Cont *front = NULL;
Cont *rear = NULL;   // antes era "end", ahora "rear"

bool aprob(estudiante stu) {
    return stu.prom >= 10;
}

float prom(float not1, float not2, float not3) {
    return (not1 * 0.3) + (not2 * 0.3) + (not3 * 0.4);
}

// Pila
void sozoPhill(Cont *&phill, estudiante stu) {
    Cont *novo_dono = new Cont();
    novo_dono->stu = stu;
    novo_dono->foll = phill;
    phill = novo_dono;
}

void hakaiPhill(Cont *&phill, estudiante &stutu) {
    if (phill == NULL) {
        cout << "La pila está vacía." << endl;
        return;
    }
    cout << "Estudiantes en la pila:" << endl;
    while (phill != NULL) {
        cout << "Nombre y Apellido: " << phill->stu.pipol.nom << " " << phill->stu.pipol.ap << endl;
        cout << "Edad: " << phill->stu.pipol.age << endl;
        cout << "Nacionalidad: " << phill->stu.pipol.contry << endl;
        cout << "Curso: " << phill->stu.cur << endl;
        cout << "Promedio: " << phill->stu.prom << " - " 
             << (aprob(phill->stu) ? "Aprobado" : "Reprobado") << endl;
        Cont *axil = phill;
        stutu = axil->stu;
        phill = phill->foll;
        delete axil;
    }
}

// Cola
bool VoidCoil(Cont *front) {
    return front == NULL;
}

void sozoCoil(Cont *&front, Cont *&rear, estudiante stu) {
    Cont *novo_dono = new Cont();
    novo_dono->stu = stu;
    novo_dono->foll = NULL;
    if (VoidCoil(front)) {
        front = novo_dono;
    } else {
        rear->foll = novo_dono;
    }
    rear = novo_dono;
}

void hakaiCoil(Cont *&front, Cont *&rear, estudiante &stutu) {
    if (VoidCoil(front)) {
        cout << "La cola está vacía." << endl;
        return;
    }
    cout << "Estudiantes en la cola:" << endl;
    while (!VoidCoil(front)) {
        cout << "Nombre y Apellido: " << front->stu.pipol.nom << " " << front->stu.pipol.ap << endl;
        cout << "Edad: " << front->stu.pipol.age << endl;
        cout << "Nacionalidad: " << front->stu.pipol.contry << endl;
        cout << "Curso: " << front->stu.cur << endl;
        cout << "Promedio: " << front->stu.prom << " - " 
             << (aprob(front->stu) ? "Aprobado" : "Reprobado") << endl;
        Cont *axil = front;
        stutu = axil->stu;
        front = front->foll;
        if (front == NULL) {
            rear = NULL;
        }
        delete axil;
    }
}

int main() {
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
                    cout << "Ingrese nombre de la persona: ";
                    cin >> stu.pipol.nom;
                    cout << "Ingrese apellido de la persona: ";
                    cin >> stu.pipol.ap;
                    cout << "Ingrese nacionalidad de la persona: ";
                    cin >> stu.pipol.contry;
                    cout << "Ingrese edad de la persona: ";
                    cin >> stu.pipol.age;
                    cout << "Ingrese el curso del estudiante: ";
                    cin >> stu.cur;
                    cout << "Ingrese la nota 1: ";
                    cin >> not_1;
                    cout << "Ingrese nota 2: ";
                    cin >> not_2;
                    cout << "Ingrese nota 3: ";
                    cin >> not_3;
                    stu.prom = prom(not_1, not_2, not_3);
                    cout << (aprob(stu) ? "El estudiante aprobó" : "El estudiante reprobó") << endl;
                    sozoPhill(phill, stu);
                    cout << "¿Ingresar más datos? (s/n): ";
                    cin >> opc;
                    cout << string(20, '\n'); // limpiar pantalla
                } while (opc == 's');
                hakaiPhill(phill, stu);
                break;
            case 2:
                do {
                    cout << "Ingrese nombre de la persona: ";
                    cin >> stu.pipol.nom;
                    cout << "Ingrese apellido de la persona: ";
                    cin >> stu.pipol.ap;
                    cout << "Ingrese nacionalidad de la persona: ";
                    cin >> stu.pipol.contry;
                    cout << "Ingrese edad de la persona: ";
                    cin >> stu.pipol.age;
                    cout << "Ingrese el curso del estudiante: ";
                    cin >> stu.cur;
                    cout << "Ingrese la nota 1: ";
                    cin >> not_1;
                    cout << "Ingrese nota 2: ";
                    cin >> not_2;
                    cout << "Ingrese nota 3: ";
                    cin >> not_3;
                    stu.prom = prom(not_1, not_2, not_3);
                    cout << (aprob(stu) ? "El estudiante aprobó" : "El estudiante reprobó") << endl;
                    sozoCoil(front, rear, stu);
                    cout << "¿Ingresar más datos? (s/n): ";
                    cin >> opc;
                    cout << string(20, '\n'); // limpiar pantalla
                } while (opc == 's');
                hakaiCoil(front, rear, stu);
                break;
            case 3:
                cout << "Saliendo..." << endl;
                return 0;
            default:
                cout << "Opción no válida. Intente de nuevo." << endl;
                break;
        }
        cout << "¿Desea regresar al menú principal? (s/n): ";
        cin >> res;
        cout << string(20, '\n'); // limpiar pantalla
    } while (res == 's');
    return 0;
}