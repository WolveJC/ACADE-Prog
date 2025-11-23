"""
Módulo InventarioManager.

Contiene la clase Inventario, responsable de gestionar la colección de
objetos Producto y manejar la persistencia de datos (carga y guardado
en formato JSON).
"""

import os
import json

from ..models.productos import Producto


class Inventario:
    """
    Gestiona la colección de objetos Producto y sus operaciones de persistencia.

    Attributes:
        route_file (str): Ruta completa al archivo JSON de stock.
        productos (dict): Diccionario de productos, clave=código, valor=Objeto Producto.
    """

    def __init__(self, file_name: str = "data_stock.json"):
        """
        Inicializa el Inventario, configura la ruta del archivo y carga el stock inicial.

        Args:
            file_name: Nombre del archivo de persistencia JSON.
        """
        # Crear referencia de ruta (asumiendo estructura src/services/inventario_manager.py)
        current_dir = os.path.dirname(__file__)
        # Construye la ruta para que apunte a la carpeta 'models' un nivel superior.
        # Esto es un patrón común en proyectos modulados.
        base_dir = os.path.join(current_dir, "..", "models_data")

        # Crear archio en la ruta indicada y nombre declarado
        self.route_file = os.path.join(base_dir, file_name)

        # Asegurar que exista la ruta
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)  # Si la ruta NO existe ENTONCES la crea

        # Diccionario: clave=código (str), valor=objeto Producto
        # El operador 'or {}' garantiza que self.productos sea un diccionario.
        self.productos = self.load_stock() or {}

    def load_stock(self) -> dict | None:
        """
        Carga los datos del inventario desde el archivo JSON de persistencia.

        Transforma los datos JSON cargados de vuelta a objetos Producto.

        Returns:
            dict | None: Un diccionario con objetos Producto si la carga es exitosa,
                         o None si hay un error o el archivo no existe.
        """
        if os.path.exists(self.route_file):
            try:
                # W1514: Especificar 'encoding="utf-8"' es buena práctica.
                with open(self.route_file, "r", encoding="utf-8") as dicc:
                    data_loaded = json.load(dicc)
                    stock_loaded = {}
                    for codigo, data in data_loaded.items():
                        # Aquí se reconstruye el objeto Producto
                        stock_loaded[codigo] = Producto(
                            data["nombre"], data["precio"], data["cantidad"], data["codigo"]
                        )
                    return stock_loaded
            except (json.JSONDecodeError, FileNotFoundError, TypeError) as e:
                # Captura errores de JSON mal formado o problemas en la creación de Producto
                print(f"Error al cargar/procesar el inventario desde '{self.route_file}': {e}")
                print("Se iniciará un inventario Vacío.")
        return None

    def save_stock(self):
        """
        Guarda el inventario actual en el archivo JSON de persistencia.

        Convierte los objetos Producto a un diccionario básico para la serialización.
        """
        # Convertir objetos en Producto a un diccionario básico
        save_data = {}
        for codigo, producto_obj in self.productos.items():
            save_data[codigo] = {
                "codigo": producto_obj.codigo,
                "nombre": producto_obj.nombre,
                "precio": producto_obj.precio,
                "cantidad": producto_obj.cantidad,
            }
        try:
            # W1514: Especificar 'encoding="utf-8"' es buena práctica.
            with open(self.route_file, "w", encoding="utf-8") as file:
                json.dump(save_data, file, indent=4)
            print(f"Éxito: Inventario guardado en '{self.route_file}'")
        except IOError as e:
            # W0718: Cambiado de 'Exception' a 'IOError' para manejo específico de disco/ruta.
            print(f"Error: No fue posible guardar el inventario en '{self.route_file}'")
            print(f"Detalle del error: {e}")

    def agg_prod(self, producto: Producto):
        """
        Agrega un nuevo objeto Producto al inventario.

        Args:
            producto: El objeto Producto a añadir.
        """
        if not isinstance(producto, Producto):
            print("Error: Solo se pueden agregar objetos de tipo 'Producto' al inventario.")
            return

        if producto.codigo in self.productos:
            print(f"Error: El producto con código '{producto.codigo}' ya existe en el inventario.")
            return

        self.productos[producto.codigo] = producto
        print(f"Éxito: Producto '{producto.nombre}' (Código: {producto.codigo}) agregado.")

    def imprimir(self):
        """Muestra una lista detallada de todos los productos en el inventario."""
        if not self.productos:
            print("El inventario está vacío. No hay productos para mostrar.")
            return

        print("\n--- Listado de Productos en Inventario ---")
        # Itera sobre los valores (objetos Producto) del diccionario
        for producto_obj in self.productos.values():
            print(producto_obj)
            print("-" * 30)
        print("--- Fin del Listado ---")

    def buscar_producto(self):
        """Solicita un código y muestra la información del producto si existe."""
        id_search = input("Ingrese el código del producto a buscar: ").strip()

        if id_search in self.productos:
            # Acceso directo al objeto Producto por su código
            resultado_producto = self.productos[id_search]
            print("\n ¡Producto Encontrado!")
            print(resultado_producto)
            print("--------------------------\n")
        else:
            print(f"Error: El producto con el código {id_search} no se encuentra en el inventario.")

    def actualizar_cantidad(self):
        """Solicita un código y actualiza la cantidad de ese producto."""
        id_search = input("Ingrese el código del producto a actualizar: ").strip()

        if id_search not in self.productos:
            print(f"Error: Producto con código '{id_search}' no encontrado.")
            return

        producto_a_actualizar = self.productos[id_search]

        # Lógica de validación de entrada
        while True:
            try:
                # Muestra el nombre del producto que se está actualizando
                new_cantidad_str = input(
                    f"Ingrese la nueva cantidad para '{producto_a_actualizar.nombre}' "
                    f"(actual: {producto_a_actualizar.cantidad}): "
                ).strip()
                new_cantidad = int(new_cantidad_str)

                if new_cantidad < 0:
                    print("Error: La cantidad no puede ser un número negativo. Inténtalo de nuevo.")
                    continue

                break

            except ValueError:
                print("Error de Valor: Se espera una cantidad numérica entera.")
            except Exception as e:
                # Se mantiene la captura general para errores inesperados en un contexto interactivo
                print(f"Ocurrió un error inesperado al leer la nueva cantidad: {e}")

        # Asigna la nueva cantidad (llamando al setter de Producto)
        try:
            producto_a_actualizar.cantidad = new_cantidad
            print(
                f"Éxito: Cantidad del producto '{producto_a_actualizar.nombre}'"
                f"actualizada a {new_cantidad}."
            )
        except ValueError as e:
            # Captura si el setter de Producto rechaza el valor
            print(f"Error de validación: {e}")

    def eliminar_producto(self):
        """Solicita un código y elimina el producto del inventario."""
        id_search = input("Ingrese el código del producto a eliminar: ").strip()

        if id_search not in self.productos:
            print(f"Error: Producto con código '{id_search}' no encontrado.")
            return

        # Opcional: Mostrar nombre antes de eliminar
        nombre_producto = self.productos[id_search].nombre

        del self.productos[id_search]  # Elimina la referencia del diccionario
        print(
            f"Éxito: Producto '{nombre_producto}' (Código: {id_search}) eliminado del inventario."
        )
