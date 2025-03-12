#include <iostream>
#include <string>
#include <fstream>
#include <stack>
using namespace std;

class Persona {
	public:
		string nombre;
		string apellido;
		int edad;
		int cedula;
		int telefono;
		Persona (string nom, string ape, int _edad, int ci, int tel){
			nombre=nom;
			apellido=ape;
			edad=_edad;
			cedula=ci;
			telefono=tel;
		}
};

class Banco {
	private:
		stack<Persona> personas;
	public:
		void registrarPersona(){
			string nombre;
		    string apellido;
		    int edad;
		    int cedula;
		    int telefono;
		    cout << "Ingrese el Nombre: " << endl;
		    getline (cin, nombre);
		    cout << "Ingrese el Apellido:" << endl;
		    getline (cin, apellido);
		    cout << "Ingrese la edad:" << endl;
		    cin >> edad;
		    cout << "Ingrese la cedula:" << endl;
		    cin >> cedula;
		    cout << "Ingrese el numero de telefono: " << endl;
		    cin >> telefono;
		    cin.ignore();
		    
		    Persona nuevapersona(nombre,apellido,edad,cedula,telefono);
		    personas.push(nuevapersona);
		    cout << "Persona registrada." << endl;
		    system ("cls");
		}
		void mostrarpersonas(){
			if (personas.empty()){
				cout << "No hay personas registradas" << endl;
				return;
			}
			stack<Persona> temp = personas;
			cout << "Personas registradas: ";
			while (!temp.empty()){
				Persona p = temp.top();
				cout << "Nombre: " << p.nombre << ", Apellido: " << p.apellido << ", Edad: " << p.edad << ", Cedula: " << p.cedula << ", Telefono: " << p.telefono << "\n";
				temp.pop();
			}
		}		
};

int main(){
	Banco banco;
	int op;
	do{
		cout << "\n--- Menu ---\n";
            cout << "1. Registrar persona\n";
            cout << "2. Mostrar personas registradas\n";
            cout << "3. Salir\n";
            cout << "Seleccione una opcion: ";
            cin >> op;
            cin.ignore();
            
            switch (op){
            	case 1:
				   banco.registrarPersona();
            	   break;
            	case 2:
            		banco.mostrarpersonas();
            		break;
            	case 3:
            		cout << "Saliendo..." << endl;
            		break;
            	default:
            		cout << "Opcion invalida" << endl;
            		
			}
			
	}while(op != 3);
	return 0;
}