import React, { useRef } from "react";
import { useNutritionContext } from "../../context/NutritionContext";
import { nutritionData as staticNutritionData } from "../../data/nutrition"; // Datos estáticos

const CafeSidebar = () => {
  const { nutritionData, isNutritionLoading, nutritionError } =
    useNutritionContext();
  const sidebarRef = useRef(null);

  // Renderiza el contenido dinámico del sidebar
  const renderContent = () => {
    if (isNutritionLoading) {
      return (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-pan-tostado mx-auto mb-2"></div>
          <p className="text-sm text-pan-tostado">Cargando...</p>
        </div>
      );
    }

    // CRÍTICO: NO mostrar nutritionError aquí. La franja superior ya lo hace.
    if (!nutritionData || !nutritionData.totalNutrients) {
      // Mostrar un mensaje "No hay datos" SOLO si no hay un error global.
      // Si hay un error global (nutritionError), la franja ya lo maneja.
      if (nutritionError) {
        return (
          <div className="text-center py-8 text-sm text-gray-400 italic">
            No hay datos de nutrición disponibles.
          </div>
        );
      }
      return (
        <div className="text-center py-8 text-sm text-gray-400 italic">
          Sin datos nutricionales.
        </div>
      );
    }

    // Si hay datos, renderizar la lista de nutrientes
    return (
      <ul className="space-y-3">
        {staticNutritionData.map((item, index) => {
          const nutrientKey = item.name.replace(/\s+/g, ""); // Ej: 'Calorías' -> 'Calorias'
          // Encuentra el valor del nutriente en el data de Edamam
          const nutrientInfo = nutritionData.totalNutrients[nutrientKey];
          let displayValue = null;
          if (nutrientInfo && typeof nutrientInfo.quantity === "number") {
            displayValue = nutrientInfo.quantity.toFixed(0); // Redondea para mejor lectura
          }

          // Si no encontramos un valor específico de Edamam, usa el valor estático o null
          // Para el ejercicio, solo mostraremos los que vienen de Edamam
          if (
            displayValue === null &&
            item.name !== "Calorías" &&
            item.name !== "Proteínas" &&
            item.name !== "Carbohidratos" &&
            item.name !== "Grasas Totales"
          ) {
            return null; // O puedes mostrar 0 o N/A, dependiendo de tu UX
          }

          // Asegurarse de que el color del ícono se aplique correctamente
          const IconComponent = item.Icon;

          return (
            <li
              key={index}
              className="flex items-center space-x-2 text-white/90"
            >
              <IconComponent
                className={`${item.iconColor} text-lg md:text-xl flex-shrink-0`}
              />
              <span className="font-semibold text-sm flex-grow">
                {item.name}
              </span>
              <span className="text-xs font-normal text-white/70">
                {displayValue !== null ? `${displayValue}${item.unit}` : "N/A"}
              </span>
            </li>
          );
        })}
      </ul>
    );
  };

  return (
    <div
      ref={sidebarRef}
      className="
                bg-moca p-4 rounded-lg shadow-xl border border-pan-tostado
                lg:h-[calc(100vh-8rem)] lg:overflow-y-auto lg:sticky lg:top-[7rem] 
                transition-all duration-300 ease-in-out
                flex flex-col
            "
    >
      <h3 className="text-xl font-serif font-bold text-pan-tostado mb-4 text-center">
        Nutrición
      </h3>
      {renderContent()}
    </div>
  );
};

export default CafeSidebar;
