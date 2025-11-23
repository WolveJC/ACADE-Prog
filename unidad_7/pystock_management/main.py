"""
Módulo principal para la ejecución de la aplicación de Gestión de Inventario.

Este módulo contiene la lógica del menú interactivo y la función para
obtener datos de productos del usuario, actuando como la capa de Presentación.
"""
import sys  
# Añadido para salida limpia
from typing import Union

from src.services.inventario_manager import Inventario
from src.models.productos import Producto


def obtener_datos_producto() -> Union[Producto, None]:
    """
    Solicita los datos del producto al usuario con validación.

    Maneja errores de conversión (ValueError) y errores de validación
    lanzados por los setters de la clase Producto.

    Returns:
        Producto: Una instancia de Producto si los datos son válidos,
                  o None en caso de error de entrada.
    """
    try:
        nombre = input("Nombre del producto: ").strip()
        # Intentamos obtener y convertir precio y cantidad
        precio = float(input("Precio del producto: "))
        cantidad = int(input("Cantidad del producto: "))
        codigo = input("Código del producto: ").strip()

        # Creamos la instancia de Producto. Las validaciones se ejecutan.
        return Producto(nombre, precio, cantidad, codigo)

    except ValueError as e:
        # Captura errores si float() o int() fallan, o si un setter lanza ValueError
        print(f"Error de entrada de datos: {e}")
        print("Asegúrate de ingresar tipos y valores correctos (números para precio/cantidad).")
        return None
    except Exception as e:
        # Captura cualquier otro error no anticipado durante la lectura o creación
        print(f"Ocurrió un error inesperado al obtener los datos: {e}")
        return None


def main_menu():
    """
    Ejecuta el menú interactivo principal de la aplicación.

    Instancia el Inventario y gestiona el flujo de opciones del usuario.
    """
    # Se asume que la clase Inventario cargará el stock al inicializarse
    mi_inventario = Inventario()

    while True:
        print("\n--- Sistema de Gestión de Inventario (Monolítico) ---")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Actualizar cantidad")
        print("4. Eliminar producto")
        print("5. Listar todos los productos")
        print("6. Salir")
        print("-----------------------------------------------------")

        try:
            opcion = input("Selecciona una opción (1-6): ").strip()

            if opcion == "1":
                print("\n>>> Agregar Producto <<<")
                nuevo_producto = obtener_datos_producto()
                if nuevo_producto:
                    mi_inventario.agg_prod(nuevo_producto)

            elif opcion == "2":
                print("\n>>> Buscar Producto <<<")
                mi_inventario.buscar_producto()

            elif opcion == "3":
                print("\n>>> Actualizar Cantidad <<<")
                mi_inventario.actualizar_cantidad()

            elif opcion == "4":
                print("\n>>> Eliminar Producto <<<")
                mi_inventario.eliminar_producto()

            elif opcion == "5":
                print("\n>>> Listar Productos <<<")
                mi_inventario.imprimir()

            elif opcion == "6":
                # Se asume que save_stock() existe y guarda los datos
                mi_inventario.save_stock()
                print("\nSaliendo del sistema de inventario. ¡Hasta pronto! ")
                # Se usa sys.exit para una salida limpia, aunque 'break' es suficiente
                sys.exit(0)

            else:
                print("Opción no válida.")
                print("Por favor, selecciona un número del 1 al 6.")

        except Exception as e:
            # W0718: Se mantiene la captura de Exception aquí para garantizar
            # que el bucle del menú no se rompa por un error
            # inesperado en las funciones del manager.
            print(f"Ocurrió un error inesperado en el menú: {e}")


# Punto de entrada de la aplicación
if __name__ == "__main__":
    main_menu()
