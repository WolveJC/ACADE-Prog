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
from matplotlib import table
import pandas as pd # Añadido para manejo estructurado de datos en CSV (opcional, pero buena práctica)


# ---------------------------------------
# Ejemplo del inventario
inventario = [
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

# ---------------------------------------
# Funciones de ordenamiento


def insertion_sort(lista: list, key: callable) -> list:
    """
    Implementa el algoritmo Insertion Sort (orden ascendente).

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Una función para especificar la clave de ordenamiento.

    Returns:
        La lista ordenada.
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

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Una función para especificar la clave de ordenamiento.
        descending: Si es True, ordena de mayor a menor.

    Returns:
        La lista ordenada.
    """
    n = len(lista)
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, n):
            comparacion = (key(lista[i - 1]) < key(lista[i])) if descending else \
                          (key(lista[i - 1]) > key(lista[i]))

            if comparacion:
                lista[i - 1], lista[i] = lista[i], lista[i - 1]
                swapped = True
        n -= 1
    return lista


def quick_sort(lista: list, key: callable) -> list:
    """
    Implementa el algoritmo Quick Sort recursivo (orden ascendente).

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Una función para especificar la clave de ordenamiento.

    Returns:
        La lista ordenada.
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

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Una función para especificar la clave de ordenamiento.
        reverse: Si es True, ordena de mayor a menor.

    Returns:
        La lista ordenada.
    """
    n = len(lista)
    for i in range(n):
        index_extremo = i
        for j in range(i + 1, n):
            comparacion = (key(lista[j]) > key(lista[index_extremo])) if reverse else \
                          (key(lista[j]) < key(lista[index_extremo]))
            
            if comparacion:
                index_extremo = j
                
        lista[i], lista[index_extremo] = lista[index_extremo], lista[i]
    return lista


# ---------------------------------------
# Criterios de Ordenamiento

# Ordenar por Cantidad en inventario (usando Insertion Sort: de menor a mayor)
inventario_por_cantidad = insertion_sort(inventario.copy(), key=lambda x: x["cantidad"])

# Ordenar por Tiempo de entrega (usando Bubble Sort: de mayor a menor)
inventario_por_tiempo = bubble_sort(
    inventario.copy(), key=lambda x: x["tiempo_entrega"], descending=True
)

# Ordenar por Fecha límite (usando Quick Sort: las fechas más próximas primero)
inventario_por_fecha = quick_sort(
    inventario.copy(),
    key=lambda x: datetime.datetime.strptime(x["fecha_limite"], "%Y-%m-%d"),
)

# Ordenar por Demanda del cliente (usando Selection Sort: de mayor a menor)
inventario_por_demanda = selection_sort(inventario.copy(), key=lambda x: x["demanda"], reverse=True)


# ---------------------------------------
# Función para generar una tabla con Matplotlib y guardar un CSV de registro

def generate_table_and_csv(sorted_data: list, title: str, headers: list, query_date: str, algorithm_key: str):
    """
    Genera una tabla visual de los datos ordenados usando Matplotlib, guarda
    una imagen PNG y un archivo CSV de registro.

    Args:
        sorted_data: La lista de diccionarios de inventario ya ordenada.
        title: Título del gráfico.
        headers: Encabezados de la tabla.
        query_date: Fecha y hora de la consulta (timestamp).
        algorithm_key: Clave del algoritmo (usada para nombrar archivos).
    """
    # Crear una matriz con los datos ordenados
    data_matrix = []
    for item in sorted_data:
        row = [
            item["codigo"],
            item["nombre"],
            item["demanda"],
            item["tiempo_entrega"],
            item["fecha_limite"],
            item["cantidad"],
        ]
        data_matrix.append(row)

    # Crear figura y ejes para la tabla
    fig, ax = plt.subplots(figsize=(10, len(sorted_data) * 0.6 + 2))
    ax.axis("off")

    # Crear la tabla en el gráfico
    table_obj = ax.table(cellText=data_matrix, colLabels=headers, loc="center", cellLoc="center")
    table_obj.auto_set_font_size(False)
    table_obj.set_fontsize(10)
    table_obj.scale(1.2, 1.2)
    


    plt.title(title, fontsize=14)
    plt.figtext(0.5, 0.01, f"Consulta generada: {query_date}", ha="center", fontsize=8)

    # Guardar una imagen PNG de los datos
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"inventario_{algorithm_key}_{timestamp}.png"
    
    try:
        plt.savefig(image_filename, bbox_inches="tight")
        plt.show()  # Se mostrará la tabla
    except IOError as e:
        print(f"Error al guardar la imagen {image_filename}: {e}")
        
    plt.close(fig)

    # Generar archivo CSV con un registro de la consulta
    csv_filename = f"registro_{algorithm_key}_{timestamp}.csv"
    try:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Fecha Consulta"] + headers)
            for row in data_matrix:
                writer.writerow([query_date] + row)
    except IOError as e:
        print(f"Error al escribir el archivo CSV {csv_filename}: {e}")

    print(f"{title} - Archivos generados:")
    print(" Imagen:", image_filename)
    print(" Registro CSV:", csv_filename)
    print("-----------------------------------------")


# ---------------------------------------
# Ejecución principal
# ---------------------------------------

# Cabeceras para la tabla
headers = ["Código", "Nombre", "Demanda", "Tiempo entrega", "Fecha límite", "Cantidad"]

# Fecha y hora de la consulta
fecha_consulta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Diccionarios con cada ordenamiento
ordenamientos = [
    {
        "title": "Ordenamiento por Cantidad (Insertion Sort)",
        "data": inventario_por_cantidad,
        "algorithm_key": "insertion",
    },
    {
        "title": "Ordenamiento por Tiempo de entrega (Bubble Sort)",
        "data": inventario_por_tiempo,
        "algorithm_key": "bubble",
    },
    {
        "title": "Ordenamiento por Fecha límite (Quick Sort)",
        "data": inventario_por_fecha,
        "algorithm_key": "quick",
    },
    {
        "title": "Ordenamiento por Demanda (Selection Sort)",
        "data": inventario_por_demanda,
        "algorithm_key": "selection",
    },
]

# Iterar sobre cada criterio de ordenamiento, generar y mostrar la tabla, y guardar el CSV correspondiente.
for orden in ordenamientos:
    generate_table_and_csv(
        sorted_data=orden["data"],
        title=orden["title"],
        headers=headers,
        query_date=fecha_consulta,
        algorithm_key=orden["algorithm_key"],
)
