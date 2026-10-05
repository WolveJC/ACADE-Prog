#include <iostream>
#include <string>
#include <limits>
using namespace std;

class Loger {
private:
    string user;
    string password;
    string q1, q2;     // Preguntas secretas
    string a1, a2;     // Respuestas correctas

public:
    Loger(string user, string password, string q1, string a1, string q2, string a2)
        : user(user), password(password), q1(q1), a1(a1), q2(q2), a2(a2) {}

    // Login básico con 3 intentos
    bool login() {
        for (int intento = 1; intento <= 3; intento++) {
            string u, p;
            cout << "Usuario: ";
            getline(cin, u);
            cout << "Contraseña: ";
            getline(cin, p);
            if (u == user && p == password) {
                cout << "Acceso concedido.\n";
                return true;
            }
            cout << "Credenciales incorrectas. Intento " << intento << "/3.\n";
        }
        cout << "Demasiados intentos fallidos.\n";
        return false;
    }

    // Cambio directo de contraseña (requiere estar logueado)
    void cambiarContrasena() {
        string nueva, confirmar;
        cout << "Ingrese nueva contraseña: ";
        getline(cin, nueva);
        cout << "Confirme nueva contraseña: ";
        getline(cin, confirmar);
        if (nueva.empty()) {
            cout << "La contraseña no puede estar vacía.\n";
            return;
        }
        if (nueva != confirmar) {
            cout << "Las contraseñas no coinciden.\n";
            return;
        }
        password = nueva;
        cout << "Contraseña actualizada exitosamente.\n";
    }

    // Recuperación de contraseña usando 2 preguntas secretas
    bool recuperarContrasena() {
        string r1, r2;
        cout << "Pregunta 1: " << q1 << "\nRespuesta: ";
        getline(cin, r1);
        cout << "Pregunta 2: " << q2 << "\nRespuesta: ";
        getline(cin, r2);

        if (normalize(r1) == normalize(a1) && normalize(r2) == normalize(a2)) {
            cout << "Validación correcta. Establezca nueva contraseña.\n";
            cambiarContrasena();
            return true;
        } else {
            cout << "Respuestas incorrectas. No se pudo recuperar la contraseña.\n";
            return false;
        }
    }

    // Utilidad: muestra datos (sin exponer la contraseña)
    void mostrarPerfil() const {
        cout << "Usuario: " << user << "\n";
        cout << "Pregunta 1: " << q1 << "\n";
        cout << "Pregunta 2: " << q2 << "\n";
    }

private:
    static string normalize(const string& s) {
        // Trim simple + case-insensitive
        size_t start = s.find_first_not_of(" \t\n\r");
        size_t end = s.find_last_not_of(" \t\n\r");
        string t = (start == string::npos) ? "" : s.substr(start, end - start + 1);
        for (char& c : t) c = tolower(static_cast<unsigned char>(c));
        return t;
    }
};

// Multiplica dos números y repite un mensaje n = a * b veces
void multiplicarYRepetir() {
    long long a, b;
    string frase;

    cout << "Ingrese el primer número: ";
    while (!(cin >> a)) {
        cout << "Número inválido. Intente de nuevo: ";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
    cout << "Ingrese el segundo número: ";
    while (!(cin >> b)) {
        cout << "Número inválido. Intente de nuevo: ";
        cin.clear();
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }
    cin.ignore(numeric_limits<streamsize>::max(), '\n'); // limpiar salto

    cout << "Ingrese la frase: ";
    getline(cin, frase);

    long long n = a * b;
    if (n < 0) {
        cout << "El producto es negativo. No se puede repetir una cantidad negativa.\n";
        return;
    }
    if (n > 100000) {
        cout << "Cantidad excesiva (" << n << "). Limite de seguridad: 100000.\n";
        return;
    }
    for (long long i = 0; i < n; i++) {
        cout << frase << "\n";
    }
}

int main() {
    // Configuración inicial (puedes reemplazar por entradas del usuario si deseas)
    string user = "Fullo355";
    string pass = "346464";
    string q1 = "Color favorito";
    string a1 = "Azul";
    string q2 = "Ciudad natal";
    string a2 = "Caracas";

    Loger auth(user, pass, q1, a1, q2, a2);

    cout << "=== Sistema de Login ===\n";
    auth.mostrarPerfil();
    cout << "\nIntente iniciar sesión.\n";

    bool acceso = auth.login();

    int opcion = -1;
    do {
        cout << "\n--- MENU ---\n";
        cout << "1. Cambiar contraseña\n";
        cout << "2. Recuperar contraseña (2 preguntas secretas)\n";
        cout << "3. Multiplicar y repetir mensaje (n = a*b)\n";
        cout << "4. Mostrar perfil\n";
        cout << "5. Salir\n";
        cout << "Seleccione una opción: ";
        if (!(cin >> opcion)) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Entrada inválida.\n";
            continue;
        }
        cin.ignore(numeric_limits<streamsize>::max(), '\n'); // limpiar salto

        switch (opcion) {
            case 1:
                if (!acceso) {
                    cout << "Debe iniciar sesión para cambiar la contraseña.\n";
                } else {
                    auth.cambiarContrasena();
                }
                break;
            case 2:
                auth.recuperarContrasena();
                // Si recuperación exitosa, considera acceso concedido
                acceso = true;
                break;
            case 3:
                multiplicarYRepetir();
                break;
            case 4:
                auth.mostrarPerfil();
                break;
            case 5:
                cout << "Saliendo...\n";
                break;
            default:
                cout << "Opción no válida.\n";
        }
    } while (opcion != 5);

    return 0;
}