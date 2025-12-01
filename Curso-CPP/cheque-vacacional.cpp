#include <iostream>
using namespace std;

// Definición correcta de la función
void fun1(double h, double c, int d) {
    double mont = d * (h + c + 3000);  // declaramos mont como double
    cout << "Monto total del cheque: " << mont << endl;
}

int main() {
    int com;
    int hot;
    int days;

    cout << "¿Cuántos días estará de viaje?" << endl;
    cin >> days;

    cout << "Ingrese monto por la comida: " << endl;
    cin >> com;

    cout << "Monto por habitación de hotel: " << endl;
    cin >> hot;

    fun1(hot, com, days);

    return 0;
}