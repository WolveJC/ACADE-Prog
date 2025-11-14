import React, { useState, useCallback, useEffect } from 'react';
import usePageTitle from '../hooks/usePageTitle';
import RecipeCard from '../components/Cafe/RecipeCard'; 
import TriviaWidget from '../components/Cafe/TriviaWidget';
import CafeSidebar from '../components/Cafe/CafeSidebar';
import { useNutritionContext } from '../context/NutritionContext';

// Constantes de la API de Edamam
const RAPIDAPI_KEY = 'ea40e1fb71msh1630c71aa1e941dp15b910jsndb8283303c08'; 
const RAPIDAPI_HOST = 'edamam-edamam-nutrition-analysis.p.rapidapi.com';

// Función para normalizar medida + ingrediente
const normalizeIngredient = (measure, ingredient) => {
  let m = (measure || "").trim().toLowerCase();
  let ing = (ingredient || "").trim().toLowerCase();

  // Correcciones comunes de unidades
  m = m
    .replace(/\btbs\b/g, "tbsp")
    .replace(/\btbls\b/g, "tbsp")
    .replace(/\btsp\b/g, "tsp")
    .replace(/\bml\b/g, " ml")
    .replace(/\bg\b/g, " g")
    .replace(/\bkg\b/g, " kg")
    .replace(/\bl\b/g, " l")
    .replace(/\bpinch\b/g, "1 pinch")
    .replace(/\bdash\b/g, "1 dash")
    .replace(/\bto taste\b/g, "")
    .replace(/\bas needed\b/g, "");

  // Correcciones de ingredientes
  ing = ing
    .replace(/free[- ]?range/gi, "") // quita "free-range"
    .replace(/beaten/gi, "")         // quita "beaten"
    .replace(/pinkling/gi, "pickling")
    .replace(/sea salt/gi, "salt")
    .replace(/black pepper/gi, "pepper")
    .replace(/clove[s]? garlic/gi, "garlic")
    .replace(/egg[s]?/gi, "egg");

  // Reconstruir string limpio
  let formatted = `${m} ${ing}`.trim();

  // Si no hay medida, al menos devolver el ingrediente
  if (!m) formatted = ing;

  return formatted;
};

// 🛠️ Función para formatear ingredientes de MealDB para Edamam
const formatIngredientsForEdamam = (recipe) => {
  let queryParts = [];
  for (let i = 1; i <= 20; i++) {
    const ingredient = recipe[`strIngredient${i}`];
    const measure = recipe[`strMeasure${i}`];
    if (ingredient && ingredient.trim() !== "") {
      const normalized = normalizeIngredient(measure, ingredient);
      queryParts.push(`ingr=${encodeURIComponent(normalized)}`);
    }
  }
  return queryParts.join("&");
};

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

    const ingredientQuery = formatIngredientsForEdamam(recipeData);
    if (!ingredientQuery) {
      setEdamamData(null, "No se encontraron ingredientes para el análisis nutricional.");
      setHasFetchedNutrition(true); // Si no hay query, marcamos como fetch terminada
      return;
    }

    // 2. Marcar el estado como true.
    // Esto asegura que la segunda pasada del Strict Mode se detenga en la validación inicial.
    setHasFetchedNutrition(true); 

    // Debug: mostrar ingredientes normalizados (Solo se ejecutará una vez)
    const ingredientList = [];
    for (let i = 1; i <= 20; i++) {
      const ingredient = recipeData[`strIngredient${i}`];
      const measure = recipeData[`strMeasure${i}`];
      if (ingredient && ingredient.trim() !== "") {
        ingredientList.push(normalizeIngredient(measure, ingredient));
      }
    }

    const apiUrlBase = `https://${RAPIDAPI_HOST}/api/nutrition-data?nutrition-type=cooking&`;

    console.log("=====================================================");
    console.log("🍽️ DEBUG: INGREDIENTES NORMALIZADOS PARA EDAMAM (Receta):", recipeData.strMeal);
    console.log("-----------------------------------------------------");
    console.log("INGREDIENTES LISTA (Normalizados):", ingredientList); 
    console.log("URL de Query FINAL:", `${apiUrlBase}${ingredientQuery}`);
    console.log("=====================================================");

    setIsNutritionLoading(true);
    const apiUrl = `${apiUrlBase}${ingredientQuery}`;

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
        } else {
          userErrorMessage = `Error ${status}: La solicitud falló.`;
        }

        try {
          const errorBody = await response.json();
          developerMessage += ` Detalle: ${errorBody.error || errorBody.message || response.statusText}`;
        } catch {
          developerMessage += ` Detalle: ${response.statusText}`;
        }
        console.error("❌ Error de Edamam:", developerMessage);

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
        <div className="fixed top-[4rem] left-0 w-full bg-red-600 text-white font-medium text-center py-2 z-50 transition-all duration-300 shadow-md">
          <p className="max-w-7xl mx-auto px-4 md:px-6 flex items-center justify-center space-x-2">
            <span>⚠️</span>
            <span className="text-sm md:text-base">{nutritionError}</span>
          </p>
        </div>
      )}

      <div className={`max-w-7xl mx-auto px-4 md:px-6 ${nutritionError ? 'pt-[9rem]' : 'pt-[7rem]'}`}> 
        <h2 className="text-4xl md:text-5xl font-serif font-bold text-center mb-4 text-cafe-oscuro">
          El Café de las APIs
        </h2>
        <p className="text-lg text-gray-500 text-center mb-8 max-w-3xl mx-auto italic">
          Una pausa para explorar la sinergia de los datos. Hoy te servimos una receta al azar.
        </p>

        <div className="flex flex-col lg:flex-row lg:items-start lg:space-x-8">
          <aside className="w-full lg:w-40 flex-shrink-0 mb-6 lg:mb-0 lg:sticky lg:top-[7rem]"> 
            <CafeSidebar /> 
          </aside>

          {/* COMIENZO DEL CONTENIDO PRINCIPAL */}
          <main className="flex-grow">
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