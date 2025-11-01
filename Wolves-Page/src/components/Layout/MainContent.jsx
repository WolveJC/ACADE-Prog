import React from "react";
import usePageTitle from "../../hooks/usePageTitle";
// Importar el contexto en lugar del hook directo
import { useCarouselContext } from "../../context/GlobalCarousel"; 

// Importar los componentes de las secciones
import Welcome from "../Sections/Welcome";
import Projects from "../Sections/Projects";
import AboutMe from "../Sections/AboutMe";

const MainContent = () => {
  // Llamar el hook para cambiar el titulo de la pagina
  usePageTitle("WolveJC | Portafolio y Proyectos");
  
  // CONSUMIR EL CONTEXTO: Obtenemos todas las funciones y estados
  const { 
    carouselRef, 
    handleMouseEnter, 
    handleCarouselMouseLeave,
    startAcceleration,
    stopAcceleration,
    isPaused, 
    currentSpeed 
  } = useCarouselContext();

  // Constantes de diseño (deben coincidir con Header y Sidebar)
  const SIDEBAR_WIDTH = '64px'; // w-16
  const HEADER_HEIGHT = '64px'; // Aproximadamente p-4

  // Lógica para mostrar feedback de velocidad (si es mayor a la velocidad base de 5)
  const isAccelerating = Math.abs(currentSpeed) > 5.5; 

  return (
    // Contenedor principal para el carrusel y las flechas
    <div className="relative w-full min-h-screen">
        
        {/* 1. Indicador de Feedback (Pausa / Velocidad) */}
        {(isPaused || isAccelerating) && (
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-black/60 text-white px-4 py-2 rounded-lg z-40 text-lg font-bold tracking-widest animate-pulse">
                {isPaused ? 'PAUSADO' : `VELOCIDAD: ${Math.abs(currentSpeed).toFixed(1)}x`}
            </div>
        )}

        {/* 2. Contenedor del Carrusel Desplazable */}
        <div
            ref={carouselRef}
            className="flex overflow-x-hidden min-h-screen w-full relative"
            onMouseEnter={handleMouseEnter} // Pausa con hover
            onMouseLeave={handleCarouselMouseLeave} // Reanudar al salir
        >
            {/* === COPIA 1 DEL CONTENIDO PRINCIPAL === */}
            <SectionWrapper><Welcome /></SectionWrapper>
            <SectionWrapper><Projects /></SectionWrapper>
            <SectionWrapper><AboutMe /></SectionWrapper>

            {/* === COPIA 2 DEL CONTENIDO (PARA EL LOOP) === */}
            <SectionWrapper><Welcome /></SectionWrapper>
            <SectionWrapper><Projects /></SectionWrapper>
            <SectionWrapper><AboutMe /></SectionWrapper>
        </div>
        
        {/* 3. Flecha de Navegación IZQUIERDA (<) */}
        <ArrowButton 
            side="left" 
            height={HEADER_HEIGHT} 
            width={SIDEBAR_WIDTH}
            onStart={() => startAcceleration(-1)} // Acelera atrás
            onStop={stopAcceleration}
        />

        {/* 4. Flecha de Navegación DERECHA (>) */}
        <ArrowButton 
            side="right" 
            height={HEADER_HEIGHT} 
            width={SIDEBAR_WIDTH}
            onStart={() => startAcceleration(1)} // Acelera adelante
            onStop={stopAcceleration}
        />

    </div>
  );
};


// Componente para las Flechas de Aceleración
const ArrowButton = ({ side, width, height, onStart, onStop }) => {
    // La barra de skills debe SUPERPONERSE a la flecha izquierda
    const zIndex = side === 'left' ? 'z-30' : 'z-30'; 

    return (
        <div
            // POSICIONAMIENTO Y TAMAÑO PARA OCUPAR EL ESPACIO RESTANTE
            className={`
                absolute top-0 bottom-0 flex items-center justify-center cursor-pointer 
                opacity-0 hover:opacity-100 transition duration-300 
                ${side === 'left' ? 'left-0' : 'right-0'} // Posición
                ${zIndex} // Aseguramos que la flecha izquierda no bloquee la Sidebar
            `}
            style={{ 
                // Aseguramos que el área clicable empiece debajo del Header
                marginTop: height, 
                // El ancho de la columna clicleable es la mitad de la pantalla - el ancho de la Sidebar/Controles
                width: `calc(50vw - ${width})`, 
            }}
            onMouseEnter={onStart}
            onMouseLeave={onStop}
        >
            <span 
                className={`
                    text-white text-9xl font-thin select-none pointer-events-none 
                    text-shadow-lg // Opcional: añade sombra al texto para visibilidad
                `}
                // Posiciona el símbolo de flecha justo en el borde de la Sidebar (Izquierda) o en el borde derecho (Derecha)
                style={{ 
                    transform: side === 'left' ? `translateX(${width})` : `translateX(-${width})`, 
                }}
            >
                {side === 'left' ? '<' : '>'}
            </span>
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
            shadow-2xl border-x border-
gray-700/50
        `}
  >
    {children}
  </div>
);

export default MainContent;