import React, { useState, useEffect, useRef } from 'react';
import { skillsData } from '../../data/skills';
import SkillIcon from './Skill-Icon';

const FLOWER_CLASS = 'flower-trigger';

const Sidebar = () => {
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    const [isSidebarHovering, setIsSidebarHovering] = useState(false);

    const sidebarRef = useRef(null);

    // Optimización: usar requestAnimationFrame para suavizar el tracking
    useEffect(() => {
        let frameId = null;

        const handleMouseMove = (e) => {
            if (frameId) cancelAnimationFrame(frameId);
            frameId = requestAnimationFrame(() => {
                setMousePosition({ x: e.clientX, y: e.clientY });
            });
        };

        window.addEventListener('mousemove', handleMouseMove);
        return () => {
            window.removeEventListener('mousemove', handleMouseMove);
            if (frameId) cancelAnimationFrame(frameId);
        };
    }, []);

    // Sidebar responsive
    const widthClass = 'w-14 sm:w-16';

    return (
        <div
            ref={sidebarRef}
            className={`
                fixed top-0 left-0 
                h-dvh 
                z-40 
                p-2 
                pt-16 sm:pt-20 
                bg-forest-start/90 
                shadow-2xl 
                transition-all duration-300 ease-in-out
                ${widthClass}
                ${FLOWER_CLASS}
            `}
            onMouseEnter={() => setIsSidebarHovering(true)}
            onMouseLeave={() => setIsSidebarHovering(false)}
        >
            <div className="flex flex-col space-y-4 sm:space-y-6 mt-4">
                {skillsData.map((skill) => (
                    <SkillIcon
                        key={skill.name}
                        skill={skill}
                        mousePosition={mousePosition}
                        sidebarRef={sidebarRef}
                        isSidebarHovering={isSidebarHovering}
                    />
                ))}
            </div>
        </div>
    );
};

export default Sidebar;
