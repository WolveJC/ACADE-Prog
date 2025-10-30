import { useEffect } from 'react';

{/* Hook para establecer el título de la pestaña del navegador. */}
 @param {string} title {/* El título que se desea mostrar. */}
 
const usePageTitle = (title) => {
    useEffect(() => {
        // Guarda el título original (opcional, útil si necesitas restaurarlo)
        const previousTitle = document.title;
        
        // Establece el nuevo título de la página
        document.title = title;

        // Función de limpieza: Se ejecuta cuando el componente se desmonta 
        // o antes de que el efecto se vuelva a ejecutar.
        return () => {
            // NOTA: Podría restaurar el título si fuera necesario, 
            // pero en una aplicación de página única (SPA) con rutas, 
            // es mejor dejar que el próximo hook lo sobrescriba.
        };
    }, [title]); // El efecto se vuelve a ejecutar solo si el 'title' cambia.
};

export default usePageTitle;
