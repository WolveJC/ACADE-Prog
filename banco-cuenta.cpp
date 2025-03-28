#include <iostream>
#include <string>
using namespace std;

// Definición de la clase CuentaBancaria
class CuentaBancaria {
private:
    string titular;
    string numeroCuenta;
    double saldo;

public:
    // Constructor
    CuentaBancaria(string titular, string numero, double saldoInicial) {
        this->titular = titular;
        this->numeroCuenta = numero;
        this->saldo = saldoInicial;
    }

    // Método para depositar dinero
    void depositar(double monto) {
        if (monto > 0) {
            saldo += monto;
            cout << "Depósito exitoso. Nuevo saldo: $" << saldo << endl;
        } else {
            cout << "El monto debe ser mayor a 0." << endl;
        }
    }

    // Método para retirar dinero
    void retirar(double monto) {
        if (monto > 0 && monto <= saldo) {
            saldo -= monto;
            cout << "Retiro exitoso. Nuevo saldo: $" << saldo << endl;
        } else {
            cout << "Fondos insuficientes o monto inválido." << endl;
        }
    }

    // Método para mostrar información de la cuenta
    void mostrarInformacionCuenta() {
        cout << "Titular de la cuenta: " << titular << endl;
        cout << "Número de cuenta: " << numeroCuenta << endl;
        cout << "Saldo: $" << saldo << endl;
    }
};

int main() {
    // Crear una cuenta bancaria
    CuentaBancaria miCuenta("Juan Pérez", "123456789", 1000.00);

    // Mostrar información inicial de la cuenta
    cout << "Información inicial de la cuenta:" << endl;
    miCuenta.mostrarInformacionCuenta();

    // Realizar operaciones
    cout << "\nRealizando un depósito de $500..." << endl;
    miCuenta.depositar(500);

    cout << "\nIntentando retirar $2000..." << endl;
    miCuenta.retirar(2000);

    cout << "\nRetirando $300..." << endl;
    miCuenta.retirar(300);

    // Mostrar información final de la cuenta
    cout << "\nInformación final de la cuenta:" << endl;
    miCuenta.mostrarInformacionCuenta();

    return 0;
}