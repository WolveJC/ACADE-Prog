"""
Registro de movimientos de stock: cada retirada o entrada con su fecha.

Es la base de datos que permite medir la demanda real (unidades por día),
detectar tendencias y separar los eventos puntuales del consumo habitual.
Lógica pura, sin Flask.

Un movimiento es un diccionario:
    {"fecha": date, "codigo": str, "cantidad": int > 0,
     "tipo": "salida" | "entrada" | "merma", "motivo": str, "evento": bool}

* salida: mercancía que sale del stock (pedido de stock). Son las que miden la demanda.
* entrada: mercancía que llega (recepción). Queda en el historial pero no
  cuenta como demanda.
* merma: mercancía que se descarta (vencida, dañada...). Baja el stock pero NO es
  demanda: nadie la quiso comprar. Lleva un `motivo` (vencido, danado, otro).
* evento=True (solo salidas) marca una retirada excepcional (una fiesta, un
  pedido temático) que se guarda pero NO cuenta para el consumo habitual.
"""

import csv
import datetime
import io
from typing import Any, Dict, Iterable, List, Mapping, Optional

from .inventario import MOTIVOS_MERMA, InventarioError, a_entero, leer_tabla_csv

SALIDA = "salida"
ENTRADA = "entrada"
MERMA = "merma"
TIPOS = (SALIDA, ENTRADA, MERMA)

COLUMNAS_MOV: List[str] = ["fecha", "codigo", "cantidad", "tipo", "evento", "motivo"]
COLUMNAS_MOV_OBLIGATORIAS = ["fecha", "codigo", "cantidad"]

Movimiento = Dict[str, Any]

_VERDADERO = {"1", "on", "true", "verdadero", "si", "sí", "s", "x", "yes", "y", "evento"}
_FALSO = {"", "0", "false", "falso", "no", "n"}


def a_booleano(valor: Any) -> bool:
    """Interpreta 1/0, true/false, sí/no, x (o vacío = False). Lanza ValueError."""
    if isinstance(valor, bool):
        return valor
    texto = str(valor if valor is not None else "").strip().lower()
    if texto in _VERDADERO:
        return True
    if texto in _FALSO:
        return False
    raise ValueError("valor booleano no reconocido")


def parsear_tipo(valor: Any) -> str:
    """"salida", "entrada" o "merma" (vacío = salida). Lanza ValueError si no se reconoce."""
    texto = str(valor if valor is not None else "").strip().lower()
    if texto == "":
        return SALIDA
    if texto in TIPOS:
        return texto
    raise ValueError("tipo desconocido")


def parsear_motivo(valor: Any, tipo: str) -> str:
    """
    Motivo de una merma: vencido, danado u otro (vacío = otro). Para los demás
    tipos no aplica y se devuelve "". Lanza ValueError si no se reconoce.
    """
    if tipo != MERMA:
        return ""
    texto = str(valor if valor is not None else "").strip().lower()
    if texto == "":
        return "otro"
    if texto in MOTIVOS_MERMA:
        return texto
    raise ValueError("motivo desconocido")


def parsear_fecha(texto: Any, hoy: datetime.date) -> datetime.date:
    """
    Fecha YYYY-MM-DD no futura. Un valor vacío significa "hoy".
    Lanza ValueError con un mensaje apto para mostrar al usuario.
    """
    texto = str(texto if texto is not None else "").strip()
    if not texto:
        return hoy
    try:
        fecha = datetime.datetime.strptime(texto, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("la fecha debe tener formato YYYY-MM-DD válido") from None
    if len(texto) != 10:
        raise ValueError("la fecha debe tener formato YYYY-MM-DD válido")
    if fecha > hoy:
        raise ValueError("la fecha no puede ser futura")
    return fecha


def validar_movimientos(
    filas: List[Mapping[str, Any]],
    codigos_validos: Optional[Iterable[str]],
    hoy: datetime.date,
    etiqueta: str = "Fila",
    primera: int = 2,
) -> List[Movimiento]:
    """
    Valida y normaliza filas con las claves de `COLUMNAS_MOV`
    (`tipo`, `evento` y `motivo` son opcionales). Si `codigos_validos` se indica, rechaza los
    códigos que no estén en el inventario (evita errores de tipeo).
    """
    if not filas:
        raise InventarioError(["El historial no contiene ningún movimiento."])

    validos = {str(c) for c in codigos_validos} if codigos_validos is not None else None
    errores: List[str] = []
    resultado: List[Movimiento] = []

    for numero, fila in enumerate(filas, start=primera):
        problemas: List[str] = []

        try:
            fecha = parsear_fecha(fila.get("fecha", ""), hoy)
            if not str(fila.get("fecha", "")).strip():
                raise ValueError("la fecha es obligatoria")
        except ValueError as exc:
            fecha = None
            problemas.append(str(exc))

        codigo = str(fila.get("codigo", "")).strip()
        if not codigo:
            problemas.append("el código es obligatorio")
        elif validos is not None and codigo not in validos:
            problemas.append(f"el código '{codigo}' no existe en el inventario")

        try:
            cantidad = a_entero(fila.get("cantidad", ""))
            if cantidad <= 0:
                raise ValueError("no positiva")
        except ValueError:
            cantidad = 0
            problemas.append("la cantidad debe ser un entero mayor que 0")

        try:
            tipo = parsear_tipo(fila.get("tipo", ""))
        except ValueError:
            tipo = SALIDA
            problemas.append("tipo debe ser salida, entrada o merma")

        try:
            evento = a_booleano(fila.get("evento", ""))
        except ValueError:
            evento = False
            problemas.append("evento debe ser 1/0, sí/no o vacío")
        if evento and tipo != SALIDA:
            problemas.append(f"una {tipo} no puede ser un evento")

        try:
            motivo = parsear_motivo(fila.get("motivo", ""), tipo)
        except ValueError:
            motivo = ""
            problemas.append("motivo debe ser vencido, danado u otro")

        if problemas:
            errores.append(f"{etiqueta} {numero}: {'; '.join(problemas)}.")
        else:
            resultado.append(
                {"fecha": fecha, "codigo": codigo, "cantidad": cantidad, "tipo": tipo,
                 "evento": evento, "motivo": motivo}
            )

    if errores:
        raise InventarioError(errores)
    return resultado


def desde_csv_bytes(
    contenido: bytes, codigos_validos: Iterable[str], hoy: datetime.date
) -> List[Movimiento]:
    """Lee un CSV de historial (columnas fecha, codigo, cantidad y opcionales tipo, evento y motivo)."""
    df = leer_tabla_csv(contenido)
    faltantes = [c for c in COLUMNAS_MOV_OBLIGATORIAS if c not in df.columns]
    if faltantes:
        raise InventarioError(
            [
                "El CSV de historial debe contener las columnas: fecha, codigo, cantidad "
                f"(y opcionalmente tipo, evento y motivo). Faltan: {', '.join(faltantes)}."
            ]
        )
    for opcional in ("tipo", "evento", "motivo"):
        if opcional not in df.columns:
            df[opcional] = ""
    return validar_movimientos(df[COLUMNAS_MOV].to_dict(orient="records"), codigos_validos, hoy)


def a_csv_texto(movimientos: Iterable[Movimiento]) -> str:
    """Serializa movimientos al formato CSV del historial (el mismo que se importa)."""
    salida = io.StringIO()
    escritor = csv.writer(salida, lineterminator="\n")
    escritor.writerow(COLUMNAS_MOV)
    for m in movimientos:
        escritor.writerow(
            [m["fecha"].isoformat(), m["codigo"], m["cantidad"], m["tipo"],
             1 if m["evento"] else 0, m.get("motivo", "")]
        )
    return salida.getvalue()
