"""
Sistema de Gestión de Inventario para Restaurantes (v0.2 alpha).

Implementa y demuestra cuatro algoritmos de ordenamiento (Insertion, Bubble,
Quick, Selection) aplicados a diferentes criterios de gestión de inventario:
cantidad, tiempo de entrega, fecha límite y demanda.
"""
from datetime import datetime

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
# Algoritmos de Ordenamiento
# ==========================================================================

def insertion_sort(lista: list, key: callable) -> list:
    """
    Implementa el algoritmo Insertion Sort.

    Ordena la lista en orden ascendente basándose en la clave proporcionada.
    Utilizado para ordenar por cantidad (mas agotados primero).

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Una función lambda para especificar la clave de ordenamiento.

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

    Ordena la lista en orden ascendente (o descendente si `descending=True`)
    basándose en la clave. Utilizado para ordenar por tiempo de entrega.

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Una función lambda para especificar la clave de ordenamiento.
        descending: Si es True, ordena de mayor a menor.

    Returns:
        La lista ordenada.
    """
    n = len(lista)
    swapped = True
    while swapped:
        swapped = False
        for i in range(1, n):
            # Lógica central del Bubble Sort con manejo de orden
            comparacion = (key(lista[i - 1]) < key(lista[i])) if descending else \
                          (key(lista[i - 1]) > key(lista[i]))

            if comparacion:
                lista[i - 1], lista[i] = lista[i], lista[i - 1]
                swapped = True
        n -= 1
    return lista


def quick_sort(lista: list, key: callable) -> list:
    """
    Implementa el algoritmo Quick Sort (recursivo).

    Ordena la lista en orden ascendente basándose en la clave.
    Utilizado para ordenar por fecha (más próximas primero).

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Una función lambda para especificar la clave de ordenamiento.

    Returns:
        La lista ordenada.
    """
    if len(lista) <= 1:
        return lista
    
    pivot = lista[0]
    # Se usa list comprehensions para crear las particiones
    menos = [x for x in lista[1:] if key(x) < key(pivot)]
    iguales = [x for x in lista if key(x) == key(pivot)]
    mayor = [x for x in lista[1:] if key(x) >= key(pivot)]
    
    return quick_sort(menos, key) + iguales + quick_sort(mayor, key)


def selection_sort(lista: list, key: callable, reverse: bool = False) -> list:
    """
    Implementa el algoritmo Selection Sort.

    Ordena la lista en orden ascendente (o descendente si `reverse=True`)
    basándose en la clave. Utilizado para ordenar por demanda.

    Args:
        lista: La lista de diccionarios a ordenar.
        key: Una función lambda para especificar la clave de ordenamiento.
        reverse: Si es True, ordena de mayor a menor.

    Returns:
        La lista ordenada.
    """
    n = len(lista)
    # Se itera sobre la lista
    for i in range(n):
        index_extremo = i
        # Se busca el índice del elemento más extremo (mínimo o máximo)
        for j in range(i + 1, n):
            comparacion = (key(lista[j]) > key(lista[index_extremo])) if reverse else \
                          (key(lista[j]) < key(lista[index_extremo]))

            if comparacion:
                index_extremo = j
        # Intercambio
        lista[i], lista[index_extremo] = lista[index_extremo], lista[i]
    return lista


# ==========================================================================
# Aplicación de Ordenamientos
# ==========================================================================

# 1. Ordenar por 'cantidad' (Mas agotados primero)
inventario_por_cantidad = insertion_sort(inventario.copy(), key=lambda x: x["cantidad"])
print("--- Inventario Ordenado por Cantidad (Insertion Sort) ---")
print("Ordenados por cantidad (Mas agotados primero):")
for item in inventario_por_cantidad:
    print(f"{item['nombre']} - Cantidad: {item['cantidad']}")
print("---------------------------------------------------------")

# 2. Ordenar por 'tiempo_entrega' (Entregas más tardías primero)
inventario_por_tiempo = bubble_sort(
    inventario.copy(), key=lambda x: x["tiempo_entrega"], descending=True
)
print("\n--- Inventario Ordenado por Tiempo de Entrega (Bubble Sort) ---")
print("Ordenados por tiempo de entrega(en Días):")
for item in inventario_por_tiempo:
    print(f"{item['nombre']} - Tiempo de entrega: {item['tiempo_entrega']}")
print("-------------------------------------------------------------")

# 3. Ordenar por 'fecha_limite' (Próximas a vencer primero)
inventario_por_fecha = quick_sort(
    inventario.copy(), key=lambda x: datetime.strptime(x["fecha_limite"], "%Y-%m-%d")
)
print("\n--- Inventario Ordenado por Fecha Límite (Quick Sort) ---")
print("Ordenados por fecha límite (próximas primero):")
for item in inventario_por_fecha:
    print(f"{item['nombre']} - Fecha límite para consumir: {item['fecha_limite']}")
print("-------------------------------------------------------")

# 4. Ordenar por 'demanda' (Mas populares primero)
inventario_por_demanda = selection_sort(inventario.copy(), key=lambda x: x["demanda"], reverse=True)
print("\n--- Inventario Ordenado por Demanda (Selection Sort) ---")
print("Ordenados por demanda (Mas populares primero):")
for item in inventario_por_demanda:
    print(f"{item['nombre']} - Demanda: {item['demanda']}")
print("----------------------------------------------------")
