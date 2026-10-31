"""Pruebas de las alertas de vencimiento, reposición y popularidad."""

import datetime

import pytest

from conftest import historial_csv, importar_historial, subir
from services import alertas

HOY = datetime.date(2026, 6, 15)


def producto(cantidad=10, tiempo=1, dias=365):   # por defecto con fecha lejana: sin alertas de fecha
    fecha = "" if dias is None else (HOY + datetime.timedelta(days=dias)).isoformat()
    return {"Código": "1", "Nombre": "X", "Cantidad": cantidad,
            "Tiempo entrega(Días)": tiempo, "Fecha límite": fecha}


def stats(consumo=None, tendencia=None, variacion=None):
    return {"consumo_diario": consumo, "tendencia": tendencia, "variacion": variacion}


def evaluar(prod, estadisticas=None, aviso=7, seguridad=1):
    return alertas.evaluar_producto(prod, HOY, aviso, estadisticas, seguridad)


# ---------------------------------------------------------------- vencimiento
@pytest.mark.parametrize("dias, esperado", [
    (-30, "vencido"), (-1, "vencido"),
    (0, "por_vencer"), (7, "por_vencer"),   # el propio día y el límite del aviso cuentan
    (8, None), (365, None), (None, None),   # fuera de ventana / sin fecha
])
def test_vencimiento_segun_dias_restantes(dias, esperado):
    assert evaluar(producto(dias=dias))["vencimiento"] == esperado


def test_dias_de_aviso_es_configurable():
    assert evaluar(producto(dias=10))["vencimiento"] is None
    assert evaluar(producto(dias=10), aviso=14)["vencimiento"] == "por_vencer"


def test_sin_stock_no_hay_lotes_y_por_tanto_nada_que_caducar():
    a = evaluar(producto(cantidad=0, dias=-5))
    assert a["vencimiento"] is None and a["dias_restantes"] is None and a["unidades_vencidas"] == 0
    assert not a["sin_fecha"]


# ------------------------------------------------------------------ reposición
@pytest.mark.parametrize("cantidad, consumo, tiempo, reponer", [
    (14, 5, 2, True),    # necesita 5 × (2+1) = 15 y tiene 14
    (15, 5, 2, False),   # justo alcanza: no se pide
    (50, 5, 2, False),
    (0, 5, 0, True),     # agotado con consumo: necesita 5 y tiene 0
    (0, 0, 5, False),    # historial suficiente pero no se vende: no se repone
    (3, 0, 9, False),
])
def test_reposicion_con_consumo_real(cantidad, consumo, tiempo, reponer):
    assert evaluar(producto(cantidad, tiempo), stats(consumo))["reponer"] is reponer


def test_sin_historial_no_se_inventan_cifras():
    a = evaluar(producto(cantidad=1, tiempo=9), None)
    assert a["sin_historial"] and not a["reponer"] and a["sugerido"] == 0 and a["consumo_diario"] is None
    a = evaluar(producto(cantidad=1, tiempo=9), stats(consumo=None))
    assert a["sin_historial"] and not a["reponer"]


def test_agotado_con_o_sin_historial_pero_no_si_no_se_vende():
    assert evaluar(producto(cantidad=0), None)["agotado"] is True          # no se sabe: se avisa
    assert evaluar(producto(cantidad=0), stats(2.0))["agotado"] is True    # se vende: se avisa
    assert evaluar(producto(cantidad=0), stats(0.0))["agotado"] is False   # no se vende: no
    assert evaluar(producto(cantidad=1), None)["agotado"] is False


def test_sugerido_cobertura_y_colchon_configurable():
    a = evaluar(producto(cantidad=4, tiempo=3), stats(2.5))      # necesita 2.5 × 4 = 10
    assert a["sugerido"] == 6 and a["cobertura"] == 1.6
    assert evaluar(producto(cantidad=1, tiempo=0), stats(1.3))["sugerido"] == 1   # sube al entero
    assert evaluar(producto(cantidad=50), stats(2.0))["sugerido"] == 0
    # sin colchón: necesita 2.5 × 3 = 7.5 → con 7 hay que reponer, con 8 no
    assert evaluar(producto(cantidad=7, tiempo=3), stats(2.5), seguridad=0)["reponer"] is True
    assert evaluar(producto(cantidad=8, tiempo=3), stats(2.5), seguridad=0)["reponer"] is False


def test_tendencia_en_alza_cuenta_como_alerta_pero_baja_no():
    alza = evaluar(producto(), stats(2.0, "alza", 0.5))
    assert alza["tendencia"] == "alza" and alza["con_alerta"] and alza["variacion"] == 0.5
    assert not evaluar(producto(), stats(2.0, "baja", -0.5))["con_alerta"]
    assert not evaluar(producto(), stats(2.0, "estable", 0.0))["con_alerta"]


def test_resumen_cuenta_categorias_excluyentes_de_stock():
    inventario = [
        {**producto(dias=-1), "Código": "venc"},
        {**producto(cantidad=1, dias=3), "Código": "porvenc"},
        {**producto(), "Código": "ok"},
        {**producto(cantidad=0), "Código": "agot"},
        {**producto(cantidad=1, tiempo=2), "Código": "rep"},
        {**producto(), "Código": "alza"},
    ]
    analisis = {"productos": {
        "venc": stats(0.0), "porvenc": stats(0.0), "ok": stats(1.0), "agot": stats(3.0),
        "rep": stats(2.0), "alza": stats(1.0, "alza", None)}}
    por_codigo = alertas.evaluar_inventario(inventario, HOY, 7, analisis)
    assert alertas.resumir(por_codigo) == {
        "vencidos": 1, "por_vencer": 1, "sin_fecha": 0, "agotados": 1, "reponer": 1,
        "en_alza": 1, "con_alerta": 5, "total": 6, "sin_historial": False}


def test_resumen_sin_historial_en_todo_el_inventario():
    por_codigo = alertas.evaluar_inventario([producto()], HOY, 7, None)
    assert alertas.resumir(por_codigo)["sin_historial"] is True


# ----------------------------------------------------------------- integración
def csv_con_fechas(*filas):
    cab = "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n"
    hoy = datetime.date.today()
    return cab + "".join(
        f"{c},{n},{q},{t},{(hoy + datetime.timedelta(days=off)).isoformat()}\n"
        for c, n, q, t, off in filas)


INVENTARIO = csv_con_fechas(
    ("1", "Leche", 5, 1, -2),     # vencida
    ("2", "Yogur", 50, 1, 3),     # por vencer
    ("3", "Pan", 2, 2, 300),      # se vende 6/día: necesita 6 × 3 = 18 → sugerido 16
    ("4", "Sal", 99, 1, 300),     # se vende 1/día: sobra
    ("5", "Café", 0, 3, 300))     # agotado, 4/día → necesita 16

HISTORIAL = historial_csv(
    [(d, "3", 6) for d in range(14)] + [(d, "4", 1) for d in range(14)] + [(d, "5", 4) for d in range(14)])


def test_paginas_muestran_alertas_con_historial(client):
    subir(client, INVENTARIO)
    assert importar_historial(client, HISTORIAL).status_code == 302
    stock = client.get("/pedir_stock").get_data(as_text=True)
    assert 'badge text-bg-danger' in stock and "Vencido · 5 u.</span>" in stock   # insignia, no la leyenda
    assert "Vence en 3 d" in stock
    assert "Reponer · sugerido 16" in stock                                   # Pan y Café
    assert stock.count("Reponer · sugerido 16") == 2 and ">Sin stock</span>" in stock
    assert "1 vencido, 1 por vencer, 1 sin stock, 1 por reponer" in stock
    assert "sin historial" not in stock
    prov = client.get("/pedir_proveedor").get_data(as_text=True)
    assert "Reponer · sugerido 16" in prov and "Consumo/día" in prov
    home = client.get("/").get_data(as_text=True)
    assert "Atención" in home and "1 vencido" in home


def test_sin_historial_solo_avisa_de_agotados_y_lo_explica(client):
    subir(client, INVENTARIO)
    stock = client.get("/pedir_stock").get_data(as_text=True)
    assert "Reponer ·" not in stock                    # nada de sugeridos inventados
    assert ">Sin stock</span>" in stock                # el agotado sí se avisa
    assert "Aún no hay suficiente historial" in stock
    assert "OK · sin historial" in stock               # Sal: caducidad OK, reposición sin evaluar
    assert "Vencido · 5 u.</span>" in stock            # el vencimiento no depende del historial


def test_inicio_sin_alertas_muestra_confirmacion(client):
    subir(client, csv_con_fechas(("1", "Sal", 99, 1, 300)))
    importar_historial(client, historial_csv([(d, "1", 1) for d in range(14)]))
    home = client.get("/").get_data(as_text=True)
    assert "Sin alertas" in home and "Atención" not in home
    assert 'text-body-secondary">OK</span>' in client.get("/pedir_stock").get_data(as_text=True)


def test_inicio_sin_inventario_no_muestra_resumen(client):
    home = client.get("/").get_data(as_text=True)
    assert "Atención" not in home and "Sin alertas" not in home


def test_inventario_sin_fechas_funciona(client):
    subir(client, "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n1,A,5,1,\n")
    pagina = client.get("/pedir_stock").get_data(as_text=True)
    assert "—" in pagina and "badge text-bg-danger" not in pagina and "badge text-bg-warning" not in pagina
