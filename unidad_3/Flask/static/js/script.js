// Versión Final: Incluye utilidades, validación mejorada, toasts,
//                fetch asíncrono, drag & drop y año dinámico en footer.

"use strict"; 

// ==========================================================================
//                          UTILITY FUNCTIONS
// ==========================================================================

/**
 * Muestra un mensaje de error asociado a un elemento del formulario.
 * Busca o crea un elemento span.error-message con un data-for attribute.
 * @param {HTMLElement} inputElement - El elemento del input.
 * @param {string} message - El mensaje de error a mostrar.
 */
function showError(inputElement, message) {
    clearError(inputElement); // Limpiar errores previos
    const identifier = inputElement.id || inputElement.name;
    if (!identifier) return;

    let errorElement = inputElement.parentNode.querySelector(`.error-message[data-for="${identifier}"]`);
    if (!errorElement) {
        errorElement = document.createElement('span');
        errorElement.className = 'error-message invalid-feedback';
        errorElement.dataset.for = identifier;
        inputElement.parentNode.insertBefore(errorElement, inputElement.nextSibling);
    }
    errorElement.textContent = message;
    inputElement.classList.add('is-invalid');
}

/**
 * Limpia el mensaje de error asociado a un elemento.
 * @param {HTMLElement} inputElement - El elemento del input.
 */
function clearError(inputElement) {
    const identifier = inputElement.id || inputElement.name;
    if (!identifier) return;

    const errorElement = inputElement.parentNode.querySelector(`.error-message[data-for="${identifier}"]`);
    if (errorElement) {
        errorElement.textContent = '';
    }
    inputElement.classList.remove('is-invalid');
}

/**
 * Limpia todos los mensajes de error y estilos 'is-invalid' dentro de un formulario o contenedor.
 * @param {HTMLFormElement | HTMLElement} containerElement - El formulario o contenedor a limpiar.
 */
function clearFormErrors(containerElement) {
    if (!containerElement) return;
    containerElement.querySelectorAll('.error-message').forEach(el => el.textContent = '');
    containerElement.querySelectorAll('.is-invalid').forEach(el => el.classList.remove('is-invalid'));
}

/**
 * Cierra un aviso con transición y lo quita del DOM.
 * El temporizador de respaldo cubre el caso en que no hay transición
 * (p. ej. usuarios con "reducir movimiento" activado).
 * @param {HTMLElement} toast - El aviso a cerrar.
 */
function cerrarToast(toast) {
    toast.classList.remove('show');
    const quitar = () => toast.remove();
    toast.addEventListener('transitionend', quitar, { once: true });
    setTimeout(quitar, 400);
}

/**
 * Muestra una notificación temporal en la esquina (alerta de Bootstrap).
 * @param {string} message - El mensaje a mostrar.
 * @param {'success' | 'error' | 'warning' | 'info'} type - Tipo de notificación.
 * @param {number} duration - Duración en milisegundos antes de desaparecer.
 */
function showToast(message, type = 'info', duration = 4000) {
    const container = document.getElementById('toast-container');
    if (!container) {
        console.error('Contenedor de Toast (#toast-container) no encontrado en el DOM!');
        alert(`${type.toUpperCase()}: ${message}`);
        return;
    }

    const clases = { success: 'alert-success', error: 'alert-danger', warning: 'alert-warning', info: 'alert-info' };
    const toast = document.createElement('div');
    toast.className = `alert ${clases[type] || 'alert-info'} alert-dismissible fade shadow-sm mb-2`;
    toast.style.pointerEvents = 'auto'; // el contenedor ignora el ratón; el aviso no
    toast.setAttribute('role', 'alert');
    toast.textContent = message;

    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'btn-close';
    closeButton.setAttribute('aria-label', 'Cerrar notificación');
    closeButton.addEventListener('click', () => {
        clearTimeout(timeoutId);
        cerrarToast(toast);
    });
    toast.appendChild(closeButton);

    container.appendChild(toast);

    toast.offsetHeight; // fuerza el reflow para que la transición de entrada se aplique

    requestAnimationFrame(() => {
        toast.classList.add('show');
    });

    const timeoutId = setTimeout(() => cerrarToast(toast), duration);
}


/**
 * Wrapper para la API Fetch con manejo de errores básico y JSON/Texto.
 * @param {string} url - La URL del endpoint.
 * @param {object} options - Opciones para fetch (method, headers, body, etc.).
 * @returns {Promise<any>} - Promesa con la respuesta procesada (JSON o texto).
 */
async function apiFetch(url, options = {}) {
    try {
        // Cabeceras para que el servidor responda JSON (y no con redirecciones HTML).
        // No se fija Content-Type: el navegador lo calcula (necesario con FormData).
        const opciones = {
            ...options,
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                ...(options.headers || {})
            }
        };
        const response = await fetch(url, opciones);
        const contentType = response.headers.get("content-type");
        let data;
        if (contentType && contentType.includes("application/json")) {
            data = await response.json();
        } else {
            data = await response.text();
        }
        if (!response.ok) {
            let errorMessage = response.statusText;
            if (data) {
                if (typeof data === 'object' && data !== null && (data.message || data.error)) {
                    errorMessage = data.message || data.error;
                } else if (typeof data === 'string' && data.length > 0 && data.length < 500) {
                    errorMessage = data;
                }
            }
            throw new Error(errorMessage || `HTTP error ${response.status}`);
        }
        return data;
    } catch (error) {
        console.error('API Fetch Error:', url, error);
        if (!(error instanceof Error)) {
             throw new Error(String(error.message || error));
        }
        throw error;
    }
}

/**
 * Muestra como toasts los mensajes flash enviados por el servidor
 * (JSON embebido en #flash-data por base.html).
 */
function showFlashMessages() {
    const el = document.getElementById('flash-data');
    if (!el) return;
    let mensajes = [];
    try {
        mensajes = JSON.parse(el.textContent);
    } catch (e) {
        return;
    }
    const tipos = { message: 'info', info: 'info', success: 'success', warning: 'warning', error: 'error' };
    mensajes.forEach(([categoria, texto]) => showToast(texto, tipos[categoria] || 'info', 6000));
}

/**
 * Establece el año actual en el elemento del pie de página.
 */
function setCopyrightYear() {
    const yearSpan = document.getElementById('current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    } else {
        // Opcional: Advertir si no se encuentra el span
        // console.warn('Elemento con ID "current-year" no encontrado para el año de copyright.');
    }
}


// ==========================================================================
//                LÓGICA ESPECÍFICA PARA CADA PÁGINA/SECCIÓN
// ==========================================================================

// Variable para el archivo a subir (Drag & Drop)
let fileToUpload = null;

// ------------------------------------------------------------
//             PÁGINA DE SUBIDA DE CSV (subir_csv.html)
// ------------------------------------------------------------
function setupFileUpload() {
    const form = document.querySelector('#form-subir-csv');
    const fileInput = form?.querySelector('#file');
    const dropZone = form?.querySelector('#drop-zone');
    const submitButton = form?.querySelector('button[type="submit"]');
    const fileNameDisplay = form?.querySelector('#drop-zone-filename');

    if (!form || !fileInput || !dropZone || !submitButton || !fileNameDisplay) return;

    function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('drag-over'), false);
    });
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('drag-over'), false);
    });
    dropZone.addEventListener('drop', handleDrop, false);
    function handleDrop(e) { const dt = e.dataTransfer; handleFiles(dt.files); }
    dropZone.addEventListener('click', (e) => {
        if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'A' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'LABEL') {
             fileInput.click();
        }
    });
    fileInput.addEventListener('change', (e) => handleFiles(e.target.files));

    function handleFiles(files) {
        clearFormErrors(form);
        fileNameDisplay.textContent = '';
        fileToUpload = null;

        if (files.length > 1) {
            showError(fileInput, 'Solo un archivo.');
            showToast('Solo puedes subir un archivo a la vez.', 'error');
            fileInput.value = ''; return;
        }
        if (files.length === 0) return;

        const file = files[0];
        const allowedExtension = '.csv';

        if (!file.name.toLowerCase().endsWith(allowedExtension)) {
            showError(fileInput, `Archivo inválido. Solo ${allowedExtension}.`);
            showToast(`Archivo inválido. Solo se permiten archivos ${allowedExtension}.`, 'error');
            fileInput.value = ''; return;
        }

        fileToUpload = file;
        fileNameDisplay.textContent = `Archivo: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        showToast('Archivo listo para subir.', 'info');
        clearError(fileInput);
    }

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        clearFormErrors(form);

        const file = fileToUpload;
        if (!file) {
            showError(fileInput, 'Selecciona o suelta un archivo CSV.');
            showToast('Por favor, selecciona o suelta un archivo CSV válido primero.', 'error');
            return;
        }
        if (!file.name.toLowerCase().endsWith('.csv')) {
            showError(fileInput, 'Archivo inválido. Selecciona un CSV.');
            showToast('Archivo inválido. Solo se permiten archivos CSV.', 'error');
            fileToUpload = null; fileNameDisplay.textContent = ''; fileInput.value = ''; return;
        }

        showToast(`Subiendo ${file.name}...`, 'info', 5000);
        submitButton.disabled = true;
        fileNameDisplay.textContent = `Subiendo: ${file.name}`;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await apiFetch('/', { method: 'POST', body: formData });
            showToast(response.message || 'Archivo CSV cargado con éxito.', 'success');
            fileToUpload = null; fileNameDisplay.textContent = '¡Subido con éxito!'; fileInput.value = '';
            setTimeout(() => window.location.reload(), 1500);
        } catch (error) {
            showToast(`Error al subir: ${error.message}`, 'error', 6000);
            fileNameDisplay.textContent = `Error al subir ${file.name}`;
             // SOLO rehabilitar el botón si NO hay recarga programada
             submitButton.disabled = false;
        }
        // finally {
            // La rehabilitación está ahora en el catch, porque en caso de éxito se recarga
        // }
    });
}


// ------------------------------------------------------------
//           PÁGINA DE PEDIDO DE STOCK (pedir_stock.html)
// ------------------------------------------------------------
function setupPedirStock() {
    const form = document.querySelector('#form-pedir-stock');
    const submitButton = form?.querySelector('button[type="submit"]');

    if (!form || !submitButton) return;

    form.addEventListener('input', (event) => {
        if (event.target.matches('input[type="number"]')) { clearError(event.target); }
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        clearFormErrors(form);

        let totalPedido = 0;
        let isValid = true;
        const inputsCantidad = form.querySelectorAll('input[type="number"][name^="pedido_stock"]');

        inputsCantidad.forEach(input => {
            const cantidad = parseInt(input.value) || 0;
            const maxStock = parseInt(input.max);
            if (cantidad < 0) { showError(input, 'No negativo.'); isValid = false; }
            else if (!isNaN(maxStock) && cantidad > maxStock) { showError(input, `Máx: ${maxStock}.`); isValid = false; }
            totalPedido += cantidad;
        });

        if (totalPedido <= 0 && inputsCantidad.length > 0) {
            showToast('Debes pedir al menos un producto (cantidad > 0).', 'warning');
            isValid = false;
        }

        if (!isValid) {
            showToast('Corrige los errores antes de enviar.', 'error');
            return;
        }

        showToast('Procesando pedido...', 'info');
        submitButton.disabled = true;

        try {
            const formData = new FormData(form);
            const response = await apiFetch('/pedir_stock', { method: 'POST', body: formData });

            let messageType = response.hubo_cambios ? 'success' : 'info';
            showToast(response.message || 'Proceso completado.', messageType, 6000);
            if(response.detalles && response.detalles.length > 0) { console.log("Detalles:", response.detalles); }

            setTimeout(() => window.location.reload(), 3000);

        } catch (error) {
             showToast(`Error al procesar pedido: ${error.message}`, 'error');
             submitButton.disabled = false;
        }
    });
}


// ------------------------------------------------------------
//        PÁGINA DE PEDIDO AL PROVEEDOR (pedir_proveedor.html)
// ------------------------------------------------------------
function setupPedirProveedor() {
    const form = document.querySelector('#form-pedir-proveedor');
    const submitButton = form?.querySelector('button[type="submit"]');

    if (!form || !submitButton) return;

    form.addEventListener('input', (event) => {
        if (event.target.matches('input[type="number"]')) { clearError(event.target); }
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        clearFormErrors(form);

        let isValid = true;
        let itemCount = 0;
        const rows = form.querySelectorAll('tbody tr');

        rows.forEach(row => {
            const inputCantidad = row.querySelector('input[type="number"][name^="pedido_proveedor"]');
            const inputPrecio = row.querySelector('input[type="number"][name^="precio_proveedor"]');
            const cantidad = parseInt(inputCantidad.value) || 0;
            const precio = parseFloat(inputPrecio.value) || 0;

            if (cantidad < 0) { showError(inputCantidad, 'No negativo.'); isValid = false; }
            if (cantidad > 0) {
                itemCount++;
                if (precio <= 0) { showError(inputPrecio, 'Precio > 0.'); isValid = false; }
            }
        });

        if (itemCount === 0 && rows.length > 0) {
            showToast('Debes pedir al menos un producto (cantidad > 0).', 'warning');
            isValid = false;
        }

        if (!isValid) {
            showToast('Corrige los errores en el formulario.', 'error');
            return;
        }

        showToast('Enviando pedido para generar PDF...', 'info');
        submitButton.disabled = true;

        try {
            const formData = new FormData(form);
            const response = await apiFetch('/pedir_proveedor', { method: 'POST', body: formData });

            if (response.redirect_url) {
                showToast(response.message || 'Pedido enviado. Redirigiendo a PDF...', 'success');
                setTimeout(() => window.location.href = response.redirect_url, 1500);
            } else {
                showToast(response.message || 'Pedido procesado, pero ocurrió un problema inesperado al redirigir.', 'warning');
                 submitButton.disabled = false;
            }

        } catch (error) {
            showToast(`Error al enviar pedido: ${error.message}`, 'error');
            submitButton.disabled = false;
        }
    });
}


// ==========================================================================
//                          INICIALIZACIÓN
// ==========================================================================
document.addEventListener('DOMContentLoaded', function() {
    setupFileUpload();
    setupPedirStock();
    setupPedirProveedor();
    setCopyrightYear();
    showFlashMessages();
});