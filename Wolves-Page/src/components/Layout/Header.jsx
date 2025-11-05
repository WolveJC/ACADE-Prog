import React from "react";
import { Link, useLocation } from "react-router-dom";
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

    // 1. Definición de estilos condicionales
    // Estilos del Header: Cambia el color de fondo según la ruta
    const headerBgClass = isCafePage 
        ? 'bg-[#4B3621] border-b border-[#EEDCB3]' // Café Oscuro y Dorado para el Café
        : 'bg-black/60 backdrop-blur-md border-b border-gray-700/50'; // Bosque (Transparente)

    // Estilos del Botón: Cambia color y destino
    const buttonText = isCafePage ? 'Volver al Bosque' : 'Ir al Café ';
    const buttonTo = isCafePage ? '/' : '/cafe';
    
    // Color del botón: Dorado para el Bosque -> Café; Verde para el Café -> Bosque
    const buttonBgClass = isCafePage 
        ? 'bg-green-600 hover:bg-green-700' // Café -> Bosque
        : 'bg-[#EEDCB3] text-[#4B3621] hover:bg-white'; // Bosque -> Café (Dorado)
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

  // 1. Definición de Clases de Color Sincronizadas
  const COLOR_MAP = {
    // 0: Welcome
    0: 'bg-forest-start', 
    // 1: Projects
    1: 'bg-forest-mid',   
    // 2: AboutMe
    2: 'bg-forest-end',   
  };

  // 2. Determinar el color base según la sección del carrusel
  const baseColorClass = COLOR_MAP[currentSlideIndex] || 'bg-forest-start';

  // 3. Control de Solidez al Scroll Vertical
  const opacityClass = 
    scrollY > 50 
    ? "opacity-100" // Fondo Sólido
    : "opacity-90 backdrop-blur-sm"; // Fondo Semitransparente con Blur

  // Estilo de Íconos (Unificado)
  const iconClass = "w-6 h-6 text-green-300 hover:text-white transition duration-300";


  return (
    // Aplicamos el color base, la opacidad/blur, y la transición
    <header 
      className={`
        fixed top-0 w-full z-50 p-4 shadow-xl
        ${baseColorClass} 
        ${opacityClass}
        transition-all duration-1000 ease-in-out // Transición de 1s para el cambio de color
      `}
    >
      <nav className="flex items-center justify-between max-w-7xl mx-auto">
        {/* 1. SECCIÓN IZQUIERDA: Avatar y Nombre */}
        <div className="flex items-center space-x-4">
          <Link to="/" aria-label="Volver a la página principal">
            {/* Asumiendo que Avatar recibe 'small' para el tamaño */}
            <Avatar size="small" />
          </Link>
          <span className="text-xl font-bold text-white hidden sm:block">
            WolveJC
          </span>
        </div>
{/* Contenedor de Navegación del Ambiente (Nuevo Botón) */}
                <div className="flex items-center space-x-6">
                    
                    {/* Botón de Transición */}
                    <Link 
                        to={buttonTo} 
                        className={`
                            px-4 py-2 rounded-full font-semibold text-sm 
                            shadow-md transition-all duration-300 ease-in-out 
                            ${buttonBgClass}
                        `}
                    >
                        {buttonText}
                    </Link>

        {/* 2. SECCIÓN DERECHA: Íconos Sociales y Correo */}
        <div className="flex items-center space-x-6">
          {/* Íconos de Redes Sociales */}
          <div className="flex space-x-4">
            {socialLinks.map(({ Icon, href, name }) => (
              <a
                key={name}
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`Enlace a mi perfil de ${name}`}
                //Usar la clase de estilo unificada
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
            className={iconClass} // Usar la clase de estilo unificada
          >
            <HiOutlineMail className="w-7 h-7" />
          </Link>
        </div>
      </nav>
    </header>
  );
};

export default Header;