import React, { useEffect, useState } from 'react';

const RecipeCard = () => {
    const [recipe, setRecipe] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    // Lógica de Carga de Receta Diaria Aleatoria (TheMealDB)
    useEffect(() => {
        const fetchRandomRecipe = async () => {
            setIsLoading(true);
            setError(null);
            try {
                // API TheMealDB: Obtener una comida aleatoria
                const response = await fetch('https://www.themealdb.com/api/json/v1/1/random.php');
                
                if (!response.ok) {
                    throw new Error('No se pudo cargar la receta del día.');
                }

                const data = await response.json();
                setRecipe(data.meals ? data.meals[0] : null);
                
                // NOTA IMPORTANTE: La lógica de la API de Edamam (análisis nutricional) 
                // deberá ser implementada aquí o inmediatamente después de esta llamada, 
                // para que la Sidebar pueda consumir los datos nutricionales.
                
            } catch (err) {
                console.error("Error fetching meal:", err);
                setError(err.message);
            } finally {
                setIsLoading(false);
            }
        };
        fetchRandomRecipe();
    }, []);

    const renderContent = () => {
        if (isLoading) {
            // Usa el color del texto de la tarjeta (blanco o pan-tostado)
            return (
                <div className="text-xl font-bold text-pan-tostado animate-pulse p-10">
                    Preparando el plato del día... 
                </div>
            );
        }
        
        if (error || !recipe) {
            return (
                <div className="text-xl text-red-300 p-10">
                     Lo sentimos, no pudimos cargar la receta.
                </div>
            );
        }
        
        // Extraer ingredientes y medidas (TheMealDB usa un patrón de 20 pares)
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
                    border border-pan-tostado //  Color Dorado/Acento
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

    // Renderiza el contenido dentro de un contenedor centrado
    return <div className="flex justify-center">{renderContent()}</div>;
};

export default RecipeCard;