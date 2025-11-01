import React from "react";
import useCarousel from "../../hooks/ useCarousel";
import usePageTitle from "../../hooks/usePageTitle";

// Importar los componentes de las secciones
import Welcome from "../Sections/Welcome";
import Projects from "../Sections/Projects";
import AboutMe from "../Sections/AboutMe";

const MainContent = () => {
  // Llamar el hook para cambiar el titulo de la pagina
  usePageTitle('WolveJC | Portafolio y Proyectos');
  // Configurar el hook del carrusel: velocidad y tiempo de intervalo
  const { carouselRef, handleMouseEnter, handleMouseLeave, isPaused } =
    useCarousel(
      5, // Velocidad (ajusta este valor para ir más rápido o lento)
      40 // Intervalo (milisegundos)
    );

  return (
    // Contenedor principal que se desplaza:
    <div
      ref={carouselRef}
      className="flex overflow-x-hidden min-h-screen w-full relative"
      onMouseEnter={handleMouseEnter} // Pausar al entrar el mouse
      onMouseLeave={handleMouseLeave} // Reanudar al salir el mouse
    >
      {/* Indicador de Pausa (proporciona feedback visual) */}
      {isPaused && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-black/60 text-white px-4 py-2 rounded-lg z-40 text-lg font-bold tracking-widest animate-pulse">
          PAUSADO
        </div>
      )}

      {/*
                El contenido se DUPLICA para simular un bucle infinito de desplazamiento 
                de derecha a izquierda.
            */}

      {/* === COPIA 1 DEL CONTENIDO PRINCIPAL === */}
      <SectionWrapper>
        <Welcome />
      </SectionWrapper>

      <SectionWrapper>
        <Projects />
      </SectionWrapper>

      <SectionWrapper>
        <AboutMe />
      </SectionWrapper>

      {/* === COPIA 2 DEL CONTENIDO (PARA EL LOOP) === */}
      <SectionWrapper>
        <Welcome />
      </SectionWrapper>

      <SectionWrapper>
        <Projects />
      </SectionWrapper>

      <SectionWrapper>
        <AboutMe />
      </SectionWrapper>
    </div>
  );
};

// Componente utilitario para envolver cada sección (pestaña transparente)
const SectionWrapper = ({ children }) => (
  <div
    // Clases Cruciales para el Carrusel:
    // flex-shrink-0: Evita que se encojan
    // w-screen: Ocupa el 100% del ancho del viewport
    // min-h-screen: Ocupa el 100% de la altura (menos el Header)
    // Estilos de Transparencia:
    className={`
            flex-shrink-0 w-screen min-h-screen 
            flex items-center justify-center p-4 sm:p-8 
            
            // Fondo semi-transparente
            bg-black/30 backdrop-blur-sm 
            shadow-2xl border-x border-gray-700/50
        `}
  >
    {children}
  </div>
);

export default MainContent;
