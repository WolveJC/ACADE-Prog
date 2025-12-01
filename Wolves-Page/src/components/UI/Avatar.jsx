import React from "react";
// Importar la imagen del avatar
import avatarImg from "../../assets/avatar.webp";

const Avatar = ({ size = "large" }) => {
  // Definir las clases de tamaño con Tailwind
  const sizeClasses = {
    // Usado en el Header
    small: "w-10 h-10 md:w-12 md:h-12",
    // Usado en la sección Welcome
    large: "w-32 h-32 md:w-48 md:h-48",
  };

  return (
    <img
      src={avatarImg}
      alt="Avatar de Portafolio"
      // Clases de Tailwind: circular, borde y sombra
      className={`
                ${sizeClasses[size]} 
                rounded-full 
                object-cover 
                shadow-2xl 
                border-4 border-green-300 
                transition-transform 
                hover:scale-105
            `}
    />
  );
};

export default Avatar;
