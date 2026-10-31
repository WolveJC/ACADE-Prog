"""
Gestión de productos del inventario: agregar, editar y quitar de uno en uno.

Lógica pura (sin Flask). A diferencia de cargar un CSV, que REEMPLAZA todo el
inventario, estas operaciones solo tocan el producto indicado y conservan el
resto, así como el historial de movimientos (que se enlaza por código).

Al agregar, la cantidad y la fecha límite forman el primer lote del producto.
Al editar se corrigen el nombre, el tiempo de entrega y la lista de lotes.
"""

import re
import secrets
import string
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Tuple

from . import lotes as _lotes
from .inventario import InventarioError, Producto, a_entero, validar_fecha, validar_filas

LONGITUD_CODIGO = 6
MAX_CODIGO = 30
MAX_NOMBRE = 80

# Los códigos nuevos usan letras, números, punto y guion (sin espacios ni barras):
# así son seguros en direcciones web y en el CSV. Los cargados desde un CSV no se restringen.
_CODIGO_NUEVO = re.compile(r"^[\w.\-]{1,%d}$" % MAX_CODIGO)
_ALFABETO = string.ascii_uppercase + string.digits


def generar_codigo(
    existentes: Iterable[Any],
    longitud: int = LONGITUD_CODIGO,
    azar: Optional[Callable[[str], str]] = None,
) -> str:
    """Código alfanumérico aleatorio (A-Z, 0-9) que no coincide con ninguno existente."""
    usados = {str(c) for c in existentes}
    elegir = azar or secrets.choice
    for _ in range(100):
        codigo = "".join(elegir(_ALFABETO) for _ in range(longitud))
        if codigo not in usados:
            return codigo
    raise InventarioError(["No se pudo generar un código único. Indica uno manualmente."])


def fila_desde_formulario(form: Mapping[str, Any]) -> Dict[str, Any]:
    """Convierte los campos del formulario en una fila con las columnas del inventario."""
    return {
        "Código": str(form.get("codigo", "")).strip(),
        "Nombre": form.get("nombre", ""),
        "Cantidad": form.get("cantidad", ""),
        "Tiempo entrega(Días)": form.get("tiempo_entrega", ""),
        "Fecha límite": form.get("fecha_limite", ""),
    }


def _validar_uno(fila: Mapping[str, Any]) -> Producto:
    """Valida un producto aislado con las reglas del inventario, con mensajes sin número de fila."""
    try:
        producto = validar_filas([fila], etiqueta="Producto", primera=1)[0]
    except InventarioError as exc:
        limpios = [re.sub(r"^Producto 1: ", "", e) for e in exc.errores]
        raise InventarioError([e[:1].upper() + e[1:] for e in limpios]) from None
    if len(producto["Nombre"]) > MAX_NOMBRE:
        raise InventarioError([f"El nombre no puede superar los {MAX_NOMBRE} caracteres."])
    return producto


def _buscar(productos: List[Producto], codigo: str) -> int:
    for indice, producto in enumerate(productos):
        if str(producto["Código"]) == codigo:
            return indice
    raise InventarioError([f"El producto {codigo} no existe."])


def agregar_producto(
    productos: List[Producto],
    fila: Mapping[str, Any],
    azar: Optional[Callable[[str], str]] = None,
) -> Tuple[List[Producto], Producto]:
    """
    Añade un producto al final, sin tocar los demás. Un código vacío se genera
    solo. Lanza InventarioError con todos los problemas encontrados.
    """
    errores: List[str] = []
    fila = dict(fila)
    codigo = str(fila.get("Código", "")).strip()
    if not codigo:
        codigo = generar_codigo([p["Código"] for p in productos], azar=azar)
        fila["Código"] = codigo
    elif not _CODIGO_NUEVO.match(codigo):
        errores.append(
            f"El código solo puede tener letras, números, punto y guion (máximo {MAX_CODIGO} caracteres)."
        )
    elif any(str(p["Código"]) == codigo for p in productos):
        errores.append(f"El código '{codigo}' ya existe.")

    producto: Optional[Producto] = None
    try:
        producto = _validar_uno(fila)
    except InventarioError as exc:
        errores = exc.errores + errores
    if errores:
        raise InventarioError(errores)
    return productos + [producto], producto


def lotes_desde_formulario(
    fechas: Iterable[Any], cantidades: Iterable[Any]
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Convierte las filas (fecha, cantidad) del editor de lotes en lotes.

    Una fila totalmente vacía se ignora. La cantidad va siempre (>= 0; con 0 el
    lote desaparece) y la fecha es opcional: un lote sin fecha es mercancía sin
    caducidad conocida. Devuelve (lotes, errores).
    """
    lotes: List[Dict[str, Any]] = []
    errores: List[str] = []
    for numero, (fecha, cantidad) in enumerate(zip(fechas, cantidades), start=1):
        if not str(fecha).strip() and not str(cantidad).strip():
            continue
        problemas = []
        try:
            fecha_ok = validar_fecha(fecha)
        except ValueError:
            fecha_ok = ""
            problemas.append("la fecha debe tener formato YYYY-MM-DD válido")
        try:
            cantidad_ok = a_entero(cantidad)
            if cantidad_ok < 0:
                raise ValueError("negativa")
        except ValueError:
            cantidad_ok = 0
            problemas.append("la cantidad debe ser un entero >= 0")
        if problemas:
            errores.append(f"Lote {numero}: {'; '.join(problemas)}.")
        else:
            lotes.append({"Fecha límite": fecha_ok, "Cantidad": cantidad_ok})
    return lotes, errores


def editar_producto(
    productos: List[Producto],
    codigo: str,
    fila: Mapping[str, Any],
    lotes: Iterable[Mapping[str, Any]],
) -> Tuple[List[Producto], Producto]:
    """
    Modifica nombre, tiempo de entrega y lotes de un producto (`lotes` reemplaza
    a los actuales; los de la misma fecha se suman y los de 0 desaparecen).
    El código no cambia (es lo que enlaza el producto con su historial).
    """
    indice = _buscar(productos, codigo)
    # Se valida el nombre y el tiempo de entrega con las reglas de siempre; el stock va en los lotes.
    base = _validar_uno({**fila, "Código": codigo, "Cantidad": "0", "Fecha límite": ""})
    producto = _lotes.construir_producto(codigo, base["Nombre"], base["Tiempo entrega(Días)"], lotes)
    nuevos = list(productos)
    nuevos[indice] = producto
    return nuevos, producto


def eliminar_producto(productos: List[Producto], codigo: str) -> Tuple[List[Producto], Producto]:
    """Quita un producto del inventario (su historial de movimientos se conserva)."""
    indice = _buscar(productos, codigo)
    return productos[:indice] + productos[indice + 1 :], productos[indice]
