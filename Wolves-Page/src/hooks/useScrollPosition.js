import { useState, useEffect } from 'react';

const useScrollPosition = () => {
    // Estado para almacenar la posición vertical del scroll
    const [scrollY, setScrollY] = useState(0);

    useEffect(() => {
        const handleScroll = () => {
            // Lee la posición vertical actual
            setScrollY(window.scrollY);
        };

        // Escucha el evento 'scroll' en la ventana
        // { passive: true } mejora el rendimiento de la interacción
        window.addEventListener('scroll', handleScroll, { passive: true });

        // Función de limpieza: elimina el listener cuando el componente se desmonta
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
        
    }, []); // El array de dependencia vacío asegura que el listener se configure y limpie solo una vez

    // Devuelve la posición de scroll
    return scrollY;
};

export default useScrollPosition;