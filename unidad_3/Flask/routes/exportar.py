"""Rutas de exportación del inventario actual."""

import io

import pandas as pd
from flask import Blueprint, flash, jsonify, redirect, send_file, url_for

from services.inventario import COLUMNAS
from services.lotes import a_filas

from .comun import cargar_inventario

bp = Blueprint("exportar", __name__)


@bp.route("/export_json")
def export_json():
    productos = cargar_inventario()
    if productos is None:
        return jsonify({"message": "No hay datos de inventario para exportar."}), 404
    return jsonify(productos)


@bp.route("/export_csv")
def export_csv():
    productos = cargar_inventario()
    if productos is None:
        flash("No hay datos de inventario para exportar.", "warning")
        return redirect(url_for("inventario.upload_csv"))

    # utf-8-sig (con BOM) para que Excel en Windows muestre bien las tildes.
    texto = pd.DataFrame(a_filas(productos), columns=COLUMNAS).to_csv(index=False)  # una fila por lote
    return send_file(
        io.BytesIO(texto.encode("utf-8-sig")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="inventario_exportado.csv",
    )
