import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom"; 

// 1. IMPORTACIÓN DE ÍCONOS (USANDO URLS)
import TrunkImage from "./wood_32x32.png"; 
import LeafImage from "./leaf_32x32.png"; 
import FlowerImage from "./flower_32x32.png"; 
import CoffeeImage from "./coffee_32x32.png"; 
import BreadImage from "./bread_32x32.png"; 


// Constantes de Página y Comportamiento
const CAFE_PATH = "/cafe";
const FLOWER_CLASS = "flower-trigger"; 
const CURSOR_NONE_CLASS = "cursor-none"; 

const STATES = {
  TRUNK: "trunk",
  LEAF: "leaf",
  FLOWER: "flower",
  COFFEE: "coffee", 
  BREAD: "bread",   
};

const ICON_CYCLE_INTERVAL = 5000; // 5 segundos para cambiar de ícono en Café
const SPIN_DURATION = 300; // 0.3 segundos para la animación de giro

const CustomCursor = () => {
  const location = useLocation();
  
  // Detección de página
  const isBosquePage = location.pathname === "/" || location.pathname === "/contact";
  const isCafePage = location.pathname === CAFE_PATH;
  const isCursorActive = isBosquePage || isCafePage; 

  // Estados
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [cursorState, setCursorState] = useState(isCafePage ? STATES.COFFEE : STATES.TRUNK);
  const [isSpinning, setIsSpinning] = useState(false); 
  
  // ----------------------------------------------------
  // 1. EFECTO DE CONTROL DEL CURSOR NATIVO
  // ----------------------------------------------------
  useEffect(() => {
    if (isCursorActive) {
      document.body.classList.add(CURSOR_NONE_CLASS);
    } else {
      document.body.classList.remove(CURSOR_NONE_CLASS);
      return; 
    }

    return () => {
      document.body.classList.remove(CURSOR_NONE_CLASS);
    };
  }, [isCursorActive]);

  // ----------------------------------------------------
  // 2. EFECTO DE MOVIMIENTO Y LÓGICA DEL BOSQUE
  // ----------------------------------------------------
  useEffect(() => {
    if (!isCursorActive) {
        return;
    }

    const updatePosition = (e) => {
      setPosition({ x: e.clientX, y: e.clientY });

      if (isCafePage) {
          return;
      }
      
      // Lógica de Interacción del Bosque
      const target = e.target;
      const pointer =
        target.closest("a") ||
        target.closest("button") ||
        target.style.cursor === "pointer";
      const isFlowerTrigger = target.closest(`.${FLOWER_CLASS}`);

      // Lógica de Asignación de Estado (Bosque)
      if (isFlowerTrigger) {
        setCursorState(STATES.FLOWER);
      } else if (pointer) {
        setCursorState(STATES.LEAF);
      } else {
        setCursorState(STATES.TRUNK);
      }
    };

    window.addEventListener("mousemove", updatePosition);

    return () => {
      window.removeEventListener("mousemove", updatePosition);
    };
  }, [isCursorActive, isCafePage]);

  // ----------------------------------------------------
  // 3. EFECTO DE CICLO Y GIRO DEL CAFÉ
  // ----------------------------------------------------
  useEffect(() => {
    if (!isCafePage) {
        if (isBosquePage) {
            setCursorState(STATES.TRUNK);
        }
        return;
    }
    
    if (cursorState !== STATES.COFFEE && cursorState !== STATES.BREAD) {
        setCursorState(STATES.COFFEE);
    }

    const intervalId = setInterval(() => {
        setIsSpinning(true); 
        
        const spinTimeout = setTimeout(() => {
            setCursorState(prev => 
                prev === STATES.COFFEE ? STATES.BREAD : STATES.COFFEE
            );
            setIsSpinning(false); 
        }, SPIN_DURATION);

        return () => clearTimeout(spinTimeout);
        
    }, ICON_CYCLE_INTERVAL); 

    return () => {
        clearInterval(intervalId);
        setIsSpinning(false); 
    };
  }, [isCafePage]); 


  // ----------------------------------------------------
  // 4. LÓGICA DE RENDERIZADO Y ESTILOS (AJUSTADO)
  // ----------------------------------------------------
  let currentIconSrc = null;
  let sizeClass = "w-8 h-8";
  let transformEffect = "scale(1)";
  let altText = "Cursor Icon";

  // Definición de ícono (URL) y estilo según el estado
  switch (cursorState) {
    case STATES.TRUNK:
      currentIconSrc = TrunkImage;
      sizeClass = "w-8 h-8";
      transformEffect = "scale(1)";
      altText = "Tronco";
      break;

    case STATES.LEAF:
      currentIconSrc = LeafImage;
      sizeClass = "w-8 h-8";
      transformEffect = "scale(1.5)"; 
      altText = "Hoja";
      break;

    case STATES.FLOWER:
      currentIconSrc = FlowerImage;
      sizeClass = "w-8 h-8";
      transformEffect = "scale(1) opacity(0.7)"; // Si quieres que la imagen se desvanezca
      altText = "Flor";
      break;
      
    case STATES.COFFEE:
      currentIconSrc = CoffeeImage;
      sizeClass = "w-8 h-8";
      transformEffect = "scale(1)";
      altText = "Café";
      break;
      
    case STATES.BREAD:
      currentIconSrc = BreadImage;
      sizeClass = "w-8 h-8";
      transformEffect = "scale(1.2)"; 
      altText = "Pan";
      break;

    default:
      currentIconSrc = TrunkImage;
      break;
  }

  // Si está girando, la animación de giro tiene prioridad sobre otros efectos.
  const rotation = isSpinning ? `rotate(360deg)` : 'rotate(0deg)';
  let finalTransformEffect = `${transformEffect} ${rotation}`;
  
  if (!isCursorActive || !currentIconSrc) {
    return null;
  }

  return (
    <div
      className={`
          fixed top-0 left-0 pointer-events-none z-[9999]
      `}
      style={{
        // 1. Posicionamiento del contenedor principal (sigue al ratón)
        transform: `translate(${position.x}px, ${position.y}px)`,
        transition: `transform 0.1s ease-out`, 
      }}
    >
        {/* 2. Contenedor del Ícono: Aplica el tamaño, y efecto de transformación/giro */}
        <div
            className={`
                absolute top-0 left-0 transition-all z-[9999]
                ${sizeClass}`}
            style={{
                // Traslación para centrar el ícono + Efecto (escala/giro)
                transform: `
                    translate(-50%, -50%) 
                    ${finalTransformEffect}
                `,
                // Transición específica para el giro
                transition: `transform ${SPIN_DURATION / 1000}s ease-in-out, width 0.3s, height 0.3s, opacity 0.3s`,
            }}
        >
            {/* 3. Renderizado de la IMAGEN */}
            <img 
                src={currentIconSrc} 
                alt={altText} 
                className="w-full h-full object-contain"
            />
        </div>
    </div>
  );
};

export default CustomCursor;