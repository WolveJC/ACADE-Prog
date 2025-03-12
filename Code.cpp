//Crea un programa que maneje una lista de estudiantes utilizando una pila. Cada estudiante debe tener un "struct" que contenga su nombre, edad y nota. 
#include <iostream>
#include <fstream>
#include <stdlib.h>
using namespace std;

struct estudiante{
	string nom;
	int edad, ci, nota;
};

struct nodo{
	estudiante estu;
	nodo *siguiente;
};

void ingresarpila(nodo *&, estudiante estu);
void sacarpila(nodo *&, estudiante &estupila);

int main (){
	nodo *pila=NULL;
	estudiante estu;
	string rep;
	
	do{
	cout << "Ingrese el nombre del alumno:"<< endl;
	cin>> estu.nom;
	cout << "Ingrese la edad del alumno:" << endl;
	cin>> estu.edad;
	cout << "Ingrese la cedula del alumno:" << endl;
	cin >> estu.ci;
	cout << "Ingrese la calificacion del alumno:" << endl;
	cin >> estu.nota;
	ingresarpila(pila,estu);
	cout << "¿Desea agregar mas alumnos al sistema? (s/n)" << endl;
	cin>> rep;
	system("cls");
	}
	while (rep=="s");
	while (pila != NULL){
		sacarpila (pila,estu);
		if (pila != NULL){
			cout << "Nombre: " << estu.nom << endl;
			cout << "Edad: " << estu.edad << endl;
			cout << "Cedula: " << estu.ci << endl;
			cout << "Calificacion: " << estu.nota << endl;
			cout << "-----------" << endl;
		}
		else {
			cout << "." << endl;
		}
	}

	return 0;
}
void ingresarpila(nodo *&pila,estudiante estupila){
	nodo *nuevo_nodo = new nodo();
	nuevo_nodo->estu = estupila;
	nuevo_nodo->siguiente = pila;
	pila = nuevo_nodo;
	cout << "Ingresando datos del estudiante a la pila..."<< endl;
}
void sacarpila(nodo *&pila, estudiante &estupila){
	nodo *aux=pila;
	estupila = aux->estu;
	pila = aux->siguiente;
	delete aux;
	string o;
	fstream sacarpila;
	cout << "Ingrese un nombre para guardar el archivo y su extension" << endl;
	cin>> o;
	sacarpila.open(o.c_str(),ios::app);
		if (sacarpila.fail()){
			cout<< "Error" << endl;
		}
		else {
			sacarpila << "Nombre: " << estupila.nom << endl;
			sacarpila << "Edad: " << estupila.edad << endl;
			sacarpila << "Cedula: " << estupila.ci << endl;
			sacarpila << "Calificacion: " << estupila.nota << endl;
			sacarpila << "-----------" << endl;
		}
		sacarpila.close();
}
