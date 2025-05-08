#include<iostream>
#include<conio.h>
#include<stdlib.h>
using namespace std;

struct nodo {
	char dato;
	nodo *siguiente;
};

void menu();
void insertarcola(nodo *&, nodo *&, char n);
bool colavacia(nodo *frente);
void sacarcola(nodo *&frente, nodo *&final, char &n);
int main (){
	
	int op;
	char dato;
	nodo *frente = NULL;
	nodo *fin = NULL;
	do{
		cout << "Menu" << endl;
		cout << "1. Insertar" << endl;
		cout << "2. Mostrar" << endl;
		cout << "3. Salir" << endl;
		cin>> op;
		
		switch (op){
			case 1:
				cout << "Ingresa un caracter" << endl;
				cin>> dato;
				insertarcola (frente,fin,dato);
				break;
			case 2:
				cout << "mostrando elementos de la cola:" << endl;
				while (frente != NULL){
					sacarcola (frente, fin, dato);
					if (frente != NULL){
						cout << dato << "," << endl;
					}
					else{
						cout << dato << "." << endl;
					}
				}
				system ("pause");
				break;
			case 3: break;
		}
		system ("cls");
	}while (op != 3);
	
	return 0;
}
void insertarcola (nodo *&frente, nodo *&final, char n) {
	nodo *nuevo_nodo = new nodo();
	nuevo_nodo->dato = n;
	nuevo_nodo->siguiente = NULL;
	if (colavacia(frente)){
		frente = nuevo_nodo;
	}
	else {
		final->siguiente = nuevo_nodo;
	}
}
bool colavacia (nodo *frente){
	return (frente == NULL)? true : false;
}
void sacarcola(nodo *&frente, nodo *&final, char &n){
	n = frente->dato;
	nodo *aux = frente;
	if (frente == final){
		frente = NULL;
		final = NULL;
	}
	else{
		frente = frente->siguiente;
	}
	delete aux;
}
