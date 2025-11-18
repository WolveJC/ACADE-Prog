import React from "react";
const ProjectCard = ({ title, imageUrl, repoLink, description }) => {
  return (
    <a
      href={repoLink}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={`Ver el repositorio de ${title} en GitHub`}
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
        {/* Encabezado: IMAGEN y Título */}{" "}
        <div className="flex items-start space-x-4 mb-3">
          {/* Renderizamos la IMAGEN de la aplicación (solo si la URL fue encontrada) */}
          {
            <div className="shrink-0 w-10 h-10">
              <img
                src={imageUrl}
                alt={`Logo de ${title}`}
                className="w-full h-full object-cover rounded-md border border-gray-600 group-hover:scale-105 transition-transform"
              />
            </div>
          }

          <h3 className="text-xl font-bold text-white group-hover:text-green-300 transition-colors leading-tight">
            {title}
          </h3>
        </div>
        {/* Descripción del Proyecto */}
        <p className="text-gray-400 text-sm mt-4">{description}</p>
      </div>

      {/* Enlace al Repositorio */}
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
          <svg
            className="w-4 h-4 ml-1 transform group-hover:translate-x-1 transition-transform"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M14 5l7 7m0 0l-7 7m7-7H3"
            ></path>
          </svg>
        </span>
      </div>
    </a>
  );
};

export default ProjectCard;
