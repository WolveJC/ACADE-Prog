import React from 'react';
import CafePage from '../pages/CafePage';
import { NutritionProvider } from '../context/NutritionContext';

/**
 * CafeLayout envuelve CafePage con el NutritionProvider,
 * permitiendo que todos los componentes hijos (como la Sidebar)
 * accedan a los datos nutricionales obtenidos en RecipeCard.
 */
const CafeLayout = () => {
    return (
        // Aquí encapsulamos la página con el Provider de Nutrición
        <NutritionProvider>
            <CafePage />
        </NutritionProvider>
    );
};

export default CafeLayout;