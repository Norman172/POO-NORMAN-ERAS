"""
Sistema de Gestión de Biblioteca Digital
========================================

Este sistema permite gestionar una biblioteca digital con las siguientes funcionalidades:
- Gestión de libros (añadir, quitar, buscar)
- Gestión de usuarios (registrar, dar de baja)
- Gestión de préstamos (prestar, devolver)
- Búsquedas por título, autor o categoría

Autores: Norman Eras
Fecha: Septiembre 2025
"""

from datetime import datetime
from typing import List, Dict, Set, Optional, Tuple
import json


class Libro:
    """
    Clase que representa un libro en la biblioteca.
    
    Utiliza una tupla para almacenar autor y título ya que son inmutables.
    """
    
    def __init__(self, titulo: str, autor: str, categoria: str, isbn: str):
        """
        Inicializa un nuevo libro.
        
        Args:
            titulo (str): Título del libro
            autor (str): Autor del libro
            categoria (str): Categoría del libro
            isbn (str): ISBN único del libro
        """
        # Tupla inmutable para título y autor
        self._titulo_autor: Tuple[str, str] = (titulo, autor)
        self._categoria = categoria
        self._isbn = isbn
        self._disponible = True
        self._fecha_agregado = datetime.now()
    
    @property
    def titulo(self) -> str:
        """Obtiene el título del libro."""
        return self._titulo_autor[0]
    
    @property
    def autor(self) -> str:
        """Obtiene el autor del libro."""
        return self._titulo_autor[1]
    
    @property
    def categoria(self) -> str:
        """Obtiene la categoría del libro."""
        return self._categoria
    
    @categoria.setter
    def categoria(self, nueva_categoria: str):
        """Establece una nueva categoría para el libro."""
        self._categoria = nueva_categoria
    
    @property
    def isbn(self) -> str:
        """Obtiene el ISBN del libro."""
        return self._isbn
    
    @property
    def disponible(self) -> bool:
        """Verifica si el libro está disponible."""
        return self._disponible
    
    def prestar(self) -> bool:
        """
        Marca el libro como prestado.
        
        Returns:
            bool: True si se pudo prestar, False si ya estaba prestado
        """
        if self._disponible:
            self._disponible = False
            return True
        return False
    
    def devolver(self) -> bool:
        """
        Marca el libro como devuelto.
        
        Returns:
            bool: True si se pudo devolver, False si ya estaba disponible
        """
        if not self._disponible:
            self._disponible = True
            return True
        return False
    
    def to_dict(self) -> dict:
        """Convierte el libro a diccionario para serialización."""
        return {
            'titulo': self.titulo,
            'autor': self.autor,
            'categoria': self._categoria,
            'isbn': self._isbn,
            'disponible': self._disponible,
            'fecha_agregado': self._fecha_agregado.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Libro':
        """Crea un libro desde un diccionario."""
        libro = cls(data['titulo'], data['autor'], data['categoria'], data['isbn'])
        libro._disponible = data['disponible']
        libro._fecha_agregado = datetime.fromisoformat(data['fecha_agregado'])
        return libro
    
    def __str__(self) -> str:
        estado = "Disponible" if self._disponible else "Prestado"
        return f"'{self.titulo}' por {self.autor} [{self._categoria}] - {estado}"
    
    def __repr__(self) -> str:
        return f"Libro(titulo='{self.titulo}', autor='{self.autor}', isbn='{self._isbn}')"


class Usuario:
    """
    Clase que representa un usuario de la biblioteca.
    
    Utiliza una lista para gestionar los libros prestados.
    """
    
    def __init__(self, nombre: str, id_usuario: str):
        """
        Inicializa un nuevo usuario.
        
        Args:
            nombre (str): Nombre completo del usuario
            id_usuario (str): ID único del usuario
        """
        self._nombre = nombre
        self._id_usuario = id_usuario
        self._libros_prestados: List[str] = []  # Lista de ISBNs
        self._fecha_registro = datetime.now()
        self._historial_prestamos: List[dict] = []
    
    @property
    def nombre(self) -> str:
        """Obtiene el nombre del usuario."""
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        """Establece un nuevo nombre para el usuario."""
        self._nombre = nuevo_nombre
    
    @property
    def id_usuario(self) -> str:
        """Obtiene el ID del usuario."""
        return self._id_usuario
    
    @property
    def libros_prestados(self) -> List[str]:
        """Obtiene la lista de ISBNs de libros prestados."""
        return self._libros_prestados.copy()  # Devuelve una copia para proteger la lista original
    
    @property
    def cantidad_libros_prestados(self) -> int:
        """Obtiene la cantidad de libros actualmente prestados."""
        return len(self._libros_prestados)
    
    def prestar_libro(self, isbn: str) -> bool:
        """
        Añade un libro a la lista de prestados.
        
        Args:
            isbn (str): ISBN del libro a prestar
            
        Returns:
            bool: True si se añadió correctamente
        """
        if isbn not in self._libros_prestados:
            self._libros_prestados.append(isbn)
            # Registrar en historial
            self._historial_prestamos.append({
                'accion': 'prestamo',
                'isbn': isbn,
                'fecha': datetime.now().isoformat()
            })
            return True
        return False
    
    def devolver_libro(self, isbn: str) -> bool:
        """
        Quita un libro de la lista de prestados.
        
        Args:
            isbn (str): ISBN del libro a devolver
            
        Returns:
            bool: True si se quitó correctamente
        """
        if isbn in self._libros_prestados:
            self._libros_prestados.remove(isbn)
            # Registrar en historial
            self._historial_prestamos.append({
                'accion': 'devolucion',
                'isbn': isbn,
                'fecha': datetime.now().isoformat()
            })
            return True
        return False
    
    def tiene_libro(self, isbn: str) -> bool:
        """Verifica si el usuario tiene un libro específico prestado."""
        return isbn in self._libros_prestados
    
    def to_dict(self) -> dict:
        """Convierte el usuario a diccionario para serialización."""
        return {
            'nombre': self._nombre,
            'id_usuario': self._id_usuario,
            'libros_prestados': self._libros_prestados,
            'fecha_registro': self._fecha_registro.isoformat(),
            'historial_prestamos': self._historial_prestamos
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Usuario':
        """Crea un usuario desde un diccionario."""
        usuario = cls(data['nombre'], data['id_usuario'])
        usuario._libros_prestados = data['libros_prestados']
        usuario._fecha_registro = datetime.fromisoformat(data['fecha_registro'])
        usuario._historial_prestamos = data.get('historial_prestamos', [])
        return usuario
    
    def __str__(self) -> str:
        return f"Usuario: {self._nombre} (ID: {self._id_usuario}) - {self.cantidad_libros_prestados} libros prestados"
    
    def __repr__(self) -> str:
        return f"Usuario(nombre='{self._nombre}', id_usuario='{self._id_usuario}')"


class Biblioteca:
    """
    Clase principal que gestiona la biblioteca digital.
    
    Utiliza:
    - Diccionario para almacenar libros (ISBN como clave)
    - Conjunto para IDs de usuarios únicos
    - Diccionario para almacenar usuarios
    """
    
    def __init__(self, nombre_biblioteca: str = "Biblioteca Digital"):
        """
        Inicializa la biblioteca.
        
        Args:
            nombre_biblioteca (str): Nombre de la biblioteca
        """
        self._nombre = nombre_biblioteca
        # Diccionario: ISBN -> Libro (para búsquedas eficientes)
        self._libros: Dict[str, Libro] = {}
        # Diccionario: ID_Usuario -> Usuario
        self._usuarios: Dict[str, Usuario] = {}
        # Conjunto para IDs únicos de usuarios
        self._ids_usuarios: Set[str] = set()
        # Estadísticas
        self._total_prestamos = 0
        self._fecha_creacion = datetime.now()
    
    # ==================== GESTIÓN DE LIBROS ====================
    
    def añadir_libro(self, libro: Libro) -> bool:
        """
        Añade un libro a la biblioteca.
        
        Args:
            libro (Libro): Libro a añadir
            
        Returns:
            bool: True si se añadió correctamente, False si ya existía
        """
        if libro.isbn not in self._libros:
            self._libros[libro.isbn] = libro
            print(f"✅ Libro añadido: {libro}")
            return True
        else:
            print(f"❌ El libro con ISBN {libro.isbn} ya existe en la biblioteca")
            return False
    
    def quitar_libro(self, isbn: str) -> bool:
        """
        Quita un libro de la biblioteca.
        
        Args:
            isbn (str): ISBN del libro a quitar
            
        Returns:
            bool: True si se quitó correctamente
        """
        if isbn in self._libros:
            libro = self._libros[isbn]
            if libro.disponible:
                del self._libros[isbn]
                print(f"✅ Libro eliminado: {libro.titulo}")
                return True
            else:
                print(f"❌ No se puede eliminar '{libro.titulo}' porque está prestado")
                return False
        else:
            print(f"❌ No se encontró libro con ISBN: {isbn}")
            return False
    
    def buscar_libro_por_isbn(self, isbn: str) -> Optional[Libro]:
        """Busca un libro por ISBN."""
        return self._libros.get(isbn)
    
    def buscar_libros_por_titulo(self, titulo: str) -> List[Libro]:
        """
        Busca libros por título (búsqueda parcial, insensible a mayúsculas).
        
        Args:
            titulo (str): Título o parte del título a buscar
            
        Returns:
            List[Libro]: Lista de libros que coinciden
        """
        titulo_lower = titulo.lower()
        return [libro for libro in self._libros.values() 
                if titulo_lower in libro.titulo.lower()]
    
    def buscar_libros_por_autor(self, autor: str) -> List[Libro]:
        """
        Busca libros por autor (búsqueda parcial, insensible a mayúsculas).
        
        Args:
            autor (str): Autor o parte del nombre del autor
            
        Returns:
            List[Libro]: Lista de libros que coinciden
        """
        autor_lower = autor.lower()
        return [libro for libro in self._libros.values() 
                if autor_lower in libro.autor.lower()]
    
    def buscar_libros_por_categoria(self, categoria: str) -> List[Libro]:
        """
        Busca libros por categoría.
        
        Args:
            categoria (str): Categoría a buscar
            
        Returns:
            List[Libro]: Lista de libros de esa categoría
        """
        categoria_lower = categoria.lower()
        return [libro for libro in self._libros.values() 
                if categoria_lower == libro.categoria.lower()]
    
    def obtener_todos_los_libros(self) -> List[Libro]:
        """Obtiene todos los libros de la biblioteca."""
        return list(self._libros.values())
    
    def obtener_libros_disponibles(self) -> List[Libro]:
        """Obtiene todos los libros disponibles."""
        return [libro for libro in self._libros.values() if libro.disponible]
    
    def obtener_libros_prestados(self) -> List[Libro]:
        """Obtiene todos los libros prestados."""
        return [libro for libro in self._libros.values() if not libro.disponible]
    
    # ==================== GESTIÓN DE USUARIOS ====================
    
    def registrar_usuario(self, usuario: Usuario) -> bool:
        """
        Registra un nuevo usuario en la biblioteca.
        
        Args:
            usuario (Usuario): Usuario a registrar
            
        Returns:
            bool: True si se registró correctamente
        """
        if usuario.id_usuario not in self._ids_usuarios:
            self._usuarios[usuario.id_usuario] = usuario
            self._ids_usuarios.add(usuario.id_usuario)
            print(f"✅ Usuario registrado: {usuario}")
            return True
        else:
            print(f"❌ El usuario con ID {usuario.id_usuario} ya existe")
            return False
    
    def dar_de_baja_usuario(self, id_usuario: str) -> bool:
        """
        Da de baja a un usuario.
        
        Args:
            id_usuario (str): ID del usuario a dar de baja
            
        Returns:
            bool: True si se dio de baja correctamente
        """
        if id_usuario in self._ids_usuarios:
            usuario = self._usuarios[id_usuario]
            if usuario.cantidad_libros_prestados == 0:
                del self._usuarios[id_usuario]
                self._ids_usuarios.remove(id_usuario)
                print(f"✅ Usuario dado de baja: {usuario.nombre}")
                return True
            else:
                print(f"❌ No se puede dar de baja a {usuario.nombre} porque tiene {usuario.cantidad_libros_prestados} libros prestados")
                return False
        else:
            print(f"❌ No se encontró usuario con ID: {id_usuario}")
            return False
    
    def buscar_usuario(self, id_usuario: str) -> Optional[Usuario]:
        """Busca un usuario por ID."""
        return self._usuarios.get(id_usuario)
    
    def obtener_todos_los_usuarios(self) -> List[Usuario]:
        """Obtiene todos los usuarios registrados."""
        return list(self._usuarios.values())
    
    # ==================== GESTIÓN DE PRÉSTAMOS ====================
    
    def prestar_libro(self, isbn: str, id_usuario: str) -> bool:
        """
        Presta un libro a un usuario.
        
        Args:
            isbn (str): ISBN del libro a prestar
            id_usuario (str): ID del usuario
            
        Returns:
            bool: True si se prestó correctamente
        """
        # Verificar que el libro existe
        libro = self.buscar_libro_por_isbn(isbn)
        if not libro:
            print(f"❌ No se encontró libro con ISBN: {isbn}")
            return False
        
        # Verificar que el usuario existe
        usuario = self.buscar_usuario(id_usuario)
        if not usuario:
            print(f"❌ No se encontró usuario con ID: {id_usuario}")
            return False
        
        # Verificar que el libro está disponible
        if not libro.disponible:
            print(f"❌ El libro '{libro.titulo}' no está disponible")
            return False
        
        # Realizar el préstamo
        if libro.prestar() and usuario.prestar_libro(isbn):
            self._total_prestamos += 1
            print(f"✅ Libro prestado: '{libro.titulo}' a {usuario.nombre}")
            return True
        else:
            print(f"❌ Error al prestar el libro")
            return False
    
    def devolver_libro(self, isbn: str, id_usuario: str) -> bool:
        """
        Devuelve un libro prestado.
        
        Args:
            isbn (str): ISBN del libro a devolver
            id_usuario (str): ID del usuario
            
        Returns:
            bool: True si se devolvió correctamente
        """
        # Verificar que el libro existe
        libro = self.buscar_libro_por_isbn(isbn)
        if not libro:
            print(f"❌ No se encontró libro con ISBN: {isbn}")
            return False
        
        # Verificar que el usuario existe
        usuario = self.buscar_usuario(id_usuario)
        if not usuario:
            print(f"❌ No se encontró usuario con ID: {id_usuario}")
            return False
        
        # Verificar que el usuario tiene el libro
        if not usuario.tiene_libro(isbn):
            print(f"❌ El usuario {usuario.nombre} no tiene prestado el libro '{libro.titulo}'")
            return False
        
        # Realizar la devolución
        if libro.devolver() and usuario.devolver_libro(isbn):
            print(f"✅ Libro devuelto: '{libro.titulo}' por {usuario.nombre}")
            return True
        else:
            print(f"❌ Error al devolver el libro")
            return False
    
    def listar_libros_prestados_usuario(self, id_usuario: str) -> List[Libro]:
        """
        Lista todos los libros prestados a un usuario específico.
        
        Args:
            id_usuario (str): ID del usuario
            
        Returns:
            List[Libro]: Lista de libros prestados al usuario
        """
        usuario = self.buscar_usuario(id_usuario)
        if not usuario:
            return []
        
        libros_prestados = []
        for isbn in usuario.libros_prestados:
            libro = self.buscar_libro_por_isbn(isbn)
            if libro:
                libros_prestados.append(libro)
        
        return libros_prestados
    
    # ==================== PERSISTENCIA DE DATOS ====================
    
    def guardar_datos(self, archivo: str = "biblioteca_data.json") -> bool:
        """
        Guarda los datos de la biblioteca en un archivo JSON.
        
        Args:
            archivo (str): Nombre del archivo donde guardar
            
        Returns:
            bool: True si se guardó correctamente
        """
        try:
            datos = {
                'nombre_biblioteca': self._nombre,
                'fecha_creacion': self._fecha_creacion.isoformat(),
                'total_prestamos': self._total_prestamos,
                'libros': {isbn: libro.to_dict() for isbn, libro in self._libros.items()},
                'usuarios': {id_user: usuario.to_dict() for id_user, usuario in self._usuarios.items()}
            }
            
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Datos guardados en: {archivo}")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar datos: {e}")
            return False
    
    def cargar_datos(self, archivo: str = "biblioteca_data.json") -> bool:
        """
        Carga los datos de la biblioteca desde un archivo JSON.
        
        Args:
            archivo (str): Nombre del archivo de donde cargar
            
        Returns:
            bool: True si se cargó correctamente
        """
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Cargar información básica
            self._nombre = datos.get('nombre_biblioteca', 'Biblioteca Digital')
            self._fecha_creacion = datetime.fromisoformat(datos.get('fecha_creacion', datetime.now().isoformat()))
            self._total_prestamos = datos.get('total_prestamos', 0)
            
            # Cargar libros
            self._libros = {}
            for isbn, libro_data in datos.get('libros', {}).items():
                self._libros[isbn] = Libro.from_dict(libro_data)
            
            # Cargar usuarios
            self._usuarios = {}
            self._ids_usuarios = set()
            for id_usuario, usuario_data in datos.get('usuarios', {}).items():
                usuario = Usuario.from_dict(usuario_data)
                self._usuarios[id_usuario] = usuario
                self._ids_usuarios.add(id_usuario)
            
            print(f"✅ Datos cargados desde: {archivo}")
            print(f"📚 Libros cargados: {len(self._libros)}")
            print(f"👥 Usuarios cargados: {len(self._usuarios)}")
            return True
            
        except FileNotFoundError:
            print(f"📄 Archivo {archivo} no encontrado. Iniciando con biblioteca vacía.")
            return False
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            return False
    
    # ==================== REPORTES Y ESTADÍSTICAS ====================
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas generales de la biblioteca."""
        print(f"\n📊 ESTADÍSTICAS DE {self._nombre.upper()}")
        print("=" * 50)
        print(f"📚 Total de libros: {len(self._libros)}")
        print(f"✅ Libros disponibles: {len(self.obtener_libros_disponibles())}")
        print(f"📤 Libros prestados: {len(self.obtener_libros_prestados())}")
        print(f"👥 Usuarios registrados: {len(self._usuarios)}")
        print(f"📊 Total de préstamos realizados: {self._total_prestamos}")
        print(f"📅 Biblioteca creada: {self._fecha_creacion.strftime('%d/%m/%Y %H:%M')}")
        
        # Categorías más populares
        categorias = {}
        for libro in self._libros.values():
            cat = libro.categoria
            categorias[cat] = categorias.get(cat, 0) + 1
        
        if categorias:
            print(f"\n📚 LIBROS POR CATEGORÍA:")
            for categoria, cantidad in sorted(categorias.items(), key=lambda x: x[1], reverse=True):
                print(f"  • {categoria}: {cantidad} libros")
    
    def generar_reporte_usuarios(self):
        """Genera un reporte detallado de usuarios."""
        print(f"\n👥 REPORTE DE USUARIOS")
        print("=" * 50)
        
        if not self._usuarios:
            print("No hay usuarios registrados.")
            return
        
        for usuario in self._usuarios.values():
            print(f"\n• {usuario}")
            if usuario.cantidad_libros_prestados > 0:
                print("  Libros prestados:")
                for libro in self.listar_libros_prestados_usuario(usuario.id_usuario):
                    print(f"    - {libro.titulo} ({libro.autor})")
            else:
                print("  Sin libros prestados actualmente.")
    
    def __str__(self) -> str:
        return f"{self._nombre} - {len(self._libros)} libros, {len(self._usuarios)} usuarios"


# ==================== SISTEMA DE MENÚ INTERACTIVO ====================

class MenuBiblioteca:
    """Clase para manejar el menú interactivo de la biblioteca."""
    
    def __init__(self, biblioteca: Biblioteca):
        self.biblioteca = biblioteca
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal."""
        print(f"\n🏛️  {self.biblioteca._nombre.upper()}")
        print("=" * 50)
        print("1.  📚 Gestión de Libros")
        print("2.  👥 Gestión de Usuarios") 
        print("3.  📤 Gestión de Préstamos")
        print("4.  🔍 Búsquedas")
        print("5.  📊 Reportes y Estadísticas")
        print("6.  💾 Guardar Datos")
        print("7.  📁 Cargar Datos")
        print("0.  🚪 Salir")
        print("=" * 50)
    
    def menu_gestion_libros(self):
        """Submenú para gestión de libros."""
        while True:
            print(f"\n📚 GESTIÓN DE LIBROS")
            print("-" * 30)
            print("1. ➕ Añadir libro")
            print("2. ➖ Quitar libro")
            print("3. 📋 Listar todos los libros")
            print("4. ✅ Listar libros disponibles")
            print("5. 📤 Listar libros prestados")
            print("0. ⬅️  Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.añadir_libro()
            elif opcion == "2":
                self.quitar_libro()
            elif opcion == "3":
                self.listar_libros(self.biblioteca.obtener_todos_los_libros(), "TODOS LOS LIBROS")
            elif opcion == "4":
                self.listar_libros(self.biblioteca.obtener_libros_disponibles(), "LIBROS DISPONIBLES")
            elif opcion == "5":
                self.listar_libros(self.biblioteca.obtener_libros_prestados(), "LIBROS PRESTADOS")
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
    
    def menu_gestion_usuarios(self):
        """Submenú para gestión de usuarios."""
        while True:
            print(f"\n👥 GESTIÓN DE USUARIOS")
            print("-" * 30)
            print("1. ➕ Registrar usuario")
            print("2. ➖ Dar de baja usuario")
            print("3. 📋 Listar todos los usuarios")
            print("4. 🔍 Buscar usuario")
            print("0. ⬅️  Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.registrar_usuario()
            elif opcion == "2":
                self.dar_baja_usuario()
            elif opcion == "3":
                self.listar_usuarios()
            elif opcion == "4":
                self.buscar_usuario()
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
    
    def menu_gestion_prestamos(self):
        """Submenú para gestión de préstamos."""
        while True:
            print(f"\n📤 GESTIÓN DE PRÉSTAMOS")
            print("-" * 30)
            print("1. 📤 Prestar libro")
            print("2. 📥 Devolver libro")
            print("3. 📋 Listar préstamos de usuario")
            print("0. ⬅️  Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.prestar_libro()
            elif opcion == "2":
                self.devolver_libro()
            elif opcion == "3":
                self.listar_prestamos_usuario()
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
    
    def menu_busquedas(self):
        """Submenú para búsquedas."""
        while True:
            print(f"\n🔍 BÚSQUEDAS")
            print("-" * 30)
            print("1. 📖 Buscar por título")
            print("2. ✍️  Buscar por autor")
            print("3. 📚 Buscar por categoría")
            print("4. 🔢 Buscar por ISBN")
            print("0. ⬅️  Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.buscar_por_titulo()
            elif opcion == "2":
                self.buscar_por_autor()
            elif opcion == "3":
                self.buscar_por_categoria()
            elif opcion == "4":
                self.buscar_por_isbn()
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
    
    def menu_reportes(self):
        """Submenú para reportes y estadísticas."""
        while True:
            print(f"\n📊 REPORTES Y ESTADÍSTICAS")
            print("-" * 30)
            print("1. 📊 Estadísticas generales")
            print("2. 👥 Reporte de usuarios")
            print("0. ⬅️  Volver al menú principal")
            
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.biblioteca.mostrar_estadisticas()
            elif opcion == "2":
                self.biblioteca.generar_reporte_usuarios()
            elif opcion == "0":
                break
            else:
                print("❌ Opción no válida")
    
    # Métodos auxiliares
    def añadir_libro(self):
        """Interfaz para añadir un libro."""
        print("\n➕ AÑADIR NUEVO LIBRO")
        print("-" * 25)
        
        titulo = input("Título: ").strip()
        if not titulo:
            print("❌ El título no puede estar vacío")
            return
        
        autor = input("Autor: ").strip()
        if not autor:
            print("❌ El autor no puede estar vacío")
            return
        
        categoria = input("Categoría: ").strip()
        if not categoria:
            print("❌ La categoría no puede estar vacía")
            return
        
        isbn = input("ISBN: ").strip()
        if not isbn:
            print("❌ El ISBN no puede estar vacío")
            return
        
        libro = Libro(titulo, autor, categoria, isbn)
        self.biblioteca.añadir_libro(libro)
    
    def quitar_libro(self):
        """Interfaz para quitar un libro."""
        print("\n➖ QUITAR LIBRO")
        print("-" * 15)
        
        isbn = input("ISBN del libro a quitar: ").strip()
        if isbn:
            self.biblioteca.quitar_libro(isbn)
        else:
            print("❌ Debe proporcionar un ISBN")
    
    def listar_libros(self, libros: List[Libro], titulo: str):
        """Lista libros con formato."""
        print(f"\n📚 {titulo}")
        print("-" * len(titulo))
        
        if not libros:
            print("No hay libros para mostrar.")
            return
        
        for i, libro in enumerate(libros, 1):
            print(f"{i:2d}. {libro}")
    
    def registrar_usuario(self):
        """Interfaz para registrar un usuario."""
        print("\n➕ REGISTRAR NUEVO USUARIO")
        print("-" * 30)
        
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("❌ El nombre no puede estar vacío")
            return
        
        id_usuario = input("ID de usuario: ").strip()
        if not id_usuario:
            print("❌ El ID de usuario no puede estar vacío")
            return
        
        usuario = Usuario(nombre, id_usuario)
        self.biblioteca.registrar_usuario(usuario)
    
    def dar_baja_usuario(self):
        """Interfaz para dar de baja a un usuario."""
        print("\n➖ DAR DE BAJA USUARIO")
        print("-" * 25)
        
        id_usuario = input("ID del usuario: ").strip()
        if id_usuario:
            self.biblioteca.dar_de_baja_usuario(id_usuario)
        else:
            print("❌ Debe proporcionar un ID de usuario")
    
    def listar_usuarios(self):
        """Lista todos los usuarios."""
        usuarios = self.biblioteca.obtener_todos_los_usuarios()
        print(f"\n👥 TODOS LOS USUARIOS")
        print("-" * 20)
        
        if not usuarios:
            print("No hay usuarios registrados.")
            return
        
        for i, usuario in enumerate(usuarios, 1):
            print(f"{i:2d}. {usuario}")
    
    def buscar_usuario(self):
        """Interfaz para buscar un usuario."""
        print("\n🔍 BUSCAR USUARIO")
        print("-" * 17)
        
        id_usuario = input("ID del usuario: ").strip()
        if not id_usuario:
            print("❌ Debe proporcionar un ID de usuario")
            return
        
        usuario = self.biblioteca.buscar_usuario(id_usuario)
        if usuario:
            print(f"\n✅ Usuario encontrado:")
            print(f"   {usuario}")
            
            # Mostrar libros prestados
            libros_prestados = self.biblioteca.listar_libros_prestados_usuario(id_usuario)
            if libros_prestados:
                print(f"\n📚 Libros prestados:")
                for libro in libros_prestados:
                    print(f"   • {libro}")
            else:
                print("   Sin libros prestados actualmente.")
        else:
            print(f"❌ No se encontró usuario con ID: {id_usuario}")
    
    def prestar_libro(self):
        """Interfaz para prestar un libro."""
        print("\n📤 PRESTAR LIBRO")
        print("-" * 16)
        
        isbn = input("ISBN del libro: ").strip()
        if not isbn:
            print("❌ Debe proporcionar un ISBN")
            return
        
        id_usuario = input("ID del usuario: ").strip()
        if not id_usuario:
            print("❌ Debe proporcionar un ID de usuario")
            return
        
        self.biblioteca.prestar_libro(isbn, id_usuario)
    
    def devolver_libro(self):
        """Interfaz para devolver un libro."""
        print("\n📥 DEVOLVER LIBRO")
        print("-" * 17)
        
        isbn = input("ISBN del libro: ").strip()
        if not isbn:
            print("❌ Debe proporcionar un ISBN")
            return
        
        id_usuario = input("ID del usuario: ").strip()
        if not id_usuario:
            print("❌ Debe proporcionar un ID de usuario")
            return
        
        self.biblioteca.devolver_libro(isbn, id_usuario)
    
    def listar_prestamos_usuario(self):
        """Lista los préstamos de un usuario específico."""
        print("\n📋 PRÉSTAMOS DE USUARIO")
        print("-" * 23)
        
        id_usuario = input("ID del usuario: ").strip()
        if not id_usuario:
            print("❌ Debe proporcionar un ID de usuario")
            return
        
        usuario = self.biblioteca.buscar_usuario(id_usuario)
        if not usuario:
            print(f"❌ No se encontró usuario con ID: {id_usuario}")
            return
        
        libros_prestados = self.biblioteca.listar_libros_prestados_usuario(id_usuario)
        print(f"\n📚 Libros prestados a {usuario.nombre}:")
        
        if libros_prestados:
            for i, libro in enumerate(libros_prestados, 1):
                print(f"{i:2d}. {libro}")
        else:
            print("   Sin libros prestados actualmente.")
    
    def buscar_por_titulo(self):
        """Busca libros por título."""
        print("\n🔍 BUSCAR POR TÍTULO")
        print("-" * 21)
        
        titulo = input("Título (o parte del título): ").strip()
        if not titulo:
            print("❌ Debe proporcionar un título")
            return
        
        libros = self.biblioteca.buscar_libros_por_titulo(titulo)
        self.listar_libros(libros, f"RESULTADOS PARA: '{titulo}'")
    
    def buscar_por_autor(self):
        """Busca libros por autor."""
        print("\n🔍 BUSCAR POR AUTOR")
        print("-" * 20)
        
        autor = input("Autor (o parte del nombre): ").strip()
        if not autor:
            print("❌ Debe proporcionar un autor")
            return
        
        libros = self.biblioteca.buscar_libros_por_autor(autor)
        self.listar_libros(libros, f"RESULTADOS PARA: '{autor}'")
    
    def buscar_por_categoria(self):
        """Busca libros por categoría."""
        print("\n🔍 BUSCAR POR CATEGORÍA")
        print("-" * 23)
        
        categoria = input("Categoría: ").strip()
        if not categoria:
            print("❌ Debe proporcionar una categoría")
            return
        
        libros = self.biblioteca.buscar_libros_por_categoria(categoria)
        self.listar_libros(libros, f"CATEGORÍA: '{categoria}'")
    
    def buscar_por_isbn(self):
        """Busca un libro por ISBN."""
        print("\n🔍 BUSCAR POR ISBN")
        print("-" * 18)
        
        isbn = input("ISBN: ").strip()
        if not isbn:
            print("❌ Debe proporcionar un ISBN")
            return
        
        libro = self.biblioteca.buscar_libro_por_isbn(isbn)
        if libro:
            print(f"\n✅ Libro encontrado:")
            print(f"   {libro}")
        else:
            print(f"❌ No se encontró libro con ISBN: {isbn}")
    
    def ejecutar(self):
        """Ejecuta el menú principal."""
        # Intentar cargar datos al inicio
        self.biblioteca.cargar_datos()
        
        while True:
            self.mostrar_menu_principal()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self.menu_gestion_libros()
            elif opcion == "2":
                self.menu_gestion_usuarios()
            elif opcion == "3":
                self.menu_gestion_prestamos()
            elif opcion == "4":
                self.menu_busquedas()
            elif opcion == "5":
                self.menu_reportes()
            elif opcion == "6":
                self.biblioteca.guardar_datos()
            elif opcion == "7":
                archivo = input("Nombre del archivo (presione Enter para 'biblioteca_data.json'): ").strip()
                if not archivo:
                    archivo = "biblioteca_data.json"
                self.biblioteca.cargar_datos(archivo)
            elif opcion == "0":
                print("\n💾 Guardando datos antes de salir...")
                self.biblioteca.guardar_datos()
                print("👋 ¡Gracias por usar la Biblioteca Digital!")
                break
            else:
                print("❌ Opción no válida")


# ==================== FUNCIÓN PRINCIPAL Y EJEMPLOS ====================

def cargar_datos_ejemplo(biblioteca: Biblioteca):
    """Carga datos de ejemplo en la biblioteca."""
    print("📚 Cargando datos de ejemplo...")
    
    # Crear libros de ejemplo
    libros_ejemplo = [
        Libro("Cien años de soledad", "Gabriel García Márquez", "Ficción", "978-84-376-0494-7"),
        Libro("1984", "George Orwell", "Distopía", "978-84-376-0495-4"),
        Libro("El Quijote", "Miguel de Cervantes", "Clásico", "978-84-376-0496-1"),
        Libro("Programación en Python", "John Smith", "Tecnología", "978-84-376-0497-8"),
        Libro("Historia del Arte", "María González", "Arte", "978-84-376-0498-5"),
        Libro("Física Cuántica", "Albert Einstein", "Ciencia", "978-84-376-0499-2"),
        Libro("El Principito", "Antoine de Saint-Exupéry", "Infantil", "978-84-376-0500-5"),
        Libro("Cómo ganar amigos", "Dale Carnegie", "Autoayuda", "978-84-376-0501-2"),
    ]
    
    for libro in libros_ejemplo:
        biblioteca.añadir_libro(libro)
    
    # Crear usuarios de ejemplo
    usuarios_ejemplo = [
        Usuario("Juan Pérez", "U001"),
        Usuario("María García", "U002"),
        Usuario("Carlos López", "U003"),
        Usuario("Ana Martínez", "U004"),
    ]
    
    for usuario in usuarios_ejemplo:
        biblioteca.registrar_usuario(usuario)
    
    # Realizar algunos préstamos de ejemplo
    biblioteca.prestar_libro("978-84-376-0494-7", "U001")  # Cien años de soledad a Juan
    biblioteca.prestar_libro("978-84-376-0495-4", "U002")  # 1984 a María
    biblioteca.prestar_libro("978-84-376-0497-8", "U001")  # Programación en Python a Juan
    
    print("✅ Datos de ejemplo cargados correctamente")


def demo_sistema():
    """Función de demostración del sistema."""
    print("🎯 DEMOSTRACIÓN DEL SISTEMA DE BIBLIOTECA DIGITAL")
    print("=" * 60)
    
    # Crear biblioteca
    biblioteca = Biblioteca("Biblioteca Central Universitaria")
    
    # Cargar datos de ejemplo
    cargar_datos_ejemplo(biblioteca)
    
    # Mostrar estadísticas
    biblioteca.mostrar_estadisticas()
    
    # Demostrar búsquedas
    print(f"\n🔍 DEMOSTRANDO BÚSQUEDAS:")
    print("-" * 30)
    
    print("📖 Búsqueda por título 'El':")
    libros = biblioteca.buscar_libros_por_titulo("El")
    for libro in libros:
        print(f"  • {libro}")
    
    print(f"\n✍️  Búsqueda por autor 'García':")
    libros = biblioteca.buscar_libros_por_autor("García")
    for libro in libros:
        print(f"  • {libro}")
    
    print(f"\n📚 Libros de categoría 'Ficción':")
    libros = biblioteca.buscar_libros_por_categoria("Ficción")
    for libro in libros:
        print(f"  • {libro}")
    
    # Mostrar reportes
    biblioteca.generar_reporte_usuarios()
    
    # Guardar datos
    biblioteca.guardar_datos("demo_biblioteca.json")
    
    print(f"\n✅ Demostración completada")


def main():
    """Función principal del programa."""
    print("🏛️  SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL")
    print("=" * 50)
    print("Desarrollado con Python - Programación Orientada a Objetos")
    print("Autor: Norman Eras")
    print("=" * 50)
    
    # Crear biblioteca
    biblioteca = Biblioteca("Biblioteca Digital POO")
    
    # Preguntar si quiere cargar datos de ejemplo
    respuesta = input("\n¿Desea cargar datos de ejemplo? (s/n): ").strip().lower()
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        cargar_datos_ejemplo(biblioteca)
    
    # Crear y ejecutar el menú
    menu = MenuBiblioteca(biblioteca)
    menu.ejecutar()


if __name__ == "__main__":
    # Ejecutar demostración o programa principal
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_sistema()
    else:
        main()