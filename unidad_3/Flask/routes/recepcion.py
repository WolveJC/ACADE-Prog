"""Rutas de recepción de mercancía (entradas de stock)."""

import datetime

from flask import Blueprint, current_app, render_template, request, url_for

from services import inventario as logica
from services.movimientos import parsear_fecha

from .comun import (
    actualizar_inventario,
    alertas_inventario,
    almacen,
    cargar_inventario,
    inventario_id,
    responder,
    sin_inventario,
)

bp = Blueprint("recepcion", __name__)


@bp.route("/recepcion", methods=["GET", "POST"])
def recepcion():
    """
    Registra la mercancía que llega (p. ej. de un pedido al proveedor): suma al
    stock y guarda cada entrada en el historial. Es un formulario normal: sin
    JavaScript los avisos llegan como mensajes flash tras la redirección.
    """
    productos = cargar_inventario()
    if productos is None:
        return sin_inventario()

    hoy = datetime.date.today()
    destino = url_for("recepcion.recepcion")

    if request.method == "GET":
        alertas, resumen = alertas_inventario(productos)
        return render_template(
            "recepcion.html",
            productos=productos,
            alertas=alertas,
            resumen=resumen,
            hoy=hoy.isoformat(),
        )

    try:
        fecha = parsear_fecha(request.form.get("fecha_movimiento", ""), hoy)
    except ValueError as exc:
        return responder(f"Fecha de recepción inválida: {exc}.", 400, destino=destino)

    recibidos, fechas, errores = logica.parsear_recepcion(
        request.form, [p["Código"] for p in productos], fecha
    )
    if errores:
        return responder(" ".join(errores), 400, destino=destino, errors=errores)
    if not recibidos:
        return responder("Indica la cantidad recibida de al menos un producto.", 400, destino=destino)

    nuevos, detalles = logica.aplicar_recepcion(productos, recibidos, fechas)
    try:
        actualizar_inventario(nuevos)
    except OSError:
        current_app.logger.exception("No se pudo guardar la recepción")
        return responder("No se pudo guardar la recepción. Inténtalo de nuevo.", 500, destino=destino)

    mensaje = (
        f"Recepción registrada: {sum(recibidos.values())} unidades "
        f"de {len(recibidos)} producto(s)."
    )
    sin_fecha = [p["Nombre"] for p in productos if str(p["Código"]) in recibidos and str(p["Código"]) not in fechas]
    if sin_fecha:
        mensaje += (
            f" Atención: falta la fecha de caducidad de {', '.join(sin_fecha)}. "
            "Se registró igualmente, pero el sistema te lo seguirá avisando."
        )

    movimientos = [
        {"fecha": fecha, "codigo": str(p["Código"]), "cantidad": recibidos[str(p["Código"])],
         "tipo": "entrada", "evento": False}
        for p in productos
        if str(p["Código"]) in recibidos
    ]
    try:
        almacen().agregar_movimientos(inventario_id(), movimientos)
    except OSError:
        current_app.logger.exception("No se pudo registrar la entrada en el historial")
        mensaje += " Atención: el stock se actualizó pero no se pudo guardar en el historial."

    return responder(
        mensaje, 200, destino=destino, detalles=detalles, hubo_cambios=True, sin_fecha=sin_fecha
    )
