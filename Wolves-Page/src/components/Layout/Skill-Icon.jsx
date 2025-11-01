// src/components/Layout/SkillIcon.jsx (RE-CORREGIDO: Incluye Barra de Progreso)

import React, { useRef, useState } from 'react';

// Constantes de Magnificación (lógica de la lupa)
const INFLUENCE_RADIUS = 120; 
const MAX_SCALE = 1.6; // Amplitud: 160%

const SkillIcon = ({ skill, mousePosition, sidebarRef, isSidebarHovering }) => {
    const iconRef = useRef(null);
    const [isFocused, setIsFocused] = useState(false); 
    const { name, Icon, percentage, iconColor, barColor } = skill;

    let scale = 1;

    // --- CÁLCULO DE LA ESCALA (LUPA) ---
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

    const showExperienceBar = isFocused && isSidebarHovering;

    return (
        <div 
            key={name} 
            className="relative w-full flex items-center justify-center h-10 transition-transform duration-100 ease-out" 
            onMouseEnter={() => setIsFocused(true)}
            onMouseLeave={() => setIsFocused(false)}
        >
            {/* Contenedor del Ícono (Lupa) */}
            <div ref={iconRef} className="flex justify-center items-center">
                <Icon 
                    className={`w-7 h-7 ${iconColor} transition-all duration-100 ease-out`}
                    style={{ transform: `scale(${scale})` }} 
                />
            </div>
            
            {/* BARRA DE EXPERIENCIA FLOTANTE */}
            {showExperienceBar && (
                <div 
                    // Posicionamiento correcto a la DERECHA: left-full para superposición.
                    // Ancho más amplio (w-48) para acomodar la barra de progreso.
                    className="absolute left-full top-1/2 -translate-y-1/2 ml-4 flex items-center w-48 transition-opacity duration-300 z-50 bg-gray-900/95 p-2 rounded-md shadow-xl" 
                    
                    style={{ 
                        opacity: showExperienceBar ? 1 : 0,
                        transition: 'opacity 0.3s ease-in-out' 
                    }}
                >
                    {/* 1. Nombre de la Skill */}
                    <span className="text-sm font-semibold text-white mr-2 whitespace-nowrap">
                        {name}:
                    </span>

                    {/* 2. Barra de Progreso Interna (Llena según el porcentaje) */}
                    <div className="relative w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                        <div 
                            className={`${barColor} h-full rounded-full transition-all duration-500`}
                            style={{ width: `${percentage}%` }}
                        ></div>
                    </div>
                    
                    {/* 3. Porcentaje Numérico */}
                    <span className={`text-xs ml-2 font-bold text-gray-300 whitespace-nowrap`}>
                        {percentage}%
                    </span>
         
                </div>
            )}
        </div>
    );
};

export default SkillIcon;