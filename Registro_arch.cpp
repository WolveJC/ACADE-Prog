#include<iostream>
#include<fstream>
#include<cstdio>
using namespace std;
int sem, dai, hours, h2, h3, dai2, dai3, seg, temp;
string nomapp;
int op;
struct Registro {
    char nombre [45];
    char cur [45];
    int ci;
};
int resolver( int sem, int hours, int dai);
int main()
{
    Registro log;
    cout << "Bienvenido usuario" << endl;
    cout << "Por favor ingresa tu nombre" << endl;
    cin >> log.nombre;
    cout << "Hola " << log.nombre<< ", ingresa tu n�mero de c�dula"<< endl;
    cin >> log.ci;
    cout << log.nombre<< ", �Que curso est�s cursando?" << endl;
    cin >> log.cur;
    cout << "�Cu�ntas semanas dura el curso?" << endl;
    cin >> sem;
    cout << "�Cu�ntos d�as extra tiene adem�s de las semanas?" << endl;
    cin >> dai;
    cout << "�Cu�ntas horas extra tiene adem�s de los d�as extra?" << endl;
    cin >> hours;
    cout << "Nombre para el archivo: " << endl;
    cin >> nomapp;
    cout << "Seleccione una extensi�n para el archivo" << endl;
    cout << "1. Texto (.txt)" << endl;
    cout << "2. Registro (.log)" << endl;
    cout << "3. Documento (.doc)" << endl;
    cin >> op;
    ofstream file;
    file.open (nomapp.c_str());
    if (!file){
    cout<< "Error abriendo el archivo\n";
    }
    file << log.nombre<<"\n";
    file << log.ci<<"\n";
    file << log.cur<<"\n";
    file.close();
    
    resolver (sem, hours, dai);
    return 0;
}
int resolver( int sem, int hours, int dai) {
    dai2=sem*7;
    dai3=dai+dai2;
    h2=dai2*24;
    h3=h2+hours;
    seg=h3*3600;
    cin >> temp;
    return temp;
}

