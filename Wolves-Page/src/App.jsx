import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";

// Componentes de Layout
import Header from "./components/Layout/Header.jsx";
import Sidebar from "./components/Layout/Sidebar.jsx"; // Sidebar del Bosque (Skills)
import MainContent from "./components/Layout/MainContent.jsx";
import ContactPage from "./pages/ContactPage.jsx";
import CafePage from "./pages/CafePage.jsx"; // Nuevo: Página del Café
import TransitionOverlay from './components/Layout/TransitionOverlay'; // Nuevo: Overlay de Transición

// Componentes y Contextos de Interacción
import CustomCursor from "./components/Cursor/CustomCursor.js";
import { CarouselProvider } from "./context/GlobalCarousel.jsx";
import { TransitionProvider } from "./context/TransitionContext"; // Nuevo: Provider de Transición
import { NutritionProvider } from "./context/NutritionContext"; // Nuevo: Provider de Nutrición

// --------------------------------------------------------
// COMPONENTE WRAPPER: Gestiona la lógica de layout condicional
// --------------------------------------------------------
const LayoutWrapper = () => {
    const location = useLocation();
    const isCafePage = location.pathname === '/cafe';

    // 1. Lógica de Fondo Temático
    // El fondo debe ser dinámico: degradado en Bosque, color fijo en Café
    const bgClasses = isCafePage 
        ? 'bg-leche-crema text-cafe-oscuro' // Color fijo y texto oscuro para Café
        : 'bg-gradient-to-b from-forest-start via-forest-mid to-forest-end text-white'; // Degradado y texto blanco para Bosque

    return (
        <div 
            className={`
                relative min-h-screen pt-16
                transition-colors duration-1000 ease-in-out // Permite la transición del fondo
                ${bgClasses}
            `}
        >
            {/* El pt-16 empuja el contenido debajo del Header fijo */}
            <Header />
            
            {/* Sidebar Condicional: Solo se muestra si NO estamos en la página del Café */}
            {!isCafePage && <Sidebar />}

            {/* Contenido Dinámico: Aquí se gestionan las rutas */}
            <main>
                <Routes>
                    <Route path="/" element={<MainContent />} />
                    <Route path="/contact" element={<ContactPage />} />
                    {/* Ruta del Café: Usará su propia sidebar internamente */}
                    <Route path="/cafe" element={<CafePage />} /> 
                </Routes>
            </main>
            
            {/*  El Overlay siempre se renderiza para manejar las animaciones */}
            <TransitionOverlay />
        </div>
    );
};

// --------------------------------------------------------
// COMPONENTE PRINCIPAL APP
// --------------------------------------------------------
function App() {
    return (
        <Router>
            {/* 1. Componentes Fijos */}
            <CustomCursor />

            {/* 2. Providers Globales (en el orden adecuado) */}
            <TransitionProvider>
                <NutritionProvider> {/* Nutrición debe estar dentro de Transition si es usada por un componente que activa la transición */}
                    <CarouselProvider>
                        
                        {/* 3. Renderizar el Layout (Routes, Sidebar, etc.) */}
                        <LayoutWrapper />
                        
                    </CarouselProvider>
                </NutritionProvider>
            </TransitionProvider>
        </Router>
    );
}

export default App;