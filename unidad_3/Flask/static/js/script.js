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
        errorElement.className = 'error-message';
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
 * Muestra una notificación "toast" temporal en la esquina.
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

    const toast = document.createElement('div');
    toast.className = `toast-message toast-${type}`;
    toast.textContent = message;

    const closeButton = document.createElement('button');
    closeButton.className = 'toast-close-button';
    closeButton.innerHTML = '&times;';
    closeButton.setAttribute('aria-label', 'Cerrar notificación');
    closeButton.onclick = () => {
        toast.classList.remove('show');
        toast.classList.add('hide');
        toast.addEventListener('transitionend', () => toast.remove(), { once: true });
    };
    toast.appendChild(closeButton);

    container.appendChild(toast);

    toast.offsetHeight;

    requestAnimationFrame(() => {
        toast.classList.add('show');
    });

    const timeoutId = setTimeout(() => {
        toast.classList.remove('show');
        toast.classList.add('hide');
        toast.addEventListener('transitionend', () => toast.remove(), { once: true });
    }, duration);

    closeButton.addEventListener('click', () => clearTimeout(timeoutId));
}


/**
 * Wrapper para la API Fetch con manejo de errores básico y JSON/Texto.
 * @param {string} url - La URL del endpoint.
 * @param {object} options - Opciones para fetch (method, headers, body, etc.).
 * @returns {Promise<any>} - Promesa con la respuesta procesada (JSON o texto).
 */
async function apiFetch(url, options = {}) {
    try {
        const response = await fetch(url, options);
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
 * Genera un código alfanumérico aleatorio único dentro de un conjunto opcional.
 * @param {number} longitud - Longitud del código.
 * @param {string[]} [existingCodes=[]] - Array opcional de códigos existentes para verificar unicidad.
 * @returns {string} - Código aleatorio único.
 */
function generarCodigoAleatorio(longitud = 6, existingCodes = []) {
    const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let attempts = 0;
    const maxAttempts = 100;
    while(attempts < maxAttempts) {
        let resultado = '';
        for (let i = 0; i < longitud; i++) {
            resultado += caracteres.charAt(Math.floor(Math.random() * caracteres.length));
        }
        if (!existingCodes.includes(resultado)) {
            return resultado;
        }
        attempts++;
    }
    console.warn("No se pudo generar un código aleatorio único después de", maxAttempts, "intentos.");
    return `TEMP_${Date.now()}`;
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
        if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'A' && e.target.tagName !== 'INPUT') {
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
//       PÁGINA DE CREACIÓN DE INVENTARIO (crear_inventario.html)
// ------------------------------------------------------------
let inventarioCreadoUI = [];

function setupCrearInventario() {
    const formContainer = document.querySelector('#form-crear-inventario');
    const btnAgregar = document.querySelector('#agregar-producto-btn');
    const btnGuardar = document.querySelector('#guardar-inventario-btn');
    const tablaBody = document.querySelector('#inventario-creado-tbody');

    if (!formContainer || !btnAgregar || !btnGuardar || !tablaBody) return;

    const guardado = sessionStorage.getItem('inventarioCreadoUI');
    if (guardado) {
        try {
            inventarioCreadoUI = JSON.parse(guardado);
            if (!Array.isArray(inventarioCreadoUI)) inventarioCreadoUI = [];
        } catch(e) {
            inventarioCreadoUI = [];
            sessionStorage.removeItem('inventarioCreadoUI');
        }
        renderTablaInventarioCreado(tablaBody);
    }

    btnAgregar.addEventListener('click', () => {
        clearFormErrors(formContainer);
        const producto = {};
        let isValid = true;

        const codigoInput = formContainer.querySelector('#codigo');
        const nombreInput = formContainer.querySelector('#nombre');
        const demandaInput = formContainer.querySelector('#demanda');
        const tiempoInput = formContainer.querySelector('#tiempo_entrega');
        const fechaInput = formContainer.querySelector('#fecha_limite');
        const cantidadInput = formContainer.querySelector('#cantidad');

        // Validaciones.
        producto.nombre = nombreInput.value.trim();
        if (!producto.nombre) { showError(nombreInput, 'Obligatorio.'); isValid = false; }
        producto.demanda = parseInt(demandaInput.value);
        if (isNaN(producto.demanda) || producto.demanda < 1 || producto.demanda > 10) { showError(demandaInput, 'Número 1-10.'); isValid = false; }
        producto.tiempo_entrega = parseInt(tiempoInput.value);
        if (isNaN(producto.tiempo_entrega) || producto.tiempo_entrega < 0) { showError(tiempoInput, 'Número >= 0.'); isValid = false; }
        producto.fecha_limite = fechaInput.value.trim();
        const datePattern = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/;
        if (!producto.fecha_limite) { showError(fechaInput, 'Obligatorio.'); isValid = false; }
        else if (!datePattern.test(producto.fecha_limite)) { showError(fechaInput, 'Formato YYYY-MM-DD.'); isValid = false; }
        producto.cantidad = parseInt(cantidadInput.value);
        if (isNaN(producto.cantidad) || producto.cantidad < 0) { showError(cantidadInput, 'Número >= 0.'); isValid = false; }
        const currentCodes = inventarioCreadoUI.map(p => p.codigo);
        producto.codigo = codigoInput.value.trim() || generarCodigoAleatorio(6, currentCodes);
        if (codigoInput.value.trim() && currentCodes.includes(codigoInput.value.trim())) { showError(codigoInput, 'Código ya existe.'); isValid = false; }

        if (isValid) {
            inventarioCreadoUI.push(producto);
            sessionStorage.setItem('inventarioCreadoUI', JSON.stringify(inventarioCreadoUI));
            renderTablaInventarioCreado(tablaBody);
            formContainer.querySelectorAll('input:not([type=button]):not([type=submit])').forEach(input => input.value = '');
            clearFormErrors(formContainer);
            showToast('Producto agregado a la lista.', 'info');
        } else {
            showToast('Corrige los errores en el formulario.', 'error');
        }
    });

    btnGuardar.addEventListener('click', async () => {
        if (inventarioCreadoUI.length === 0) {
            showToast('Agrega al menos un producto antes de guardar.', 'warning');
            return;
        }
        showToast('Guardando inventario...', 'info');
        btnGuardar.disabled = true;
        btnAgregar.disabled = true;
        try {
            const response = await apiFetch('/crear_inventario', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ inventario: inventarioCreadoUI, guardar_csv: true })
            });
            showToast(response.message || 'Inventario guardado y cargado.', 'success', 5000);
            inventarioCreadoUI = [];
            sessionStorage.removeItem('inventarioCreadoUI');
            renderTablaInventarioCreado(tablaBody);
            setTimeout(() => window.location.href = '/', 2000);
        } catch (error) {
            showToast(`Error al guardar: ${error.message}`, 'error');
            btnGuardar.disabled = false;
            btnAgregar.disabled = false;
        }
    });
}

function renderTablaInventarioCreado(tbody) {
    if (!tbody) return;
    tbody.innerHTML = ''; // Limpiar
    inventarioCreadoUI.forEach((producto, index) => {
        const row = tbody.insertRow();
        row.dataset.index = index;
        row.insertCell().textContent = producto.codigo;
        row.insertCell().textContent = producto.nombre;
        row.insertCell().textContent = producto.demanda;
        row.insertCell().textContent = producto.tiempo_entrega;
        row.insertCell().textContent = producto.fecha_limite;
        row.insertCell().textContent = producto.cantidad;
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
    setupCrearInventario();
    setupPedirStock();
    setupPedirProveedor();
    setCopyrightYear();
});