#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
using namespace std;

// Parametros
const double Lx = 1.0, Ly = 1.0;  // Dimensiones de la placa
const double T_left = 100, T_right = 50;  // Temperaturas en los bordes izquierdo y derecho
const double T_top = 75, T_bottom = 25;  // Temperaturas en los bordes superior e inferior
const double alpha = 0.01;  // Difusividad térmica
const int nx = 50, ny = 50;  // Número de puntos espaciales
const int nt = 1000;  // Número de puntos temporales
const double dx = Lx / (nx - 1), dy = Ly / (ny - 1);
const double dt = 0.01;  // Paso de tiempo

void initialize_temperature(vector<vector<double> >& T) {
    for (int i = 0; i < nx; ++i) {
        for (int j = 0; j < ny; ++j) {
            T[i][j] = 20.0;  // Temperatura inicial
        }
    }
    for (int i = 0; i < nx; ++i) {
        T[i][0] = T_left;
        T[i][ny-1] = T_right;
    }
    for (int j = 0; j < ny; ++j) {
        T[0][j] = T_top;
        T[nx-1][j] = T_bottom;
    }
}

void solve_heat_equation(vector<vector<double> >& T) {
    for (int n = 0; n < nt; ++n) {
        vector<vector<double> > Tn = T;
        for (int i = 1; i < nx-1; ++i) {
            for (int j = 1; j < ny-1; ++j) {
                T[i][j] = Tn[i][j] + alpha * dt * (
                    (Tn[i+1][j] - 2*Tn[i][j] + Tn[i-1][j]) / (dx*dx) +
                    (Tn[i][j+1] - 2*Tn[i][j] + Tn[i][j-1]) / (dy*dy)
                );
            }
        }
    }
}

void save_to_file(const vector<vector<double> >& T, const string& filename) {
    ofstream file;
    file.open(filename.c_str());  // Aseguramos abrir el archivo con c_str()
    if (!file) {
        cerr << "Error abriendo el archivo para escribir.\n";
        return;
    }
    for (size_t i = 0; i < T.size(); ++i) {  // Reemplazo el uso de range-based for
        for (size_t j = 0; j < T[i].size(); ++j) {
            file << T[i][j] << " ";
        }
        file << "\n";
    }
    file.close();
}

int main() {
    vector<vector<double> > T(nx, vector<double>(ny));
    initialize_temperature(T);
    solve_heat_equation(T);
    save_to_file(T, "temperature_distribution.txt");
    cout << "Distribucion de temperatura guardada en 'temperature_distribution.txt'\n";
    return 0;
}
