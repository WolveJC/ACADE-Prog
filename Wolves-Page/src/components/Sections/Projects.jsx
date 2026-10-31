import React from "react";
import ProjectCard from "../UI/ProjectCard";
import { projectsData } from "../../data/projects";
import { useCarouselContext } from "../../context/GlobalCarousel";
import { chunkProjects, PROJECTS_PAGE_SIZE } from "../../utils/chunkProjects";

/* -------------------------------------------------------------
   COMPONENTE INTERNO: ProjectsPage
   -------------------------------------------------------------
   Renderiza UNA sola página de proyectos (máximo PROJECTS_PAGE_SIZE
   tarjetas).
   - Siempre mantiene un grid 5×2 fijo.
   - Si hay menos de PROJECTS_PAGE_SIZE proyectos, rellena con
     placeholders invisibles.
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

      {/* Relleno si hay menos de PROJECTS_PAGE_SIZE proyectos */}
      {Array.from({ length: PROJECTS_PAGE_SIZE - projects.length }).map(
        (_, i) => (
          <div key={`empty-${i}`} className="opacity-0 pointer-events-none" />
        )
      )}
    </div>
  );
};

/* -------------------------------------------------------------
   COMPONENTE PRINCIPAL: Projects
   -------------------------------------------------------------
   - Recibe `pageIndex`: la página que le corresponde renderizar
     dentro del carrusel (asignada por MainContent.jsx).
   - Ya NO renderiza todas las páginas: solo la que le toca.
   - Si `pageIndex` viene fuera de rango (bug de sincronización
     con MainContent.jsx), avisa en consola en vez de fallar en
     silencio o duplicar contenido.
------------------------------------------------------------- */
const Projects = ({ pageIndex = 0 }) => {
  const { isPaused } = useCarouselContext();

  // Dividir proyectos en páginas (mismo tamaño que usa MainContent.jsx)
  const pages = chunkProjects(projectsData, PROJECTS_PAGE_SIZE);

  const currentPageProjects = pages[pageIndex];

  if (!currentPageProjects) {
    console.warn(
      `[Projects] pageIndex=${pageIndex} fuera de rango (hay ${pages.length} página(s)). ` +
        `Revisa que MainContent.jsx esté generando las secciones con el mismo tamaño de página.`
    );
  }

  // El título/subtítulo son la "portada" del portafolio: deben verse
  // una sola vez. Si se repitieran en cada página, el usuario podría
  // pensar que está entrando a una sección nueva en vez de ver la
  // continuación del mismo portafolio.
  const isFirstPage = pageIndex === 0;

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
      {isFirstPage && (
        <>
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
            Una colección de mis trabajos más representativos. Haz clic en
            cualquier tarjeta para acceder al repositorio y explorar el
            código.
          </p>
        </>
      )}

      {/* === Render de SOLO la página que corresponde a esta instancia === */}
      <ProjectsPage
        projects={currentPageProjects || []}
        isPaused={isPaused}
      />
    </div>
  );
};

export default Projects;