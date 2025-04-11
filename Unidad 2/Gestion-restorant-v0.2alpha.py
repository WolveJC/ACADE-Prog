from datetime import datetime

# Ejemplo para el inventario
inventario = [
    {"codigo": 1, "nombre": "Manzana", "demanda": 8, "tiempo_entrega": 3, "fecha_limite": "2025-04-28", "cantidad": 15},
    {"codigo": 2, "nombre": "Banana", "demanda": 7, "tiempo_entrega": 5, "fecha_limite": "2025-04-25", "cantidad": 2},
    {"codigo": 3, "nombre": "Lechuga", "demanda": 6, "tiempo_entrega": 2, "fecha_limite": "2025-04-22", "cantidad": 7},
    {"codigo": 4, "nombre": "Tomate", "demanda": 9, "tiempo_entrega": 4, "fecha_limite": "2025-05-01", "cantidad": 3},
]

# Algoritmos de ordenamiento que se usarán
# 1. Insertion Sort para ordenar por cantidad (de menor a mayor)
def insertion_sort(lista, key):
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1
        while j >= 0 and key(lista[j]) > key(actual):
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = actual
    return lista

# Ordenar por 'cantidad' para identificar alimentos que se están agotando
inventario_por_cantidad = insertion_sort(inventario.copy(), key=lambda x: x["cantidad"])
print("Ordenados por cantidad (Mas agotados primero):")
for item in inventario_por_cantidad:
    print(f"{item['nombre']} - Cantidad: {item['cantidad']}")

# 2. Bubble Sort para ordenar por tiempo de entrega (de mayor a menor)
def bubble_sort(lista, key, descending=False):
    n = len(lista)
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, n):
            if descending:
                if key(lista[i-1]) < key(lista[i]):
                    lista[i-1], lista[i] = lista[i], lista[i-1]
                    swapped = True
            else:
                if key(lista[i-1]) > key(lista[i]):
                    lista[i-1], lista[i] = lista[i], lista[i-1]
                    swapped = True
        n -= 1
    return lista

# Ordenar por 'tiempo_entrega' de mayor a menor (priorizando entregas mas tardías)
inventario_por_tiempo = bubble_sort(inventario.copy(), key=lambda x: x["tiempo_entrega"], descending=True)
print("\nOrdenados por tiempo de entrega(en Días):")
for item in inventario_por_tiempo:
    print(f"{item['nombre']} - Tiempo de entrega: {item['tiempo_entrega']}")

# 3. Quick Sort para ordenar por fecha límite de consumo (las más próximas primero)
def quick_sort(lista, key):
    if len(lista) <= 1:
        return lista
    else:
        pivot = lista[0]
        menos = [x for x in lista[1:] if key(x) < key(pivot)]
        iguales = [x for x in lista if key(x) == key(pivot)]
        mayor = [x for x in lista[1:] if key(x) >= key(pivot)]
        return quick_sort(menos, key) + iguales + quick_sort(mayor, key)

# Conversión de la fecha
inventario_por_fecha = quick_sort(inventario.copy(), key=lambda x: datetime.strptime(x["fecha_limite"], "%Y-%m-%d"))
print("\nOrdenados por fecha límite (próximas primero):")
for item in inventario_por_fecha:
    print(f"{item['nombre']} - Fecha límite para consumir: {item['fecha_limite']}")

# 4. Selection Sort para ordenar por demanda (de mayor a menor)
def selection_sort(lista, key, reverse=False):
    n = len(lista)
    for i in range(n):
        index_extremo = i
        for j in range(i+1, n):
            if reverse:
                if key(lista[j]) > key(lista[index_extremo]):
                    index_extremo = j
            else:
                if key(lista[j]) < key(lista[index_extremo]):
                    index_extremo = j
        lista[i], lista[index_extremo] = lista[index_extremo], lista[i]
    return lista

# Ordenar por 'demanda' de mayor a menor (Preferencias del cliente primero)
inventario_por_demanda = selection_sort(inventario.copy(), key=lambda x: x["demanda"], reverse=True)
print("\nOrdenados por demanda (Mas populares primero):")
for item in inventario_por_demanda:
    print(f"{item['nombre']} - Demanda: {item['demanda']}")
