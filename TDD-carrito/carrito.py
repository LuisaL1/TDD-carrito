class Producto:

    def __init__(self, nombre, cantidad, precio):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio


class Carrito:

    def __init__(self):
        self.productos = []

    def agregar_producto(self, producto):
        self.productos.append(producto)

    def eliminar_producto(self, nombre_producto):

        producto_encontrado = any(
            producto.nombre == nombre_producto
            for producto in self.productos
        )

        if producto_encontrado:

            self.productos = [
                producto for producto in self.productos
                if producto.nombre != nombre_producto
            ]

            return "Producto eliminado correctamente"

        return "Producto no encontrado"

    def calcular_total(self):

        return sum(
            producto.cantidad * producto.precio
            for producto in self.productos
        )