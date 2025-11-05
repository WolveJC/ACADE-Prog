import React, { useEffect, useState } from 'react';
import { useNutritionContext } from '../../context/NutritionContext'; // ⬅️ Importamos el contexto

const RecipeCard = () => {
    const [recipe, setRecipe] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // Contexto de Nutrición para guardar el resultado de Edamam
    const { setIsNutritionLoading, setEdamamData } = useNutritionContext();
    
    // Clave de Edamam/RapidAPI (ADVERTENCIA: No es seguro en el frontend)
    const RAPIDAPI_KEY = 'ea40e1fb71msh1630c71aa1e941dp15b910jsndb8283303c08'; 
    const RAPIDAPI_HOST = 'edamam-edamam-nutrition-analysis.p.rapidapi.com';

    // Función para formatear ingredientes de MealDB para Edamam
    const formatIngredientsForEdamam = (recipe) => {
        let queryParts = [];
        for (let i = 1; i <= 20; i++) {
            const ingredient = recipe[`strIngredient${i}`];
            const measure = recipe[`strMeasure${i}`];
            
            if (ingredient && ingredient.trim() !== '') {
                // Formato de Edamam: [Medida] [Nombre del Ingrediente]
                const ingredientString = `${measure || ''} ${ingredient}`.trim();
                
                // Agregamos 'ingr=' y URL-encodeamos el valor
                queryParts.push(`ingr=${encodeURIComponent(ingredientString)}`);
            }
        }
        return queryParts.join('&');
    };
    
    // Función para hacer el fetch a Edamam
    const fetchNutritionData = async (recipe) => {
        const ingredientQuery = formatIngredientsForEdamam(recipe);
        if (!ingredientQuery) {
            setEdamamData(null, "No se encontraron ingredientes para el análisis nutricional.");
            return;
        }

        setIsNutritionLoading(true);
        
        // Construcción de la URL de Edamam
        const apiUrl = `https://${RAPIDAPI_HOST}/api/nutrition-data?nutrition-type=cooking&${ingredientQuery}`;

        try {
            const response = await fetch(apiUrl, {
                method: 'GET',
                headers: {
                    'x-rapidapi-key': RAPIDAPI_KEY,
                    'x-rapidapi-host': RAPIDAPI_HOST
                }
            });

            if (!response.ok) {
                const errorBody = await response.json();
                throw new Error(`Error de Edamam: ${response.status}. Mensaje: ${errorBody.error || response.statusText}`);
            }

            const data = await response.json();
            setEdamamData(data); // ⬅️ Guardamos el JSON de Edamam en el contexto
        } catch (err) {
            console.error("Error fetching nutrition data:", err);
            setEdamamData(null, err.message);
        }
    };


    // Lógica principal: Fetch de MealDB y luego Edamam
    useEffect(() => {
        const fetchRandomRecipe = async () => {
            setIsLoading(true);
            setError(null);
            
            try {
                // 1. Fetch de TheMealDB
                const response = await fetch('https://www.themealdb.com/api/json/v1/1/random.php');
                if (!response.ok) {
                    throw new Error('No se pudo cargar la receta del día (MealDB).');
                }
                const data = await response.json();
                const fetchedRecipe = data.meals ? data.meals[0] : null;

                setRecipe(fetchedRecipe);
                
                // 2. Fetch de Edamam
                if (fetchedRecipe) {
                    await fetchNutritionData(fetchedRecipe);
                } else {
                    setEdamamData(null, "Receta no encontrada, no se puede analizar.");
                }

            } catch (err) {
                console.error("Error general:", err);
                setError(err.message);
                setEdamamData(null, "Error al cargar la receta y los datos nutricionales.");
            } finally {
                setIsLoading(false);
            }
        };

        fetchRandomRecipe();
    }, []);

    // ... (El resto del componente renderContent, sin cambios en el renderizado) ...
    const renderContent = () => {
        // ... (Tu lógica de rendering con las clases de Tailwind) ...
        if (isLoading) {
            return (
                <div className="text-xl font-bold text-pan-tostado animate-pulse p-10">
                    Preparando el plato del día y analizando nutrición... ☕
                </div>
            );
        }
        
        if (error || !recipe) {
            return (
                <div className="text-xl text-red-300 p-10">
                    ❌ Lo sentimos, no pudimos cargar la receta.
                </div>
            );
        }
        
        // Extraer ingredientes y medidas
        const ingredients = [];
        for (let i = 1; i <= 20; i++) {
            const ingredient = recipe[`strIngredient${i}`];
            const measure = recipe[`strMeasure${i}`];
            if (ingredient && ingredient.trim() !== '') {
                ingredients.push({ ingredient, measure });
            }
        }

        return (
            <div 
                className="
                    w-full max-w-4xl bg-moca text-white p-6 md:p-10 rounded-xl shadow-2xl 
                    border border-pan-tostado 
                "
            >
                <h3 className="text-3xl md:text-4xl font-serif font-bold mb-4 text-pan-tostado">
                    {recipe.strMeal}
                </h3>
                <p className="text-sm italic mb-6 border-b border-pan-tostado/50 pb-4">
                    Categoría: {recipe.strCategory} | Origen: {recipe.strArea}
                </p>

                <div className="md:flex md:space-x-8">
                    {/* Sección Izquierda: Imagen */}
                    <div className="md:w-1/3 mb-6 md:mb-0 flex-shrink-0">
                        <img 
                            src={recipe.strMealThumb} 
                            alt={`Imagen de ${recipe.strMeal}`} 
                            className="w-full h-auto rounded-lg shadow-lg border-2 border-pan-tostado"
                        />
                    </div>

                    {/* Sección Derecha: Ingredientes y Pasos */}
                    <div className="md:w-2/3">
                        <h4 className="text-2xl font-semibold mb-3 text-pan-tostado">Ingredientes</h4>
                        <ul className="grid grid-cols-2 gap-2 text-sm mb-6 max-h-40 overflow-y-auto pr-2 custom-scrollbar">
                            {ingredients.map((item, index) => (
                                <li key={index} className="flex justify-between border-b border-white/20 pb-1">
                                    <span className="font-medium">{item.ingredient}</span>
                                    <span className="italic text-gray-200">{item.measure}</span>
                                </li>
                            ))}
                        </ul>

                        <h4 className="text-2xl font-semibold mb-3 text-pan-tostado">Instrucciones</h4>
                        <p className="text-sm leading-relaxed whitespace-pre-line max-h-60 overflow-y-auto pr-2 custom-scrollbar">
                            {recipe.strInstructions}
                        </p>
                    </div>
                </div>
            </div>
        );
    };

    return <div className="flex justify-center">{renderContent()}</div>;
};

export default RecipeCard;