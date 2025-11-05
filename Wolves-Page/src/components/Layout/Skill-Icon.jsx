import React, { useRef, useState, useEffect } from 'react';

// Constantes de Magnificación (lógica de la lupa)
const INFLUENCE_RADIUS = 120; // Radio en píxeles donde el ratón afecta al ícono
const MAX_SCALE = 1.6; // Escala máxima: 160%

// Función para determinar el color de la barra según el porcentaje
const getBarColor = (percentage) => {
    if (percentage >= 70) return 'bg-green-500'; // Verde (70-100%)
    if (percentage >= 50) return 'bg-yellow-500'; // Amarillo (50-69%)
    if (percentage >= 20) return 'bg-orange-500'; // Naranja (20-49%)
    return 'bg-red-600'; // Rojo (0-19%)
};


const SkillIcon = ({ skill, mousePosition, sidebarRef, isSidebarHovering }) => {
    const iconRef = useRef(null);
    const [isFocused, setIsFocused] = useState(false); // Estado para el hover en el ícono
    const [animatedPercentage, setAnimatedPercentage] = useState(0); // Estado para el conteo animado
    const { name, Icon, percentage, iconColor } = skill; 

    let scale = 1;

    // --- 1. CÁLCULO DE LA ESCALA (LUPA) ---
    // Este cálculo define el valor de 'scale' basado en la distancia del ratón
    if (iconRef.current && sidebarRef.current && mousePosition) {
        const rect = iconRef.current.getBoundingClientRect();
        
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const distance = Math.sqrt(
            Math.pow(centerX - mousePosition.x, 2) + Math.pow(centerY - mousePosition.y, 2)
        );
        
        if (distance < INFLUENCE_RADIUS) {
            const influenceFactor = 1 - distance / INFLUENCE_RADIUS;
            scale = 1 + (MAX_SCALE - 1) * influenceFactor;
        }
    }

    // La barra de experiencia se muestra si el mouse está sobre el Sidebar Y el ícono está enfocado
    const showExperienceBar = isFocused && isSidebarHovering;


    // --- 2. LÓGICA DE ANIMACIÓN DE CONTEO Y LLENADO DE BARRA ---
    useEffect(() => {
        if (showExperienceBar) {
            let start = null;
            const duration = 800; // Duración total de la animación de llenado (0.8s)

            const step = (timestamp) => {
                if (!start) start = timestamp;
                const progress = timestamp - start;
                
                // Calcula el valor actual que avanza de 0 hasta el porcentaje real
                const current = Math.min(percentage, (progress / duration) * percentage);
                setAnimatedPercentage(Math.round(current));
                
                // Continúa la animación hasta alcanzar la duración
                if (progress < duration) {
                    requestAnimationFrame(step);
                }
            };

            // Inicia la animación de conteo
            requestAnimationFrame(step);
        } else {
            // Reinicia la barra a 0 al salir del hover
            setAnimatedPercentage(0); 
        }
    }, [showExperienceBar, percentage]); // Depende del estado del hover y del porcentaje final

    // El color actual de la barra se determina dinámicamente
    const currentBarColor = getBarColor(animatedPercentage); 

    return (
        <div 
            key={name} 
            className="relative w-full flex items-center justify-center h-10 transition-transform duration-100 ease-out" 
            onMouseEnter={() => setIsFocused(true)}
            onMouseLeave={() => setIsFocused(false)}
        >
            {/* Contenedor del Ícono (Aplica la escala de la Lupa) */}
            <div ref={iconRef} className="flex justify-center items-center">
                <Icon 
                    className={`w-7 h-7 ${iconColor} transition-all duration-100 ease-out`}
                    style={{ transform: `scale(${scale})` }} 
                />
            </div>
            
            {/* BARRA DE EXPERIENCIA FLOTANTE (Animada y Sincronizada) */}
            {showExperienceBar && (
                <div 
                    // Posicionamiento correcto a la DERECHA del sidebar (left-full)
                    className={`
                        absolute left-full top-1/2 -translate-y-1/2 ml-4 flex items-center w-48 z-50 bg-gray-900/95 p-2 rounded-md shadow-xl
                        transition-opacity duration-300 ease-in-out 
                        ${showExperienceBar ? 'opacity-100' : 'opacity-0'}
                    `}
                >
                    {/* 1. Nombre de la Skill */}
                    <span className="text-sm font-semibold text-white mr-2 whitespace-nowrap">
                        {name}:
                    </span>

                    {/* 2. Barra de Progreso Interna (ANIMADA) */}
                    <div className="relative w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                        <div 
                            // Aplica el color y el ancho dinámicos basados en la animación
                            className={`${currentBarColor} h-full rounded-full transition-all duration-300`}
                            style={{ width: `${animatedPercentage}%` }}
                        ></div>
                    </div>
                    
                    {/* 3. Porcentaje Numérico (ANIMADO) */}
                    <span className={`text-xs ml-2 font-bold text-gray-300 whitespace-nowrap`}>
                        {animatedPercentage}%
                    </span>
         
                </div>
            )}
        </div>
    );
};

export default SkillIcon;