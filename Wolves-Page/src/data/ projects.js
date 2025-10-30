import dataflyImage from '../../assets/datafly.png'; 
import structbankImage from '../../assets/structbank.png'; 
import taskflowImage from '../../assets/taskflow.jpg'; 
import objectusrexImage from '../../assets/objectusrex.jpg';
import pysorterImage from '../../assets/pysorter.jpg'; 
import pykitchensortImage from '../../assets/pykitchensort.jpg'; 
import kitchenjsonconnectImage from '../../assets/kitchenjsonconnect.jpg'; 
import carfixImage from '../../assets/carfix.jpg'; 
export const projectsData = [
  // C++ Projects
  {
    id: "A9#kT7!pQ2$z",
    title: "DataFly",
    imageUrl: dataflyImg.default || dataflyImg,
    description:
      "Ejercicio de manejo de archivos en C++ para simular una línea de vuelo.",
    repoLink:
      "https://github.com/WolveJC/ACADE-Prog/blob/main/Curso-CPP/If-matason-fly.cpp",
  },
  {
    id: "mX4&Z1@rL8^y",
    title: "StructBank",
    imageUrl: structbankImg.default || structbankImg,
    description:
      "Programa en C++ que simula un sistema bancario usando estructuras de datos.",
    repoLink:
      "https://github.com/WolveJC/ACADE-Prog/blob/main/Curso-CPP/banco-cuenta.cpp",
  },
  {
    id: "!G7u$Q9h*V2w",
    title: "TaskFlow",
    imageUrl: taskflowImg.default || taskflowImg,
    description:
      "Manejo de tareas en C++ usando Programación Orientada a Objetos (POO).",
    repoLink:
      "https://github.com/WolveJC/ACADE-Prog/blob/main/Curso-CPP/Tareas%20completa.cpp",
  },
  {
    id: "R3^nF6#oT8@b",
    title: "Objectus Rex",
    imageUrl: objectusrexImg.default || objectusrexImg,
    description:
      "Ejercicio de POO en C++ enfocado en el diseño de clases y herencia.",
    repoLink:
      "https://github.com/WolveJC/ACADE-Prog/blob/main/Curso-CPP/Jerarqu%C3%ADa_persona.cpp",
  },

  // Python Projects
  {
    id: "zP5!L1$kW7^x",
    title: "PySorter",
    imageUrl: pysorterImg.default || pysorterImg,
    description:
      "Organizador y clasificador de archivos en Google Drive usando Python.",
    repoLink: "https://github.com/WolveJC/ACADE-Prog/tree/main/Ejercicio%201",
  },
  {
    id: "q8@H2#vM9!tY",
    title: "PyKitchenSort",
    imageUrl: pykitchensortImg.default || pykitchensortImg,
    description:
      "Práctica de manejo de archivos y algoritmos de ordenamiento para un stock de cocina usando Python.",
    repoLink: "https://github.com/WolveJC/ACADE-Prog/tree/main/Unidad%202",
  },
  {
    id: "B4^s!J7$gR1@",
    title: "Py JSON Connect",
    imageUrl: kitchenjsonconnectImg.default || kitchenjsonconnectImg,
    description:
      "Manejo de archivos JSON con Python para simular un stock con operaciones de Compra/Uso.",
    repoLink:
      "https://github.com/WolveJC/ACADE-Prog/tree/main/Unidad%203/Flask",
  },

  // Web Project
  {
    id: "X7!pR2^mQ9@z",
    title: "CarFix",
    imageUrl: carfixImg.default || carfixImg,
    description:
      "Página web para compra/venta de repuestos vehiculares (tecnologías web generales).",
    repoLink: "https://github.com/bufferring/carfix-mono",
  },
];

// Nota: Podría necesitar importar dinámicamente las imágenes aquí
// Esto depende del bundler (Webpack/Vite). Usaremos la forma más compatible
// en el ProjectCard
