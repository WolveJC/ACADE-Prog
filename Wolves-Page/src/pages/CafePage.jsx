import React, { useState, useCallback, useEffect } from 'react';
import usePageTitle from '../hooks/usePageTitle';
import RecipeCard from '../components/Cafe/RecipeCard'; 
import TriviaWidget from '../components/Cafe/TriviaWidget';
import CafeSidebar from '../components/Cafe/CafeSidebar';
import { useNutritionContext } from '../context/NutritionContext';

// Antes: la key de RapidAPI vivía aquí en texto plano, y este mismo
// archivo normalizaba los ingredientes (normalizeIngredient /
// formatIngredientsForEdamam) antes de llamar a RapidAPI directo.
// Ahora todo eso se mudó a Wolves-Page-Backend: el cliente solo manda
// la receta completa (tal cual la devuelve MealDB) y el backend hace
// la normalización + la llamada a RapidAPI con su key, que el
// navegador nunca ve.
const BACKEND_URL = process.env.BACKEND_URL;

const CafePage = () => {
  usePageTitle("WolveJC | El Café de las APIs");

  const { setIsNutritionLoading, setEdamamData, nutritionError } = useNutritionContext();
  const [recipeData, setRecipeData] = useState(null);
  const [hasFetchedNutrition, setHasFetchedNutrition] = useState(false); 

  // Callback para recibir la receta de RecipeCard
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
    // 1. Validaciones iniciales
    if (!recipeData || hasFetchedNutrition) return; 

    // Validación rápida en el cliente: si la receta no trae ni un
    // ingrediente, ni vale la pena llamar al backend. La normalización
    // real (y la llamada a RapidAPI) ya vive del lado del servidor.
    const hasAnyIngredient = Array.from({ length: 20 }, (_, i) => i + 1).some(
      (i) => recipeData[`strIngredient${i}`]?.trim()
    );
    if (!hasAnyIngredient) {
      setEdamamData(null, "No se encontraron ingredientes para el análisis nutricional.");
      setHasFetchedNutrition(true); // Si no hay ingredientes, marcamos como fetch terminada
      return;
    }

    // 2. Marcar el estado como true.
    // Esto asegura que la segunda pasada del Strict Mode se detenga en la validación inicial.
    setHasFetchedNutrition(true); 

    setIsNutritionLoading(true);

    let userErrorMessage = "Error desconocido. Vuelve a intentarlo más tarde.";

    try {
      // Mandamos la receta completa (tal cual la devolvió MealDB) al
      // backend; él normaliza los ingredientes y llama a RapidAPI con
      // su key, que el navegador nunca ve.
      const response = await fetch(`${BACKEND_URL}/api/nutricion`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ recipe: recipeData }),
      });

      if (!response.ok) {
        const status = response.status;
        let developerMessage = `Error de API [${status}].`;

        if (status === 429) {
          userErrorMessage = "¡Límite de solicitudes excedido! 😥 ";
        } else if (status >= 500) {
          userErrorMessage = "El servicio de nutrición falló temporalmente. ¡Prueba recargar en un minuto!";
        } else {
          userErrorMessage = `Error ${status}: La solicitud falló.`;
        }

        try {
          const errorBody = await response.json();
          developerMessage += ` Detalle: ${errorBody.error || errorBody.message || response.statusText}`;
        } catch {
          developerMessage += ` Detalle: ${response.statusText}`;
        }
        console.error("❌ Error del backend de nutrición:", developerMessage);

        // Si hay error, queremos que el usuario pueda reintentar, por lo que NO restablecemos hasFetchedNutrition.
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
      console.error("⚠️ Error final al cargar el JSON/Datos:", err);

    } finally {
      setIsNutritionLoading(false);
    }
  }, [recipeData, hasFetchedNutrition, setEdamamData, setIsNutritionLoading]);

  useEffect(() => {
    // Este useEffect ahora solo se ejecutará cuando recipeData cambie, y la lógica interna de fetchNutritionData
    // se encargará de limitar la ejecución a una sola vez.
    if (recipeData && !hasFetchedNutrition) {
      fetchNutritionData();
    }
  }, [recipeData, hasFetchedNutrition, fetchNutritionData]);

  return (
    <div className="min-h-screen pb-10 bg-leche-crema text-cafe-oscuro transition-colors duration-500">
      {nutritionError && (
        <div className="fixed top-16 left-0 w-full bg-red-600 text-white font-medium text-center py-2 z-50 transition-all duration-300 shadow-md">
          <p className="max-w-7xl mx-auto px-4 md:px-6 flex items-center justify-center space-x-2">
            <span>⚠️</span>
            <span className="text-sm md:text-base">{nutritionError}</span>
          </p>
        </div>
      )}

      <div className={`max-w-7xl mx-auto px-4 md:px-6 ${nutritionError ? 'pt-36' : 'pt-28'}`}> 
        <h2 className="text-4xl md:text-5xl font-serif font-bold text-center mb-4 text-cafe-oscuro">
          El Café de las APIs
        </h2>
        <p className="text-lg text-gray-500 text-center mb-8 max-w-3xl mx-auto italic">
          Una pausa para explorar la sinergia de los datos. Hoy te servimos una receta al azar.
        </p>

        <div className="flex flex-col lg:flex-row lg:items-start lg:space-x-8">
          <aside className="w-full lg:w-40 shrink-0 mb-6 lg:mb-0 lg:sticky lg:top-28"> 
            <CafeSidebar /> 
          </aside>

          {/* COMIENZO DEL CONTENIDO PRINCIPAL */}
          <main className="grow">
            <div className="flex flex-col items-center">

              <RecipeCard onRecipeLoaded={handleRecipeLoaded} />

              <div className="w-full max-w-4xl mt-6"> 
                <TriviaWidget />
              </div>

            </div>
          </main>
        </div> {/* Cierra el div del contenedor flex principal */}

      </div> {/* Cierra el div max-w-7xl mx-auto */}
    </div> // Cierra el div min-h-screen
  );
};

export default CafePage;