"""Generación del PDF de pedido a proveedor con fpdf2."""

import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from fpdf import FPDF

_FUENTE = "DejaVu"


def _configurar_fuente(pdf: FPDF, dir_fuentes: Optional[Path]) -> bool:
    """
    Registra DejaVu Sans (Unicode) si está disponible.
    Devuelve True si se pudo; si no, se usa Helvetica (solo latin-1).
    """
    if not dir_fuentes:
        return False
    normal = Path(dir_fuentes) / "DejaVuSans.ttf"
    negrita = Path(dir_fuentes) / "DejaVuSans-Bold.ttf"
    if not (normal.is_file() and negrita.is_file()):
        return False
    pdf.add_font(_FUENTE, "", str(normal))
    pdf.add_font(_FUENTE, "B", str(negrita))
    return True


def generar_pdf_pedido(
    pedido: List[Dict[str, Any]],
    dir_fuentes: Optional[Path] = None,
    ahora: Optional[datetime.datetime] = None,
) -> Tuple[bytes, str]:
    """
    Construye el PDF del pedido.

    Args:
        pedido: líneas con codigo, nombre, cantidad y precio_unitario.
        dir_fuentes: carpeta con DejaVuSans.ttf y DejaVuSans-Bold.ttf.
        ahora: fecha/hora a mostrar (útil para pruebas).

    Returns:
        (contenido del PDF en bytes, nombre de archivo sugerido)
    """
    ahora = ahora or datetime.datetime.now()
    pdf = FPDF()
    pdf.add_page()

    unicode_ok = _configurar_fuente(pdf, dir_fuentes)
    familia = _FUENTE if unicode_ok else "Helvetica"

    def txt(valor: Any) -> str:
        """Sin fuente Unicode, sustituye lo que latin-1 no puede representar."""
        texto = str(valor)
        return texto if unicode_ok else texto.encode("latin-1", "replace").decode("latin-1")

    pdf.set_font(familia, "B", 14)
    pdf.cell(0, 10, txt("Pedido al Proveedor - Touken Café"), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font(familia, "", 9)
    pdf.cell(
        0, 6, txt(f"Fecha de generación: {ahora:%Y-%m-%d %H:%M:%S}"),
        align="C", new_x="LMARGIN", new_y="NEXT",
    )
    pdf.ln(8)

    pdf.set_font(familia, "", 9)
    total = 0.0
    with pdf.table(
        col_widths=(25, 75, 25, 30, 35),
        text_align=("CENTER", "LEFT", "CENTER", "RIGHT", "RIGHT"),
        line_height=7,
        padding=1,
    ) as tabla:
        encabezado = tabla.row()
        for titulo in ("Código", "Producto", "Cantidad", "Precio Unit.", "Precio Total"):
            encabezado.cell(txt(titulo))
        for item in pedido:
            subtotal = item["cantidad"] * item["precio_unitario"]
            total += subtotal
            fila = tabla.row()
            fila.cell(txt(item["codigo"]))
            fila.cell(txt(item["nombre"]))
            fila.cell(str(item["cantidad"]))
            fila.cell(f"${item['precio_unitario']:.2f}")
            fila.cell(f"${subtotal:.2f}")

    pdf.ln(4)
    pdf.set_font(familia, "B", 10)
    pdf.cell(155, 8, "Total del Pedido:", align="R")
    pdf.cell(35, 8, f"${total:.2f}", border=1, align="R", new_x="LMARGIN", new_y="NEXT")

    nombre = f"pedido_proveedor_{ahora:%Y%m%d_%H%M%S}.pdf"
    return bytes(pdf.output()), nombre
