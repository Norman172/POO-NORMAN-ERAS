# Ejemplo de una escuela usando POO
# Este código es para aprender cómo funcionan las clases y objetos en Python

class Estudiante:
    # Esta clase representa a un estudiante
    def __init__(self, nombre, grado):
        self.nombre = nombre  # Guardamos el nombre del estudiante
        self.grado = grado    # Guardamos el grado del estudiante

class Profesor:
    # Esta clase representa a un profesor
    def __init__(self, nombre, materia):
        self.nombre = nombre    # Guardamos el nombre del profesor
        self.materia = materia  # Guardamos la materia que enseña

class Escuela:
    # Esta clase representa la escuela
    def __init__(self):
        self.estudiantes = []  # Lista de estudiantes
        self.profesores = []   # Lista de profesores

    def agregar_estudiante(self, estudiante):
        # Agrega un estudiante a la escuela
        self.estudiantes.append(estudiante)
        print(f"Estudiante {estudiante.nombre} agregado al grado {estudiante.grado}.")

    def agregar_profesor(self, profesor):
        # Agrega un profesor a la escuela
        self.profesores.append(profesor)
        print(f"Profesor {profesor.nombre} agregado para la materia {profesor.materia}.")

    def mostrar_estudiantes(self):
        # Muestra todos los estudiantes
        print("Lista de estudiantes:")
        for estudiante in self.estudiantes:
            print(f"- {estudiante.nombre}, Grado: {estudiante.grado}")

    def mostrar_profesores(self):
        # Muestra todos los profesores
        print("Lista de profesores:")
        for profesor in self.profesores:
            print(f"- {profesor.nombre}, Materia: {profesor.materia}")

# Ejemplo de uso
escuela = Escuela()
est1 = Estudiante("Pedro", "5to")
est2 = Estudiante("Lucía", "6to")
prof1 = Profesor("Carlos", "Matemáticas")
prof2 = Profesor("Juan", "Programación")
escuela.agregar_estudiante(est1)
escuela.agregar_estudiante(est2)
escuela.agregar_profesor(prof1)
escuela.agregar_profesor(prof2)
escuela.mostrar_estudiantes()
escuela.mostrar_profesores()
