"""Pruebas de las mermas: mercancía descartada (vencida, dañada...) que no cuenta como demanda."""

import datetime

import pytest

from conftest import JSON_HEADERS, historial_csv, importar_historial, subir
from services import demanda
from services import inventario as inv
from services import lotes as lotes_mod
from services import movimientos as mv
from services.almacenamiento import AlmacenInventario
from services.inventario import InventarioError

HOY = datetime.date(2026, 6, 15)
CODIGOS = ["1", "2"]


def dia(offset, base=HOY):
    return (base + datetime.timedelta(days=offset)).isoformat()


def producto(codigo="1", cantidad=10, fecha=None):
    return {"Código": codigo, "Nombre": f"P{codigo}", "Cantidad": cantidad,
            "Tiempo entrega(Días)": 2, "Fecha límite": fecha if fecha is not None else dia(30)}


# ------------------------------------------------------------- parsear_merma
def parsear(form):
    return inv.parsear_merma(form, CODIGOS)


def test_parsea_cantidad_y_motivo_por_lote_ignorando_lineas_vacias_o_en_cero():
    mermas, motivos, errores = parsear({
        "merma_cantidad[1@2026-07-01]": "4", "merma_motivo[1@2026-07-01]": "vencido",
        "merma_cantidad[1@2026-08-01]": "0", "merma_cantidad[2@2026-07-01]": "",
        "merma_motivo[2@2026-07-01]": "danado"})
    assert mermas == {("1", "2026-07-01"): 4} and motivos == {("1", "2026-07-01"): "vencido"} and not errores


def test_el_lote_sin_fecha_va_con_la_clave_vacia_y_el_motivo_por_defecto_es_otro():
    mermas, motivos, _ = parsear({"merma_cantidad[1@]": "2", "merma_cantidad[2@2026-07-01]": "1",
                                  "merma_motivo[2@2026-07-01]": " DANADO "})
    assert mermas == {("1", ""): 2, ("2", "2026-07-01"): 1}
    assert motivos == {("1", ""): "otro", ("2", "2026-07-01"): "danado"}


def test_un_codigo_con_arroba_se_separa_por_la_ultima_arroba():
    mermas, _, errores = inv.parsear_merma({"merma_cantidad[a@b@2026-07-01]": "1"}, ["a@b"])
    assert mermas == {("a@b", "2026-07-01"): 1} and not errores


@pytest.mark.parametrize("campos, texto", [
    ({"merma_cantidad[1@2026-07-01]": "x"}, "inválida"),
    ({"merma_cantidad[1@2026-07-01]": "1.5"}, "inválida"),
    ({"merma_cantidad[1@2026-07-01]": "-1"}, "negativa"),
    ({"merma_cantidad[9@2026-07-01]": "1"}, "no encontrado"),
    ({"merma_cantidad[1@15/07/2026]": "1"}, "YYYY-MM-DD"),
    ({"merma_cantidad[1]": "1"}, "Línea de merma inválida"),
    ({"merma_cantidad[1@2026-07-01]": "1", "merma_motivo[1@2026-07-01]": "robo"}, "motivo desconocido"),
])
def test_mermas_invalidas(campos, texto):
    assert texto in " ".join(parsear(campos)[2])


# -------------------------------------------------------------- aplicar_merma
def con_lotes(codigo="1", *lotes):
    return lotes_mod.construir_producto(
        codigo, f"P{codigo}", 2, [{"Fecha límite": f, "Cantidad": c} for f, c in lotes])


def lotes_de(p):
    return [(l["Fecha límite"], l["Cantidad"]) for l in p["Lotes"]]


def test_aplicar_merma_descuenta_del_lote_indicado_sin_tocar_los_demas_ni_mutar():
    original = [con_lotes("1", (dia(-2), 6), (dia(20), 30)), con_lotes("2", (dia(5), 7))]
    nuevos, mensajes = inv.aplicar_merma(original, {("1", dia(-2)): 4})
    assert lotes_de(nuevos[0]) == [(dia(-2), 2), (dia(20), 30)] and nuevos[1] == original[1]
    assert lotes_de(original[0]) == [(dia(-2), 6), (dia(20), 30)]
    assert "Descartados 4 P1 del lote" in mensajes[0] and "Nuevo stock: 32." in mensajes[0]


def test_descartar_todo_un_lote_lo_elimina_y_la_fecha_mostrada_pasa_al_siguiente():
    p = inv.aplicar_merma([con_lotes("1", (dia(-2), 6), (dia(20), 30))], {("1", dia(-2)): 6})[0][0]
    assert lotes_de(p) == [(dia(20), 30)] and p["Fecha límite"] == dia(20) and p["Cantidad"] == 30


def test_el_lote_sin_fecha_se_descarta_con_la_fecha_vacia():
    p = inv.aplicar_merma([con_lotes("1", (dia(5), 3), ("", 8))], {("1", ""): 8})[0][0]
    assert lotes_de(p) == [(dia(5), 3)]


def test_si_alguna_linea_falla_no_se_aplica_nada():
    original = [con_lotes("1", (dia(5), 10)), con_lotes("2", (dia(5), 3))]
    with pytest.raises(InventarioError) as exc:
        inv.aplicar_merma(original, {("1", dia(5)): 4, ("2", dia(5)): 5})      # la 1 sí podría; la 2 no
    assert "no se pueden descartar 5 (hay 3)" in str(exc.value)
    assert original[0]["Cantidad"] == 10 and original[1]["Cantidad"] == 3


def test_descartar_de_un_lote_que_no_existe_es_un_error():
    with pytest.raises(InventarioError, match="ese lote no existe"):
        inv.aplicar_merma([con_lotes("1", (dia(5), 10))], {("1", dia(6)): 1})


# ------------------------------------------------------- tipo y motivo en el historial
def fila(**kw):
    base = {"fecha": "2026-06-10", "codigo": "1", "cantidad": "3", "tipo": "merma"}
    base.update(kw)
    return base


def test_merma_con_motivo_por_defecto_y_motivos_validos():
    motivos = [mv.validar_movimientos([fila(**kw)], CODIGOS, HOY)[0]["motivo"]
               for kw in ({}, {"motivo": ""}, {"motivo": "vencido"}, {"motivo": "Danado"}, {"motivo": "otro"})]
    assert motivos == ["otro", "otro", "vencido", "danado", "otro"]


def test_el_motivo_solo_aplica_a_las_mermas():
    assert mv.validar_movimientos([fila(tipo="salida", motivo="vencido")], CODIGOS, HOY)[0]["motivo"] == ""
    assert mv.validar_movimientos([fila(tipo="entrada", motivo="x")], CODIGOS, HOY)[0]["motivo"] == ""


def test_motivo_desconocido_y_mermas_marcadas_como_evento_se_rechazan():
    with pytest.raises(InventarioError, match="motivo debe ser"):
        mv.validar_movimientos([fila(motivo="robo")], CODIGOS, HOY)
    with pytest.raises(InventarioError, match="una merma no puede ser un evento"):
        mv.validar_movimientos([fila(evento="1")], CODIGOS, HOY)


def test_exportar_e_importar_conserva_las_mermas_y_su_motivo():
    movs = mv.validar_movimientos([fila(motivo="vencido"), fila(tipo="salida", codigo="2")], CODIGOS, HOY)
    texto = mv.a_csv_texto(movs)
    assert "2026-06-10,1,3,merma,0,vencido" in texto and "2026-06-10,2,3,salida,0," in texto
    assert mv.desde_csv_bytes(texto.encode(), CODIGOS, HOY) == movs


def test_un_historial_de_cinco_columnas_se_migra_al_agregar_una_merma(tmp_path):
    al = AlmacenInventario(tmp_path); inv_id = al.nuevo_id()
    (tmp_path / f"{inv_id}.movimientos.csv").write_text(
        "fecha,codigo,cantidad,tipo,evento\n2026-06-10,1,4,salida,0\n2026-06-11,2,9,entrada,0\n", encoding="utf-8")
    al.agregar_movimientos(inv_id, mv.validar_movimientos([fila(motivo="vencido")], CODIGOS, HOY))
    texto = (tmp_path / f"{inv_id}.movimientos.csv").read_text(encoding="utf-8")
    assert texto.startswith("fecha,codigo,cantidad,tipo,evento,motivo\n") and texto.count("fecha,codigo") == 1
    movs = al.leer_movimientos(inv_id)
    assert [m["tipo"] for m in movs] == ["salida", "entrada", "merma"] and movs[2]["motivo"] == "vencido"


# ------------------------------------------------------------------- demanda
def m(atras, codigo, cantidad, tipo="salida"):
    return {"fecha": HOY - datetime.timedelta(days=atras), "codigo": codigo,
            "cantidad": cantidad, "tipo": tipo, "evento": False}


def test_las_mermas_no_son_demanda_ni_alargan_el_historial():
    solo_mermas = demanda.analizar([m(d, "1", 9, "merma") for d in range(20)], CODIGOS, HOY)
    assert solo_mermas["historial_dias"] == 0 and not solo_mermas["suficiente"]
    movs = [m(d, "1", 2) for d in range(14)] + [m(3, "1", 500, "merma")]
    p = demanda.analizar(movs, CODIGOS, HOY)["productos"]["1"]
    assert p["consumo_diario"] == 2.0 and p["total_ventana"] == 28 and p["ranking"] == 1
    assert p["ultima_salida"] == HOY


def test_las_mermas_se_cuentan_aparte_en_la_ventana_incluso_con_poco_historial():
    r = demanda.analizar([m(2, "1", 6, "merma"), m(5, "1", 4, "merma"), m(20, "1", 99, "merma")], CODIGOS, HOY)
    assert not r["suficiente"] and r["productos"]["1"]["unidades_merma"] == 10      # la de hace 20 días queda fuera
    assert r["productos"]["2"]["unidades_merma"] == 0


# --------------------------------------------------------------------- rutas
def hoy_mas(dias):
    return (datetime.date.today() + datetime.timedelta(days=dias)).isoformat()


VENCIDA, FRESCA = hoy_mas(-2), hoy_mas(40)


def inventario_csv(*filas):
    return "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n" + "".join(
        f"{c},{n},{q},2,{f}\n" for c, n, q, f in filas)


@pytest.fixture
def con_inventario(client):
    # Leche (1): un lote vencido de 5 u. y otro fresco de 30 u.  Yogur (2): un lote de 30 u.
    assert subir(client, inventario_csv(("1", "Leche", 5, VENCIDA), ("1", "Leche", 30, FRESCA),
                                        ("2", "Yogur", 30, FRESCA))).status_code == 200
    return client


def descartar(client, headers=None, **campos):
    datos = {f"merma_cantidad[1@{VENCIDA}]": "5", f"merma_motivo[1@{VENCIDA}]": "vencido", **campos}
    return client.post("/mermas", data=datos, headers=headers or {})


def producto_exportado(client, codigo):
    return next(p for p in client.get("/export_json").get_json() if p["Código"] == codigo)


def historial(client):
    return client.get("/export_movimientos").get_data(as_text=True).lstrip("\ufeff")


def test_la_pagina_de_mermas_muestra_una_fila_por_lote_y_prepara_el_descarte_de_lo_vencido(con_inventario):
    pagina = con_inventario.get("/mermas").get_data(as_text=True)
    assert pagina.count('name="merma_cantidad[') == 3                              # 2 lotes de Leche + 1 de Yogur
    assert f'name="merma_cantidad[1@{VENCIDA}]"' in pagina and f'name="merma_cantidad[2@{FRESCA}]"' in pagina
    assert "hay 5 unidad(es) en lotes vencidos" in pagina and "preparar=vencidos" in pagina
    assert 'value="5"' not in pagina                                               # sin preparar, nada se rellena solo
    preparada = con_inventario.get("/mermas?preparar=vencidos").get_data(as_text=True)
    assert 'value="5"' in preparada and 'value="30"' not in preparada              # solo el lote vencido, no el fresco
    assert 'value="vencido" selected' in preparada and "Se rellenó el descarte" in preparada
    assert 'value="danado" selected' in preparada                                  # en los demás, por defecto «dañado»


def test_sin_inventario_las_mermas_redirigen_o_dan_409(client):
    assert client.get("/mermas").status_code == 302
    assert client.post("/mermas", headers=JSON_HEADERS).status_code == 409
    assert 'href="/mermas"' not in client.get("/").get_data(as_text=True)          # el menú la oculta


def test_descartar_el_lote_vencido_no_toca_el_fresco(con_inventario):
    r = descartar(con_inventario)
    assert r.status_code == 302
    leche = producto_exportado(con_inventario, "1")
    assert [(l["Fecha límite"], l["Cantidad"]) for l in leche["Lotes"]] == [(FRESCA, 30)]
    assert leche["Cantidad"] == 30 and leche["Fecha límite"] == FRESCA             # la fecha mostrada pasó al lote fresco
    assert producto_exportado(con_inventario, "2")["Cantidad"] == 30
    assert f"{datetime.date.today().isoformat()},1,5,merma,0,vencido" in historial(con_inventario)
    pagina = con_inventario.get("/mermas").get_data(as_text=True)
    assert "Mermas registradas: 5 unidades de 1 producto(s). No cuentan como demanda." in pagina


def test_descartar_por_dano_un_lote_fresco_baja_solo_ese_lote(con_inventario):
    clave = f"2@{FRESCA}"
    r = con_inventario.post("/mermas", headers=JSON_HEADERS,
                            data={f"merma_cantidad[{clave}]": "3", f"merma_motivo[{clave}]": "danado"})
    assert r.status_code == 200 and r.get_json()["hubo_cambios"] is True
    assert producto_exportado(con_inventario, "2")["Cantidad"] == 27
    assert producto_exportado(con_inventario, "1")["Cantidad"] == 35               # el otro producto, intacto
    assert f"{datetime.date.today().isoformat()},2,3,merma,0,danado" in historial(con_inventario)


def test_descartar_con_fecha_pasada_queda_con_esa_fecha(con_inventario):
    assert descartar(con_inventario, headers=JSON_HEADERS, fecha_movimiento="2026-01-05").status_code == 200
    assert "2026-01-05,1,5,merma,0,vencido" in historial(con_inventario)


@pytest.mark.parametrize("campos, texto", [
    ({"merma_cantidad[1@" + VENCIDA + "]": ""}, "al menos un lote"),
    ({"merma_cantidad[1@" + VENCIDA + "]": "0"}, "al menos un lote"),
    ({"merma_cantidad[1@" + VENCIDA + "]": "6"}, "no se pueden descartar 6 (hay 5)"),
    ({"merma_cantidad[1@" + VENCIDA + "]": "x"}, "inválida"),
    ({"merma_cantidad[1@" + hoy_mas(3) + "]": "1"}, "ese lote no existe"),
    ({"merma_cantidad[77@]": "1"}, "no encontrado"),
    ({"merma_motivo[1@" + VENCIDA + "]": "robo"}, "motivo desconocido"),
    ({"fecha_movimiento": "2999-01-01"}, "futura"),
])
def test_descartes_invalidos_no_cambian_nada(con_inventario, campos, texto):
    # Salvo en los casos "ninguna cantidad", el Yogur lleva una línea válida: nada debe aplicarse (todo o nada)
    valida = {} if texto == "al menos un lote" else {f"merma_cantidad[2@{FRESCA}]": "3"}
    r = descartar(con_inventario, headers=JSON_HEADERS, **{**valida, **campos})
    assert r.status_code == 400 and texto in r.get_json()["message"]
    assert producto_exportado(con_inventario, "1")["Cantidad"] == 35 and producto_exportado(con_inventario, "2")["Cantidad"] == 30
    assert con_inventario.get("/export_movimientos").status_code == 302


def test_una_merma_no_infla_la_demanda_pero_una_retirada_si(con_inventario):
    subir(con_inventario, inventario_csv(("1", "Leche", 100, FRESCA)))
    importar_historial(con_inventario, historial_csv([(d, "1", 4) for d in range(14)]))   # 4 u./día × 14 d = 56
    descartar(con_inventario, **{f"merma_cantidad[1@{FRESCA}]": "20", f"merma_motivo[1@{FRESCA}]": "vencido",
                                 f"merma_cantidad[1@{VENCIDA}]": ""})
    pagina = con_inventario.get("/demanda").get_data(as_text=True)
    assert "4.0" in pagina and ">56<" in pagina                                     # consumo intacto
    assert '<td class="text-center">20</td>' in pagina                              # …y las 20 salen como merma
    assert "Merma · vencido" in pagina and "5.4" not in pagina

    # Las mismas 20 unidades registradas como una retirada normal SÍ distorsionan (76 u. / 14 d = 5.4)
    con_inventario.post("/pedir_stock", data={"pedido_stock[1]": "20"}, headers=JSON_HEADERS)
    assert "5.4" in con_inventario.get("/demanda").get_data(as_text=True)


def test_flujo_recibir_un_lote_fresco_con_unidades_vencidas_y_descartar_solo_lo_vencido(con_inventario):
    nueva = hoy_mas(10)
    con_inventario.post("/recepcion", data={"recepcion_cantidad[1]": "12", "recepcion_fecha[1]": nueva})
    leche = producto_exportado(con_inventario, "1")
    assert [l["Cantidad"] for l in leche["Lotes"]] == [5, 12, 30] and leche["Fecha límite"] == VENCIDA
    assert "Vencido · 5 u.</span>" in con_inventario.get("/pedir_stock").get_data(as_text=True)
    # Se descarta solo el lote vencido: los otros dos (42 u. frescas) no se tocan y el aviso desaparece.
    descartar(con_inventario)
    leche = producto_exportado(con_inventario, "1")
    assert [(l["Fecha límite"], l["Cantidad"]) for l in leche["Lotes"]] == [(nueva, 12), (FRESCA, 30)]
    assert leche["Fecha límite"] == nueva and leche["Cantidad"] == 42
    assert "Vencido ·" not in con_inventario.get("/pedir_stock").get_data(as_text=True)


def test_la_pagina_demanda_muestra_la_columna_la_insignia_y_el_total_de_mermas(con_inventario):
    descartar(con_inventario)
    pagina = con_inventario.get("/demanda").get_data(as_text=True)                 # historial aún insuficiente
    assert ">Mermas</th>" in pagina and 'badge text-bg-danger">Merma · vencido' in pagina
    importar_historial(con_inventario, historial_csv([(d, "2", 1) for d in range(1, 10)] + [(1, "1", 5, 0, "merma", "vencido")]))
    assert "1 mermas" in con_inventario.get("/demanda").get_data(as_text=True)     # el resumen aparece con historial suficiente


def test_importar_historial_con_mermas_no_cambia_el_stock(con_inventario):
    importar_historial(con_inventario, historial_csv([(2, "1", 3, 0, "merma", "danado"), (1, "1", 1)]))
    assert producto_exportado(con_inventario, "1")["Cantidad"] == 35
    assert "merma,0,danado" in historial(con_inventario)
    malo = importar_historial(con_inventario, historial_csv([(1, "1", 3, 0, "merma", "robo")]), headers=JSON_HEADERS)
    assert malo.status_code == 400 and "motivo debe ser" in malo.get_json()["message"]


def test_pedir_stock_remite_a_las_mermas_y_el_menu_las_enlaza(con_inventario):
    pagina = con_inventario.get("/pedir_stock").get_data(as_text=True)
    assert 'Descártala en <a href="/mermas">Mermas</a>' in pagina
    assert 'href="/mermas"' in con_inventario.get("/").get_data(as_text=True)
