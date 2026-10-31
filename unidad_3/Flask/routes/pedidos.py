"""Rutas de pedidos: stock interno (con registro de movimientos) y proveedor (con PDF)."""

import datetime
import io

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from fpdf.errors import FPDFException

from services import inventario as logica
from services.movimientos import a_booleano, parsear_fecha
from services.pdf import generar_pdf_pedido

from .comun import (
    actualizar_inventario,
    alertas_inventario,
    almacen,
    cargar_inventario,
    inventario_id,
    sin_inventario,
)

bp = Blueprint("pedidos", __name__)


@bp.route("/pedir_stock", methods=["GET", "POST"])
def pedir_stock():
    """
    Pedido interno (retirada de stock). Descuenta existencias y registra cada
    retirada en el historial de movimientos (de donde sale la demanda real).
    """
    productos = cargar_inventario()
    if productos is None:
        return sin_inventario()

    hoy = datetime.date.today()
    if request.method == "GET":
        alertas, resumen = alertas_inventario(productos)
        return render_template(
            "pedir_stock.html",
            productos_stock=productos,
            alertas=alertas,
            resumen=resumen,
            hoy=hoy.isoformat(),
        )

    pedido, errores = logica.parsear_pedido_stock(request.form)
    if errores:
        return jsonify({"message": " ".join(errores), "errors": errores}), 400
    if not pedido:
        return jsonify({"message": "No se especificó ninguna cantidad válida."}), 400

    try:
        fecha = parsear_fecha(request.form.get("fecha_movimiento", ""), hoy)
        evento = a_booleano(request.form.get("es_evento", ""))
    except ValueError as exc:
        return jsonify({"message": f"Fecha o evento del pedido inválido: {exc}."}), 400

    aplicados = logica.pedidos_aplicables(productos, pedido)
    nuevos, mensajes, hubo_cambios = logica.aplicar_pedido_stock(productos, pedido)
    mensaje = "Proceso de pedido de stock completado."

    if hubo_cambios:
        try:
            actualizar_inventario(nuevos)
        except OSError:
            current_app.logger.exception("No se pudo guardar el inventario actualizado")
            return jsonify({"message": "No se pudo guardar el pedido. Inténtalo de nuevo."}), 500

        movimientos = [
            {"fecha": fecha, "codigo": str(p["Código"]), "cantidad": aplicados[str(p["Código"])],
             "tipo": "salida", "evento": evento}
            for p in productos
            if str(p["Código"]) in aplicados
        ]
        try:
            almacen().agregar_movimientos(inventario_id(), movimientos)
        except OSError:
            current_app.logger.exception("No se pudo registrar el historial de movimientos")
            mensaje += " Atención: el stock se actualizó pero no se pudo guardar en el historial."

    return jsonify({"message": mensaje, "detalles": mensajes, "hubo_cambios": hubo_cambios}), 200


@bp.route("/pedir_proveedor", methods=["GET", "POST"])
def pedir_proveedor():
    """Recopila y valida el pedido a proveedor; luego redirige a la descarga del PDF."""
    productos = cargar_inventario()
    if productos is None:
        return sin_inventario()

    if request.method == "GET":
        alertas, resumen = alertas_inventario(productos)
        return render_template(
            "pedir_proveedor.html", productos_proveedor=productos, alertas=alertas, resumen=resumen
        )

    pedido, errores = logica.validar_pedido_proveedor(productos, request.form)
    if errores:
        return jsonify({"message": "Errores en el formulario. " + " ".join(errores), "errors": errores}), 400
    if not pedido:
        return jsonify({"message": "No se seleccionaron productos válidos."}), 400

    try:
        almacen().guardar_pedido(inventario_id(), pedido)
    except OSError:
        current_app.logger.exception("No se pudo guardar el pedido a proveedor")
        return jsonify({"message": "No se pudo preparar el pedido. Inténtalo de nuevo."}), 500

    return jsonify(
        {
            "message": "Pedido listo para generar PDF.",
            "redirect_url": url_for("pedidos.generar_pdf_proveedor"),
        }
    ), 200


@bp.route("/generar_pdf_proveedor", methods=["GET"])
def generar_pdf_proveedor():
    """Descarga el PDF del último pedido a proveedor preparado."""
    pedido = almacen().leer_pedido(inventario_id())
    if not pedido:
        flash("No hay ningún pedido pendiente para generar el PDF.", "warning")
        return redirect(url_for("pedidos.pedir_proveedor"))

    try:
        contenido, nombre = generar_pdf_pedido(pedido, dir_fuentes=current_app.config["DIR_FUENTES"])
    except (FPDFException, RuntimeError, OSError, ValueError):
        current_app.logger.exception("Error al generar el PDF")
        flash("Error al generar el archivo PDF.", "error")
        return redirect(url_for("pedidos.pedir_proveedor"))

    almacen().descartar_pedido(inventario_id())  # solo tras generar con éxito
    return send_file(
        io.BytesIO(contenido),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=nombre,
    )
