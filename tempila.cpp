#include <iostream>
#include <stdlib.h>
#include <fstream>
using namespace std;


struct tiempo{
	int semanas, dias, horas, minutos, segundos;
};

struct persona{
	string nom,curso;
	int ci;
};

struct nodo{
	persona per;
	tiempo tem;
	nodo *siguiente;
};

void seg(tiempo &tempila);
void ingresarpila (nodo *&, persona perpila, tiempo tempila);
void sacarpila(nodo *&, persona &perpila, tiempo &tempila);


int main(){
	persona per;
	tiempo tem;
	nodo *pila = NULL;
	cout << "Bienvenido" << endl;
	cout << "Ingrese su nombre:" << endl;
	getline (cin,per.nom);
	cout << "Ingrese su cedula:" << endl;
	cin >> per.ci;
	cout << "Ingrese la materia que desea cursar:" << endl;
	cin >> per.curso;
	cout << "Ingrese cuantas semanas cursara:" << endl;
	cin>> tem.semanas;
	cout << "Ingrese los dias que vera el curso:" << endl;
	cin>> tem.dias;
	cout << "Ingrese las horas que vera el curso:" << endl;
	cin >>  tem.horas;
	seg (tem);
	ingresarpila(pila, per, tem);
	
	while (pila != NULL){
		sacarpila(pila, per, tem);
		if (pila != NULL){
			cout << "Horas: " << tem.horas << endl;
			cout << "Dias: "  << tem.dias <<  endl;
			cout << "Semanas: " << tem.semanas << endl;
			cout << "Curso: " << per.curso << endl;
			cout << "Cedula: " << per.ci << endl;
			cout << "Nombre: " << per.nom << endl;
		}
		else {
			cout << "Ahora se mostraran los datos ingresados: " << endl;
			cout << "Nombre: " << per.nom << endl;
			cout << "Cedula: " << per.ci << endl;
			cout << "Curso: " << per.curso << endl;
			cout << "Semanas: " << tem.semanas << endl;
			cout << "Dias: " << tem.dias << endl;
			cout << "Horas: " << tem.horas << endl;
			cout << "Tiempo total en segundos: " << tem.segundos << endl;
		}
	}
	
	return 0;
}

void seg (tiempo &tempila){
	int dias2,horas2;
	dias2 = tempila.semanas*7;
	dias2 = tempila.dias+dias2;
	horas2=dias2*24;
	horas2=tempila.horas+horas2;
	tempila.segundos = horas2*3600;
}

void ingresarpila (nodo *&pila, persona perpila, tiempo tempila){
	nodo *nuevo_nodo = new nodo();
	nuevo_nodo->per = perpila;
	nuevo_nodo->tem = tempila;
	nuevo_nodo->siguiente = pila;
	pila = nuevo_nodo;
	cout << "Ingresando datos a la pila..." << endl;
	string o;
	fstream ingresarpila;
	cout << "Ingrese el nombre y la extension con la que guardara el archvio" << endl;
	cin >> o;
	ingresarpila.open(o.c_str(),ios::out);
	if (ingresarpila.fail()){
		cout << "Error" << endl;
	}
	else {
		ingresarpila << "Tiempo total en segundos: " << tempila.segundos << endl;
		ingresarpila << "Horas: " << tempila.horas << endl;
	    ingresarpila << "Dias: "  << tempila.dias <<  endl;
		ingresarpila << "Semanas: " << tempila.semanas << endl;
		ingresarpila << "Curso: " << perpila.curso << endl;
		ingresarpila << "Cedula: " << perpila.ci << endl;
		ingresarpila << "Nombre: " << perpila.nom << endl;
	}
	ingresarpila.close();
}
void sacarpila (nodo *&pila, persona &perpila, tiempo &tempila){
	nodo *aux = pila;
	perpila = aux->per;
	tempila = aux->tem;
	pila = aux->siguiente;
	delete aux;
	string o;
	fstream sacarpila;
	cout << "Ingrese el nombre y la extension con la que guardara el archvio" << endl;
	cin >> o;
	sacarpila.open(o.c_str(),ios::out);
	if (sacarpila.fail()){
		cout << "Error" << endl;
	}
	else {
		sacarpila << "Nombre: " << perpila.nom << endl;
		sacarpila << "Cedula: " << perpila.ci << endl;
		sacarpila << "Curso: " << perpila.curso << endl;
		sacarpila << "Horas: " << tempila.horas << endl;
	    sacarpila << "Dias: "  << tempila.dias <<  endl;
		sacarpila << "Semanas: " << tempila.semanas << endl;
		sacarpila << "Tiempo total en segundos: " << tempila.segundos << endl;
	}
	sacarpila.close();
}

