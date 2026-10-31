"""
Genera un historial de movimientos de ejemplo para probar la pantalla «Demanda».

Uso (desde la carpeta Flask):
    python ejemplos/generar_movimientos.py            # escribe ejemplos/movimientos_demo.csv
    python ejemplos/generar_movimientos.py -d 45      # 45 días de historial

Las fechas se calculan hacia atrás desde HOY, así que el archivo siempre es
reciente. Está pensado para los códigos 1-4 de inventario_ejemplo.csv:

    1 Manzana  consumo estable
    2 Banana   en alza (la última semana se retira más del doble)
    3 Lechuga  en baja
    4 Tomate   consumo bajo + una retirada enorme marcada como evento
    (tras importar, el consumo de Tomate sigue siendo bajo: el evento no cuenta)
    También incluye algunas entradas de mercancía (tipo "entrada") y una merma de
    Lechuga vencida (tipo "merma", motivo "vencido"): quedan en el historial pero
    no cuentan como demanda.

Después impórtalo en la página «Demanda» de la aplicación.
"""

import argparse
import csv
import datetime
import random
from pathlib import Path


def generar(dias: int, semilla: int = 7):
    azar = random.Random(semilla)
    hoy = datetime.date.today()
    filas = []
    for atras in range(dias - 1, -1, -1):
        fecha = hoy - datetime.timedelta(days=atras)
        ultima_semana = atras < 7
        filas.append((fecha, "1", azar.randint(2, 4), "salida", 0, ""))                       # estable
        filas.append((fecha, "2", azar.randint(6, 8) if ultima_semana else azar.randint(2, 3), "salida", 0, ""))  # en alza
        filas.append((fecha, "3", azar.randint(1, 2) if ultima_semana else azar.randint(3, 5), "salida", 0, ""))  # en baja
        if azar.random() < 0.5:
            filas.append((fecha, "4", azar.randint(1, 2), "salida", 0, ""))                    # consumo bajo
        if atras % 7 == 3:                                                                     # llega mercancía cada semana
            filas.append((fecha, "1", 30, "entrada", 0, ""))
            filas.append((fecha, "2", 40, "entrada", 0, ""))
    filas.append((hoy - datetime.timedelta(days=min(12, dias - 1)), "4", 60, "salida", 1, ""))  # evento especial
    filas.append((hoy - datetime.timedelta(days=min(4, dias - 1)), "3", 5, "merma", 0, "vencido"))  # descarte
    return filas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-d", "--dias", type=int, default=28, help="días de historial (por defecto 28)")
    ap.add_argument("-o", "--salida", default=Path(__file__).with_name("movimientos_demo.csv"))
    args = ap.parse_args()

    with open(args.salida, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["fecha", "codigo", "cantidad", "tipo", "evento", "motivo"])
        for fecha, codigo, cantidad, tipo, evento, motivo in generar(args.dias):
            w.writerow([fecha.isoformat(), codigo, cantidad, tipo, evento, motivo])
    print(f"Escrito {args.salida}")


if __name__ == "__main__":
    main()
