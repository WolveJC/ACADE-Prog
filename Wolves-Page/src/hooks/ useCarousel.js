import { useState, useEffect, useRef } from 'react';

// scrollSpeed: La cantidad de píxeles a desplazar en cada intervalo (mayor = más rápido).
// intervalTime: El tiempo en milisegundos entre cada desplazamiento (menor = más suave/frecuente).
const useCarousel = (scrollSpeed = 5, intervalTime = 40) => {
    const carouselRef = useRef(null);
    const [isPaused, setIsPaused] = useState(false);

    // 1. Efecto para FORZAR el inicio en la posición 0 (Welcome)
    useEffect(() => {
        const carousel = carouselRef.current;
        if (carousel) {
            // Asegurar que el carrusel empiece en Welcome
            carousel.scrollLeft = 0; 
        }
    }, []); // Se ejecuta solo una vez al montar el componente

    // 2. Efecto para manejar el desplazamiento automático y el bucle infinito
    useEffect(() => {
        const carousel = carouselRef.current;
        if (!carousel) return;

        let intervalId;

        const startScrolling = () => {
            clearInterval(intervalId); 
            intervalId = setInterval(() => {
                if (isPaused) return; 

                // Muever de IZQUIERDA a DERECHA 
                carousel.scrollLeft += scrollSpeed; 

                // Lógica de bucle:
                // Si el scrollLeft es mayor o igual al punto donde acaba la primera copia del contenido (que es el ancho del viewport * número de secciones únicas), reiniciamos el scroll a la posición 0.
                
                // NOTA: Para un loop perfecto hacia la derecha, el reinicio debe ocurrir cuando el final del primer conjunto de secciones pasa el viewport. Lo más simple y efectivo es reiniciar a 0 cuando llega al límite.
                if (carousel.scrollLeft >= carousel.scrollWidth - carousel.clientWidth) {
                    // Reinicia al principio (posición 0)
                    carousel.scrollLeft = 0; 
                }

            }, intervalTime);
        };

        startScrolling();
        // Función de limpieza para detener el intervalo al desmontar el componente
        return () => clearInterval(intervalId);
        
    }, [isPaused, scrollSpeed, intervalTime]);

    // Handlers para pausar el carrusel con el mouse
    const handleMouseEnter = () => setIsPaused(true);
    const handleMouseLeave = () => setIsPaused(false);

    return { carouselRef, handleMouseEnter, handleMouseLeave, isPaused };
};

export default useCarousel;