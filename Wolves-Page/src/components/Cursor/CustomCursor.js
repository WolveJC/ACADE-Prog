import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

// ICONOS
import TrunkImage from "./wood_32x32.png";
import LeafImage from "./leaf_32x32.png";
import FlowerImage from "./flower_32x32.png";
import CoffeeImage from "./coffee_32x32.png";
import BreadImage from "./bread_32x32.png";

// CONSTANTES
const CAFE_PATH = "/cafe";
const FLOWER_CLASS = "flower-trigger";
const LEAF_CLASS = "leaf-trigger";

const STATES = {
  TRUNK: "trunk",
  LEAF: "leaf",
  FLOWER: "flower",
  COFFEE: "coffee",
  BREAD: "bread",
};

const ICON_CYCLE_INTERVAL = 5000;
const SPIN_DURATION = 300;

const CustomCursor = () => {
  const location = useLocation();

  const isBosquePage =
    location.pathname === "/" || location.pathname === "/contact" || location.pathname === "/documentacion";
  const isCafePage = location.pathname === CAFE_PATH;

  // Cursor solo activo en Bosque y Café
  const isCursorActive = isBosquePage || isCafePage;

  // ESTADOS
  const [position, setPosition] = useState({ x: -100, y: -100 });
  const [cursorState, setCursorState] = useState(
    isCafePage ? STATES.COFFEE : STATES.TRUNK
  );
  const [isSpinning, setIsSpinning] = useState(false);

  // ----------------------------------------------------
  // 1. MOVIMIENTO DEL CURSOR
  // ----------------------------------------------------
  useEffect(() => {
    if (!isCursorActive) return;

    const updatePosition = (e) => {
      setPosition({ x: e.clientX, y: e.clientY });

      if (isCafePage) return;

      const target = e.target;

      const isFlowerTrigger = target.closest(`.${FLOWER_CLASS}`);
      const isLeafTrigger =
        target.closest(`.${LEAF_CLASS}`) ||
        target.closest("a") ||
        target.closest("button");

      if (isFlowerTrigger) setCursorState(STATES.FLOWER);
      else if (isLeafTrigger) setCursorState(STATES.LEAF);
      else setCursorState(STATES.TRUNK);
    };

    window.addEventListener("mousemove", updatePosition);
    return () => window.removeEventListener("mousemove", updatePosition);
  }, [isCursorActive, isCafePage]);

  // ----------------------------------------------------
  // 2. ANIMACIÓN DEL CAFÉ (CICLO)
  // ----------------------------------------------------
  useEffect(() => {
    if (!isCafePage) {
      if (isBosquePage) setCursorState(STATES.TRUNK);
      return;
    }

    if (cursorState !== STATES.COFFEE && cursorState !== STATES.BREAD) {
      setCursorState(STATES.COFFEE);
    }

    const intervalId = setInterval(() => {
      setIsSpinning(true);

      const spinTimeout = setTimeout(() => {
        setCursorState((prev) =>
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
  }, [isCafePage, isBosquePage, cursorState]);

  // ----------------------------------------------------
  // 3. DEFINICIÓN DE ICONO Y ESTILO
  // ----------------------------------------------------
  let currentIconSrc = TrunkImage;
  let sizeClass = "w-6 h-6";
  let transformEffect = "scale(1)";
  let altText = "Cursor";

  switch (cursorState) {
    case STATES.LEAF:
      currentIconSrc = LeafImage;
      transformEffect = "scale(1.4)";
      altText = "Hoja";
      break;

    case STATES.FLOWER:
      currentIconSrc = FlowerImage;
      transformEffect = "scale(1) opacity(0.7)";
      altText = "Flor";
      break;

    case STATES.COFFEE:
      currentIconSrc = CoffeeImage;
      altText = "Café";
      break;

    case STATES.BREAD:
      currentIconSrc = BreadImage;
      transformEffect = "scale(1.2)";
      altText = "Pan";
      break;

    default:
      currentIconSrc = TrunkImage;
      altText = "Tronco";
  }

  const rotation = isSpinning ? "rotate(360deg)" : "rotate(0deg)";
  const finalTransform = `${transformEffect} ${rotation}`;

  if (!isCursorActive) return null;

  return (
    <div
      className="fixed top-0 left-0 pointer-events-none z-[9999]"
      style={{
        transform: `translate(${position.x}px, ${position.y}px)`,
        transition: "transform 0.05s linear",
      }}
    >
      <div
        className={`absolute top-0 left-0 ${sizeClass}`}
        style={{
          transform: `translate(-50%, -50%) ${finalTransform}`,
          transition: `transform ${SPIN_DURATION}ms ease-in-out`,
        }}
      >
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
