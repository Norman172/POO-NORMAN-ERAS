"""
Sistema Avanzado de Gestión de Inventarios
Autor: Norman Eras
Descripción: Sistema POO con colecciones y almacenamiento en archivos
para gestionar el inventario de una tienda de manera eficiente.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Set


class Producto:
    """
    Clase que representa un producto en el inventario.
    
    Atributos:
        _id (str): Identificador único del producto
        _nombre (str): Nombre del producto
        _cantidad (int): Cantidad disponible en inventario
        _precio (float): Precio unitario del producto
        _categoria (str): Categoría del producto
        _proveedor (str): Proveedor del producto
    """
    
    def __init__(self, id_producto: str, nombre: str, cantidad: int, 
                 precio: float, categoria: str = "", proveedor: str = ""):
        """
        Constructor de la clase Producto.
        
        Args:
            id_producto (str): ID único del producto
            nombre (str): Nombre del producto
            cantidad (int): Cantidad inicial
            precio (float): Precio unitario
            categoria (str): Categoría del producto
            proveedor (str): Proveedor del producto
        """
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = max(0, cantidad)  # No permite cantidades negativas
        self._precio = max(0.0, precio)    # No permite precios negativos
        self._categoria = categoria
        self._proveedor = proveedor
        self._fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Getters (Métodos de acceso)
    @property
    def id(self) -> str:
        """Retorna el ID del producto."""
        return self._id
    
    @property
    def nombre(self) -> str:
        """Retorna el nombre del producto."""
        return self._nombre
    
    @property
    def cantidad(self) -> int:
        """Retorna la cantidad del producto."""
        return self._cantidad
    
    @property
    def precio(self) -> float:
        """Retorna el precio del producto."""
        return self._precio
    
    @property
    def categoria(self) -> str:
        """Retorna la categoría del producto."""
        return self._categoria
    
    @property
    def proveedor(self) -> str:
        """Retorna el proveedor del producto."""
        return self._proveedor
    
    @property
    def fecha_creacion(self) -> str:
        """Retorna la fecha de creación del producto."""
        return self._fecha_creacion
    
    # Setters (Métodos de modificación)
    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        """Establece un nuevo nombre para el producto."""
        if nuevo_nombre.strip():
            self._nombre = nuevo_nombre.strip()
    
    @cantidad.setter
    def cantidad(self, nueva_cantidad: int):
        """Establece una nueva cantidad para el producto."""
        self._cantidad = max(0, nueva_cantidad)
    
    @precio.setter
    def precio(self, nuevo_precio: float):
        """Establece un nuevo precio para el producto."""
        self._precio = max(0.0, nuevo_precio)
    
    @categoria.setter
    def categoria(self, nueva_categoria: str):
        """Establece una nueva categoría para el producto."""
        self._categoria = nueva_categoria.strip()
    
    @proveedor.setter
    def proveedor(self, nuevo_proveedor: str):
        """Establece un nuevo proveedor para el producto."""
        self._proveedor = nuevo_proveedor.strip()
    
    def actualizar_stock(self, cantidad_cambio: int) -> bool:
        """
        Actualiza el stock del producto.
        
        Args:
            cantidad_cambio (int): Cambio en la cantidad (positivo o negativo)
            
        Returns:
            bool: True si la operación fue exitosa, False si no
        """
        nueva_cantidad = self._cantidad + cantidad_cambio
        if nueva_cantidad >= 0:
            self._cantidad = nueva_cantidad
            return True
        return False
    
    def calcular_valor_total(self) -> float:
        """Calcula el valor total del inventario de este producto."""
        return self._cantidad * self._precio
    
    def esta_en_stock(self) -> bool:
        """Verifica si el producto tiene stock disponible."""
        return self._cantidad > 0
    
    def to_dict(self) -> Dict:
        """Convierte el producto a diccionario para serialización."""
        return {
            'id': self._id,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': self._precio,
            'categoria': self._categoria,
            'proveedor': self._proveedor,
            'fecha_creacion': self._fecha_creacion
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Crea un producto desde un diccionario."""
        producto = cls(
            data['id'], 
            data['nombre'], 
            data['cantidad'], 
            data['precio'],
            data.get('categoria', ''),
            data.get('proveedor', '')
        )
        producto._fecha_creacion = data.get('fecha_creacion', 
                                          datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        return producto
    
    def __str__(self) -> str:
        """Representación en string del producto."""
        return (f"ID: {self._id} | {self._nombre} | "
                f"Cantidad: {self._cantidad} | Precio: ${self._precio:.2f} | "
                f"Categoría: {self._categoria} | Proveedor: {self._proveedor}")
    
    def __repr__(self) -> str:
        """Representación técnica del producto."""
        return (f"Producto(id='{self._id}', nombre='{self._nombre}', "
                f"cantidad={self._cantidad}, precio={self._precio})")


class Inventario:
    """
    Clase que gestiona una colección de productos usando diferentes estructuras de datos.
    
    Utiliza:
    - Diccionario para búsqueda rápida por ID
    - Set para categorías únicas
    - Lista para histórico de operaciones
    - Tuplas para almacenar operaciones inmutables
    """
    
    def __init__(self, archivo_inventario: str = "inventario.json"):
        """
        Constructor de la clase Inventario.
        
        Args:
            archivo_inventario (str): Nombre del archivo de inventario
        """
        # Diccionario principal: ID -> Producto (O(1) para búsquedas)
        self._productos: Dict[str, Producto] = {}
        
        # Set de categorías únicas (O(1) para verificación de existencia)
        self._categorias: Set[str] = set()
        
        # Lista de historial de operaciones (preserva orden temporal)
        self._historial_operaciones: List[tuple] = []
        
        # Diccionario para índice por nombre (facilita búsquedas por nombre)
        self._indice_nombres: Dict[str, str] = {}  # nombre_lower -> id
        
        # Diccionario para agrupar por proveedor
        self._productos_por_proveedor: Dict[str, List[str]] = {}  # proveedor -> [ids]
        
        # Archivo de persistencia
        self._archivo_inventario = archivo_inventario
        
        # Cargar datos existentes
        self.cargar_desde_archivo()
    
    def _registrar_operacion(self, tipo_operacion: str, producto_id: str, 
                           detalles: str = ""):
        """
        Registra una operación en el historial.
        
        Args:
            tipo_operacion (str): Tipo de operación realizada
            producto_id (str): ID del producto afectado
            detalles (str): Detalles adicionales de la operación
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        operacion = (timestamp, tipo_operacion, producto_id, detalles)
        self._historial_operaciones.append(operacion)
    
    def _actualizar_indices(self, producto: Producto):
        """Actualiza los índices auxiliares."""
        # Actualizar índice de nombres
        self._indice_nombres[producto.nombre.lower()] = producto.id
        
        # Actualizar categorías
        if producto.categoria:
            self._categorias.add(producto.categoria)
        
        # Actualizar índice de proveedores
        if producto.proveedor:
            if producto.proveedor not in self._productos_por_proveedor:
                self._productos_por_proveedor[producto.proveedor] = []
            if producto.id not in self._productos_por_proveedor[producto.proveedor]:
                self._productos_por_proveedor[producto.proveedor].append(producto.id)
    
    def _limpiar_indices(self, producto: Producto):
        """Limpia los índices auxiliares al eliminar un producto."""
        # Limpiar índice de nombres
        if producto.nombre.lower() in self._indice_nombres:
            del self._indice_nombres[producto.nombre.lower()]
        
        # Limpiar proveedor
        if producto.proveedor in self._productos_por_proveedor:
            if producto.id in self._productos_por_proveedor[producto.proveedor]:
                self._productos_por_proveedor[producto.proveedor].remove(producto.id)
                if not self._productos_por_proveedor[producto.proveedor]:
                    del self._productos_por_proveedor[producto.proveedor]
    
    def agregar_producto(self, producto: Producto) -> bool:
        """
        Agrega un nuevo producto al inventario.
        
        Args:
            producto (Producto): El producto a agregar
            
        Returns:
            bool: True si se agregó exitosamente, False si el ID ya existe
        """
        if producto.id in self._productos:
            return False
        
        self._productos[producto.id] = producto
        self._actualizar_indices(producto)
        self._registrar_operacion("AGREGAR", producto.id, 
                                f"Producto '{producto.nombre}' agregado")
        return True
    
    def eliminar_producto(self, id_producto: str) -> bool:
        """
        Elimina un producto del inventario por su ID.
        
        Args:
            id_producto (str): ID del producto a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente, False si no existe
        """
        if id_producto not in self._productos:
            return False
        
        producto = self._productos[id_producto]
        self._limpiar_indices(producto)
        del self._productos[id_producto]
        self._registrar_operacion("ELIMINAR", id_producto, 
                                f"Producto '{producto.nombre}' eliminado")
        return True
    
    def buscar_producto_por_id(self, id_producto: str) -> Optional[Producto]:
        """
        Busca un producto por su ID.
        
        Args:
            id_producto (str): ID del producto a buscar
            
        Returns:
            Optional[Producto]: El producto encontrado o None
        """
        return self._productos.get(id_producto)
    
    def buscar_productos_por_nombre(self, nombre: str) -> List[Producto]:
        """
        Busca productos por nombre (búsqueda parcial, insensible a mayúsculas).
        
        Args:
            nombre (str): Nombre o parte del nombre a buscar
            
        Returns:
            List[Producto]: Lista de productos que coinciden
        """
        nombre_lower = nombre.lower()
        productos_encontrados = []
        
        for producto in self._productos.values():
            if nombre_lower in producto.nombre.lower():
                productos_encontrados.append(producto)
        
        return productos_encontrados
    
    def buscar_productos_por_categoria(self, categoria: str) -> List[Producto]:
        """
        Busca productos por categoría.
        
        Args:
            categoria (str): Categoría a buscar
            
        Returns:
            List[Producto]: Lista de productos de la categoría
        """
        return [producto for producto in self._productos.values() 
                if producto.categoria.lower() == categoria.lower()]
    
    def buscar_productos_por_proveedor(self, proveedor: str) -> List[Producto]:
        """
        Busca productos por proveedor.
        
        Args:
            proveedor (str): Proveedor a buscar
            
        Returns:
            List[Producto]: Lista de productos del proveedor
        """
        if proveedor in self._productos_por_proveedor:
            return [self._productos[pid] 
                   for pid in self._productos_por_proveedor[proveedor]]
        return []
    
    def actualizar_cantidad(self, id_producto: str, nueva_cantidad: int) -> bool:
        """
        Actualiza la cantidad de un producto.
        
        Args:
            id_producto (str): ID del producto
            nueva_cantidad (int): Nueva cantidad
            
        Returns:
            bool: True si se actualizó exitosamente
        """
        if id_producto not in self._productos:
            return False
        
        cantidad_anterior = self._productos[id_producto].cantidad
        self._productos[id_producto].cantidad = nueva_cantidad
        self._registrar_operacion("ACTUALIZAR_CANTIDAD", id_producto, 
                                f"Cantidad cambiada de {cantidad_anterior} a {nueva_cantidad}")
        return True
    
    def actualizar_precio(self, id_producto: str, nuevo_precio: float) -> bool:
        """
        Actualiza el precio de un producto.
        
        Args:
            id_producto (str): ID del producto
            nuevo_precio (float): Nuevo precio
            
        Returns:
            bool: True si se actualizó exitosamente
        """
        if id_producto not in self._productos:
            return False
        
        precio_anterior = self._productos[id_producto].precio
        self._productos[id_producto].precio = nuevo_precio
        self._registrar_operacion("ACTUALIZAR_PRECIO", id_producto, 
                                f"Precio cambiado de ${precio_anterior:.2f} a ${nuevo_precio:.2f}")
        return True
    
    def obtener_todos_productos(self) -> List[Producto]:
        """
        Obtiene una lista de todos los productos en el inventario.
        
        Returns:
            List[Producto]: Lista de todos los productos
        """
        return list(self._productos.values())
    
    def obtener_categorias(self) -> Set[str]:
        """
        Obtiene todas las categorías disponibles.
        
        Returns:
            Set[str]: Conjunto de categorías únicas
        """
        return self._categorias.copy()
    
    def obtener_proveedores(self) -> List[str]:
        """
        Obtiene todos los proveedores.
        
        Returns:
            List[str]: Lista de proveedores
        """
        return list(self._productos_por_proveedor.keys())
    
    def obtener_estadisticas(self) -> Dict:
        """
        Obtiene estadísticas del inventario.
        
        Returns:
            Dict: Diccionario con estadísticas
        """
        productos = list(self._productos.values())
        
        if not productos:
            return {
                'total_productos': 0,
                'total_items': 0,
                'valor_total_inventario': 0.0,
                'producto_mas_caro': None,
                'producto_mas_barato': None,
                'categoria_con_mas_productos': None,
                'productos_sin_stock': 0
            }
        
        valor_total = sum(p.calcular_valor_total() for p in productos)
        total_items = sum(p.cantidad for p in productos)
        producto_mas_caro = max(productos, key=lambda p: p.precio)
        producto_mas_barato = min(productos, key=lambda p: p.precio)
        productos_sin_stock = len([p for p in productos if not p.esta_en_stock()])
        
        # Categoría con más productos
        categoria_count = {}
        for producto in productos:
            if producto.categoria:
                categoria_count[producto.categoria] = categoria_count.get(producto.categoria, 0) + 1
        
        categoria_popular = max(categoria_count.items(), key=lambda x: x[1])[0] if categoria_count else None
        
        return {
            'total_productos': len(productos),
            'total_items': total_items,
            'valor_total_inventario': valor_total,
            'producto_mas_caro': producto_mas_caro,
            'producto_mas_barato': producto_mas_barato,
            'categoria_con_mas_productos': categoria_popular,
            'productos_sin_stock': productos_sin_stock,
            'total_categorias': len(self._categorias),
            'total_proveedores': len(self._productos_por_proveedor)
        }
    
    def obtener_historial_operaciones(self, limite: int = 50) -> List[tuple]:
        """
        Obtiene el historial de operaciones.
        
        Args:
            limite (int): Número máximo de operaciones a devolver
            
        Returns:
            List[tuple]: Lista de operaciones recientes
        """
        return self._historial_operaciones[-limite:]
    
    def productos_con_stock_bajo(self, umbral: int = 5) -> List[Producto]:
        """
        Obtiene productos con stock bajo.
        
        Args:
            umbral (int): Umbral de stock bajo
            
        Returns:
            List[Producto]: Productos con stock menor al umbral
        """
        return [producto for producto in self._productos.values() 
                if producto.cantidad <= umbral]
    
    def guardar_en_archivo(self) -> bool:
        """
        Guarda el inventario en un archivo JSON.
        
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            # Crear backup antes de guardar
            if os.path.exists(self._archivo_inventario):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"backup_{timestamp}_{self._archivo_inventario}"
                
                # Crear directorio de backups si no existe
                backup_dir = "backups"
                os.makedirs(backup_dir, exist_ok=True)
                backup_path = os.path.join(backup_dir, backup_name)
                
                import shutil
                shutil.copy2(self._archivo_inventario, backup_path)
            
            # Preparar datos para guardar
            datos = {
                'productos': {id_prod: producto.to_dict() 
                             for id_prod, producto in self._productos.items()},
                'historial_operaciones': self._historial_operaciones[-100:],  # Solo últimas 100
                'fecha_guardado': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Guardar en archivo
            with open(self._archivo_inventario, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error al guardar el inventario: {e}")
            return False
    
    def cargar_desde_archivo(self) -> bool:
        """
        Carga el inventario desde un archivo JSON.
        
        Returns:
            bool: True si se cargó exitosamente
        """
        try:
            if not os.path.exists(self._archivo_inventario):
                return True  # Archivo no existe, se inicia vacío
            
            with open(self._archivo_inventario, 'r', encoding='utf-8') as archivo:
                datos = json.load(archivo)
            
            # Cargar productos
            if 'productos' in datos:
                for id_producto, datos_producto in datos['productos'].items():
                    producto = Producto.from_dict(datos_producto)
                    self._productos[id_producto] = producto
                    self._actualizar_indices(producto)
            
            # Cargar historial
            if 'historial_operaciones' in datos:
                self._historial_operaciones = datos['historial_operaciones']
            
            return True
            
        except Exception as e:
            print(f"Error al cargar el inventario: {e}")
            return False
    
    def exportar_reporte(self, nombre_archivo: str = None) -> str:
        """
        Exporta un reporte completo del inventario.
        
        Args:
            nombre_archivo (str): Nombre del archivo de reporte
            
        Returns:
            str: Ruta del archivo generado
        """
        if not nombre_archivo:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_inventario_{timestamp}.txt"
        
        try:
            with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
                archivo.write("="*80 + "\n")
                archivo.write("REPORTE DE INVENTARIO - SISTEMA AVANZADO\n")
                archivo.write("="*80 + "\n")
                archivo.write(f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Estadísticas generales
                stats = self.obtener_estadisticas()
                archivo.write("ESTADÍSTICAS GENERALES:\n")
                archivo.write("-" * 30 + "\n")
                archivo.write(f"Total de productos únicos: {stats['total_productos']}\n")
                archivo.write(f"Total de items en inventario: {stats['total_items']}\n")
                archivo.write(f"Valor total del inventario: ${stats['valor_total_inventario']:.2f}\n")
                archivo.write(f"Total de categorías: {stats['total_categorias']}\n")
                archivo.write(f"Total de proveedores: {stats['total_proveedores']}\n")
                archivo.write(f"Productos sin stock: {stats['productos_sin_stock']}\n\n")
                
                if stats['producto_mas_caro']:
                    archivo.write(f"Producto más caro: {stats['producto_mas_caro'].nombre} "
                                f"(${stats['producto_mas_caro'].precio:.2f})\n")
                if stats['producto_mas_barato']:
                    archivo.write(f"Producto más barato: {stats['producto_mas_barato'].nombre} "
                                f"(${stats['producto_mas_barato'].precio:.2f})\n")
                if stats['categoria_con_mas_productos']:
                    archivo.write(f"Categoría más popular: {stats['categoria_con_mas_productos']}\n")
                
                archivo.write("\n" + "="*80 + "\n")
                archivo.write("LISTA COMPLETA DE PRODUCTOS:\n")
                archivo.write("="*80 + "\n")
                
                # Lista de productos ordenados por categoría
                productos_por_categoria = {}
                for producto in self._productos.values():
                    categoria = producto.categoria if producto.categoria else "Sin categoría"
                    if categoria not in productos_por_categoria:
                        productos_por_categoria[categoria] = []
                    productos_por_categoria[categoria].append(producto)
                
                for categoria, productos in sorted(productos_por_categoria.items()):
                    archivo.write(f"\nCATEGORÍA: {categoria}\n")
                    archivo.write("-" * 50 + "\n")
                    for producto in sorted(productos, key=lambda p: p.nombre):
                        archivo.write(f"{producto}\n")
                        archivo.write(f"  Valor total: ${producto.calcular_valor_total():.2f}\n")
                        archivo.write(f"  Fecha de creación: {producto.fecha_creacion}\n")
                        archivo.write(f"  Stock disponible: {'Sí' if producto.esta_en_stock() else 'No'}\n\n")
                
                # Stock bajo
                productos_stock_bajo = self.productos_con_stock_bajo()
                if productos_stock_bajo:
                    archivo.write("\n" + "="*80 + "\n")
                    archivo.write("PRODUCTOS CON STOCK BAJO (≤5 unidades):\n")
                    archivo.write("="*80 + "\n")
                    for producto in productos_stock_bajo:
                        archivo.write(f"⚠️  {producto}\n")
                
                # Historial reciente
                historial = self.obtener_historial_operaciones(20)
                if historial:
                    archivo.write("\n" + "="*80 + "\n")
                    archivo.write("HISTORIAL RECIENTE DE OPERACIONES (últimas 20):\n")
                    archivo.write("="*80 + "\n")
                    for operacion in reversed(historial):
                        timestamp, tipo, producto_id, detalles = operacion
                        archivo.write(f"{timestamp} | {tipo} | ID: {producto_id} | {detalles}\n")
                
                archivo.write("\n" + "="*80 + "\n")
                archivo.write("Fin del reporte\n")
                archivo.write("="*80 + "\n")
            
            return nombre_archivo
            
        except Exception as e:
            print(f"Error al generar reporte: {e}")
            return ""
    
    def __len__(self) -> int:
        """Retorna el número de productos en el inventario."""
        return len(self._productos)
    
    def __contains__(self, id_producto: str) -> bool:
        """Verifica si un producto existe en el inventario."""
        return id_producto in self._productos
    
    def __str__(self) -> str:
        """Representación en string del inventario."""
        return f"Inventario con {len(self._productos)} productos"


# Funciones utilitarias para la interfaz de usuario
def mostrar_menu_principal():
    """Muestra el menú principal del sistema."""
    print("\n" + "="*60)
    print("🏪  SISTEMA AVANZADO DE GESTIÓN DE INVENTARIOS  🏪")
    print("="*60)
    print("1.  ➕ Agregar nuevo producto")
    print("2.  🗑️  Eliminar producto")
    print("3.  🔍 Buscar producto por ID")
    print("4.  🔎 Buscar productos por nombre")
    print("5.  📂 Buscar productos por categoría")
    print("6.  🏭 Buscar productos por proveedor")
    print("7.  📊 Actualizar cantidad de producto")
    print("8.  💲 Actualizar precio de producto")
    print("9.  📋 Mostrar todos los productos")
    print("10. 📈 Ver estadísticas del inventario")
    print("11. 📜 Ver historial de operaciones")
    print("12. ⚠️  Ver productos con stock bajo")
    print("13. 📁 Ver categorías disponibles")
    print("14. 🏭 Ver proveedores disponibles")
    print("15. 💾 Guardar inventario manualmente")
    print("16. 📄 Generar reporte completo")
    print("17. ❌ Salir del sistema")
    print("="*60)


def obtener_input_numero(mensaje: str, tipo=int, minimo=None, maximo=None):
    """
    Obtiene un número del usuario con validación.
    
    Args:
        mensaje (str): Mensaje a mostrar al usuario
        tipo (type): Tipo de dato esperado (int o float)
        minimo: Valor mínimo permitido
        maximo: Valor máximo permitido
    """
    while True:
        try:
            valor = tipo(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"❌ El valor debe ser mayor o igual a {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"❌ El valor debe ser menor o igual a {maximo}")
                continue
            return valor
        except ValueError:
            print(f"❌ Por favor, ingrese un {tipo.__name__} válido")


def obtener_input_texto(mensaje: str, obligatorio: bool = True) -> str:
    """
    Obtiene texto del usuario con validación.
    
    Args:
        mensaje (str): Mensaje a mostrar
        obligatorio (bool): Si el campo es obligatorio
    """
    while True:
        texto = input(mensaje).strip()
        if not obligatorio or texto:
            return texto
        print("❌ Este campo es obligatorio")


def confirmar_accion(mensaje: str) -> bool:
    """
    Pide confirmación al usuario para una acción.
    
    Args:
        mensaje (str): Mensaje de confirmación
        
    Returns:
        bool: True si el usuario confirma
    """
    respuesta = input(f"{mensaje} (s/n): ").lower().strip()
    return respuesta in ['s', 'si', 'sí', 'y', 'yes']


def mostrar_producto(producto: Producto, mostrar_detalles: bool = True):
    """
    Muestra la información de un producto de forma formateada.
    
    Args:
        producto (Producto): Producto a mostrar
        mostrar_detalles (bool): Si mostrar información detallada
    """
    print("┌" + "─" * 78 + "┐")
    print(f"│ ID: {producto.id:<20} │ Nombre: {producto.nombre:<35} │")
    print(f"│ Cantidad: {producto.cantidad:<12} │ Precio: ${producto.precio:<25.2f} │")
    
    if mostrar_detalles:
        print(f"│ Categoría: {producto.categoria:<15} │ Proveedor: {producto.proveedor:<25} │")
        print(f"│ Valor total: ${producto.calcular_valor_total():<10.2f} │ Stock: {'✅' if producto.esta_en_stock() else '❌':<30} │")
        print(f"│ Fecha creación: {producto.fecha_creacion:<52} │")
    
    print("└" + "─" * 78 + "┘")


def main():
    """Función principal que ejecuta la interfaz de usuario."""
    print("🚀 Iniciando Sistema Avanzado de Gestión de Inventarios...")
    inventario = Inventario()
    print(f"✅ Sistema iniciado. Inventario cargado con {len(inventario)} productos.")
    
    while True:
        try:
            mostrar_menu_principal()
            opcion = obtener_input_numero("👉 Seleccione una opción: ", int, 1, 17)
            print()  # Línea en blanco para mejor legibilidad
            
            if opcion == 1:  # Agregar producto
                print("📝 AGREGAR NUEVO PRODUCTO")
                print("-" * 30)
                
                id_producto = obtener_input_texto("🆔 ID del producto: ")
                if inventario.buscar_producto_por_id(id_producto):
                    print(f"❌ Ya existe un producto con ID '{id_producto}'")
                    continue
                
                nombre = obtener_input_texto("📦 Nombre del producto: ")
                cantidad = obtener_input_numero("📊 Cantidad inicial: ", int, 0)
                precio = obtener_input_numero("💰 Precio unitario: $", float, 0)
                categoria = obtener_input_texto("📂 Categoría (opcional): ", False)
                proveedor = obtener_input_texto("🏭 Proveedor (opcional): ", False)
                
                producto = Producto(id_producto, nombre, cantidad, precio, categoria, proveedor)
                
                if inventario.agregar_producto(producto):
                    print(f"✅ Producto '{nombre}' agregado exitosamente!")
                    mostrar_producto(producto)
                else:
                    print("❌ Error al agregar el producto")
            
            elif opcion == 2:  # Eliminar producto
                print("🗑️  ELIMINAR PRODUCTO")
                print("-" * 20)
                
                id_producto = obtener_input_texto("🆔 ID del producto a eliminar: ")
                producto = inventario.buscar_producto_por_id(id_producto)
                
                if not producto:
                    print(f"❌ No existe un producto con ID '{id_producto}'")
                    continue
                
                print("📦 Producto encontrado:")
                mostrar_producto(producto)
                
                if confirmar_accion("⚠️  ¿Está seguro que desea eliminar este producto?"):
                    if inventario.eliminar_producto(id_producto):
                        print("✅ Producto eliminado exitosamente!")
                    else:
                        print("❌ Error al eliminar el producto")
                else:
                    print("❌ Operación cancelada")
            
            elif opcion == 3:  # Buscar por ID
                print("🔍 BUSCAR PRODUCTO POR ID")
                print("-" * 25)
                
                id_producto = obtener_input_texto("🆔 ID del producto: ")
                producto = inventario.buscar_producto_por_id(id_producto)
                
                if producto:
                    print("✅ Producto encontrado:")
                    mostrar_producto(producto)
                else:
                    print(f"❌ No se encontró un producto con ID '{id_producto}'")
            
            elif opcion == 4:  # Buscar por nombre
                print("🔎 BUSCAR PRODUCTOS POR NOMBRE")
                print("-" * 32)
                
                nombre = obtener_input_texto("📦 Nombre o parte del nombre: ")
                productos = inventario.buscar_productos_por_nombre(nombre)
                
                if productos:
                    print(f"✅ Se encontraron {len(productos)} productos:")
                    for i, producto in enumerate(productos, 1):
                        print(f"\n--- Producto {i} ---")
                        mostrar_producto(producto, False)
                else:
                    print(f"❌ No se encontraron productos con nombre '{nombre}'")
            
            elif opcion == 5:  # Buscar por categoría
                print("📂 BUSCAR PRODUCTOS POR CATEGORÍA")
                print("-" * 35)
                
                categorias = inventario.obtener_categorias()
                if categorias:
                    print("📋 Categorías disponibles:")
                    for i, categoria in enumerate(sorted(categorias), 1):
                        print(f"  {i}. {categoria}")
                    print()
                
                categoria = obtener_input_texto("📂 Categoría: ")
                productos = inventario.buscar_productos_por_categoria(categoria)
                
                if productos:
                    print(f"✅ Se encontraron {len(productos)} productos en la categoría '{categoria}':")
                    for i, producto in enumerate(productos, 1):
                        print(f"\n--- Producto {i} ---")
                        mostrar_producto(producto, False)
                else:
                    print(f"❌ No se encontraron productos en la categoría '{categoria}'")
            
            elif opcion == 6:  # Buscar por proveedor
                print("🏭 BUSCAR PRODUCTOS POR PROVEEDOR")
                print("-" * 33)
                
                proveedores = inventario.obtener_proveedores()
                if proveedores:
                    print("📋 Proveedores disponibles:")
                    for i, proveedor in enumerate(sorted(proveedores), 1):
                        print(f"  {i}. {proveedor}")
                    print()
                
                proveedor = obtener_input_texto("🏭 Proveedor: ")
                productos = inventario.buscar_productos_por_proveedor(proveedor)
                
                if productos:
                    print(f"✅ Se encontraron {len(productos)} productos del proveedor '{proveedor}':")
                    for i, producto in enumerate(productos, 1):
                        print(f"\n--- Producto {i} ---")
                        mostrar_producto(producto, False)
                else:
                    print(f"❌ No se encontraron productos del proveedor '{proveedor}'")
            
            elif opcion == 7:  # Actualizar cantidad
                print("📊 ACTUALIZAR CANTIDAD DE PRODUCTO")
                print("-" * 35)
                
                id_producto = obtener_input_texto("🆔 ID del producto: ")
                producto = inventario.buscar_producto_por_id(id_producto)
                
                if not producto:
                    print(f"❌ No existe un producto con ID '{id_producto}'")
                    continue
                
                print("📦 Producto encontrado:")
                mostrar_producto(producto, False)
                print(f"📊 Cantidad actual: {producto.cantidad}")
                
                nueva_cantidad = obtener_input_numero("📊 Nueva cantidad: ", int, 0)
                
                if inventario.actualizar_cantidad(id_producto, nueva_cantidad):
                    print(f"✅ Cantidad actualizada de {producto.cantidad} a {nueva_cantidad}")
                else:
                    print("❌ Error al actualizar la cantidad")
            
            elif opcion == 8:  # Actualizar precio
                print("💲 ACTUALIZAR PRECIO DE PRODUCTO")
                print("-" * 32)
                
                id_producto = obtener_input_texto("🆔 ID del producto: ")
                producto = inventario.buscar_producto_por_id(id_producto)
                
                if not producto:
                    print(f"❌ No existe un producto con ID '{id_producto}'")
                    continue
                
                print("📦 Producto encontrado:")
                mostrar_producto(producto, False)
                print(f"💰 Precio actual: ${producto.precio:.2f}")
                
                nuevo_precio = obtener_input_numero("💰 Nuevo precio: $", float, 0)
                
                if inventario.actualizar_precio(id_producto, nuevo_precio):
                    print(f"✅ Precio actualizado de ${producto.precio:.2f} a ${nuevo_precio:.2f}")
                else:
                    print("❌ Error al actualizar el precio")
            
            elif opcion == 9:  # Mostrar todos los productos
                print("📋 TODOS LOS PRODUCTOS EN INVENTARIO")
                print("-" * 37)
                
                productos = inventario.obtener_todos_productos()
                
                if not productos:
                    print("❌ No hay productos en el inventario")
                    continue
                
                # Ordenar productos por categoría y luego por nombre
                productos_ordenados = sorted(productos, key=lambda p: (p.categoria, p.nombre))
                categoria_actual = None
                
                for i, producto in enumerate(productos_ordenados, 1):
                    if producto.categoria != categoria_actual:
                        categoria_actual = producto.categoria
                        categoria_mostrar = categoria_actual if categoria_actual else "Sin categoría"
                        print(f"\n{'='*20} {categoria_mostrar} {'='*20}")
                    
                    print(f"\n--- Producto {i} ---")
                    mostrar_producto(producto, False)
                
                print(f"\n📊 Total de productos: {len(productos)}")
            
            elif opcion == 10:  # Estadísticas
                print("📈 ESTADÍSTICAS DEL INVENTARIO")
                print("-" * 30)
                
                stats = inventario.obtener_estadisticas()
                
                print(f"📦 Total de productos únicos: {stats['total_productos']}")
                print(f"📊 Total de items en stock: {stats['total_items']}")
                print(f"💰 Valor total del inventario: ${stats['valor_total_inventario']:.2f}")
                print(f"📂 Total de categorías: {stats['total_categorias']}")
                print(f"🏭 Total de proveedores: {stats['total_proveedores']}")
                print(f"⚠️  Productos sin stock: {stats['productos_sin_stock']}")
                
                if stats['producto_mas_caro']:
                    print(f"💎 Producto más caro: {stats['producto_mas_caro'].nombre} "
                          f"(${stats['producto_mas_caro'].precio:.2f})")
                
                if stats['producto_mas_barato']:
                    print(f"💲 Producto más barato: {stats['producto_mas_barato'].nombre} "
                          f"(${stats['producto_mas_barato'].precio:.2f})")
                
                if stats['categoria_con_mas_productos']:
                    print(f"🏆 Categoría más popular: {stats['categoria_con_mas_productos']}")
            
            elif opcion == 11:  # Historial
                print("📜 HISTORIAL DE OPERACIONES")
                print("-" * 27)
                
                limite = obtener_input_numero("📊 ¿Cuántas operaciones mostrar? (por defecto 20): ", 
                                            int, 1, 100)
                historial = inventario.obtener_historial_operaciones(limite)
                
                if not historial:
                    print("❌ No hay operaciones en el historial")
                    continue
                
                print(f"\n📋 Últimas {len(historial)} operaciones:")
                print("-" * 80)
                print(f"{'Fecha/Hora':<20} {'Operación':<18} {'ID Producto':<12} {'Detalles'}")
                print("-" * 80)
                
                for operacion in reversed(historial):
                    timestamp, tipo, producto_id, detalles = operacion
                    print(f"{timestamp:<20} {tipo:<18} {producto_id:<12} {detalles}")
            
            elif opcion == 12:  # Stock bajo
                print("⚠️  PRODUCTOS CON STOCK BAJO")
                print("-" * 28)
                
                umbral = obtener_input_numero("📊 Umbral de stock bajo (por defecto 5): ", int, 0)
                productos_stock_bajo = inventario.productos_con_stock_bajo(umbral)
                
                if not productos_stock_bajo:
                    print(f"✅ No hay productos con stock menor o igual a {umbral}")
                    continue
                
                print(f"⚠️  Se encontraron {len(productos_stock_bajo)} productos con stock bajo:")
                
                for i, producto in enumerate(productos_stock_bajo, 1):
                    print(f"\n--- Producto {i} ---")
                    mostrar_producto(producto, False)
                    if producto.cantidad == 0:
                        print("🚨 ¡SIN STOCK!")
            
            elif opcion == 13:  # Ver categorías
                print("📂 CATEGORÍAS DISPONIBLES")
                print("-" * 25)
                
                categorias = inventario.obtener_categorias()
                
                if not categorias:
                    print("❌ No hay categorías registradas")
                    continue
                
                print(f"📋 Total de categorías: {len(categorias)}")
                print("-" * 30)
                
                for i, categoria in enumerate(sorted(categorias), 1):
                    productos_categoria = inventario.buscar_productos_por_categoria(categoria)
                    print(f"{i:2d}. {categoria} ({len(productos_categoria)} productos)")
            
            elif opcion == 14:  # Ver proveedores
                print("🏭 PROVEEDORES DISPONIBLES")
                print("-" * 25)
                
                proveedores = inventario.obtener_proveedores()
                
                if not proveedores:
                    print("❌ No hay proveedores registrados")
                    continue
                
                print(f"📋 Total de proveedores: {len(proveedores)}")
                print("-" * 30)
                
                for i, proveedor in enumerate(sorted(proveedores), 1):
                    productos_proveedor = inventario.buscar_productos_por_proveedor(proveedor)
                    print(f"{i:2d}. {proveedor} ({len(productos_proveedor)} productos)")
            
            elif opcion == 15:  # Guardar manualmente
                print("💾 GUARDAR INVENTARIO")
                print("-" * 20)
                
                if inventario.guardar_en_archivo():
                    print("✅ Inventario guardado exitosamente!")
                else:
                    print("❌ Error al guardar el inventario")
            
            elif opcion == 16:  # Generar reporte
                print("📄 GENERAR REPORTE COMPLETO")
                print("-" * 28)
                
                if confirmar_accion("¿Desea generar un reporte completo del inventario?"):
                    archivo_reporte = inventario.exportar_reporte()
                    if archivo_reporte:
                        print(f"✅ Reporte generado exitosamente: {archivo_reporte}")
                    else:
                        print("❌ Error al generar el reporte")
            
            elif opcion == 17:  # Salir
                print("👋 SALIR DEL SISTEMA")
                print("-" * 18)
                
                if confirmar_accion("¿Desea guardar los cambios antes de salir?"):
                    if inventario.guardar_en_archivo():
                        print("✅ Inventario guardado exitosamente!")
                    else:
                        print("❌ Error al guardar el inventario")
                
                print("👋 ¡Gracias por usar el Sistema de Gestión de Inventarios!")
                print("🚪 Saliendo del sistema...")
                break
            
            # Pausa para que el usuario pueda leer el resultado
            input("\n📌 Presione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Operación interrumpida por el usuario")
            if confirmar_accion("¿Desea salir del sistema?"):
                if confirmar_accion("¿Desea guardar los cambios antes de salir?"):
                    inventario.guardar_en_archivo()
                    print("✅ Cambios guardados")
                print("👋 ¡Hasta luego!")
                break
            
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            input("📌 Presione Enter para continuar...")


if __name__ == "__main__":
    main()