import React from 'react';
// Importar tu foto peronal
import profilePic from './assets/profile-pic.png'; 

const AboutMe = () => {
  return (
    <div className="p-8 md:p-12 max-w-4xl mx-auto w-full">
      
      <h2 className="text-5xl font-extrabold text-white mb-10 text-center tracking-wide">
        Sobre <span className="text-green-300">Mí</span>
      </h2>

      <div className="md:flex md:space-x-12 items-center text-left bg-black/40 p-6 rounded-xl shadow-2xl">
        
        {/* Foto personal */}
        <div className="flex-shrink-0 mb-8 md:mb-0">
          <img 
            src={profilePic} 
            alt="Tu Foto Personal"
            // Estilo de foto de perfil (circular, borde contrastante)
            className="w-48 h-48 object-cover rounded-full mx-auto shadow-xl border-4 border-green-300/80"
          />
        </div>
        
        {/* Texto biográfico */}
        <div>
          <p className="text-gray-200 text-lg mb-4 leading-relaxed">
            Soy un desarrollador en constante crecimiento con una profunda curiosidad por diversas tecnologías. Aunque me considero <strong>novato en muchas áreas</strong>, me gusta diversificar mis conocimientos, explorando las posibilidades de <strong>Python, Java y Javascript</strong> para construir soluciones.
          </p>
          
          <p className="text-gray-200 text-lg mb-4 leading-relaxed">
            Mi enfoque está en aprender de manera continua y estructurada, pero mi vida no se limita al código. También encuentro gran valor y disfrute en actividades como la <strong>lectura y escritura</strong>, que nutren mi creatividad y lógica.
          </p>
          
          <p className="text-gray-200 text-lg mb-4 leading-relaxed">
            Además, me atraen las artes de <strong>los videojuegos</strong> (por su narrativa y diseño), <strong>la música</strong> (como forma de expresión) y <strong>la cocina</strong> (por su precisión y experimentación). Son disciplinas que, al igual que la programación, siempre me ha llamado la atención aprender y dominar.
          </p>
          
          <p className="text-sm italic text-green-300 mt-4">
            — "Siempre buscando la intersección entre la creatividad y la función."
          </p>
        </div>
      </div>
    </div>
  );
};

export default AboutMe;