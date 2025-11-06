import React, { useRef, useState, useEffect } from 'react';

// Constantes de Magnificación (lógica de la lupa) - Replicadas de SkillIcon
const INFLUENCE_RADIUS = 120; // Radio en píxeles donde el ratón afecta al ícono
const MAX_SCALE = 1.6; // Escala máxima: 160%

// Valores de referencia para calcular el 100% de la barra de progreso
const MAX_VALUE_STANDARD = 100; // Gramos/miligramos de referencia (arbitrario para la visualización)
const MAX_VALUE_KCAL = 1500; // Kcal de referencia (arbitrario para la visualización)

// Función para determinar el color de la barra (Replicada y adaptada)
const getBarColor = (percentage) => {
    if (percentage >= 70) return 'bg-red-600';     // Rojo (Alto / Advertencia)
    if (percentage >= 50) return 'bg-orange-500';  // Naranja (Medio)
    if (percentage >= 20) return 'bg-yellow-500';  // Amarillo (Bajo)
    return 'bg-green-500';                         // Verde (Muy bajo, okay)
};


const NutritionBar = ({ staticData, apiData, mousePosition, sidebarRef, isSidebarHovering }) => {
    const iconRef = useRef(null);
    const [isFocused, setIsFocused] = useState(false); // Estado para el hover en el ícono
    const [animatedValue, setAnimatedValue] = useState(0); // Estado para el conteo animado

    // Datos estáticos y dinámicos combinados
    const { name, Icon, iconColor, barColor } = staticData; // Usamos name y Icon/iconColor para el ícono
    const { quantity, unit } = apiData; // Usamos quantity y unit para la barra

    // Determinar el valor de referencia según la unidad
    const maxValue = (unit === 'kcal') ? MAX_VALUE_KCAL : MAX_VALUE_STANDARD;

    // Valor real de llenado de la barra (máx. 100%)
    const fillPercentage = Math.min(100, (quantity / maxValue) * 100);

    let scale = 1;

    // --- 1. CÁLCULO DE LA ESCALA (LUPA) --- (Lógica idéntica a SkillIcon)
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

    // El tooltip se muestra si el mouse está sobre el Sidebar Y el ícono está enfocado
    const showNutritionTooltip = isFocused && isSidebarHovering;


    // --- 2. LÓGICA DE ANIMACIÓN DE CONTEO Y LLENADO DE BARRA --- (Lógica adaptada de SkillIcon)
    useEffect(() => {
        if (showNutritionTooltip) {
            let start = null;
            const duration = 800; // Duración total de la animación de llenado (0.8s)
            const targetValue = quantity;

            const step = (timestamp) => {
                if (!start) start = timestamp;
                const progress = timestamp - start;
                
                // Calcula el valor actual que avanza de 0 hasta la cantidad real
                const current = Math.min(targetValue, (progress / duration) * targetValue);
                
                // Formateo: 0 decimales para mg/µg, 1 para g/kcal
                const decimals = (unit === 'mg' || unit === 'µg') ? 0 : 1;
                setAnimatedValue(parseFloat(current.toFixed(decimals))); 

                if (progress < duration) {
                    requestAnimationFrame(step);
                }
            };

            requestAnimationFrame(step);
        } else {
            // Reinicia la barra a 0 al salir del hover
            setAnimatedValue(0); 
        }
    }, [showNutritionTooltip, quantity, unit]); 

    // El color de la barra (usando la función getBarColor para el color de salud)
    const currentBarColor = getBarColor(fillPercentage); 
    
    // El porcentaje animado de la barra (para el estilo width)
    const animatedBarPercentage = Math.min(100, (animatedValue / maxValue) * 100);


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

            {/* BARRA DE NUTRICIÓN FLOTANTE (Animada y Sincronizada) */}
            {showNutritionTooltip && (
                <div 
                    // Estilos adaptados al tema Café
                    className={`
                        absolute left-full top-1/2 -translate-y-1/2 ml-4 flex items-center w-48 z-50 bg-cafe-oscuro/95 p-2 rounded-md shadow-xl
                        transition-opacity duration-300 ease-in-out 
                        ${showNutritionTooltip ? 'opacity-100' : 'opacity-0'}
                    `}
                >
                    {/* 1. Nombre del Nutriente */}
                    <span className="text-sm font-semibold text-pan-tostado mr-2 whitespace-nowrap">
                        {name}:
                    </span>

                    {/* 2. Barra de Progreso Interna (ANIMADA) */}
                    <div className="relative w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                        <div 
                            // Aplica el color de salud y el ancho dinámicos basados en la animación
                            className={`${currentBarColor} h-full rounded-full transition-all duration-300`}
                            style={{ width: `${animatedBarPercentage}%` }}
                        ></div>
                    </div>

                    {/* 3. Valor Numérico (ANIMADO) */}
                    <span className={`text-xs ml-2 font-bold text-pan-tostado whitespace-nowrap`}>
                        {animatedValue} {unit}
                    </span>

                </div>
            )}
        </div>
    );
};

export default NutritionBar;