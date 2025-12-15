import React, { useCallback } from "react"; 
import { Link, useLocation } from "react-router-dom";
import { FaGithub, FaLinkedin, FaInstagram } from "react-icons/fa";
import { HiOutlineMail } from "react-icons/hi";
import Avatar from "../UI/Avatar";
import { useCarouselContext } from '../../context/GlobalCarousel';
import useScrollPosition from "../../hooks/useScrollPosition";
import { useTransitionContext } from '../../context/TransitionContext'; 

const Header = () => {
    const location = useLocation();
    const isCafePage = location.pathname === '/cafe';

    const { currentSlideIndex } = useCarouselContext(); 
    const scrollY = useScrollPosition();
    const { startTransition } = useTransitionContext(); 

    const socialLinks = [
        { Icon: FaLinkedin, href: "https://ve.linkedin.com/in/wolvejc-467456172", name: "LinkedIn" },
        { Icon: FaGithub, href: "https://github.com/WolveJC", name: "GitHub" },
        { Icon: FaInstagram, href: "https://www.instagram.com/wolvejc05?igsh=bTFqem5scnU1cGh4", name: "Instagram" },
    ];

    const COLOR_MAP = {
        0: 'bg-forest-start', 
        1: 'bg-forest-mid',   
        2: 'bg-forest-end',   
    };

    const opacityClass = scrollY > 50 
        ? "opacity-100" 
        : "opacity-90 backdrop-blur-xs"; 

    let finalBgClass, finalBorderClass;

    if (isCafePage) {
        finalBgClass = 'bg-cafe-oscuro'; 
        finalBorderClass = 'border-b border-pan-tostado'; 
    } else {
        finalBgClass = COLOR_MAP[currentSlideIndex] || 'bg-forest-start';
        finalBorderClass = 'border-b border-gray-700/50';
    }

    const buttonText = isCafePage ? 'Volver al Bosque' : 'Ir al Café ☕';
    const buttonTo = isCafePage ? '/' : '/cafe';

    const buttonBgClass = isCafePage 
        ? 'bg-bosque-verde hover:bg-green-700 text-white' 
        : 'bg-pan-tostado text-cafe-oscuro hover:bg-white'; 

    const iconClass = isCafePage 
        ? "w-6 h-6 text-pan-tostado hover:text-white transition duration-300" 
        : "w-6 h-6 text-green-300 hover:text-white transition duration-300"; 

    const handleInternalNavClick = useCallback((e, path) => {
        e.preventDefault();
        startTransition(path);
    }, [startTransition]);

    return (
        <header 
            className={`
                fixed top-0 w-full z-50 
                p-3 sm:p-4 
                shadow-xl
                ${finalBgClass} 
                ${isCafePage ? finalBorderClass : `border-transparent ${opacityClass}`}
                transition-all duration-1000 ease-in-out 
                ${isCafePage ? 'backdrop-blur-none' : 'backdrop-blur-xs'}
            `}
        >
            <nav className="flex items-center justify-between max-w-7xl mx-auto">
                
                {/* IZQUIERDA: Avatar + Nombre */}
                <div className="flex items-center space-x-3 sm:space-x-4">
                    <a 
                        href="/"
                        onClick={(e) => handleInternalNavClick(e, '/')}
                        aria-label="Volver a la página principal"
                        className="cursor-pointer leaf-trigger flex items-center"
                    >
                        <Avatar size="small" />
                    </a>

                    <span className="text-lg sm:text-xl font-bold text-white hidden sm:block">
                        WolveJC
                    </span>
                </div>

                {/* DERECHA: Botón + Redes + Correo */}
                <div className="flex items-center space-x-4 sm:space-x-6">

                    <a 
                        href={buttonTo} 
                        onClick={(e) => handleInternalNavClick(e, buttonTo)}
                        className={`
                            px-3 sm:px-4 
                            py-1.5 sm:py-2 
                            rounded-full 
                            font-semibold 
                            text-xs sm:text-sm md:text-base
                            shadow-md 
                            transition-all duration-300 ease-in-out 
                            ${buttonBgClass} cursor-pointer
                            leaf-trigger
                        `}
                    >
                        {buttonText}
                    </a>

                    <div className="hidden md:flex space-x-4">
                        {socialLinks.map(({ Icon, href, name }) => (
                            <a
                                key={name}
                                href={href}
                                target="_blank"
                                rel="noopener noreferrer"
                                aria-label={`Enlace a mi perfil de ${name}`}
                                className={`${iconClass} leaf-trigger`} 
                            >
                                <Icon className="w-6 h-6" />
                            </a>
                        ))}
                    </div>

                    <a
                        href="/contact"
                        onClick={(e) => handleInternalNavClick(e, '/contact')}
                        aria-label="Ir a la página de contacto"
                        className={`cursor-pointer ${iconClass} leaf-trigger`}
                    >
                        <HiOutlineMail className="w-7 h-7" />
                    </a>
                </div>
            </nav>
        </header>
    );
};

export default Header;
