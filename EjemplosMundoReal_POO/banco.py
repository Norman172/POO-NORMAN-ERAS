# Ejemplo de un banco usando POO
# Este código es para aprender cómo funcionan las clases y objetos en Python

class CuentaBancaria:
    # Esta clase representa una cuenta bancaria
    def __init__(self, titular, saldo=0):
        self.titular = titular  # Guardamos el nombre del titular
        self.saldo = saldo      # Guardamos el saldo de la cuenta

    def depositar(self, cantidad):
        # Este método sirve para depositar dinero
        self.saldo += cantidad
        print(f"Depósito de ${cantidad} realizado. Nuevo saldo: ${self.saldo}")

    def retirar(self, cantidad):
        # Este método sirve para retirar dinero si hay suficiente saldo
        if cantidad <= self.saldo:
            self.saldo -= cantidad
            print(f"Retiro de ${cantidad} realizado. Nuevo saldo: ${self.saldo}")
        else:
            print("No hay suficiente saldo para retirar.")

    def mostrar_saldo(self):
        # Muestra el saldo actual
        print(f"Saldo actual de {self.titular}: ${self.saldo}")

# Ejemplo de uso
cuenta = CuentaBancaria("María", 100)
cuenta.depositar(50)
cuenta.retirar(30)
cuenta.mostrar_saldo()
