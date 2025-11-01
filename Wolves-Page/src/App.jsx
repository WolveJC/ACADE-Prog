import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Componentes de Layout
import Header from "./components/Layout/Header.jsx";
import Sidebar from "./components/Layout/Sidebar.jsx";
import MainContent from "./components/Layout/MainContent.jsx";
import ContactPage from "./pages/ContactPage.jsx";

// Componentes de Interacción
import CustomCursor from "./components/Cursor/CustomCursor.js";
import { CarouselProvider } from "./context/GlobalCarousel.jsx";

function App() {
  return (
    // 1. Envolver toda la aplicación en el Router
    <Router>
      {/* 2. Renderizar el Cursor Personalizado al nivel más alto */}
      <CustomCursor />

      {/* 3. Envolver la lógica principal en el Contexto del Carrusel */}
      <CarouselProvider>
        {/* 4. Contenedor Principal: Aplicar el degradado de fondo */}
        <div
          className="
                    relative min-h-screen 
                    bg-gradient-to-b from-forest-start via-forest-mid to-forest-end
                    text-white
                "
        >
          {/* 5. Componentes Fijos: Header y Sidebar. Se muestran en TODAS las rutas */}
          <Header />
          <Sidebar />

          {/* 6. Contenido Dinámico: Aquí se gestionan las rutas */}
          <main className="pt-16">
            {/* El pt-16 (padding-top) es crucial para empujar el contenido debajo del Header fijo */}
            <Routes>
              {/* Ruta Raíz: Muestra el contenido principal */}
              <Route path="/" element={<MainContent />} />

              {/* Ruta de Contacto: Muestra la nueva página de contacto */}
              <Route path="/contact" element={<ContactPage />} />
            </Routes>
          </main>
        </div>
      </CarouselProvider>
    </Router>
  );
}

export default App;
