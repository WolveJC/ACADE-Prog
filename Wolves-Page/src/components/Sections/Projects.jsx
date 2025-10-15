import React from 'react';
import ProjectCard from '../UI/ProjectCard';
import { projectsData } from '../../data/projects'; 

const Projects = () => {
  return (
    // Uso padding y un ancho máximo para centrar el contenido.
    <div className="p-8 md:p-12 max-w-7xl mx-auto w-full">
      
      {/* Título de la Sección */}
      <h2 className="text-5xl font-extrabold text-white mb-10 text-center tracking-wide">
        Mi <span className="text-green-300">Portafolio</span>
      </h2>
      
      {/* Subtítulo o breve descripción */}
      <p className="text-lg text-gray-300 text-center mb-12 max-w-3xl mx-auto">
        Una colección de mis trabajos más representativos. Haz clic en cualquier tarjeta para acceder al repositorio y explorar el código.
      </p>

      {/* Cuadrícula de Proyectos */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        {projectsData.map(project => (
          // Usamos la ProjectCard para cada proyecto
          <ProjectCard 
            key={project.id}
            title={project.title}
            icon={project.icon}
            repoLink={project.repoLink}
            description={project.description}
          />
        ))}
      </div>
      
    </div>
  );
};

export default Projects;