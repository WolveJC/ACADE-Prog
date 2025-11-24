import matplotlib.pyplot as plt
from matplotlib import table
import datetime
import csv

# Ejemplo para el inventario
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


# 1. Selection Sort para ordenar por demanda (de mayor a menor)
def selection_sort(lista, key, reverse=False):
    n = len(lista)
    for i in range(n):
        index_extremo = i
        for j in range(i + 1, n):
            if reverse:
                if key(lista[j]) > key(lista[index_extremo]):
                    index_extremo = j
            else:
                if key(lista[j]) < key(lista[index_extremo]):
                    index_extremo = j
        lista[i], lista[index_extremo] = lista[index_extremo], lista[i]
    return lista


inventario_ordenado = selection_sort(inventario.copy(), key=lambda x: x["demanda"], reverse=True)

# 2. Preparar la estructura de la tabla para visualizar
headers = ["Código", "Nombre", "Demanda", "Tiempo entrega", "Fecha límite", "Cantidad"]

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
fecha_consulta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 3. Visualización con Matplotlib
fig, ax = plt.subplots(figsize=(8, 3))
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False)

tabla = table.Table(ax, bbox=[0, 0, 1, 1])
tabla = ax.table(cellText=data_matrix, colLabels=headers, loc="center", cellLoc="center")

tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1.2, 1.2)

plt.title("Inventario ordenado por Demanda", fontsize=14)

# Agregar la fecha de la consulta en la parte inferior
plt.figtext(0.5, 0.01, f"Consulta generada: {fecha_consulta}", ha="center", fontsize=8)

# 4. Guardar la figura generada con una fecha en el nombre del archivo
imagen_filename = f"inventario_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
plt.savefig(imagen_filename, bbox_inches="tight")
plt.show()

# 5. Crear un archivo CSV de registro con los datos y la fecha de consulta
csv_filename = f"registro_inventario_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Fecha Consulta"] + headers)
    for row in data_matrix:
        writer.writerow([fecha_consulta] + row)

print("Archivos generados:")
print("Imagen:", imagen_filename)
print("Registro CSV:", csv_filename)
