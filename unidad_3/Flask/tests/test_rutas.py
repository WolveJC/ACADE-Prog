"""Pruebas de extremo a extremo con el cliente de pruebas de Flask."""

import re

from conftest import CSV_OK, JSON_HEADERS, subir


def test_errores_de_subida_llegan_al_js_como_error_no_como_exito(client):
    r = subir(client, "a,b\n1,2\n")  # columnas incorrectas
    assert r.status_code == 400 and "Faltan" in r.get_json()["message"]
    r = subir(client, CSV_OK, nombre="datos.txt")
    assert r.status_code == 400
    r = client.post("/", data={}, headers=JSON_HEADERS)
    assert r.status_code == 400


def test_subida_acepta_cualquier_content_type_de_csv(client):
    for tipo in ("text/csv", "application/vnd.ms-excel", "application/octet-stream"):
        assert subir(client, CSV_OK, tipo=tipo).status_code == 200, tipo


def test_nombre_malicioso_no_escribe_fuera_ni_se_usa_en_disco(client, app, tmp_path):
    r = subir(client, CSV_OK, nombre="../../../evil.csv")
    assert r.status_code == 200
    archivos = [p.name for p in app.config["DATA_DIR"].iterdir()]
    assert len(archivos) == 1 and re.fullmatch(r"[0-9a-f]{32}\.csv", archivos[0])
    assert not (tmp_path.parent / "evil.csv").exists()


def test_dos_sesiones_con_mismo_nombre_no_se_pisan(app):
    a, b = app.test_client(), app.test_client()
    subir(a, CSV_OK, nombre="inv.csv")
    subir(b, CSV_OK.replace("Manzana", "Pera"), nombre="inv.csv")
    assert "Manzana" in a.get("/export_json").get_data(as_text=True)
    assert "Pera" in b.get("/export_json").get_data(as_text=True)


def test_nueva_subida_reemplaza_y_borra_el_archivo_anterior(client, app):
    subir(client, CSV_OK); subir(client, CSV_OK)
    assert len(list(app.config["DATA_DIR"].glob("*.csv"))) == 1


def test_cookie_de_sesion_no_crece_con_el_inventario(client):
    filas = "".join(f"{i},Producto {i},10,2,2025-05-01\n" for i in range(1, 801))
    r = subir(client, "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n" + filas)
    assert r.status_code == 200
    set_cookie = r.headers.getlist("Set-Cookie")
    assert set_cookie and all(len(c) < 500 for c in set_cookie)  # límite real ~4096
    assert len(client.get("/export_json").get_json()) == 800


def crear_producto(client, **campos):
    """Agrega un producto desde la página «Productos» (formulario normal, sin JS)."""
    datos = {"codigo": "A1", "nombre": "Café molido", "cantidad": "10", "tiempo_entrega": "2",
             "fecha_limite": "2025-06-01", **campos}
    return client.post("/productos", data=datos)


def test_un_producto_creado_a_mano_funciona_en_todo_el_flujo(client):
    r = crear_producto(client)
    assert r.status_code == 302                                    # PRG: redirige a la lista
    assert "Café molido" in client.get("/pedir_stock").get_data(as_text=True)
    assert "Café molido" in client.get("/pedir_proveedor").get_data(as_text=True)
    r = client.post("/pedir_stock", data={"pedido_stock[A1]": "4"}, headers=JSON_HEADERS)
    assert r.get_json()["hubo_cambios"] is True
    assert client.get("/export_json").get_json()[0]["Cantidad"] == 6


def test_flujo_completo_hasta_pdf_con_caracteres_unicode(client):
    crear_producto(client, nombre="Crème brûlée — Ñandú €")
    r = client.post("/pedir_proveedor", headers=JSON_HEADERS,
                    data={"pedido_proveedor[A1]": "3", "precio_proveedor[A1]": "2.50"})
    assert r.status_code == 200
    pdf = client.get(r.get_json()["redirect_url"])
    assert pdf.status_code == 200 and pdf.data.startswith(b"%PDF")
    assert "attachment" in pdf.headers["Content-Disposition"]
    # el pedido se consume: una segunda descarga redirige con aviso
    assert client.get("/generar_pdf_proveedor").status_code == 302


def test_proveedor_errores_de_validacion(client):
    crear_producto(client)
    r = client.post("/pedir_proveedor", headers=JSON_HEADERS,
                    data={"pedido_proveedor[A1]": "3", "precio_proveedor[A1]": ""})
    assert r.status_code == 400 and r.get_json()["errors"]
    r = client.post("/pedir_proveedor", headers=JSON_HEADERS, data={"pedido_proveedor[A1]": "0"})
    assert r.status_code == 400


def test_sin_inventario_hay_aviso_visible_y_redireccion(client):
    r = client.get("/pedir_stock")
    assert r.status_code == 302
    pagina = client.get("/").get_data(as_text=True)  # el aviso llega como toast
    assert 'id="flash-data"' in pagina and "No hay inventario cargado" in pagina
    r = client.post("/pedir_stock", data={}, headers=JSON_HEADERS)
    assert r.status_code == 409


def test_enlaces_de_pedido_y_exportacion_solo_con_inventario(client):
    assert "pedir_stock" not in client.get("/").get_data(as_text=True)
    subir(client, CSV_OK)
    pagina = client.get("/").get_data(as_text=True)
    assert "/pedir_stock" in pagina and "/export_csv" in pagina


def test_exportaciones(client):
    assert client.get("/export_json").status_code == 404
    subir(client, CSV_OK)
    assert client.get("/export_csv").data.startswith("\ufeffCódigo".encode("utf-8"))
    assert "Código" in client.get("/export_json").get_data(as_text=True)  # sin escapes \u00f3


def test_archivo_demasiado_grande(app):
    app.config["MAX_CONTENT_LENGTH"] = 200
    r = subir(app.test_client(), CSV_OK * 20)
    assert r.status_code == 413 and "tamaño máximo" in r.get_json()["message"]


def test_sin_js_la_subida_redirige_con_flash(client):
    r = subir(client, "a,b\n1,2\n", headers={})  # navegador sin JS: sin cabeceras de fetch
    assert r.status_code == 302
    assert "Faltan" in client.get("/").get_data(as_text=True)


def test_secret_key_por_defecto_no_es_la_antigua(tmp_path):
    from config import Config
    assert Config.SECRET_KEY and Config.SECRET_KEY != "secret-key-default-insecure"
