/** @type {import('tailwindcss').Config} */
module.exports = {
  // 1. CONTENT: Le dice a Tailwind qué archivos escanear para encontrar clases.
  content: [
    // Escanea todos los archivos .js, .jsx, .ts, y .tsx dentro de la carpeta src
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  
  // 2. THEME: Aquí esse sobrescribe los valores predeterminados de Tailwind.
  theme: {
    extend: {
      // Definición de  colores personalizados
      colors: {
        // Verde Oscuro (para la parte superior de la página)
        'forest-start': '#1B4D3E', 
        
        // Tono intermedio (para la transición)
        'forest-mid': '#4B3621',   
        
        // Café Muy Oscuro (para la parte inferior de la página)
        'forest-end': '#2C2016',   
      },
    },
  },
  
  // 3. PLUGINS: 
  plugins: [],
}