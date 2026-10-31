"""Rutas de mermas: mercancía que se descarta de un lote (vencida, dañada, rota...)."""

import datetime

from flask import Blueprint, current_app, render_template, request, url_for

from services import inventario as logica
from services import lotes as servicio_lotes
from services.inventario import InventarioError
from services.movimientos import parsear_fecha

from .comun import (
    actualizar_inventario,
    almacen,
    cargar_inventario,
    inventario_id,
    responder,
    sin_inventario,
)

bp = Blueprint("mermas", __name__)


def _lineas(productos, hoy, dias_aviso):
    """Una línea por lote, para que cada descarte se haga sobre el lote correcto."""
    lineas = []
    for producto in productos:
        for lote in servicio_lotes.lotes_de(producto):
            fecha = lote["Fecha límite"]
            dias = (datetime.date.fromisoformat(fecha) - hoy).days if fecha else None
            lineas.append(
                {
                    "producto": producto,
                    "lote": lote,
                    "clave": f"{producto['Código']}@{fecha}",
                    "dias": dias,
                    "vencido": dias is not None and dias < 0,
                    "por_vencer": dias is not None and 0 <= dias <= dias_aviso,
                }
            )
    return lineas


@bp.route("/mermas", methods=["GET", "POST"])
def mermas():
    """
    Da de baja mercancía que no se vendió. Baja el stock del lote elegido y queda
    en el historial como merma: NO cuenta como demanda. Los lotes que llegan a su
    fecha límite los descarta el propio sistema; aquí se registra el resto (rotura,
    daño...). Con `?preparar=vencidos` el formulario llega con lo vencido rellenado
    (solo puede haberlo si el descarte automático está desactivado).
    """
    productos = cargar_inventario()
    if productos is None:
        return sin_inventario()

    hoy = datetime.date.today()
    destino = url_for("mermas.mermas")

    if request.method == "GET":
        lineas = _lineas(productos, hoy, current_app.config["DIAS_AVISO_VENCIMIENTO"])
        return render_template(
            "mermas.html",
            lineas=lineas,
            unidades_vencidas=sum(l["lote"]["Cantidad"] for l in lineas if l["vencido"]),
            hoy=hoy.isoformat(),
            preparar=request.args.get("preparar") == "vencidos",
            etiquetas=logica.ETIQUETA_MOTIVO,
        )

    try:
        fecha = parsear_fecha(request.form.get("fecha_movimiento", ""), hoy)
    except ValueError as exc:
        return responder(f"Fecha de la baja inválida: {exc}.", 400, destino=destino)

    descartes, motivos, errores = logica.parsear_merma(request.form, [p["Código"] for p in productos])
    if errores:
        return responder(" ".join(errores), 400, destino=destino, errors=errores)
    if not descartes:
        return responder("Indica la cantidad a descartar de al menos un lote.", 400, destino=destino)

    try:
        nuevos, detalles = logica.aplicar_merma(productos, descartes)
    except InventarioError as exc:
        return responder(str(exc), 400, destino=destino, errors=exc.errores)

    try:
        actualizar_inventario(nuevos)
    except OSError:
        current_app.logger.exception("No se pudo guardar la merma")
        return responder("No se pudo guardar la baja. Inténtalo de nuevo.", 500, destino=destino)

    mensaje = (
        f"Mermas registradas: {sum(descartes.values())} unidades "
        f"de {len({c for c, _ in descartes})} producto(s). No cuentan como demanda."
    )
    movimientos = [
        {"fecha": fecha, "codigo": codigo, "cantidad": cantidad, "tipo": "merma",
         "evento": False, "motivo": motivos[(codigo, fecha_lote)]}
        for (codigo, fecha_lote), cantidad in descartes.items()
    ]
    try:
        almacen().agregar_movimientos(inventario_id(), movimientos)
    except OSError:
        current_app.logger.exception("No se pudo registrar la merma en el historial")
        mensaje += " Atención: el stock se actualizó pero no se pudo guardar en el historial."

    return responder(mensaje, 200, destino=destino, detalles=detalles, hubo_cambios=True)
