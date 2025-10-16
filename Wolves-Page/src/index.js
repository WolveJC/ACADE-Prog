import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './styles/index.css';

// 1. Obtener el elemento raíz del DOM (un div con id="root")
const rootElement = document.getElementById('root');

// 2. Crear la raíz de React 
// (Esto inicializa la aplicación React para la versión 18+)
if (rootElement) {
    ReactDOM.createRoot(rootElement).render(
        <React.StrictMode>
            {/* 3. Renderizar el componente App */}
            <App />
        </React.StrictMode>,
    );
} else {
    // Manejo de error simple si el elemento raíz no existe
    console.error("No se encontró el elemento con ID 'root' para renderizar la aplicación React.");
}