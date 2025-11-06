import React, { useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTransitionContext } from '../../context/TransitionContext';
import { motion, AnimatePresence } from 'framer-motion'; // Importamos Framer Motion

// Duración total de la animación (debe coincidir con la duración de la animación Framer Motion)
// Ajustaremos esto en las variantes de Framer Motion.
const NAVIGATION_DELAY_MS = 600; // Momento en que la navegación ocurre (cuando la pantalla está cubierta)

const TransitionOverlay = () => {
    const { isTransitioning, destinationPath, endTransition } = useTransitionContext();
    const navigate = useNavigate();
    const location = useLocation(); // Ruta actual
    const timerRef = useRef(null);

    // Determinamos el origen y el destino para elegir la animación
    const isToCafe = destinationPath === '/cafe';
    const isToBosque = destinationPath === '/';

    // --- 1. Lógica de Navegación y Control ---
    useEffect(() => {
        if (isTransitioning) {
            // Navegar cuando la pantalla esté cubierta
            timerRef.current = setTimeout(() => {
                navigate(destinationPath);
            }, NAVIGATION_DELAY_MS); 

            // Terminar la transición para iniciar la animación de revelado
            // Suma las duraciones de las variantes de Framer Motion
            const totalAnimationDuration = 1400; // Ajusta esto al valor más largo de tus animaciones
            const revealTimer = setTimeout(() => {
                endTransition();
            }, totalAnimationDuration); 

            return () => {
                clearTimeout(timerRef.current);
                clearTimeout(revealTimer);
            };
        }
    }, [isTransitioning, destinationPath, navigate, endTransition]);


    // --- 2. Variantes de Framer Motion para las Animaciones Temáticas ---

    // Variantes para la transición BOSQUE -> CAFÉ (Lluvia de Granos / Disipación de Vapor)
    const cafeVariants = {
        // Estado inicial (antes de que el overlay entre)
        initial: { y: '-100%', opacity: 0 }, 
        // Estado cuando el overlay está cubriendo la pantalla (animación de salida)
        animate: { 
            y: '0%', 
            opacity: 1, 
            transition: { duration: 0.6, ease: 'easeOut' } // Lluvia de granos
        },
        // Estado de salida (cuando el overlay se disipa para revelar la nueva página)
        exit: { 
            y: '-100%', // Se mueve hacia arriba como vapor
            opacity: 0, 
            transition: { duration: 0.8, ease: 'easeIn', delay: 0.6 } // Disipación de vapor
        },
    };

    // Variantes para la transición CAFÉ -> BOSQUE (Llenado/Vacío de Árboles)
    const bosqueVariants = {
        initial: { scaleX: 0, opacity: 0 },
        animate: { 
            scaleX: 1, 
            opacity: 1, 
            transition: { duration: 0.7, ease: 'easeIn' } // Árboles llenan
        },
        exit: { 
            scaleX: 0, 
            opacity: 0, 
            transition: { duration: 0.7, ease: 'easeOut', delay: 0.7 } // Árboles se vacían
        },
    };

    // Determinamos qué variantes usar y el color de fondo
    let variantsToUse = {};
    let overlayBgColor = '';

    if (isToCafe) {
        variantsToUse = cafeVariants;
        overlayBgColor = 'bg-cafe-oscuro'; // Color para la transición al Café
    } else if (isToBosque) {
        variantsToUse = bosqueVariants;
        overlayBgColor = 'bg-forest-start'; // Color para la transición al Bosque
    }

    // El componente se renderiza solo cuando isTransitioning es true o cuando la página actual es la de destino
    const showOverlay = isTransitioning || (location.pathname === destinationPath && destinationPath !== '/');


    return (
        <AnimatePresence>
            {showOverlay && (
                <motion.div 
                    key="transition-overlay" // Una key única es crucial para AnimatePresence
                    className={`
                        fixed top-0 left-0 w-full h-full z-[9999] 
                        flex items-center justify-center transform origin-center
                        ${overlayBgColor}
                    `}
                    initial="initial"
                    animate="animate"
                    exit="exit"
                    variants={variantsToUse}
                    // Deshabilitar eventos de puntero durante la animación
                    style={{ pointerEvents: isTransitioning ? 'auto' : 'none' }}
                >
                    {/* Contenido opcional dentro del overlay */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ delay: 0.3, duration: 0.3 }}
                        className="text-white text-lg font-bold"
                    >
                        {isToCafe ? ' Preparando...' : isToBosque ? ' Explorando...' : ''}
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default TransitionOverlay;