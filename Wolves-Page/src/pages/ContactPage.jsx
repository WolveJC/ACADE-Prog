import React from 'react';
import { Link } from 'react-router-dom';
import usePageTitle from '../hooks/usePageTitle'; 
import ArrowWoodPNG from '../assets/arrow-return.png';

const ContactPage = () => {
    usePageTitle('WolveJC | Contacto'); 
    
    const FORM_ENDPOINT = "https://formsubmit.co/walkgotrlust@hotmail.com";

    return (
        <div className="p-8 max-w-xl mx-auto">
            
            {/* Botón de Retorno con Imagen PNG */}
            <Link 
                to="/" 
                className="flex items-center text-white hover:text-gray-300 mb-6 transition duration-300"
            >
                <img 
                    src={ArrowWoodPNG} 
                    alt="Volver" 
                    className="w-8 h-8 mr-2" // Ajustar tamaño aquí (w-8 h-8 es 32x32px)
                />
                <span className="font-semibold">Volver al Portafolio</span>
            </Link>

            {/* Títulos y Párrafos: Texto Blanco/Crema sobre Oscuro */}
            <h1 className="text-4xl font-bold mb-3 text-white">
                ¡Hablemos en la Profundidad del Bosque!
            </h1>
            <p className="text-lg mb-8 text-gray-300">
                Siempre estoy dispuesto a conversar sobre proyectos, ideas o tecnología. Escríbeme y exploremos nuevas sendas juntos.
            </p>

            {/* Formulario FormSubmit: Base Oscura, Campos Claros */}
            <form 
                action={FORM_ENDPOINT} 
                method="POST" 
                // Fondo oscuro (el color forest-start o un gris muy oscuro)
                className="space-y-4 p-6 bg-forest-start/50 border border-gray-700 rounded-xl shadow-2xl" 
            >
                {/* Campos de Entrada */}
                <input 
                    type="text" 
                    name="name" 
                    placeholder="Tu Nombre" 
                    required 
                    className="w-full p-3 rounded-sm bg-gray-800 border border-gray-700 text-white focus:outline-hidden focus:ring-2 focus:ring-green-500"
                />

                <input 
                    type="email" 
                    name="email" 
                    placeholder="Tu Correo Electrónico" 
                    required 
                    className="w-full p-3 rounded-sm bg-gray-800 border border-gray-700 text-white focus:outline-hidden focus:ring-2 focus:ring-green-500"
                />
                
                <input type="hidden" name="_subject" value="Buy Me A Coffee!" />
                
                <textarea 
                    name="message" 
                    placeholder="Cuéntame sobre tu idea..." 
                    rows="4" 
                    required 
                    className="w-full p-3 rounded-sm bg-gray-800 border border-gray-700 text-white focus:outline-hidden focus:ring-2 focus:ring-green-500 resize-none"
                ></textarea>
                
                {/* Botón de Envío: Color de botón temático */}
                <button 
                    type="submit" 
                    // Un color de botón
                    className="w-full py-3 bg-green-700 text-white font-bold rounded-sm hover:bg-green-600 transition duration-300 shadow-lg"
                >
                    Enviar Mensaje y Conectar
                </button>
            </form>
        </div>
    );
};

export default ContactPage;