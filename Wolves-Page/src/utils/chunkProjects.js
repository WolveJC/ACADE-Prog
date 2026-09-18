/* -------------------------------------------------------------
   UTILIDAD COMPARTIDA: chunkProjects
   -------------------------------------------------------------
   Divide un array de proyectos en páginas de tamaño fijo.
   Usada tanto por MainContent.jsx (para saber CUÁNTAS secciones
   crear en el carrusel) como por Projects.jsx (para saber QUÉ
   proyectos mostrar en la página que le corresponde).

   Mantenerla en un solo lugar evita que ambos archivos se
   desincronicen si el tamaño de página cambia en el futuro.
------------------------------------------------------------- */

// Tamaño de página por defecto (grid fijo 5×2)
export const PROJECTS_PAGE_SIZE = 10;

export const chunkProjects = (arr, size = PROJECTS_PAGE_SIZE) => {
  const chunks = [];
  for (let i = 0; i < arr.length; i += size) {
    chunks.push(arr.slice(i, i + size));
  }
  return chunks;
};