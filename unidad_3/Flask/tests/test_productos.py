"""Pruebas de la gestión de productos: agregar, editar y quitar SIN borrar el resto del inventario."""

import re

import pytest

from conftest import JSON_HEADERS, historial_csv, importar_historial, subir
from services import productos as lg
from services.inventario import InventarioError


def prod(codigo="1", nombre="Manzana", cantidad=10, tiempo=2, fecha="2099-01-01"):
    return {"Código": codigo, "Nombre": nombre, "Cantidad": cantidad,
            "Tiempo entrega(Días)": tiempo, "Fecha límite": fecha}


def fila(**kw):
    base = {"Código": "N1", "Nombre": "Mango", "Cantidad": "5", "Tiempo entrega(Días)": "3", "Fecha límite": "2099-02-02"}
    base.update(kw)
    return base


# ------------------------------------------------------------- generar_codigo
def test_codigo_generado_tiene_seis_caracteres_alfanumericos_en_mayuscula():
    codigo = lg.generar_codigo([])
    assert re.fullmatch(r"[A-Z0-9]{6}", codigo)


def test_el_codigo_generado_evita_los_existentes():
    secuencia = iter("AAAAAA" + "BBBBBB")
    azar = lambda alfabeto: next(secuencia)          # noqa: E731  (primero "AAAAAA" y luego "BBBBBB", letra a letra)
    assert lg.generar_codigo(["AAAAAA"], longitud=6, azar=azar) == "BBBBBB"


def test_si_no_logra_un_codigo_unico_lo_dice():
    with pytest.raises(InventarioError, match="código único"):
        lg.generar_codigo(["AAAAAA"], azar=lambda alfabeto: "A")


# ------------------------------------------------------------------- agregar
def test_agregar_conserva_los_demas_sin_mutar_la_lista_original():
    original = [prod("1"), prod("2", "Banana")]
    nuevos, producto = lg.agregar_producto(original, fila())
    assert [p["Código"] for p in nuevos] == ["1", "2", "N1"] and len(original) == 2
    assert nuevos[:2] == original and producto["Nombre"] == "Mango" and producto["Cantidad"] == 5
    assert list(producto.keys()) == ["Código", "Nombre", "Cantidad", "Tiempo entrega(Días)", "Fecha límite", "Lotes"]
    assert producto["Lotes"] == [{"Fecha límite": "2099-02-02", "Cantidad": 5}]      # cantidad + fecha = primer lote


def test_el_codigo_vacio_se_genera_y_no_choca_con_los_existentes():
    nuevos, producto = lg.agregar_producto([prod("1")], fila(**{"Código": ""}))
    assert re.fullmatch(r"[A-Z0-9]{6}", producto["Código"]) and len(nuevos) == 2


@pytest.mark.parametrize("codigo", ["ñandú", "A-1", "x.y", "123", "A" * 30])
def test_codigos_nuevos_validos(codigo):
    assert lg.agregar_producto([], fila(**{"Código": codigo}))[1]["Código"] == codigo


@pytest.mark.parametrize("codigo", ["a b", "a/b", "a?b", "A" * 31, "a#b"])
def test_codigos_nuevos_invalidos(codigo):
    with pytest.raises(InventarioError, match="solo puede tener"):
        lg.agregar_producto([], fila(**{"Código": codigo}))


def test_un_codigo_repetido_se_rechaza():
    with pytest.raises(InventarioError, match="'1' ya existe"):
        lg.agregar_producto([prod("1")], fila(**{"Código": "1"}))


@pytest.mark.parametrize("cambio, texto", [
    ({"Nombre": "  "}, "nombre es obligatorio"),
    ({"Nombre": "x" * 81}, "80 caracteres"),
    ({"Cantidad": "-1"}, "Cantidad"),
    ({"Cantidad": "2.5"}, "Cantidad"),
    ({"Cantidad": ""}, "Cantidad"),
    ({"Tiempo entrega(Días)": "x"}, "Tiempo de entrega"),
    ({"Fecha límite": "01/02/2099"}, "Fecha límite"),
])
def test_validacion_de_campos(cambio, texto):
    with pytest.raises(InventarioError) as exc:
        lg.agregar_producto([], fila(**cambio))
    assert texto in str(exc.value)


def test_los_mensajes_no_llevan_numero_de_fila_y_empiezan_en_mayuscula():
    with pytest.raises(InventarioError) as exc:
        lg.agregar_producto([], fila(Nombre="", Cantidad="-1"))
    texto = " ".join(exc.value.errores)
    assert "Producto 1" not in texto and exc.value.errores[0][0].isupper()


def test_se_informan_a_la_vez_el_codigo_repetido_y_los_demas_errores():
    with pytest.raises(InventarioError) as exc:
        lg.agregar_producto([prod("1")], fila(**{"Código": "1"}, Cantidad="-3"))
    assert any("ya existe" in e for e in exc.value.errores) and any("Cantidad" in e for e in exc.value.errores)


def test_fila_desde_formulario_recorta_el_codigo_y_mapea_los_campos():
    f = lg.fila_desde_formulario({"codigo": "  ab ", "nombre": "N", "cantidad": "3",
                                  "tiempo_entrega": "2", "fecha_limite": "2099-01-01"})
    assert f == {"Código": "ab", "Nombre": "N", "Cantidad": "3", "Tiempo entrega(Días)": "2", "Fecha límite": "2099-01-01"}


# -------------------------------------------------------------------- editar
def test_editar_cambia_solo_ese_producto_y_conserva_posicion_y_codigo():
    original = [prod("1"), prod("2", "Banana"), prod("3", "Lechuga")]
    nuevos, editado = lg.editar_producto(original, "2", fila(**{"Código": "OTRO"}, Nombre="Banano"),
                                         [{"Fecha límite": "2099-05-01", "Cantidad": 99}])
    assert [p["Código"] for p in nuevos] == ["1", "2", "3"]                  # el código del formulario se ignora
    assert nuevos[1]["Nombre"] == "Banano" and nuevos[1]["Cantidad"] == 99 and editado == nuevos[1]
    assert nuevos[0] == original[0] and nuevos[2] == original[2] and original[1]["Nombre"] == "Banana"


def test_editar_un_producto_inexistente_o_con_datos_invalidos():
    with pytest.raises(InventarioError, match="no existe"):
        lg.editar_producto([prod("1")], "9", fila(), [])
    with pytest.raises(InventarioError, match="nombre es obligatorio"):
        lg.editar_producto([prod("1")], "1", fila(Nombre=" "), [])
    with pytest.raises(InventarioError, match="Tiempo de entrega"):
        lg.editar_producto([prod("1")], "1", fila(**{"Tiempo entrega(Días)": "x"}), [])


# ------------------------------------------------------------------ eliminar
def test_eliminar_quita_solo_ese_producto():
    original = [prod("1"), prod("2", "Banana"), prod("3", "Lechuga")]
    nuevos, quitado = lg.eliminar_producto(original, "2")
    assert [p["Código"] for p in nuevos] == ["1", "3"] and quitado["Nombre"] == "Banana" and len(original) == 3


def test_eliminar_el_ultimo_deja_la_lista_vacia_y_un_inexistente_falla():
    assert lg.eliminar_producto([prod("1")], "1")[0] == []
    with pytest.raises(InventarioError, match="no existe"):
        lg.eliminar_producto([prod("1")], "9")


# ---------------------------------------------------------------------- rutas
INV = ("Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n"
       "1,Manzana,15,3,2099-04-28\n2,Banana,2,5,2099-04-25\n3,Lechuga,7,2,2099-04-22\n")


def agregar(client, seguir=False, **campos):
    datos = {"codigo": "", "nombre": "Mango", "cantidad": "9", "tiempo_entrega": "2", "fecha_limite": "", **campos}
    return client.post("/productos", data=datos, follow_redirects=seguir)


def editar(client, codigo, seguir=False, lotes=(("2099-05-01", "20"),), **campos):
    """Edita un producto: nombre, tiempo de entrega y la lista de lotes (fecha, unidades)."""
    datos = {"nombre": "Banano", "tiempo_entrega": "5",
             "lote_fecha": [f for f, _ in lotes], "lote_cantidad": [c for _, c in lotes], **campos}
    return client.post(f"/productos/{codigo}/editar", data=datos, follow_redirects=seguir)


def inventario(client):
    return {p["Código"]: p for p in client.get("/export_json").get_json()}


def historial(client):
    return client.get("/export_movimientos").get_data(as_text=True).lstrip("\ufeff")


def test_agregar_editar_y_quitar_no_borran_lo_que_ya_hay(client):
    """La corrección pedida: gestionar productos desde la página nunca reemplaza el inventario."""
    subir(client, INV)
    importar_historial(client, historial_csv([(2, "1", 3), (1, "2", 1)]))
    antes = inventario(client)
    lineas_historial = historial(client)

    assert agregar(client, codigo="N1", nombre="Mango", cantidad="9").status_code == 302
    despues = inventario(client)
    assert set(despues) == {"1", "2", "3", "N1"} and all(despues[c] == antes[c] for c in antes)

    assert editar(client, "2").status_code == 302
    editado = inventario(client)
    assert editado["2"]["Nombre"] == "Banano" and editado["2"]["Cantidad"] == 20
    assert editado["1"] == antes["1"] and editado["3"] == antes["3"] and editado["N1"] == despues["N1"]

    assert client.post("/productos/3/eliminar").status_code == 302
    final = inventario(client)
    assert set(final) == {"1", "2", "N1"} and final["1"] == antes["1"] and final["N1"] == despues["N1"]
    assert historial(client) == lineas_historial                      # el historial no se tocó


def test_la_pagina_funciona_sin_inventario_y_el_primer_producto_lo_crea(client):
    pagina = client.get("/productos")
    assert pagina.status_code == 200 and "Todavía no hay productos" in pagina.get_data(as_text=True)
    assert 'href="/productos"' in client.get("/").get_data(as_text=True)         # el menú no la oculta
    r = agregar(client, codigo="A1", nombre="Limón")
    assert r.status_code == 302 and "Expires=" in r.headers["Set-Cookie"]        # sesión duradera
    assert list(inventario(client)) == ["A1"]
    assert "Limón" in client.get("/pedir_stock").get_data(as_text=True)          # el resto de la app ya lo ve


def test_agregar_con_errores_vuelve_a_mostrar_el_formulario_con_lo_escrito(client):
    subir(client, INV)
    r = agregar(client, codigo="1", nombre="Mi mango", cantidad="-4")
    pagina = r.get_data(as_text=True)
    assert r.status_code == 400 and "No se pudo guardar" in pagina and "ya existe" in pagina
    assert 'value="Mi mango"' in pagina and 'value="-4"' in pagina               # no se pierde lo escrito
    assert set(inventario(client)) == {"1", "2", "3"}                           # nada se guardó


def test_el_codigo_generado_se_informa_en_el_aviso(client):
    subir(client, INV)
    pagina = agregar(client, seguir=True, nombre="Mango").get_data(as_text=True)
    nuevo = next(c for c in inventario(client) if c not in {"1", "2", "3"})
    assert f"Producto «Mango» agregado con el código {nuevo}." in pagina


def test_agregar_un_codigo_con_historial_huerfano_lo_avisa(client):
    subir(client, INV)
    importar_historial(client, historial_csv([(d, "3", 2) for d in range(3)]))
    client.post("/productos/3/eliminar")
    pagina = agregar(client, seguir=True, codigo="3", nombre="Otra lechuga").get_data(as_text=True)
    assert "ya tenía 3 movimiento(s) en el historial" in pagina


def test_la_pagina_de_edicion_muestra_los_datos_y_bloquea_el_codigo(client):
    subir(client, INV)
    pagina = client.get("/productos/2/editar").get_data(as_text=True)
    assert 'value="Banana"' in pagina and 'value="2099-04-25"' in pagina and 'value="5"' in pagina
    assert re.search(r'name="codigo" value="2"[^>]*readonly', pagina)


def test_editar_actualiza_avisa_y_no_registra_movimientos(client):
    subir(client, INV)
    pagina = editar(client, "2", seguir=True).get_data(as_text=True)
    assert "Producto «Banano» actualizado." in pagina
    assert client.get("/export_movimientos").status_code == 302               # corregir stock no es un movimiento


def test_editar_con_errores_conserva_lo_escrito_y_no_guarda(client):
    subir(client, INV)
    r = editar(client, "2", nombre="Banano nuevo", lotes=(("2099-05-01", "x"),))
    pagina = r.get_data(as_text=True)
    assert r.status_code == 400 and "la cantidad debe ser un entero" in pagina and 'value="Banano nuevo"' in pagina
    assert 'value="x"' in pagina and 'value="2099-05-01"' in pagina               # también se conservan los lotes escritos
    assert inventario(client)["2"]["Nombre"] == "Banana"


def test_editar_o_quitar_un_producto_inexistente(client):
    subir(client, INV)
    assert client.get("/productos/9/editar", headers=JSON_HEADERS).status_code == 404
    assert editar(client, "9").status_code == 302                              # sin JS: aviso y vuelta a la lista
    assert client.post("/productos/9/eliminar", headers=JSON_HEADERS).status_code == 404


def test_quitar_con_cliente_js_responde_json_y_conserva_el_historial(client):
    subir(client, INV)
    importar_historial(client, historial_csv([(1, "2", 4)]))
    r = client.post("/productos/2/eliminar", headers=JSON_HEADERS)
    assert r.status_code == 200 and "historial de movimientos se conserva" in r.get_json()["message"]
    assert "2" not in inventario(client) and ",2,4,salida" in historial(client)


def test_quitar_el_ultimo_producto_conserva_el_inventario_y_el_historial(client):
    subir(client, "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n1,Manzana,15,3,2099-04-28\n")
    importar_historial(client, historial_csv([(1, "1", 2)]))
    client.post("/productos/1/eliminar")
    assert client.get("/export_json").get_json() == []                         # vacío, no 404
    assert "Todavía no hay productos" in client.get("/productos").get_data(as_text=True)
    assert 'href="/pedir_stock"' in client.get("/").get_data(as_text=True)     # el inventario sigue existiendo
    assert "No hay productos" in client.get("/pedir_stock").get_data(as_text=True)
    assert client.get("/export_csv").data.decode("utf-8-sig").strip().startswith("Código,Nombre")
    # al agregar de nuevo se sigue en el mismo inventario: el historial no se perdió
    agregar(client, codigo="1", nombre="Manzana nueva")
    assert list(inventario(client)) == ["1"] and ",1,2,salida" in historial(client)


def test_codigos_cargados_desde_csv_con_barra_espacio_o_acentos_se_pueden_editar_y_quitar(client):
    subir(client, "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n"
                  "A/B,Mesa,3,1,\nmesa 1,Silla,4,1,\nñandú,Ave,5,1,\n")
    pagina = client.get("/productos").get_data(as_text=True)
    enlaces = re.findall(r'href="(/productos/[^"]+/editar)"', pagina)
    assert len(enlaces) == 3
    for enlace in enlaces:
        assert client.get(enlace).status_code == 200
    assert client.post("/productos/A/B/eliminar").status_code == 302
    assert editar(client, "ñandú", nombre="Pájaro").status_code == 302
    assert set(inventario(client)) == {"mesa 1", "ñandú"} and inventario(client)["ñandú"]["Nombre"] == "Pájaro"


def test_los_nombres_con_html_o_comillas_se_escapan(client):
    agregar(client, codigo="X1", nombre="<b>negrita</b> y Bob's \"pizza\"")
    pagina = client.get("/productos").get_data(as_text=True)
    assert "<b>negrita</b>" not in pagina and "&lt;b&gt;negrita&lt;/b&gt;" in pagina
    assert "Bob\\u0027s" in pagina                          # la pregunta de confirmación no rompe el atributo


def test_la_lista_de_productos_muestra_el_estado_de_cada_uno(client):
    subir(client, "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n1,Leche,5,1,2000-01-01\n2,Sal,9,1,2099-01-01\n")
    pagina = client.get("/productos").get_data(as_text=True)
    assert 'class="table-danger"' in pagina and "Vencido · 5 u.</span>" in pagina and "(2 productos)" in pagina


# ------------------------------------------------- el CSV sigue reemplazando
def test_cargar_un_csv_reemplaza_el_inventario_pero_conserva_el_historial(client):
    subir(client, INV)
    agregar(client, codigo="N1", nombre="Mango")
    importar_historial(client, historial_csv([(1, "1", 3)]))
    subir(client, "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n1,Pera,4,1,\n")
    assert list(inventario(client)) == ["1"] and inventario(client)["1"]["Nombre"] == "Pera"   # reemplazó
    assert ",1,3,salida" in historial(client)                                                  # historial intacto


def test_la_pantalla_del_csv_avisa_que_reemplaza_solo_si_ya_hay_inventario(client):
    assert "subir un CSV lo reemplaza" not in client.get("/").get_data(as_text=True)
    subir(client, INV)
    pagina = client.get("/").get_data(as_text=True)
    assert "subir un CSV lo reemplaza" in pagina and 'href="/productos"' in pagina


# ------------------------------------------------------------ compatibilidad
def test_la_direccion_antigua_redirige_a_productos(client):
    r = client.get("/crear_inventario")
    assert r.status_code == 302 and r.headers["Location"].endswith("/productos")


def test_el_js_ya_no_contiene_la_pagina_de_creacion_antigua(client):
    js = client.get("/static/js/script.js").get_data(as_text=True)
    assert "crear_inventario" not in js and "inventarioCreadoUI" not in js and "sessionStorage" not in js
