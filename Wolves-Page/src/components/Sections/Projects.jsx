import React from "react";
import ProjectCard from "../UI/ProjectCard";
import { projectsData } from "../../data/projects";
import { useCarouselContext } from "../../context/GlobalCarousel";

const Projects = () => {
  const { isPaused } = useCarouselContext();
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

      {/* === Grid 3×3 con altura fija === */}
      <div
        className="
          grid
          grid 
          grid-cols-5 
          grid-rows-2 
          gap-6
          "
      >
        {projectsData.map((project) => (
          <ProjectCard
            key={project.id}
            title={project.title}
            imageUrl={project.imageUrl}
            repoLink={project.repoLink}
            description={project.description}
            isPaused={isPaused}
          />
        ))}

        {/* === Espacios vacíos para completar 3×3 si hay menos de 9 === */}
        {Array.from({ length: Math.max(0, 9 - projectsData.length) }).map(
          (_, i) => (
            <div key={`empty-${i}`} className="opacity-0 pointer-events-none" />
          )
        )}
      </div>
    </div>
  );
};

export default Projects;
