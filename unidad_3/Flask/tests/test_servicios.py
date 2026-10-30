"""Pruebas de la lógica de negocio (sin Flask)."""

import pytest

from services import inventario as inv
from services.almacenamiento import AlmacenInventario
from services.inventario import InventarioError


def fila(**kw):
    base = {"Código": "1", "Nombre": "X", "Cantidad": "5",
            "Tiempo entrega(Días)": "2", "Fecha límite": "2025-01-31"}
    base.update(kw)
    return base


def test_csv_ignora_columnas_extra_y_acepta_punto_y_coma_y_latin1():
    texto = "Fecha Consulta;Código;Nombre;Cantidad;Tiempo entrega(Días);Fecha límite\n" \
            "x;1;Piña colada;4;2;2025-04-28\n"
    productos = inv.desde_csv_bytes(texto.encode("latin-1"))
    assert productos[0]["Nombre"] == "Piña colada"


def test_csv_antiguo_con_columna_demanda_sigue_cargando_pero_se_descarta():
    texto = "Código,Nombre,Cantidad,Demanda,Tiempo entrega(Días),Fecha límite\n1,Manzana,15,8,3,2025-04-28\n"
    productos = inv.desde_csv_bytes(texto.encode("utf-8"))
    assert list(productos[0].keys()) == inv.COLUMNAS + ["Lotes"] and "Demanda" not in productos[0]


def test_csv_acepta_bom_utf8():
    texto = "\ufeffCódigo,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n1,A,1,1,\n"
    assert inv.desde_csv_bytes(texto.encode("utf-8"))[0]["Fecha límite"] == ""


@pytest.mark.parametrize("cambio", [
    {"Cantidad": "-1"}, {"Cantidad": "abc"}, {"Cantidad": "2.5"}, {"Tiempo entrega(Días)": "x"},
    {"Tiempo entrega(Días)": "-2"}, {"Fecha límite": "28/04/2025"}, {"Fecha límite": "2025-02-30"},
    {"Nombre": " "}, {"Código": ""},
])
def test_validacion_rechaza_valores_invalidos(cambio):
    with pytest.raises(InventarioError):
        inv.validar_filas([fila(**cambio)])


def test_el_mismo_codigo_en_varias_filas_son_lotes_del_mismo_producto():
    productos = inv.validar_filas([fila(Cantidad="4", **{"Fecha límite": "2025-03-01"}),
                                   fila(Cantidad="6", **{"Fecha límite": "2025-02-01"}),
                                   fila(**{"Código": "2"})])
    assert [p["Código"] for p in productos] == ["1", "2"]            # un producto por código, en orden
    assert productos[0]["Lotes"] == [{"Fecha límite": "2025-02-01", "Cantidad": 6},
                                     {"Fecha límite": "2025-03-01", "Cantidad": 4}]   # ordenados por caducidad
    assert productos[0]["Cantidad"] == 10 and productos[0]["Fecha límite"] == "2025-02-01"


def test_las_filas_con_el_mismo_codigo_y_la_misma_fecha_se_suman_en_un_solo_lote():
    p = inv.validar_filas([fila(Cantidad="4"), fila(Cantidad="6")])[0]
    assert p["Lotes"] == [{"Fecha límite": "2025-01-31", "Cantidad": 10}]


def test_un_codigo_repetido_con_otro_nombre_o_tiempo_de_entrega_es_un_error_con_su_fila():
    with pytest.raises(InventarioError) as exc:
        inv.validar_filas([fila(), fila(Nombre="Otro")])
    assert "Fila 3" in str(exc.value) and "repetido" in str(exc.value) and "nombre" in str(exc.value)
    with pytest.raises(InventarioError, match="tiempo de entrega"):
        inv.validar_filas([fila(), fila(**{"Tiempo entrega(Días)": "9"})])


def test_una_fila_con_cantidad_cero_deja_el_producto_sin_lotes():
    p = inv.validar_filas([fila(Cantidad="0")])[0]
    assert p["Lotes"] == [] and p["Cantidad"] == 0 and p["Fecha límite"] == ""


def test_csv_vacio_o_sin_filas():
    for contenido in (b"", b"   \n", "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n".encode()):
        with pytest.raises(InventarioError):
            inv.desde_csv_bytes(contenido)


def test_pedido_stock_descuenta_sin_mutar_el_original():
    productos = inv.validar_filas([fila(Cantidad="10")])
    nuevos, msgs, cambios = inv.aplicar_pedido_stock(productos, {"1": 4})
    assert cambios and nuevos[0]["Cantidad"] == 6
    assert list(nuevos[0].keys()) == inv.COLUMNAS + ["Lotes"]   # ya no se guarda ninguna "demanda" en el producto
    assert productos[0]["Cantidad"] == 10


def test_pedido_stock_insuficiente_y_codigo_inexistente():
    productos = inv.validar_filas([fila(Cantidad="2")])
    nuevos, msgs, cambios = inv.aplicar_pedido_stock(productos, {"1": 5, "99": 1})
    assert not cambios and nuevos[0]["Cantidad"] == 2
    assert any("insuficiente" in m for m in msgs) and any("99" in m for m in msgs)


def test_proveedor_rechaza_precio_cero_nan_e_inf_y_conserva_orden():
    productos = inv.validar_filas([fila(Código="b", Nombre="B"), fila(Código="a", Nombre="A")])
    for precio in ("0", "nan", "inf", "-1", "x"):
        _, errores = inv.validar_pedido_proveedor(
            productos, {"pedido_proveedor[a]": "2", "precio_proveedor[a]": precio})
        assert errores, precio
    pedido, errores = inv.validar_pedido_proveedor(productos, {
        "pedido_proveedor[a]": "2", "precio_proveedor[a]": "1.5",
        "pedido_proveedor[b]": "1", "precio_proveedor[b]": "3"})
    assert not errores and [p["codigo"] for p in pedido] == ["b", "a"]


def test_almacen_ids_invalidos_no_tocan_el_disco(tmp_path):
    almacen = AlmacenInventario(tmp_path)
    for malo in ("../../etc/passwd", "abc", None, "", "G" * 32):
        assert almacen.cargar(malo) is None and not almacen.existe(malo)
        with pytest.raises(ValueError):
            almacen.guardar(malo, [])


def test_limpieza_solo_borra_archivos_propios_y_antiguos(tmp_path):
    import os, time
    almacen = AlmacenInventario(tmp_path)
    viejo, nuevo = almacen.nuevo_id(), almacen.nuevo_id()
    productos = inv.validar_filas([fila()])
    almacen.guardar(viejo, productos); almacen.guardar(nuevo, productos)
    ajeno = tmp_path / "notas.txt"; ajeno.write_text("no tocar")
    hace_2_dias = time.time() - 2 * 24 * 3600
    os.utime(tmp_path / f"{viejo}.csv", (hace_2_dias, hace_2_dias))
    os.utime(ajeno, (hace_2_dias, hace_2_dias))
    assert almacen.limpiar_antiguos(1) == 1
    assert almacen.existe(nuevo) and not almacen.existe(viejo) and ajeno.exists()
