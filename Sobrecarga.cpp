#include <iostream>
using namespace std;

class Tempo {
	private:
		int hour;
		int minu;
		int secu;
	public:
		Tempo (int, int, int);
		Tempo (long);
		void timer ();
		void pass();
};

Tempo :: Tempo (int c_hour, int c_minu, int c_secu){
	hour = c_hour;
	minu = c_minu;
	secu = c_secu;
}

Tempo :: Tempo(long seg){
	hour = seg/3600;
	seg %= 3600;
	minu = seg/60;
	seg %= 60;
	secu = seg % 60;
}

void Tempo :: timer(){
	cout <<"Son las: "<<hour<< " horas con " <<minu<< " minutos y "<<secu<< " segundos" <<endl;
}
void Tempo :: pass (){
	cout << "Han pasado: " <<hour<< " horas con " <<minu<< " minutos y "<<secu<< " segundos" <<endl;
}
int main (){
	Tempo tiempo(23,20,57);
	Tempo prisa (21500);
	tiempo.timer();
	prisa.pass();
	return 0;	
}

