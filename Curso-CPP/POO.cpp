#include <iostream>
#include <string>
using namespace std;

//Un programa que haga login de acceso, ingrese a menú, que pueda hacer cambio y recuperación de clave y utilece 2 preguntas secretas, multiplique dos numeros y muestre un mensaje n cantidad de veces n=a*b

class loger {
	protected: 
		string usser, contra, as1, as2, r1, r2;
	public:
		loger(string, string, string, string, string, string);
		string stich(string, string, string, string, string);
};

loger::loger (string c_usser, string c_contra, string c_as1, string c_as2, string c_r1, string c_r2){
	usser=c_usser;
	contra= c_contra;
	as1=c_as1;
	as2=c_as2;
	r1=c_r1;
	r2=c_r2;
}


string stich(string as1,string as2, string r1, string r2, string contra){
	cout << "" << r1<<endl;
	r1=as1;
	cin >> r1;
	do {
		cout << "Respuesta correcta!"<< endl;
		cout << "" <<r2<<endl;
		r2=as2;
		do {
			cout<< "Repuesta correcta!"<<endl;
			cout << "Ingrese nueva contaseña:"<<endl;
			cin >> contra;
		}while (r2==as2);
	}while (r1==as1);
}
void multi (int a, int b){
	int i,n;
	string sentence;
	cout << "Ingrese un numero:"<<endl;
	cin >>a;
	cout << "Ingrese otro numero:"<<endl;
	cin >> b;
	n=a*b;
	cout << "Ingrese una frase:"<<endl;
	cin>> sentence;
	i=1;
	for(i=1; i<=n; i++) {
		cout<<""<<sentence<< "\n"<<endl;
	}
}
string c_r1,c_as1,c_r2,c_as2, c_contra;
int op;
int main (){
	cout << "Pregunta 1:"<<endl;
	cin >> c_r1;
	cout << "Respuesta:"<<endl;
	cin >> c_as1;
	cout<<"Pregunta 2:"<<endl;
	cin >> c_r2;
	cout << "Respuesta:"<<endl;
	cin >> c_as2;
	loger("Fullo355", "346464", c_as1,c_as2,c_r1,c_r2);
	cout<< "-MENU-"<<endl;
	cout<< "1. Cambiar contraseña"<<endl;
	cout<< "2. Multiplicar mensaje"<<endl;
	cin>>op;
	switch(op) {
		case 1:
			stich (c_as1,c_as2,c_r1,c_r2,c_contra);
	default:
}
	return 0;
}
