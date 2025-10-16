import React from "react";
import Header from "./components/Layout/Header.jsx";
import Sidebar from "./components/Layout/Sidebar.jsx";
import MainContent from "./components/Layout/MainContent.jsx";

// Definir los colores  aquí para que se apliquen al body/principal div
// Los tonos deben coincidir con lo que se configuro en tailwind.config.js:
// 'forest-start', 'forest-mid', 'forest-end'

function App() {
  return (
    // 1. Contenedor Principal: Aplicar el degradado de fondo vertical a toda la página.
    // bg-gradient-to-b: Degradado de arriba (top) a abajo (bottom).
    <div
      className="
        relative min-h-screen 
        bg-gradient-to-b from-forest-start via-forest-mid to-forest-end
        text-white
      "
    >
      {/* 2. Header: Fijo en la parte superior (z-50) */}
      <Header />

      {/* 3. Sidebar: Fija en la izquierda (z-40) */}
      <Sidebar />

      {/* 4. Contenido Principal: Ocupa el resto del espacio y contiene el carrusel */}
      <main className="pt-16">
        {/* El pt-16 (padding-top) es crucial para empujar el contenido debajo del Header fijo */}
        <MainContent />
      </main>
    </div>
  );
}

export default App;
