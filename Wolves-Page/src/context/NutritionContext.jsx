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
    // nutritionData: Almacenará el JSON de Edamam
    const [nutritionData, setNutritionData] = useState(null);
    const [isNutritionLoading, setIsNutritionLoading] = useState(false);
    const [nutritionError, setNutritionError] = useState(null); // Estado para el mensaje de error

    // Función que será llamada por CafePage para guardar los resultados finales
    // El estado de carga (setIsNutritionLoading) se maneja en el componente que ejecuta el fetch (CafePage).
    const setEdamamData = (data, error = null) => {
        setNutritionData(data);
        setNutritionError(error);
        // Se eliminó setIsNutritionLoading(false);
    };

    const value = {
        nutritionData,
        isNutritionLoading,
        nutritionError,
        setIsNutritionLoading,
        setEdamamData, // Se usa para guardar datos y errores
    };

    return (
        <NutritionContext.Provider value={value}>
            {children}
        </NutritionContext.Provider>
    );
};