import React from 'react';
import Avatar from '../UI/Avatar'; 

const Welcome = () => {
  return (
    <div className="text-center p-8 max-w-4xl mx-auto">
      
      {/* === Avatar === */}
      <Avatar size="large" /> 
      
      {/* === Título === */}
      <h1 className="text-6xl font-extrabold text-white mt-8 mb-4 tracking-tight">
        Hola, soy <span className="text-green-300">Tu Nombre</span>.
      </h1>
      
      {/* === Descripción === */}
      <p className="text-xl text-gray-200 max-w-2xl mx-auto leading-relaxed">
        Desarrollador Full Stack con pasión por crear soluciones web robustas y estéticas. Bienvenido a mi rincón digital, donde la lógica y la naturaleza se encuentran.
      </p>
      
      {/* === Llamada a la Acción === */}
      <div className="mt-8">
        <a 
          href="#projects" 
          // Botón en tonos forestales para que contraste con el fondo oscuro general
          className="inline-block px-8 py-3 text-lg font-semibold text-white bg-green-600 rounded-full hover:bg-green-700 transition duration-300 shadow-xl"
        >
          Explorar mi Bosque de Proyectos
        </a>
      </div>
    </div>
  );
};

export default Welcome;