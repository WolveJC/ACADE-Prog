import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
// Importaciones específicas del Café
import { useNutritionContext } from '../../context/NutritionContext';
import NutritionBar from './NutritionBar'; 
import { nutritionData } from '../../data/nutritionData'; 

// Clase para el cursor (se mantiene, aunque podría cambiar si el cursor del café es diferente)
const FLOWER_CLASS = 'flower-trigger'; 

// Mapeo para conectar el nombre estático con la clave dinámica de Edamam
// 💻 src/components/Cafe/CafeSidebar.jsx (Fragmento a actualizar)

// Mapeo para conectar el nombre estático (tu nutritionData.js) con la clave dinámica de Edamam (la API)
const EDAMAM_KEY_MAP = {
    // Macronutrientes y Generales
    'Calorías': 'ENERC_KCAL',
    'Proteínas': 'PROCNT',
    'Carbohidratos': 'CHOCDF',
    'Grasas Totales': 'FAT',
    'Fibra': 'FIBTG',
    'Azúcares': 'SUGAR',
    'Sodio': 'NA', 
    'Colesterol': 'CHOLE',

    // Subdivisiones de Grasas
    'Grasas Saturadas': 'FASAT',
    'Grasas Monoinsaturadas': 'FAMS', // Clave Edamam para Monoinsaturadas
    'Grasas Poliinsaturadas': 'FAPU', // Clave Edamam para Poliinsaturadas

    // Minerales
    'Fósforo': 'P',
    'Calcio': 'CA',
    'Hierro': 'FE',
    'Magnesio': 'MG',
    'Potasio': 'K',
    'Zinc': 'ZN',

    // Vitaminas (las claves Edamam suelen ser la abreviatura de la vitamina)
    'Vitamina A': 'VITA_RAE', // Vitamina A (Retinol Activity Equivalents)
    'Vitamina C': 'VITC',
    'Vitamina D': 'VITD',
    'Vitamina E': 'TOCPHA', // Alpha-tocopherol (forma común de Vitamina E)
    'Vitamina K': 'VITK1',
    // Complejo B (Edamam tiene claves individuales, agrupamos las principales)
    // Nota: 'Complejo B' no es una clave única; Edamam usa B6, B12, THIA, RBF, NIA, etc.
    // Usaremos una clave representativa (ej. B6) o deberás mapear cada una individualmente.
    // Por simplicidad, si la API trae muchas del complejo B, tu filtro mostrará solo las que tengan valor.
    'Vitamina B6': 'VITB6A', 
};

const CafeSidebar = () => {
    // 1. Estados y Hooks de la Lupa/Hover
    const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
    const [isSidebarHovering, setIsSidebarHovering] = useState(false);
    const sidebarRef = useRef(null); 

    // Hook para rastrear el movimiento del mouse
    useEffect(() => {
        const handleMouseMove = (e) => {
            setMousePosition({ x: e.clientX, y: e.clientY });
        };
        window.addEventListener('mousemove', handleMouseMove);
        return () => window.removeEventListener('mousemove', handleMouseMove);
    }, []);

    // 2. Consumo de Datos de Nutrición
    const { nutritionData: edamamData, isNutritionLoading, nutritionError } = useNutritionContext();

    // 3. Estilos
    const widthClass = 'w-16'; 
    // Estilos fijos del café (mismos que definimos antes)
    const finalBgClass = 'bg-moca/95 border-r border-pan-tostado'; 
    
    
    // ----------------------------------------------------
    // 4. RENDERIZADO DEL CONTENIDO NUTRICIONAL
    // ----------------------------------------------------
    const renderContent = () => {
        if (isNutritionLoading) {
            return <div className="text-sm text-pan-tostado mt-4 animate-pulse px-1">Analizando nutrición...</div>;
        }

        if (nutritionError || !edamamData || !edamamData.totalNutrients) {
            return <div className="text-xs text-red-300 mt-4 px-1 leading-snug">No hay datos nutricionales listos.</div>;
        }

        const totalNutrients = edamamData.totalNutrients;

        return (
            <div className="flex flex-col space-y-6 mt-4">
                {nutritionData.map((staticNutrient) => {
                    // Obtener la clave de Edamam
                    const edamamKey = EDAMAM_KEY_MAP[staticNutrient.name]; 
                    
                    // Buscar los datos dinámicos (fallback por si Edamam usa el nombre completo)
                    const dynamicNutrient = totalNutrients[edamamKey] || totalNutrients[staticNutrient.name.toUpperCase().replace(/\s/g, '_')];

                    // Filtrado: Si no hay valor o la cantidad es 0, no se renderiza.
                    const hasValue = dynamicNutrient && dynamicNutrient.quantity > 0;

                    if (hasValue) {
                        return (
                            <NutritionBar
                                key={staticNutrient.name}
                                staticData={staticNutrient}
                                apiData={dynamicNutrient}
                                mousePosition={mousePosition}
                                sidebarRef={sidebarRef}
                                isSidebarHovering={isSidebarHovering}
                            />
                        );
                    }
                    return null;
                })}
            </div>
        );
    }


    return (
        <div 
            ref={sidebarRef}
            className={`
                fixed top-0 left-0 h-screen z-40 p-2 pt-20 
                shadow-2xl transition-all duration-300 ease-in-out
                ${widthClass}
                ${FLOWER_CLASS} // Puedes cambiar esta clase si defines un cursor específico para el café
                ${finalBgClass} 
            `}
            onMouseEnter={() => setIsSidebarHovering(true)} 
            onMouseLeave={() => setIsSidebarHovering(false)} 
        >
            {renderContent()}
        </div>
    );
};

export default CafeSidebar;