#include <iostream>
using namespace std;

//Clases
class persona{
	private:
		string nom,ap;
		int ci, age;
	public:
		persona ();
		~persona();
		void ter_setpersona (string, string, int, int);
		string ter_getnom ();
		string ter_getap ();
		int ter_getci ();
		int ter_getage ();
		virtual void show_pipol();
};

class trabajador : public persona {
	private:	
		string puesto;
		float salario;
	public:
		trabajador();
		~trabajador();
		void ter_setjob(string, string, int, int, string, float);
		string ter_getpuesto();
		float ter_getsalario();
		void show_job();
};

class stu : public persona{
	private:
		string curso;
		float nota1, nota2, nota3, prom;
	public:
		stu();
		~stu();
		float set_promedio(float,float,float);
		void ter_setestu(string, string, int, int, string, float, float, float);
		string ter_getcuerso();
		float ter_getprom();
		void show_estu();
};

class uni : public stu{
	private:
		string carear;
		string title;
	public:
		uni();
		~uni();
		void ter_setuni(string, string, int, int, string, float, float, float, string, string);
		string ter_getcarear();
		string ter_gettitle();
		void show_unity();
		
};

//Extras
persona :: persona(){}

persona :: ~persona (){}

trabajador::trabajador(){}

trabajador::~trabajador(){}

stu::stu(){}

stu::~stu(){}

uni::uni(){}

uni::~uni(){}

float stu::set_promedio(float not1, float not2, float not3){
	prom= (not1 + not2 + not3)/3;
	return prom;
}

//Polimorfismo

void persona::show_pipol(){
	cout << "Nombre: " << nom <<endl;
	cout << "Apellido: " << ap <<endl;
	cout << "Cedula de identidad: " << ci <<endl;
	cout << "Edad: " << age <<endl;
}

void trabajador::show_job(){
	cout << "-Empleado-"<<endl;
	persona::show_pipol();
	cout << "Cargo: " << puesto <<endl;
	cout << "Salario: " << salario << "Bs." <<endl;
}

void stu::show_estu(){
	cout << "-Estudiante-" <<endl;
	persona::show_pipol();
	cout << "Curso: " << curso <<endl;
	cout << "Notas: " << nota1 << "/" << nota2 << "/" << nota3 <<endl;
	cout << "Promedio: " << prom << endl;
}

void uni::show_unity(){
	cout << "-Estudiante universitario"<< endl;
	persona::show_pipol();
	stu::show_estu();
	cout << "Carreara: " << carear <<endl;
	cout << "Grado de formación: " << title <<endl;
	
}
//Sets
void persona::ter_setpersona(string set_nom, string set_ap, int set_ci, int set_age){
	nom = set_nom;
	ap = set_ap;
	ci = set_ci;
	age = set_age;
}

void trabajador::ter_setjob(string set_nom, string set_ap, int set_ci, int set_age, string set_puesto, float set_salario){
	ter_setpersona(set_nom, set_ap, set_ci, set_age);
	puesto = set_puesto;
	salario = set_salario;
}

void stu::ter_setestu(string set_nom, string set_ap, int set_ci, int set_age, string set_curso, float not1, float not2, float not3){
	ter_setpersona(set_nom, set_ap, set_ci, set_age);
	curso = set_curso;
	nota1 = not1;
	nota2 = not2;
	nota3 = not3;
	prom = set_promedio(not1, not2, not3);
}

void uni::ter_setuni(string set_nom, string set_ap, int set_ci, int set_age, string set_curso, float not1, float not2, float not3, string set_carear, string set_title) {
    ter_setpersona(set_nom, set_ap, set_ci, set_age);
    ter_setestu(set_nom, set_ap, set_ci, set_age, set_curso, not1, not2, not3);
    carear = set_carear;
    title = set_title;
}
//Gets
string persona::ter_getnom(){
	return nom;
}

string persona::ter_getap(){
	return ap;
}

int persona::ter_getci(){
	return ci;
}

int persona::ter_getage(){
	return age;
}

string trabajador::ter_getpuesto(){
	return puesto;
}

float trabajador::ter_getsalario(){
	return salario;
}

string stu::ter_getcuerso(){
	return curso;
}

float stu::ter_getprom(){
	return prom;
}

string uni::ter_getcarear(){
	return carear;
}

string uni::ter_gettitle(){
	return title;
}

int main (){
	trabajador* emp = new trabajador();
    emp->ter_setjob("Mario", "Garcia", 4567233, 34, "Obrero", 130);

    stu* estudiante = new stu();
    estudiante->ter_setestu("Adol", "Cristin", 30665344, 18, "Castellano", 16, 13, 14);

    uni* estUni = new uni();
    estUni->ter_setuni(" Juan", "Pérez", 12345678, 20, "Ingeniería", 18, 17, 19, "Ingeniería de Sistemas", "Licenciado");
    emp->show_job();
    estudiante->show_estu();
    estUni->show_unity();

    // Liberar memoria
    delete emp;
    delete estudiante;
    delete estUni;

    return 0;
}
