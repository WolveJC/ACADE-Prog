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

/* -------------------------------------------------------------
   getUniqueSectionsCount
   -------------------------------------------------------------
   Devuelve el número TOTAL de secciones únicas del carrusel de
   MainContent.jsx: Welcome (1) + páginas de proyectos (N) +
   AboutMe (1).

   Esta es la ÚNICA fuente de verdad sobre "cuántas secciones
   hay". La usan:
   - App.jsx: para inicializar <CarouselProvider totalUniqueSlides=.../>
   - MainContent.jsx: para construir el array `sections`

   Si el día de mañana se agrega o quita una sección fija
   (ej. una nueva página "Certificaciones"), este es el único
   lugar que hay que tocar.
------------------------------------------------------------- */
const FIXED_SECTIONS_COUNT = 2; // Welcome + AboutMe

export const getUniqueSectionsCount = (arr, size = PROJECTS_PAGE_SIZE) => {
  return FIXED_SECTIONS_COUNT + chunkProjects(arr, size).length;
};
