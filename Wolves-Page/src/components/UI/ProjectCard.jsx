import React from "react";

const ProjectCard = ({ title, imageUrl, repoLink, description, isPaused }) => {
  return (
    <div className="ProjectCard group relative">
      <a
        href={repoLink}
        target="_blank"
        rel="noopener noreferrer"
        aria-label={`Ver el repositorio de ${title} en GitHub`}
        className="
          block 
          mx-auto

          /* Tamaño fijo + límites dinámicos */
          min-w-[180px] 
          max-w-[260px]
          w-full
          h-[150px] sm:h-[120px] md:h-[135px]
          p-4 sm:p-5
          rounded-xl 
          bg-black/50 hover:bg-black/70 
          border border-gray-700/80 
          transition-all duration-300 
          shadow-lg hover:shadow-2xl 
          flex flex-col
          justify-between 
          leaf-trigger
        "
      >
        {/* Encabezado */}
        <div className="flex items-start space-x-4">
          <div className="shrink-0 w-10 h-10 sm:w-12 sm:h-12">
            <img
              src={imageUrl}
              alt={`Logo de ${title}`}
              className="
                w-full h-full 
                object-cover 
                rounded-md 
                border border-gray-600 
                group-hover:scale-105 
                transition-transform
              "
            />
          </div>

          <h3
            className="
              text-base sm:text-lg 
              font-bold 
              text-white 
              group-hover:text-green-300 
              transition-colors 
              leading-tight 
              break-words
            "
          >
            {title}
          </h3>
        </div>

        {/* Enlace */}
        <div className="mt-2 pt-2 border-t border-gray-700/50">
          <span
            className="
              text-xs sm:text-sm 
              font-semibold 
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

      {/* Tooltip flotante */}
      {isPaused && (
        <div
          className="
            absolute 
            bottom-full left-1/2 -translate-x-1/2 
            mb-2           
            w-64 
            p-4 
            bg-black/80 
            text-gray-200 
            rounded-xl 
            shadow-xl 
            border border-gray-700 
            opacity-0 
            group-hover:opacity-100 
            transition-opacity 
            pointer-events-none 
            z-50
          "
        >
          {description}
        </div>
      )}
    </div>
  );
};

export default ProjectCard;
