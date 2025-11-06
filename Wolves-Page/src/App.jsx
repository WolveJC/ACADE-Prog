import React from "react";
import { Link, useLocation } from "react-router-dom";
// ⬅️ Importación Crítica
import { useTransitionContext } from '../../context/TransitionContext'; 
// Íconos
import { FaGithub, FaLinkedin, FaInstagram } from "react-icons/fa";
import { HiOutlineMail } from "react-icons/hi";
import Avatar from "../UI/Avatar";
// Importaciones de Interactividad
import { useCarouselContext } from '../../context/GlobalCarousel';
import useScrollPosition from "../../hooks/useScrollPosition"; 

const Header = () => {
    const location = useLocation();
    const isCafePage = location.pathname === '/cafe';

    // ⬅️ Obtener la función de transición
    const { startTransition } = useTransitionContext(); 
    
    // Obtener estados globales
    const { currentSlideIndex } = useCarouselContext(); 
    const scrollY = useScrollPosition();

    // Datos de Configuración (Contactos)
    const socialLinks = [
        {
            Icon: FaLinkedin,
            href: "https://ve.linkedin.com/in/wolvejc-467456172",
            name: "LinkedIn",
        },
        { Icon: FaGithub, href: "https://github.com/WolveJC", name: "GitHub" },
        {
            Icon: FaInstagram,
            href: "https://www.instagram.com/wolvejc05?igsh=bTFqem5scnU1cGh4",
            name: "Instagram",
        },
    ];

    // 1. Definición de Clases de Color Sincronizadas del BOSQUE
    const COLOR_MAP = {
        0: 'bg-forest-start', 
        1: 'bg-forest-mid',   
        2: 'bg-forest-end',   
    };

    // 2. Control de Solidez al Scroll Vertical (Solo aplica en el Bosque)
    const opacityClass = 
        scrollY > 50 
        ? "opacity-100" // Fondo Sólido
        : "opacity-90 backdrop-blur-sm"; // Fondo Semitransparente con Blur

    // 3. LÓGICA DE FONDO FINAL UNIFICADA
    let finalBgClass, finalBorderClass;

    if (isCafePage) {
        // Estilos FIJOS para la página del Café
        finalBgClass = 'bg-cafe-oscuro';
        finalBorderClass = 'border-b border-pan-tostado';
    } else {
        // Estilos DINÁMICOS para la página del Bosque
        finalBgClass = COLOR_MAP[currentSlideIndex] || 'bg-forest-start';
        finalBorderClass = 'border-b border-gray-700/50';
    }

    // 4. LÓGICA DEL BOTÓN DE TRANSICIÓN
    const buttonText = isCafePage ? 'Volver al Bosque' : 'Ir al Café ☕';
    const buttonTo = isCafePage ? '/' : '/cafe';

    const buttonBgClass = isCafePage 
        ? 'bg-bosque-verde hover:bg-green-700 text-white' 
        : 'bg-pan-tostado text-cafe-oscuro hover:bg-white'; 

    // Estilo de Íconos (Unificado)
    const iconClass = isCafePage 
        ? "w-6 h-6 text-pan-tostado hover:text-white transition duration-300"
        : "w-6 h-6 text-green-300 hover:text-white transition duration-300"; 

    // 5. MANEJADOR DE CLIC DE TRANSICIÓN (CRÍTICO)
    const handleTransitionClick = (e, path) => {
        e.preventDefault(); // Detenemos la acción por defecto del <Link>
        if (location.pathname !== path) {
            // ⬅️ Llamamos al contexto para iniciar la animación y luego la navegación
            startTransition(path); 
        }
    };


    return (
        <header 
            className={`
                fixed top-0 w-full z-50 p-4 shadow-xl
                ${finalBgClass} 
                ${isCafePage ? finalBorderClass : `border-transparent ${opacityClass}`}
                transition-all duration-1000 ease-in-out
                ${isCafePage ? 'backdrop-blur-none' : 'backdrop-blur-sm'}
            `}
        >
            <nav className="flex items-center justify-between max-w-7xl mx-auto">
                {/* 1. SECCIÓN IZQUIERDA: Avatar y Nombre */}
                <div className="flex items-center space-x-4">
                    {/* El link al inicio SÍ usa navegación normal, ya que no tiene animación de salida temática */}
                    <Link to="/" aria-label="Volver a la página principal">
                        <Avatar size="small" />
                    </Link>
                    <span className="text-xl font-bold text-white hidden sm:block">
                        WolveJC
                    </span>
                </div>

                {/* 2. SECCIÓN DERECHA: Botón de Transición + Íconos Sociales */}
                <div className="flex items-center space-x-6">

                    {/* Botón de Transición de Ambiente (USO DE startTransition) */}
                    <Link 
                        to={buttonTo} 
                        onClick={(e) => handleTransitionClick(e, buttonTo)} // ⬅️ Nuevo manejador
                        className={`
                            px-4 py-2 rounded-full font-semibold text-sm 
                            shadow-md transition-all duration-300 ease-in-out 
                            ${buttonBgClass}
                        `}
                    >
                        {buttonText}
                    </Link>

                    {/* Íconos de Redes Sociales */}
                    <div className="hidden md:flex space-x-4">
                        {socialLinks.map(({ Icon, href, name }) => (
                            <a
                                key={name}
                                href={href}
                                target="_blank"
                                rel="noopener noreferrer"
                                aria-label={`Enlace a mi perfil de ${name}`}
                                className={iconClass} 
                            >
                                <Icon className="w-6 h-6" />
                            </a>
                        ))}
                    </div>

                    {/* Ícono de Correo Electrónico (Ruta Interna) */}
                    <Link
                        to="/contact"
                        aria-label="Ir a la página de contacto"
                        className={iconClass}
                    >
                        <HiOutlineMail className="w-7 h-7" />
                    </Link>
                </div>
            </nav>
        </header>
    );
};

export default Header;