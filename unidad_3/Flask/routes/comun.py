"""Utilidades compartidas por los blueprints."""

import datetime
import threading
from typing import Any, Dict, List, Optional, Tuple

from flask import current_app, flash, jsonify, redirect, request, session, url_for

from services import alertas as servicio_alertas
from services import demanda as servicio_demanda
from services import lotes as servicio_lotes
from services.almacenamiento import AlmacenInventario
from services.inventario import Producto

CLAVE_SESION = "inventario_id"


def almacen() -> AlmacenInventario:
    return current_app.extensions["almacen"]


def inventario_id() -> Optional[str]:
    return session.get(CLAVE_SESION)


_BLOQUEO_DESCARTE = threading.Lock()
MAX_PRODUCTOS_EN_AVISO = 5


def cargar_inventario() -> Optional[List[Producto]]:
    """
    Inventario de la sesión actual, o None si no hay (o ya fue limpiado).
    Antes de devolverlo descarta los lotes vencidos (si está activado).
    """
    inv_id = inventario_id()
    if not inv_id:
        return None
    productos = almacen().cargar(inv_id)
    if productos is None:
        session.pop(CLAVE_SESION, None)
        return None
    if current_app.config["DESCARTE_AUTOMATICO_VENCIDOS"]:
        productos = _descartar_vencidos(inv_id, productos)
    return productos


def _descartar_vencidos(inv_id: str, productos: List[Producto]) -> List[Producto]:
    """
    Quita del stock los lotes cuya fecha límite ya pasó y los registra como
    mermas por vencimiento, con la fecha de hoy (el día en que el sistema los
    retira). Avisa al usuario, porque el stock cambia sin que él haga nada.
    """
    hoy = datetime.date.today()
    if not any(servicio_lotes.esta_vencido(l, hoy) for p in productos for l in servicio_lotes.lotes_de(p)):
        return productos  # lo habitual: nada que hacer, sin bloqueo ni escrituras

    with _BLOQUEO_DESCARTE:
        # Se vuelve a leer: otra petición pudo haberlo descartado mientras se esperaba el bloqueo.
        productos = almacen().cargar(inv_id) or productos
        nuevos, descartes = servicio_lotes.descartar_vencidos(productos, hoy)
        if not descartes:
            return productos
        try:
            almacen().guardar(inv_id, nuevos)
            almacen().agregar_movimientos(
                inv_id,
                [
                    {"fecha": hoy, "codigo": d["codigo"], "cantidad": d["cantidad"],
                     "tipo": "merma", "evento": False, "motivo": "vencido"}
                    for d in descartes
                ],
            )
        except OSError:
            current_app.logger.exception("No se pudieron descartar los lotes vencidos")
            return productos

    flash(_aviso_descarte(descartes), "warning")
    return nuevos


def _aviso_descarte(descartes: List[Dict[str, Any]]) -> str:
    total = sum(d["cantidad"] for d in descartes)
    detalle = ", ".join(
        f"{d['nombre']} ({d['cantidad']} u., vencidas el {d['fecha_limite']})"
        for d in descartes[:MAX_PRODUCTOS_EN_AVISO]
    )
    resto = len(descartes) - MAX_PRODUCTOS_EN_AVISO
    if resto > 0:
        detalle += f" y {resto} lote(s) más"
    return (
        f"El sistema descartó automáticamente {total} unidad(es) vencidas: {detalle}. "
        "Quedaron registradas como mermas por vencimiento."
    )


def reemplazar_inventario(productos: List[Producto]) -> None:
    """
    Carga un inventario nuevo (subido o creado a mano) para esta sesión.

    Se reutiliza el identificador existente: así el historial de movimientos
    sobrevive al cambio de inventario (los códigos de producto son los que
    lo enlazan). Un pedido a proveedor pendiente sí se descarta.
    """
    inv_id = inventario_id() or almacen().nuevo_id()
    almacen().guardar(inv_id, productos)
    almacen().descartar_pedido(inv_id)
    session[CLAVE_SESION] = inv_id
    session.permanent = True  # la cookie dura PERMANENT_SESSION_LIFETIME, no solo la pestaña


def actualizar_inventario(productos: List[Producto]) -> None:
    """Persiste cambios sobre el inventario actual de la sesión."""
    almacen().guardar(inventario_id(), productos)


def analizar_demanda(productos: List[Producto]) -> Dict[str, Any]:
    """Estadísticas de demanda del inventario actual a partir de su historial."""
    config = current_app.config
    return servicio_demanda.analizar(
        almacen().leer_movimientos(inventario_id()),
        [p["Código"] for p in productos],
        datetime.date.today(),
        ventana=config["VENTANA_DEMANDA_DIAS"],
        min_historial=config["MIN_DIAS_HISTORIAL"],
    )


def alertas_inventario(
    productos: List[Producto], analisis: Optional[Dict[str, Any]] = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Alertas por producto (indexadas por código) y su resumen, con la fecha de hoy.
    Si ya se calculó el análisis de demanda se puede pasar para no repetirlo.
    """
    if analisis is None:
        analisis = analizar_demanda(productos)
    alertas = servicio_alertas.evaluar_inventario(
        productos,
        datetime.date.today(),
        current_app.config["DIAS_AVISO_VENCIMIENTO"],
        analisis,
        current_app.config["DIAS_SEGURIDAD"],
    )
    return alertas, servicio_alertas.resumir(alertas)


def sin_inventario():
    """JSON 409 para el JS; aviso (toast) y redirección al inicio para el navegador."""
    return responder(
        "No hay inventario cargado. Sube o crea un archivo CSV.",
        409,
        categoria="warning",
        destino=url_for("inventario.upload_csv"),
    )


def quiere_json() -> bool:
    """True si el cliente es nuestro JS (fetch) y espera una respuesta JSON."""
    return (
        request.is_json
        or request.headers.get("X-Requested-With") == "XMLHttpRequest"
        or request.accept_mimetypes.best == "application/json"
    )


def responder(
    mensaje: str,
    estado: int = 200,
    categoria: Optional[str] = None,
    destino: Optional[str] = None,
    **extra: Any,
):
    """
    Respuesta coherente para clientes JS y navegadores sin JS.

    - Cliente JS: JSON {"message": ..., **extra} con el código de estado real.
    - Sin JS: mensaje flash (se muestra como toast) y redirección a `destino`.
    """
    if quiere_json():
        return jsonify({"message": mensaje, **extra}), estado
    flash(mensaje, categoria or ("error" if estado >= 400 else "success"))
    return redirect(destino or request.url)
