"""Rutas del historial de movimientos y el análisis de demanda."""

import datetime
import io

from flask import Blueprint, current_app, flash, redirect, render_template, request, send_file, url_for

from services import movimientos as logica
from services.inventario import ETIQUETA_MOTIVO, InventarioError

from .comun import (
    alertas_inventario,
    almacen,
    analizar_demanda,
    cargar_inventario,
    inventario_id,
    responder,
    sin_inventario,
)

bp = Blueprint("movimientos", __name__)

RECIENTES = 15  # movimientos que se muestran en la página


@bp.route("/demanda")
def demanda():
    """Demanda por producto: consumo diario, tendencia, ranking y últimos movimientos."""
    productos = cargar_inventario()
    if productos is None:
        return sin_inventario()

    analisis = analizar_demanda(productos)
    alertas, resumen = alertas_inventario(productos, analisis)
    movimientos = almacen().leer_movimientos(inventario_id())

    filas = [
        {
            "codigo": str(p["Código"]),
            "nombre": p["Nombre"],
            "stock": p["Cantidad"],
            "stats": analisis["productos"][str(p["Código"])],
            "alerta": alertas[str(p["Código"])],
        }
        for p in productos
    ]
    filas.sort(key=lambda f: (-f["stats"]["total_ventana"], f["nombre"].lower()))

    nombres = {str(p["Código"]): p["Nombre"] for p in productos}
    ordenados = sorted(enumerate(movimientos), key=lambda x: (x[1]["fecha"], x[0]), reverse=True)
    recientes = [
        {**m, "nombre": nombres.get(m["codigo"], f"{m['codigo']} (ya no está en el inventario)")}
        for _, m in ordenados[:RECIENTES]
    ]

    config = current_app.config
    return render_template(
        "movimientos.html",
        filas=filas,
        analisis=analisis,
        resumen=resumen,
        recientes=recientes,
        total_movimientos=len(movimientos),
        total_salidas=sum(1 for m in movimientos if m["tipo"] == "salida"),
        total_entradas=sum(1 for m in movimientos if m["tipo"] == "entrada"),
        total_mermas=sum(1 for m in movimientos if m["tipo"] == "merma"),
        etiquetas=ETIQUETA_MOTIVO,
        total_eventos=sum(1 for m in movimientos if m["evento"]),
        min_historial=config["MIN_DIAS_HISTORIAL"],
        ventana=config["VENTANA_DEMANDA_DIAS"],
    )


@bp.route("/demanda/importar", methods=["POST"])
def importar():
    """Importa un historial CSV. Reemplaza el historial actual (no se duplican filas)."""
    productos = cargar_inventario()
    if productos is None:
        return sin_inventario()

    destino = url_for("movimientos.demanda")
    archivo = request.files.get("file")
    if archivo is None or archivo.filename == "":
        return responder("No se seleccionó ningún archivo.", 400, destino=destino)
    if not archivo.filename.lower().endswith(".csv"):
        return responder("Por favor, sube un archivo CSV válido (.csv).", 400, destino=destino)

    try:
        movimientos = logica.desde_csv_bytes(
            archivo.read(), [p["Código"] for p in productos], datetime.date.today()
        )
        almacen().reemplazar_movimientos(inventario_id(), movimientos)
    except InventarioError as exc:
        return responder(str(exc), 400, destino=destino, errors=exc.errores)
    except OSError:
        current_app.logger.exception("No se pudo guardar el historial importado")
        return responder("No se pudo guardar el historial. Inténtalo de nuevo.", 500, destino=destino)

    return responder(
        f"Historial importado: {len(movimientos)} movimientos (reemplaza el anterior).",
        200,
        destino=destino,
    )


@bp.route("/demanda/borrar", methods=["POST"])
def borrar():
    """Elimina todo el historial de movimientos del inventario actual."""
    if cargar_inventario() is None:
        return sin_inventario()
    almacen().borrar_movimientos(inventario_id())
    return responder("Historial de movimientos borrado.", 200, destino=url_for("movimientos.demanda"))


@bp.route("/export_movimientos")
def export_movimientos():
    """Descarga el historial en el mismo formato CSV que acepta la importación."""
    if cargar_inventario() is None:
        return sin_inventario()
    movimientos = almacen().leer_movimientos(inventario_id())
    if not movimientos:
        flash("Todavía no hay movimientos registrados para exportar.", "warning")
        return redirect(url_for("movimientos.demanda"))

    # utf-8-sig (con BOM) para que Excel en Windows muestre bien el archivo.
    texto = logica.a_csv_texto(movimientos)
    return send_file(
        io.BytesIO(texto.encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="historial_movimientos.csv",
    )
