import React, { createContext, useContext, useState } from 'react';

// 1. Creamos el Contexto
const NutritionContext = createContext(null);

// 2. Hook de Consumo
export const useNutritionContext = () => {
    const context = useContext(NutritionContext);
    if (!context) {
        throw new Error('useNutritionContext debe usarse dentro de un NutritionProvider');
    }
    return context;
};

// 3. El Provider
export const NutritionProvider = ({ children }) => {
    // nutritionData: Almacenará el JSON de Edamam (ej: { calories: 300, totalNutrients: {...} })
    const [nutritionData, setNutritionData] = useState(null);
    const [isNutritionLoading, setIsNutritionLoading] = useState(false);
    const [nutritionError, setNutritionError] = useState(null);

    // Función que será llamada por RecipeCard para guardar los resultados
    const setEdamamData = (data, error = null) => {
        setNutritionData(data);
        setNutritionError(error);
        setIsNutritionLoading(false);
    };

    const value = {
        nutritionData,
        isNutritionLoading,
        nutritionError,
        setIsNutritionLoading,
        setEdamamData,
    };

    return (
        <NutritionContext.Provider value={value}>
            {children}
        </NutritionContext.Provider>
    );
};