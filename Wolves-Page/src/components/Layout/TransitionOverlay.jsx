import React, { useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useTransitionContext } from '../../context/TransitionContext';
import { motion, AnimatePresence } from 'framer-motion';

// Momento en que la navegación ocurre (cuando la pantalla está cubierta)
const NAVIGATION_DELAY_MS = 600; 

const TransitionOverlay = () => {
    const { isTransitioning, destinationPath, endTransition } = useTransitionContext();
    const navigate = useNavigate();
    const location = useLocation(); // Ruta actual (Página de origen)
    const timerRef = useRef(null);

    // ----------------------------------------------------
    // 1. Lógica de Navegación y Control (Sin Cambios)
    // ----------------------------------------------------
    useEffect(() => {
        if (isTransitioning) {
            // Navegar cuando la pantalla esté cubierta (600ms)
            timerRef.current = setTimeout(() => {
                navigate(destinationPath);
            }, NAVIGATION_DELAY_MS); 

            // Terminar la transición para iniciar la animación de revelado (1400ms)
            // La duración total de la animación más larga es 1400ms (0.8s exit + 0.6s delay, o 0.7s exit + 0.7s delay)
            const totalAnimationDuration = 1400; 
            const revealTimer = setTimeout(() => {
                endTransition();
            }, totalAnimationDuration); 

            return () => {
                clearTimeout(timerRef.current);
                clearTimeout(revealTimer);
            };
        }
    }, [isTransitioning, destinationPath, navigate, endTransition]);


    // ----------------------------------------------------
    // 2. Variantes de Framer Motion (Sin Cambios)
    // ----------------------------------------------------

    // Variantes para la transición BOSQUE/CONTACTO -> CAFÉ (Lluvia de Granos / Disipación de Vapor)
    const cafeVariants = {
        initial: { y: '-100%', opacity: 0 }, 
        animate: { 
            y: '0%', 
            opacity: 1, 
            transition: { duration: 0.6, ease: 'easeOut' }
        },
        exit: { 
            y: '-100%', 
            opacity: 0, 
            transition: { duration: 0.8, ease: 'easeIn', delay: 0.6 }
        },
    };

    // Variantes para la transición CAFÉ -> BOSQUE/CONTACTO (Llenado/Vacío de Árboles)
    const bosqueVariants = {
        initial: { scaleX: 0, opacity: 0 },
        animate: { 
            scaleX: 1, 
            opacity: 1, 
            transition: { duration: 0.7, ease: 'easeIn' }
        },
        exit: { 
            scaleX: 0, 
            opacity: 0, 
            transition: { duration: 0.7, ease: 'easeOut', delay: 0.7 }
        },
    };

    // ----------------------------------------------------
    // 3. Lógica de Decisión de Animación (MODIFICADA)
    // ----------------------------------------------------
    
    // 1. Identificar la dirección de la transición
    const isGoingToCafe = destinationPath === '/cafe';
    const isComingFromCafe = location.pathname === '/cafe';

    let variantsToUse = {};
    let overlayBgColor = '';
    let overlayText = '';

    // A. TRANSICIÓN HACIA EL CAFÉ (Bosque/Contacto -> Café)
    if (isGoingToCafe) {
        variantsToUse = cafeVariants;
        overlayBgColor = 'bg-cafe-oscuro';
        overlayText = ' Preparando...';
    } 
    // B. TRANSICIÓN DESDE EL CAFÉ (Café -> Bosque/Contacto)
    else if (isComingFromCafe) {
        variantsToUse = bosqueVariants;
        overlayBgColor = 'bg-forest-start';
        overlayText = ' Volviendo al Bosque...';
    }
    // C. TRANSICIÓN DENTRO DEL BOSQUE (Bosque <-> Contacto)
    else {
        // Usa la animación de Bosque por defecto para las transiciones internas
        variantsToUse = bosqueVariants;
        overlayBgColor = 'bg-forest-start';
        // Determinar el texto de la ruta del Bosque
        overlayText = destinationPath === '/contact' ? ' Contactando...' : ' Explorando...';
    }


    // El overlay solo se muestra si está en proceso de transición
    const showOverlay = isTransitioning; 

    return (
        <AnimatePresence>
            {showOverlay && (
                <motion.div 
                    key="transition-overlay"
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
                    style={{ pointerEvents: 'auto' }} // Permitimos el puntero para asegurar el focus del overlay
                >
                    {/* Contenido dentro del overlay (Texto de Feedback) */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        transition={{ delay: 0.3, duration: 0.3 }}
                        className="text-white text-lg font-bold"
                    >
                        {overlayText}
                    </motion.div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default TransitionOverlay;