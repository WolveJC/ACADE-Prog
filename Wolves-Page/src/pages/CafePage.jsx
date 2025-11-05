import React from 'react';
import usePageTitle from '../hooks/usePageTitle';
import RecipeCard from '../components/Cafe/RecipeCard'; 
import TriviaWidget from '../components/Cafe/TriviaWidget'; 

const CafePage = () => {
    // 1. Hook para cambiar el título de la página
    usePageTitle("WolveJC | El Café de las APIs");

    return (
        <div 
            className="
                min-h-screen pt-20 pb-10 
                bg-leche-crema text-cafe-oscuro //  Fondo Crema, Texto Café Oscuro
                transition-colors duration-500
            "
        >
            {/* Contenedor principal para el contenido, dejando espacio para la Sidebar a la izquierda */}
            <div className="max-w-7xl mx-auto pl-16 md:pl-20 pr-4 md:pr-6">
                
                {/* Título de Bienvenida */}
                <h2 className="text-4xl md:text-5xl font-serif font-bold text-center mb-10 text-cafe-oscuro">
                     El Café de las APIs
                </h2>
                <p className="text-lg text-gray-500 text-center mb-12 max-w-3xl mx-auto italic">
                    Una pausa para explorar la sinergia de los datos. Hoy te servimos una receta al azar.
                </p>

                {/* Contenedor Flex para la Tarjeta de Receta y la Trivia */}
                <div className="flex flex-col items-center">
                    
                    {/* 1. Tarjeta de Receta (TheMealDB) */}
                    <RecipeCard />

                    {/* 2. Trivia Widget (Spoonacular) - Posicionada debajo de la tarjeta */}
                    <div className="w-full max-w-4xl mt-6"> 
                        <TriviaWidget />
                    </div>
                    
                </div>
                
            </div>
        </div>
    );
};

export default CafePage;