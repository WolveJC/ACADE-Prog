import { FaPython, FaJava, FaJsSquare, FaHtml5, FaCss3Alt } from 'react-icons/fa';
import { SiCplusplus } from 'react-icons/si';

// Definimos la información completa de la habilidad
export const skillsData = [
    { 
        name: 'Python', 
        Icon: FaPython, 
        percentage: 54, 
        iconColor: 'text-yellow-400', 
        barColor: 'bg-yellow-500' // Barra color amarillo
    },
    { 
        name: 'C++', 
        Icon: SiCplusplus, 
        percentage: 22, 
        iconColor: 'text-blue-500', 
        barColor: 'bg-orange-500' // Barra color naranja 
    },
    { 
        name: 'JavaScript', 
        Icon: FaJsSquare, 
        percentage: 10, 
        iconColor: 'text-yellow-400', 
        barColor: 'bg-red-600' // Barra color rojo
    },
    { 
        name: 'Java', 
        Icon: FaJava, 
        percentage: 5, 
        iconColor: 'text-red-500', 
        barColor: 'bg-red-600' // Barra color rojo
    },
    { 
        name: 'HTML5', 
        Icon: FaHtml5, 
        percentage: 5, 
        iconColor: 'text-orange-500', 
        barColor: 'bg-red-600' // Barra color rojo
    },
    { 
        name: 'CSS3', 
        Icon: FaCss3Alt, 
        percentage: 4, 
        iconColor: 'text-blue-600', 
        barColor: 'bg-red-600' // Barra color rojo
    },
];