import React from "react";
import ProjectCard from "../UI/ProjectCard";
import { projectsData } from "../../data/projects";
import { useCarouselContext } from "../../context/GlobalCarousel";

/* -------------------------------------------------------------
   UTILIDAD INTERNA: Dividir proyectos en páginas de 10 (5×2)
   -------------------------------------------------------------
   Esta función toma el array completo de proyectos y lo divide 
   en grupos de 10 elementos. Cada grupo representa una "página"
   del portafolio, ideal para el grid fijo 5×2.
------------------------------------------------------------- */
const chunkProjects = (arr, size = 10) => {
  const chunks = [];
  for (let i = 0; i < arr.length; i += size) {
    chunks.push(arr.slice(i, i + size));
  }
  return chunks;
};

/* -------------------------------------------------------------
   COMPONENTE INTERNO: ProjectsPage
   -------------------------------------------------------------
   Renderiza UNA sola página de proyectos (máximo 10 tarjetas).
   - Siempre mantiene un grid 5×2 fijo.
   - Si hay menos de 10 proyectos, rellena con placeholders invisibles.
   - No empuja el layout hacia abajo.
------------------------------------------------------------- */
const ProjectsPage = ({ projects, isPaused }) => {
  return (
    <div
      className="
        grid
        grid-cols-5 
        grid-rows-2 
        gap-6
      "
    >
      {projects.map((project) => (
        <ProjectCard
          key={project.id}
          title={project.title}
          imageUrl={project.imageUrl}
          repoLink={project.repoLink}
          description={project.description}
          isPaused={isPaused}
        />
      ))}

      {/* Relleno si hay menos de 10 proyectos */}
      {Array.from({ length: 10 - projects.length }).map((_, i) => (
        <div key={`empty-${i}`} className="opacity-0 pointer-events-none" />
      ))}
    </div>
  );
};

/* -------------------------------------------------------------
   COMPONENTE PRINCIPAL: Projects
   -------------------------------------------------------------
   - Divide los proyectos en páginas de 10.
   - Renderiza cada página como una sección independiente.
   - Este componente será consumido por MainContent.jsx, que 
     insertará cada página dentro del carrusel infinito.
------------------------------------------------------------- */
const Projects = () => {
  const { isPaused } = useCarouselContext();

  // Dividir proyectos en páginas de 10
  const pages = chunkProjects(projectsData, 10);

  return (
    <div
      className="
        w-full 
        max-w-7xl 
        mx-auto 
        px-6 
        md:px-12 
        py-4 
        md:py-6
      "
    >
      {/* === Título === */}
      <h2
        className="
          text-center 
          font-extrabold 
          tracking-wide 
          text-white 
          mb-6
          text-3xl 
          sm:text-4xl 
          md:text-5xl
        "
      >
        Mi <span className="text-green-300">Portafolio</span>
      </h2>

      {/* === Subtítulo === */}
      <p
        className="
          text-center 
          text-gray-300 
          mx-auto 
          max-w-3xl 
          mb-8
          text-sm
          sm:text-base
        "
      >
        Una colección de mis trabajos más representativos. Haz clic en cualquier
        tarjeta para acceder al repositorio y explorar el código.
      </p>

      {/* === Render dinámico de páginas === */}
      {pages.map((page, index) => (
        <ProjectsPage key={index} projects={page} isPaused={isPaused} />
      ))}
    </div>
  );
};

export default Projects;
