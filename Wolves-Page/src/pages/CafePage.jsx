import React from 'react';
import usePageTitle from '../hooks/usePageTitle';
import RecipeCard from '../components/Cafe/RecipeCard'; 
import TriviaWidget from '../components/Cafe/TriviaWidget';
import CafeSidebar from '../components/Cafe/CafeSidebar'; // ⬅️ IMPORTAR LA SIDEBAR DE NUTRIENTES

const CafePage = () => {
    // 1. Hook para cambiar el título de la página
    usePageTitle("WolveJC | El Café de las APIs");

    return (
        <div 
            className="
                min-h-screen pt-20 pb-10 
                bg-leche-crema text-cafe-oscuro // Fondo Crema, Texto Café Oscuro
                transition-colors duration-500
            "
        >
            {/* Contenedor principal que abarca toda la página, justo debajo del Header */}
            <div className="max-w-7xl mx-auto px-4 md:px-6"> 

                {/* Título y Párrafo (Mantener centrados sobre las columnas) */}
                <h2 className="text-4xl md:text-5xl font-serif font-bold text-center mb-4 text-cafe-oscuro">
                     El Café de las APIs
                </h2>
                <p className="text-lg text-gray-500 text-center mb-8 max-w-3xl mx-auto italic">
                    Una pausa para explorar la sinergia de los datos. Hoy te servimos una receta al azar.
                </p>

                {/* ⬅️ CONTENEDOR FLEX PRINCIPAL: Crea el layout de 2 o 3 columnas */}
                <div className="flex flex-col lg:flex-row lg:items-start lg:space-x-8">

                    {/* 1. COLUMNA IZQUIERDA: Sidebar de Nutrientes */}
                    <aside className="w-full lg:w-40 flex-shrink-0 mb-6 lg:mb-0">
                        {/* ⬅️ La CafeSidebar debe estar aquí */}
                        <CafeSidebar /> 
                    </aside>

                    {/* 2. COLUMNA DERECHA: Contenido Principal (Receta + Trivia) */}
                    <main className="flex-grow">
                        
                        {/* Contenedor de la Receta (Aseguramos que no se salga del flex-grow) */}
                        <div className="flex flex-col items-center">

                            {/* a. Tarjeta de Receta */}
                            <RecipeCard />

                            {/* b. Trivia Widget */}
                            <div className="w-full max-w-4xl mt-6"> 
                                <TriviaWidget />
                            </div>

                        </div>
                    </main>

                </div>
                
            </div>
        </div>
    );
};

export default CafePage;