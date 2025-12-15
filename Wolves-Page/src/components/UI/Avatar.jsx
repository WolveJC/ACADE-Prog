import React from "react";
import avatarImg from "../../assets/avatar.webp";

const Avatar = ({ size = "large", className = "" }) => {
  // Tamaños fluidos y responsivos
  const sizeClasses = {
    small: `
      w-10 h-10 
      sm:w-12 sm:h-12 
      md:w-14 md:h-14
    `,
    large: `
      w-28 h-28 
      sm:w-32 sm:h-32 
      md:w-44 md:h-44 
      lg:w-52 lg:h-52
    `,
  };

  // Hover más suave en modo small (para no romper el header)
  const hoverEffect =
    size === "small" ? "hover:scale-[1.03]" : "hover:scale-105";

  return (
    <img
      src={avatarImg}
      alt="Avatar de Portafolio"
      className={`
        ${sizeClasses[size]}
        rounded-full 
        object-cover 
        shadow-2xl 
        border-2 sm:border-4 border-green-300 
        transition-transform duration-300
        ${hoverEffect}
        ${className}
      `}
    />
  );
};

export default Avatar;
