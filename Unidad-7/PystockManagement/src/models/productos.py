class Producto:
    def __init__(self, nombre, precio, cantidad, codigo):
        # Al asignar a self.atributo, se llama automáticamente al setter
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.codigo = codigo

    def __del__(self):
        # Método para demostrar la eliminación de la referencia
        # (no garantizado que se ejecute al instante)
        print(f"Objeto {self.codigo} - {self.nombre} eliminado")

    def __str__(self):
        # Representación legible del objeto
        return f"Código: {self.codigo}\n  Producto: {self.nombre}\n  Precio: ${self.precio:.2f}\n  Cantidad: {self.cantidad}"

    # Métodos dunder de comparación
    def __lt__(self, otro):
        if not isinstance(otro, Producto):
            return NotImplemented
        return self.precio < otro.precio  # Compara por precio

    def __eq__(self, otro):
        if not isinstance(otro, Producto):
            return NotImplemented
        return self.codigo == otro.codigo  # Compara por unicidad del código

    # --- Propiedades (Getters y Setters con validación) ---
    # Usamos __ para los atributos internos para indicar que son privados

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, nombre):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError(
                "El nombre del producto debe ser una cadena no vacía.")
        self.__nombre = nombre

    @property
    def precio(self):
        return self.__precio

    @precio.setter
    def precio(self, precio):
        if not isinstance(precio, (int, float)) or precio <= 0:
            raise ValueError(
                "El precio debe ser un número positivo mayor que cero.")
        self.__precio = precio

    @property
    def cantidad(self):
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, cantidad):
        if not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError(
                "La cantidad debe ser un número entero no negativo.")
        self.__cantidad = cantidad

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ValueError(
                "El código del producto debe ser una cadena no vacía.")
        self.__codigo = codigo
