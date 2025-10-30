import React from 'react';
import usePageTitle from '../hooks/usePageTitle';

const ContactPage = () => {
    usePageTitle('WolveJC | ContactMe'); 

    // 1. Reemplaza 'TU_CORREO_AQUI' con tu dirección real de Hotmail.
    // FormSubmit procesará esto y enviará un correo de confirmación la primera vez.
    const FORM_ENDPOINT = "https://formsubmit.co/walkgotrlust@hotmail.com";

    return (
        <div className="p-8 max-w-xl mx-auto">
            <h1 className="text-4xl font-bold mb-6 text-green-400">
                Contactemos
            </h1>
            <p className="text-lg mb-8">
                Déjame tu mensaje, y te responderé lo antes posible.
            </p>

            {/* 2. Formulario HTML con la acción apuntando a FormSubmit */}
            <form 
                action={FORM_ENDPOINT} 
                method="POST" 
                className="space-y-4"
            >
                {/* Campo para el Nombre */}
                <input 
                    type="text" 
                    name="name" // El atributo name es crucial
                    placeholder="Tu Nombre" 
                    required 
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                />

                {/* Campo para el Correo del Usuario (_replyto para responder) */}
                <input 
                    type="email" 
                    name="email" // Usamos 'email' para que FormSubmit lo use como Reply-To por defecto
                    placeholder="Tu Correo Electrónico" 
                    required 
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-green-500"
                />
                
                {/* Campo Oculto para Asunto (Opcional) */}
                <input 
                    type="hidden" 
                    name="_subject" 
                    value="Nuevo Mensaje desde tu Portafolio" 
                />
                
                {/* Campo para Mensaje */}
                <textarea 
                    name="message" // El atributo name es crucial
                    placeholder="Tu Mensaje" 
                    rows="4" 
                    required 
                    className="w-full p-3 rounded bg-gray-700 border border-gray-600 text-white focus:outline-none focus:ring-2 focus:ring-green-500 resize-none"
                ></textarea>
                
                {/* Botón de Envío */}
                <button 
                    type="submit" 
                    className="w-full py-3 bg-green-600 text-white font-bold rounded hover:bg-green-700 transition duration-300"
                >
                    Enviar Mensaje
                </button>
            </form>
        </div>
    );
};

export default ContactPage;
