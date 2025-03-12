#include<iostream>

using namespace std;


struct estudiante{
	
	char nombre[];
	char materia[60];
	float nota1,nota2,nota3,promedio;

};

float calcularPromedio(float,float,float);

int main(){
	
	estudiante alumno[1];
	int i=1;
	
	for(int i=0;i<=1;i++){
	
	
	cout<<"ingrese el nombre del estudiante   :"<<i+1<<endl;cin>>alumno[i].nombre;
	cout<<"ingrese el nombre de la materia    :"<<i+1<<endl;cin>>alumno[i].materia;
	
	cout<<"ingrese el la nota 1               :"<<endl;cin>>alumno[i].nota1;
	cout<<"ingrese el la nota 2               :"<<endl;cin>>alumno[i].nota2;
	cout<<"ingrese el la nota 3               :"<<endl;cin>>alumno[i].nota3;
	
	alumno[i].promedio=calcularPromedio(alumno[i].nota1,alumno[i].nota2,alumno[i].nota3);
	
	cout<<"Nota del estudiante  "<<alumno[i].nombre<<" de la materia "<< alumno[i].materia<<" es :"<<alumno[i].promedio<<endl;
	cout<<endl;
		
}
		
	
	
	
	return 0;

}

float calcularPromedio(float nota1,float nota2,float nota3){
	
	float promedio;
	
	promedio=(nota1*0.3)+(nota2*0.3)+(nota3*0.4);
	
return promedio;
}
