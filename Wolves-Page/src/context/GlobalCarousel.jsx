import React, { createContext, useContext } from "react";
import useCarousel from "../hooks/useCarousel";

// 1. Creamos el Contexto
const CarouselContext = createContext(null);

// 2. Hook de Consumo para usar el Contexto en cualquier componente
export const useCarouselContext = () => {
  const context = useContext(CarouselContext);
  if (!context) {
    // Mensaje de error útil si "alguien" olvida el Provider
    throw new Error(
      "useCarouselContext debe usarse dentro de un CarouselProvider"
    );
  }
  return context;
};

// 3. El Provider (El envoltorio que gestiona y proporciona los valores)
// totalSlides = 3 secciones únicas * 2 copias = 6. totalUniqueSlides = 3.
export const CarouselProvider = ({
  children,
  totalSlides = 6,
  totalUniqueSlides = 3,
}) => {
  // Ejecutar el hook de lógica, obteniendo TODOS los estados y handlers
  const carouselData = useCarousel(5, 40);
  const // Retornar todos los datos y funciones para que puedan ser consumidos globalmente
    value = {
      ...carouselData,
      totalSlides,
      totalUniqueSlides,
    };

  return (
    <CarouselContext.Provider value={value}>
      {children}
    </CarouselContext.Provider>
  );
};
