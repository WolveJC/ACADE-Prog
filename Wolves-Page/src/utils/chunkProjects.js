/* -------------------------------------------------------------
   UTILIDAD COMPARTIDA: chunkProjects
   -------------------------------------------------------------
   Divide un array de proyectos en paginas de size fijo.
   Usada tanto por MainContent.jsx (para saber CUANTAS secciones
   crear en el carrusel) como por Projects.jsx (para saber QUE
   proyectos mostrar en la pagina que le corresponde).

   Mantenerla en un solo lugar evita que ambos archivos se
   desincronicen si el size de pagina cambia en el futuro.
------------------------------------------------------------- */

// Size de pagina por defecto (grid fijo 5x2)
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
   Devuelve el numero TOTAL de secciones unicas del carrusel de
   MainContent.jsx: Welcome (1) + paginas de proyectos (N) +
   AboutMe (1).

   Esta es la UNICA fuente de verdad sobre "cuantas secciones
   hay". La usan:
   - App.jsx: para inicializar <CarouselProvider totalUniqueSlides=.../>
   - MainContent.jsx: para construir el array `sections`

   Si el dia de manana se agrega o quita una seccion fija
   (ej. una nueva pagina "Certificaciones"), este es el unico
   lugar que hay que tocar.
------------------------------------------------------------- */
const FIXED_SECTIONS_COUNT = 2; // Welcome + AboutMe

export const getUniqueSectionsCount = (arr, size = PROJECTS_PAGE_SIZE) => {
  return FIXED_SECTIONS_COUNT + chunkProjects(arr, size).length;
};