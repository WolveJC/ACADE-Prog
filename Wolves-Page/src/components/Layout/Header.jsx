import React from "react";
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

  // Correo y Enlace mailto (Prueba)
  const emailAddress = "walkgotrlust@hotmail.com";
  const emailSubject = "Contacto desde Portafolio";
  // Codificamos el asunto para que funcione correctamente en URLs
  const mailtoLink = `mailto:${emailAddress}?subject=${encodeURIComponent(
    emailSubject
  )}`;

  return (
    // Header fijo con estilo oscuro y sutilmente borroso
    <header className="fixed top-0 w-full z-50 p-4 shadow-lg bg-forest-start/90 backdrop-blur-sm">
      <nav className="flex items-center justify-between max-w-7xl mx-auto">
        {/* 1. SECCIÓN IZQUIERDA: Avatar y Nombre */}
        <div className="flex items-center space-x-4">
          {/* El Avatar aquí será pequeño */}
          {/* Nota: Se necesita crear un archivo Avatar.jsx */}
          <Avatar size="small" />
          <span className="text-xl font-bold text-white hidden sm:block">
            WolveJC
          </span>
        </div>

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
                // Tono verde contrastante
                className="text-green-300 hover:text-white transition duration-300"
              >
                <Icon className="w-6 h-6" />
              </a>
            ))}
          </div>

          {/* Ícono de Correo Electrónico (mailto) */}
          <a
            href={mailtoLink}
            aria-label={`Enviar correo a ${emailAddress}`}
            className="text-green-300 hover:text-white transition duration-300"
          >
            <HiOutlineMail className="w-7 h-7" />
          </a>
        </div>
      </nav>
    </header>
  );
};

export default Header;
