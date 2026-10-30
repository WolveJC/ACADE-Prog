import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import create_app  # noqa: E402


@pytest.fixture
def app(tmp_path):
    # Descarte automático APAGADO por defecto: muchas pruebas usan fechas pasadas a propósito para
    # comprobar las alertas de "vencido". El descarte automático tiene sus propias pruebas
    # (fixture `app_con_descarte`) y se verifica además con el navegador, que usa la configuración real.
    return create_app({"TESTING": True, "DATA_DIR": tmp_path / "datos", "SECRET_KEY": "test",
                       "DESCARTE_AUTOMATICO_VENCIDOS": False})


@pytest.fixture
def app_con_descarte(tmp_path):
    """La aplicación con la configuración de producción: los lotes vencidos se descartan solos."""
    return create_app({"TESTING": True, "DATA_DIR": tmp_path / "datos_descarte", "SECRET_KEY": "test"})


@pytest.fixture
def client_con_descarte(app_con_descarte):
    return app_con_descarte.test_client()


@pytest.fixture
def client(app):
    return app.test_client()


CSV_OK = (
    "Código,Nombre,Cantidad,Tiempo entrega(Días),Fecha límite\n"
    "1,Manzana,15,3,2025-04-28\n"
    "2,Banana,2,5,2025-04-25\n"
)

JSON_HEADERS = {"Accept": "application/json", "X-Requested-With": "XMLHttpRequest"}


def subir(client, contenido, nombre="inv.csv", tipo="text/csv", headers=None):
    import io

    if isinstance(contenido, str):
        contenido = contenido.encode("utf-8")
    return client.post(
        "/",
        data={"file": (io.BytesIO(contenido), nombre, tipo)},
        content_type="multipart/form-data",
        headers=JSON_HEADERS if headers is None else headers,
    )


def historial_csv(filas, hoy=None):
    """CSV de historial a partir de (días_atrás, código, cantidad[, evento[, tipo[, motivo]]]) relativos a hoy."""
    import datetime

    hoy = hoy or datetime.date.today()
    lineas = ["fecha,codigo,cantidad,tipo,evento,motivo"]
    for fila in filas:
        atras, codigo, cantidad = fila[:3]
        evento = fila[3] if len(fila) > 3 else 0
        tipo = fila[4] if len(fila) > 4 else "salida"
        motivo = fila[5] if len(fila) > 5 else ""
        fecha = (hoy - datetime.timedelta(days=atras)).isoformat()
        lineas.append(f"{fecha},{codigo},{cantidad},{tipo},{evento},{motivo}")
    return "\n".join(lineas) + "\n"


def importar_historial(client, contenido, nombre="historial.csv", headers=None):
    """Sube un historial a /demanda/importar (sin cabeceras JSON = como un navegador sin JS)."""
    import io

    if isinstance(contenido, str):
        contenido = contenido.encode("utf-8")
    return client.post(
        "/demanda/importar",
        data={"file": (io.BytesIO(contenido), nombre, "text/csv")},
        content_type="multipart/form-data",
        headers=headers or {},
    )
