import React from 'react';
import { useNutritionContext } from '../../context/NutritionContext';
import { FaHeartbeat, FaAppleAlt, FaBreadSlice, FaWeight } from 'react-icons/fa'; // Íconos Nutricionales

// NOTA: Este componente requiere un componente hijo (NutrientIcon) similar a SkillIcon 
// para manejar la lógica de la barra desplegable al hacer hover.

const NutritionBar = () => {
    // Consumimos los datos del contexto de Edamam
    const { nutritionData, isNutritionLoading, nutritionError } = useNutritionContext();

    // Nutrientes clave a mostrar y sus íconos (Ejemplo)
    const primaryNutrients = [
        { key: 'ENERC_KCAL', name: 'Calorías', Icon: FaHeartbeat, unit: 'kcal' },
        { key: 'PROCNT', name: 'Proteína', Icon: FaAppleAlt, unit: 'g' },
        { key: 'FAT', name: 'Grasas', Icon: FaWeight, unit: 'g' },
        { key: 'CHOCDF', name: 'Carbohidratos', Icon: FaBreadSlice, unit: 'g' },
    ];
    
    // Controles visuales (usaremos color 'pan-tostado' para los íconos)
    const iconClass = "w-6 h-6 text-pan-tostado transition-colors duration-300";

    if (isNutritionLoading) {
        return (
            <div className="text-sm text-pan-tostado mt-4 text-center animate-pulse">
                Analizando...
            </div>
        );
    }
    
    if (nutritionError || !nutritionData || !nutritionData.totalNutrients) {
        return (
            <div className="text-xs text-red-300 mt-4 text-center p-1">
                Análisis no disponible.
            </div>
        );
    }

    // Si tenemos datos, mostramos los principales nutrientes
    return (
        <div className="flex flex-col space-y-6 mt-4">
            <h3 className="text-sm font-bold text-pan-tostado text-center uppercase tracking-widest">
                Nutrición
            </h3>
            
            {primaryNutrients.map(({ key, name, Icon, unit }) => {
                // El objeto 'totalNutrients' de Edamam tiene los datos
                const nutrient = nutritionData.totalNutrients[key];
                
                if (!nutrient) return null;

                // NOTA: Aquí deberás usar un componente hijo 'NutrientIcon' 
                // para replicar la funcionalidad de 'SkillIcon' (barra al pasar el ratón)
                return (
                    <div 
                        key={key} 
                        // El estilo y la lógica de hover para el despliegue de la barra
                        // deben ir en este contenedor o en un componente hijo.
                        className="relative flex justify-center items-center group cursor-default"
                    >
                        <Icon className={iconClass} title={`${name}: ${nutrient.quantity.toFixed(1)} ${nutrient.unit}`} />

                        {/* //  Placeholder para la barra desplegable (Similar al SkillIcon)
                          <div className="absolute left-full ml-4 p-2 bg-moca border border-pan-tostado rounded shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                             {name}: {nutrient.quantity.toFixed(1)}{unit} 
                          </div> 
                        */}
                    </div>
                );
            })}
            
        </div>
    );
};

export default NutritionBar;