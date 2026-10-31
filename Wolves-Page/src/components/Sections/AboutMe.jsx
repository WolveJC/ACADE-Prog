import React from "react";
import profilePic from "../../assets/profile-pic.webp";

const AboutMe = () => {
  return (
    <div
      className="
        w-full 
        max-w-4xl 
        mx-auto 
        px-4 
        md:px-8 
        pt-4 md:pt-6
      "
    >
      {/* === Título === */}
      <h2
        className="
          text-center 
          font-extrabold 
          tracking-wide 
          text-white 
          mb-6
          text-3xl 
          sm:text-4xl 
          md:text-5xl
        "
      >
        Sobre <span className="text-green-300">Mí</span>
      </h2>

      {/* === Contenedor principal === */}
      <div
        className="
          bg-black/40 
          rounded-xl 
          shadow-xl 
          p-4 
          md:p-6
          flex 
          flex-col 
          md:flex-row 
          md:space-x-8 
          items-center
        "
      >
        {/* === Foto personal === */}
        <div className="shrink-0 mb-6 md:mb-0 flex justify-center">
          <img
            src={profilePic}
            alt="Foto Personal"
            className="
              w-28 
              h-28 
              sm:w-32 
              sm:h-32 
              object-cover 
              rounded-full 
              shadow-lg 
              border-4 
              border-green-300/80
            "
          />
        </div>

        {/* === Texto biográfico === */}
        <div className="text-left max-w-xl">
          <p
            className="
              text-gray-200 
              leading-relaxed 
              mb-3
              text-sm 
              sm:text-base
            "
          >
            Soy un desarrollador en constante crecimiento con una profunda
            curiosidad por diversas tecnologías. Aunque me considero{" "}
            <strong>novato en muchas áreas</strong>, me gusta diversificar mis
            conocimientos explorando <strong>Python, Java y Javascript</strong>.
          </p>

          <p
            className="
              text-gray-200 
              leading-relaxed 
              mb-3
              text-sm 
              sm:text-base
            "
          >
            Mi enfoque está en aprender de manera continua y estructurada, pero
            también encuentro valor en la <strong>lectura y escritura</strong>,
            que nutren mi creatividad.
          </p>

          <p
            className="
              text-gray-200 
              leading-relaxed 
              mb-3
              text-sm 
              sm:text-base
            "
          >
            Me atraen los <strong>videojuegos</strong>, la{" "}
            <strong>música</strong> y la <strong>cocina</strong>, disciplinas
            que combinan técnica, narrativa y precisión.
          </p>

          <p className="text-xs sm:text-sm italic text-green-300 mt-3">
            — "Siempre buscando la intersección entre la creatividad y la
            funcionalidad."
          </p>
        </div>
      </div>
    </div>
  );
};

export default AboutMe;
