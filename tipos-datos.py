# Programa para calcular el área de un triángulo
# Autor: [Norman Eras]
# Fecha: 20/06/2025
# Este programa solicita al usuario la base y la altura de un triángulo,
# luego calcula y muestra el área usando la fórmula: (base * altura) / 2.

def calcular_area_triangulo(base: float, altura: float) -> float:
    """
    Calcula el área de un triángulo dados su base y altura.
    :param base: Base del triángulo (float)
    :param altura: Altura del triángulo (float)
    :return: Área del triángulo (float)
    """
    area = (base * altura) / 2
    return area


# Entrada de datos
print("CÁLCULO DEL ÁREA DE UN TRIÁNGULO")
nombre_usuario: str = input("Ingrese su nombre: ")
base_str: str = input("Ingrese la base del triángulo en cm: ")
altura_str: str = input("Ingrese la altura del triángulo en cm: ")

# Conversión de tipos de datos
base: float = float(base_str)
altura: float = float(altura_str)

# Procesamiento
area_resultado: float = calcular_area_triangulo(base, altura)

# Salida
print(f"\nHola {nombre_usuario}, el área del triángulo es {area_resultado:.2f} cm².")

# Validación (uso de tipo booleano)
es_area_mayor_que_diez: bool = area_resultado > 10
print("¿El área es mayor que 10 cm²?", es_area_mayor_que_diez)
