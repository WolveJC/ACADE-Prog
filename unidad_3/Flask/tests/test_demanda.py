"""Pruebas del análisis de demanda (consumo diario, tendencia y ranking)."""

import datetime

from services import demanda

HOY = datetime.date(2026, 6, 15)


def mov(atras, codigo, cantidad, evento=False):
    return {"fecha": HOY - datetime.timedelta(days=atras), "codigo": codigo,
            "cantidad": cantidad, "evento": evento}


def analizar(movs, codigos=("a", "b", "z"), **kw):
    return demanda.analizar(movs, codigos, HOY, **kw)


# --------------------------------------------------------------- suficiencia
def test_sin_movimientos_no_hay_historial():
    r = analizar([])
    assert r["historial_dias"] == 0 and not r["suficiente"]
    assert r["productos"]["a"]["consumo_diario"] is None


def test_historial_corto_no_calcula_consumo_y_el_limite_es_inclusivo():
    corto = analizar([mov(5, "a", 10)])               # 6 días de historial (hoy cuenta)
    assert corto["historial_dias"] == 6 and corto["productos"]["a"]["consumo_diario"] is None
    justo = analizar([mov(6, "a", 14)])               # 7 días
    assert justo["suficiente"] and justo["productos"]["a"]["consumo_diario"] == 2.0


def test_consumo_diario_promedia_la_ventana_completa():
    movs = [mov(d, "a", 2) for d in range(14)]       # 2 por día durante 14 días
    r = analizar(movs)["productos"]["a"]
    assert r["consumo_diario"] == 2.0 and r["total_ventana"] == 28


def test_con_menos_historial_que_la_ventana_se_divide_entre_los_dias_reales():
    movs = [mov(d, "a", 3) for d in range(10)]       # 10 días de historial, ventana 14
    r = analizar(movs)
    assert r["ventana"] == 10 and r["productos"]["a"]["consumo_diario"] == 3.0


def test_producto_sin_ventas_con_historial_suficiente_consume_cero():
    r = analizar([mov(d, "a", 1) for d in range(8)])
    assert r["productos"]["b"]["consumo_diario"] == 0.0 and r["productos"]["b"]["ranking"] is None


def test_movimientos_fuera_de_la_ventana_no_cuentan_para_el_consumo():
    r = analizar([mov(20, "a", 100), mov(0, "a", 7)] + [mov(d, "z", 1) for d in range(1, 20)])
    assert r["productos"]["a"]["total_ventana"] == 7           # los 100 de hace 20 días quedan fuera
    assert r["productos"]["a"]["ultima_salida"] == HOY


# ------------------------------------------------------------------- eventos
def test_los_eventos_no_cuentan_para_el_consumo_pero_si_se_registran():
    movs = [mov(d, "a", 2) for d in range(14)] + [mov(3, "a", 500, evento=True)]
    p = analizar(movs)["productos"]["a"]
    assert p["consumo_diario"] == 2.0 and p["total_ventana"] == 28 and p["unidades_evento"] == 500


def test_los_eventos_no_distorsionan_la_tendencia_ni_el_ranking():
    movs = [mov(13, "z", 1), mov(10, "a", 10), mov(1, "a", 10), mov(2, "a", 900, evento=True)]
    r = analizar(movs)["productos"]["a"]
    assert r["tendencia"] == "estable" and r["ranking"] == 1 and r["total_ventana"] == 20


def test_un_producto_solo_con_eventos_no_tiene_ranking():
    movs = [mov(d, "z", 1) for d in range(8)] + [mov(1, "a", 50, evento=True)]
    p = analizar(movs)["productos"]["a"]
    assert p["ranking"] is None and p["consumo_diario"] == 0.0 and p["ultima_salida"] is not None


# ----------------------------------------------------------------- tendencia
def tendencia(reciente, previo):
    movs = [mov(13, "z", 1)]                                   # fija 14 días de historial
    if previo: movs.append(mov(10, "a", previo))               # primera mitad (días 7-13)
    if reciente: movs.append(mov(2, "a", reciente))            # segunda mitad (días 0-6)
    return analizar(movs)["productos"]["a"]


def test_alza_baja_y_estable():
    assert tendencia(20, 10)["tendencia"] == "alza" and tendencia(20, 10)["variacion"] == 1.0
    assert tendencia(5, 10)["tendencia"] == "baja" and tendencia(5, 10)["variacion"] == -0.5
    assert tendencia(11, 10)["tendencia"] == "estable"


def test_los_umbrales_de_30_por_ciento_son_inclusivos():
    assert tendencia(13, 10)["tendencia"] == "alza"
    assert tendencia(7, 10)["tendencia"] == "baja"
    assert tendencia(12, 10)["tendencia"] == "estable"


def test_poco_volumen_no_genera_tendencia():
    assert tendencia(2, 1)["tendencia"] is None                # 3 unidades: es ruido
    assert tendencia(3, 2)["tendencia"] == "alza"              # 5 unidades: ya cuenta


def test_producto_que_antes_no_se_vendia_aparece_en_alza_sin_porcentaje():
    p = tendencia(6, 0)
    assert p["tendencia"] == "alza" and p["variacion"] is None


def test_sin_ventana_completa_no_hay_tendencia():
    movs = [mov(9, "z", 1), mov(8, "a", 10), mov(1, "a", 100)]  # 10 días < ventana de 14
    assert analizar(movs)["productos"]["a"]["tendencia"] is None


# ------------------------------------------------------------------- ranking
def test_ranking_por_unidades_con_desempate_por_codigo():
    movs = [mov(d, "z", 1) for d in range(8)] + [mov(1, "a", 3), mov(1, "b", 3), mov(1, "c", 9)]
    r = analizar(movs, codigos=("a", "b", "c", "z"))["productos"]
    assert (r["c"]["ranking"], r["a"]["ranking"], r["b"]["ranking"], r["z"]["ranking"]) == (1, 3, 4, 2)


def test_codigos_desconocidos_y_fechas_futuras_se_ignoran():
    futuro = {"fecha": HOY + datetime.timedelta(days=3), "codigo": "a", "cantidad": 99, "evento": False}
    r = analizar([mov(8, "desconocido", 50), futuro])
    assert r["historial_dias"] == 0 and "desconocido" not in r["productos"]
