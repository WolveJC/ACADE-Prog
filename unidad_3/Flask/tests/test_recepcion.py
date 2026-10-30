"""Pruebas de la recepción de mercancía (entradas de stock) y del tipo de movimiento."""

import datetime

import pytest

from conftest import JSON_HEADERS, historial_csv, importar_historial, subir
from services import demanda
from services import inventario as inv
from services import movimientos as mv
from services.almacenamiento import AlmacenInventario
from services.inventario import InventarioError

HOY = datetime.date(2026, 6, 15)
CODIGOS = ["1", "2"]


def producto(codigo="1", cantidad=10, fecha="2026-12-01"):
    return {"Código": codigo, "Nombre": f"P{codigo}", "Cantidad": cantidad,
            "Tiempo entrega(Días)": 2, "Fecha límite": fecha}


# ------------------------------------------------------- parsear_recepcion
def parsear(form, fecha=HOY):
    return inv.parsear_recepcion(form, CODIGOS, fecha)


def test_parsea_cantidades_y_fechas_ignorando_lineas_vacias_o_en_cero():
    recibidos, fechas, errores = parsear({
        "recepcion_cantidad[1]": "5", "recepcion_fecha[1]": "2026-07-01",
        "recepcion_cantidad[2]": "0", "recepcion_fecha[2]": "2026-07-01"})   # 0 → se ignora con su fecha
    assert recibidos == {"1": 5} and fechas == {"1": "2026-07-01"} and not errores


def test_una_fecha_sin_cantidad_se_ignora_y_la_cantidad_acepta_decimales_enteros():
    recibidos, fechas, errores = parsear({"recepcion_fecha[1]": "2026-07-01", "recepcion_cantidad[2]": "3.0"})
    assert recibidos == {"2": 3} and fechas == {} and not errores


@pytest.mark.parametrize("campos, texto", [
    ({"recepcion_cantidad[1]": "x"}, "inválida"),
    ({"recepcion_cantidad[1]": "2.5"}, "inválida"),
    ({"recepcion_cantidad[1]": "-2"}, "negativa"),
    ({"recepcion_cantidad[99]": "2"}, "no encontrado"),
    ({"recepcion_cantidad[1]": "2", "recepcion_fecha[1]": "01/07/2026"}, "YYYY-MM-DD"),
    ({"recepcion_cantidad[1]": "2", "recepcion_fecha[1]": "2026-06-14"}, "anterior a la recepción"),
])
def test_recepciones_invalidas(campos, texto):
    assert texto in " ".join(parsear(campos)[2])


def test_la_fecha_limite_puede_ser_el_mismo_dia_de_la_recepcion():
    assert parsear({"recepcion_cantidad[1]": "2", "recepcion_fecha[1]": "2026-06-15"})[2] == []


# -------------------------------------------------------- aplicar_recepcion
def lotes_de(p):
    return [(l["Fecha límite"], l["Cantidad"]) for l in p["Lotes"]]


def test_la_recepcion_suma_al_stock_sin_mutar_el_original():
    original = [producto(cantidad=10)]
    nuevos, mensajes = inv.aplicar_recepcion(original, {"1": 5}, {})
    assert nuevos[0]["Cantidad"] == 15 and original[0]["Cantidad"] == 10
    assert "Nuevo stock: 15" in mensajes[0] and "sin fecha de caducidad" in mensajes[0]


@pytest.mark.parametrize("fecha_vieja, fecha_nueva, lotes, proxima", [
    ("2026-12-01", "2027-03-01", [("2026-12-01", 10), ("2027-03-01", 3)], "2026-12-01"),  # el nuevo caduca después
    ("2026-12-01", "2026-09-01", [("2026-09-01", 3), ("2026-12-01", 10)], "2026-09-01"),  # el nuevo caduca antes
    ("2026-12-01", "2026-12-01", [("2026-12-01", 13)], "2026-12-01"),                     # misma fecha: se suma
    ("2026-12-01", "", [("2026-12-01", 10), ("", 3)], "2026-12-01"),                      # sin fecha: lote aparte
    ("", "2026-09-01", [("2026-09-01", 3), ("", 10)], "2026-09-01"),                      # antes no tenía fecha
])
def test_recibir_crea_un_lote_y_se_muestra_siempre_la_fecha_mas_proxima(
        fecha_vieja, fecha_nueva, lotes, proxima):
    nuevos, mensajes = inv.aplicar_recepcion(
        [producto(cantidad=10, fecha=fecha_vieja)], {"1": 3}, {"1": fecha_nueva} if fecha_nueva else {})
    assert lotes_de(nuevos[0]) == lotes and nuevos[0]["Fecha límite"] == proxima
    assert ("Lote con fecha límite" in mensajes[0]) is bool(fecha_nueva)


def test_recibir_en_un_producto_sin_stock_no_hereda_la_fecha_vieja():
    nuevos, _ = inv.aplicar_recepcion([producto(cantidad=0, fecha="2000-01-01")], {"1": 4}, {"1": "2026-09-01"})
    assert lotes_de(nuevos[0]) == [("2026-09-01", 4)] and nuevos[0]["Fecha límite"] == "2026-09-01"


def test_solo_cambian_los_productos_recibidos():
    nuevos, _ = inv.aplicar_recepcion([producto("1"), producto("2", cantidad=7)], {"1": 1}, {})
    assert [p["Cantidad"] for p in nuevos] == [11, 7]


# ------------------------------------------------------- tipo de movimiento
def fila(**kw):
    base = {"fecha": "2026-06-10", "codigo": "1", "cantidad": "3"}
    base.update(kw)
    return base


def test_tipo_por_defecto_es_salida_y_se_acepta_en_cualquier_capitalizacion():
    tipos = [mv.validar_movimientos([fila(**kw)], CODIGOS, HOY)[0]["tipo"]
             for kw in ({}, {"tipo": ""}, {"tipo": "salida"}, {"tipo": "ENTRADA"}, {"tipo": " Entrada "})]
    assert tipos == ["salida", "salida", "salida", "entrada", "entrada"]


def test_tipo_desconocido_y_entradas_marcadas_como_evento_se_rechazan():
    with pytest.raises(InventarioError, match="salida, entrada o merma"):
        mv.validar_movimientos([fila(tipo="compra")], CODIGOS, HOY)
    with pytest.raises(InventarioError, match="no puede ser un evento"):
        mv.validar_movimientos([fila(tipo="entrada", evento="1")], CODIGOS, HOY)


def test_un_historial_antiguo_de_cuatro_columnas_se_importa_como_salidas():
    antiguo = b"fecha,codigo,cantidad,evento\n2026-06-10,1,4,0\n2026-06-11,2,9,1\n"
    movs = mv.desde_csv_bytes(antiguo, CODIGOS, HOY)
    assert [m["tipo"] for m in movs] == ["salida", "salida"] and movs[1]["evento"] is True


def test_exportar_e_importar_conserva_las_entradas():
    movs = mv.validar_movimientos([fila(), fila(tipo="entrada", cantidad="50", codigo="2")], CODIGOS, HOY)
    texto = mv.a_csv_texto(movs)
    assert "2026-06-10,2,50,entrada,0" in texto
    assert mv.desde_csv_bytes(texto.encode(), CODIGOS, HOY) == movs


def test_las_entradas_no_cuentan_como_demanda_ni_como_historial():
    def m(atras, codigo, cantidad, tipo="salida"):
        return {"fecha": HOY - datetime.timedelta(days=atras), "codigo": codigo,
                "cantidad": cantidad, "tipo": tipo, "evento": False}
    solo_entradas = demanda.analizar([m(d, "1", 100, "entrada") for d in range(20)], CODIGOS, HOY)
    assert solo_entradas["historial_dias"] == 0 and not solo_entradas["suficiente"]

    mezcla = [m(d, "1", 2) for d in range(14)] + [m(d, "1", 500, "entrada") for d in range(14)]
    p = demanda.analizar(mezcla, CODIGOS, HOY)["productos"]["1"]
    assert p["consumo_diario"] == 2.0 and p["total_ventana"] == 28
    assert p["ultima_salida"] == HOY            # solo cuenta como retirada la última salida


# ------------------------------------------------- migración del historial
def test_un_historial_guardado_antes_de_existir_tipo_se_migra_al_agregar(tmp_path):
    al = AlmacenInventario(tmp_path); inv_id = al.nuevo_id()
    (tmp_path / f"{inv_id}.movimientos.csv").write_text(
        "fecha,codigo,cantidad,evento\n2026-06-10,1,4,0\n2026-06-11,2,9,1\n", encoding="utf-8")
    assert [m["tipo"] for m in al.leer_movimientos(inv_id)] == ["salida", "salida"]   # se lee tal cual

    al.agregar_movimientos(inv_id, mv.validar_movimientos([fila(tipo="entrada", cantidad="7")], CODIGOS, HOY))
    texto = (tmp_path / f"{inv_id}.movimientos.csv").read_text(encoding="utf-8")
    assert texto.startswith("fecha,codigo,cantidad,tipo,evento,motivo\n") and texto.count("fecha,codigo") == 1
    assert "2026-06-11,2,9,salida,1" in texto and "2026-06-10,1,7,entrada,0" in texto
    assert len(al.leer_movimientos(inv_id)) == 3


# ----------------------------------------------------------------- rutas
INV = ("Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n"
       "1,Manzana,20,2,2099-01-01\n2,Banana,0,2,2099-01-01\n")


@pytest.fixture
def con_inventario(client):
    assert subir(client, INV).status_code == 200
    return client


def recibir(client, headers=None, **campos):
    datos = {"recepcion_cantidad[1]": "5", **campos}
    return client.post("/recepcion", data=datos, headers=headers or {})


def stock(client):
    return {p["Código"]: p["Cantidad"] for p in client.get("/export_json").get_json()}


def historial(client):
    return client.get("/export_movimientos").get_data(as_text=True).lstrip("\ufeff")


def test_la_pagina_de_recepcion_lista_los_productos(con_inventario):
    pagina = con_inventario.get("/recepcion").get_data(as_text=True)
    assert "Recepción de mercancía" in pagina and 'name="recepcion_cantidad[1]"' in pagina
    assert 'name="recepcion_fecha[2]"' in pagina and "Banana" in pagina


def test_sin_inventario_la_recepcion_redirige_o_da_409(client):
    assert client.get("/recepcion").status_code == 302
    assert client.post("/recepcion", headers=JSON_HEADERS).status_code == 409
    assert "/recepcion" not in client.get("/").get_data(as_text=True)      # el menú la oculta


def test_recibir_suma_stock_guarda_la_entrada_y_avisa(con_inventario):
    r = recibir(con_inventario, **{"recepcion_cantidad[2]": "8"})
    assert r.status_code == 302                                        # formulario normal: flash + redirección
    assert stock(con_inventario) == {"1": 25, "2": 8}
    assert f"{datetime.date.today().isoformat()},1,5,entrada,0" in historial(con_inventario)
    pagina = con_inventario.get("/recepcion").get_data(as_text=True)
    assert "Recepción registrada: 13 unidades de 2 producto(s)." in pagina   # el aviso llega como toast


def test_recibir_con_cliente_js_responde_json(con_inventario):
    r = recibir(con_inventario, headers=JSON_HEADERS)
    assert r.status_code == 200 and r.get_json()["hubo_cambios"] is True and r.get_json()["detalles"]


def test_recibir_con_fecha_pasada_queda_con_esa_fecha(con_inventario):
    recibir(con_inventario, fecha_movimiento="2026-01-05")
    assert "2026-01-05,1,5,entrada,0" in historial(con_inventario)


@pytest.mark.parametrize("campos, texto", [
    ({"recepcion_cantidad[1]": ""}, "al menos un producto"),
    ({"recepcion_cantidad[1]": "0"}, "al menos un producto"),
    ({"recepcion_cantidad[1]": "x"}, "inválida"),
    ({"recepcion_cantidad[1]": "-3"}, "negativa"),
    ({"recepcion_cantidad[77]": "3"}, "no encontrado"),
    ({"fecha_movimiento": "2999-01-01"}, "futura"),
    ({"fecha_movimiento": "ayer"}, "YYYY-MM-DD"),
    ({"recepcion_fecha[1]": "2000-01-01"}, "anterior a la recepción"),
])
def test_recepciones_invalidas_no_cambian_nada(con_inventario, campos, texto):
    r = recibir(con_inventario, headers=JSON_HEADERS, **campos)
    assert r.status_code == 400 and texto in r.get_json()["message"]
    assert stock(con_inventario) == {"1": 20, "2": 0}
    assert con_inventario.get("/export_movimientos").status_code == 302    # sigue sin historial


def producto_exportado(client, codigo):
    return next(p for p in client.get("/export_json").get_json() if p["Código"] == codigo)


def test_los_lotes_a_traves_de_las_rutas(con_inventario):
    # Manzana (1): 20 u. con fecha 2099-01-01. Banana (2): sin stock.
    recibir(con_inventario, **{"recepcion_fecha[1]": "2099-06-01"})
    manzana = producto_exportado(con_inventario, "1")
    assert [(l["Fecha límite"], l["Cantidad"]) for l in manzana["Lotes"]] == [("2099-01-01", 20), ("2099-06-01", 5)]
    assert manzana["Fecha límite"] == "2099-01-01" and manzana["Cantidad"] == 25   # la más próxima, aunque llegó una más lejana

    recibir(con_inventario, **{"recepcion_fecha[1]": "2098-06-01"})                # caduca antes: pasa a mostrarse esa
    assert producto_exportado(con_inventario, "1")["Fecha límite"] == "2098-06-01"

    recibir(con_inventario, **{"recepcion_fecha[1]": "2099-06-01"})                # misma fecha: se suma al lote
    lotes = {l["Fecha límite"]: l["Cantidad"] for l in producto_exportado(con_inventario, "1")["Lotes"]}
    assert lotes == {"2098-06-01": 5, "2099-01-01": 20, "2099-06-01": 10}

    recibir(con_inventario, **{"recepcion_cantidad[1]": "", "recepcion_cantidad[2]": "4",
                               "recepcion_fecha[2]": "2099-03-03"})                # estaba en 0: el lote nuevo es el único
    banana = producto_exportado(con_inventario, "2")
    assert [(l["Fecha límite"], l["Cantidad"]) for l in banana["Lotes"]] == [("2099-03-03", 4)]


def test_recibir_sin_fecha_se_registra_pero_avisa_siempre(con_inventario):
    r = recibir(con_inventario, headers=JSON_HEADERS)
    datos = r.get_json()
    assert r.status_code == 200 and datos["sin_fecha"] == ["Manzana"]
    assert "falta la fecha de caducidad de Manzana" in datos["message"] and "seguirá avisando" in datos["message"]
    assert "Sin fecha · 5 u.</span>" in con_inventario.get("/recepcion").get_data(as_text=True)   # y el aviso permanece
    r = recibir(con_inventario, headers=JSON_HEADERS, **{"recepcion_fecha[1]": "2099-03-03"})
    assert r.get_json()["sin_fecha"] == [] and "falta la fecha" not in r.get_json()["message"]


def test_recibir_resuelve_la_alerta_de_reponer_y_no_altera_la_demanda(con_inventario):
    importar_historial(con_inventario, historial_csv([(d, "1", 4) for d in range(14)]))
    antes = con_inventario.get("/pedir_stock").get_data(as_text=True)
    assert "Reponer · sugerido" not in antes                        # 20 u. cubren 4/día × (2+1)
    con_inventario.post("/pedir_stock", data={"pedido_stock[1]": "18"}, headers=JSON_HEADERS)
    # La retirada de hoy también cuenta: (14 días × 4 + 18) / 14 = 5.3 u./día → necesita 5.3 × 3 = 15.9; quedan 2
    assert "Reponer · sugerido 14" in con_inventario.get("/pedir_stock").get_data(as_text=True)
    recibir(con_inventario, **{"recepcion_cantidad[1]": "100"})
    despues = con_inventario.get("/pedir_stock").get_data(as_text=True)
    assert "Reponer · sugerido" not in despues
    # la entrada de 100 no infló el consumo: sigue en 74 u. / 14 d = 5.3 (solo cuentan las retiradas)
    demanda_html = con_inventario.get("/demanda").get_data(as_text=True)
    assert "5.3" in demanda_html and ">Entrada<" in demanda_html


def test_la_pagina_demanda_cuenta_entradas_aparte(con_inventario):
    recibir(con_inventario)
    pagina = con_inventario.get("/demanda").get_data(as_text=True)
    assert "0 retiradas registradas" in pagina and 'badge text-bg-success">Entrada' in pagina


def test_el_inventario_exportado_ya_no_tiene_demanda(con_inventario):
    assert "Demanda" not in con_inventario.get("/export_csv").get_data(as_text=True)
    assert all("Demanda" not in p for p in con_inventario.get("/export_json").get_json())


def test_el_pedido_al_proveedor_enlaza_con_la_recepcion_y_el_menu_tambien(con_inventario):
    assert "/recepcion" in con_inventario.get("/pedir_proveedor").get_data(as_text=True)
    assert 'href="/recepcion"' in con_inventario.get("/").get_data(as_text=True)


def test_importar_historial_con_entradas_no_cambia_el_stock(con_inventario):
    importar_historial(con_inventario, historial_csv([(3, "1", 50, 0, "entrada"), (2, "1", 5)]))
    assert stock(con_inventario) == {"1": 20, "2": 0}
    assert historial(con_inventario).count("entrada") == 1
