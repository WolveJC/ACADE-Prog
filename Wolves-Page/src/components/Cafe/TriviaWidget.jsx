import React, { useEffect, useState } from 'react';

// Paleta de Colores: Pan Tostado/Dorado: #EEDCB3, Café Oscuro: #4B3621

// Antes: la API key de Spoonacular vivía aquí mismo, en texto plano,
// visible para cualquiera que abriera las DevTools. Ahora la key vive
// solo en el servidor (Wolves-Page-Backend); el navegador nunca la ve.
const BACKEND_URL = process.env.BACKEND_URL;

const TriviaWidget = () => {
    const [trivia, setTrivia] = useState('');
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchTrivia = async () => {
            setIsLoading(true);
            try {
                // Antes: fetch directo a Spoonacular con la key en la URL.
                // Ahora pasa por nuestro backend, que guarda la key y
                // aplica el límite de cuota.
                const response = await fetch(`${BACKEND_URL}/api/trivia`);

                if (response.status === 429) {
                    setTrivia('Ya usaste tu curiosidad del día. Vuelve más tarde.');
                    return;
                }
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

        fetchTrivia();
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