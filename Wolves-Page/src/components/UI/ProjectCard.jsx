import React from 'react';

const ProjectCard = ({ title, icon, repoLink, description }) => {
  return (
    // Nota de novato: la tarjeta es un enlace (<a>) envuelve el contenido
    <a 
      href={repoLink} 
      target="_blank" 
      rel="noopener noreferrer" 
      aria-label={`Ver el repositorio de ${title} en GitHub`}
      
      // Estilos de Tailwind:
      // 1. Fondo oscuro semi-transparente (destaca sobre el fondo del carrusel)
      // 2. Borde y redondeado suave.
      // 3. Sombra al pasar el ratón para dar sensación de elevación.
      className="
        block p-6 rounded-xl 
        bg-black/50 hover:bg-black/70 
        border border-gray-700/80 
        transition-all duration-300 
        shadow-lg hover:shadow-xl group
        h-full flex flex-col justify-between
      "
    >
      <div>
        {/* Encabezado: Ícono y Título */}
        <div className="flex items-start space-x-4 mb-3">
          {/* El ícono que se renderiza aquí viene de projects.js */}
          <div className="flex-shrink-0 text-green-300 group-hover:text-white transition-colors">
            {React.cloneElement(icon, { className: 'w-8 h-8' })}
          </div>
          
          <h3 className="text-xl font-bold text-white group-hover:text-green-300 transition-colors leading-tight">
            {title}
          </h3>
        </div>
        
        {/* Descripción del Proyecto */}
        <p className="text-gray-400 text-sm mt-4">{description}</p>
      </div>

      {/* Enlace al Repositorio (Pie de Tarjeta) */}
      <div className="mt-6 pt-4 border-t border-gray-700/50">
        <span 
          className="
            text-sm font-semibold 
            text-green-300 
            group-hover:text-white 
            transition duration-300 
            inline-flex items-center
          "
        >
          Ver Repositorio
          {/* Ícono de flecha o código */}
          <svg className="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
        </span>
      </div>
    </a>
  );
};

export default ProjectCard;