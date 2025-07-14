class Archivo:
    def __init__(self, nombre_archivo):
        # Constructor: inicializa el atributo y abre el archivo
        self.nombre = nombre_archivo
        self.archivo = open(nombre_archivo, 'w')  # Simulamos una tarea con recurso
        print(f"[__init__] Archivo '{self.nombre}' abierto para escritura.")

    def escribir(self, texto):
        # Método para escribir en el archivo
        self.archivo.write(texto)
        print(f"[escribir] Se escribió en el archivo: {texto}")

    def __del__(self):
        # Destructor: cierra el archivo
        print(f"[__del__] Cerrando archivo '{self.nombre}'...")
        try:
            self.archivo.close()
            print(f"[__del__] Archivo '{self.nombre}' cerrado correctamente.")
        except AttributeError:
            print(f"[__del__] El archivo ya fue cerrado o no existe.")

# -------------------------------
# Uso del programa
# -------------------------------

# Creamos una instancia de la clase Archivo
archivo1 = Archivo("ejemplo.txt")
archivo1.escribir("Hola desde Python con __init__ y __del__.\n")

# Cuando termine el programa o se elimine el objeto, se llamará automáticamente a __del__
del archivo1  # Esto forzará la llamada al destructor en este momento
