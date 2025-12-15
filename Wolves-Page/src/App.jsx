import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";

// Componentes de Layout
import Header from "./components/Layout/Header.jsx";
import Sidebar from "./components/Layout/Sidebar.jsx";
import MainContent from "./components/Layout/MainContent.jsx";
import ContactPage from "./pages/ContactPage.jsx";
import CafePage from "./pages/CafePage.jsx";
import ProjectDocumentationViewer from "./pages/ProjectDocumentationViewer.jsx";
import TransitionOverlay from "./components/Layout/TransitionOverlay";

// Componentes y Contextos
import CustomCursor from "./components/Cursor/CustomCursor.js";
import { CarouselProvider } from "./context/GlobalCarousel.jsx";
import { TransitionProvider } from "./context/TransitionContext";
import { NutritionProvider } from "./context/NutritionContext";

// --------------------------------------------------------
const LayoutWrapper = () => {
  const location = useLocation();
  const isCafePage = location.pathname === "/cafe";
  const isDocPage = location.pathname === "/documentacion";

  const bgClasses = isCafePage
    ? "bg-leche-crema text-cafe-oscuro"
    : "bg-linear-to-b from-forest-start via-forest-mid to-forest-end text-white";

  return (
    <div
      className={`
        relative min-h-screen pt-16
        transition-colors duration-1000 ease-in-out
        ${bgClasses}
      `}
    >
      <Header />

      {!isCafePage && !isDocPage && <Sidebar />}

      <main>
        <Routes>
          <Route path="/" element={<MainContent />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/cafe" element={<CafePage />} />
          <Route path="/documentacion" element={<ProjectDocumentationViewer />} />
        </Routes>
      </main>

      <TransitionOverlay />
    </div>
  );
};

// --------------------------------------------------------
function App() {
  return (
    <Router>
      {/* Cursor personalizado SIEMPRE visible */}
      <div className="cursor-none">
        <CustomCursor />

        <TransitionProvider>
          <NutritionProvider>
            <CarouselProvider>
              <LayoutWrapper />
            </CarouselProvider>
          </NutritionProvider>
        </TransitionProvider>
      </div>
    </Router>
  );
}

export default App;
