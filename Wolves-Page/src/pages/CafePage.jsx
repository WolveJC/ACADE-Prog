import React, { useState, useCallback, useEffect } from 'react';
import usePageTitle from '../hooks/usePageTitle';
import RecipeCard from '../components/Cafe/RecipeCard'; 
import TriviaWidget from '../components/Cafe/TriviaWidget';
import CafeSidebar from '../components/Cafe/CafeSidebar';
import { useNutritionContext } from '../context/NutritionContext';

// Constantes de la API de Edamam (Ahora en el componente padre)
const RAPIDAPI_KEY = 'ea40e1fb71msh1630c71aa1e941dp15b910jsndb8283303c08'; 
const RAPIDAPI_HOST = 'edamam-edamam-nutrition-analysis.p.rapidapi.com';

const CafePage = () => {
    usePageTitle("WolveJC | El Café de las APIs");
    
    const { setIsNutritionLoading, setEdamamData, nutritionError } = useNutritionContext();
    const [recipeData, setRecipeData] = useState(null);
    const [hasFetchedNutrition, setHasFetchedNutrition] = useState(false); 

    const formatIngredientsForEdamam = (recipe) => {
        let queryParts = [];
        for (let i = 1; i <= 20; i++) {
            const ingredient = recipe[`strIngredient${i}`];
            const measure = recipe[`strMeasure${i}`];
            if (ingredient && ingredient.trim() !== '') {
                const ingredientString = `${measure || ''} ${ingredient}`.trim();
                queryParts.push(`ingr=${encodeURIComponent(ingredientString)}`);
            }
        }
        return queryParts.join('&');
    };

    const handleRecipeLoaded = useCallback((recipe, error) => {
        if (recipe) {
            setRecipeData(recipe);
        } else if (error) {
            setEdamamData(null, `Error al cargar la receta: ${error}`);
        } else {
            setEdamamData(null, "No se pudo obtener la receta para analizar.");
        }
    }, [setEdamamData]);


    const fetchNutritionData = useCallback(async () => {
        if (!recipeData || hasFetchedNutrition) return;
        
        const ingredientQuery = formatIngredientsForEdamam(recipeData);
        if (!ingredientQuery) {
            setEdamamData(null, "No se encontraron ingredientes para el análisis nutricional.");
            setHasFetchedNutrition(true);
            return;
        }

        setIsNutritionLoading(true);
        const apiUrl = `https://${RAPIDAPI_HOST}/api/nutrition-data?nutrition-type=cooking&${ingredientQuery}`;
        
        let userErrorMessage = "Error desconocido. Vuelve a intentarlo más tarde.";

        try {
            const response = await fetch(apiUrl, {
                method: 'GET',
                headers: {
                    'x-rapidapi-key': RAPIDAPI_KEY,
                    'x-rapidapi-host': RAPIDAPI_HOST
                }
            });

            if (!response.ok) {
                const status = response.status;
                let developerMessage = `Error de API [${status}].`;

                if (status === 429) {
                    userErrorMessage = "¡Límite de solicitudes excedido! 😥 ";
                } else if (status >= 500) {
                    userErrorMessage = "El servicio de nutrición falló temporalmente. ¡Prueba recargar en un minuto!";
                } else if (status === 401 || status === 403 || status === 404) {
                    // Errores técnicos: Mantenemos el mensaje genérico (userErrorMessage)
                } else {
                    userErrorMessage = `Error ${status}: La solicitud falló.`;
                }
                
                try {
                    const errorBody = await response.json();
                    developerMessage += ` Detalle: ${errorBody.error || errorBody.message || response.statusText}`;
                } catch {
                    developerMessage += ` Detalle: ${response.statusText}`;
                }
                console.error("Error de Edamam:", developerMessage);
                
                throw new Error(userErrorMessage); 
            }

            const data = await response.json();
            setEdamamData(data); 

        } catch (err) {
            let finalErrorMessage = err.message;

            if (err instanceof TypeError && err.message.includes('Failed to fetch')) {
                finalErrorMessage = "Problemas de conexión a la red. Revisa tu internet y vuelve a cargar.";
            } else if (err.message.includes("JSON")) {
                finalErrorMessage = "Error al procesar la respuesta del servidor. Inténtalo de nuevo.";
            }

            setEdamamData(null, finalErrorMessage); 
            console.error("Error al cargar el JSON (tiempo excedido)", err);
            
        } finally {
            setIsNutritionLoading(false);
            setHasFetchedNutrition(true); 
        }
    }, [recipeData, hasFetchedNutrition, setEdamamData, setIsNutritionLoading]);

    useEffect(() => {
        if (recipeData && !hasFetchedNutrition) {
            fetchNutritionData();
        }
    }, [recipeData, hasFetchedNutrition, fetchNutritionData]);


    return (
        <div 
            className="
                min-h-screen pb-10 
                bg-leche-crema text-cafe-oscuro
                transition-colors duration-500
            "
        >
            {/* FRANJA DE ERROR: Posicionamiento fijo justo debajo del header */}
            {nutritionError && (
                <div 
                    className="
                        fixed top-[4rem] left-0 w-full bg-red-600 text-white font-medium text-center py-2 z-50 
                        transition-all duration-300 shadow-md
                    "
                >
                    <p className="max-w-7xl mx-auto px-4 md:px-6 flex items-center justify-center space-x-2">
                        <span>⚠️</span>
                        <span className="text-sm md:text-base">{nutritionError}</span>
                    </p>
                </div>
            )}
            {/* ------------------------------------ */}

            {/* Contenedor principal: Añadimos padding-top para dejar espacio al header y, si existe, a la franja de error */}
            <div className={`max-w-7xl mx-auto px-4 md:px-6 ${nutritionError ? 'pt-[9rem]' : 'pt-[7rem]'}`}> 
                {/* NOTA: 'pt-[9rem]' (4rem del header + 2rem del error + 3rem de espacio) o 'pt-[7rem]' (4rem del header + 3rem de espacio) */}

                <h2 className="text-4xl md:text-5xl font-serif font-bold text-center mb-4 text-cafe-oscuro">
                     El Café de las APIs
                </h2>
                <p className="text-lg text-gray-500 text-center mb-8 max-w-3xl mx-auto italic">
                    Una pausa para explorar la sinergia de los datos. Hoy te servimos una receta al azar.
                </p>

                {/* CONTENEDOR FLEX PRINCIPAL: Usa 'flex-row' en LG y 'items-start' para alinear arriba */}
                <div className="flex flex-col lg:flex-row lg:items-start lg:space-x-8">

                    {/* 1. COLUMNA IZQUIERDA: Sidebar de Nutrientes */}
                    <aside className="w-full lg:w-40 flex-shrink-0 mb-6 lg:mb-0 lg:sticky lg:top-[7rem]"> 
                        {/* 'top-[7rem]' para sticky, considerando el header (4rem) y la franja de error (2rem) + espacio */}
                        <CafeSidebar /> 
                    </aside>

                    {/* 2. COLUMNA DERECHA: Contenido Principal */}
                    <main className="flex-grow">
                        <div className="flex flex-col items-center">

                            <RecipeCard onRecipeLoaded={handleRecipeLoaded} />

                            <div className="w-full max-w-4xl mt-6"> 
                                <TriviaWidget />
                            </div>

                        </div>
                    </main>

                </div>
                
            </div>
        </div>
    );
};

export default CafePage;