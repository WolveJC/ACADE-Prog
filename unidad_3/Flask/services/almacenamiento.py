"""
Almacenamiento del inventario en disco.

Cada sesión de usuario tiene un identificador aleatorio (uuid4 hex). Su
inventario vive en `<DATA_DIR>/<id>.csv`, su historial de movimientos
(retiradas con fecha) en `<DATA_DIR>/<id>.movimientos.csv` y el pedido a
proveedor pendiente en `<DATA_DIR>/<id>.pedido.json`. La cookie de sesión solo
guarda el id, así el tamaño de los datos no depende del límite de ~4 KB.

Los nombres de archivo nunca provienen del usuario, lo que evita colisiones y
ataques de path traversal.
"""

import csv
import datetime
import json
import os
import re
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from .inventario import COLUMNAS, Producto, validar_filas
from .lotes import a_filas
from .movimientos import COLUMNAS_MOV, Movimiento, a_csv_texto, parsear_motivo, parsear_tipo

_ID_RE = re.compile(r"^[0-9a-f]{32}$")
_ARCHIVO_PROPIO_RE = re.compile(r"^[0-9a-f]{32}\.(csv|movimientos\.csv|pedido\.json)(\.tmp)?$")


class AlmacenInventario:
    """Lee y escribe inventarios y pedidos pendientes en un directorio."""

    def __init__(self, directorio: Any):
        self.directorio = Path(directorio)
        self.directorio.mkdir(parents=True, exist_ok=True)

    # -- utilidades internas ------------------------------------------------
    @staticmethod
    def nuevo_id() -> str:
        """Genera un identificador de inventario nuevo e impredecible."""
        return uuid.uuid4().hex

    def _ruta(self, inv_id: Any, sufijo: str) -> Path:
        if not isinstance(inv_id, str) or not _ID_RE.match(inv_id):
            raise ValueError("Identificador de inventario inválido.")
        return self.directorio / f"{inv_id}{sufijo}"

    @staticmethod
    def _escribir_atomico(destino: Path, escribir) -> None:
        """Escribe en un temporal y lo renombra, para no dejar archivos a medias."""
        temporal = destino.with_name(destino.name + ".tmp")
        try:
            escribir(temporal)
            os.replace(temporal, destino)
        finally:
            if temporal.exists():
                temporal.unlink()

    # -- inventario ---------------------------------------------------------
    def guardar(self, inv_id: str, productos: List[Producto]) -> Path:
        """Guarda el inventario completo (reemplaza el contenido anterior)."""
        destino = self._ruta(inv_id, ".csv")
        df = pd.DataFrame(a_filas(productos), columns=COLUMNAS)  # una fila por lote
        self._escribir_atomico(
            destino, lambda tmp: df.to_csv(tmp, index=False, encoding="utf-8")
        )
        return destino

    def existe(self, inv_id: Any) -> bool:
        try:
            return self._ruta(inv_id, ".csv").exists()
        except ValueError:
            return False

    def cargar(self, inv_id: Any) -> Optional[List[Producto]]:
        """Devuelve los productos, o None si no existe o el archivo no es válido."""
        try:
            ruta = self._ruta(inv_id, ".csv")
            if not ruta.exists():
                return None
            df = pd.read_csv(ruta, dtype=str, keep_default_na=False, encoding="utf-8")
            if df.empty:
                # Inventario sin productos (se quitó el último desde la página): es válido.
                productos = []
            else:
                productos = validar_filas(df.to_dict(orient="records"))
        except (OSError, ValueError):
            return None
        try:
            os.utime(ruta, None)  # uso reciente: evita que la limpieza lo borre
        except OSError:
            pass
        return productos

    def eliminar(self, inv_id: Any) -> None:
        """Borra el inventario y su pedido pendiente (si existen)."""
        for sufijo in (".csv", ".movimientos.csv", ".pedido.json"):
            try:
                self._ruta(inv_id, sufijo).unlink(missing_ok=True)
            except (ValueError, OSError):
                pass

    # -- historial de movimientos --------------------------------------------
    def agregar_movimientos(self, inv_id: str, movimientos: List[Movimiento]) -> None:
        """Añade movimientos al final del historial (crea el archivo si no existe)."""
        if not movimientos:
            return
        ruta = self._ruta(inv_id, ".movimientos.csv")
        self._migrar_formato_antiguo(inv_id, ruta)
        nuevo = not ruta.exists() or ruta.stat().st_size == 0
        with open(ruta, "a", encoding="utf-8", newline="") as archivo:
            escritor = csv.writer(archivo, lineterminator="\n")
            if nuevo:
                escritor.writerow(COLUMNAS_MOV)
            for m in movimientos:
                escritor.writerow(
                    [m["fecha"].isoformat(), m["codigo"], m["cantidad"], m["tipo"],
                     1 if m["evento"] else 0, m.get("motivo", "")]
                )

    def _migrar_formato_antiguo(self, inv_id: str, ruta: Path) -> None:
        """Reescribe con la cabecera actual un historial guardado antes de existir `tipo`."""
        if not ruta.exists() or ruta.stat().st_size == 0:
            return
        with open(ruta, encoding="utf-8", newline="") as archivo:
            cabecera = archivo.readline().strip()
        if cabecera != ",".join(COLUMNAS_MOV):
            self.reemplazar_movimientos(inv_id, self.leer_movimientos(inv_id))

    def reemplazar_movimientos(self, inv_id: str, movimientos: List[Movimiento]) -> None:
        """Sustituye todo el historial (escritura atómica)."""
        destino = self._ruta(inv_id, ".movimientos.csv")
        texto = a_csv_texto(movimientos)
        self._escribir_atomico(destino, lambda tmp: tmp.write_text(texto, encoding="utf-8"))

    def leer_movimientos(self, inv_id: Any) -> List[Movimiento]:
        """Historial completo en orden de registro. Ignora filas dañadas."""
        try:
            ruta = self._ruta(inv_id, ".movimientos.csv")
            if not ruta.exists():
                return []
            with open(ruta, encoding="utf-8", newline="") as archivo:
                filas = list(csv.DictReader(archivo))
        except (OSError, ValueError, csv.Error):
            return []

        movimientos: List[Movimiento] = []
        for fila in filas:
            try:
                tipo = parsear_tipo(fila.get("tipo"))
                movimientos.append(
                    {
                        "fecha": datetime.date.fromisoformat(fila["fecha"]),
                        "codigo": str(fila["codigo"]),
                        "cantidad": int(fila["cantidad"]),
                        "tipo": tipo,
                        "evento": fila.get("evento") == "1",
                        "motivo": parsear_motivo(fila.get("motivo"), tipo),
                    }
                )
            except (KeyError, TypeError, ValueError):
                continue
        return movimientos

    def borrar_movimientos(self, inv_id: Any) -> None:
        try:
            self._ruta(inv_id, ".movimientos.csv").unlink(missing_ok=True)
        except (ValueError, OSError):
            pass

    # -- pedido a proveedor pendiente ----------------------------------------
    def guardar_pedido(self, inv_id: str, pedido: List[Dict[str, Any]]) -> None:
        destino = self._ruta(inv_id, ".pedido.json")
        self._escribir_atomico(
            destino,
            lambda tmp: tmp.write_text(
                json.dumps(pedido, ensure_ascii=False), encoding="utf-8"
            ),
        )

    def leer_pedido(self, inv_id: Any) -> Optional[List[Dict[str, Any]]]:
        try:
            ruta = self._ruta(inv_id, ".pedido.json")
            if not ruta.exists():
                return None
            pedido = json.loads(ruta.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        return pedido if isinstance(pedido, list) and pedido else None

    def descartar_pedido(self, inv_id: Any) -> None:
        try:
            self._ruta(inv_id, ".pedido.json").unlink(missing_ok=True)
        except (ValueError, OSError):
            pass

    # -- mantenimiento -------------------------------------------------------
    def limpiar_antiguos(self, dias: float = 1) -> int:
        """
        Elimina los archivos generados por la app sin modificar/usar desde hace
        más de `dias` días. No toca ningún otro archivo del directorio.
        Devuelve la cantidad de archivos eliminados.
        """
        limite = time.time() - dias * 24 * 3600
        eliminados = 0
        for ruta in self.directorio.iterdir():
            if not (ruta.is_file() and _ARCHIVO_PROPIO_RE.match(ruta.name)):
                continue
            try:
                if ruta.stat().st_mtime < limite:
                    ruta.unlink()
                    eliminados += 1
            except OSError:
                continue
        return eliminados
