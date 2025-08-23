# gestion-inventarios-mejorado.py
"""
Sistema de Gestión de Inventarios Mejorado
Versión avanzada con manejo de archivos y excepciones

Autor: Norman Eras
Fecha: Agosto 2025

Características:
- Almacenamiento persistente en archivos
- Manejo robusto de excepciones
- Carga automática de inventario al inicio
- Notificaciones de estado de operaciones
"""

import os
import json
from datetime import datetime


class Producto:
    """Clase que representa un producto en el inventario"""
    
    def __init__(self, id_producto, nombre, cantidad, precio):
        """
        Inicializa un producto con sus atributos básicos
        
        Args:
            id_producto (str): Identificador único del producto
            nombre (str): Nombre del producto
            cantidad (int): Cantidad disponible en inventario
            precio (float): Precio unitario del producto
        """
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
        self._fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Getters
    def get_id(self):
        """Retorna el ID del producto"""
        return self._id

    def get_nombre(self):
        """Retorna el nombre del producto"""
        return self._nombre

    def get_cantidad(self):
        """Retorna la cantidad del producto"""
        return self._cantidad

    def get_precio(self):
        """Retorna el precio del producto"""
        return self._precio
    
    def get_fecha_creacion(self):
        """Retorna la fecha de creación del producto"""
        return self._fecha_creacion

    # Setters
    def set_nombre(self, nombre):
        """Establece el nombre del producto"""
        if nombre.strip():
            self._nombre = nombre.strip()
        else:
            raise ValueError("El nombre del producto no puede estar vacío")

    def set_cantidad(self, cantidad):
        """Establece la cantidad del producto"""
        if cantidad >= 0:
            self._cantidad = cantidad
        else:
            raise ValueError("La cantidad no puede ser negativa")

    def set_precio(self, precio):
        """Establece el precio del producto"""
        if precio > 0:
            self._precio = precio
        else:
            raise ValueError("El precio debe ser mayor que cero")

    def to_dict(self):
        """Convierte el producto a diccionario para almacenamiento"""
        return {
            'id': self._id,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': self._precio,
            'fecha_creacion': self._fecha_creacion
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un producto desde un diccionario"""
        producto = cls(data['id'], data['nombre'], data['cantidad'], data['precio'])
        producto._fecha_creacion = data.get('fecha_creacion', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return producto

    def __str__(self):
        return f"ID: {self._id}, Nombre: {self._nombre}, Cantidad: {self._cantidad}, Precio: ${self._precio:.2f}"


class InventarioException(Exception):
    """Excepción personalizada para errores del inventario"""
    pass


class Inventario:
    """Clase que gestiona la colección de productos con persistencia en archivos"""
    
    def __init__(self, archivo_inventario='inventario.json'):
        """
        Inicializa el inventario
        
        Args:
            archivo_inventario (str): Nombre del archivo donde se almacena el inventario
        """
        self.productos = []
        self.archivo_inventario = archivo_inventario
        self.backup_dir = 'backups'
        self._crear_directorio_backup()
        self.cargar_inventario()

    def _crear_directorio_backup(self):
        """Crea el directorio de respaldo si no existe"""
        try:
            if not os.path.exists(self.backup_dir):
                os.makedirs(self.backup_dir)
        except OSError as e:
            print(f"Advertencia: No se pudo crear el directorio de backup: {e}")

    def _crear_backup(self):
        """Crea un respaldo del inventario actual"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"inventario_backup_{timestamp}.json")
            
            if os.path.exists(self.archivo_inventario):
                with open(self.archivo_inventario, 'r', encoding='utf-8') as origen:
                    with open(backup_file, 'w', encoding='utf-8') as destino:
                        destino.write(origen.read())
                print(f"✓ Backup creado: {backup_file}")
        except Exception as e:
            print(f"Advertencia: No se pudo crear backup: {e}")

    def cargar_inventario(self):
        """Carga el inventario desde el archivo"""
        try:
            if os.path.exists(self.archivo_inventario):
                with open(self.archivo_inventario, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read().strip()
                    if contenido:  # Verificar que el archivo no esté vacío
                        datos = json.loads(contenido)
                        self.productos = [Producto.from_dict(item) for item in datos]
                        print(f"✓ Inventario cargado exitosamente. {len(self.productos)} productos encontrados.")
                    else:
                        print("✓ Archivo de inventario vacío. Iniciando con inventario nuevo.")
            else:
                print("✓ No se encontró archivo de inventario. Iniciando con inventario nuevo.")
                self._crear_archivo_vacio()
                
        except FileNotFoundError:
            print("✓ No se encontró archivo de inventario. Iniciando con inventario nuevo.")
            self._crear_archivo_vacio()
            
        except json.JSONDecodeError as e:
            print(f"✗ Error: El archivo de inventario está corrupto: {e}")
            print("¿Desea crear un nuevo archivo de inventario? (s/n): ", end="")
            respuesta = input().lower().strip()
            if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
                self._crear_backup()  # Respaldar archivo corrupto
                self._crear_archivo_vacio()
                print("✓ Nuevo archivo de inventario creado.")
            else:
                raise InventarioException("No se puede continuar sin un archivo de inventario válido.")
                
        except PermissionError:
            raise InventarioException(f"✗ Error: Sin permisos para leer el archivo {self.archivo_inventario}")
            
        except Exception as e:
            raise InventarioException(f"✗ Error inesperado al cargar inventario: {e}")

    def _crear_archivo_vacio(self):
        """Crea un archivo de inventario vacío"""
        try:
            with open(self.archivo_inventario, 'w', encoding='utf-8') as archivo:
                json.dump([], archivo, indent=2, ensure_ascii=False)
        except PermissionError:
            raise InventarioException(f"✗ Error: Sin permisos para crear el archivo {self.archivo_inventario}")
        except Exception as e:
            raise InventarioException(f"✗ Error al crear archivo de inventario: {e}")

    def guardar_inventario(self):
        """Guarda el inventario actual en el archivo"""
        try:
            # Crear backup antes de guardar
            self._crear_backup()
            
            datos = [producto.to_dict() for producto in self.productos]
            
            # Escritura atómica: escribir a archivo temporal primero
            archivo_temp = self.archivo_inventario + '.tmp'
            with open(archivo_temp, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
            
            # Reemplazar archivo original con el temporal
            os.replace(archivo_temp, self.archivo_inventario)
            print("✓ Inventario guardado exitosamente.")
            return True
            
        except PermissionError:
            print(f"✗ Error: Sin permisos para escribir en el archivo {self.archivo_inventario}")
            return False
            
        except OSError as e:
            print(f"✗ Error del sistema al guardar inventario: {e}")
            return False
            
        except Exception as e:
            print(f"✗ Error inesperado al guardar inventario: {e}")
            return False

    def agregar_producto(self, producto):
        """
        Añade un producto al inventario
        
        Args:
            producto (Producto): Producto a añadir
            
        Returns:
            bool: True si se añadió exitosamente, False en caso contrario
        """
        try:
            # Verificar que el ID sea único
            if any(p.get_id() == producto.get_id() for p in self.productos):
                print(f"✗ Error: El ID '{producto.get_id()}' ya existe en el inventario.")
                return False
            
            # Validar datos del producto
            if not producto.get_nombre().strip():
                print("✗ Error: El nombre del producto no puede estar vacío.")
                return False
            
            if producto.get_cantidad() < 0:
                print("✗ Error: La cantidad no puede ser negativa.")
                return False
            
            if producto.get_precio() <= 0:
                print("✗ Error: El precio debe ser mayor que cero.")
                return False
            
            # Añadir producto y guardar
            self.productos.append(producto)
            if self.guardar_inventario():
                print(f"✓ Producto '{producto.get_nombre()}' añadido correctamente al inventario.")
                return True
            else:
                # Si falla el guardado, remover el producto de la lista
                self.productos.remove(producto)
                print("✗ Error: No se pudo guardar el producto en el archivo.")
                return False
                
        except Exception as e:
            print(f"✗ Error inesperado al añadir producto: {e}")
            return False

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto del inventario por ID
        
        Args:
            id_producto (str): ID del producto a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            producto_eliminado = None
            for producto in self.productos:
                if producto.get_id() == id_producto:
                    producto_eliminado = producto
                    self.productos.remove(producto)
                    break
            
            if producto_eliminado:
                if self.guardar_inventario():
                    print(f"✓ Producto '{producto_eliminado.get_nombre()}' eliminado correctamente.")
                    return True
                else:
                    # Si falla el guardado, restaurar el producto
                    self.productos.append(producto_eliminado)
                    print("✗ Error: No se pudo eliminar el producto del archivo.")
                    return False
            else:
                print(f"✗ Error: No se encontró producto con ID '{id_producto}'.")
                return False
                
        except Exception as e:
            print(f"✗ Error inesperado al eliminar producto: {e}")
            return False

    def actualizar_producto(self, id_producto, nombre=None, cantidad=None, precio=None):
        """
        Actualiza un producto del inventario
        
        Args:
            id_producto (str): ID del producto a actualizar
            nombre (str, optional): Nuevo nombre del producto
            cantidad (int, optional): Nueva cantidad del producto
            precio (float, optional): Nuevo precio del producto
            
        Returns:
            bool: True si se actualizó exitosamente, False en caso contrario
        """
        try:
            for producto in self.productos:
                if producto.get_id() == id_producto:
                    # Guardar valores originales para posible rollback
                    nombre_original = producto.get_nombre()
                    cantidad_original = producto.get_cantidad()
                    precio_original = producto.get_precio()
                    
                    try:
                        # Actualizar campos especificados
                        if nombre is not None:
                            producto.set_nombre(nombre)
                        if cantidad is not None:
                            producto.set_cantidad(cantidad)
                        if precio is not None:
                            producto.set_precio(precio)
                        
                        # Guardar cambios
                        if self.guardar_inventario():
                            cambios = []
                            if nombre is not None:
                                cambios.append(f"nombre: '{nombre}'")
                            if cantidad is not None:
                                cambios.append(f"cantidad: {cantidad}")
                            if precio is not None:
                                cambios.append(f"precio: ${precio:.2f}")
                            
                            print(f"✓ Producto '{producto.get_id()}' actualizado correctamente ({', '.join(cambios)}).")
                            return True
                        else:
                            # Rollback en caso de error al guardar
                            producto.set_nombre(nombre_original)
                            producto.set_cantidad(cantidad_original)
                            producto.set_precio(precio_original)
                            print("✗ Error: No se pudieron guardar los cambios en el archivo.")
                            return False
                            
                    except ValueError as e:
                        print(f"✗ Error de validación: {e}")
                        return False
                    
            print(f"✗ Error: No se encontró producto con ID '{id_producto}'.")
            return False
            
        except Exception as e:
            print(f"✗ Error inesperado al actualizar producto: {e}")
            return False

    def buscar_por_nombre(self, nombre):
        """
        Busca productos por nombre (búsqueda parcial, case-insensitive)
        
        Args:
            nombre (str): Nombre o parte del nombre a buscar
            
        Returns:
            list: Lista de productos encontrados
        """
        try:
            if not nombre.strip():
                return []
            
            resultados = [p for p in self.productos 
                         if nombre.lower().strip() in p.get_nombre().lower()]
            return resultados
            
        except Exception as e:
            print(f"✗ Error al buscar productos: {e}")
            return []

    def buscar_por_id(self, id_producto):
        """
        Busca un producto por su ID exacto
        
        Args:
            id_producto (str): ID del producto a buscar
            
        Returns:
            Producto or None: Producto encontrado o None si no existe
        """
        try:
            for producto in self.productos:
                if producto.get_id() == id_producto:
                    return producto
            return None
            
        except Exception as e:
            print(f"✗ Error al buscar producto por ID: {e}")
            return None

    def obtener_productos_bajo_stock(self, umbral=5):
        """
        Obtiene productos con stock bajo el umbral especificado
        
        Args:
            umbral (int): Cantidad mínima de stock
            
        Returns:
            list: Lista de productos con stock bajo
        """
        try:
            return [p for p in self.productos if p.get_cantidad() <= umbral]
        except Exception as e:
            print(f"✗ Error al obtener productos con stock bajo: {e}")
            return []

    def mostrar_productos(self):
        """Muestra todos los productos del inventario"""
        try:
            if not self.productos:
                print("\n📦 Inventario vacío.")
                return
            
            print(f"\n📦 INVENTARIO ACTUAL ({len(self.productos)} productos):")
            print("-" * 80)
            
            for i, producto in enumerate(self.productos, 1):
                estado_stock = "⚠️ STOCK BAJO" if producto.get_cantidad() <= 5 else "✓ OK"
                print(f"{i:2d}. {producto} [{estado_stock}]")
            
            print("-" * 80)
            
            # Mostrar estadísticas
            valor_total = sum(p.get_precio() * p.get_cantidad() for p in self.productos)
            cantidad_total = sum(p.get_cantidad() for p in self.productos)
            
            print(f"💰 Valor total del inventario: ${valor_total:.2f}")
            print(f"📊 Cantidad total de items: {cantidad_total}")
            
            productos_bajo_stock = self.obtener_productos_bajo_stock()
            if productos_bajo_stock:
                print(f"⚠️  Productos con stock bajo (≤5): {len(productos_bajo_stock)}")
                
        except Exception as e:
            print(f"✗ Error al mostrar productos: {e}")

    def generar_reporte(self):
        """Genera un reporte detallado del inventario"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archivo_reporte = f"reporte_inventario_{timestamp}.txt"
            
            with open(archivo_reporte, 'w', encoding='utf-8') as archivo:
                archivo.write("="*80 + "\n")
                archivo.write("REPORTE DE INVENTARIO\n")
                archivo.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                archivo.write("="*80 + "\n\n")
                
                if self.productos:
                    archivo.write(f"Total de productos: {len(self.productos)}\n\n")
                    
                    for i, producto in enumerate(self.productos, 1):
                        archivo.write(f"{i:2d}. {producto}\n")
                        archivo.write(f"    Fecha de creación: {producto.get_fecha_creacion()}\n\n")
                    
                    # Estadísticas
                    valor_total = sum(p.get_precio() * p.get_cantidad() for p in self.productos)
                    cantidad_total = sum(p.get_cantidad() for p in self.productos)
                    
                    archivo.write("-" * 80 + "\n")
                    archivo.write("ESTADÍSTICAS\n")
                    archivo.write(f"Valor total: ${valor_total:.2f}\n")
                    archivo.write(f"Cantidad total: {cantidad_total}\n")
                    
                    productos_bajo_stock = self.obtener_productos_bajo_stock()
                    if productos_bajo_stock:
                        archivo.write(f"Productos con stock bajo: {len(productos_bajo_stock)}\n")
                        for p in productos_bajo_stock:
                            archivo.write(f"  - {p.get_nombre()} (ID: {p.get_id()}, Stock: {p.get_cantidad()})\n")
                else:
                    archivo.write("Inventario vacío.\n")
            
            print(f"✓ Reporte generado: {archivo_reporte}")
            return True
            
        except Exception as e:
            print(f"✗ Error al generar reporte: {e}")
            return False


def validar_entrada_numerica(mensaje, tipo=int, minimo=None, maximo=None):
    """
    Valida entrada numérica del usuario
    
    Args:
        mensaje (str): Mensaje a mostrar al usuario
        tipo (type): Tipo de dato esperado (int o float)
        minimo (int/float, optional): Valor mínimo permitido
        maximo (int/float, optional): Valor máximo permitido
        
    Returns:
        int/float: Valor validado ingresado por el usuario
    """
    while True:
        try:
            valor = tipo(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"✗ Error: El valor debe ser mayor o igual a {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"✗ Error: El valor debe ser menor o igual a {maximo}")
                continue
            return valor
        except ValueError:
            print(f"✗ Error: Ingrese un valor numérico válido.")
        except KeyboardInterrupt:
            print("\n✗ Operación cancelada por el usuario.")
            return None


def menu_principal():
    """Función principal que maneja el menú interactivo"""
    print("="*80)
    print("SISTEMA DE GESTIÓN DE INVENTARIOS MEJORADO")
    print("Versión 2.0 - Con persistencia en archivos")
    print("="*80)
    
    try:
        inventario = Inventario()
    except InventarioException as e:
        print(f"✗ Error crítico: {e}")
        print("No se puede iniciar el sistema.")
        return
    except Exception as e:
        print(f"✗ Error inesperado al inicializar: {e}")
        return

    while True:
        try:
            print("\n" + "="*50)
            print("MENÚ PRINCIPAL")
            print("="*50)
            print("1. 📝 Añadir producto")
            print("2. 🗑️  Eliminar producto")
            print("3. ✏️  Actualizar producto")
            print("4. 🔍 Buscar producto por nombre")
            print("5. 🔎 Buscar producto por ID")
            print("6. 📦 Mostrar todos los productos")
            print("7. ⚠️  Mostrar productos con stock bajo")
            print("8. 📄 Generar reporte")
            print("9. 🔄 Recargar inventario desde archivo")
            print("0. 🚪 Salir")
            print("="*50)
            
            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                print("\n--- AÑADIR PRODUCTO ---")
                try:
                    id_producto = input("ID único del producto: ").strip()
                    if not id_producto:
                        print("✗ Error: El ID no puede estar vacío.")
                        continue
                    
                    nombre = input("Nombre del producto: ").strip()
                    if not nombre:
                        print("✗ Error: El nombre no puede estar vacío.")
                        continue
                    
                    cantidad = validar_entrada_numerica("Cantidad en stock: ", int, minimo=0)
                    if cantidad is None:
                        continue
                        
                    precio = validar_entrada_numerica("Precio unitario: $", float, minimo=0.01)
                    if precio is None:
                        continue
                    
                    producto = Producto(id_producto, nombre, cantidad, precio)
                    inventario.agregar_producto(producto)
                    
                except ValueError as e:
                    print(f"✗ Error de validación: {e}")
                except Exception as e:
                    print(f"✗ Error inesperado: {e}")

            elif opcion == "2":
                print("\n--- ELIMINAR PRODUCTO ---")
                if not inventario.productos:
                    print("✗ No hay productos en el inventario.")
                    continue
                    
                id_producto = input("ID del producto a eliminar: ").strip()
                if id_producto:
                    inventario.eliminar_producto(id_producto)

            elif opcion == "3":
                print("\n--- ACTUALIZAR PRODUCTO ---")
                if not inventario.productos:
                    print("✗ No hay productos en el inventario.")
                    continue
                    
                id_producto = input("ID del producto a actualizar: ").strip()
                if not id_producto:
                    print("✗ Error: Debe ingresar un ID.")
                    continue
                
                producto_actual = inventario.buscar_por_id(id_producto)
                if not producto_actual:
                    print(f"✗ No se encontró producto con ID '{id_producto}'.")
                    continue
                
                print(f"Producto actual: {producto_actual}")
                print("Deje vacío cualquier campo que no desee actualizar:")
                
                # Nuevo nombre
                nuevo_nombre = input(f"Nuevo nombre [{producto_actual.get_nombre()}]: ").strip()
                nuevo_nombre = nuevo_nombre if nuevo_nombre else None
                
                # Nueva cantidad
                entrada_cantidad = input(f"Nueva cantidad [{producto_actual.get_cantidad()}]: ").strip()
                nueva_cantidad = None
                if entrada_cantidad:
                    try:
                        nueva_cantidad = int(entrada_cantidad)
                        if nueva_cantidad < 0:
                            print("✗ Error: La cantidad no puede ser negativa.")
                            continue
                    except ValueError:
                        print("✗ Error: La cantidad debe ser un número entero.")
                        continue
                
                # Nuevo precio
                entrada_precio = input(f"Nuevo precio [${producto_actual.get_precio():.2f}]: ").strip()
                nuevo_precio = None
                if entrada_precio:
                    try:
                        nuevo_precio = float(entrada_precio)
                        if nuevo_precio <= 0:
                            print("✗ Error: El precio debe ser mayor que cero.")
                            continue
                    except ValueError:
                        print("✗ Error: El precio debe ser un número válido.")
                        continue
                
                inventario.actualizar_producto(id_producto, nuevo_nombre, nueva_cantidad, nuevo_precio)

            elif opcion == "4":
                print("\n--- BUSCAR POR NOMBRE ---")
                nombre = input("Ingrese nombre o parte del nombre: ").strip()
                if nombre:
                    resultados = inventario.buscar_por_nombre(nombre)
                    if resultados:
                        print(f"\n🔍 Se encontraron {len(resultados)} resultado(s):")
                        print("-" * 60)
                        for i, producto in enumerate(resultados, 1):
                            print(f"{i}. {producto}")
                    else:
                        print("✗ No se encontraron productos con ese nombre.")

            elif opcion == "5":
                print("\n--- BUSCAR POR ID ---")
                id_producto = input("Ingrese el ID del producto: ").strip()
                if id_producto:
                    producto = inventario.buscar_por_id(id_producto)
                    if producto:
                        print(f"\n🔍 Producto encontrado:")
                        print("-" * 60)
                        print(producto)
                        print(f"Fecha de creación: {producto.get_fecha_creacion()}")
                    else:
                        print(f"✗ No se encontró producto con ID '{id_producto}'.")

            elif opcion == "6":
                inventario.mostrar_productos()

            elif opcion == "7":
                print("\n--- PRODUCTOS CON STOCK BAJO ---")
                umbral = validar_entrada_numerica("Ingrese umbral de stock (default: 5): ", int, minimo=0)
                if umbral is None:
                    umbral = 5
                
                productos_bajo_stock = inventario.obtener_productos_bajo_stock(umbral)
                if productos_bajo_stock:
                    print(f"\n⚠️ Se encontraron {len(productos_bajo_stock)} producto(s) con stock ≤ {umbral}:")
                    print("-" * 60)
                    for i, producto in enumerate(productos_bajo_stock, 1):
                        print(f"{i}. {producto}")
                else:
                    print(f"✓ Todos los productos tienen stock superior a {umbral}.")

            elif opcion == "8":
                print("\n--- GENERAR REPORTE ---")
                inventario.generar_reporte()

            elif opcion == "9":
                print("\n--- RECARGAR INVENTARIO ---")
                try:
                    inventario.cargar_inventario()
                except InventarioException as e:
                    print(f"✗ Error al recargar: {e}")

            elif opcion == "0":
                print("\n👋 ¡Gracias por usar el Sistema de Gestión de Inventarios!")
                print("Todos los cambios han sido guardados automáticamente.")
                break

            else:
                print("✗ Opción inválida. Por favor, seleccione una opción del 0 al 9.")

        except KeyboardInterrupt:
            print("\n\n👋 Salida forzada del sistema. Los cambios están guardados.")
            break
        except Exception as e:
            print(f"✗ Error inesperado en el menú: {e}")
            print("El sistema continuará ejecutándose...")


if __name__ == "__main__":
    menu_principal()
