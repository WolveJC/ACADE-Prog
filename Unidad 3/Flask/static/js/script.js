document.addEventListener('DOMContentLoaded', function() {
    setupCrearInventarioUI();
    setupPedirStockUI();
    setupPedirProveedorUI();
    setupFileUploadUI(); // Lógica UI para la subida de archivos
});

// ------------------------------------------------------------
// Lógica de Interfaz de Usuario para la página de subida de CSV (subir_csv.html)
// ------------------------------------------------------------
function setupFileUploadUI() {
    const formSubirCsv = document.querySelector('form');
    if (formSubirCsv) {
        formSubirCsv.addEventListener('submit', () => {
            alert('Subiendo archivo...'); // Feedback inmediato al usuario
        });
    }
}

// ------------------------------------------------------------
// Lógica de Interfaz de Usuario y Gestión de Formulario para la página de creación de inventario (crear_inventario.html)
// ------------------------------------------------------------
let inventarioCreadoUI = []; // Mantener temporalmente en el frontend para la UI

function setupCrearInventarioUI() {
    const formAgregarProducto = document.querySelector('#crear-inventario-form');
    const btnAgregarProducto = document.querySelector('#agregar-producto-btn');
    const btnGuardarCsv = document.querySelector('#guardar-inventario-btn');
    const tablaInventario = document.querySelector('#inventario-creado-table tbody');

    if (btnAgregarProducto) {
        btnAgregarProducto.addEventListener('click', (event) => {
            event.preventDefault();
            const nuevoProducto = obtenerDatosFormulario('#crear-inventario-form');
            if (validarProducto(nuevoProducto)) {
                inventarioCreadoUI.push(nuevoProducto);
                renderTablaInventarioUI(tablaInventario);
                formAgregarProducto.reset();
            }
        });
    }

    if (btnGuardarCsv) {
        btnGuardarCsv.addEventListener('click', () => {
            // Cuando se guarda, simplemente enviamos los datos al backend
            // El backend se encargará de crear el CSV y actualizar la sesión.
            const inventarioParaGuardar = { inventario: inventarioCreadoUI };
            // Aquí podrías usar fetch para enviar los datos al backend de forma asíncrona
            // y manejar la respuesta (éxito/error) sin recargar la página.
            console.log('Inventario para guardar:', inventarioParaGuardar);
            alert('Enviando inventario para guardar (la lógica real está en el backend).');
            // Para un envío tradicional, podrías crear un formulario dinámicamente y enviarlo.
        });
    }

    // Cargar el inventario temporal de sessionStorage (opcional para persistencia en la sesión)
    const inventarioGuardadoUI = sessionStorage.getItem('inventarioCreadoUI');
    if (inventarioGuardadoUI) {
        inventarioCreadoUI = JSON.parse(inventarioGuardadoUI);
        renderTablaInventarioUI(tablaInventario);
    }
}

function obtenerDatosFormulario(selectorForm) {
    const form = document.querySelector(selectorForm);
    if (!form) return {};
    const formData = new FormData(form);
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    return data;
}

function validarProducto(producto) {
    if (!producto.nombre || isNaN(parseInt(producto.demanda)) || parseInt(producto.demanda) < 1 || parseInt(producto.demanda) > 10 || isNaN(parseInt(producto.tiempo_entrega)) || !producto.fecha_limite || isNaN(parseInt(producto.cantidad))) {
        alert('Por favor, complete todos los campos correctamente.');
        return false;
    }
    return true;
}

function renderTablaInventarioUI(tbody) {
    tbody.innerHTML = '';
    inventarioCreadoUI.forEach(producto => {
        const row = tbody.insertRow();
        row.insertCell().textContent = producto.codigo || generarCodigoAleatorioUI();
        row.insertCell().textContent = producto.nombre;
        row.insertCell().textContent = producto.demanda;
        row.insertCell().textContent = producto.tiempo_entrega;
        row.insertCell().textContent = producto.fecha_limite;
        row.insertCell().textContent = producto.cantidad;
    });
}

function generarCodigoAleatorioUI(longitud = 6) {
    const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let resultado = '';
    for (let i = 0; i < longitud; i++) {
        resultado += caracteres.charAt(Math.floor(Math.random() * caracteres.length));
    }
    return resultado;
}

// ------------------------------------------------------------
// Lógica de Interfaz de Usuario y Gestión de Formulario para la página de pedido de stock (pedir_stock.html)
// ------------------------------------------------------------
function setupPedirStockUI() {
    const formPedirStock = document.querySelector('#pedir-stock-form');
    if (formPedirStock) {
        formPedirStock.addEventListener('submit', (event) => {
            if (!validarPedidoUI()) {
                event.preventDefault(); // Evitar envío si no se selecciona nada
            } else {
                alert('Realizando pedido de stock...');
            }
        });
    }
}

function validarPedidoUI() {
    const inputs = document.querySelectorAll('#pedir-stock-form input[type="number"]');
    let total = 0;
    inputs.forEach(input => {
        total += parseInt(input.value) || 0;
    });
    if (total === 0) {
        alert("No has seleccionado ningún producto para el pedido de stock.");
        return false;
    }
    return true;
}

// ------------------------------------------------------------
// Lógica de Interfaz de Usuario y Gestión de Formulario para la página de pedido al proveedor (pedir_proveedor.html)
// ------------------------------------------------------------
function setupPedirProveedorUI() {
    const formPedirProveedor = document.querySelector('#pedir-proveedor-form');
    if (formPedirProveedor) {
        formPedirProveedor.addEventListener('submit', (event) => {
            if (!validarPedidoProveedorUI()) {
                event.preventDefault();
            } else {
                alert('Realizando pedido al proveedor...');
            }
        });
    }
}

function validarPedidoProveedorUI() {
    const inputsCantidad = document.querySelectorAll('#pedir-proveedor-form input[name^="pedido_proveedor"]');
    let algunPedido = false;
    inputsCantidad.forEach(input => {
        if (parseInt(input.value) > 0) {
            algunPedido = true;
        }
    });
    if (!algunPedido) {
        alert("No has especificado ninguna cantidad para el pedido al proveedor.");
        return false;
    }
    return true;
}