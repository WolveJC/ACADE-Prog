/* -------------------------------------------------------------
   UTILIDAD: sectionColor
   -------------------------------------------------------------
   Antes, el color de fondo del Header vivía en un COLOR_MAP fijo
   de 3 entradas (0, 1, 2), pensado para exactamente 3 secciones
   (Welcome, Projects, AboutMe). Al paginar el portafolio en N
   páginas, el número real de secciones dejó de ser 3, y ese mapa
   fijo ya no podía representar una transición completa.

   Esta utilidad reemplaza el mapa fijo por una INTERPOLACIÓN
   continua entre 3 colores (inicio, medio, fin), calculada según
   la posición relativa de la sección actual dentro del total real
   de secciones (currentSlideIndex / totalUniqueSlides). Así, sin
   importar si hay 3 o 10 secciones, el recorrido siempre arranca
   en el color de inicio y termina en el de fin, pasando por el
   color medio a mitad de camino — la misma "atmósfera" de antes,
   pero generalizada.

   Los colores se leen directamente de las variables CSS definidas
   en @theme (src/styles/index.css) para no duplicar los valores
   hex en JavaScript. Si cambias el tema ahí, este util lo refleja
   automáticamente.
------------------------------------------------------------- */

const CSS_VARS = {
  start: "--color-forest-start",
  mid: "--color-forest-mid",
  end: "--color-forest-end",
};

// Fallbacks por si el componente se evalúa antes de que el CSS
// esté disponible (deben coincidir con index.css como respaldo).
const FALLBACK_HEX = {
  start: "#1b4d3e",
  mid: "#4b3621",
  end: "#2c2016",
};

const readCssVar = (varName, fallbackHex) => {
  if (typeof window === "undefined" || typeof document === "undefined") {
    return fallbackHex;
  }
  const value = getComputedStyle(document.documentElement)
    .getPropertyValue(varName)
    .trim();
  return value || fallbackHex;
};

const hexToRgb = (hex) => {
  const clean = hex.replace("#", "");
  const bigint = parseInt(clean, 16);
  return {
    r: (bigint >> 16) & 255,
    g: (bigint >> 8) & 255,
    b: bigint & 255,
  };
};

const lerp = (a, b, t) => Math.round(a + (b - a) * t);

const lerpColor = (hexA, hexB, t) => {
  const a = hexToRgb(hexA);
  const b = hexToRgb(hexB);
  return `rgb(${lerp(a.r, b.r, t)}, ${lerp(a.g, b.g, t)}, ${lerp(a.b, b.b, t)})`;
};

/**
 * Devuelve el color de fondo (como string rgb(...)) que le corresponde
 * a la sección `index` dentro de un total de `total` secciones únicas.
 *
 * @param {number} index - currentSlideIndex (0-based)
 * @param {number} total - totalUniqueSlides (viene de GlobalCarousel.jsx,
 *                          calculado en última instancia por
 *                          getUniqueSectionsCount en utils/chunkProjects.js)
 */
export const getSectionBackgroundColor = (index, total) => {
  const start = readCssVar(CSS_VARS.start, FALLBACK_HEX.start);
  const mid = readCssVar(CSS_VARS.mid, FALLBACK_HEX.mid);
  const end = readCssVar(CSS_VARS.end, FALLBACK_HEX.end);

  // Con 1 sola sección (o total inválido) no hay recorrido que interpolar.
  if (!total || total <= 1) return start;

  // Normaliza el índice por si llega negativo o fuera de rango.
  const safeIndex = Math.min(Math.max(index, 0), total - 1);
  const t = safeIndex / (total - 1); // 0 → primera sección, 1 → última

  // Primera mitad del recorrido: start -> mid
  if (t <= 0.5) {
    return lerpColor(start, mid, t / 0.5);
  }
  // Segunda mitad del recorrido: mid -> end
  return lerpColor(mid, end, (t - 0.5) / 0.5);
};