import React from 'react';
import { FaJsSquare, FaHtml5, FaCss3Alt } from 'react-icons/fa';
import { SiCplusplus } from 'react-icons/si';

// 1. Importación de las URLs de las imágenes
import FlatPython from "./python.png" 
import FlatJava from "./java.png" 

// 2. CREACIÓN DE COMPONENTES CONTENEDORES
const PythonIcon = ({ className, style }) => (
    <img src={FlatPython} alt="Python Logo" className={className} style={style} />
);

const JavaIcon = ({ className, style }) => (
    <img src={FlatJava} alt="Java Logo" className={className} style={style} />
);



// Definimos la información completa de la habilidad
export const skillsData = [
    { 
        name: 'Python', 
        Icon: PythonIcon,
        percentage: 54, 
        iconColor: '', 
    },
    { 
        name: 'C++', 
        Icon: SiCplusplus, 
        percentage: 22, 
        iconColor: 'text-blue-500', 
        barColor: 'bg-orange-500' ,
    },
    { 
        name: 'JavaScript', 
        Icon: FaJsSquare, 
        percentage: 10, 
        iconColor: 'text-yellow-400',
    },
    { 
        name: 'Java', 
        Icon: JavaIcon,
        percentage: 5, 
        iconColor: '',
    },
    { 
        name: 'HTML5', 
        Icon: FaHtml5, 
        percentage: 5, 
        iconColor: 'text-orange-500',
    },
    { 
        name: 'CSS3', 
        Icon: FaCss3Alt, 
        percentage: 4, 
        iconColor: 'text-blue-600',
    },
];