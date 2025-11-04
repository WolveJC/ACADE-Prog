import { useState, useEffect, useRef } from 'react';
import useScrollPosition from './useScrollPosition'; 

// CONSTANTES BASE
const BASE_SPEED = 3; 
const ACCEL_SPEED = 15; // Velocidad base de aceleración con flechas

const useCarousel = (baseScrollSpeed = BASE_SPEED, intervalTime = 40) => {
    const carouselRef = useRef(null);
    
    // Estados de Interacción (Pausa/Aceleración)
    const [isPaused, setIsPaused] = useState(false);
    const [arrowDirection, setArrowDirection] = useState(0); // 1: Adelante, -1: Atrás, 0: Normal
    
    // Control de Velocidad por Scroll Vertical
    const scrollY = useScrollPosition(); 
    const [wheelSpeedMultiplier, setWheelSpeedMultiplier] = useState(1);
    
    // Sincronización con el Header (Índice de 0 a 2)
    const [currentSlideIndex, setCurrentSlideIndex] = useState(0);

    // --- 1. Inicialización y Posición de Scroll Vertical (Modulador de Velocidad) ---
    useEffect(() => {
        const carousel = carouselRef.current;
        if (carousel) {
            // Asegurar el inicio en la posición 0
            carousel.scrollLeft = 0; 
        }

        // Modulación de velocidad: Aumentar la velocidad base al hacer scroll vertical
        const sensitivityFactor = 0.05; 
        const newMultiplier = 1 + (scrollY * sensitivityFactor); 
        // Limitamos el multiplicador máximo para evitar saltos caóticos
        const clampedMultiplier = Math.min(newMultiplier, 5); 
        
        setWheelSpeedMultiplier(clampedMultiplier);

    }, [scrollY]); // Depende del scroll vertical de la ventana


    // --- 2. CÁLCULO DE LA VELOCIDAD EFECTIVA ---
    
    // 2a. Velocidad de Flechas: es ACCEL_SPEED si la flecha está activa, sino 0
    const arrowSpeed = arrowDirection * ACCEL_SPEED; 
    
    // 2b. Velocidad Base/Acelerada: Usamos la velocidad de flecha si es diferente de 0, sino la velocidad base.
    let effectiveSpeed = (arrowDirection !== 0) ? arrowSpeed : baseScrollSpeed;

    // 2c. Aplicar Multiplicador de Rueda de Ratón: Acelera la velocidad actual
    effectiveSpeed = effectiveSpeed * Math.max(1, wheelSpeedMultiplier);


    // --- 3. Desplazamiento Automático e Infinito (Interval) ---
    useEffect(() => {
        const carousel = carouselRef.current;
        if (!carousel) return;

        let intervalId;

        const startScrolling = () => {
            clearInterval(intervalId); 
            intervalId = setInterval(() => {
                if (isPaused) return; 

                // Aplicamos el desplazamiento
                carousel.scrollLeft += effectiveSpeed; 

                // Lógica de bucle para desplazamiento hacia ADELANTE (effectiveSpeed > 0)
                if (effectiveSpeed > 0) {
                    // Cuando el carrusel pasa el punto medio (donde comienza la copia), reinicia
                    if (carousel.scrollLeft >= carousel.scrollWidth / 2) { 
                        carousel.scrollLeft = 0; 
                    }
                } 
                // Lógica de bucle para desplazamiento hacia ATRÁS (effectiveSpeed < 0)
                else if (effectiveSpeed < 0) {
                    // Si el scrollLeft llega a 0 (el principio de la primera copia)
                     if (carousel.scrollLeft <= 0) {
                        // Reinicia al inicio de la segunda copia (scrollWidth / 2)
                        carousel.scrollLeft = carousel.scrollWidth / 2; 
                     }
                }

            }, intervalTime);
        };

        startScrolling();
        
        return () => clearInterval(intervalId);
        
    }, [isPaused, effectiveSpeed, intervalTime]);


    // --- 4. CÁLCULO DEL ÍNDICE DE DIAPOSITIVA (Para el Header) ---
    useEffect(() => {
        const carousel = carouselRef.current;
        if (!carousel) return;

        const handleScroll = () => {
            // El ancho de una diapositiva es el ancho del viewport (window.innerWidth)
            const slideWidth = window.innerWidth;
            const scrollLeft = carousel.scrollLeft;
            
            // Para asegurar que el índice cambie justo al centro de la diapositiva, 
            // se añade la mitad del ancho de la diapositiva al cálculo
            // Luego el % 3 (total de secciones únicas: Welcome, Projects, AboutMe)
            const index = Math.floor((scrollLeft + (slideWidth / 2)) / slideWidth) % 3; 
            
            if (index !== currentSlideIndex) {
                setCurrentSlideIndex(index);
            }
        };

        carousel.addEventListener('scroll', handleScroll, { passive: true });
        
        return () => {
            carousel.removeEventListener('scroll', handleScroll);
        };
    }, [currentSlideIndex]); 


    // --- 5. HANDLERS PARA EL CONSUMIDOR ---
    const togglePause = () => {
    // Invierte el estado actual de isPaused
    setIsPaused(prev => !prev);
  };
    
    // Funciones para las flechas de aceleración
    const startAcceleration = (direction) => setArrowDirection(direction); // 1 o -1
    const stopAcceleration = () => setArrowDirection(0);
    
    // La velocidad de feedback para el usuario debe ser un valor absoluto y legible
    const feedbackSpeed = Math.abs(effectiveSpeed);


    return { 
        carouselRef,
        togglepause,
        startAcceleration,
        stopAcceleration,
        isPaused,
        currentSpeed: feedbackSpeed,
        currentSlideIndex // CRUCIAL para la sincronización
    };
};

export default useCarousel;
