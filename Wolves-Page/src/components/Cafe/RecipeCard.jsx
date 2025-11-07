import React, { useEffect, useState, useRef } from 'react'; // 1. Importar useRef

const RecipeCard = ({ onRecipeLoaded }) => {
    const [recipe, setRecipe] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
    
    // 2. Crear el Ref para controlar la ejecución única
    const hasFetchedRef = useRef(false); 

    // Lógica principal: Fetch de MealDB y notificar al padre
    useEffect(() => {
        // 3. Verificar si ya se ha ejecutado el fetch. Si sí, detener la re-ejecución.
        if (hasFetchedRef.current) {
            // console.log("MealDB Fetch Evitado por Strict Mode."); // Opcional: para debug
            return;
        }

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

                // 2. Notificar al componente padre (CafePage)
                if (fetchedRecipe) {
                    //  4. Marcar el ref como true solo después de un fetch exitoso
                    hasFetchedRef.current = true; 
                    onRecipeLoaded(fetchedRecipe); 
                } else {
                    onRecipeLoaded(null);
                }

            } catch (err) {
                console.error("Error al cargar la receta:", err);
                setError(err.message);
                onRecipeLoaded(null, err.message); 
            } finally {
                setIsLoading(false);
            }
        };

        fetchRandomRecipe();
    }, [onRecipeLoaded]);


    // El resto del renderizado (renderContent) se mantiene sin cambios.
    const renderContent = () => {
        if (isLoading) {
            return (
                <div className="text-xl font-bold text-pan-tostado animate-pulse p-10">
data.meals                    Preparando el plato del día... ☕
                </div>
           );
      }

        if (error || !recipe) {
            return (
                <div className="text-xl text-red-300 p-10">
                     Lo sentimos, no pudimos cargar la receta de MealDB.
                </div>
            );
        }

        // Extraer ingredientes y medidas para mostrar en la tarjeta
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
                {/* ... (Marcado de receta, imagen, ingredientes e instrucciones) ... */}
                <h3 className="text-3xl md:text-4xl font-serif font-bold mb-4 text-pan-tostado">
                    {recipe.strMeal}
                </h3>

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