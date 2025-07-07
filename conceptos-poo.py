# Clase base: Animal
class Animal:
    def __init__(self, nombre, especie):
        self.__nombre = nombre            # Encapsulación (atributo privado)
        self.__especie = especie          # Encapsulación (atributo privado)

    def hacer_sonido(self):
        return "Hace un sonido genérico."

    def get_nombre(self):
        return self.__nombre              # Método público para acceder a un atributo privado

    def get_especie(self):
        return self.__especie

    def describir(self):
        return f"{self.get_nombre()} es un(a) {self.get_especie()}."

# Clase derivada: Perro
class Perro(Animal):
    def __init__(self, nombre, raza):
        super().__init__(nombre, "Perro")  # Llama al constructor de la clase base
        self.raza = raza                   # Atributo adicional

    # Polimorfismo: sobrescribe el método de la clase base
    def hacer_sonido(self):
        return "¡Guau!"

    def describir(self):
        base_descripcion = super().describir()
        return f"{base_descripcion} Es de raza {self.raza}."

# Otra clase derivada: Gato
class Gato(Animal):
    def __init__(self, nombre, color):
        super().__init__(nombre, "Gato")
        self.color = color

    # Otro ejemplo de polimorfismo
    def hacer_sonido(self):
        return "¡Miau!"

    def describir(self):
        base_descripcion = super().describir()
        return f"{base_descripcion} Tiene un pelaje color {self.color}."

# Función polimórfica
def hacer_que_suene(animal):
    print(f"{animal.get_nombre()} dice: {animal.hacer_sonido()}")

# Crear instancias
perro1 = Perro("Rex", "Pastor Alemán")
gato1 = Gato("Misu", "Negro")

# Mostrar funcionalidad
print(perro1.describir())
print(gato1.describir())

hacer_que_suene(perro1)
hacer_que_suene(gato1)
