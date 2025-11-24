import matplotlib.pyplot as plt
from matplotlib import table
import datetime
import csv

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
# Algoritmos de ordenamiento
# 1. Insertion Sort (modificado para aceptar orden descendente o ascendente)
def insertion_sort(lista, key, descending=False):
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        if descending:
            while j >= 0 and key(lista[j]) < key(actual):
                lista[j + 1] = lista[j]
                j -= 1
        else:
            while j >= 0 and key(lista[j]) > key(actual):
                lista[j + 1] = lista[j]
                j -= 1
        lista[j + 1] = actual
    return lista


# 2. Quick Sort (modificado para ordenar por fecha límite de forma recursiva y asumiendo orden ascendente)
def quick_sort(lista, key):
    if len(lista) <= 1:
        return lista
    else:
        pivot = lista[0]
        menos = [x for x in lista[1:] if key(x) < key(pivot)]
        iguales = [x for x in lista if key(x) == key(pivot)]
        mayor = [x for x in lista[1:] if key(x) >= key(pivot)]
        return quick_sort(menos, key) + iguales + quick_sort(mayor, key)


# 3. Selection Sort (implementado de forma estable para listas pequeñas)
def selection_sort(lista, key, reverse=False):
    nueva_lista = []
    temp = lista.copy()
    while temp:
        candidato = temp[0]
        for item in temp:
            if reverse:
                if key(item) > key(candidato):
                    candidato = item
            else:
                if key(item) < key(candidato):
                    candidato = item
        nueva_lista.append(candidato)
        temp.remove(candidato)
    return nueva_lista


# ---------------------------------------
# Ordenamiento jerárquico

# Para aplicar un sort múltiple estable se ordena partiendo del criterio menos importante:
# 4º (menos importante): Demanda (Selection Sort, orden descendente)
ordenados = selection_sort(inventario.copy(), key=lambda x: x["demanda"], reverse=True)

# 3º: Tiempo de entrega (con Insertion Sort en orden descendente)
ordenados = insertion_sort(ordenados, key=lambda x: x["tiempo_entrega"], descending=True)

# 2º: Cantidad en inventario (con Insertion Sort en orden ascendente)
ordenados = insertion_sort(ordenados, key=lambda x: x["cantidad"], descending=False)

# 1º (más importante): Fecha límite (con Quick Sort en orden ascendente)
ordenados = quick_sort(
    ordenados, key=lambda x: datetime.datetime.strptime(x["fecha_limite"], "%Y-%m-%d")
)

# ---------------------------------------
# Preparar datos en cabeceras para la visualizar
headers = ["Código", "Nombre", "Demanda", "Tiempo entrega(Días)", "Fecha límite", "Cantidad"]

data_matrix = []
for item in ordenados:
    row = [
        item["codigo"],
        item["nombre"],
        item["demanda"],
        item["tiempo_entrega"],
        item["fecha_limite"],
        item["cantidad"],
    ]
    data_matrix.append(row)

# Fecha y hora de la consulta
fecha_consulta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ---------------------------------------
# Visualización con Matplotlib
fig, ax = plt.subplots(figsize=(10, len(ordenados) * 0.6 + 2))
ax.axis("off")

tabla = ax.table(cellText=data_matrix, colLabels=headers, loc="center", cellLoc="center")
tabla.auto_set_font_size(False)
tabla.set_fontsize(10)
tabla.scale(1.2, 1.2)

plt.title("Inventario Ordenado Jerárquicamente", fontsize=16)
plt.figtext(0.5, 0.01, f"Consulta generada: {fecha_consulta}", ha="center", fontsize=8)

# Guardar una imagen con un timestamp (PNG)
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
nombre_imagen = f"inventario_jerarquico_{timestamp}.png"
plt.savefig(nombre_imagen, bbox_inches="tight")
plt.show()

# ---------------------------------------
# Generar un archivo CSV con el registro de la consulta
nombre_csv = f"registro_inventario_jerarquico_{timestamp}.csv"
with open(nombre_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Escribir encabezado con la fecha de consulta
    writer.writerow(["Fecha Consulta"] + headers)
    for row in data_matrix:
        writer.writerow([fecha_consulta] + row)

print("Archivos generados:")
print(" Imagen:", nombre_imagen)
print(" Registro CSV:", nombre_csv)
