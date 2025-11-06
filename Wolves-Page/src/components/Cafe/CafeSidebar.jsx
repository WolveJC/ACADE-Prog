import React, { useState, useEffect, useRef } from "react";
// import { useLocation } from 'react-router-dom'; // No es necesario si no se usa
// Importaciones específicas del Café
import { useNutritionContext } from "../../context/NutritionContext";
import NutritionBar from "./NutritionBar";
import { nutritionData } from "../../data/nutrition";

// Clase para el cursor (se mantiene)
const FLOWER_CLASS = "flower-trigger";

// Mapeo para conectar el nombre estático con la clave dinámica de Edamam
const EDAMAM_KEY_MAP = {
  // ... (Tu mapeo de EDAMAM_KEY_MAP se mantiene sin cambios) ...
  // Macronutrientes y Generales
  Calorías: "ENERC_KCAL",
  Proteínas: "PROCNT",
  Carbohidratos: "CHOCDF",
  "Grasas Totales": "FAT",
  Fibra: "FIBTG",
  Azúcares: "SUGAR",
  Sodio: "NA",
  Colesterol: "CHOLE",

  // Subdivisiones de Grasas
  "Grasas Saturadas": "FASAT",
  "Grasas Monoinsaturadas": "FAMS",
  "Grasas Poliinsaturadas": "FAPU",

  // Minerales
  Fósforo: "P",
  Calcio: "CA",
  Hierro: "FE",
  Magnesio: "MG",
  Potasio: "K",
  Zinc: "ZN",

  // Vitaminas
  "Vitamina A": "VITA_RAE",
  "Vitamina C": "VITC",
  "Vitamina D": "VITD",
  "Vitamina E": "TOCPHA",
  "Vitamina K": "VITK1",
  "Vitamina B6": "VITB6A",
};

const CafeSidebar = () => {
  // 1. Estados y Hooks de la Lupa/Hover
  const [mousePosition, setMousePosition] = useState(null); // Inicializar como null
  const [isSidebarHovering, setIsSidebarHovering] = useState(false);
  const sidebarRef = useRef(null);

  // Hook para rastrear el movimiento del mouse SOLO cuando el mouse está dentro del componente
  const handleMouseMove = (e) => {
    if (sidebarRef.current) {
      setMousePosition({ x: e.clientX, y: e.clientY });
    }
  };

  // 2. Consumo de Datos de Nutrición
  const {
    nutritionData: edamamData,
    isNutritionLoading,
    nutritionError,
  } = useNutritionContext();

  // 3. Estilos
  // Eliminamos el 'w-16' estático del ancho principal, dejamos que la columna del layout lo defina.
  // Estilos fijos del café (se mantienen)
  const finalBgClass = "bg-cafe-oscuro border-r border-pan-tostado";

  // ----------------------------------------------------
  // 4. RENDERIZADO DEL CONTENIDO NUTRICIONAL
  // ----------------------------------------------------
  const renderContent = () => {
    if (isNutritionLoading) {
      return (
        <div className="text-sm text-pan-tostado mt-4 animate-pulse px-1">
          Analizando nutrición...
        </div>
      );
    }

    if (nutritionError || !edamamData || !edamamData.totalNutrients) {
      // Muestra el mensaje de error de nutrición de forma más clara si el fetch falla
      const message = nutritionError || "No hay datos nutricionales listos.";
      return (
        <div className="text-xs text-red-300 mt-4 px-1 leading-snug">
          Error: {message}
        </div>
      );
    }

    const totalNutrients = edamamData.totalNutrients;

    return (
      <div className="flex flex-col space-y-6 mt-4">
        {nutritionData.map((staticNutrient) => {
          const edamamKey = EDAMAM_KEY_MAP[staticNutrient.name];

          // Aseguramos la búsqueda de la clave Edamam correcta
          const dynamicNutrient = totalNutrients[edamamKey];

          // Filtrado: Si no hay valor o la cantidad es 0, no se renderiza.
          const hasValue = dynamicNutrient && dynamicNutrient.quantity > 0;

          if (hasValue) {
            return (
              <NutritionBar
                key={staticNutrient.name}
                staticData={staticNutrient}
                apiData={dynamicNutrient}
                allApiData={totalNutrients} // Pasamos la data completa para las sub-barras
                mousePosition={mousePosition}
                sidebarRef={sidebarRef}
                isSidebarHovering={isSidebarHovering}
              />
            );
          }
          return null;
        })}
      </div>
    );
  };

  return (
    <div
      ref={sidebarRef}
      className={`
                // CRÍTICO: Eliminamos 'fixed top-0 left-0 h-screen'
                sticky top-20 // Se pega debajo del Header (pt-20 de CafePage)
                w-full // Ocupa el 100% de la columna que le asignó CafePage.jsx
                h-[calc(100vh-100px)] // Le da una altura definida para ser 'sticky'
                flex flex-col items-center p-4 
                shadow-2xl transition-all duration-300 ease-in-out
                ${FLOWER_CLASS} 
                ${finalBgClass} 
                rounded-xl // Añadimos el redondeo para mejor estética
                overflow-y-auto // Permitimos scroll si hay muchos nutrientes
            `}
      onMouseEnter={() => setIsSidebarHovering(true)}
      onMouseLeave={() => setIsSidebarHovering(false)}
      onMouseMove={handleMouseMove} //  CRÍTICO: Movemos el manejador del mouse aquí
    >
      {renderContent()}
    </div>
  );
};

export default CafeSidebar;
