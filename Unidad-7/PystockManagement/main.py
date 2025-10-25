from src.services.inventario_manager import Inventario
def obtener_datos_producto():
    """Solicita los datos del producto al usuario con validación."""
    try:
        nombre = input("Nombre del producto: ").strip()
        # Intentamos obtener y convertir precio y cantidad
        precio = float(input("Precio del producto: "))
        cantidad = int(input("Cantidad del producto: "))
        codigo = input("Código del producto: ").strip()

        # Creamos la instancia de Producto. Las validaciones de los setters se ejecutan aquí.
        return Producto(nombre, precio, cantidad, codigo)
        
    except ValueError as e:
        # Captura errores si float() o int() fallan, o si un setter lanza ValueError
        print(f"Error de entrada de datos: {e}. Asegúrate de ingresar tipos y valores correctos.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado al obtener los datos: {e}")
        return None

def main_menu():
    """Ejecuta el menú interactivo."""
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

            if opcion == '1':
                print("\n>>> Agregar Producto <<<")
                nuevo_producto = obtener_datos_producto()
                if nuevo_producto:
                    mi_inventario.agg_prod(nuevo_producto)

            elif opcion == '2':
                print("\n>>> Buscar Producto <<<")
                mi_inventario.buscar_producto()

            elif opcion == '3':
                print("\n>>> Actualizar Cantidad <<<")
                mi_inventario.actualizar_cantidad()

            elif opcion == '4':
                print("\n>>> Eliminar Producto <<<")
                mi_inventario.eliminar_producto()

            elif opcion == '5':
                print("\n>>> Listar Productos <<<")
                mi_inventario.imprimir()

            elif opcion == '6':
                mi_inventario.save_stock()
                print("\nSaliendo del sistema de inventario. ¡Hasta pronto!")
                break

            else:
                print("Opción no válida. Por favor, selecciona un número del 1 al 6.")

        except Exception as e:
            print(f" Ocurrió un error inesperado en el menú: {e}")
            
# Punto de entrada de la aplicación
if __name__ == "__main__":
    main_menu()