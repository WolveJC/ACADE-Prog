"""Pruebas del registro de movimientos: validación, almacenamiento y rutas."""

import datetime
import os
import re
import time

import pytest

from conftest import JSON_HEADERS, historial_csv, importar_historial, subir
from services import movimientos as mv
from services.almacenamiento import AlmacenInventario
from services.inventario import InventarioError

HOY = datetime.date(2026, 6, 15)
CODIGOS = ["1", "2"]


def fila(**kw):
    base = {"fecha": "2026-06-10", "codigo": "1", "cantidad": "3", "evento": "0"}
    base.update(kw)
    return base


# ------------------------------------------------------------------ validación
def test_movimiento_valido_se_normaliza():
    r = mv.validar_movimientos([fila(cantidad="3.0", evento="sí")], CODIGOS, HOY)
    assert r == [{"fecha": datetime.date(2026, 6, 10), "codigo": "1", "cantidad": 3,
                  "tipo": "salida", "evento": True, "motivo": ""}]


@pytest.mark.parametrize("cambio, texto", [
    ({"fecha": "2026-06-16"}, "futura"),
    ({"fecha": "2026-13-01"}, "YYYY-MM-DD"),
    ({"fecha": "10/06/2026"}, "YYYY-MM-DD"),
    ({"fecha": "2026-6-1"}, "YYYY-MM-DD"),
    ({"fecha": ""}, "obligatoria"),
    ({"codigo": ""}, "obligatorio"),
    ({"codigo": "99"}, "no existe"),
    ({"cantidad": "0"}, "mayor que 0"),
    ({"cantidad": "-2"}, "mayor que 0"),
    ({"cantidad": "2.5"}, "mayor que 0"),
    ({"cantidad": "x"}, "mayor que 0"),
    ({"evento": "quizás"}, "evento"),
])
def test_movimientos_invalidos(cambio, texto):
    with pytest.raises(InventarioError) as exc:
        mv.validar_movimientos([fila(**cambio)], CODIGOS, HOY)
    assert texto in str(exc.value)


def test_se_reportan_todos_los_errores_con_su_fila():
    with pytest.raises(InventarioError) as exc:
        mv.validar_movimientos([fila(), fila(cantidad="0"), fila(codigo="99")], CODIGOS, HOY)
    assert "Fila 3" in str(exc.value) and "Fila 4" in str(exc.value) and len(exc.value.errores) == 2


@pytest.mark.parametrize("valor, esperado", [
    ("1", True), ("on", True), ("Sí", True), ("TRUE", True), ("x", True),
    ("", False), ("0", False), ("no", False), ("false", False), (None, False)])
def test_booleanos(valor, esperado):
    assert mv.a_booleano(valor) is esperado


def test_fecha_vacia_significa_hoy_y_la_futura_se_rechaza():
    assert mv.parsear_fecha("", HOY) == HOY
    with pytest.raises(ValueError):
        mv.parsear_fecha("2026-06-16", HOY)


# ------------------------------------------------------------------------- CSV
def test_csv_acepta_bom_punto_y_coma_latin1_y_evento_opcional():
    texto = "fecha;codigo;cantidad\n2026-06-10;1;4\n"
    assert mv.desde_csv_bytes(texto.encode("latin-1"), CODIGOS, HOY)[0]["evento"] is False
    con_bom = "\ufefffecha,codigo,cantidad,evento\n2026-06-10,2,1,1\n".encode("utf-8")
    assert mv.desde_csv_bytes(con_bom, CODIGOS, HOY)[0]["evento"] is True


def test_csv_sin_columnas_obligatorias_vacio_o_sin_filas():
    for malo in (b"a,b\n1,2\n", b"", b"fecha,codigo,cantidad\n"):
        with pytest.raises(InventarioError):
            mv.desde_csv_bytes(malo, CODIGOS, HOY)


def test_exportar_e_importar_es_un_ciclo_sin_perdidas():
    movs = mv.validar_movimientos([fila(), fila(fecha="2026-06-11", evento="1", cantidad="9")], CODIGOS, HOY)
    assert mv.desde_csv_bytes(mv.a_csv_texto(movs).encode(), CODIGOS, HOY) == movs


# ---------------------------------------------------------------- almacenamiento
def movs_ejemplo():
    return mv.validar_movimientos([fila(), fila(fecha="2026-06-11", codigo="2", evento="1")], CODIGOS, HOY)


def test_almacen_agrega_lee_reemplaza_y_borra(tmp_path):
    al = AlmacenInventario(tmp_path); inv = al.nuevo_id()
    assert al.leer_movimientos(inv) == []
    al.agregar_movimientos(inv, movs_ejemplo()); al.agregar_movimientos(inv, movs_ejemplo()[:1])
    assert len(al.leer_movimientos(inv)) == 3                       # se añaden, con una sola cabecera
    assert (tmp_path / f"{inv}.movimientos.csv").read_text().count("fecha,codigo") == 1
    al.reemplazar_movimientos(inv, movs_ejemplo()[:1])
    assert len(al.leer_movimientos(inv)) == 1
    al.borrar_movimientos(inv)
    assert al.leer_movimientos(inv) == []


def test_almacen_ignora_filas_danadas_e_ids_invalidos(tmp_path):
    al = AlmacenInventario(tmp_path); inv = al.nuevo_id()
    (tmp_path / f"{inv}.movimientos.csv").write_text(
        "fecha,codigo,cantidad,evento\n2026-06-10,1,3,0\nbasura\n2026-99-99,1,3,0\n2026-06-11,2,x,0\n", encoding="utf-8")
    assert len(al.leer_movimientos(inv)) == 1
    for malo in ("../../x", None, "", "abc"):
        assert al.leer_movimientos(malo) == []
    with pytest.raises(ValueError):
        al.agregar_movimientos("../x", movs_ejemplo())


def test_limpieza_y_eliminacion_incluyen_el_historial(tmp_path):
    al = AlmacenInventario(tmp_path); viejo, vivo = al.nuevo_id(), al.nuevo_id()
    al.agregar_movimientos(viejo, movs_ejemplo()); al.agregar_movimientos(vivo, movs_ejemplo())
    hace_dos_dias = time.time() - 2 * 86400
    os.utime(tmp_path / f"{viejo}.movimientos.csv", (hace_dos_dias, hace_dos_dias))
    assert al.limpiar_antiguos(1) == 1 and al.leer_movimientos(vivo) and not al.leer_movimientos(viejo)
    al.eliminar(vivo)
    assert not list(tmp_path.glob("*.movimientos.csv"))


# ------------------------------------------------------------------------ rutas
INV = "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n1,Manzana,20,2,2099-01-01\n2,Banana,5,2,2099-01-01\n"


@pytest.fixture
def con_inventario(client):
    assert subir(client, INV).status_code == 200
    return client


def retirar(client, **campos):
    datos = {"pedido_stock[1]": "4", **campos}
    return client.post("/pedir_stock", data=datos, headers=JSON_HEADERS)


def historial(client):
    return client.get("/export_movimientos").get_data(as_text=True).lstrip("\ufeff")


def test_pedir_stock_registra_la_retirada_con_fecha_de_hoy(con_inventario):
    assert retirar(con_inventario).status_code == 200
    assert f"{datetime.date.today().isoformat()},1,4,salida,0" in historial(con_inventario)


def test_pedir_stock_con_fecha_pasada_y_evento(con_inventario):
    r = retirar(con_inventario, fecha_movimiento="2026-01-05", es_evento="on")
    assert r.status_code == 200 and "2026-01-05,1,4,salida,1" in historial(con_inventario)


@pytest.mark.parametrize("campos", [{"fecha_movimiento": "2999-01-01"}, {"fecha_movimiento": "ayer"}, {"es_evento": "tal vez"}])
def test_pedir_stock_con_datos_invalidos_no_cambia_nada(con_inventario, campos):
    assert retirar(con_inventario, **campos).status_code == 400
    assert con_inventario.get("/export_json").get_json()[0]["Cantidad"] == 20
    assert con_inventario.get("/export_movimientos").status_code == 302     # sigue sin historial


def test_solo_se_registra_lo_que_realmente_se_retiro(con_inventario):
    r = con_inventario.post("/pedir_stock", headers=JSON_HEADERS,
                            data={"pedido_stock[1]": "4", "pedido_stock[2]": "99"})   # Banana: solo hay 5
    assert r.get_json()["hubo_cambios"] is True
    registro = historial(con_inventario)
    assert ",1,4,salida,0" in registro and ",2," not in registro
    assert con_inventario.get("/export_json").get_json()[1]["Cantidad"] == 5


def test_pedido_imposible_no_registra_movimientos(con_inventario):
    r = con_inventario.post("/pedir_stock", data={"pedido_stock[2]": "99"}, headers=JSON_HEADERS)
    assert r.get_json()["hubo_cambios"] is False
    assert con_inventario.get("/export_movimientos").status_code == 302


def test_el_historial_sobrevive_a_subir_otro_csv_y_la_cookie_es_duradera(client, app):
    r = subir(client, INV)
    assert "Expires=" in r.headers["Set-Cookie"]                       # sesión permanente, no de pestaña
    retirar(client)
    subir(client, INV.replace("Manzana", "Pera"))                      # cargar otro inventario
    assert ",1,4,salida,0" in historial(client)
    assert len(list(app.config["DATA_DIR"].glob("*.csv"))) == 2        # inventario + historial, sin huérfanos


def test_importar_reemplaza_el_historial_y_valida(con_inventario):
    importar_historial(con_inventario, historial_csv([(3, "1", 5), (2, "2", 1)]))
    assert historial(con_inventario).count("\n") == 3                  # cabecera + 2 filas
    importar_historial(con_inventario, historial_csv([(1, "1", 9)]))
    assert historial(con_inventario).count("\n") == 2                  # reemplazó, no sumó

    malo = importar_historial(con_inventario, historial_csv([(1, "99", 5)]), headers=JSON_HEADERS)
    assert malo.status_code == 400 and "no existe en el inventario" in malo.get_json()["message"]
    assert historial(con_inventario).count("\n") == 2                  # el error no tocó nada
    assert importar_historial(con_inventario, b"x", nombre="a.txt", headers=JSON_HEADERS).status_code == 400


def test_importar_sin_js_muestra_el_resultado_como_aviso(con_inventario):
    r = importar_historial(con_inventario, historial_csv([(1, "1", 2)]))
    assert r.status_code == 302
    assert "Historial importado: 1 movimientos" in con_inventario.get("/demanda").get_data(as_text=True)
    r = importar_historial(con_inventario, "a,b\n1,2\n")
    assert "debe contener las columnas" in con_inventario.get("/demanda").get_data(as_text=True)


def test_exportar_historial_en_csv_con_bom(con_inventario):
    assert con_inventario.get("/export_movimientos").status_code == 302
    retirar(con_inventario)
    r = con_inventario.get("/export_movimientos")
    assert r.data.startswith(b"\xef\xbb\xbffecha,codigo,cantidad,tipo,evento,motivo") and "attachment" in r.headers["Content-Disposition"]


def test_borrar_historial(con_inventario):
    retirar(con_inventario)
    r = con_inventario.post("/demanda/borrar", headers=JSON_HEADERS)
    assert r.status_code == 200 and con_inventario.get("/export_movimientos").status_code == 302


def test_sin_inventario_las_rutas_de_historial_redirigen_o_dan_409(client):
    assert client.get("/demanda").status_code == 302
    assert client.get("/export_movimientos").status_code == 302
    assert client.post("/demanda/importar", headers=JSON_HEADERS).status_code == 409
    assert client.post("/demanda/borrar", headers=JSON_HEADERS).status_code == 409
    assert "/demanda" not in client.get("/").get_data(as_text=True)    # el menú lo oculta


def test_pagina_demanda_historial_insuficiente_y_con_datos(con_inventario):
    pagina = con_inventario.get("/demanda").get_data(as_text=True)
    assert "Historial insuficiente" in pagina and "0 de los 7" in pagina

    # 14 días: producto 1 sube (2/día → 6/día), producto 2 estable; hay un evento enorme
    filas = [(d, "1", 6) for d in range(7)] + [(d, "1", 2) for d in range(7, 14)] + [(d, "2", 1) for d in range(14)]
    filas.append((3, "2", 400, 1))
    importar_historial(con_inventario, historial_csv(filas))
    pagina = con_inventario.get("/demanda").get_data(as_text=True)
    assert "Historial insuficiente" not in pagina and "Historial de 14 días" in pagina
    assert "↑ +200 %" in pagina                                        # 42 recientes vs 14 previos
    assert re.search(r"Banana.*?<td class=\"text-center\">1\.0</td>", pagina, re.S)   # el evento no cuenta
    assert ">400<" in pagina                                           # …pero se muestra como evento
    assert pagina.index("Manzana") < pagina.index("Banana")            # ordenado por popularidad
    assert "En alza" in con_inventario.get("/pedir_stock").get_data(as_text=True)
    assert "badge text-bg-secondary\">Evento" in pagina


def test_el_menu_enlaza_demanda_e_historial_con_inventario(con_inventario):
    pagina = con_inventario.get("/").get_data(as_text=True)
    assert 'href="/demanda"' in pagina and "/export_movimientos" in pagina
