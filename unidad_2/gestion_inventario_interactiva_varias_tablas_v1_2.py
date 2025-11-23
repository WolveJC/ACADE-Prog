"""
Sistema de Gestión de Inventario Interactivo (v1.2 - Múltiples Tablas).

Permite el ingreso interactivo de productos, aplica cuatro algoritmos de
ordenamiento a criterios clave (cantidad, tiempo, fecha, demanda) y genera
una visualización tabular (Matplotlib) y un archivo de registro CSV para
cada uno de los criterios.
"""

# Standard library
import csv
import datetime
import random
import string
# import sys  # Eliminado W0611: sys no se usa.
from typing import Union, List, Tuple # Añadido List/Tuple para compatibilidad si Python < 3.9

# Third-party libraries
import matplotlib.pyplot as plt

# ------------------------------------------
# 1. Funciones Auxiliares
# ------------------------------------------


def generar_codigo_aleatorio(longitud: int = 6) -> str:
    """
    Genera un código alfanumérico aleatorio.

    Args:
        longitud: Longitud del código deseado.

    Returns:
        Cadena alfanumérica aleatoria.
    """
    caracteres = string.ascii_uppercase + string.digits
    return "".join(random.choices(caracteres, k=longitud))


def _obtener_entero_valido(prompt: str) -> Union[int, None]:
    """Función auxiliar para obtener una entrada entera válida."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Entrada inválida. Se espera un número entero.")
        return None


def _obtener_fecha_valida(prompt: str, formato: str = "%Y-%m-%d") -> Union[str, None]:
    """Función auxiliar para obtener una fecha válida."""
    fecha_str = input(prompt).strip()
    try:
        datetime.datetime.strptime(fecha_str, formato)
        return fecha_str
    except ValueError:
        print(f"Fecha inválida. Asegúrate de ingresar en el formato {formato}.")
        return None


# ------------------------------------------
# Ingreso interactivo de productos (W0621 Corregido)
# ------------------------------------------
def ingresar_productos(lista_inventario: list):
    """Permite al usuario ingresar productos de manera interactiva."""
    while True:
        print("\n--- Ingrese los datos del nuevo producto ---")

        # 1. Código
        codigo_input = input("Código (dejar vacío para auto-generar): ").strip()
        if not codigo_input:
            codigo = generar_codigo_aleatorio()
            # W0621 corregido: usar lista_inventario en lugar de inventario
            existentes = {p["codigo"] for p in lista_inventario}
            while codigo in existentes:
                codigo = generar_codigo_aleatorio()
            print(f"Se generó el código automático: {codigo}")
        else:
            codigo = codigo_input
            # W0621 corregido: usar lista_inventario en lugar de inventario
            if codigo in {p["codigo"] for p in lista_inventario}:
                print(f"Error: El código '{codigo}' ya existe.")
                continue

        nombre = input("Nombre del producto: ").strip()
        if not nombre:
            print("El nombre no puede estar vacío.")
            continue

        # 2. Demanda
        demanda = _obtener_entero_valido("Demanda (valor entre 1-10): ")
        if (
            demanda is None
            or demanda < 1
            or demanda > 10):
            print("La demanda debe ser un número entre 1 y 10.")
            continue

        # 3. Tiempo de entrega
        tiempo_entrega = _obtener_entero_valido("Tiempo de entrega (en días): ")
        if tiempo_entrega is None or tiempo_entrega < 0:
            print("El tiempo de entrega no puede ser negativo.")
            continue

        # 4. Fecha límite
        fecha_limite = _obtener_fecha_valida("Fecha límite para consumo (YYYY-MM-DD): ")
        if fecha_limite is None:
            continue

        # 5. Cantidad
        cantidad = _obtener_entero_valido("Cantidad en inventario: ")
        if cantidad is None or cantidad < 0:
            print("La cantidad en inventario no puede ser negativa.")
            continue

        producto = {
            "codigo": codigo,
            "nombre": nombre,
            "demanda": demanda,
            "tiempo_entrega": tiempo_entrega,
            "fecha_limite": fecha_limite,
            "cantidad": cantidad,
        }
        lista_inventario.append(producto)

        continuar = input("¿Desea ingresar otro producto? (s/n): ").strip().lower()
        if continuar != "s":
            break


# ------------------------------------------
# 2. Funciones de ordenamiento
# ------------------------------------------


def insertion_sort(lista: list, key: callable, descending: bool = False) -> list:
    """
    Implementa el Insertion Sort, adaptable para orden ascendente o descendente.
    ...
    """
    for i in range(1, len(lista)):
        actual = lista[i]
        j = i - 1

        while j >= 0:
            # Lógica de comparación
            comparacion = (
                (key(lista[j]) < key(actual)) if descending else (key(lista[j]) > key(actual))
            )

            if comparacion:
                lista[j + 1] = lista[j]
                j -= 1
            else:
                break
        lista[j + 1] = actual
    return lista


def bubble_sort(lista: list, key: callable, descending: bool = False) -> list:
    """
    Implementa el algoritmo Bubble Sort.
    ...
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
    Implementa el Quick Sort recursivo (orden ascendente).
    ...
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
    Implementa el Selection Sort (utilizado aquí de forma estable con lista temporal).
    ...
    """
    # Esta implementación es la versión 'estable' del selection sort
    nueva_lista = []
    temp = lista.copy()
    while temp:
        candidato = temp[0]
        indice_candidato = 0
        for i, item in enumerate(temp):
            comparacion = (key(item) > key(candidato)) if reverse else (key(item) < key(candidato))

            if comparacion:
                candidato = item
                indice_candidato = i

        nueva_lista.append(candidato)
        temp.pop(indice_candidato)
    return nueva_lista


# ------------------------------------------
# 3. Generar listas ordenadas utilizando distintos algoritmos (W0621 Corregido)
# ------------------------------------------


def generar_inventarios_ordenados(datos_originales: list) -> dict:
    """Aplica los cuatro algoritmos de ordenamiento al inventario."""
    return {
        "cantidad": insertion_sort(
            datos_originales.copy(), key=lambda x: x["cantidad"], descending=False
        ),
        "tiempo": bubble_sort(
            datos_originales.copy(), key=lambda x: x["tiempo_entrega"], descending=True
        ),
        "fecha": quick_sort(
            datos_originales.copy(),
            key=lambda x: datetime.datetime.strptime(x["fecha_limite"], "%Y-%m-%d"),
        ),
        "demanda": selection_sort(
            datos_originales.copy(), 
            key=lambda x: x["demanda"],
            reverse=True
        ),
    }


# ------------------------------------------
# 4. Función para visualizar y guardar cada tabla (E/W Corregidos)
# ------------------------------------------


def generate_table_and_csv(
    sorted_data: list, title: str, headers_visual: list, csv_headers: list, # <-- Firma Corregida
    query_date: str, algorithm_key: str
):
    """
    Genera una tabla visual con Matplotlib, guarda la imagen PNG y un CSV de registro.

    Args:
        sorted_data: La lista de diccionarios de inventario ya ordenada.
        title: Título del gráfico.
        headers_visual: Encabezados de la tabla para Matplotlib.
        csv_headers: Encabezados para el archivo CSV.
        query_date: Fecha y hora de la consulta (timestamp).
        algorithm_key: Clave del algoritmo (usada para nombrar archivos).
    """
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
    # E0606 Corregido: Usar el parámetro 'headers_visual' para la tabla
    tbl = ax.table(cellText=data_matrix, colLabels=headers_visual, loc="center", cellLoc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1.2, 1.2)

    plt.title(title, fontsize=14)
    plt.figtext(0.5, 0.01, f"Consulta generada: {query_date}", ha="center", fontsize=8)

    # Guardar la figura
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"inventario_{algorithm_key}_{timestamp}.png"

    try:
        plt.savefig(image_filename, bbox_inches="tight")
        plt.show()  # Muestra la tabla
    except IOError as e:
        print(f" Error al guardar la imagen {image_filename}: {e}")

    plt.close(fig)

    # Guardar registro en CSV
    csv_filename = f"registro_{algorithm_key}_{timestamp}.csv"
    try:
        with open(csv_filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # W0613 Corregido: Usar el parámetro 'csv_headers' para el CSV
            writer.writerow(["Fecha Consulta"] + csv_headers)
            for row in data_matrix:
                writer.writerow([query_date] + row)
    except IOError as e:
        print(f"Error al escribir el archivo CSV {csv_filename}: {e}")

    print(f"\n {title} - Archivos generados:")
    print(" Imagen:", image_filename)
    print(" Registro CSV:", csv_filename)
    print("-----------------------------------------")


# ------------------------------------------
# 5. Ejecución Principal
# ------------------------------------------

if __name__ == "__main__":
    inventario = []
    ingresar_productos(inventario)

    if not inventario:
        print("\n No se ingresaron productos. El programa se cerrará.")
        # Usamos quit() o exit() en lugar de sys.exit() ya que sys fue eliminado
        quit()

    inventarios_ordenados = generar_inventarios_ordenados(inventario)

    # Definición de variables locales para los encabezados
    headers_visual = ["Código", "Nombre", "Demanda", "Tiempo entrega", "Fecha límite", "Cantidad"]
    headers_csv = headers_visual.copy()
    
    fecha_consulta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ordenamientos_config = [
        {
            "title": "Ordenamiento por Cantidad (Insertion Sort) - Mas agotados",
            "data": inventarios_ordenados["cantidad"],
            "algorithm_key": "insertion_cantidad",
        },
        {
            "title": "Ordenamiento por Tiempo de entrega (Bubble Sort) - Mas tardados",
            "data": inventarios_ordenados["tiempo"],
            "algorithm_key": "bubble_tiempo",
        },
        {
            "title": "Ordenamiento por Fecha límite (Quick Sort) - Mas próximas",
            "data": inventarios_ordenados["fecha"],
            "algorithm_key": "quick_fecha",
        },
        {
            "title": "Ordenamiento por Demanda (Selection Sort) - Mas populares",
            "data": inventarios_ordenados["demanda"],
            "algorithm_key": "selection_demanda",
        },
    ]

    for orden in ordenamientos_config:
        generate_table_and_csv(
            sorted_data=orden["data"],
            title=orden["title"],
            # E1123/E1120 Corregidos: Usar los nombres de argumentos esperados
            headers_visual=headers_visual, 
            csv_headers=headers_csv,
            query_date=fecha_consulta,
            algorithm_key=orden["algorithm_key"],
        )