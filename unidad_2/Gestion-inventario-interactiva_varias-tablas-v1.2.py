import matplotlib.pyplot as plt
from matplotlib import table
import datetime
import csv
import random
import string


# ------------------------------------------
# Función para generar código alfanumérico aleatorio
def generar_codigo_aleatorio(longitud=6):
    caracteres = string.ascii_uppercase + string.digits
    return "".join(random.choices(caracteres, k=longitud))


# ------------------------------------------
# 1. Ingreso interactivo de productos con código alfanumérico
inventario = []

while True:
    print("\nIngrese los datos del nuevo producto:")

    # Se solicita el código; si se deja vacío, se genera automáticamente un código alfanumérico
    codigo_input = input("Código:  ").strip()
    if codigo_input == "":
        codigo = generar_codigo_aleatorio()  # Código aleatorio de 6 caracteres
        # Verificar que el código sea único:
        existentes = [p["codigo"] for p in inventario]
        while codigo in existentes:
            codigo = generar_codigo_aleatorio()
        print(f"Se generó el código automático: {codigo}")
    else:
        codigo = codigo_input  # Se acepta el código alfanumérico ingresado por el usuario

    nombre = input("Nombre del producto: ").strip()

    try:
        demanda = int(input("Demanda (valor entre 1-10): ").strip())
    except ValueError:
        print("Entrada inválida. Se espera un número entero para la demanda.")
        continue

    try:
        tiempo_entrega = int(input("Tiempo de entrega (en días): ").strip())
    except ValueError:
        print("Entrada inválida. Se espera un número entero para el tiempo de entrega.")
        continue

    fecha_limite = input("Fecha límite para consumo (YYYY-MM-DD): ").strip()
    try:
        datetime.datetime.strptime(fecha_limite, "%Y-%m-%d")
    except ValueError:
        print("Fecha inválida. Asegúrate de ingresar en el formato YYYY-MM-DD.")
        continue

    try:
        cantidad = int(input("Cantidad en inventario: ").strip())
    except ValueError:
        print("Entrada inválida. Se espera un número entero para la cantidad.")
        continue

    producto = {
        "codigo": codigo,
        "nombre": nombre,
        "demanda": demanda,
        "tiempo_entrega": tiempo_entrega,
        "fecha_limite": fecha_limite,
        "cantidad": cantidad,
    }
    inventario.append(producto)

    continuar = input("¿Desea ingresar otro producto? (s/n): ").strip().lower()
    if continuar != "s":
        break

if not inventario:
    print("No se ingresaron productos. El programa se cerrará.")
    exit()

# ------------------------------------------
# 2. Funciones de ordenamiento


# Insertion Sort:
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


# Bubble Sort:
def bubble_sort(lista, key, descending=False):
    n = len(lista)
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, n):
            if descending:
                if key(lista[i - 1]) < key(lista[i]):
                    lista[i - 1], lista[i] = lista[i], lista[i - 1]
                    swapped = True
            else:
                if key(lista[i - 1]) > key(lista[i]):
                    lista[i - 1], lista[i] = lista[i], lista[i - 1]
                    swapped = True
        n -= 1
    return lista


# Quick Sort:
def quick_sort(lista, key):
    if len(lista) <= 1:
        return lista
    else:
        pivot = lista[0]
        menos = [x for x in lista[1:] if key(x) < key(pivot)]
        iguales = [x for x in lista if key(x) == key(pivot)]
        mayor = [x for x in lista[1:] if key(x) >= key(pivot)]
        return quick_sort(menos, key) + iguales + quick_sort(mayor, key)


# Selection Sort:
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


# ------------------------------------------
# 3. Generar listas ordenadas utilizando distintos algoritmos

# Ordenar por Cantidad usando Insertion Sort (Mas agotados primero)
inventario_por_cantidad = insertion_sort(
    inventario.copy(), key=lambda x: x["cantidad"], descending=False
)

# Ordenar por Tiempo de entrega usando Bubble Sort (Mas tardados primero)
inventario_por_tiempo = bubble_sort(
    inventario.copy(), key=lambda x: x["tiempo_entrega"], descending=True
)

# Ordenar por Fecha límite usando Quick Sort (las fechas más próximas primero)
inventario_por_fecha = quick_sort(
    inventario.copy(), key=lambda x: datetime.datetime.strptime(x["fecha_limite"], "%Y-%m-%d")
)

# Ordenar por Demanda usando Selection Sort (Preferencia del cliente)
inventario_por_demanda = selection_sort(inventario.copy(), key=lambda x: x["demanda"], reverse=True)

# ------------------------------------------
# 4. Función para visualizar y guardar cada tabla


def generate_table_and_csv(sorted_data, title, headers, query_date, algorithm_key):
    # Preparar la matriz de datos para la tabla
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

    # Crear figura para la tabla
    fig, ax = plt.subplots(figsize=(10, len(sorted_data) * 0.6 + 2))
    ax.axis("off")
    tbl = ax.table(cellText=data_matrix, colLabels=headers, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1.2, 1.2)

    plt.title(title, fontsize=14)
    plt.figtext(0.5, 0.01, f"Consulta generada: {query_date}", ha="center", fontsize=8)

    # Guardar la figura con un nombre que incluya la clave del algoritmo y un timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"inventario_{algorithm_key}_{timestamp}.png"
    plt.savefig(image_filename, bbox_inches="tight")
    plt.show()
    plt.close(fig)

    # Guardar registro en CSV
    csv_filename = f"registro_{algorithm_key}_{timestamp}.csv"
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Fecha Consulta"] + headers)
        for row in data_matrix:
            writer.writerow([query_date] + row)

    print(f"{title} - Archivos generados:")
    print(" Imagen:", image_filename)
    print(" Registro CSV:", csv_filename)
    print("-----------------------------------------")


# ------------------------------------------
# 5. Visualización: Generar una tabla para cada criterio de ordenamiento

headers = ["Código", "Nombre", "Demanda", "Tiempo entrega", "Fecha límite", "Cantidad"]
fecha_consulta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

ordenamientos = [
    {
        "title": "Ordenamiento por Cantidad (Insertion Sort)",
        "data": inventario_por_cantidad,
        "algorithm_key": "insertion_cantidad",
    },
    {
        "title": "Ordenamiento por Tiempo de entrega (Bubble Sort)",
        "data": inventario_por_tiempo,
        "algorithm_key": "bubble_tiempo",
    },
    {
        "title": "Ordenamiento por Fecha límite (Quick Sort)",
        "data": inventario_por_fecha,
        "algorithm_key": "quick_fecha",
    },
    {
        "title": "Ordenamiento por Demanda (Selection Sort)",
        "data": inventario_por_demanda,
        "algorithm_key": "selection_demanda",
    },
]

for orden in ordenamientos:
    generate_table_and_csv(
        sorted_data=orden["data"],
        title=orden["title"],
        headers=headers,
        query_date=fecha_consulta,
        algorithm_key=orden["algorithm_key"],
    )
