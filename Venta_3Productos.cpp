#include<iostream>

#include<fstream>

using namespace std;


struct productos {

    
string nomp;
    
int cod;
int pre;
int exis;

};


struct persona {

   
char nom[45];
    
char ape[45];
    
int cedula;
    
int tel;
    
double credito;

};


void recibo ();



int main()
{
int cant;
int op;
    
int ven;
    
int com;
    

productos merca[1];
    
for (int i=1; i<=3; i++) {

        
cout << "Nombre del producto"<< i << ":"  << endl;
        
cin >> merca[i].nomp;
        
cout << "Código del producto" << i << ":" << endl;
        
cin >> merca[i].cod;
        
cout << "Precio del producto" << i << ":" << endl;
        
cin >> merca[i].pre;
        
cout << "Existencia" << i << ":" << endl;
        
cin >> merca[i].exis;
    
}

    

persona cliente;
    
cout << "Nombre de la persona: " << endl;
    
cin >> cliente.nom;
    
cout << "Apellido de la persona: " << endl;
    
cin >> cliente.ape;
    
cout << "Cédula de la persona: " << endl;
    
cin >> cliente.cedula;
    
cout << "Teléfono de la persona: " << endl;
    
cin >> cliente.tel;
    
cout << "Credito de la persona: " << endl;
    
cin >> cliente.credito;

    
cout << "Bienvenido, elige una opción:" << endl;
    
cout << "1. " << merca[1].nomp << endl;
    
cout << "2. " << merca[2].nomp << endl;
    
cout << "3. " << merca[3].nomp << endl;
    
cout << "4. " << "salir"  << endl;
    
cin >> op;
    
    
switch(op){
    
    

case 1: 
    
  
  
cout << "Producto seleccionado: " << merca[1].nomp << endl; 
cout << "Existen actualmente: " << merca[1].exis << endl; 
cout << "Tiene un precio de: " << merca[1].pre << endl;
cout << "El cliente posee un crédito de: " << cliente.credito << endl;
cout << "¿Desea comprar este producto?" << endl;
cout << "1. Si" << endl;
    
cout << "2. No" << endl;
    
cin >> ven;
    

while (ven=1){
     
      cout << "¿Cuanto desea adquirir de este producto?" << endl;
      cin >> cant;
      
      };}}
            
