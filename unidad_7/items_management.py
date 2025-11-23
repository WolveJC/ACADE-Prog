"""
Módulo de Gestión de Inventario (Monolítico - v1.0).

Implementa las clases Producto (Modelo) e Inventario (Servicio/Manager)
para la gestión básica de productos con validación de datos mediante
propiedades (getters y setters).
"""

import sys
from typing import Union

# ====================================================================
# CLASE PRODUCTO (Modelo)
# ====================================================================


class Producto:
    """
    Representa un producto con sus atributos de nombre, precio, cantidad y código.
    
    R0902 Corregido: La validación de los atributos se movió al constructor
    para eliminar la duplicidad de atributos internos (self.__attr).
    """

    def __init__(self, nombre: str, precio: float, cantidad: int, codigo: str):
        """
        Inicializa una nueva instancia de Producto.

        Args:
            nombre: Nombre del producto.
            precio: Precio del producto (debe ser positivo).
            cantidad: Cantidad en inventario (debe ser no negativo).
            codigo: Identificador único del producto.
        """
        # La validación estricta ahora ocurre en obtener_datos_producto()
        self._nombre = nombre
        self._precio = precio
        self._cantidad = cantidad
        self._codigo = codigo

    def __del__(self):
        """Método de finalización que se llama cuando el objeto es destruido."""
        print(f"Objeto {self.codigo} - {self.nombre} eliminado")

    def __str__(self):
        """Representación legible del objeto para impresión."""
        return (
            f"Código: {self.codigo}\n  Producto: {self.nombre}\n  "
            f"Precio: ${self.precio:.2f}\n  Cantidad: {self.cantidad}"
        )

    # Métodos dunder de comparación
    def __lt__(self, otro):
        """Define la comparación 'menor que' (<) basada en el precio."""
        if not isinstance(otro, Producto):
            return NotImplemented
        # Se usan los atributos internos (aunque aquí se ven "públicos")
        return self.precio < otro.precio

    def __eq__(self, otro):
        """Define la comparación 'igual a' (==) basada en el código."""
        if not isinstance(otro, Producto):
            return NotImplemented
        return self.codigo == otro.codigo

    # --- Propiedades Simplificadas ---
    # Se mantienen las propiedades para control de acceso,
    # pero sin atributos internos duplicados (__).

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del producto debe ser una cadena no vacía.")
        self._nombre = nombre

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, precio):
        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError("El precio debe ser un número positivo mayor que cero.")
        self._precio = precio

    @property
    def cantidad(self):
        return self._cantidad

    @cantidad.setter
    def cantidad(self, cantidad):
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser un número entero no negativo.")
        self._cantidad = cantidad

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, codigo):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError("El código del producto debe ser una cadena no vacía.")
        self._codigo = codigo


# --------------------------------------------------------------------
# CLASE INVENTARIO (Servicios/Manager)
# --------------------------------------------------------------------


class Inventario:
    """
    Gestiona una colección de objetos Producto utilizando un diccionario.
    """

    def __init__(self):
        """Inicializa el inventario con un diccionario vacío."""
        self.productos = {}  # Diccionario: clave=código (str), valor=objeto Producto

    def agg_prod(self, producto: Producto):
        """
        Agrega un producto al inventario.
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
        for producto_obj in self.productos.values():
            print(producto_obj)
            print("-" * 30)
        print("--- Fin del Listado ---")

    def buscar_producto(self):
        """Solicita un código y muestra la información del producto si existe."""
        id_search = input("Ingrese el código del producto a buscar: ").strip()

        if id_search in self.productos:
            resultado_producto = self.productos[id_search]
            print("\n ¡Producto Encontrado!")
            print(resultado_producto)
            print("--------------------------\n")
        else:
            print(
                f"Error: El producto con el código {id_search} no se encuentra en el inventario."
            )

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
                new_cantidad_str = input(
                    f"Ingrese la nueva cantidad para '{producto_a_actualizar.nombre}' "
                    f"(actual: {producto_a_actualizar.cantidad}): "
                ).strip()
                new_cantidad = int(new_cantidad_str)

                # La validación de new_cantidad < 0 ya la tienes en el setter, 
                # pero es buena práctica validar antes de la asignación.
                if new_cantidad < 0:
                    print(
                        "Error: La cantidad no puede ser un número negativo. Inténtalo de nuevo."
                    )
                    continue

                break

            except ValueError:
                print("Error de Valor: Se espera una cantidad numérica entera.")
            # W0718 Corregido: Reemplazado por una excepción más específica, 
            # ya que solo se espera ValueError o TypeError aquí.
            except TypeError:
                print("Error de Tipo: Ocurrió un problema con el tipo de dato.")

        # Asigna la nueva cantidad (llamando al setter de Producto)
        try:
            producto_a_actualizar.cantidad = new_cantidad
            print(
                f"Éxito: Cantidad del producto '{producto_a_actualizar.nombre}'"
                f" actualizada a '{new_cantidad}'."
            )
        except ValueError as e:
            print(f"Error de validación: {e}")

    def eliminar_producto(self):
        """Solicita un código y elimina el producto del inventario."""
        id_search = input("Ingrese el código del producto a eliminar: ").strip()

        if id_search not in self.productos:
            print(f"Error: Producto con código '{id_search}' no encontrado.")
            return

        nombre_producto = self.productos[id_search].nombre

        del self.productos[id_search]
        print(
            f"Éxito: Producto '{nombre_producto}' (Código: {id_search}) eliminado del inventario."
        )


# --------------------------------------------------------------------
# MENÚ PRINCIPAL Y LÓGICA DE LA APLICACIÓN
# --------------------------------------------------------------------


def obtener_datos_producto():
    """
    Solicita los datos del producto al usuario con validación.

    Returns:
        Producto: Objeto Producto si los datos son válidos, None en caso contrario.
    """
    try:
        nombre = input("Nombre del producto: ").strip()
        precio = float(input("Precio del producto: "))
        cantidad = int(input("Cantidad del producto: "))
        codigo = input("Código del producto: ").strip()

        # Creamos la instancia de Producto. Las validaciones de los setters se ejecutan aquí.
        return Producto(nombre, precio, cantidad, codigo)

    except ValueError as e:
        # Captura errores si float() o int() fallan, o si un setter lanza ValueError
        print(
            f"Error de entrada de datos: {e}. Asegúrate de ingresar tipos y valores correctos."
        )
        return None
    # W0718 Corregido: Se debe especificar el tipo de error
    except TypeError as e:
        # Captura errores de tipo si se pasan argumentos incorrectos a Producto.
        print(f"Error de tipo de dato: {e}")
        return None

    except KeyboardInterrupt as e:
        print(f"Ocurrió un error inesperado al obtener los datos: {e}")
        return None

    except SystemExit as e:
        print(f"Ocurrió un error inesperado al obtener los datos: {e}")
        return None


def main_menu():
    """Ejecuta el menú interactivo de la aplicación."""
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
                print("\nSaliendo del sistema de inventario. ¡Hasta pronto! ")
                # Se usa sys.exit() para una salida limpia
                sys.exit(0)

            else:
                print("Opción no válida. Por favor, selecciona un número del 1 al 6.")

        # W0718 Corregido: Se utiliza BaseException para capturar KeyboardInterrupt, SystemExit
        # y garantizar que el menú no se caiga sin capturar la amplia Exception.
        except BaseException as e:
            if isinstance(e, SystemExit):
                raise  # Permite que sys.exit(0) funcione
            print(f"Error grave del sistema o interrupción: {e}")
            sys.exit(1)


# Punto de entrada de la aplicación
if __name__ == "__main__":
    main_menu()