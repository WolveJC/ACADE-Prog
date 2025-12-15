import React from "react";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";
import usePageTitle from "../../hooks/usePageTitle";
import { useCarouselContext } from "../../context/GlobalCarousel";

// Importar secciones
import Welcome from "../Sections/Welcome";
import Projects from "../Sections/Projects";
import AboutMe from "../Sections/AboutMe";

// Importar el nuevo SectionWrapper
import SectionWrapper from "./SectionWrapper.jsx";

const FLOWER_CLASS = "flower-trigger";
const HOVER_ZONE_WIDTH = "80px";

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
          <SectionWrapper mode="center">
            <Welcome />
          </SectionWrapper>

          <SectionWrapper mode="panel">
            <Projects />
          </SectionWrapper>

          <SectionWrapper mode="default">
            <AboutMe />
          </SectionWrapper>

          {/* === COPIA 2 (loop) === */}
          <SectionWrapper mode="center">
            <Welcome />
          </SectionWrapper>

          <SectionWrapper mode="panel">
            <Projects />
          </SectionWrapper>

          <SectionWrapper mode="default">
            <AboutMe />
          </SectionWrapper>
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

      {/* ✅ Indicador fuera del stacking context, pero dentro del componente */}
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
