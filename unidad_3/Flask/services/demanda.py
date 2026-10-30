"""
Análisis de demanda a partir del historial de movimientos.

Lógica pura (sin Flask). Responde a tres preguntas por producto:

1. ¿Cuánto se consume por día?  → `consumo_diario` (unidades/día), promediando
   la ventana reciente. Los movimientos marcados como evento NO cuentan.
2. ¿Se está volviendo más (o menos) popular?  → `tendencia`: se compara la
   segunda mitad de la ventana contra la primera (p. ej. última semana contra
   la anterior). Requiere una ventana completa de historial y un volumen
   mínimo, para no reaccionar al ruido (1 → 2 unidades no es una tendencia).
3. ¿Cuál es más popular?  → `ranking` por unidades retiradas en la ventana.

Mientras el historial sea más corto que `min_historial` días no se inventa
nada: `consumo_diario` es None y las alertas de reposición no se activan.
"""

import datetime
from typing import Any, Dict, Iterable, List

ALZA = "alza"
BAJA = "baja"
ESTABLE = "estable"


def analizar(
    movimientos: List[Dict[str, Any]],
    codigos: Iterable[str],
    hoy: datetime.date,
    ventana: int = 14,
    min_historial: int = 7,
    umbral_tendencia: float = 0.3,
    min_unidades_tendencia: int = 5,
) -> Dict[str, Any]:
    """
    Calcula las estadísticas de demanda del inventario.

    Args:
        movimientos: lista de {"fecha": date, "codigo": str, "cantidad": int,
            "tipo": "salida"|"entrada"|"merma", "evento": bool}. Solo las salidas
            miden la demanda; las mermas se cuentan aparte y las entradas se ignoran.
        codigos: códigos de los productos del inventario actual.
        hoy: fecha de referencia (el día de hoy cuenta como parte de la ventana).
        ventana: días de la ventana de consumo (par: se parte en dos mitades).
        min_historial: días de historial necesarios para calcular el consumo.
        umbral_tendencia: variación relativa a partir de la cual hay alza/baja.
        min_unidades_tendencia: volumen mínimo (dos mitades juntas) para opinar.

    Returns:
        {"historial_dias": int, "suficiente": bool, "ventana": int,
         "productos": {codigo: {consumo_diario, total_ventana, unidades_evento, unidades_merma,
                                tendencia, variacion, ultima_salida, ranking}}}
    """
    codigos = [str(c) for c in codigos]
    conocidos = set(codigos)
    # Solo las salidas miden la demanda; las entradas (recepciones) no cuentan.
    propios = [
        m for m in movimientos
        if m["codigo"] in conocidos and m["fecha"] <= hoy and m.get("tipo", "salida") == "salida"
    ]

    primera = min((m["fecha"] for m in propios), default=None)
    historial_dias = (hoy - primera).days + 1 if primera else 0
    suficiente = historial_dias >= min_historial
    ventana_efectiva = min(ventana, historial_dias) if suficiente else 0
    mitad = ventana // 2
    con_tendencia = suficiente and historial_dias >= ventana and mitad > 0
    inicio = hoy - datetime.timedelta(days=ventana_efectiva - 1) if ventana_efectiva else None

    acumulado: Dict[str, Dict[str, Any]] = {
        c: {"total": 0, "evento": 0, "reciente": 0, "previo": 0, "ultima": None}
        for c in codigos
    }
    for m in propios:
        a = acumulado[m["codigo"]]
        if a["ultima"] is None or m["fecha"] > a["ultima"]:
            a["ultima"] = m["fecha"]
        if not suficiente:
            continue
        if inicio is not None and m["fecha"] >= inicio:
            a["evento" if m["evento"] else "total"] += m["cantidad"]
        if con_tendencia and not m["evento"]:
            dias_atras = (hoy - m["fecha"]).days
            if dias_atras < mitad:
                a["reciente"] += m["cantidad"]
            elif dias_atras < 2 * mitad:
                a["previo"] += m["cantidad"]

    # Las mermas no son demanda, pero se contabilizan aparte (últimos `ventana` días).
    inicio_mermas = hoy - datetime.timedelta(days=ventana - 1)
    mermas = {c: 0 for c in codigos}
    for m in movimientos:
        if m.get("tipo") == "merma" and m["codigo"] in conocidos and inicio_mermas <= m["fecha"] <= hoy:
            mermas[m["codigo"]] += m["cantidad"]

    productos: Dict[str, Dict[str, Any]] = {}
    for codigo, a in acumulado.items():
        tendencia = None
        variacion = None
        if con_tendencia and a["reciente"] + a["previo"] >= min_unidades_tendencia:
            if a["previo"] == 0:
                tendencia = ALZA  # no se vendía y ahora sí: variación no definida
            else:
                variacion = (a["reciente"] - a["previo"]) / a["previo"]
                if variacion >= umbral_tendencia:
                    tendencia = ALZA
                elif variacion <= -umbral_tendencia:
                    tendencia = BAJA
                else:
                    tendencia = ESTABLE
        productos[codigo] = {
            "consumo_diario": a["total"] / ventana_efectiva if suficiente else None,
            "total_ventana": a["total"],
            "unidades_evento": a["evento"],
            "unidades_merma": mermas[codigo],
            "tendencia": tendencia,
            "variacion": variacion,
            "ultima_salida": a["ultima"],
            "ranking": None,
        }

    con_ventas = sorted(
        (c for c, p in productos.items() if p["total_ventana"] > 0),
        key=lambda c: (-productos[c]["total_ventana"], c),
    )
    for posicion, codigo in enumerate(con_ventas, start=1):
        productos[codigo]["ranking"] = posicion

    return {
        "historial_dias": historial_dias,
        "suficiente": suficiente,
        "ventana": ventana_efectiva,
        "productos": productos,
    }
