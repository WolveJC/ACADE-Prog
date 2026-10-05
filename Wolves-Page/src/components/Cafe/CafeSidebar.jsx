import React, { useRef, useState, useEffect } from "react";
import { useNutritionContext } from "../../context/NutritionContext";
import { nutritionData as staticNutritionData } from "../../data/nutrition"; // Datos estáticos
import NutritionBar from "./NutritionBar";

const CafeSidebar = () => {
  const { nutritionData, isNutritionLoading, nutritionError } =
    useNutritionContext();
  const sidebarRef = useRef(null);

  // Mismo patrón de tracking de mouse que Sidebar.jsx (Bosque) usa para
  // Skill-Icon.jsx: NutritionBar es su "gemelo" y necesita exactamente
  // estos dos datos (posición del mouse + si el sidebar está en hover)
  // para el efecto de lupa.
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const [isSidebarHovering, setIsSidebarHovering] = useState(false);

  useEffect(() => {
    let frameId = null;

    const handleMouseMove = (e) => {
      if (frameId) cancelAnimationFrame(frameId);
      frameId = requestAnimationFrame(() => {
        setMousePosition({ x: e.clientX, y: e.clientY });
      });
    };

    window.addEventListener("mousemove", handleMouseMove);
    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      if (frameId) cancelAnimationFrame(frameId);
    };
  }, []);

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

    // Si hay datos, renderizar un NutritionBar por cada nutriente
    // (el gemelo de SkillIcon: ícono con lupa + barra animada al pasar
    // el mouse, en vez de una lista plana de texto).
    const CORE_MACROS = ["Calorías", "Proteínas", "Carbohidratos", "Grasas Totales"];

    return (
      <div className="space-y-1">
        {staticNutritionData.map((item) => {
          const nutrientKey = item.name.replace(/\s+/g, ""); // Ej: 'Calorías' -> 'Calorias'
          // Encuentra el valor del nutriente en el data de Edamam
          const nutrientInfo = nutritionData.totalNutrients[nutrientKey];
          const isCoreMacro = CORE_MACROS.includes(item.name);

          // Si no encontramos un valor específico de Edamam Y no es uno
          // de los 4 macros núcleo, no se muestra (igual que antes, para
          // no listar 20 barras en 0 cuando el dato simplemente no vino).
          if (!nutrientInfo && !isCoreMacro) return null;

          const apiData = {
            quantity:
              nutrientInfo && typeof nutrientInfo.quantity === "number"
                ? nutrientInfo.quantity
                : 0,
            unit: (nutrientInfo && nutrientInfo.unit) || item.unit,
          };

          return (
            <NutritionBar
              key={item.name}
              staticData={item}
              apiData={apiData}
              mousePosition={mousePosition}
              sidebarRef={sidebarRef}
              isSidebarHovering={isSidebarHovering}
            />
          );
        })}
      </div>
    );
  };

  return (
    <div
      ref={sidebarRef}
      className="
                bg-moca p-4 rounded-lg shadow-xl border border-pan-tostado
                lg:h-[calc(100vh-8rem)] lg:overflow-y-auto lg:sticky lg:top-28 
                transition-all duration-300 ease-in-out
                flex flex-col
            "
      onMouseEnter={() => setIsSidebarHovering(true)}
      onMouseLeave={() => setIsSidebarHovering(false)}
    >
      <h3 className="text-xl font-serif font-bold text-pan-tostado mb-4 text-center">
        Nutrición
      </h3>
      {renderContent()}
    </div>
  );
};

export default CafeSidebar;
