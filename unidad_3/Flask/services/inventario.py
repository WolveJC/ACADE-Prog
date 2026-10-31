"""
Lógica de negocio del inventario: lectura, validación y reglas de pedidos.

Este módulo no depende de Flask, por lo que se puede probar de forma aislada.
Todas las funciones trabajan con "productos": una lista de diccionarios cuyas
claves son exactamente las de `COLUMNAS`.
"""

import datetime
import io
import math
import re
from typing import Any, Dict, Iterable, List, Mapping, Tuple

import pandas as pd
from pandas.errors import EmptyDataError, ParserError

from . import lotes as _lotes

# --------------------------------------------------------------------------
#  Esquema
# --------------------------------------------------------------------------
COLUMNAS: List[str] = [
    "Código",
    "Nombre",
    "Cantidad",
    "Tiempo entrega(Días)",
    "Fecha límite",
]

MAX_ERRORES_MOSTRADOS = 5

Producto = Dict[str, Any]

MOTIVOS_MERMA = ("vencido", "danado", "otro")
ETIQUETA_MOTIVO = {"vencido": "vencido", "danado": "dañado", "otro": "otro motivo"}


class InventarioError(ValueError):
    """Error de validación con la lista completa de problemas encontrados."""

    def __init__(self, errores: List[str]):
        self.errores = list(errores)
        visibles = self.errores[:MAX_ERRORES_MOSTRADOS]
        texto = " ".join(visibles)
        restantes = len(self.errores) - len(visibles)
        if restantes > 0:
            texto += f" (y {restantes} error(es) más)"
        super().__init__(texto)


# --------------------------------------------------------------------------
#  Conversión y validación de valores
# --------------------------------------------------------------------------
def a_entero(valor: Any) -> int:
    """Convierte a int aceptando 7, "7" y "7.0". Lanza ValueError si no es entero."""
    if isinstance(valor, bool):
        raise ValueError("booleano no permitido")
    if isinstance(valor, int):
        return valor
    texto = str(valor).strip()
    if not texto:
        raise ValueError("vacío")
    numero = float(texto)
    if not numero.is_integer():  # también rechaza nan e inf
        raise ValueError("no es entero")
    return int(numero)


def validar_fecha(valor: Any) -> str:
    """Devuelve la fecha en formato YYYY-MM-DD (o "" si viene vacía)."""
    texto = str(valor if valor is not None else "").strip()
    if not texto:
        return ""
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", texto):
        raise ValueError("formato de fecha")
    datetime.datetime.strptime(texto, "%Y-%m-%d")
    return texto


def validar_filas(
    filas: List[Mapping[str, Any]], etiqueta: str = "Fila", primera: int = 2
) -> List[Producto]:
    """
    Valida y normaliza filas con las claves de `COLUMNAS`.

    Cada fila es un producto con un lote (su Cantidad y su Fecha límite). Si el
    mismo código aparece en varias filas son lotes del mismo producto: deben
    coincidir en Nombre y Tiempo de entrega, y las que tengan la misma fecha se
    suman. Una fila con Cantidad 0 deja el producto sin stock (sin lote).

    Devuelve productos con tipos correctos y sus lotes (ver services/lotes.py).
    Si hay problemas, lanza InventarioError con todos los errores, indicando la
    fila de cada uno.
    """
    if not filas:
        raise InventarioError(["El inventario no contiene ningún producto."])

    errores: List[str] = []
    grupos: Dict[str, Dict[str, Any]] = {}  # código -> datos del producto y sus lotes

    for numero, fila in enumerate(filas, start=primera):
        prefijo = f"{etiqueta} {numero}:"
        faltantes = [c for c in COLUMNAS if c not in fila]
        if faltantes:
            errores.append(f"{prefijo} faltan los campos {', '.join(faltantes)}.")
            continue

        errores_fila: List[str] = []
        codigo = str(fila["Código"]).strip()
        nombre = str(fila["Nombre"]).strip()

        if not codigo:
            errores_fila.append("el código es obligatorio")
        if not nombre:
            errores_fila.append("el nombre es obligatorio")

        enteros: Dict[str, int] = {}
        reglas = {
            "Cantidad": "Cantidad debe ser un entero >= 0",
            "Tiempo entrega(Días)": "Tiempo de entrega debe ser un entero >= 0",
        }
        for columna, mensaje in reglas.items():
            try:
                valor = a_entero(fila[columna])
                if valor < 0:
                    raise ValueError("fuera de rango")
                enteros[columna] = valor
            except ValueError:
                errores_fila.append(mensaje)

        try:
            fecha = validar_fecha(fila["Fecha límite"])
        except ValueError:
            fecha = ""
            errores_fila.append("Fecha límite debe tener formato YYYY-MM-DD válido")

        if errores_fila:
            errores.append(f"{prefijo} {'; '.join(errores_fila)}.")
            continue

        tiempo = enteros["Tiempo entrega(Días)"]
        lote = {"Fecha límite": fecha, "Cantidad": enteros["Cantidad"]}
        grupo = grupos.get(codigo)
        if grupo is None:
            grupos[codigo] = {"nombre": nombre, "tiempo": tiempo, "lotes": [lote], "fila": numero}
            continue

        conflictos = []
        if nombre != grupo["nombre"]:
            conflictos.append(f"el nombre '{nombre}' no coincide con '{grupo['nombre']}' (fila {grupo['fila']})")
        if tiempo != grupo["tiempo"]:
            conflictos.append(f"el tiempo de entrega no coincide con el de la fila {grupo['fila']}")
        if conflictos:
            errores.append(
                f"{prefijo} el código '{codigo}' está repetido (varias filas con el mismo código "
                f"son lotes del mismo producto) pero {'; '.join(conflictos)}."
            )
        else:
            grupo["lotes"].append(lote)

    if errores:
        raise InventarioError(errores)
    return [
        _lotes.construir_producto(codigo, g["nombre"], g["tiempo"], g["lotes"])
        for codigo, g in grupos.items()
    ]


# --------------------------------------------------------------------------
#  Construcción del inventario desde distintas fuentes
# --------------------------------------------------------------------------
def leer_tabla_csv(contenido: bytes) -> pd.DataFrame:
    """
    Decodifica y parsea un CSV subido por el usuario (todo como texto).

    Tolera BOM y codificación latin-1 (típico de Excel en Windows) y los
    separadores coma, punto y coma y tabulador.
    """
    if not contenido.strip():
        raise InventarioError(["El archivo CSV está vacío."])

    try:
        texto = contenido.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = contenido.decode("latin-1")

    lineas = texto.splitlines()
    cabecera = lineas[0] if lineas else ""
    delimitador = max(",;\t", key=cabecera.count) if any(d in cabecera for d in ",;\t") else ","

    try:
        df = pd.read_csv(io.StringIO(texto), sep=delimitador, dtype=str, keep_default_na=False)
    except EmptyDataError:
        raise InventarioError(["El archivo CSV está vacío."]) from None
    except ParserError as exc:
        raise InventarioError(["Error al procesar el archivo CSV. Verifique el formato."]) from exc

    df.columns = [str(c).strip() for c in df.columns]
    return df


def desde_csv_bytes(contenido: bytes) -> List[Producto]:
    """Lee el CSV de inventario subido. Ignora columnas adicionales."""
    df = leer_tabla_csv(contenido)
    faltantes = [c for c in COLUMNAS if c not in df.columns]
    if faltantes:
        raise InventarioError(
            [
                f"El CSV debe contener las columnas: {', '.join(COLUMNAS)}. "
                f"Faltan: {', '.join(faltantes)}."
            ]
        )
    return validar_filas(df[COLUMNAS].to_dict(orient="records"))


# --------------------------------------------------------------------------
#  Pedido de stock interno
# --------------------------------------------------------------------------
def parsear_pedido_stock(form: Mapping[str, Any]) -> Tuple[Dict[str, int], List[str]]:
    """Extrae {código: cantidad} de los campos `pedido_stock[<código>]`."""
    prefijo = "pedido_stock["
    pedido: Dict[str, int] = {}
    errores: List[str] = []
    for clave, valor in form.items():
        if not (clave.startswith(prefijo) and clave.endswith("]")):
            continue
        codigo = clave[len(prefijo) : -1]
        if str(valor).strip() == "":
            continue
        try:
            cantidad = a_entero(valor)
        except ValueError:
            errores.append(f"Producto {codigo}: cantidad inválida.")
            continue
        if cantidad < 0:
            errores.append(f"Producto {codigo}: cantidad negativa.")
        elif cantidad > 0:
            pedido[codigo] = cantidad
    return pedido, errores


def pedidos_aplicables(productos: List[Producto], pedido: Dict[str, int]) -> Dict[str, int]:
    """Parte del pedido que se puede surtir: el producto existe y hay stock suficiente."""
    stock = {str(p["Código"]): int(p["Cantidad"]) for p in productos}
    return {c: q for c, q in pedido.items() if c in stock and q <= stock[c]}


def aplicar_pedido_stock(
    productos: List[Producto], pedido: Dict[str, int]
) -> Tuple[List[Producto], List[str], bool]:
    """
    Descuenta el stock pedido (solo si hay existencias suficientes), tomándolo
    siempre del lote que caduca antes. No modifica la lista original.
    """
    mensajes: List[str] = []
    hubo_cambios = False
    actualizados = list(productos)

    existentes = {str(p["Código"]) for p in actualizados}
    for codigo in pedido:
        if codigo not in existentes:
            mensajes.append(f"Producto {codigo} no encontrado.")
    aplicables = pedidos_aplicables(actualizados, pedido)

    for indice, producto in enumerate(actualizados):
        codigo = str(producto["Código"])
        if codigo not in pedido:
            continue
        cantidad_pedida = pedido[codigo]

        if codigo in aplicables:
            actualizados[indice] = _lotes.consumir_fefo(producto, cantidad_pedida)
            mensajes.append(
                f"Pedido de {cantidad_pedida} {producto['Nombre']} OK. "
                f"Nuevo stock: {actualizados[indice]['Cantidad']}"
            )
            hubo_cambios = True
        else:
            mensajes.append(
                f"Stock insuficiente de {producto['Nombre']} "
                f"(disp: {int(producto['Cantidad'])}) para pedir {cantidad_pedida}."
            )
    return actualizados, mensajes, hubo_cambios


# --------------------------------------------------------------------------
#  Recepción de mercancía (entradas de stock)
# --------------------------------------------------------------------------
def parsear_recepcion(
    form: Mapping[str, Any], codigos_validos: Iterable[str], fecha_recepcion: datetime.date
) -> Tuple[Dict[str, int], Dict[str, str], List[str]]:
    """
    Extrae lo recibido de los campos `recepcion_cantidad[<código>]` y, para
    cada producto, la fecha límite opcional de ese lote en
    `recepcion_fecha[<código>]`.

    Devuelve ({código: cantidad}, {código: fecha}, errores). Las líneas vacías
    o en 0 se ignoran; una fecha sin cantidad también.
    """
    prefijo = "recepcion_cantidad["
    validos = {str(c) for c in codigos_validos}
    recibidos: Dict[str, int] = {}
    fechas: Dict[str, str] = {}
    errores: List[str] = []

    for clave, valor in form.items():
        if not (clave.startswith(prefijo) and clave.endswith("]")):
            continue
        codigo = clave[len(prefijo) : -1]
        if str(valor).strip() == "":
            continue
        if codigo not in validos:
            errores.append(f"Producto {codigo} no encontrado.")
            continue
        try:
            cantidad = a_entero(valor)
        except ValueError:
            errores.append(f"Producto {codigo}: cantidad recibida inválida.")
            continue
        if cantidad < 0:
            errores.append(f"Producto {codigo}: la cantidad recibida no puede ser negativa.")
            continue
        if cantidad == 0:
            continue
        recibidos[codigo] = cantidad

        texto_fecha = str(form.get(f"recepcion_fecha[{codigo}]", "")).strip()
        if texto_fecha:
            try:
                fecha = validar_fecha(texto_fecha)
            except ValueError:
                errores.append(f"Producto {codigo}: la fecha límite debe tener formato YYYY-MM-DD válido.")
                continue
            if fecha < fecha_recepcion.isoformat():
                errores.append(
                    f"Producto {codigo}: la fecha límite del lote no puede ser anterior a la recepción."
                )
                continue
            fechas[codigo] = fecha
    return recibidos, fechas, errores


def aplicar_recepcion(
    productos: List[Producto], recibidos: Dict[str, int], fechas: Dict[str, str]
) -> Tuple[List[Producto], List[str]]:
    """
    Suma al stock la mercancía recibida como un lote nuevo (o al lote que ya
    tenga esa misma fecha). La fecha de los lotes anteriores no se toca: el
    producto mostrará siempre la más próxima. Sin fecha el lote queda "sin fecha
    de caducidad". No modifica la lista original.
    """
    mensajes: List[str] = []
    actualizados: List[Producto] = []
    for producto in productos:
        codigo = str(producto["Código"])
        if codigo in recibidos:
            fecha = fechas.get(codigo, "")
            producto = _lotes.agregar_lote(producto, fecha, recibidos[codigo])
            mensaje = f"Recibidos {recibidos[codigo]} {producto['Nombre']}. Nuevo stock: {producto['Cantidad']}."
            mensaje += f" Lote con fecha límite {fecha}." if fecha else " Lote sin fecha de caducidad."
            mensajes.append(mensaje)
        actualizados.append(producto)
    return actualizados, mensajes


# --------------------------------------------------------------------------
#  Mermas: mercancía que se descarta (vencida, dañada...)
# --------------------------------------------------------------------------
def parsear_merma(
    form: Mapping[str, Any], codigos_validos: Iterable[str]
) -> Tuple[Dict[Tuple[str, str], int], Dict[Tuple[str, str], str], List[str]]:
    """
    Extrae lo que se descarta de los campos `merma_cantidad[<código>@<fecha>]`
    (un campo por lote; la fecha va vacía para el lote sin fecha) y su motivo en
    `merma_motivo[<código>@<fecha>]` (vencido, danado u otro; vacío = otro).

    Devuelve ({(código, fecha): cantidad}, {(código, fecha): motivo}, errores).
    Las líneas vacías o en 0 se ignoran.
    """
    prefijo = "merma_cantidad["
    validos = {str(c) for c in codigos_validos}
    mermas: Dict[Tuple[str, str], int] = {}
    motivos: Dict[Tuple[str, str], str] = {}
    errores: List[str] = []

    for clave, valor in form.items():
        if not (clave.startswith(prefijo) and clave.endswith("]")):
            continue
        interior = clave[len(prefijo) : -1]
        if str(valor).strip() == "":
            continue
        codigo, separador, texto_fecha = interior.rpartition("@")
        if not separador or not codigo:
            errores.append(f"Línea de merma inválida ({interior}).")
            continue
        if codigo not in validos:
            errores.append(f"Producto {codigo} no encontrado.")
            continue
        try:
            fecha = validar_fecha(texto_fecha)
        except ValueError:
            errores.append(f"Producto {codigo}: la fecha del lote debe tener formato YYYY-MM-DD válido.")
            continue
        try:
            cantidad = a_entero(valor)
        except ValueError:
            errores.append(f"Producto {codigo}: cantidad a descartar inválida.")
            continue
        if cantidad < 0:
            errores.append(f"Producto {codigo}: la cantidad a descartar no puede ser negativa.")
            continue
        if cantidad == 0:
            continue

        motivo = str(form.get(f"merma_motivo[{interior}]", "")).strip().lower() or "otro"
        if motivo not in MOTIVOS_MERMA:
            errores.append(f"Producto {codigo}: motivo desconocido (usa vencido, danado u otro).")
            continue
        mermas[(codigo, fecha)] = cantidad
        motivos[(codigo, fecha)] = motivo
    return mermas, motivos, errores


def aplicar_merma(
    productos: List[Producto], mermas: Dict[Tuple[str, str], int]
) -> Tuple[List[Producto], List[str]]:
    """
    Descuenta del lote indicado lo descartado. No modifica la lista original.

    Todo o nada: si algún lote no existe o no tiene suficientes unidades se
    lanza InventarioError y no se aplica nada.
    """
    por_codigo = {str(p["Código"]): p for p in productos}
    errores: List[str] = []
    for (codigo, fecha), cantidad in mermas.items():
        existencias = {l["Fecha límite"]: l["Cantidad"] for l in _lotes.lotes_de(por_codigo[codigo])}
        etiqueta = f" (lote {fecha})" if fecha else " (lote sin fecha)"
        if fecha not in existencias:
            errores.append(f"Producto {codigo}{etiqueta}: ese lote no existe.")
        elif cantidad > existencias[fecha]:
            errores.append(
                f"Producto {codigo}{etiqueta}: no se pueden descartar {cantidad} (hay {existencias[fecha]})."
            )
    if errores:
        raise InventarioError(errores)

    mensajes: List[str] = []
    actualizados: List[Producto] = []
    for producto in productos:
        codigo = str(producto["Código"])
        for (c, fecha), cantidad in mermas.items():
            if c == codigo:
                producto = _lotes.quitar_de_lote(producto, fecha, cantidad)
                origen = f" del lote {fecha}" if fecha else " del lote sin fecha"
                mensajes.append(
                    f"Descartados {cantidad} {producto['Nombre']}{origen}. Nuevo stock: {producto['Cantidad']}."
                )
        actualizados.append(producto)
    return actualizados, mensajes


# --------------------------------------------------------------------------
#  Pedido a proveedor
# --------------------------------------------------------------------------
def validar_pedido_proveedor(
    productos: List[Producto], form: Mapping[str, Any]
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """
    Valida los campos `pedido_proveedor[<código>]` y `precio_proveedor[<código>]`.

    Devuelve (líneas del pedido en el mismo orden del inventario, errores).
    """
    prefijo = "pedido_proveedor["
    por_codigo = {str(p["Código"]): p for p in productos}
    enviados = {k[len(prefijo) : -1] for k in form.keys() if k.startswith(prefijo) and k.endswith("]")}

    pedido: List[Dict[str, Any]] = []
    errores: List[str] = [f"Producto {c} no encontrado." for c in sorted(enviados - set(por_codigo))]

    for producto in productos:
        codigo = str(producto["Código"])
        if codigo not in enviados:
            continue

        try:
            texto = str(form.get(f"pedido_proveedor[{codigo}]", "")).strip()
            cantidad = a_entero(texto) if texto else 0
        except ValueError:
            errores.append(f"Producto {codigo}: cantidad inválida.")
            continue
        if cantidad < 0:
            errores.append(f"Producto {codigo}: cantidad negativa.")
            continue
        if cantidad == 0:
            continue

        try:
            texto_precio = str(form.get(f"precio_proveedor[{codigo}]", "")).strip()
            precio = float(texto_precio) if texto_precio else 0.0
        except ValueError:
            errores.append(f"Producto {codigo}: precio inválido.")
            continue
        if not math.isfinite(precio) or precio <= 0:
            errores.append(f"Producto {codigo}: el precio debe ser mayor que 0.")
            continue

        pedido.append(
            {
                "codigo": producto["Código"],
                "nombre": producto["Nombre"],
                "cantidad": cantidad,
                "precio_unitario": precio,
                "tiempo_entrega": producto["Tiempo entrega(Días)"],
                "stock_actual": producto["Cantidad"],
            }
        )
    return pedido, errores
