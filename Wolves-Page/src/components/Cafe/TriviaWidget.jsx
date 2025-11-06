import React, { useEffect, useState } from 'react';

// Paleta de Colores: Pan Tostado/Dorado: #EEDCB3, Café Oscuro: #4B3621

//  ATENCIÓN: REEMPLAZAR ESTE VALOR con la API key de Spoonacular
const SPOONACULAR_API_KEY = '4e2e88d3f42a4fd4b626ae8dc0eb1e49'; 

const TriviaWidget = () => {
    const [trivia, setTrivia] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchTrivia = async () => {
            setIsLoading(true);
            try {
                // API Spoonacular: Obtener una trivia aleatoria de comida
                const response = await fetch(`https://api.spoonacular.com/food/trivia/random?apiKey=${SPOONACULAR_API_KEY}`);
                
                if (!response.ok) {
                    throw new Error('Error al cargar la trivia.');
                }

                const data = await response.json();
                setTrivia(data.text);
            } catch (err) {
                console.error("Error fetching trivia:", err);
                setTrivia('Curiosidad del día no disponible. Inténtalo de nuevo más tarde.');
            } finally {
                setIsLoading(false);
            }
        };

        if (SPOONACULAR_API_KEY !== 'YOUR_SPOONACULAR_API_KEY') {
            fetchTrivia();
        } else {
            setTrivia('Por favor, ingresa tu clave de Spoonacular API para activar la trivia.');
            setIsLoading(false);
        }
    }, []);

    return (
        <div 
            className="
                mt-6 p-4 rounded-lg 
                bg-white/80 border-l-4 border-[#EEDCB3] // Borde Dorado
                text-[#4B3621] shadow-inner // Texto Café Oscuro
            "
        >
            <h5 className="text-sm font-bold mb-2 uppercase tracking-wider">
                Curiosidad del Día
            </h5>
            {isLoading 
                ? <p className="text-xs italic animate-pulse">Buscando un dato interesante...</p>
                : <p className="text-sm">{trivia}</p>
            }
        </div>
    );
};

export default TriviaWidget;