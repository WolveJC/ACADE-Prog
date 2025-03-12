#include <iostream>
#include <math.h>
using namespace std ;
double x;
double a;
double b;
double c;
float Bhaskara ( double b, double c){

x= b* ( sqrt ( c));
return x;

}

int main (){
cout << "Ingrese un número para x²" << endl;
cin >> a;
cout << "Ingrese un número para x¹" << endl;
cin >> b;
cout << "Ingrese un número para x⁰" << endl;
cin >> c;
Bhaskara (b, c);
}