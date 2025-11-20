import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom"; 

// 1. IMPORTACIÓN DE ÍCONOS (USANDO PNG/URLS)
import TrunkImage from "./wood_32x32.png"; 
import LeafImage from "./leaf_32x32.png"; 
import FlowerImage from "./flower_32x32.png"; 
import CoffeeImage from "./coffee_32x32.png"; 
import BreadImage from "./bread_32x32.png";  


// Constantes de Página y Comportamiento
const CAFE_PATH = "/cafe";
const FLOWER_CLASS = "flower-trigger"; 
// 🚨 NUEVA CONSTANTE PARA DETECCIÓN DE ELEMENTOS CLICKEABLES
const LEAF_CLASS = "leaf-trigger"; 
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
  // 1. EFECTO DE CONTROL DEL CURSOR NATIVO (Problema 2 resuelto)
  // ----------------------------------------------------
  useEffect(() => {
    // Aplicamos la clase principal de ocultación al BODY
    if (isCursorActive) {
      // 🚨 La clase 'cursor-none' debe estar definida en tu CSS global para el body
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
  // 2. EFECTO DE MOVIMIENTO Y LÓGICA DEL BOSQUE (Problema 1 resuelto)
  // ----------------------------------------------------
  useEffect(() => {
    if (!isCursorActive) {
        return;
    }

    const updatePosition = (e) => {
      setPosition({ x: e.clientX, y: e.clientY });

      if (isCafePage) {
          // Si estamos en Café, solo movemos el cursor, no cambiamos el estado.
          return;
      }

      // 🚨 Lógica de Detección del Bosque (Prioridad por FLOWER > LEAF > TRUNK)
      const target = e.target;
      
      // 1. Prioridad FLOWER (Flechas, Iconos de Habilidad de la Sidebar)
      const isFlowerTrigger = target.closest(`.${FLOWER_CLASS}`);
      
      // 2. Prioridad LEAF (Links de Proyectos, Header, Contacto, Café)
      const isLeafTrigger = 
        target.closest(`.${LEAF_CLASS}`) || 
        target.closest("a") || 
        target.closest("button");

      // Lógica de Asignación de Estado
      if (isFlowerTrigger) {
        setCursorState(STATES.FLOWER);
      } else if (isLeafTrigger) {
        // Incluye detección de 'a' y 'button' (para Header, Contacto, Botones)
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
    // Si no es la página del Café
    if (!isCafePage) {
        // Lógica de limpieza: Si salimos de Café e ingresamos a Bosque, resetear a TRUNK.
        if (isBosquePage) { 
            setCursorState(STATES.TRUNK); 
        }
        return;
    }

    // Si entramos en la página del café, forzamos el estado inicial de Café si es necesario
    if (cursorState !== STATES.COFFEE && cursorState !== STATES.BREAD) {
        setCursorState(STATES.COFFEE);
    }

    // Intervalo que dispara el cambio de ícono
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

    // Limpieza al desmontar o cambiar de página
    return () => {
        clearInterval(intervalId);
        setIsSpinning(false); 
    };
  }, [isCafePage, isBosquePage, cursorState]);


  // ----------------------------------------------------
  // 4. LÓGICA DE RENDERIZADO Y ESTILOS
  // ----------------------------------------------------
  let currentIconSrc = null; 
  let themeClass = ""; 
  let sizeClass = "w-6 h-6";
  let transformEffect = "scale(1)";
  let altText = "Cursor Icon";

  // Definición de ícono (URL) y estilo según el estado
  switch (cursorState) {
    case STATES.TRUNK:
      currentIconSrc = TrunkImage; 
      sizeClass = "w-6 h-6";
      transformEffect = "scale(1)";
      altText = "Tronco";
      break;

    case STATES.LEAF:
      currentIconSrc = LeafImage; 
      sizeClass = "w-6 h-6";
      transformEffect = "scale(1.5)"; 
      altText = "Hoja";
      break;

    case STATES.FLOWER:
      currentIconSrc = FlowerImage; 
      sizeClass = "w-6 h-6";
      transformEffect = "scale(1.0) opacity(0.7)"; 
      altText = "Flor";
      break;

    case STATES.COFFEE:
      currentIconSrc = CoffeeImage; 
      sizeClass = "w-6 h-6";
      transformEffect = "scale(1)";
      altText = "Café";
      break;

    case STATES.BREAD:
      currentIconSrc = BreadImage; 
      sizeClass = "w-6 h-6";
      transformEffect = "scale(1.2)"; 
      altText = "Pan";
      break;

    default:
      currentIconSrc = TrunkImage;
      break;
  }

  // Si está girando, la animación de giro (rotate(360deg)) tiene prioridad.
  const rotation = isSpinning ? `rotate(360deg)` : 'rotate(0deg)';
  let finalTransformEffect = `${transformEffect} ${rotation}`;

  if (!isCursorActive || !currentIconSrc) {
    return null;
  }

  return (
    <div
      className={`
          fixed top-0 left-0 pointer-events-none z-9999
      `}
      style={{
        // 1. Posicionamiento del contenedor principal (sigue al ratón)
        transform: `translate(${position.x}px, ${position.y}px)`,
        transition: `transform 0.1s ease-out`, 
      }}
    >
        {/* 2. Contenedor del Ícono: Aplica el tamaño y efecto de transformación/giro */}
        <div
            className={`
                absolute top-0 left-0 transition-all z-9999
                ${sizeClass}
                ${themeClass}
            `}
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
            {/* 3. Renderizado de la IMAGEN PNG */}
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