"""Pruebas de lotes: unidades que comparten fecha de caducidad, FEFO, descarte automático y aviso de fecha faltante."""

import datetime
import random
import threading

import pytest

from conftest import JSON_HEADERS, historial_csv, importar_historial, subir
from services import alertas
from services import lotes as L
from services.almacenamiento import AlmacenInventario

HOY = datetime.date(2026, 6, 15)


def dia(offset, base=HOY):
    return (base + datetime.timedelta(days=offset)).isoformat()


def hoy_mas(offset):
    return dia(offset, datetime.date.today())


def prod(codigo="1", *lotes, tiempo=2):
    return L.construir_producto(codigo, f"P{codigo}", tiempo, [{"Fecha límite": f, "Cantidad": c} for f, c in lotes])


def ver(p):
    return [(l["Fecha límite"], l["Cantidad"]) for l in p["Lotes"]]


# ------------------------------------------------------------- construcción
def test_normalizar_une_fechas_iguales_descarta_vacios_y_ordena_dejando_los_sin_fecha_al_final():
    lotes = L.normalizar_lotes([
        {"Fecha límite": dia(20), "Cantidad": 5}, {"Fecha límite": "", "Cantidad": 4},
        {"Fecha límite": dia(5), "Cantidad": 3}, {"Fecha límite": dia(20), "Cantidad": 7},
        {"Fecha límite": dia(9), "Cantidad": 0}])
    assert [(l["Fecha límite"], l["Cantidad"]) for l in lotes] == [(dia(5), 3), (dia(20), 12), ("", 4)]


def test_el_producto_muestra_el_total_y_la_fecha_mas_proxima_aunque_haya_otras_mas_lejanas():
    p = prod("1", (dia(40), 20), (dia(5), 10))
    assert p["Cantidad"] == 30 and p["Fecha límite"] == dia(5)
    assert list(p.keys()) == ["Código", "Nombre", "Cantidad", "Tiempo entrega(Días)", "Fecha límite", "Lotes"]


def test_un_producto_solo_con_lotes_sin_fecha_o_sin_stock_no_tiene_fecha_proxima():
    assert prod("1", ("", 8))["Fecha límite"] == "" and prod("1")["Cantidad"] == 0 and prod("1")["Lotes"] == []


def test_un_producto_plano_cuenta_como_un_unico_lote():
    plano = {"Código": "1", "Nombre": "X", "Cantidad": 7, "Tiempo entrega(Días)": 2, "Fecha límite": dia(3)}
    assert L.lotes_de(plano) == [{"Fecha límite": dia(3), "Cantidad": 7}]
    assert L.lotes_de({**plano, "Cantidad": 0}) == []
    assert L.stock_total(plano) == 7 and L.unidades_sin_fecha({**plano, "Fecha límite": ""}) == 7


# -------------------------------------------------------------------- FEFO
def test_consumir_toma_primero_el_lote_que_caduca_antes_y_pasa_al_siguiente():
    p = prod("1", (dia(5), 10), (dia(20), 30), ("", 4))
    q = L.consumir_fefo(p, 12)
    assert ver(q) == [(dia(20), 28), ("", 4)] and q["Fecha límite"] == dia(20) and q["Cantidad"] == 32
    assert ver(p) == [(dia(5), 10), (dia(20), 30), ("", 4)]                       # el original no cambia


def test_el_lote_sin_fecha_se_consume_el_ultimo():
    q = L.consumir_fefo(prod("1", (dia(5), 2), ("", 4)), 5)
    assert ver(q) == [("", 1)]


def test_consumir_mas_de_lo_que_hay_falla():
    with pytest.raises(ValueError):
        L.consumir_fefo(prod("1", (dia(5), 3)), 4)


def test_fefo_con_muchos_casos_aleatorios_conserva_las_unidades_y_el_orden():
    azar = random.Random(7)
    for _ in range(300):
        lotes = [(dia(azar.choice([-3, 0, 2, 5, 9, 20, 40])) if azar.random() > .2 else "", azar.randint(1, 9))
                 for _ in range(azar.randint(1, 5))]
        p = prod("1", *lotes)
        pedido = azar.randint(0, p["Cantidad"])
        q = L.consumir_fefo(p, pedido)
        assert q["Cantidad"] == p["Cantidad"] - pedido                               # se descuenta exactamente lo pedido
        fechas = [l["Fecha límite"] for l in q["Lotes"]]
        assert fechas == sorted(fechas, key=lambda f: (f == "", f)) and len(set(fechas)) == len(fechas)
        # lo que se consumió salió de los lotes que caducaban antes: si queda algo de un lote, no queda
        # ningún lote anterior (con fecha) intacto o parcial más viejo que uno ya agotado
        antes = {l["Fecha límite"]: l["Cantidad"] for l in p["Lotes"]}
        despues = {l["Fecha límite"]: l["Cantidad"] for l in q["Lotes"]}
        tocados = [f for f in antes if despues.get(f, 0) != antes[f]]
        if tocados:
            orden = [l["Fecha límite"] for l in p["Lotes"]]
            ultimo = max(orden.index(f) for f in tocados)
            assert all(despues.get(f, 0) == 0 for f in orden[:ultimo])               # todo lo anterior se agotó


# ------------------------------------------------------ agregar y quitar de un lote
def test_agregar_lote_suma_a_la_misma_fecha_o_crea_otro():
    p = prod("1", (dia(5), 10))
    assert ver(L.agregar_lote(p, dia(5), 3)) == [(dia(5), 13)]
    assert ver(L.agregar_lote(p, dia(2), 3)) == [(dia(2), 3), (dia(5), 10)]
    assert ver(L.agregar_lote(p, "", 3)) == [(dia(5), 10), ("", 3)]


def test_quitar_de_un_lote_concreto():
    p = prod("1", (dia(5), 10), (dia(20), 30))
    assert ver(L.quitar_de_lote(p, dia(5), 10)) == [(dia(20), 30)]
    assert ver(L.quitar_de_lote(p, dia(20), 4)) == [(dia(5), 10), (dia(20), 26)]
    with pytest.raises(ValueError, match="no tiene tantas"):
        L.quitar_de_lote(p, dia(5), 11)
    with pytest.raises(ValueError, match="no existe"):
        L.quitar_de_lote(p, dia(6), 1)


# ---------------------------------------------------------- vencimiento y descarte
def test_el_ultimo_dia_todavia_se_puede_vender_y_se_vence_al_dia_siguiente():
    assert not L.esta_vencido({"Fecha límite": dia(0), "Cantidad": 1}, HOY)
    assert L.esta_vencido({"Fecha límite": dia(-1), "Cantidad": 1}, HOY)
    assert not L.esta_vencido({"Fecha límite": "", "Cantidad": 1}, HOY)


def test_descartar_vencidos_quita_solo_los_lotes_vencidos_y_los_informa():
    original = [prod("1", (dia(-2), 5), (dia(10), 30)), prod("2", (dia(-1), 8)), prod("3", (dia(0), 4), ("", 2))]
    nuevos, descartes = L.descartar_vencidos(original, HOY)
    assert ver(nuevos[0]) == [(dia(10), 30)] and nuevos[1]["Cantidad"] == 0 and nuevos[1]["Lotes"] == []
    assert nuevos[2] is original[2]                                                 # vence hoy: todavía vendible
    assert descartes == [{"codigo": "1", "nombre": "P1", "cantidad": 5, "fecha_limite": dia(-2)},
                         {"codigo": "2", "nombre": "P2", "cantidad": 8, "fecha_limite": dia(-1)}]
    assert ver(original[0]) == [(dia(-2), 5), (dia(10), 30)]                        # el original no cambia


def test_sin_nada_vencido_no_se_descarta_nada():
    original = [prod("1", (dia(0), 5), ("", 3))]
    nuevos, descartes = L.descartar_vencidos(original, HOY)
    assert descartes == [] and nuevos[0] is original[0]


# ------------------------------------------------------------------ a_filas
def test_a_filas_genera_una_fila_por_lote_y_una_con_cero_para_el_producto_sin_stock():
    filas = L.a_filas([prod("1", (dia(5), 10), ("", 3)), prod("2")])
    assert [(f["Código"], f["Cantidad"], f["Fecha límite"]) for f in filas] == [
        ("1", 10, dia(5)), ("1", 3, ""), ("2", 0, "")]


# ---------------------------------------------------------------- almacenamiento
def test_guardar_y_cargar_conserva_lotes_y_productos_sin_stock(tmp_path):
    al = AlmacenInventario(tmp_path); inv_id = al.nuevo_id()
    original = [prod("1", (dia(5), 10), (dia(20), 30), ("", 2)), prod("2"), prod("3", (dia(1), 4))]
    al.guardar(inv_id, original)
    cargado = al.cargar(inv_id)
    assert [p["Código"] for p in cargado] == ["1", "2", "3"] and cargado == original
    assert cargado[1]["Lotes"] == [] and cargado[1]["Cantidad"] == 0


def test_un_inventario_guardado_con_una_fila_por_producto_sigue_cargando(tmp_path):
    al = AlmacenInventario(tmp_path); inv_id = al.nuevo_id()
    (tmp_path / f"{inv_id}.csv").write_text(
        f"Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n1,Manzana,15,3,{dia(9)}\n2,Sal,4,1,\n", encoding="utf-8")
    p1, p2 = al.cargar(inv_id)
    assert ver(p1) == [(dia(9), 15)] and ver(p2) == [("", 4)]


# ------------------------------------------------------------------- alertas
def evaluar(p, stats=None, aviso=7):
    return alertas.evaluar_producto(p, HOY, aviso, stats)


def test_vencimiento_por_lote_con_sus_unidades():
    a = evaluar(prod("1", (dia(-3), 5), (dia(4), 12), (dia(30), 40)))
    assert a["vencimiento"] == "vencido" and a["unidades_vencidas"] == 5 and a["dias_restantes"] == -3
    assert a["dias_por_vencer"] == 4 and a["unidades_por_vencer"] == 12           # también avisa del siguiente lote
    assert a["proxima_fecha"] == dia(-3) and a["unidades_proximo"] == 5


def test_la_fecha_mostrada_es_la_del_lote_mas_proximo_aunque_haya_mercancia_con_fecha_lejana():
    a = evaluar(prod("1", (dia(60), 100), (dia(5), 3)))
    assert a["proxima_fecha"] == dia(5) and a["unidades_proximo"] == 3 and a["vencimiento"] == "por_vencer"


def test_el_dia_limite_cuenta_como_por_vencer_con_cero_dias_y_un_lote_lejano_no_avisa():
    assert evaluar(prod("1", (dia(0), 2)))["dias_por_vencer"] == 0
    a = evaluar(prod("1", (dia(60), 9)))
    assert a["dias_por_vencer"] is None and a["vencimiento"] is None and not a["con_alerta"]


def test_la_falta_de_fecha_avisa_siempre_si_hay_stock_y_no_si_no_lo_hay():
    a = evaluar(prod("1", (dia(60), 5), ("", 3)))
    assert a["sin_fecha"] and a["unidades_sin_fecha"] == 3 and a["con_alerta"]
    assert evaluar(prod("1", ("", 4)))["sin_fecha"] and evaluar(prod("1", ("", 4)))["proxima_fecha"] == ""
    assert not evaluar(prod("1"))["sin_fecha"]                                     # sin stock no hay nada que avisar


def test_la_reposicion_solo_cuenta_el_stock_vigente():
    stats = {"consumo_diario": 5.0, "tendencia": None, "variacion": None}
    # necesita 5 × (2 + 1) = 15. Con 20 u. alcanzaría, pero 8 están vencidas: vigentes 12 < 15.
    a = evaluar(prod("1", (dia(-2), 8), (dia(60), 12)), stats)
    assert a["reponer"] and a["sugerido"] == 3 and a["cobertura"] == 2.4
    assert not evaluar(prod("1", (dia(60), 20)), stats)["reponer"]


def test_el_resumen_cuenta_los_productos_sin_fecha():
    por_codigo = alertas.evaluar_inventario(
        [prod("1", ("", 3)), prod("2", (dia(60), 3)), prod("3", ("", 1), (dia(60), 1))], HOY)
    assert alertas.resumir(por_codigo)["sin_fecha"] == 2


# ===================================================================== rutas
def csv_lotes(*filas):
    return "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n" + "".join(
        f"{c},{n},{q},{t},{f}\n" for c, n, q, t, f in filas)


INV = csv_lotes(("1", "Leche", 10, 2, hoy_mas(5)), ("1", "Leche", 30, 2, hoy_mas(20)), ("2", "Sal", 9, 3, ""))


def exportado(client, codigo):
    return next(p for p in client.get("/export_json").get_json() if p["Código"] == codigo)


def historial(client):
    return client.get("/export_movimientos").get_data(as_text=True).lstrip("\ufeff")


def test_un_csv_con_el_mismo_codigo_en_varias_filas_carga_los_lotes_de_un_producto(client):
    r = subir(client, INV)
    datos = r.get_json()
    assert r.status_code == 200 and "2 productos" in datos["message"]
    leche = exportado(client, "1")
    assert [(l["Fecha límite"], l["Cantidad"]) for l in leche["Lotes"]] == [(hoy_mas(5), 10), (hoy_mas(20), 30)]
    assert leche["Cantidad"] == 40 and leche["Fecha límite"] == hoy_mas(5)


def test_cargar_un_producto_sin_fecha_funciona_pero_avisa(client):
    datos = subir(client, INV).get_json()
    assert datos["sin_fecha"] == ["Sal"]
    assert "falta la fecha de caducidad de 1 producto(s) (Sal)" in datos["message"] and "seguirá avisando" in datos["message"]
    assert subir(client, csv_lotes(("1", "Leche", 5, 2, hoy_mas(3)))).get_json()["sin_fecha"] == []


def test_un_csv_con_el_mismo_codigo_y_otro_nombre_se_rechaza(client):
    r = subir(client, csv_lotes(("1", "Leche", 5, 2, hoy_mas(3)), ("1", "Yogur", 5, 2, hoy_mas(9))))
    assert r.status_code == 400 and "Fila 3" in r.get_json()["message"] and "repetido" in r.get_json()["message"]


def test_la_exportacion_csv_tiene_una_fila_por_lote_y_se_puede_volver_a_cargar(client):
    subir(client, INV)
    texto = client.get("/export_csv").data.decode("utf-8-sig")
    assert texto.splitlines() == [
        "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite",
        f"1,Leche,10,2,{hoy_mas(5)}", f"1,Leche,30,2,{hoy_mas(20)}", "2,Sal,9,3,"]
    antes = client.get("/export_json").get_json()
    subir(client, texto)                                                            # el CSV exportado es una plantilla válida
    assert client.get("/export_json").get_json() == antes


def test_la_exportacion_json_anida_los_lotes_y_conserva_los_campos_planos(client):
    subir(client, INV)
    leche = exportado(client, "1")
    assert list(leche.keys()) == ["Código", "Nombre", "Cantidad", "Tiempo entrega(Días)", "Fecha límite", "Lotes"]
    assert exportado(client, "2")["Lotes"] == [{"Fecha límite": "", "Cantidad": 9}]


def test_las_paginas_muestran_la_fecha_mas_proxima_y_cuantos_lotes_hay(client):
    subir(client, INV)
    for ruta in ("/pedir_stock", "/recepcion", "/productos"):
        pagina = client.get(ruta).get_data(as_text=True)
        assert hoy_mas(5) in pagina and "· 10 u." in pagina and "2 lotes" in pagina, ruta


def test_el_aviso_de_fecha_faltante_es_permanente_hasta_que_se_indica(client):
    subir(client, INV)
    for ruta in ("/pedir_stock", "/productos", "/recepcion", "/mermas"):
        assert "Sin fecha" in client.get(ruta).get_data(as_text=True), ruta
    assert "1 sin fecha de caducidad" in client.get("/pedir_stock").get_data(as_text=True)      # en el banner
    assert "1 sin fecha de caducidad" in client.get("/").get_data(as_text=True)
    client.post("/productos/2/editar", data={"nombre": "Sal", "tiempo_entrega": "3",
                                             "lote_fecha": [hoy_mas(300)], "lote_cantidad": ["9"]})
    assert "Sin fecha" not in client.get("/pedir_stock").get_data(as_text=True).replace("Sin fecha:", "")


# ---------------------------------------------------------- productos y lotes
def agregar(client, **campos):
    datos = {"codigo": "", "nombre": "Mango", "cantidad": "9", "tiempo_entrega": "2", "fecha_limite": "", **campos}
    return client.post("/productos", data=datos, follow_redirects=True).get_data(as_text=True)


def editar(client, codigo, lotes, **campos):
    datos = {"nombre": "Leche", "tiempo_entrega": "2",
             "lote_fecha": [f for f, _ in lotes], "lote_cantidad": [c for _, c in lotes], **campos}
    return client.post(f"/productos/{codigo}/editar", data=datos, follow_redirects=True)


def test_agregar_un_producto_sin_fecha_lo_registra_y_avisa(client):
    pagina = agregar(client, codigo="M1")
    assert "Producto «Mango» agregado" in pagina and "no tiene fecha de caducidad" in pagina
    assert "no tiene fecha de caducidad" not in agregar(client, codigo="M2", nombre="Pera", fecha_limite=hoy_mas(9))


def test_agregar_con_cantidad_cero_no_crea_lote_ni_aviso(client):
    pagina = agregar(client, codigo="M1", cantidad="0")
    assert "no tiene fecha de caducidad" not in pagina and exportado(client, "M1")["Lotes"] == []


def test_la_pagina_de_edicion_lista_los_lotes_y_ofrece_dos_filas_en_blanco(client):
    subir(client, INV)
    pagina = client.get("/productos/1/editar").get_data(as_text=True)
    assert pagina.count('name="lote_fecha"') == 4 and pagina.count('name="lote_cantidad"') == 4   # 2 lotes + 2 en blanco
    assert f'value="{hoy_mas(5)}"' in pagina and 'value="30"' in pagina
    assert 'name="cantidad"' not in pagina and 'name="fecha_limite"' not in pagina               # el stock se edita en los lotes


def test_editar_lotes_une_fechas_iguales_quita_los_de_cero_y_anade_los_nuevos(client):
    subir(client, INV)
    antes_sal = exportado(client, "2")
    editar(client, "1", [(hoy_mas(20), "4"), (hoy_mas(20), "6"), (hoy_mas(9), "0"), ("", ""), (hoy_mas(60), "7")])
    leche = exportado(client, "1")
    assert [(l["Fecha límite"], l["Cantidad"]) for l in leche["Lotes"]] == [(hoy_mas(20), 10), (hoy_mas(60), 7)]
    assert leche["Cantidad"] == 17 and exportado(client, "2") == antes_sal         # el resto no se toca


def test_editar_un_lote_sin_fecha_se_acepta_pero_avisa(client):
    subir(client, INV)
    pagina = editar(client, "1", [("", "5")]).get_data(as_text=True)
    assert "actualizado" in pagina and "no tiene fecha de caducidad" in pagina
    assert exportado(client, "1")["Lotes"] == [{"Fecha límite": "", "Cantidad": 5}]


@pytest.mark.parametrize("lotes, texto", [
    ([("31/12/2099", "5")], "formato YYYY-MM-DD"),
    ([(hoy_mas(5), "-1")], "la cantidad debe ser un entero"),
    ([(hoy_mas(5), "x")], "la cantidad debe ser un entero"),
    ([(hoy_mas(5), "")], "la cantidad debe ser un entero"),
])
def test_editar_con_lotes_invalidos_no_guarda_y_conserva_lo_escrito(client, lotes, texto):
    subir(client, INV)
    r = editar(client, "1", lotes, nombre="Leche nueva")
    pagina = r.get_data(as_text=True)
    assert texto in pagina and 'value="Leche nueva"' in pagina
    assert exportado(client, "1")["Cantidad"] == 40 and exportado(client, "1")["Nombre"] == "Leche"


def test_editar_el_nombre_y_los_lotes_mal_a_la_vez_informa_de_ambos_errores(client):
    subir(client, INV)
    pagina = editar(client, "1", [(hoy_mas(5), "-1")], nombre=" ").get_data(as_text=True)
    assert "nombre es obligatorio" in pagina and "la cantidad debe ser un entero" in pagina


# --------------------------------------------------------- retirada por caducidad
def test_la_retirada_sale_del_lote_que_caduca_antes_y_pasa_al_siguiente(client):
    subir(client, INV)
    r = client.post("/pedir_stock", data={"pedido_stock[1]": "12"}, headers=JSON_HEADERS)
    assert r.status_code == 200 and r.get_json()["hubo_cambios"] is True
    leche = exportado(client, "1")
    assert [(l["Fecha límite"], l["Cantidad"]) for l in leche["Lotes"]] == [(hoy_mas(20), 28)]
    assert leche["Fecha límite"] == hoy_mas(20) and leche["Cantidad"] == 28        # la fecha mostrada avanzó
    assert f"{datetime.date.today().isoformat()},1,12,salida,0" in historial(client)


def test_retirar_mas_de_lo_que_hay_en_total_no_cambia_nada(client):
    subir(client, INV)
    r = client.post("/pedir_stock", data={"pedido_stock[1]": "41"}, headers=JSON_HEADERS)
    assert r.get_json()["hubo_cambios"] is False and "Stock insuficiente" in " ".join(r.get_json()["detalles"])
    assert exportado(client, "1")["Cantidad"] == 40


# ============================================================ descarte automático
INV_VENCIDO = csv_lotes(("1", "Leche", 5, 2, hoy_mas(-2)), ("1", "Leche", 30, 2, hoy_mas(10)),
                        ("2", "Yogur", 8, 2, hoy_mas(-1)), ("3", "Pan", 4, 2, hoy_mas(0)))


def merma_lineas(client):
    return [l for l in historial(client).splitlines() if ",merma," in l]


def test_los_lotes_vencidos_se_descartan_solos_y_se_registran_como_mermas_por_vencimiento(client_con_descarte):
    c = client_con_descarte
    assert subir(c, INV_VENCIDO).status_code == 200
    pagina = c.get("/productos").get_data(as_text=True)                             # el primer uso lo detecta
    assert "El sistema descartó automáticamente 13 unidad(es) vencidas" in pagina
    assert f"Leche (5 u., vencidas el {hoy_mas(-2)})" in pagina and f"Yogur (8 u., vencidas el {hoy_mas(-1)})" in pagina
    assert "Quedaron registradas como mermas por vencimiento" in pagina

    leche = exportado(c, "1")
    assert [(l["Fecha límite"], l["Cantidad"]) for l in leche["Lotes"]] == [(hoy_mas(10), 30)]    # el lote fresco, intacto
    assert exportado(c, "2")["Cantidad"] == 0 and exportado(c, "2")["Lotes"] == []                # sigue existiendo, sin stock
    assert exportado(c, "3")["Cantidad"] == 4                                                     # vence hoy: aún se vende
    hoy = datetime.date.today().isoformat()
    assert sorted(merma_lineas(c)) == [f"{hoy},1,5,merma,0,vencido", f"{hoy},2,8,merma,0,vencido"]


def test_el_descarte_automatico_no_se_repite_ni_vuelve_a_avisar(client_con_descarte):
    c = client_con_descarte
    subir(c, INV_VENCIDO)
    c.get("/productos")
    assert len(merma_lineas(c)) == 2
    pagina = c.get("/productos").get_data(as_text=True)
    assert "descartó automáticamente" not in pagina and len(merma_lineas(c)) == 2


def test_cualquier_ruta_que_lee_el_inventario_dispara_el_descarte(client_con_descarte):
    c = client_con_descarte
    subir(c, INV_VENCIDO)
    assert exportado(c, "1")["Cantidad"] == 30                                      # bastó con exportar
    assert len(merma_lineas(c)) == 2


def test_un_lote_que_vence_hoy_no_se_descarta(client_con_descarte):
    c = client_con_descarte
    subir(c, csv_lotes(("1", "Pan", 4, 2, hoy_mas(0))))
    c.get("/productos")
    assert exportado(c, "1")["Cantidad"] == 4 and merma_lineas(c) == []


def test_ya_no_se_ve_la_alerta_de_vencido_porque_el_sistema_lo_retira(client_con_descarte):
    c = client_con_descarte
    subir(c, INV_VENCIDO)
    pagina = c.get("/pedir_stock").get_data(as_text=True)
    assert "Vencido ·" not in pagina and 'class="table-danger"' not in pagina


def test_lo_descartado_automaticamente_no_cuenta_como_demanda(client_con_descarte):
    c = client_con_descarte
    subir(c, csv_lotes(("1", "Leche", 100, 2, hoy_mas(40))))
    importar_historial(c, historial_csv([(d, "1", 4) for d in range(14)]))           # 4 u./día × 14 d
    # Entra a editarse un lote que ya está vencido (20 u.): al volver a la lista el sistema lo retira solo.
    c.post("/productos/1/editar", data={"nombre": "Leche", "tiempo_entrega": "2",
                                        "lote_fecha": [hoy_mas(-1), hoy_mas(40)], "lote_cantidad": ["20", "100"]},
           follow_redirects=True)
    assert exportado(c, "1")["Cantidad"] == 100 and len(merma_lineas(c)) == 1
    pagina = c.get("/demanda").get_data(as_text=True)
    assert "4.0" in pagina and ">56<" in pagina and "5.4" not in pagina              # consumo intacto
    assert '<td class="text-center">20</td>' in pagina and "Merma · vencido" in pagina


def test_con_muchos_lotes_vencidos_el_aviso_se_resume(client_con_descarte):
    c = client_con_descarte
    subir(c, csv_lotes(*[(str(i), f"P{i}", 2, 1, hoy_mas(-1)) for i in range(1, 8)]))
    pagina = c.get("/productos").get_data(as_text=True)
    assert "descartó automáticamente 14 unidad(es)" in pagina and "y 2 lote(s) más" in pagina
    assert len(merma_lineas(c)) == 7                                                 # todos se registran, aunque el aviso resuma


def test_con_el_descarte_apagado_los_lotes_vencidos_se_conservan_y_se_avisan(client):
    subir(client, INV_VENCIDO)
    pagina = client.get("/pedir_stock").get_data(as_text=True)
    assert "Vencido · 5 u.</span>" in pagina and exportado(client, "1")["Cantidad"] == 35 and merma_lineas(client) == []


def test_el_descarte_automatico_esta_activado_por_defecto():
    from config import Config
    assert Config.DESCARTE_AUTOMATICO_VENCIDOS is True


def test_el_descarte_es_seguro_con_peticiones_simultaneas(app_con_descarte):
    from routes import comun
    cli = app_con_descarte.test_client()
    subir(cli, INV_VENCIDO)
    almacen = app_con_descarte.extensions["almacen"]
    inv_id = next(almacen.directorio.glob("*.csv")).stem
    productos = almacen.cargar(inv_id)                                               # todavía con los lotes vencidos

    def tarea():
        with app_con_descarte.test_request_context():
            comun._descartar_vencidos(inv_id, productos)

    hilos = [threading.Thread(target=tarea) for _ in range(10)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    mermas = [m for m in almacen.leer_movimientos(inv_id) if m["tipo"] == "merma"]
    assert len(mermas) == 2 and sum(m["cantidad"] for m in mermas) == 13             # una sola vez, no diez
    assert almacen.cargar(inv_id)[0]["Cantidad"] == 30
