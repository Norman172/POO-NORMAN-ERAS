# Ejemplo de un sistema de reservas usando POO
# Este código es para aprender cómo funcionan las clases y objetos en Python

class Cliente:
    # Esta clase representa a un cliente que quiere hacer una reserva
    def __init__(self, nombre):
        self.nombre = nombre  # Guardamos el nombre del cliente

class Reserva:
    # Esta clase representa una reserva hecha por un cliente
    def __init__(self, cliente, fecha):
        self.cliente = cliente  # Aquí guardamos el objeto cliente
        self.fecha = fecha      # Aquí guardamos la fecha de la reserva

class SistemaReservas:
    # Esta clase es el sistema que maneja todas las reservas
    def __init__(self):
        self.reservas = []  # Aquí guardamos todas las reservas en una lista

    def hacer_reserva(self, cliente, fecha):
        # Este método sirve para crear una nueva reserva
        reserva = Reserva(cliente, fecha)
        self.reservas.append(reserva)  # Agregamos la reserva a la lista
        print(f"Reserva hecha para {cliente.nombre} el {fecha}")

    def mostrar_reservas(self):
        # Este método muestra todas las reservas
        print("Reservas actuales:")
        for reserva in self.reservas:
            print(f"Cliente: {reserva.cliente.nombre}, Fecha: {reserva.fecha}")

# Ejemplo de uso
sistema = SistemaReservas()
cliente1 = Cliente("Norman")
cliente2 = Cliente("Luis")
sistema.hacer_reserva(cliente1, "2025-07-01")
sistema.hacer_reserva(cliente2, "2025-07-02")
sistema.mostrar_reservas()
