#include <iostream>
#include <fstream>
using namespace std;

struct fly{
int code;
float km;
int num;
};

void recibocode(float vuela){
    string filename;
    string ext;
    fstream recibo;
    ext=".txt";
    cout << "Ingrese el nombre con el que desea guardar el archivo para el recibo del recorrido con mas pasajeros: " << endl;
    cin >> filename;
    filename+=ext;
    recibo.open(filename.c_str(),ios::out);
    if (recibo.fail()) {
        cout << "* ERROR GENERARANDO RECIBO *" << endl;
    }
    recibo << "El vuelo con mayor pasajeros recorrío: " << vuela << endl;
    cout << "Archivo Generado" << endl;
    recibo.close();
}
    
void recibokm(int vuela){
    string filename;
    fstream recibo;
    string ext;
    ext=".txt";
    cout << "Ingrese el nombre con el que desea guardar el archivo para el recibo del codigo con mayor recorrido: " << endl;
    cin >> filename;
    filename+=ext;
    recibo.open(filename.c_str(),ios::out);
    if (recibo.fail()) {
        cout << "* ERROR GENERARANDO RECIBO *" << endl;
    }
    recibo << "El vuelo con mayor pasajeros recorrío: " << vuela << endl;
    cout << "Archivo Generado" << endl;
    recibo.close();
}

int main (){
	int i;
	i=1;
	fly vuelo [i];
 for(i=1; i<=5; i++){
 	cout << "Ingrese codigo del vuelo " << i << endl;
 	cin>> vuelo[i].code;
	 cout << "Ingrese el numero de pasajeros del vuelo " << i <<endl;
	 cin >> vuelo[i].num;
 	cout << "Ingrese los kilometros que recorrera el vuelo " << i <<endl;
 	cin >> vuelo[i].km;
 }
 if (vuelo[1].km>vuelo[2].km){
 	if (vuelo[1].km > vuelo[3].km){
 		if (vuelo[1].km > vuelo[4].km){
 			if (vuelo[1].km > vuelo[5].km){
 			int vuela;
 				vuela=vuelo[1].code;
 				recibokm (vuela);
 	
			 }
		 }
	 }
}else;
if (vuelo[2].km>vuelo[3].km){
 	if (vuelo[2].km > vuelo[4].km){
 		if (vuelo[2].km > vuelo[5].km){
 			int vuela;
 				vuela=vuelo[2].code;
 				recibokm (vuela);
		 }
	 }
}else;
if (vuelo[3].km>vuelo[4].km){
 	if (vuelo[3].km > vuelo[5].km){
 		int vuela;
 			vuela=vuelo[3].code;
 			recibokm (vuela);
		 }
	 }else;
	 if (vuelo[4].km>vuelo[5].km){
 		int vuela;
 			vuela=vuelo[3].code;
 			recibokm (vuela);
	 }else;
	 	int vuela;
	 		vuela=vuelo[5].code;
 			recibokm (vuela);
if (vuelo[1].num>vuelo[2].num){
 	if (vuelo[1].num > vuelo[3].num){
 		if (vuelo[1].num > vuelo[4].num){
 			if (vuelo[1].num > vuelo[5].num){
 			int vuele;
 				vuele=vuelo[1].km;
 				recibocode (vuele);
 	
			 }
		 }
	 }
}else;
if (vuelo[2].num>vuelo[3].num){
 	if (vuelo[2].num > vuelo[4].num){
 		if (vuelo[2].num > vuelo[5].num){
 			int vuele;
 				vuela=vuelo[2].num;
 				recibocode (vuele);
		 }
	 }
}else;
if (vuelo[3].num>vuelo[4].num){
 	if (vuelo[3].num > vuelo[5].num){
 		int vuele;
 			vuele=vuelo[3].km;
 			recibocode (vuele);
		 }
	 }else;
	 if (vuelo[4].num>vuelo[5].num){
 		int vuele;
 			vuele=vuelo[4].km;
 			recibocode (vuela);
	 }else;
	 	int vuele;
	 		vuele=vuelo[5].km;
 			recibocode (vuele);

return 0;
}
