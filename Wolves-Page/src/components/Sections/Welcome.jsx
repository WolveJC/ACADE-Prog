import React from "react";
import Avatar from "../UI/Avatar";
import { motion } from "framer-motion";

const Welcome = () => {
  return (
    <div
      className="
        text-center 
        w-full 
        max-w-4xl 
        mx-auto 
        px-4 
        md:px-8 
        pt-4 
        md:pt-6
      "
    >
      {/* === Avatar === */}
      <div className="flex justify-center">
        <Avatar size="medium" />
      </div>

      {/* === Título === */}
      <h1
        className="
          text-white 
          font-extrabold 
          tracking-tight 
          mt-6 
          mb-3
          text-3xl 
          sm:text-4xl 
          md:text-5xl
        "
      >
        Hola, soy <span className="text-green-300">WolveJC</span>.
      </h1>

      {/* === Descripción === */}
      <p
        className="
          text-gray-200 
          leading-relaxed 
          mx-auto 
          max-w-xl
          text-sm 
          sm:text-base 
          md:text-lg
        "
      >
        Backend Developer. Bienvenido a mi rincón digital.
      </p>

      {/* === Llamada a la Acción === */}
      <div className="mt-6">
        <motion.a
          href="/documentacion"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          transition={{ duration: 0.4 }}
          className="
            inline-block 
            px-5 
            sm:px-7 
            py-2.5 
            text-sm 
            sm:text-base 
            font-semibold 
            text-white 
            bg-green-600 
            rounded-full 
            hover:bg-green-700 
            transition 
            duration-300 
            shadow-lg
          "
        >
          Explorar mi Bosque de Proyectos
        </motion.a>
      </div>
    </div>
  );
};

export default Welcome;
