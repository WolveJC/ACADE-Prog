import React from "react";
import Avatar from "../UI/Avatar";
import { motion } from "framer-motion";

const Welcome = () => {
  return (
    <div className="text-center p-8 max-w-4xl mx-auto">
      {/* === Avatar === */}
      <Avatar size="large" />

      {/* === Título === */}
      <h1 className="text-6xl font-extrabold text-white mt-8 mb-4 tracking-tight">
        Hola, soy <span className="text-green-300">WolveJC</span>.
      </h1>

      {/* === Descripción === */}
      <p className="text-xl text-gray-200 max-w-2xl mx-auto leading-relaxed">
        Backend Developer. Bienvenido a mi rincón digital.
      </p>

      {/* === Llamada a la Acción === */}
      <div className="mt-8">
        <motion.a
          href="/documentacion"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          transition={{ duration: 0.4 }}
          className="inline-block px-8 py-3 text-lg font-semibold text-white bg-green-600 rounded-full hover:bg-green-700 transition duration-300 shadow-xl"
        >
          Explorar mi Bosque de Proyectos
        </motion.a>
      </div>
    </div>
  );
};

export default Welcome;
