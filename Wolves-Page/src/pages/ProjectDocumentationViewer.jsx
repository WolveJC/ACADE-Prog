import React, { useState, useEffect } from "react";
import { Document, Page, pdfjs } from "react-pdf";
import {
  FaChevronLeft,
  FaChevronRight,
  FaMoon,
  FaSun,
  FaDownload,
} from "react-icons/fa";

import workerSrc from "pdfjs-dist/build/pdf.worker.min.mjs";
pdfjs.GlobalWorkerOptions.workerSrc = workerSrc;

const DOCUMENT_PATH = "/docs/doc_proj.pdf";

const ProjectDocumentationViewer = () => {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [pageWidth, setPageWidth] = useState(700);

  // Ajustar ancho dinámico al contenedor
  useEffect(() => {
    const updateWidth = () => {
      const container = document.getElementById("pdf-container");
      if (container) {
        const maxWidth = container.offsetWidth;
        setPageWidth(Math.min(maxWidth - 48, 1000));
      }
    };
    updateWidth();
    window.addEventListener("resize", updateWidth);
    return () => window.removeEventListener("resize", updateWidth);
  }, []);

  const onDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
    setPageNumber(1);
  };

  const handleDownload = () => {
    window.open(DOCUMENT_PATH, "_blank");
  };

  const goToPrevPage = () => {
    if (pageNumber > 1) setPageNumber(pageNumber - 1);
  };

  const goToNextPage = () => {
    if (pageNumber < numPages) setPageNumber(pageNumber + 1);
  };

  const themeClasses = isDarkMode
    ? "bg-gray-900 text-gray-100 border-gray-700"
    : "libro-antiguo border-cafe-oscuro";

  const iconClasses = "w-6 h-6 leaf-trigger";

  return (
    <div
      id="pdf-container"
      className={`p-8 rounded-lg shadow-2xl transition-all duration-500 max-w-7xl mx-auto ${themeClasses}`}
    >
      {/* --- CONTROLES SUPERIORES --- */}
      <div className="flex justify-between items-center mb-6 pb-4 border-b border-current">
        <button
          onClick={() => setIsDarkMode((prev) => !prev)}
          className={`p-2 rounded-full hover:opacity-80 transition ${iconClasses}`}
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
          onClick={handleDownload}
        >
          <FaDownload />
        </a>
      </div>

      {/* --- VISOR DE UNA SOLA PÁGINA --- */}
      <Document
        file={DOCUMENT_PATH}
        onLoadSuccess={onDocumentLoadSuccess}
        loading={
          <p className="text-center font-bold animate-pulse p-10 mx-auto">
            Cargando Reporte...
          </p>
        }
        error={
          <p className="text-center text-red-500 font-bold p-10 mx-auto">
            Error al cargar el PDF. Asegúrate de que existe en /docs/.
          </p>
        }
      >
        <div className="flex flex-col items-center">
          <div
            className="pdf-texture page-flip w-full max-w-4xl mx-auto"
            style={{
              boxShadow:
                "0 0 40px rgba(0,0,0,0.45), inset 0 -10px 25px rgba(0,0,0,0.25)",
              borderRadius: "6px",
            }}
          >
            <Page
              pageNumber={pageNumber}
              width={pageWidth}
              renderAnnotationLayer={false}
              renderTextLayer={true}
              renderMode="svg"
            />
          </div>
        </div>
      </Document>

      {/* --- CONTROLES DE PÁGINA INFERIORES --- */}
      <div className="flex justify-center mt-6 pt-4 border-t border-current">
        <button
          onClick={goToPrevPage}
          disabled={pageNumber <= 1}
          className={`p-2 rounded-full mx-2 ${iconClasses} disabled:opacity-30 transition`}
        >
          <FaChevronLeft />
        </button>

        <button
          onClick={goToNextPage}
          disabled={!numPages || pageNumber >= numPages}
          className={`p-2 rounded-full mx-2 ${iconClasses} disabled:opacity-30 transition`}
        >
          <FaChevronRight />
        </button>
      </div>
    </div>
  );
};

export default ProjectDocumentationViewer;
