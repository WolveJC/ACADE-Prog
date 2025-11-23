"""
Módulo Producto.

Define el modelo de datos fundamental 'Producto', que encapsula los
atributos de un artículo de inventario y aplica validaciones estrictas
mediante el uso de propiedades (getters y setters).
"""


class Producto:
    """
    Representa un producto con sus atributos de nombre, precio, cantidad y código.

    Utiliza propiedades (getters/setters) para encapsular y validar los datos.

    Attributes:
        nombre (str): Nombre descriptivo del producto.
        precio (float): Precio unitario (debe ser > 0).
        cantidad (int): Cantidad en inventario (debe ser >= 0).
        codigo (str): Identificador único del producto.
    """

    def __init__(self, nombre, precio, cantidad, codigo):
        """
        Inicializa una nueva instancia de Producto.

        Al asignar a self.atributo, se llama automáticamente al setter para la validación inicial.

        Args:
            nombre: Nombre del producto.
            precio: Precio del producto.
            cantidad: Cantidad en inventario.
            codigo: Identificador único del producto.
        """
        # Al asignar a self.atributo, se llama automáticamente al setter
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.codigo = codigo

    def __del__(self):
        """Método de finalización que se llama cuando el objeto es destruido (garbage collection)."""
        # Método para demostrar la eliminación de la referencia
        # (no garantizado que se ejecute al instante)
        print(f"Objeto {self.codigo} - {self.nombre} eliminado")

    def __str__(self):
        """Representación legible del objeto para impresión (dunder method)."""
        # Representación legible del objeto
        return (
            f"Código: {self.codigo}\n  Producto: {self.nombre}\n  "
            f"Precio: ${self.precio:.2f}\n  Cantidad: {self.cantidad}"
        )

    # Métodos dunder de comparación
    def __lt__(self, otro):
        """Define la comparación 'menor que' (<) basada en el precio."""
        if not isinstance(otro, Producto):
            return NotImplemented
        return self.precio < otro.precio  # Compara por precio

    def __eq__(self, otro):
        """Define la comparación 'igual a' (==) basada en la unicidad del código."""
        if not isinstance(otro, Producto):
            return NotImplemented
        return self.codigo == otro.codigo  # Compara por unicidad del código

    # --- Propiedades (Getters y Setters con validación) ---
    # Usamos __ para los atributos internos para indicar que son privados

    @property
    def nombre(self):
        """Obtiene el nombre del producto."""
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        """Establece el nombre del producto, validando que sea una cadena no vacía."""
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del producto debe ser una cadena no vacía.")
        self.__nombre = nombre

    @property
    def precio(self):
        """Obtiene el precio del producto."""
        return self.__precio

    @precio.setter
    def precio(self, precio):
        """Establece el precio del producto, validando que sea un número positivo."""
        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError("El precio debe ser un número positivo mayor que cero.")
        self.__precio = precio

    @property
    def cantidad(self):
        """Obtiene la cantidad en inventario."""
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, cantidad):
        """Establece la cantidad, validando que sea un número entero no negativo."""
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("La cantidad debe ser un número entero no negativo.")
        self.__cantidad = cantidad

    @property
    def codigo(self):
        """Obtiene el código del producto."""
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        """Establece el código, validando que sea una cadena no vacía."""
        if not isinstance(codigo, str) or not codigo.strip():
            # Error de código original: Cierre de comillas incorrecto. Corregido.
            raise ValueError("El código del producto debe ser una cadena no vacía.")
        self.__codigo = codigo
