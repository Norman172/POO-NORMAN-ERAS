# Ejemplo de una tienda usando POO
# Este código es para aprender cómo funcionan las clases y objetos en Python

class Producto:
    # Esta clase representa un producto que se vende en la tienda
    def __init__(self, nombre, precio):
        self.nombre = nombre  # Guardamos el nombre del producto
        self.precio = precio  # Guardamos el precio del producto

class Carrito:
    # Esta clase representa el carrito de compras de un cliente
    def __init__(self):
        self.productos = []  # Aquí guardamos los productos que el cliente quiere comprar

    def agregar_producto(self, producto):
        # Este método sirve para agregar un producto al carrito
        self.productos.append(producto)
        print(f"Producto {producto.nombre} agregado al carrito.")

    def mostrar_carrito(self):
        # Este método muestra los productos en el carrito
        print("Productos en el carrito:")
        for producto in self.productos:
            print(f"- {producto.nombre}: ${producto.precio}")

    def calcular_total(self):
        # Este método suma los precios de todos los productos
        total = sum([producto.precio for producto in self.productos])
        print(f"Total a pagar: ${total}")
        return total

# Ejemplo de uso
producto1 = Producto("Cuaderno", 2.5)
producto2 = Producto("Lápiz", 0.5)
carrito = Carrito()
carrito.agregar_producto(producto1)
carrito.agregar_producto(producto2)
carrito.mostrar_carrito()
carrito.calcular_total()
