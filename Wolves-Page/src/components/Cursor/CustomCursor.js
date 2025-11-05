// src/components/Cursor/CustomCursor.jsx (Revisado y Corregido)

import React, { useState, useEffect } from 'react';

// Estados del Cursor
const STATES = {
    TRUNK: 'trunk',
    LEAF: 'leaf',
    FLOWER: 'flower'
};

// Clase que los componentes complejos deben aplicar
const FLOWER_CLASS = 'flower-trigger'; 

const CustomCursor = () => {
    const [position, setPosition] = useState({ x: 0, y: 0 });
    const [cursorState, setCursorState] = useState(STATES.TRUNK);
    const [isPointer, setIsPointer] = useState(false); 

    // Estado para detectar si se está presionando el botón izquierdo (opcional, para FLOR)
    // Lo mantendremos en 'false' para usar FLOR solo con 'flower-trigger'
    const [isPressed, setIsPressed] = useState(false); 


    // 1. Efecto para seguir el ratón y detectar interactividad
    useEffect(() => {
        const updatePosition = (e) => {
            setPosition({ x: e.clientX, y: e.clientY });
            
            const target = e.target;
            
            // Detección del puntero (cursor: pointer)
            const pointer = target.closest('a') || target.closest('button') || target.style.cursor === 'pointer';
            
            // Detección de interacción compleja (flower-trigger)
            const isFlowerTrigger = target.closest(`.${FLOWER_CLASS}`);
            
            // Lógica de Asignación de Estado (Prioridad: FLOR > HOJA > TRONCO)
            if (isFlowerTrigger) {
                setCursorState(STATES.FLOWER);
            } else if (pointer) {
                setCursorState(STATES.LEAF);
            } else {
                setCursorState(STATES.TRUNK);
            }
        };

        // Escuchas de eventos para la interacción
        window.addEventListener('mousemove', updatePosition);
        
        return () => {
            window.removeEventListener('mousemove', updatePosition);
        };
    }, []); 

    
    // 2. Definición de Estilos Dinámicos y Animación
    let sizeClass = 'w-6 h-6'; 
    let themeClass = '';
    let transformBase = 'translate(-50%, -50%)'; // Centrado del cursor
    let transformEffect = ''; // Animación de escala/rotación

    switch (cursorState) {
        case STATES.TRUNK:
            themeClass = 'bg-amber-800/80 border-amber-900 border-4 rounded-md';
            sizeClass = 'w-4 h-4'; 
            transformEffect = 'scale(1) rotate(0deg)';
            break;

        case STATES.LEAF:
            themeClass = 'border-green-500 border-2 bg-green-500/20 rounded-full';
            sizeClass = 'w-6 h-6';
            transformEffect = 'scale(1.5)'; // Expansión
            break;

        case STATES.FLOWER:
            themeClass = 'border-pink-400 border-3 bg-white/90 rounded-full';
            sizeClass = 'w-8 h-8'; 
            transformEffect = 'scale(1) opacity(0.7)'; 
            break;

        default:
            themeClass = 'border-gray-500 bg-gray-500/50 rounded-full';
            break;
    }

    return (
        <div 
            className={`
                fixed top-0 left-0 pointer-events-none transition-all duration-300 ease-out z-[9999]
                ${sizeClass}
                ${themeClass}
            `}
            style={{ 
                // CRÍTICO: Concatenación del movimiento del ratón, el centrado, y el efecto de animación.
                transform: `
                    translate(${position.x}px, ${position.y}px) 
                    ${transformBase} 
                    ${transformEffect}
                `,
            }}
        />
    );
};

export default CustomCursor;
