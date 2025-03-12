#include <iostream>
#include <stdlib.h>
using namespace std;

struct persona{
	string nom, ape, nacionalidad;
	int ci, edad;
};
struct estudiante{
	string curso;
	float nota,nota2,nota3;
	float promedio;
	persona per;
  
};
struct nodo{
	nodo *siguiente;
	estudiante estu;
};

void notafinal (estudiante &estu);
void ingresarpila(nodo *&pila, estudiante estu); //Para crear pila: puntero y dirección de memoria + el dato para rellenar
void sacarpila (nodo *&pila, estudiante &estu);

int main(){
	nodo *pila=NULL;
	estudiante estu;
	int op;
	string rpt;
	
	do{
		cout << "Bienvenido" << endl;
		cout << "Seleccione una opcion:" << endl;
		cout << "1. Ingresar datos del estudiante a pila" << endl;
		cout << "2. Sacar datos de los estudiantes ingresados a pila" << endl;
		cout << "3. Ingresar datos del estudiante a cola" << endl;
		cout << "4. Sacar datos de los estudiantes ingresados a cola" << endl;
		cout << "5. Salir" << endl; 
		cin >> op;
		system ("cls");
		switch (op){
			case 1:
				do {
					cout << "Ingrese el nombre del estudiante:" << endl;
		    		cin >> estu.per.nom;
		    		cout << "Ingrese el apellido del estudiante:" << endl;
		    		cin >> estu.per.ape;
		    		cout << "Ingrese la cedula del estudiante:" << endl;
		    		cin >> estu.per.ci;
		    		cout << "Ingrese la edad del estudiante:" << endl;
		    		cin >> estu.per.edad;
		    		cout << "Ingrese la nacionalidad del estudiante:" << endl;
		    		cin >> estu.per.nacionalidad;
		    		cout << "Ingrese el curso del estudiante:" << endl;
		    		cin >> estu.curso;
		    		cout << "Ingrese la primer nota:" << endl;
		    		cin >> estu.nota;
		   			cout << "Ingrese la segunda nota:" << endl;
		    		cin >> estu.nota2;
		    		cout << "Ingrese la tercer nota:" << endl;
		    		cin >> estu.nota3;
		    		system ("cls");
		    		ingresarpila (pila, estu);
		    		cout << "¿Desea agregar mas alumnos? (s/n)" << endl;
		    		cin >> rpt;
				}while (rpt == "s");
			case 2:
				while (pila != NULL){
					cout << "Nombre del estudiante: " << estu.per.nom << endl;
	        		cout << "Apellido del estudiante: " << estu.per.ape << endl;
	        		cout << "Cedula del estudiante: " << estu.per.ci << endl;
	        		cout << "Edad del estudiante: " << estu.per.edad << endl;
	        		cout << "Nacionalidad del estudiante: " << estu.per.nacionalidad << endl;
	        		cout << "Curso:" << estu.curso << endl;
	        		notafinal (estu);
	        		cout << "Nota final: " << estu.promedio << endl;
	        		sacarpila (pila, estu);
				}
				cout << "¿Desea continuar? (s/n)" << endl;
				cin >> rpt; 
		}
	}while (rpt == "s");
	
	return 0;
}
void notafinal(estudiante &estu){
	estu.promedio = (estu.nota*0.3)+(estu.nota2*0.3)+(estu.nota3*0.4);
	if (estu.promedio>=10){
		cout << "Aprobo" << endl;
	}
	else {
		cout << "Reprobo" << endl;
	}
}
void ingresarpila (nodo *&pila, estudiante estupila){//Le agregue "&" a "nodo *pila"
	nodo *nuevo_nodo = new nodo();
	nuevo_nodo->estu = estupila;
	nuevo_nodo->siguiente = pila;//Nuevo nodo apuntando a siguiente debe ser igual a pila, bachiller
	pila = nuevo_nodo;
	cout << "Ingresando datos a la pila...." << endl;
}
void sacarpila (nodo *&pila, estudiante &estupila){
	nodo *aux = pila;
	estupila = aux->estu;
	pila = aux->siguiente;
	delete aux;
}
