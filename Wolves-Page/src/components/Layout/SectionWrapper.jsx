import React from "react";

const SectionWrapper = ({
  children,
  mode = "default", // "default" | "center" | "panel"
}) => {
const base = `
  shrink-0 
  w-screen 
  h-full 
  px-6 md:px-12 
  py-0
  overflow-hidden
  bg-black/30 
  backdrop-blur-xs 
  shadow-2xl 
  border-x 
  border-gray-700/50
`;


  const modes = {
    default: "flex flex-col justify-start",
    center: "flex flex-col justify-center items-center",
    panel: "flex flex-col", // Projects necesita esto
  };

  return (
    <section className={`${base} ${modes[mode]}`}>
      {mode === "panel" ? (
        // ✅ Este contenedor es CLAVE:
        // - flex-1 permite que Projects tome el espacio disponible
        // - overflow-hidden evita la barra vertical interna
        // - permite que el grid 3×3 se muestre completo
        <div className="flex-1 overflow-hidden">{children}</div>
      ) : (
        children
      )}
    </section>
  );
};

export default SectionWrapper;
