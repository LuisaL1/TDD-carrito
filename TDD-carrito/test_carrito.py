import unittest
from carrito import Carrito, Producto


class TestCarrito(unittest.TestCase):

    def setUp(self):
        self.carrito = Carrito()

        producto1 = Producto("Mouse", 2, 30000)
        producto2 = Producto("Teclado", 1, 50000)

        self.carrito.agregar_producto(producto1)
        self.carrito.agregar_producto(producto2)

    def test_agregar_producto(self):
        """Verifica que se puede agregar un producto y queda en el carrito."""
        monitor = Producto("Monitor", 1, 200000)
        self.carrito.agregar_producto(monitor)
        nombres = [p.nombre for p in self.carrito.productos]
        self.assertIn("Monitor", nombres)

    def test_eliminar_producto(self):
        """Verifica que eliminar un producto existente retorna el mensaje correcto."""
        resultado = self.carrito.eliminar_producto("Mouse")
        self.assertEqual(resultado, "Producto eliminado correctamente")

    def test_eliminar_producto_inexistente(self):
        """Verifica que eliminar un producto que no existe retorna el mensaje adecuado."""
        resultado = self.carrito.eliminar_producto("Audifono")
        self.assertEqual(resultado, "Producto no encontrado")

    def test_calcular_total(self):
        """Verifica que el total se calcula correctamente: (2*30000) + (1*50000) = 110000."""
        total = self.carrito.calcular_total()
        self.assertEqual(total, 110000)

    def test_calcular_total_carrito_vacio(self):
        """Verifica que el total de un carrito vacio es 0."""
        carrito_vacio = Carrito()
        self.assertEqual(carrito_vacio.calcular_total(), 0)


if __name__ == "__main__":
    unittest.main()