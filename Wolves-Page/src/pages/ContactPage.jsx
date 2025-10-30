import React from 'react';
import Header from '../components/Layout/Header';

const ContactPage = () => {
  return (
    <>
      <Header />
      <main className="pt-20 p-8 min-h-screen bg-gray-900 text-white">
        <h1 className="text-4xl font-bold mb-6">Ponte en Contacto</h1>
        <p className="text-lg">Aquí irá tu formulario de contacto o información directa.</p>
        
        {/* Aquí se puede poner un formulario, mi correo visible, u otras cosas. */}
        {/* Ejemplo de un simple enlace mailto */}
        <a 
          href="mailto:walkgotrlust@hotmail.com?subject=Consulta%20desde%20tu%20Portafolio" 
          className="text-green-400 hover:text-green-500 underline mt-4 block"
        >
          Escríbeme directamente
        </a>
      </main>
    </>
  );
};

export default ContactPage;
