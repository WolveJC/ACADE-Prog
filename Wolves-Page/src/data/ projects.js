import dataflyImg from '../assets/datafly.png';
import structbankImg from '../assets/structbank.png';
import taskflowImg from '../assets/taskflow.jpg';
import objectusrexImg from '../assets/objectusrex.jpg'; 
import pysorterImg from '../assets/pysorter.jpg';
import pykitchensortImg from '../assets/pykitchensort.jpg';
import kitchenjsonconnectImg from '../assets/kitchenjsonconnect.jpg'; // Usamos el nombre de archivo físico
import carfixImg from '../assets/carfix.jpg';
export const projectsData = [
  // C++ Projects
  {
    id: 'A9#kT7!pQ2$z',
    title: 'DataFly',
    image: dataflyImg, 
    description: 'Ejercicio de manejo de archivos en C++ para simular una línea de vuelo.',
    repoLink: 'https://github.com/WolveJC/ACADE-Prog/blob/main/Curso-CPP/If-matason-fly.cpp', 
  },
  {
    id: 'mX4&Z1@rL8^y',
    title: 'StructBank',
    image: structbankImg,
    description: 'Programa en C++ que simula un sistema bancario usando estructuras de datos.',
    repoLink: 'https://github.com/WolveJC/ACADE-Prog/blob/main/Curso-CPP/banco-cuenta.cpp', 
  },
  {
    id: '!G7u$Q9h*V2w',
    title: 'TaskFlow',
    image: taskflowImg,
    description: 'Manejo de tareas en C++ usando Programación Orientada a Objetos (POO).',
    repoLink: 'https://github.com/WolveJC/ACADE-Prog/blob/main/Curso-CPP/Tareas%20completa.cpp', 
  },
  {
    id: 'R3^nF6#oT8@b',
    title: 'Objectus Rex',
    image: objectusrexImg,
    description: 'Ejercicio de POO en C++ enfocado en el diseño de clases y herencia.',
    repoLink: 'https://github.com/WolveJC/ACADE-Prog/blob/main/Curso-CPP/Jerarqu%C3%ADa_persona.cpp', 
  },

  // Python Projects
  {
    id: 'zP5!L1$kW7^x',
    title: 'PySorter',
    image: pysorterImg,
    description: 'Organizador y clasificador de archivos en Google Drive usando Python.',
    repoLink: 'https://github.com/WolveJC/ACADE-Prog/tree/main/Ejercicio%201', 
  },
  {
    id: 'q8@H2#vM9!tY',
    title: 'PyKitchenSort',
    image: pykitchensortImg,
    description: 'Práctica de manejo de archivos y algoritmos de ordenamiento para un stock de cocina usando Python.',
    repoLink: 'https://github.com/WolveJC/ACADE-Prog/tree/main/Unidad%202', 
  },
  {
    id: 'B4^s!J7$gR1@',
    title: 'Py JSON Connect',
    image: kitchenjsonconnectImg,
    description: 'Manejo de archivos JSON con Python para simular un stock con operaciones de Compra/Uso.',
    repoLink: 'https://github.com/WolveJC/ACADE-Prog/tree/main/Unidad%203/Flask', 
  },
  
  // Web Project
  {
    id: 'X7!pR2^mQ9@z',
    title: 'CarFix',
    image: carfixImg,
    description: 'Página web para compra/venta de repuestos vehiculares (tecnologías web generales).',
    repoLink: 'https://github.com/bufferring/carfix-mono', 
  },
];

// Nota: Podría necesitar importar dinámicamente las imágenes aquí
// Esto depende del bundler (Webpack/Vite). Usaremos la forma más compatible 
// en el ProjectCard