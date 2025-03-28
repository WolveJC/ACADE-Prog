#include <iostream>
#include <string>
using namespace std;

class Usuario {
private:
    string usuario;
    string clave;
    string pregunta1;
    string pregunta2;
    string respuesta1;
    string respuesta2;

public:
    Usuario(string usu, string cla, string pre1, string pre2, string res1, string res2) {
        usuario = usu;
        clave = cla;
        pregunta1 = pre1;
        pregunta2 = pre2;
        respuesta1 = res1;
        respuesta2 = res2;
    }

    bool Login(string usu, string cla) {
        return (usuario == usu && clave == cla);
    }

    bool Cambiarclave(string res1, string res2) {
        if (respuesta1 == res1 && respuesta2 == res2) {
            cout << "Ingrese su nueva clave: " << endl;
            string nuevaclave;
            cin >> nuevaclave;
            clave = nuevaclave;
            cout << "Clave cambiada correctamente." << endl;
            return true;
        } else {
            cout << "Respuestas incorrectas." << endl;
            return false;
        }
    }

    void mostrarmenu() {
        int op;
        do {
            cout << "\n--- Menu ---\n";
            cout << "1. Cambiar clave\n";
            cout << "2. Multiplicar dos numeros\n";
            cout << "3. Salir\n";
            cout << "Seleccione una opcion: ";
            cin >> op;

            switch (op) {
                case 1: {
                    string res1, res2;
                    bool claveCambiada = false;
                    do {
                        cout << pregunta1 << ": ";
                        cin >> res1;
                        cout << pregunta2 << ": ";
                        cin >> res2;
                        claveCambiada = Cambiarclave(res1, res2);
                    } while (!claveCambiada); // Repetir hasta que las respuestas sean correctas
                    break;
                }
                case 2: {
                    int num1, num2;
                    cout << "Ingrese el primer numero: ";
                    cin >> num1;
                    cout << "Ingrese el segundo numero: ";
                    cin >> num2;
                    int resultado = num1 * num2;
                    for (int i = 0; i < resultado; i++) {
                        cout << "Exito" << endl;
                    }
                    break;
                }
                case 3: {
                    cout << "Saliendo del menu...." << endl;
                    break;
                }
                default:
                    cout << "Opcion no valida" << endl;
            }
        } while (op != 3);
    }
};

int main() {
    string usuario, clave;

    cout << "Ingrese su nombre de usuario: " << endl;
    cin >> usuario;
    cout << "Ingrese su clave: " << endl;
    cin >> clave;

    string pregunta1, respuesta1, pregunta2, respuesta2;
    cout << "Ingrese su primera pregunta de seguridad: " << endl;
    cin.ignore();
    getline(cin, pregunta1);
    cout << "Ingrese la respuesta a la primera pregunta: " << endl;
    getline(cin, respuesta1);
    cout << "Ingrese su segunda pregunta de seguridad: " << endl;
    getline(cin, pregunta2);
    cout << "Ingrese la respuesta a la segunda pregunta: " << endl;
    getline(cin, respuesta2);

    Usuario u(usuario, clave, pregunta1, pregunta2, respuesta1, respuesta2);
    cout << "Login exitoso" << endl;

    // Llamar al menú
    u.mostrarmenu();

    return 0;
}