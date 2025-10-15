import React, { useState } from 'react';
import { skillsData } from '../../data/skills';

const Sidebar = () => {
    // 1. Estado para controlar la expansión de la Sidebar
    const [isSidebarExpanded, setIsSidebarExpanded] = useState(false);
    
    // 2. Estado para controlar el ícono que está siendo enfocado ('lupa')
    const [focusedSkill, setFocusedSkill] = useState(null); 

    // Clases de Tailwind para controlar el ancho
    const widthClass = isSidebarExpanded ? 'w-64' : 'w-20'; // Ajustamos a w-20 para iconos medianos

    return (
        <div 
            className={`
                fixed top-0 left-0 h-screen z-40 
                p-4 pt-20 
                bg-forest-start/90 shadow-2xl 
                transition-all duration-500 ease-in-out
                ${widthClass}
            `}
            onMouseEnter={() => setIsSidebarExpanded(true)}
            onMouseLeave={() => setIsSidebarExpanded(false)}
        >
            <div className="flex flex-col space-y-6 mt-4">
                
                <h3 className={`text-xl font-semibold mb-4 text-white transition-opacity duration-300 ${isSidebarExpanded ? 'opacity-100' : 'opacity-0 h-0 overflow-hidden'}`}>
                    Habilidades
                </h3>

                {skillsData.map((skill) => {
                    const { name, Icon, percentage, iconColor, barColor } = skill;
                    
                    // Lógica de la Lupa:
                    const isFocused = focusedSkill === name;
                    
                    // Tamaño base (mediano) y tamaño ampliado (lupa)
                    const iconSize = isFocused ? 'w-10 h-10' : 'w-7 h-7'; 
                    // Escala base
                    const iconScale = isFocused ? 'scale-125' : 'scale-100'; 
                    
                    return (
                        <div 
                            key={name} 
                            className="relative flex items-center h-10" // Contenedor que mantiene el alto
                            onMouseEnter={() => setFocusedSkill(name)}
                            onMouseLeave={() => setFocusedSkill(null)}
                        >
                            {/* 1. Ícono de la Habilidad (Lupa y tamaño) */}
                            <Icon 
                                className={`
                                    ${iconSize} ${iconColor} 
                                    transition-all duration-300 ease-in-out 
                                    ${iconScale}
                                `}
                            />
                            
                            {/* 2. Barra y Porcentaje (Visible solo cuando el ratón está encima) */}
                            {isFocused && isSidebarExpanded && (
                                <div className="ml-4 flex items-center w-32 md:w-44 transition-all duration-300">
                                    <div className="relative w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                                        <div 
                                            className={`${barColor} h-full rounded-full transition-all duration-500`}
                                            style={{ width: `${percentage}%` }}
                                        ></div>
                                    </div>
                                    {/* Mostrar el porcentaje al lado de la barra */}
                                    <span className={`text-sm ml-2 font-bold text-white whitespace-nowrap`}>
                                        {percentage}%
                                    </span>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default Sidebar;