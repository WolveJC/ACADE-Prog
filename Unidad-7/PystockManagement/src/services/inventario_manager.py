class Inventario:
    def __init__(self):
        self.productos = {}  # Diccionario: clave=código (str), valor=objeto Producto

    def agg_prod(self, producto):
        if not isinstance(producto, Producto):
            print("Error: Solo se pueden agregar objetos de tipo 'Producto' al inventario.")
            return

        if producto.codigo in self.productos:
            print(f"Error: El producto con código '{producto.codigo}' ya existe en el inventario.")
            return

        self.productos[producto.codigo] = producto
        print(f" Éxito: Producto '{producto.nombre}' (Código: {producto.codigo}) agregado.")

    def imprimir(self):
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
        id_search = input("Ingrese el código del producto a buscar: ").strip()

        if id_search in self.productos:
            # Acceso directo al objeto Producto por su código
            resultado_producto = self.productos[id_search]
            print("\n ¡Producto Encontrado!")
            print(resultado_producto)
            print("--------------------------\n")
        else:
            print(f" Error: El producto con el código {id_search} no se encuentra en el inventario.")

    def actualizar_cantidad(self):
        id_search = input("Ingrese el código del producto a actualizar: ").strip()

        if id_search not in self.productos:
            print(f" Error: Producto con código '{id_search}' no encontrado.")
            return

        producto_a_actualizar = self.productos[id_search]
        
        # Lógica de validación de entrada
        while True:
            try:
                # Muestra el nombre del producto que se está actualizando
                new_cantidad_str = input(f"Ingrese la nueva cantidad para '{producto_a_actualizar.nombre}' (actual: {producto_a_actualizar.cantidad}): ").strip()
                new_cantidad = int(new_cantidad_str)

                # La validación de new_cantidad < 0 ya la tienes en el setter, pero es buena práctica
                # validar antes de la asignación para mejorar el feedback al usuario.
                if new_cantidad < 0:
                    print(" Error: La cantidad no puede ser un número negativo. Inténtalo de nuevo.")
                    continue
                
                break

            except ValueError:
                print(" Error de Valor: Se espera una cantidad numérica entera.")
            except Exception as e:
                print(f"Ocurrió un error inesperado al leer la nueva cantidad: {e}")

        # Asigna la nueva cantidad (llamando al setter de Producto)
        producto_a_actualizar.cantidad = new_cantidad
        print(f" Éxito: Cantidad del producto '{producto_a_actualizar.nombre}' actualizada a {new_cantidad}.")

    def eliminar_producto(self):
        id_search = input("Ingrese el código del producto a eliminar: ").strip()

        if id_search not in self.productos:
            print(f" Error: Producto con código '{id_search}' no encontrado.")
            return

        # Opcional: Mostrar nombre antes de eliminar
        nombre_producto = self.productos[id_search].nombre
        
        del self.productos[id_search]  # Elimina la referencia del diccionario
        print(f" Éxito: Producto '{nombre_producto}' (Código: {id_search}) eliminado del inventario.")
