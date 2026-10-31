"""Rutas de carga y creación del inventario."""

from flask import Blueprint, current_app, redirect, render_template, request, url_for

from services import inventario as logica
from services import lotes as servicio_lotes
from services.inventario import InventarioError

from .comun import alertas_inventario, cargar_inventario, reemplazar_inventario, responder

bp = Blueprint("inventario", __name__)


@bp.route("/", methods=["GET", "POST"])
def upload_csv():
    """Página de inicio: carga de un CSV de inventario."""
    if request.method == "GET":
        productos = cargar_inventario()
        resumen = alertas_inventario(productos)[1] if productos else None
        return render_template("subir_csv.html", resumen=resumen)

    destino = url_for("inventario.upload_csv")
    archivo = request.files.get("file")
    if archivo is None or archivo.filename == "":
        return responder("No se seleccionó ningún archivo.", 400, destino=destino)

    # Se valida la extensión, no el content_type: según el sistema operativo el
    # navegador puede enviar text/csv, application/vnd.ms-excel, etc.
    if not archivo.filename.lower().endswith(".csv"):
        return responder("Por favor, sube un archivo CSV válido (.csv).", 400, destino=destino)

    try:
        productos = logica.desde_csv_bytes(archivo.read())
    except InventarioError as exc:
        return responder(str(exc), 400, destino=destino, errors=exc.errores)

    try:
        reemplazar_inventario(productos)
    except OSError:
        current_app.logger.exception("No se pudo guardar el inventario subido")
        return responder("No se pudo guardar el inventario. Inténtalo de nuevo.", 500, destino=destino)

    mensaje = f"Archivo CSV cargado con éxito ({len(productos)} productos)."
    sin_fecha = [p["Nombre"] for p in productos if servicio_lotes.unidades_sin_fecha(p)]
    if sin_fecha:
        mostrados = ", ".join(sin_fecha[:3]) + (f" y {len(sin_fecha) - 3} más" if len(sin_fecha) > 3 else "")
        mensaje += (
            f" Atención: falta la fecha de caducidad de {len(sin_fecha)} producto(s) ({mostrados}). "
            "Se cargaron igualmente, pero el sistema te lo seguirá avisando."
        )
    return responder(mensaje, 200, destino=destino, sin_fecha=sin_fecha)


@bp.route("/crear_inventario")
def crear_inventario():
    """Dirección antigua: la gestión manual de productos vive ahora en /productos."""
    return redirect(url_for("productos.productos"))
