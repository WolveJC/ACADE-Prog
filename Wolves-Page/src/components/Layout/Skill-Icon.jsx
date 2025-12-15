import React, { useRef, useState, useEffect } from 'react';

const INFLUENCE_RADIUS = 120;
const MAX_SCALE = 1.5;

const getBarColor = (percentage) => {
    if (percentage >= 70) return 'bg-green-500';
    if (percentage >= 50) return 'bg-yellow-500';
    if (percentage >= 20) return 'bg-orange-500';
    return 'bg-red-600';
};

const SkillIcon = ({ skill, mousePosition, sidebarRef, isSidebarHovering }) => {
    const iconRef = useRef(null);

    const [isFocused, setIsFocused] = useState(false);
    const [animatedPercentage, setAnimatedPercentage] = useState(0);
    const [scale, setScale] = useState(1);

    const { name, Icon, percentage, iconColor } = skill;

    // Escala responsiva sin romper layout
    useEffect(() => {
        if (!iconRef.current || !mousePosition) return;

        const rect = iconRef.current.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const distance = Math.sqrt(
            Math.pow(centerX - mousePosition.x, 2) +
            Math.pow(centerY - mousePosition.y, 2)
        );

        if (distance < INFLUENCE_RADIUS) {
            const influenceFactor = 1 - distance / INFLUENCE_RADIUS;
            const newScale = 1 + (MAX_SCALE - 1) * influenceFactor;
            setScale(newScale);
        } else {
            setScale(1);
        }
    }, [mousePosition]);

    //  Animación de la barra
    const showExperienceBar = isFocused && isSidebarHovering;

    useEffect(() => {
        if (!showExperienceBar) {
            setAnimatedPercentage(0);
            return;
        }

        let start = null;
        const duration = 800;

        const step = (timestamp) => {
            if (!start) start = timestamp;
            const progress = timestamp - start;

            const current = Math.min(
                percentage,
                (progress / duration) * percentage
            );

            setAnimatedPercentage(Math.round(current));

            if (progress < duration) {
                requestAnimationFrame(step);
            }
        };

        requestAnimationFrame(step);
    }, [showExperienceBar, percentage]);

    const currentBarColor = getBarColor(animatedPercentage);

    // Renderizado del ícono (imagen o componente)
    const renderIcon = () => {
        if (typeof Icon === "string") {
            return (
                <img
                    src={Icon}
                    alt={name}
                    className={`w-8 h-8 sm:w-9 sm:h-9 object-contain ${iconColor} transition-all duration-100 ease-out`}
                    style={{ transform: `scale(${scale})` }}
                />
            );
        }

        return (
            <Icon
                className={`w-8 h-8 sm:w-9 sm:h-9 ${iconColor} transition-all duration-100 ease-out`}
                style={{ transform: `scale(${scale})` }}
            />
        );
    };

    return (
        <div
            key={name}
            className="
                relative 
                w-full 
                flex 
                items-center 
                justify-center 
                h-10 sm:h-12 
                transition-transform 
                duration-100 
                ease-out 
                flower-trigger
            "
            onMouseEnter={() => setIsFocused(true)}
            onMouseLeave={() => setIsFocused(false)}
        >
            {/* Contenedor fijo para evitar saltos */}
            <div ref={iconRef} className="flex justify-center items-center w-10 h-10 sm:w-12 sm:h-12">
                {renderIcon()}
            </div>

            {/* Barra responsive */}
            {showExperienceBar && (
                <div
                    className={`
                        absolute 
                        left-full 
                        top-1/2 
                        -translate-y-1/2 
                        ml-3 
                        flex 
                        items-center 
                        w-40 sm:w-48 md:w-56 
                        z-50 
                        bg-gray-900/95 
                        p-2 
                        rounded-md 
                        shadow-xl
                        transition-opacity 
                        duration-300 
                        ease-in-out 
                        opacity-100
                    `}
                >
                    <span className="text-xs sm:text-sm font-semibold text-white mr-2 whitespace-nowrap">
                        {name}:
                    </span>

                    <div className="relative w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                        <div
                            className={`${currentBarColor} h-full rounded-full transition-all duration-300`}
                            style={{ width: `${animatedPercentage}%` }}
                        ></div>
                    </div>

                    <span className="text-xs ml-2 font-bold text-gray-300 whitespace-nowrap">
                        {animatedPercentage}%
                    </span>
                </div>
            )}
        </div>
    );
};

export default SkillIcon;
