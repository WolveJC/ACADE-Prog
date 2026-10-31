"""Rutas de gestión de productos: agregar, editar y quitar sin tocar el resto del inventario."""

from typing import Any, Dict, List, Optional

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from services import lotes as servicio_lotes
from services import productos as logica
from services.inventario import InventarioError, Producto

from .comun import (
    actualizar_inventario,
    alertas_inventario,
    almacen,
    cargar_inventario,
    inventario_id,
    reemplazar_inventario,
    responder,
    sin_inventario,
)

bp = Blueprint("productos", __name__)

FILAS_LOTES_VACIAS = 2  # filas en blanco del editor de lotes, para añadir uno nuevo

VALORES_INICIALES = {"codigo": "", "nombre": "", "cantidad": "0", "tiempo_entrega": "0", "fecha_limite": ""}


def _aviso_sin_fecha(producto: Producto) -> str:
    """Aviso que acompaña a cualquier registro que deje mercancía sin fecha de caducidad."""
    if not servicio_lotes.unidades_sin_fecha(producto):
        return ""
    return (
        f" Atención: «{producto['Nombre']}» no tiene fecha de caducidad. Se registró igualmente, "
        "pero el sistema te lo seguirá avisando hasta que la indiques."
    )


def _valores_de(producto: Producto) -> Dict[str, str]:
    return {
        "codigo": str(producto["Código"]),
        "nombre": producto["Nombre"],
        "cantidad": str(producto["Cantidad"]),
        "tiempo_entrega": str(producto["Tiempo entrega(Días)"]),
        "fecha_limite": producto["Fecha límite"],
    }


def _pagina(
    lista: Optional[List[Producto]],
    valores: Optional[Dict[str, Any]] = None,
    errores: Optional[List[str]] = None,
    estado: int = 200,
):
    """Página de productos. Con errores se vuelve a mostrar el formulario con lo que se escribió."""
    lista = lista or []
    alertas, _ = alertas_inventario(lista) if lista else ({}, None)
    return (
        render_template(
            "productos.html",
            productos=lista,
            alertas=alertas,
            valores={**VALORES_INICIALES, **(valores or {})},
            errores=errores or [],
        ),
        estado,
    )


@bp.route("/productos", methods=["GET", "POST"])
def productos():
    """
    Lista el inventario y permite agregar un producto. Funciona aunque todavía no
    haya inventario: el primer producto lo crea. Agregar NUNCA reemplaza lo existente.
    """
    lista = cargar_inventario()  # None = aún no hay inventario
    if request.method == "GET":
        return _pagina(lista)

    existentes = lista or []
    try:
        nuevos, producto = logica.agregar_producto(existentes, logica.fila_desde_formulario(request.form))
    except InventarioError as exc:
        return _pagina(lista, valores=request.form, errores=exc.errores, estado=400)

    try:
        if lista is None:
            reemplazar_inventario(nuevos)  # primer producto: se crea el inventario
        else:
            actualizar_inventario(nuevos)
    except OSError:
        current_app.logger.exception("No se pudo guardar el producto")
        return _pagina(lista, valores=request.form,
                       errores=["No se pudo guardar el producto. Inténtalo de nuevo."], estado=500)

    mensaje = f"Producto «{producto['Nombre']}» agregado con el código {producto['Código']}."
    previos = sum(1 for m in almacen().leer_movimientos(inventario_id()) if m["codigo"] == producto["Código"])
    if previos:
        mensaje += f" Atención: ese código ya tenía {previos} movimiento(s) en el historial y quedaron enlazados."
    mensaje += _aviso_sin_fecha(producto)
    flash(mensaje, "success")
    return redirect(url_for("productos.productos"))


def _producto_o_none(lista: List[Producto], codigo: str) -> Optional[Producto]:
    return next((p for p in lista if str(p["Código"]) == codigo), None)


@bp.route("/productos/<path:codigo>/editar", methods=["GET", "POST"])
def editar(codigo: str):
    """Edita nombre, stock, tiempo de entrega y fecha límite. El código no se puede cambiar."""
    lista = cargar_inventario()
    if lista is None:
        return sin_inventario()
    actual = _producto_o_none(lista, codigo)
    if actual is None:
        return responder(f"El producto {codigo} no existe.", 404, categoria="warning",
                         destino=url_for("productos.productos"))

    def pagina(valores, filas_lotes, errores=None, estado=200):
        return render_template("producto_editar.html", codigo=codigo, valores=valores,
                               lotes_filas=filas_lotes, errores=errores or []), estado

    if request.method == "GET":
        filas = [(l["Fecha límite"], l["Cantidad"]) for l in servicio_lotes.lotes_de(actual)]
        return pagina(_valores_de(actual), filas + [("", "")] * FILAS_LOTES_VACIAS)

    fechas = request.form.getlist("lote_fecha")
    cantidades = request.form.getlist("lote_cantidad")
    lotes, errores = logica.lotes_desde_formulario(fechas, cantidades)
    try:
        nuevos, producto = logica.editar_producto(lista, codigo, logica.fila_desde_formulario(request.form), lotes)
    except InventarioError as exc:
        errores = exc.errores + errores
    if errores:
        return pagina(request.form, list(zip(fechas, cantidades)), errores, 400)
    try:
        actualizar_inventario(nuevos)
    except OSError:
        current_app.logger.exception("No se pudo guardar el producto editado")
        return pagina(request.form, list(zip(fechas, cantidades)),
                      ["No se pudo guardar el producto. Inténtalo de nuevo."], 500)

    flash(f"Producto «{producto['Nombre']}» actualizado." + _aviso_sin_fecha(producto), "success")
    return redirect(url_for("productos.productos"))


@bp.route("/productos/<path:codigo>/eliminar", methods=["POST"])
def eliminar(codigo: str):
    """Quita un producto del inventario. Su historial de movimientos se conserva."""
    lista = cargar_inventario()
    if lista is None:
        return sin_inventario()
    destino = url_for("productos.productos")
    try:
        nuevos, quitado = logica.eliminar_producto(lista, codigo)
    except InventarioError as exc:
        return responder(str(exc), 404, categoria="warning", destino=destino)
    try:
        actualizar_inventario(nuevos)
    except OSError:
        current_app.logger.exception("No se pudo quitar el producto")
        return responder("No se pudo quitar el producto. Inténtalo de nuevo.", 500, destino=destino)
    return responder(
        f"Producto «{quitado['Nombre']}» quitado del inventario. Su historial de movimientos se conserva.",
        200, destino=destino,
    )
