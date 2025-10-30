import React from "react";
import { Link } from "react-router-dom";
// Íconos
import { FaGithub, FaLinkedin, FaInstagram } from "react-icons/fa";
import { HiOutlineMail } from "react-icons/hi";
import Avatar from "../UI/Avatar";

const Header = () => {
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

  return (
    // Header fijo con estilo oscuro y sutilmente borroso
    <header className="fixed top-0 w-full z-50 p-4 shadow-lg bg-forest-start/90 backdrop-blur-sm">
      <nav className="flex items-center justify-between max-w-7xl mx-auto">
        {/* 1. SECCIÓN IZQUIERDA: Avatar y Nombre */}
        <div className="flex items-center space-x-4">
          {/* Usamos Link para navegar a la página principal si se hace clic en el avatar */}
          <Link to="/" aria-label="Volver a la página principal">
            <Avatar size="small" />
          </Link>
          <span className="text-xl font-bold text-white hidden sm:block">
            WolveJC
          </span>
        </div>

        {/* 2. SECCIÓN DERECHA: Íconos Sociales y Correo */}
        <div className="flex items-center space-x-6">
          {/* Íconos de Redes Sociales (Se mantienen con <a> para enlaces externos) */}
          <div className="flex space-x-4">
            {socialLinks.map(({ Icon, href, name }) => (
              <a
                key={name}
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`Enlace a mi perfil de ${name}`}
                className="text-green-300 hover:text-white transition duration-300"
              >
                <Icon className="w-6 h-6" />
              </a>
            ))}
          </div>

          {/* Ícono de Correo Electrónico (AHORA ES UNA RUTA INTERNA) */}
          <Link
            to="/contact"
            aria-label="Ir a la página de contacto"
            className="text-green-300 hover:text-white transition duration-300"
          >
            <HiOutlineMail className="w-7 h-7" />
          </Link>
        </div>
      </nav>
    </header>
  );
};

export default Header;
