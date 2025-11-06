import React, { useState, useEffect, useRef } from 'react';
import { skillsData } from '../../data/skills';
import SkillIcon from './Skill-Icon'; 

// Clase que debe coincidir con la lógica del CustomCursor para el estado FLOR
const FLOWER_CLASS = 'flower-trigger'; 

const Sidebar = () => {
    // 1. Estado para rastrear la posición del mouse en la ventana (para la magnificación)
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    // 2. Estado para saber si el mouse está sobre la barra lateral 
    const [isSidebarHovering, setIsSidebarHovering] = useState(false);
    
    // Referencia para obtener la posición de la Sidebar
    const sidebarRef = useRef(null); 

    // Hook para rastrear el movimiento del mouse en toda la ventana
    useEffect(() => {
        const handleMouseMove = (e) => {
            setMousePosition({ x: e.clientX, y: e.clientY });
        };
        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, []);

    // El ancho es fijo, no cambia al hacer hover
    const widthClass = 'w-16'; 

    return (
        <div 
            ref={sidebarRef}
            className={`
                fixed top-0 left-0 h-screen z-40 p-2 pt-20 
                bg-forest-start/90 shadow-2xl transition-all duration-300 ease-in-out
                ${widthClass}
                ${FLOWER_CLASS} // ⬅️ CLASE CRÍTICA: Activa el cursor FLOR
            `}
            // Usamos hover para controlar el despliegue de la Barra de Experiencia en el hijo
            onMouseEnter={() => setIsSidebarHovering(true)} 
            onMouseLeave={() => setIsSidebarHovering(false)} 
        >
            <div className="flex flex-col space-y-6 mt-4">
                {skillsData.map((skill) => {
                    return (
                        <SkillIcon 
                            key={skill.name} 
                            skill={skill} 
                            mousePosition={mousePosition}
                            sidebarRef={sidebarRef}
                            isSidebarHovering={isSidebarHovering}
                        />
                    );
                })}
            </div>

        </div>
    );
};

export default Sidebar;