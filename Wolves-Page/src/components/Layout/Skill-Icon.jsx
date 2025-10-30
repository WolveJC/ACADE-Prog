import React, { useRef, useState } from 'react';

// Constantes de Magnificación (puedes ajustarlas)
const INFLUENCE_RADIUS = 120; // Radio de influencia en píxeles
const MAX_SCALE = 1.6;        // Escala máxima (160%)

const SkillIcon = ({ skill, mousePosition, sidebarRef, isSidebarHovering }) => {
    const iconRef = useRef(null);
    const [isFocused, setIsFocused] = useState(false); // Hover individual del ícono
    const { name, Icon, percentage, iconColor, barColor } = skill;

    let scale = 1;

    // --- CÁLCULO DE LA ESCALA BASADO EN LA DISTANCIA ---
    if (iconRef.current && sidebarRef.current && mousePosition) {
        const rect = iconRef.current.getBoundingClientRect();
        
        // Calcular el centro del ícono
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        // Distancia Euclidiana (Pitágoras)
        const distance = Math.sqrt(
            Math.pow(centerX - mousePosition.x, 2) + Math.pow(centerY - mousePosition.y, 2)
        );
        
        // Aplicar la magnificación si está dentro del radio de influencia
        if (distance < INFLUENCE_RADIUS) {
            const influenceFactor = 1 - distance / INFLUENCE_RADIUS;
            scale = 1 + (MAX_SCALE - 1) * influenceFactor;
        }
    }

    // El despliegue de la barra de experiencia ocurre cuando el mouse está sobre el ícono (isFocused) 
    // Y sobre la barra lateral (isSidebarHovering), aunque esta última condición es opcional.
    const showExperienceBar = isFocused && isSidebarHovering;

    return (
        <div 
            key={name} 
            // Usamos w-full para que ocupe todo el ancho de la sidebar (w-16) y centre el icono
            className="relative w-full flex items-center justify-center h-10 transition-transform duration-100 ease-out" 
            onMouseEnter={() => setIsFocused(true)}
            onMouseLeave={() => setIsFocused(false)}
        >
            {/* Contenedor del Ícono: necesario para el useRef y el cálculo del centro */}
            <div ref={iconRef} className="flex justify-center items-center">
                <Icon 
                    className={`w-7 h-7 ${iconColor} transition-all duration-100 ease-out`}
                    // La escala dinámica se aplica aquí
                    style={{ transform: `scale(${scale})` }} 
                />
            </div>
            
            {/* BARRA DE EXPERIENCIA: Se despliega hacia la izquierda, fuera del sidebar */}
            {showExperienceBar && (
                <div 
                    // right-full: Lo posiciona al borde izquierdo de la barra lateral.
                    // -mr-4: Mueve la barra 16px (1rem) más allá del borde de la sidebar.
                    // w-48: Define el ancho del contenido de la barra de experiencia.
                    className="absolute right-full -mr-4 flex items-center w-48 transition-opacity duration-300 z-30 bg-gray-900/95 p-2 rounded-md shadow-xl" 
                    
                    // Estilo para asegurar la transición de opacidad (despliegue)
                    style={{ 
                        opacity: showExperienceBar ? 1 : 0,
                        transform: showExperienceBar ? 'translateX(0)' : 'translateX(100%)',
                        transition: 'opacity 0.3s, transform 0.3s'
                    }}
                >
                    {/* Barra de Progreso */}
                    <div className="relative w-full h-2 bg-gray-500 rounded-full overflow-hidden">
                        <div 
                            className={`${barColor} h-full rounded-full transition-all duration-500`}
                            style={{ width: `${percentage}%` }}
                        ></div>
                    </div>
                    {/* Porcentaje */}
                    <span className={`text-sm ml-2 font-bold text-white whitespace-nowrap`}>
                        {percentage}%
                    </span>
                </div>
            )}
        </div>
    );
};

export default SkillIcon;
