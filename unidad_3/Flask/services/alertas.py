"""
Alertas de inventario: vencimiento, reposición, popularidad y fecha faltante.

Lógica pura (sin Flask). Reglas:

* Vencimiento (por lote, ver services/lotes.py): un lote está *vencido* si su
  fecha límite (el último día para venderlo) ya pasó; el producto lo está si
  alguno de sus lotes con stock lo está. Está *por vencer* si el lote vigente
  más próximo vence en `dias_aviso` días o menos (el propio día límite cuenta,
  con 0 días). La fecha que se muestra del producto es siempre la del lote que
  caduca antes, aunque haya otros con fechas más lejanas.

* Fecha faltante: si hay unidades en un lote sin fecha de caducidad se avisa
  siempre. Registrar el producto sin fecha es posible; el aviso no desaparece
  hasta que se indique la fecha.

* Reposición: se basa en el consumo diario REAL calculado del historial
  (services/demanda.py), sin contar eventos, y solo cuenta el stock vigente
  (el vencido no se puede vender). Mientras llega un pedido (Tiempo de entrega)
  más `dias_seguridad` de colchón se consumen consumo × (tiempo + colchón)
  unidades; si el stock vigente no alcanza, hay que reponer. Sin historial
  suficiente no se inventan números: solo se avisa si el producto está agotado.

* Popularidad: se avisa de los productos "en alza" (su consumo reciente
  supera claramente al anterior), para que el dueño anticipe la compra.
"""

import datetime
import math
from typing import Any, Dict, List, Mapping, Optional

from .demanda import ALZA
from .lotes import esta_vencido, lotes_de
from .inventario import Producto

VENCIDO = "vencido"
POR_VENCER = "por_vencer"

Alerta = Dict[str, Any]


def evaluar_producto(
    producto: Mapping[str, Any],
    hoy: datetime.date,
    dias_aviso: int = 7,
    stats: Optional[Mapping[str, Any]] = None,
    dias_seguridad: int = 1,
) -> Alerta:
    """
    Evalúa un producto con sus lotes (o un producto plano de un solo lote).

    `stats` son las estadísticas de demanda de ese producto
    (`demanda.analizar(...)["productos"][codigo]`); None = sin historial.

    Devuelve un diccionario con:
        vencimiento          None, "vencido" o "por_vencer" (el peor de sus lotes)
        dias_restantes       días hasta el lote que caduca antes (negativo si ya pasó) o None
        proxima_fecha        fecha de ese lote ("" si ninguno tiene fecha)
        unidades_proximo     unidades de ese lote
        unidades_vencidas    unidades en lotes ya vencidos
        dias_por_vencer      días del lote vigente más próximo si cae en el aviso, o None
        unidades_por_vencer  unidades de ese lote
        sin_fecha            True si hay unidades en lotes sin fecha de caducidad
        unidades_sin_fecha   cuántas
        agotado              True si no hay stock y (hay demanda o se desconoce)
        reponer              True si el stock vigente no cubre la entrega + colchón
        cobertura            días que dura el stock vigente al consumo actual, o None
        sugerido             unidades que faltan para cubrir la entrega + colchón
        consumo_diario       unidades/día (sin eventos) o None si no hay historial
        tendencia, variacion popularidad (ver services/demanda.py)
        sin_historial        True si no se pudo calcular el consumo
        con_alerta           True si hay algo que atender
    """
    tiempo = int(producto["Tiempo entrega(Días)"])
    lotes = lotes_de(producto)
    cantidad = sum(lote["Cantidad"] for lote in lotes)

    # --- Vencimiento, por lote
    unidades_vencidas = sum(lote["Cantidad"] for lote in lotes if esta_vencido(lote, hoy))
    con_fecha = [lote for lote in lotes if lote["Fecha límite"]]  # ya en orden de caducidad
    proximo = con_fecha[0] if con_fecha else None
    dias_restantes = (datetime.date.fromisoformat(proximo["Fecha límite"]) - hoy).days if proximo else None

    dias_por_vencer: Optional[int] = None
    unidades_por_vencer = 0
    vigentes = [lote for lote in con_fecha if not esta_vencido(lote, hoy)]
    if vigentes:
        dias = (datetime.date.fromisoformat(vigentes[0]["Fecha límite"]) - hoy).days
        if dias <= dias_aviso:
            dias_por_vencer, unidades_por_vencer = dias, vigentes[0]["Cantidad"]

    vencimiento: Optional[str] = None
    if unidades_vencidas:
        vencimiento = VENCIDO
    elif dias_por_vencer is not None:
        vencimiento = POR_VENCER

    # --- Fecha faltante
    sin_fecha_unidades = sum(lote["Cantidad"] for lote in lotes if not lote["Fecha límite"])

    # --- Reposición (con consumo real y solo con lo que todavía se puede vender)
    vigente = cantidad - unidades_vencidas
    consumo = stats["consumo_diario"] if stats else None
    sin_historial = consumo is None
    agotado = cantidad == 0 and (sin_historial or consumo > 0)

    reponer = False
    sugerido = 0
    cobertura: Optional[float] = None
    if not sin_historial and consumo > 0:
        necesario = consumo * (tiempo + dias_seguridad)
        reponer = vigente < necesario
        sugerido = math.ceil(necesario - vigente) if reponer else 0
        cobertura = round(vigente / consumo, 1)

    tendencia = stats["tendencia"] if stats else None
    variacion = stats["variacion"] if stats else None

    return {
        "vencimiento": vencimiento,
        "dias_restantes": dias_restantes,
        "proxima_fecha": proximo["Fecha límite"] if proximo else "",
        "unidades_proximo": proximo["Cantidad"] if proximo else 0,
        "unidades_vencidas": unidades_vencidas,
        "dias_por_vencer": dias_por_vencer,
        "unidades_por_vencer": unidades_por_vencer,
        "sin_fecha": sin_fecha_unidades > 0,
        "unidades_sin_fecha": sin_fecha_unidades,
        "agotado": agotado,
        "reponer": reponer,
        "cobertura": cobertura,
        "sugerido": sugerido,
        "consumo_diario": consumo,
        "tendencia": tendencia,
        "variacion": variacion,
        "sin_historial": sin_historial,
        "con_alerta": (
            vencimiento is not None or sin_fecha_unidades > 0 or reponer or agotado or tendencia == ALZA
        ),
    }


def evaluar_inventario(
    productos: List[Producto],
    hoy: datetime.date,
    dias_aviso: int = 7,
    analisis: Optional[Mapping[str, Any]] = None,
    dias_seguridad: int = 1,
) -> Dict[str, Alerta]:
    """
    Alertas de todo el inventario, indexadas por código de producto.
    `analisis` es el resultado de `demanda.analizar` (None = sin historial).
    """
    por_producto = analisis["productos"] if analisis else {}
    return {
        str(p["Código"]): evaluar_producto(
            p, hoy, dias_aviso, por_producto.get(str(p["Código"])), dias_seguridad
        )
        for p in productos
    }


def resumir(alertas: Mapping[str, Alerta]) -> Dict[str, Any]:
    """
    Cuenta productos por tipo de alerta. Las categorías de stock son
    excluyentes: `agotados` (sin stock) y `reponer` (con algo de stock pero
    insuficiente). Vencimiento, fecha faltante y alza pueden coincidir con ellas.
    """
    valores = list(alertas.values())
    return {
        "vencidos": sum(1 for a in valores if a["vencimiento"] == VENCIDO),
        "por_vencer": sum(1 for a in valores if a["vencimiento"] == POR_VENCER),
        "sin_fecha": sum(1 for a in valores if a["sin_fecha"]),
        "agotados": sum(1 for a in valores if a["agotado"]),
        "reponer": sum(1 for a in valores if a["reponer"] and not a["agotado"]),
        "en_alza": sum(1 for a in valores if a["tendencia"] == ALZA),
        "con_alerta": sum(1 for a in valores if a["con_alerta"]),
        "total": len(valores),
        "sin_historial": bool(valores) and all(a["sin_historial"] for a in valores),
    }
