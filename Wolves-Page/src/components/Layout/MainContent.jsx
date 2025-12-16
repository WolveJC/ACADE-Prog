import React from "react";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";
import usePageTitle from "../../hooks/usePageTitle";
import { useCarouselContext } from "../../context/GlobalCarousel";

// Secciones fijas
import Welcome from "../Sections/Welcome";
import AboutMe from "../Sections/AboutMe";

// Importar ProjectCard y datos
import Projects from "../Sections/Projects"; // ahora genera páginas dinámicas
import { projectsData } from "../../data/projects";

// Importar SectionWrapper
import SectionWrapper from "./SectionWrapper.jsx";

const FLOWER_CLASS = "flower-trigger";
const HOVER_ZONE_WIDTH = "80px";

// -------------------------------------------------------------
// Utilidad interna: dividir proyectos en páginas de 10
// -------------------------------------------------------------
const chunkProjects = (arr, size = 10) => {
  const chunks = [];
  for (let i = 0; i < arr.length; i += size) {
    chunks.push(arr.slice(i, i + size));
  }
  return chunks;
};

const MainContent = () => {
  usePageTitle("WolveJC | Portafolio y Proyectos");

  const {
    carouselRef,
    togglePause,
    startAcceleration,
    stopAcceleration,
    isPaused,
    currentSpeed,
  } = useCarouselContext();

  const SIDEBAR_WIDTH = "64px";
  const HEADER_HEIGHT = "64px";
  const isAccelerating = Math.abs(currentSpeed) > 5.5;

  // -------------------------------------------------------------
  // Generar páginas dinámicas de proyectos
  // -------------------------------------------------------------
  const projectPages = chunkProjects(projectsData, 10);

  // -------------------------------------------------------------
  // Construir TODAS las secciones del carrusel
  // -------------------------------------------------------------
  const sections = [
    { component: <Welcome />, mode: "center" },
    ...projectPages.map((page, i) => ({
      component: <Projects pageIndex={i} />, // Projects.jsx ya sabe renderizar la página correcta
      mode: "panel",
    })),
    { component: <AboutMe />, mode: "default" },
  ];

  return (
    <>
      {/* Contenedor principal del carrusel */}
      <div className="relative w-full h-[calc(100dvh-64px)] overflow-hidden">
        
        {/* Carrusel */}
        <div
          ref={carouselRef}
          className="flex overflow-x-hidden h-full w-full relative"
          onClick={togglePause}
        >
          {/* === COPIA 1 === */}
          {sections.map((sec, index) => (
            <SectionWrapper key={index} mode={sec.mode}>
              {sec.component}
            </SectionWrapper>
          ))}

          {/* === COPIA 2 (loop infinito) === */}
          {sections.map((sec, index) => (
            <SectionWrapper key={`copy-${index}`} mode={sec.mode}>
              {sec.component}
            </SectionWrapper>
          ))}
        </div>

        {/* Flecha IZQUIERDA */}
        <ArrowButton
          side="left"
          height={HEADER_HEIGHT}
          width={SIDEBAR_WIDTH}
          onStart={() => startAcceleration(-1)}
          onStop={stopAcceleration}
        />

        {/* Flecha DERECHA */}
        <ArrowButton
          side="right"
          height={HEADER_HEIGHT}
          width={SIDEBAR_WIDTH}
          onStart={() => startAcceleration(1)}
          onStop={stopAcceleration}
        />
      </div>

      {/* Indicador de velocidad / pausa */}
      {(isPaused || isAccelerating) && (
        <div
          className="
            fixed 
            top-[100px] 
            left-1/2 
            -translate-x-1/2 
            bg-black/60 
            text-white 
            px-4 py-2 
            rounded-lg 
            z-[9999] 
            text-base 
            font-bold 
            tracking-widest 
            animate-pulse 
            pointer-events-none
          "
        >
          {isPaused
            ? "PAUSADO"
            : `VELOCIDAD: ${Math.abs(currentSpeed).toFixed(1)}x`}
        </div>
      )}
    </>
  );
};

// -------------------------------------------------------------
// Flechas de aceleración
// -------------------------------------------------------------
const ArrowButton = ({ side, width, height, onStart, onStop }) => {
  const Icon = side === "left" ? FaChevronLeft : FaChevronRight;

  return (
    <div
      className={`
        absolute top-0 bottom-0 flex items-center justify-center cursor-pointer 
        opacity-0 hover:opacity-100 transition duration-300 
        z-30
        ${FLOWER_CLASS}
      `}
      style={{
        marginTop: height,
        width: HOVER_ZONE_WIDTH,
        left: side === "left" ? width : "auto",
        right: side === "right" ? "0" : "auto",
      }}
      onMouseEnter={onStart}
      onMouseLeave={onStop}
    >
      <Icon
        className="text-white text-6xl select-none pointer-events-none transition duration-300"
        style={{
          transform: side === "left" ? "translateX(10px)" : "translateX(-10px)",
        }}
      />
    </div>
  );
};

export default MainContent;
