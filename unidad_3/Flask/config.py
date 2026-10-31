"""Configuración central de la aplicación."""

import datetime
import os
import secrets
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def _obtener_secret_key() -> str:
    """
    Devuelve la clave secreta de Flask.

    Orden de prioridad:
      1. Variable de entorno FLASK_SECRET_KEY.
      2. Archivo local `.secret_key` (se genera aleatoriamente la primera vez,
         así las sesiones sobreviven a los reinicios en desarrollo).
      3. Clave aleatoria solo para este proceso, si no se puede escribir el archivo.
    """
    clave = os.environ.get("FLASK_SECRET_KEY")
    if clave:
        return clave

    archivo = BASE_DIR / ".secret_key"
    try:
        if archivo.exists():
            clave = archivo.read_text(encoding="utf-8").strip()
            if clave:
                return clave
        clave = secrets.token_hex(32)
        archivo.write_text(clave, encoding="utf-8")
        try:
            archivo.chmod(0o600)
        except OSError:
            pass
        return clave
    except OSError:
        return secrets.token_hex(32)


class Config:
    """Valores por defecto; se pueden sobrescribir con create_app(config={...})."""

    SECRET_KEY = _obtener_secret_key()

    # Ruta absoluta: no depende del directorio desde el que se ejecute la app.
    DATA_DIR = Path(os.environ.get("TOUKEN_DATA_DIR", BASE_DIR / "uploads")).resolve()
    # El inventario y su historial son datos del negocio: se conservan mientras
    # se usen. Cada uso renueva el plazo; pasado este tiempo sin tocarlos se borran.
    DIAS_RETENCION = 365
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=365)  # la cookie dura lo mismo

    DIAS_AVISO_VENCIMIENTO = 7  # días de antelación para avisar "por vencer"

    # Un lote cuya fecha límite ya pasó se descarta solo: sale del stock y queda en el
    # historial como una merma por vencimiento. Ponlo en False para descartar a mano.
    DESCARTE_AUTOMATICO_VENCIDOS = True

    # Demanda (ver services/demanda.py y services/alertas.py)
    VENTANA_DEMANDA_DIAS = 14  # días que se promedian para el consumo diario
    MIN_DIAS_HISTORIAL = 7  # sin al menos estos días de historial no se calcula consumo
    DIAS_SEGURIDAD = 1  # colchón sobre el tiempo de entrega al decidir reponer
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB por petición

    DIR_FUENTES = BASE_DIR / "fonts"

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
