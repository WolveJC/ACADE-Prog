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
// totalUniqueSlides debe reflejar el número REAL de secciones que arma
// MainContent.jsx (Welcome + páginas de proyectos + AboutMe). App.jsx lo
// calcula con getUniqueSectionsCount() y lo pasa aquí; los defaults (6/3)
// solo son un respaldo por si algún día el Provider se usa sin ese prop.
export const CarouselProvider = ({
  children,
  totalSlides = 6,
  totalUniqueSlides = 3,
}) => {
  // Antes: useCarousel(5, 40) ignoraba totalUniqueSlides por completo,
  // por eso el hook seguía con su propio "% 3" hardcodeado internamente.
  const carouselData = useCarousel(5, 40, totalUniqueSlides);
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