"""
Sistema de Gestión de Inventario para Restaurantes (v1.0 - Múltiples Tablas).

Demuestra cuatro algoritmos de ordenamiento (Insertion, Bubble, Quick, Selection)
aplicados a diferentes criterios de gestión de inventario. Por cada criterio,
genera una visualización tabular con Matplotlib y un archivo de registro CSV.
"""

# Standard library
import csv
import datetime

# Third-party libraries
import matplotlib.pyplot as plt
# pandas no es usado en este script, se elimina para evitar W0611 y E0401.

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
    """
    Implementa el algoritmo Insertion Sort (orden ascendente).
    # ... (Docstring omitido por brevedad)
    """
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and key(lista[j]) > key(actual):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    return lista


def bubble_sort(lista: list, key: callable, descending: bool = False) -> list:
    """
    Implementa el algoritmo Bubble Sort.
    # ... (Docstring omitido por brevedad)
    """
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
    """
    Implementa el algoritmo Quick Sort recursivo (orden ascendente).
    # ... (Docstring omitido por brevedad)
    """
    if len(lista) <= 1:
        return lista

    pivot = lista[0]
    menos = [x for x in lista[1:] if key(x) < key(pivot)]
    iguales = [x for x in lista if key(x) == key(pivot)]
    mayor = [x for x in lista[1:] if key(x) >= key(pivot)]

    return quick_sort(menos, key) + iguales + quick_sort(mayor, key)


def selection_sort(lista: list, key: callable, reverse: bool = False) -> list:
    """
    Implementa el algoritmo Selection Sort.
    # ... (Docstring omitido por brevedad)
    """
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
# Función para generar tabla y CSV
# =======================================

def generate_table_and_csv(
    sorted_data: list, title: str, table_headers: list, query_date: str, algorithm_key: str
):
    """
    Genera una tabla visual de los datos ordenados usando Matplotlib, guarda
    una imagen PNG y un archivo CSV de registro.
    
    # ... (Docstring omitido por brevedad)
    """
    # Crear una matriz con los datos ordenados
    data_rows = [] # Cambiado data_matrix a data_rows para reducir variables locales
    for item in sorted_data:
        data_rows.append([
            item["codigo"],
            item["nombre"],
            item["demanda"],
            item["tiempo_entrega"],
            item["fecha_limite"],
            item["cantidad"],
        ])

    # Crear figura y ejes para la tabla
    fig, ax = plt.subplots(figsize=(10, len(sorted_data) * 0.6 + 2))
    ax.axis("off")

    # Crear la tabla en el gráfico
    table_obj = ax.table(
        cellText=data_rows, colLabels=table_headers, loc="center", cellLoc="center"
    )
    table_obj.auto_set_font_size(False)
    table_obj.set_fontsize(10)
    table_obj.scale(1.2, 1.2)

    plt.title(title, fontsize=14)
    plt.figtext(0.5, 0.01, f"Consulta generada: {query_date}", ha="center", fontsize=8)

    # Guardar una imagen PNG de los datos
    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # C0103
    image_filename = f"inventario_{algorithm_key}_{time_stamp}.png" # C0103

    try:
        plt.savefig(image_filename, bbox_inches="tight")
        plt.show()  # Se mostrará la tabla
    except IOError as e:
        print(f"Error al guardar la imagen {image_filename}: {e}")

    plt.close(fig)

    # Generar archivo CSV con un registro de la consulta
    csv_filename = f"registro_{algorithm_key}_{time_stamp}.csv" # C0103
    try:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Fecha Consulta"] + table_headers)
            for row in data_rows:
                writer.writerow([query_date] + row)
    except IOError as e:
        print(f"Error al escribir el archivo CSV {csv_filename}: {e}")

    print(f"{title} - Archivos generados:")
    print(" Imagen:", image_filename)
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
        table_headers=HEADERS, # Usamos HEADERS global
        query_date=FECHA_CONSULTA,
        algorithm_key=orden["algorithm_key"],
    )