'''
Diseña una solución utilizando el paradigma de POO.
Crea una clase que represente la información diaria del clima.
Utiliza métodos de la clase para ingresar datos y calcular el promedio semanal.
Asegúrate de aplicar conceptos como encapsulamiento, herencia o polimorfismo según sea apropiado.
'''
#definir el objeto Clima que contendrá la información de la semana y las temperaturas
#en python se define un objeto como una clase
class Clima:
    #definir el constructor de la clase Clima que contendrá los atribtos de la misma
    def __init__(self, semana):
        self.semana = semana
        self.temperaturas = []
        self.dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    #método para ingresar las temperaturas de cada día de la semana
    def ingresar_temperaturas(self):
        for dia in self.dias_semana:
            temperatura = float(input(f"Ingrese la temperatura del {dia}: "))
            self.temperaturas.append(temperatura)
    #método para calcular el promedio de las temperaturas ingresadas
    def calcular_promedio(self):
        if len(self.temperaturas) == 0:
            return 0
        return sum(self.temperaturas) / len(self.temperaturas)
    #método para mostrar el promedio de temperatura de la semana ingresada
    def mostrar_promedio(self):
        promedio = self.calcular_promedio()
        print(f"El promedio de temperatura de la semana {self.semana} es: {promedio}°C")

# Función principal para ejecutar el programa
def main():
    # Ingreso de la semana que se desea calcular el promedio de temperatura
    semana = input("Ingrese la semana que desea calcular el promedio de temperatura: ")
    # Creación de una instancia de la clase Clima que la llamaré clima
    clima = Clima(semana)
    #llamo al método para ingresar las temperaturas de cada día de la semana
    clima.ingresar_temperaturas()
    #llamo al método para calcular y mostrar el promedio de temperatura de la semana ingresada
    clima.mostrar_promedio()
main()  # Llamada a la función principal para iniciar el programa