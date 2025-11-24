"""
Sistema de Gestión de Inventario para Restaurantes (v1.0 - Múltiples Tablas).

Demuestra cuatro algoritmos de ordenamiento (Insertion, Bubble, Quick, Selection)
aplicados a diferentes criterios de gestión de inventario. Por cada criterio,
genera una visualización tabular con Matplotlib y un archivo de registro CSV.
"""

# Standard library
import csv
import datetime
from typing import List, Any # Añadida importación para anotación de tipo

# Third-party libraries
import matplotlib.pyplot as plt

# =======================================
# Inventario de Ejemplo
# =======================================
INVENTARIO = [
    {
        "codigo": 1,
        "nombre": "Manzana",
        "demanda": 8,
        "tiempo_entrega": 3,
        "fecha_limite": "2025-04-28",
        "cantidad": 15,
    },
    {
        "codigo": 2,
        "nombre": "Banana",
        "demanda": 7,
        "tiempo_entrega": 5,
        "fecha_limite": "2025-04-25",
        "cantidad": 2,
    },
    {
        "codigo": 3,
        "nombre": "Lechuga",
        "demanda": 6,
        "tiempo_entrega": 2,
        "fecha_limite": "2025-04-22",
        "cantidad": 7,
    },
    {
        "codigo": 4,
        "nombre": "Tomate",
        "demanda": 9,
        "tiempo_entrega": 4,
        "fecha_limite": "2025-05-01",
        "cantidad": 3,
    },
]

# =======================================
# Funciones de ordenamiento
# =======================================


def insertion_sort(lista: list, key: callable) -> list:
    """Implementa el algoritmo Insertion Sort (orden ascendente)."""
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and key(lista[j]) > key(actual):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    return lista


def bubble_sort(lista: list, key: callable, descending: bool = False) -> list:
    """Implementa el algoritmo Bubble Sort."""
    n = len(lista)
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, n):
            comparacion = (
                (key(lista[i - 1]) < key(lista[i]))
                if descending
                else (key(lista[i - 1]) > key(lista[i]))
            )

            if comparacion:
                lista[i - 1], lista[i] = lista[i], lista[i - 1]
                swapped = True
        n -= 1
    return lista


def quick_sort(lista: list, key: callable) -> list:
    """Implementa el algoritmo Quick Sort recursivo (orden ascendente)."""
    if len(lista) <= 1:
        return lista

    pivot = lista[0]
    menos = [x for x in lista[1:] if key(x) < key(pivot)]
    iguales = [x for x in lista if key(x) == key(pivot)]
    mayor = [x for x in lista[1:] if key(x) >= key(pivot)]

    return quick_sort(menos, key) + iguales + quick_sort(mayor, key)


def selection_sort(lista: list, key: callable, reverse: bool = False) -> list:
    """Implementa el algoritmo Selection Sort."""
    n = len(lista)
    for i in range(n):
        index_extremo = i
        for j in range(i + 1, n):
            comparacion = (
                (key(lista[j]) > key(lista[index_extremo]))
                if reverse
                else (key(lista[j]) < key(lista[index_extremo]))
            )

            if comparacion:
                index_extremo = j

        lista[i], lista[index_extremo] = lista[index_extremo], lista[i]
    return lista


# =======================================
# Criterios de Ordenamiento
# =======================================

# Ordenar por Cantidad en inventario (usando Insertion Sort: de menor a mayor)
INVENTARIO_POR_CANTIDAD = insertion_sort(
    INVENTARIO.copy(), key=lambda x: x["cantidad"]
)

# Ordenar por Tiempo de entrega (usando Bubble Sort: de mayor a menor)
INVENTARIO_POR_TIEMPO = bubble_sort(
    INVENTARIO.copy(), key=lambda x: x["tiempo_entrega"], descending=True
)

# Ordenar por Fecha límite (usando Quick Sort: las fechas más próximas primero)
INVENTARIO_POR_FECHA = quick_sort(
    INVENTARIO.copy(),
    key=lambda x: datetime.datetime.strptime(x["fecha_limite"], "%Y-%m-%d"),
)

# Ordenar por Demanda del cliente (usando Selection Sort: de mayor a menor)
INVENTARIO_POR_DEMANDA = selection_sort(
    INVENTARIO.copy(), key=lambda x: x["demanda"], reverse=True
)


# =======================================
# Funciones auxiliares (para eliminar R0914)
# =======================================

def _generate_visual_table(
    data_rows: List[List[Any]], title: str, headers: list, query_date: str, algorithm_key: str
) -> str:
    """Genera la tabla visual con Matplotlib y la guarda."""
    fig, ax = plt.subplots(figsize=(10, len(data_rows) * 0.6 + 2))
    ax.axis("off")

    table_obj = ax.table(
        cellText=data_rows, colLabels=headers, loc="center", cellLoc="center"
    )
    table_obj.auto_set_font_size(False)
    table_obj.set_fontsize(10)
    table_obj.scale(1.2, 1.2)

    plt.title(title, fontsize=14)
    plt.figtext(0.5, 0.01, f"Consulta generada: {query_date}", ha="center", fontsize=8)

    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"inventario_{algorithm_key}_{time_stamp}.png"

    try:
        plt.savefig(image_filename, bbox_inches="tight")
        plt.show()
    except IOError as e:
        print(f"Error al guardar la imagen {image_filename}: {e}")
        image_filename = None

    plt.close(fig)
    return image_filename


def _generate_csv_log(
    data_rows: List[List[Any]], headers: list, query_date: str, algorithm_key: str
) -> str:
    """Genera y guarda el registro de datos en un archivo CSV."""
    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"registro_{algorithm_key}_{time_stamp}.csv"
    try:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Fecha Consulta"] + headers)
            for row in data_rows:
                writer.writerow([query_date] + row)
    except IOError as e:
        print(f"Error al escribir el archivo CSV {csv_filename}: {e}")
        csv_filename = None

    return csv_filename


# =======================================
# Función para generar tabla y CSV (Refactorizada)
# =======================================

def generate_table_and_csv(
    sorted_data: list, title: str, table_headers: list, query_date: str, algorithm_key: str
):
    """
    Genera una tabla visual de los datos ordenados usando Matplotlib, guarda
    una imagen PNG y un archivo CSV de registro.
    
    R0914 Corregido: La complejidad de variables locales se ha movido 
    a las funciones auxiliares.
    """
    # 1. Crear una matriz con los datos ordenados (Variables: data_rows, item, row)
    data_rows = []
    for item in sorted_data:
        row = [
            item["codigo"],
            item["nombre"],
            item["demanda"],
            item["tiempo_entrega"],
            item["fecha_limite"],
            item["cantidad"],
        ]
        data_rows.append(row)

    # 2. Generar y guardar la tabla visual
    image_filename = _generate_visual_table(
        data_rows, title, table_headers, query_date, algorithm_key
    )

    # 3. Generar y guardar el registro CSV
    csv_filename = _generate_csv_log(
        data_rows, table_headers, query_date, algorithm_key
    )

    print(f"{title} - Archivos generados:")
    if image_filename:
        print(" Imagen:", image_filename)
    if csv_filename:
        print(" Registro CSV:", csv_filename)
    print("-----------------------------------------")


# =======================================
# Ejecución principal
# =======================================

# Cabeceras para la tabla
HEADERS = ["Código", "Nombre", "Demanda", "Tiempo entrega", "Fecha límite", "Cantidad"]

# Fecha y hora de la consulta
FECHA_CONSULTA = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Diccionarios con cada ordenamiento
ORDENAMIENTOS = [
    {
        "title": "Ordenamiento por Cantidad (Insertion Sort)",
        "data": INVENTARIO_POR_CANTIDAD,
        "algorithm_key": "insertion",
    },
    {
        "title": "Ordenamiento por Tiempo de entrega (Bubble Sort)",
        "data": INVENTARIO_POR_TIEMPO,
        "algorithm_key": "bubble",
    },
    {
        "title": "Ordenamiento por Fecha límite (Quick Sort)",
        "data": INVENTARIO_POR_FECHA,
        "algorithm_key": "quick",
    },
    {
        "title": "Ordenamiento por Demanda (Selection Sort)",
        "data": INVENTARIO_POR_DEMANDA,
        "algorithm_key": "selection",
    },
]

# Iterar sobre cada criterio de ordenamiento, generar y mostrar la tabla
# Finalmente, guardar el CSV correspondiente.
for orden in ORDENAMIENTOS:
    generate_table_and_csv(
        sorted_data=orden["data"],
        title=orden["title"],
        table_headers=HEADERS,
        query_date=FECHA_CONSULTA,
        algorithm_key=orden["algorithm_key"],
    )