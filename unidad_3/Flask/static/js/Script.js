// Muestra una alerta subir el archivo
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    form.addEventListener("submit", function () {
        alert("¡Archivo subido con éxito!");
    });
});

// Validar campos
function validarPedido() {
    const inputs = document.querySelectorAll('input[type="number"]');
    let total = 0;

    inputs.forEach(input => {
        const cantidad = parseInt(input.value) || 0;
        total += cantidad;
    });

    if (total === 0) {
        alert("No has seleccionado ningún producto. Por favor, selecciona al menos uno.");
        return false;
    }
    return true;
    }
