#include<iostream>

using namespace std;

void tablaUnica(int);
void tablaVarias(int , int);
void tablanumero(int);
int main (){
	
	
	int numero,inicio,final;
	cout<<"ingrese un numero ";cin>>numero;
    tablanumero(numero);



	return 0;


}

void tablaUnica( int num){
	
	for( int i=1;i<=10;i++){
		
		cout<<" "<<num<<" * "<< i<<" = "<<num*i<<endl;
		
	}
	
	

}


void tablaVarias(int desde, int final){
	
	for(int inicio = desde;inicio <=final;inicio++){
		
		cout<<endl;
		
		cout<<"tabla del numero :"<<inicio<<endl;
	
		for( int num =1;num<=10;num++){
			
			cout<<inicio<<" * "<<num<<" = "<<inicio*num<<endl;
			
		}
		
	}
	

}

void tablanumero( int num){
	
	for( int i=1;i<=num;i++){
		
		cout<<" tablas de multiplicar hasta  "<<i<<endl;
		
		for( int num =1;num<=10;num++){
			
			cout<<i<<" * "<<num<<" = "<<i*num<<endl;
			
		}
	}
		
}
