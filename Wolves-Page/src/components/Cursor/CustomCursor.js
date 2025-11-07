import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom"; // CRÍTICO: Importar useLocation

// Estados del Cursor
const STATES = {
  TRUNK: "trunk",
  LEAF: "leaf",
  FLOWER: "flower",
};

// Clase que los componentes complejos deben aplicar (ej. Sidebar del Bosque)
const FLOWER_CLASS = "flower-trigger"; 
// Clase CSS definida en index.css para ocultar el cursor nativo
const CURSOR_NONE_CLASS = "cursor-none"; 


const CustomCursor = () => {
  const location = useLocation();
  // El cursor solo debe estar activo en la página principal (Bosque)
  const isBosquePage = location.pathname === "/" || location.pathname === "/contact"; // Incluir /contact si también quieres el cursor allí

  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [cursorState, setCursorState] = useState(STATES.TRUNK);
  
  // No necesitamos el estado 'isPointer' ya que está implícito en cursorState

  // 1. Efecto para controlar el cursor nativo y adjuntar el listener de mousemove
  useEffect(() => {
    // ----------------------------------------------------
    // LÓGICA DE CONTROL DEL CURSOR NATIVO (<body>)
    // ----------------------------------------------------
    if (isBosquePage) {
      // Activar: Ocultar el cursor nativo
      document.body.classList.add(CURSOR_NONE_CLASS);
    } else {
      // Desactivar: Restaurar el cursor nativo
      document.body.classList.remove(CURSOR_NONE_CLASS);
      // Salir del useEffect si no estamos en la página del Bosque
      return; 
    }

    // Función de limpieza: CRÍTICA. Asegura que el cursor nativo se restaure
    // si el componente se desmonta o el path cambia (ej. ir a /cafe)
    return () => {
      document.body.classList.remove(CURSOR_NONE_CLASS);
      // El listener de mousemove se limpia en el siguiente useEffect
    };
  }, [isBosquePage]);


  // 2. Efecto para seguir el ratón y detectar interactividad (SOLO si isBosquePage es true)
  useEffect(() => {
    // Si no estamos en la página del Bosque, salimos y no adjuntamos el listener
    if (!isBosquePage) {
        return;
    }

    const updatePosition = (e) => {
      setPosition({ x: e.clientX, y: e.clientY });

      const target = e.target;

      // Detección del puntero (cursor: pointer)
      const pointer =
        target.closest("a") ||
        target.closest("button") ||
        target.style.cursor === "pointer";

      // Detección de interacción compleja (flower-trigger)
      const isFlowerTrigger = target.closest(`.${FLOWER_CLASS}`);

      // Lógica de Asignación de Estado (Prioridad: FLOR > HOJA > TRONCO)
      if (isFlowerTrigger) {
        setCursorState(STATES.FLOWER);
      } else if (pointer) {
        setCursorState(STATES.LEAF);
      } else {
        setCursorState(STATES.TRUNK);
      }
    };

    // Escucha de eventos (solo si isBosquePage es true)
    window.addEventListener("mousemove", updatePosition);

    return () => {
      // Limpieza del listener de mousemove
      window.removeEventListener("mousemove", updatePosition);
    };
  }, [isBosquePage]); // Se re-ejecuta solo si cambiamos de Bosque a Café

  // 3. Definición de Estilos Dinámicos y Animación (Se mantiene igual)
  let sizeClass = "w-6 h-6";
  let themeClass = "";
  let transformBase = "translate(-50%, -50%)";
  let transformEffect = "";

  switch (cursorState) {
    case STATES.TRUNK:
      themeClass = "bg-amber-800/80 border-amber-900 border-4 rounded-md";
      sizeClass = "w-4 h-4";
      transformEffect = "scale(1) rotate(0deg)";
      break;

    case STATES.LEAF:
      themeClass = "border-green-500 border-2 bg-green-500/20 rounded-full";
      sizeClass = "w-6 h-6";
      transformEffect = "scale(1.5)"; 
      break;

    case STATES.FLOWER:
      themeClass = "border-pink-400 border-3 bg-white/90 rounded-full";
      sizeClass = "w-8 h-8";
      transformEffect = "scale(1) opacity(0.7)";
      break;

    default:
      themeClass = "border-gray-500 bg-gray-500/50 rounded-full";
      break;
  }

  // 4. Renderizado Condicional: No renderizar el marcado si no es la página del Bosque
  if (!isBosquePage) {
    return null;
  }

  return (
    <div
      className={`
                fixed top-0 left-0 pointer-events-none transition-all duration-300 ease-out z-[9999]
                ${sizeClass}
                ${themeClass}
            `}
      style={{
        transform: `
                    translate(${position.x}px, ${position.y}px) 
                    ${transformBase} 
                    ${transformEffect}
                `,
      }}
    />
  );
};

export default CustomCursor;