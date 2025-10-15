import React from 'react';
import useCarousel from '../../hooks/useCarousel'; // Importo el Custom Hook

// Importo los componentes de las secciones
import Welcome from '../Sections/Welcome';
import Projects from '../Sections/Projects';
import AboutMe from '../Sections/AboutMe';

const MainContent = () => {
    // Usamos el hook para obtener la referencia y los manejadores de eventos
    const { carouselRef, handleMouseEnter, handleMouseLeave, isPaused } = useCarousel(
        1.5, // Velocidad de desplazamiento (pixels por intervalo)
        40   // Tiempo del intervalo (milisegundos)
    );

    return (
        // Contenedor principal que llena la vista y gestiona el desplazamiento
        <div 
            ref={carouselRef}
            className="flex overflow-x-hidden min-h-screen w-full relative" 
            onMouseEnter={handleMouseEnter} // Pausar al entrar el mouse
            onMouseLeave={handleMouseLeave} // Reanudar al salir el mouse
        >
            {/* Indicador de Pausa (útil para feedback visual) */}
            {isPaused && (
                <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 bg-black/50 text-white px-4 py-2 rounded-lg z-40 text-sm">
                    PAUSADO
                </div>
            )}

            {/*
                PATRÓN: Duplicar las secciones
                Para simular un loop infinito de desplazamiento que va de DERECHA a IZQUIERDA,
                se duplica el contenido. Cuando el carrusel llega al final de la primera copia,
                se reinicia instantáneamente al inicio, dando la impresión de que el flujo es continuo.
            */}
            
            {/* === CONTENIDO PRINCIPAL (Copia 1) === */}
            <SectionWrapper bgColor="bg-forest-start">
                <Welcome />
            </SectionWrapper>
            
            <SectionWrapper bgColor="bg-forest-mid">
                <Projects />
            </SectionWrapper>
            
            <SectionWrapper bgColor="bg-forest-end">
                <AboutMe />
            </SectionWrapper>

            {/* === CONTENIDO DUPLICADO (Copia 2 - Para bucle infinito) === */}
            {/* NOTA: Usar los mismos colores para mantener la coherencia */}
            <SectionWrapper bgColor="bg-forest-start">
                <Welcome />
            </SectionWrapper>
            
            <SectionWrapper bgColor="bg-forest-mid">
                <Projects />
            </SectionWrapper>
            
            <SectionWrapper bgColor="bg-forest-end">
                <AboutMe />
            </SectionWrapper>
            
        </div>
    );
};

// Componente utilitario para envolver cada sección
const SectionWrapper = ({ children, bgColor }) => (
    <div 
        // Clases Cruciales para el Carrusel:
        // flex-shrink-0: No permite que el elemento se encoja
        // w-screen: Asegura que ocupe el 100% del ancho de la vista (viewport)
        // min-h-screen: Asegura que ocupe el 100% de la altura
        className={`flex-shrink-0 w-screen min-h-screen ${bgColor} flex items-center justify-center p-12`}
    >
        {children}
    </div>
);

export default MainContent;