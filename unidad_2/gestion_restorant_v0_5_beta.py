"""
Sistema de Gestión de Inventario para Restaurantes (v0.5 beta).

Combina el algoritmo Selection Sort para ordenar el inventario por demanda
y utiliza Matplotlib para generar una visualización tabular del inventario
ordenado, además de generar un registro en formato CSV.
"""

# Standard library
import csv
import datetime
import os  # Añadido para manejo de rutas de archivo si fuera necesario

# Third-party libraries
import matplotlib.pyplot as plt
from matplotlib import table

# Nota: La importación de 'table' dentro del módulo 'matplotlib' es correcta

# ==========================================================================
# Inventario de Ejemplo
# ==========================================================================
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


# ==========================================================================
# 1. Selection Sort para ordenar por demanda (de mayor a menor)
# ==========================================================================


def selection_sort(lista: list, key: callable, reverse: bool = False) -> list:
    """
    Implementa el algoritmo Selection Sort.

    Ordena la lista en orden ascendente (o descendente si `reverse=True`)
    basándose en la clave proporcionada.

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Una función lambda para especificar la clave de ordenamiento.
        reverse: Si es True, ordena de mayor a menor.

    Returns:
        La lista ordenada.
    """
    n = len(lista)
    for i in range(n):
        index_extremo = i
        # Buscar el elemento más extremo (máximo si reverse=True, mínimo si reverse=False)
        for j in range(i + 1, n):
            # Lógica de comparación
            comparacion = (
                (key(lista[j]) > key(lista[index_extremo]))
                if reverse
                else (key(lista[j]) < key(lista[index_extremo]))
            )

            if comparacion:
                index_extremo = j

        # Intercambio
        lista[i], lista[index_extremo] = lista[index_extremo], lista[i]

    return lista


# Ejecutar el ordenamiento
inventario_ordenado = selection_sort(inventario.copy(), key=lambda x: x["demanda"], reverse=True)


# ==========================================================================
# 2. Preparar la estructura de la tabla para visualizar
# ==========================================================================

HEADERS = ["Código", "Nombre", "Demanda", "Tiempo entrega", "Fecha límite", "Cantidad"]

# Crear la matriz de datos
data_matrix = []
for item in inventario_ordenado:
    row = [
        item["codigo"],
        item["nombre"],
        item["demanda"],
        item["tiempo_entrega"],
        item["fecha_limite"],
        item["cantidad"],
    ]
    data_matrix.append(row)

# Obtener la fecha y hora de la consulta
FECHA_CONSULTA = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ==========================================================================
# 3. Visualización con Matplotlib
# ==========================================================================

# Ajustar el tamaño para que la tabla quepa mejor
fig, ax = plt.subplots(figsize=(9, 2.5))
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)

# Crear la tabla en el eje (ax)
tabla = ax.table(cellText=data_matrix, collabels=HEADERS, loc="center", cellLoc="center")


tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1.0, 1.2)  # Ajuste la escala para un mejor aspecto

plt.title("Inventario Ordenado por Demanda", fontsize=14, pad=20)

# Agregar la fecha de la consulta en la parte inferior
plt.figtext(0.5, 0.05, f"Consulta generada: {FECHA_CONSULTA}", ha="center", fontsize=8)


# ==========================================================================
# 4. Guardar la figura generada con una fecha en el nombre del archivo
# ==========================================================================

IMAGEN_FILENAME = f"inventario_demanda_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
# Usar bbox_inches="tight" para que el texto adicional no se corte
plt.savefig(IMAGEN_FILENAME, bbox_inches="tight")
plt.show()

# ==========================================================================
# 5. Crear un archivo CSV de registro con los datos y la fecha de consulta
# ==========================================================================

CSV_FILENAME = f"registro_inventario_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
try:
    with open(CSV_FILENAME, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Escribir encabezados
        writer.writerow(["Fecha Consulta"] + HEADERS)
        # Escribir datos
        for row in data_matrix:
            writer.writerow([FECHA_CONSULTA] + row)
except IOError as e:
    print(f"Error al escribir el archivo CSV: {e}")


print("\n--- Generación de Archivos Finalizada ---")
print("Imagen generada:", IMAGEN_FILENAME)
print("Registro CSV generado:", CSV_FILENAME)
print("------------------------------------------")
