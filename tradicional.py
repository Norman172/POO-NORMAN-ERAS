'''
Implementa una solución utilizando estructuras de funciones.
Define funciones para la entrada de datos diarios (temperaturas) y el cálculo del promedio semanal.
Organiza el código de manera lógica y funcional utilizando la programación tradicional.
'''
#definición de la variable semana como string
semana=""
#definición del array que contendrá las temperaturas por día
temperaturas = []
#definición del array que contiene los días de la semana para luego iterar sobre ellos
dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
#ingreso por teclado de la semana que se desea calcular el promedio de temperatura
semana=input("ingrese la semana que desea calcular el promedio de temperatura: ")
#ingreso por teclado de las temperaturas de cada día de la semana
for dia in dias_semana:
    temperatura = float(input(f"Ingrese la temperatura del {dia}: "))
    temperaturas.append(temperatura)
#función para calcular el promedio de las temperaturas ingresadas y realizar validaciones
def calcular_promedio(temperaturas):
    if len(temperaturas) == 0:
        #salir del programa si no se ingresaron temperaturas
        return 0
    #retornar l valor promedio de las temperaturas ingresadas
    return sum(temperaturas) / len(temperaturas)
# Imprimir el promedio de temperatura de la semana ingresada    
print(f"El promedio de temperatura de la semana {semana} es: {calcular_promedio(temperaturas)}°C")

