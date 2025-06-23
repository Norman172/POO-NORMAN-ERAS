# Ejemplo de una biblioteca usando POO
# Este código es para aprender cómo funcionan las clases y objetos en Python

class Libro:
    # Esta clase representa un libro en la biblioteca
    def __init__(self, titulo, autor):
        self.titulo = titulo  # Guardamos el título del libro
        self.autor = autor    # Guardamos el autor del libro
        self.prestado = False # Indica si el libro está prestado

class Usuario:
    # Esta clase representa a un usuario de la biblioteca
    def __init__(self, nombre):
        self.nombre = nombre  # Guardamos el nombre del usuario

class Biblioteca:
    # Esta clase representa la biblioteca
    def __init__(self):
        self.libros = []  # Lista de libros en la biblioteca

    def agregar_libro(self, libro):
        # Agrega un libro a la biblioteca
        self.libros.append(libro)
        print(f"Libro '{libro.titulo}' agregado a la biblioteca.")

    def prestar_libro(self, libro, usuario):
        # Presta un libro a un usuario si está disponible
        if libro in self.libros and not libro.prestado:
            libro.prestado = True
            print(f"El libro '{libro.titulo}' fue prestado a {usuario.nombre}.")
        else:
            print(f"El libro '{libro.titulo}' no está disponible.")

    def mostrar_libros(self):
        # Muestra todos los libros y su estado
        print("Libros en la biblioteca:")
        for libro in self.libros:
            estado = "Prestado" if libro.prestado else "Disponible"
            print(f"- {libro.titulo} de {libro.autor} ({estado})")

# Ejemplo de uso
biblioteca = Biblioteca()
libro1 = Libro("Análisis vectorial 2", "Fedrick Mancelli")
libro2 = Libro("Cien Años de Soledad", "Gabriel García Márquez")
usuario1 = Usuario("Carlos")
biblioteca.agregar_libro(libro1)
biblioteca.agregar_libro(libro2)
biblioteca.prestar_libro(libro1, usuario1)
biblioteca.mostrar_libros()
