# Ejemplo de mascotas usando POO
# Este código es para aprender cómo funcionan las clases y objetos en Python

class Mascota:
    # Esta clase representa una mascota
    def __init__(self, nombre, tipo):
        self.nombre = nombre  # Guardamos el nombre de la mascota
        self.tipo = tipo      # Guardamos el tipo de mascota (perro, gato, etc.)

    def hacer_sonido(self):
        # Este método hace que la mascota haga un sonido
        if self.tipo == "perro":
            print(f"{self.nombre} dice: ¡Guau!")
        elif self.tipo == "gato":
            print(f"{self.nombre} dice: ¡Miau!")
        else:
            print(f"{self.nombre} hace un sonido desconocido.")

# Ejemplo de uso
mascota1 = Mascota("Firulais", "perro")
mascota2 = Mascota("Pantera", "gato")
mascota1.hacer_sonido()
mascota2.hacer_sonido()
