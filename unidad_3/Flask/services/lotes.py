"""
Lotes de producto.

Un lote es un grupo de unidades que comparten la misma fecha de caducidad
(normalmente porque llegaron juntas). El usuario nunca ve un código de lote:
solo fechas y unidades. Un producto tiene una lista de lotes y su stock es la
suma de ellos.

    {"Código": "L1", "Nombre": "Leche", "Tiempo entrega(Días)": 2,
     "Cantidad": 30,                 # total (derivado)
     "Fecha límite": "2026-10-30",   # la más próxima entre los lotes con fecha (derivado)
     "Lotes": [{"Fecha límite": "2026-10-30", "Cantidad": 10},
               {"Fecha límite": "2026-11-15", "Cantidad": 20}]}

Reglas:
* Dos lotes con la misma fecha son uno solo; un lote sin unidades no existe.
* Un lote sin fecha ("") es mercancía sin caducidad conocida: se vende al final
  (se ordena detrás de los que sí tienen fecha) y el sistema avisa de que falta.
* Las ventas salen siempre del lote que caduca antes (FEFO: el primero en
  caducar es el primero en salir).
* Un lote está vencido cuando su fecha límite es anterior a hoy: la fecha límite
  es el último día para vender, así que ese día todavía se puede vender.

Lógica pura (sin Flask). Todas las funciones devuelven productos nuevos y no
modifican los recibidos. Un producto "plano" (con Cantidad y Fecha límite pero
sin `Lotes`) se interpreta como un único lote.
"""

import datetime
from typing import Any, Dict, Iterable, List, Mapping, Tuple

Producto = Dict[str, Any]
Lote = Dict[str, Any]  # {"Fecha límite": "YYYY-MM-DD" | "", "Cantidad": int > 0}


def _orden_fefo(lote: Mapping[str, Any]) -> Tuple[bool, str]:
    fecha = lote["Fecha límite"]
    return (fecha == "", fecha)  # con fecha primero (ascendente); sin fecha al final


def normalizar_lotes(lotes: Iterable[Mapping[str, Any]]) -> List[Lote]:
    """Une los lotes con la misma fecha, descarta los vacíos y ordena por caducidad."""
    acumulado: Dict[str, int] = {}
    for lote in lotes:
        cantidad = int(lote["Cantidad"])
        if cantidad > 0:
            fecha = str(lote.get("Fecha límite") or "").strip()
            acumulado[fecha] = acumulado.get(fecha, 0) + cantidad
    return sorted(
        ({"Fecha límite": fecha, "Cantidad": cantidad} for fecha, cantidad in acumulado.items()),
        key=_orden_fefo,
    )


def construir_producto(
    codigo: str, nombre: str, tiempo_entrega: int, lotes: Iterable[Mapping[str, Any]]
) -> Producto:
    """Único punto donde se crea un producto: deja los lotes normalizados y los totales al día."""
    lotes_ok = normalizar_lotes(lotes)
    fechas = [lote["Fecha límite"] for lote in lotes_ok if lote["Fecha límite"]]
    return {
        "Código": codigo,
        "Nombre": nombre,
        "Cantidad": sum(lote["Cantidad"] for lote in lotes_ok),
        "Tiempo entrega(Días)": tiempo_entrega,
        "Fecha límite": fechas[0] if fechas else "",
        "Lotes": lotes_ok,
    }


def lotes_de(producto: Mapping[str, Any]) -> List[Lote]:
    """Lotes del producto, ordenados por caducidad (copia: se pueden modificar)."""
    if "Lotes" in producto:
        return sorted(({**lote} for lote in producto["Lotes"]), key=_orden_fefo)
    return normalizar_lotes(
        [{"Fecha límite": producto.get("Fecha límite", ""), "Cantidad": producto.get("Cantidad", 0)}]
    )


def reconstruir(producto: Mapping[str, Any], lotes: Iterable[Mapping[str, Any]]) -> Producto:
    """El mismo producto con otros lotes."""
    return construir_producto(
        producto["Código"], producto["Nombre"], producto["Tiempo entrega(Días)"], lotes
    )


def stock_total(producto: Mapping[str, Any]) -> int:
    return sum(lote["Cantidad"] for lote in lotes_de(producto))


def unidades_sin_fecha(producto: Mapping[str, Any]) -> int:
    """Unidades en lotes sin fecha de caducidad."""
    return sum(lote["Cantidad"] for lote in lotes_de(producto) if not lote["Fecha límite"])


def esta_vencido(lote: Mapping[str, Any], hoy: datetime.date) -> bool:
    """Un lote vence al día siguiente de su fecha límite (ese día todavía se puede vender)."""
    return bool(lote["Fecha límite"]) and lote["Fecha límite"] < hoy.isoformat()


def consumir_fefo(producto: Mapping[str, Any], cantidad: int) -> Producto:
    """
    Descuenta `cantidad` unidades empezando por el lote que caduca antes.
    Lanza ValueError si no hay suficientes.
    """
    lotes = lotes_de(producto)
    if cantidad > sum(lote["Cantidad"] for lote in lotes):
        raise ValueError("stock insuficiente")
    restante = cantidad
    quedan: List[Lote] = []
    for lote in lotes:
        tomar = min(restante, lote["Cantidad"])
        restante -= tomar
        if lote["Cantidad"] > tomar:
            quedan.append({**lote, "Cantidad": lote["Cantidad"] - tomar})
    return reconstruir(producto, quedan)


def agregar_lote(producto: Mapping[str, Any], fecha: str, cantidad: int) -> Producto:
    """Suma unidades como lote nuevo, o al lote que ya tenga esa misma fecha."""
    return reconstruir(producto, lotes_de(producto) + [{"Fecha límite": fecha, "Cantidad": cantidad}])


def quitar_de_lote(producto: Mapping[str, Any], fecha: str, cantidad: int) -> Producto:
    """
    Descuenta unidades de un lote concreto (`fecha` "" = el lote sin fecha).
    Lanza ValueError si el lote no existe o no tiene tantas unidades.
    """
    lotes = lotes_de(producto)
    for lote in lotes:
        if lote["Fecha límite"] == fecha:
            if cantidad > lote["Cantidad"]:
                raise ValueError("el lote no tiene tantas unidades")
            lote["Cantidad"] -= cantidad
            return reconstruir(producto, lotes)
    raise ValueError("no existe ese lote")


def descartar_vencidos(
    productos: List[Producto], hoy: datetime.date
) -> Tuple[List[Producto], List[Dict[str, Any]]]:
    """
    Quita de cada producto los lotes ya vencidos (fecha límite anterior a hoy).

    Devuelve (productos nuevos, descartes), con un descarte por lote:
    {"codigo", "nombre", "cantidad", "fecha_limite"}.
    """
    nuevos: List[Producto] = []
    descartes: List[Dict[str, Any]] = []
    for producto in productos:
        lotes = lotes_de(producto)
        vencidos = [lote for lote in lotes if esta_vencido(lote, hoy)]
        if not vencidos:
            nuevos.append(producto)
            continue
        for lote in vencidos:
            descartes.append(
                {
                    "codigo": str(producto["Código"]),
                    "nombre": producto["Nombre"],
                    "cantidad": lote["Cantidad"],
                    "fecha_limite": lote["Fecha límite"],
                }
            )
        nuevos.append(reconstruir(producto, [lote for lote in lotes if not esta_vencido(lote, hoy)]))
    return nuevos, descartes


def a_filas(productos: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    """
    Aplana el inventario a filas del CSV: una por lote. Un producto sin stock
    ocupa una fila con Cantidad 0, para que no desaparezca al guardarlo.
    """
    filas: List[Dict[str, Any]] = []
    for producto in productos:
        base = {
            "Código": producto["Código"],
            "Nombre": producto["Nombre"],
            "Tiempo entrega(Días)": producto["Tiempo entrega(Días)"],
        }
        lotes = lotes_de(producto) or [{"Fecha límite": "", "Cantidad": 0}]
        for lote in lotes:
            filas.append({**base, "Cantidad": lote["Cantidad"], "Fecha límite": lote["Fecha límite"]})
    return filas
