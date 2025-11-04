import React, { useState, useEffect } from 'react';

// Estados del Cursor
const STATES = {
    TRUNK: 'trunk',
    LEAF: 'leaf',
    FLOWER: 'flower'
};

// Clase que los componentes complejos (Sidebar, SkillIcon, Arrows) deben aplicar
// cuando están en hover para activar el estado FLOR.
const FLOWER_CLASS = 'flower-trigger'; 

const CustomCursor = () => {
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [cursorState, setCursorState] = useState(STATES.TRUNK);

    // 1. Efecto para seguir el ratón y detectar interactividad
    useEffect(() => {
        const updatePosition = (e) => {
            setPosition({ x: e.clientX, y: e.clientY });
            
            const target = e.target;
            
            // Detección del puntero (cursor: pointer)
            const isPointer = target.closest('a') || target.closest('button') || target.style.cursor === 'pointer';
            
            // Detección de interacción compleja (Hover sobre SkillIcon, Arrows, etc.)
            const isFlowerTrigger = target.closest(`.${FLOWER_CLASS}`);
            
            // 2. Lógica de Asignación de Estado (Prioridad: FLOR > HOJA > TRONCO)
            if (isFlowerTrigger) {
                // FLOR: Interacción compleja (e.g., Lupa en Sidebar)
                setCursorState(STATES.FLOWER);
            } else if (isPointer) {
                // HOJA: Elementos de navegación estándar (a, button)
                setCursorState(STATES.LEAF);
            } else {
                // TRONCO: Estado por defecto
                setCursorState(STATES.TRUNK);
            }
        };

        window.addEventListener('mousemove', updatePosition);
        
        return () => {
            window.removeEventListener('mousemove', updatePosition);
        };
    }, []); // Dependencias vacías, solo se ejecuta una vez al montar

    
    // 3. Definición de Estilos Dinámicos y Animación
    let sizeClass = 'w-6 h-6'; // Tamaño base
    let themeClass = '';
    let transformClass = 'scale-100 opacity-100'; // Propiedades de animación

    switch (cursorState) {
        case STATES.TRUNK:
            // TRONCO: Sólido, Marrón. Gira lentamente (simula rotación al cambiar)
            themeClass = 'bg-amber-800/80 border-amber-900 border-4 rounded-md';
            sizeClass = 'w-4 h-4'; // Pequeño
            transformClass = 'scale-100 rotate-0 opacity-100';
            break;

        case STATES.LEAF:
            // HOJA: Borde Verde, Expansión (se agranda al pasar por un enlace)
            themeClass = 'border-green-500 border-2 bg-green-500/20 rounded-full';
            sizeClass = 'w-6 h-6';
            transformClass = 'scale-150 opacity-100'; // Expansión
            break;

        case STATES.FLOWER:
            // FLOR: Borde Rosa, Desvanecimiento (se hace más grande y menos sólido)
            themeClass = 'border-pink-400 border-3 bg-white/90 rounded-full';
            sizeClass = 'w-8 h-8'; // Grande
            transformClass = 'scale-100 opacity-70'; // Desvanecimiento (menos opaco)
            break;

        default:
            themeClass = 'border-gray-500 bg-gray-500/50 rounded-full';
            break;
    }

    // Nota: El truco de la animación es que 'transition-all' aplica la duración a 
    // todos los cambios de clase (tamaño, color, scale, opacity) al cambiar el cursorState.
    
    return (
        <div 
            className={`
                fixed top-0 left-0 pointer-events-none transition-all duration-300 ease-out z-[9999]
                ${sizeClass}
                ${themeClass}
            `}
            style={{ 
                // Aplicamos el movimiento y la transformación/animación en el style
                transform: `translate(${position.x}px, ${position.y}px) translate(-50%, -50%) ${transformClass}`, 
            }}
        />
    );
};

export default CustomCursor;
