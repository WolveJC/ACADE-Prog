import { useState, useEffect, useRef } from 'react';

const useCarousel = (scrollSpeed = 1, intervalTime = 50) => {
    // Referencia al elemento DOM que quiero desplazar
    const carouselRef = useRef(null);
    // Estado para saber si el desplazamiento debe pausarse
    const [isPaused, setIsPaused] = useState(false);

    useEffect(() => {
        const carousel = carouselRef.current;
        if (!carousel) return;

        let intervalId;

        const startScrolling = () => {
            // Limpiar cualquier intervalo anterior para evitar duplicados
            clearInterval(intervalId); 

            intervalId = setInterval(() => {
                if (isPaused) {
                    return; // No hacer nada si está pausado
                }

                // Lógica de desplazamiento de derecha a izquierda
                // Disminuye scrollLeft (va hacia la izquierda)
                carousel.scrollLeft -= scrollSpeed; 

                // Si el desplazamiento llega al inicio, reinicia al final
                if (carousel.scrollLeft <= 0) {
                    // Reinicia el desplazamiento a la posición del final del contenido
                    // Para simular un bucle infinito
                    carousel.scrollLeft = carousel.scrollWidth - carousel.clientWidth;
                }
            }, intervalTime);
        };

        startScrolling();

        // Función de limpieza: se ejecuta cuando el componente se desmonta
        return () => clearInterval(intervalId);
        
    }, [isPaused, scrollSpeed, intervalTime]); // Se reactiva si isPaused o velocidades cambian

    // Funciones que se exponen para el manejo del mouse
    const handleMouseEnter = () => setIsPaused(true);
    const handleMouseLeave = () => setIsPaused(false);

    return { carouselRef, handleMouseEnter, handleMouseLeave, isPaused };
};

export default useCarousel;