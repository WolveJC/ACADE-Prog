"""
Sistema de Gestión de Inventario para Restaurantes (v1.0).

Implementa la clasificación de inventario utilizando una jerarquía de ordenamiento
estable, combinando Insertion Sort (modificado) y Quick Sort, para priorizar
los artículos que requieren atención inmediata. Finalmente, genera una visualización
tabular con Matplotlib y un registro en CSV.
"""

# Standard library
import csv
import datetime

# Third-party libraries
import matplotlib.pyplot as plt

# ==========================================================================
# Inventario de Ejemplo
# ==========================================================================
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


# ==========================================================================
# Algoritmos de ordenamiento
# ==========================================================================


def insertion_sort(lista: list, key: callable, descending: bool = False) -> list:
    """
    Implementa el Insertion Sort, adaptable para orden ascendente o descendente.

    Este es un algoritmo de ordenamiento **estable** y es ideal para su uso
    en un sort múltiple.

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Función para obtener el valor de ordenamiento.
        descending: True para ordenar de mayor a menor.

    Returns:
        La lista ordenada.
    """
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1

        # Determina la condición de comparación según el orden
        while j >= 0:
            if descending:
                if key(lista[j]) < key(actual):
                    lista[j + 1] = lista[j]
                    j -= 1
                else:
                    break
            else:  # Ascendente
                if key(lista[j]) > key(actual):
                    lista[j + 1] = lista[j]
                    j -= 1
                else:
                    break
        lista[j + 1] = actual
    return lista


def quick_sort(lista: list, key: callable) -> list:
    """
    Implementa el Quick Sort recursivo.

    Se utiliza aquí como el paso final (el criterio más importante) para
    ordenar por fecha límite (ascendente). Nota: La implementación con
    list comprehensions no es estrictamente estable.

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Función para obtener el valor de ordenamiento.

    Returns:
        La lista ordenada.
    """
    if len(lista) <= 1:
        return lista

    pivot = lista[0]
    # Particiones
    menos = [x for x in lista[1:] if key(x) < key(pivot)]
    iguales = [x for x in lista if key(x) == key(pivot)]
    mayor = [x for x in lista[1:] if key(x) >= key(pivot)]

    return quick_sort(menos, key) + iguales + quick_sort(mayor, key)


def selection_sort_stable(lista: list, key: callable, reverse: bool = False) -> list:
    """
    Implementación **estable** del Selection Sort para listas pequeñas.

    Busca y remueve repetidamente el elemento más extremo de una lista temporal
    y lo añade a una nueva lista.

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Función para obtener el valor de ordenamiento.
        reverse: Si es True, ordena de mayor a menor.

    Returns:
        La nueva lista ordenada.
    """
    nueva_lista = []
    temp = lista.copy()
    while temp:
        candidato = temp[0]
        indice_candidato = 0

        # Buscar el elemento más extremo
        for i, inventario_item in enumerate(temp):
            comparacion = (
                key(inventario_item) > key(candidato)
            ) if reverse else (key(inventario_item) < key(candidato))

            if comparacion:
                candidato = inventario_item
                indice_candidato = i

        # Asegurar la estabilidad: usar el índice para eliminar el primer
        # ejemplar encontrado con ese valor extremo
        nueva_lista.append(candidato)
        temp.pop(indice_candidato)
    return nueva_lista


# ==========================================================================
# Ordenamiento jerárquico (Multiple Stable Sort)
# ==========================================================================

# 4º (menos importante): Demanda (Selection Sort, orden descendente)
ordenados = selection_sort_stable(
    INVENTARIO.copy(), key=lambda x: x["demanda"], reverse=True
)

# 3º: Tiempo de entrega (Insertion Sort es estable, orden descendente)
ordenados = insertion_sort(
    ordenados, key=lambda x: x["tiempo_entrega"], descending=True
)

# 2º: Cantidad en inventario (Insertion Sort es estable, orden ascendente)
ordenados = insertion_sort(ordenados, key=lambda x: x["cantidad"], descending=False)

# 1º (más importante): Fecha límite (Quick Sort, orden ascendente)
ordenados = quick_sort(
    ordenados, key=lambda x: datetime.datetime.strptime(x["fecha_limite"], "%Y-%m-%d")
)

# ==========================================================================
# Preparar datos y Visualización
# ==========================================================================
HEADERS = [
    "Código",
    "Nombre",
    "Demanda",
    "Tiempo entrega(Días)",
    "Fecha límite",
    "Cantidad",
]

data_matrix = []
# W0621: Cambiado 'item' por 'inventario_item' para evitar la advertencia
for inventario_item in ordenados:
    row = [
        inventario_item["codigo"],
        inventario_item["nombre"],
        inventario_item["demanda"],
        inventario_item["tiempo_entrega"],
        inventario_item["fecha_limite"],
        inventario_item["cantidad"],
    ]
    data_matrix.append(row)

# Fecha y hora de la consulta
FECHA_CONSULTA = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Visualización con Matplotlib
fig, ax = plt.subplots(figsize=(10, len(ordenados) * 0.6 + 2))
ax.axis("off")

tabla = ax.table(cellText=data_matrix, colLabels=HEADERS, loc="center", cellLoc="center")
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1.2, 1.2)


plt.title("Inventario Ordenado Jerárquicamente", fontsize=16)
plt.figtext(0.5, 0.01, f"Consulta generada: {FECHA_CONSULTA}", ha="center", fontsize=8)

# Guardar una imagen con un timestamp (PNG)
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
IMAGEN_FILENAME = f"inventario_jerarquico_{TIMESTAMP}.png"
plt.savefig(IMAGEN_FILENAME, bbox_inches="tight")
plt.show()

# ==========================================================================
# Generar un archivo CSV con el registro de la consulta
# ==========================================================================
CSV_FILENAME = f"registro_inventario_jerarquico_{TIMESTAMP}.csv"
try:
    with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Escribir encabezado con la fecha de consulta
        writer.writerow(["Fecha Consulta"] + HEADERS)
        for row in data_matrix:
            writer.writerow([FECHA_CONSULTA] + row)
except IOError as e:
    print(f"Error al escribir el archivo CSV: {e}")

print("Archivos generados:")
print(" Imagen:", IMAGEN_FILENAME)
print(" Registro CSV:", CSV_FILENAME)