import React, { useState, useEffect, useCallback, useRef } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import {
  FaChevronLeft,
  FaChevronRight,
  FaMoon,
  FaSun,
  FaDownload,
} from "react-icons/fa";

import workerSrc from "pdfjs-dist/build/pdf.worker.min.js?url";

pdfjs.GlobalWorkerOptions.workerSrc = workerSrc;

// Ruta del PDF que se DEBE GENERAR PRIMERO
const DOCUMENT_PATH = "../../public/docs/doc_proj.pdf";
const PAGE_WIDTH = 700; // Ancho base para la página PDF

const ProjectDocumentationViewer = () => {
  // --- ESTADOS ---
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [isDarkMode, setIsDarkMode] = useState(false);

  // --- REFERENCIAS ---
  const scrollContainerRef = useRef(null);
  const pageRefs = useRef({});

  // --- MANEJADORES DE CARGA DEL DOCUMENTO ---
  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
    setPageNumber(1);
  };

  const handleDownload = () => {
    window.open(DOCUMENT_PATH, "_blank");
  };

  // --- 1. LÓGICA DE NAVEGACIÓN (Botones y Teclado) ---
  const goToPage = useCallback(
    (newPageIndex) => {
      if (newPageIndex >= 1 && newPageIndex <= numPages) {
        setPageNumber(newPageIndex);
        const targetPageElement = pageRefs.current[newPageIndex];
        if (scrollContainerRef.current && targetPageElement) {
          targetPageElement.scrollIntoView({
            behavior: "smooth",
            inline: "start",
          });
        }
      }
    },
    [numPages]
  );

  const goToPrevPage = () => goToPage(pageNumber - 1);
  const goToNextPage = () => goToPage(pageNumber + 1);

  // --- 2. EFECTO: CONTROL DE TECLADO ---
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === "ArrowLeft") goToPrevPage();
      else if (event.key === "ArrowRight") goToNextPage();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [goToPrevPage, goToNextPage]);

  // --- 3. EFECTO: INTERSECTION OBSERVER ---
  useEffect(() => {
    if (!numPages || !scrollContainerRef.current) return;
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && entry.intersectionRatio >= 0.8) {
            const pageIndex = parseInt(entry.target.dataset.pageIndex, 10);
            setPageNumber(pageIndex);
          }
        });
      },
      { root: scrollContainerRef.current, threshold: 0.8 }
    );
    Object.values(pageRefs.current).forEach((el) => el && observer.observe(el));
    return () => observer.disconnect();
  }, [numPages]);

  // --- CLASES DE ESTILO ---
  const themeClasses = isDarkMode
    ? "bg-gray-800 text-gray-200 border-gray-700"
    : "libro-antiguo border-cafe-oscuro";

  const iconClasses = "w-6 h-6 leaf-trigger";
  const snapScrollClasses =
    "flex overflow-x-scroll snap-x snap-mandatory w-full scrollbar-none";
  const pageWrapperClasses = "shrink-0 snap-start px-2";
  const viewerHeight = "calc(100vh - 200px)";

  return (
    <div
      className={`
      p-8 rounded-lg shadow-2xl transition-all duration-500 max-w-7xl mx-auto
      ${themeClasses}
    `}
    >
      {/* --- CONTROLES SUPERIORES --- */}
      <div
        className="flex justify-between items-center mb-6 pb-4 border-b border-current"
        role="navigation"
      >
        <button
          onClick={() => setIsDarkMode((prev) => !prev)}
          className={`p-2 rounded-full hover:opacity-80 transition ${iconClasses}`}
          aria-label={
            isDarkMode
              ? "Cambiar a modo Libro Antiguo"
              : "Cambiar a modo Oscuro"
          }
        >
          {isDarkMode ? <FaSun /> : <FaMoon />}
        </button>

        <span className="text-xl font-serif font-bold">
          {numPages ? `Página ${pageNumber} de ${numPages}` : "Cargando..."}
        </span>

        <a
          href={DOCUMENT_PATH}
          download={`reporte-proyectos-${new Date().getFullYear()}.pdf`}
          className={`p-2 rounded-full hover:opacity-80 transition ${iconClasses}`}
          aria-label="Descargar el Reporte Completo"
          onClick={handleDownload}
        >
          <FaDownload />
        </a>
      </div>

      {/* --- VISOR DE DOCUMENTACIÓN --- */}
      <div
        ref={scrollContainerRef}
        className={snapScrollClasses}
        style={{ height: viewerHeight }}
      >
        <Document
          file={DOCUMENT_PATH}
          onLoadSuccess={onDocumentLoadSuccess}
          loading={
            <p className="text-center font-bold animate-pulse p-10">
              Cargando Reporte...
            </p>
          }
          error={
            <p className="text-center text-red-500 font-bold p-10">
              Error al cargar el PDF. Asegúrate de que existe en /docs/.
            </p>
          }
        >
          {Array.from({ length: numPages || 0 }, (_, index) => {
            const pageIndex = index + 1;
            return (
              <div
                key={`page_${pageIndex}`}
                className={`${pageWrapperClasses} relative`}
                ref={(el) => (pageRefs.current[pageIndex] = el)}
                data-page-index={pageIndex}
                style={{
                  width: PAGE_WIDTH,
                  boxShadow: isDarkMode
                    ? "none"
                    : "10px 10px 30px rgba(0, 0, 0, 0.5)",
                }}
              >
                <Page
                  pageNumber={pageIndex}
                  renderAnnotationLayer={false}
                  renderTextLayer={true}
                  renderMode="svg"
                  width={PAGE_WIDTH}
                  className="mx-auto"
                />
              </div>
            );
          })}
        </Document>
      </div>

      {/* --- CONTROLES DE PÁGINA INFERIORES --- */}
      <div
        className="flex justify-center mt-6 pt-4 border-t border-current"
        role="navigation"
      >
        <button
          onClick={goToPrevPage}
          disabled={pageNumber <= 1}
          className={`p-2 rounded-full mx-2 ${iconClasses} disabled:opacity-30 transition`}
          aria-label="Página anterior"
        >
          <FaChevronLeft />
        </button>
        <button
          onClick={goToNextPage}
          disabled={pageNumber >= numPages}
          className={`p-2 rounded-full mx-2 ${iconClasses} disabled:opacity-30 transition`}
          aria-label="Página siguiente"
        >
          <FaChevronRight />
        </button>
      </div>
    </div>
  );
};

export default ProjectDocumentationViewer;
