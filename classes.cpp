#include <iostream>
using namespace std;

class RectAng {
	private:
		float large;
		float anch;
	public:
		RectAng (float,float);
		void perimetro ();
		void area ();	
};

RectAng :: RectAng (float c_large, float c_anch){
	large = c_large;
	anch= c_anch;
}

void RectAng :: perimetro (){
	float c_perimetro;
	c_perimetro= (2 * large) + (2 * anch);
	cout << "El perimetro de 'Rectangulo' es: " <<c_perimetro<< endl;
}

void RectAng :: area(){
	float c_area;
	c_area = large * anch;
	cout<< "El area de 'Reactangulo' es: " <<c_area<<endl;
}
int main (){
	RectAng kuke (25,8);
	kuke.perimetro();
	kuke.area();
	return 0;	
}

