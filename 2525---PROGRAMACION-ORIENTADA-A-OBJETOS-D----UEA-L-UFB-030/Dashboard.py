import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class DashboardPOO:
    """
    Dashboard interactivo para gestión de proyectos POO
    Autor: Norman Eras
    Fecha: Julio 2025
    """
    
    def __init__(self):
        self.ruta_base = os.path.dirname(__file__)
        self.workspace_root = os.path.dirname(self.ruta_base)
        self.archivos_recientes = []
        self.favoritos = []
    
    def limpiar_pantalla(self):
        """Limpia la pantalla del terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_cabecera(self):
        """Muestra la cabecera del dashboard"""
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print("=" * 80)
        print("    DASHBOARD POO - NORMAN ERAS    ")
        print("    Programación Orientada a Objetos - Segundo Semestre")
        print(f"    {fecha_actual}")
        print("=" * 80)
    
    def obtener_archivos_python(self):
        """Obtiene todos los archivos Python del proyecto organizados por categorías"""
        archivos = {
            'UNIDAD 1': {
                'Técnicas de Programación': [],
                'Programación Tradicional vs POO': [],
                'Características de la POO': []
            },
            'UNIDAD 2': {
                'Tipos de Datos e Identificadores': [],
                'Clases, Objetos, Herencia, Encapsulamiento y Polimorfismo': [],
                'Constructores y Destructores': []
            },
            'EJEMPLOS MUNDO REAL': [],
            'ARCHIVOS RAÍZ': []
        }
        
        # Archivos de la raíz del workspace
        workspace_root = r'c:\Users\Norman\Desktop\UNIVERSIDAD-DOCUMENTOS\SEGUNDO-SEMESTRE\PROGRAMACION-ORIENTADA-OBJETOS\PROYECTOS\POO-NORMAN-ERAS'
        archivos_raiz = [
            'conceptos-poo.py', 
            'constructores.py', 
            'poo.py', 
            'tipos-datos.py', 
            'tradicional.py',
            'gestion-inventarios-mejorado.py',
            'test_inventario_mejorado.py'
        ]
        
        for archivo in archivos_raiz:
            ruta_completa = os.path.join(workspace_root, archivo)
            if os.path.exists(ruta_completa):
                archivos['ARCHIVOS RAÍZ'].append((archivo, ruta_completa))
        
        # Ejemplos del mundo real
        ejemplos_dir = r'c:\Users\Norman\Desktop\UNIVERSIDAD-DOCUMENTOS\SEGUNDO-SEMESTRE\PROGRAMACION-ORIENTADA-OBJETOS\PROYECTOS\POO-NORMAN-ERAS\EjemplosMundoReal_POO'
        if os.path.exists(ejemplos_dir):
            for archivo in os.listdir(ejemplos_dir):
                if archivo.endswith('.py'):
                    ruta_completa = os.path.join(ejemplos_dir, archivo)
                    archivos['EJEMPLOS MUNDO REAL'].append((archivo, ruta_completa))
        
        # UNIDAD 1
        unidad1_dir = r'c:\Users\Norman\Desktop\UNIVERSIDAD-DOCUMENTOS\SEGUNDO-SEMESTRE\PROGRAMACION-ORIENTADA-OBJETOS\PROYECTOS\POO-NORMAN-ERAS\2525---PROGRAMACION-ORIENTADA-A-OBJETOS-D----UEA-L-UFB-030\UNIDAD 1'
        if os.path.exists(unidad1_dir):
            # Técnicas de Programación
            tecnicas_dir = r'c:\Users\Norman\Desktop\UNIVERSIDAD-DOCUMENTOS\SEGUNDO-SEMESTRE\PROGRAMACION-ORIENTADA-OBJETOS\PROYECTOS\POO-NORMAN-ERAS\2525---PROGRAMACION-ORIENTADA-A-OBJETOS-D----UEA-L-UFB-030\UNIDAD 1\1.2.-Tecnicas-de-Programacion'
            if os.path.exists(tecnicas_dir):
                for root, dirs, files in os.walk(tecnicas_dir):
                    for file in files:
                        if file.endswith('.py'):
                            ruta_completa = os.path.join(root, file)
                            archivos['UNIDAD 1']['Técnicas de Programación'].append((file, ruta_completa))
            
            # Programación Tradicional vs POO
            tradicional_dir = r'c:\Users\Norman\Desktop\UNIVERSIDAD-DOCUMENTOS\SEGUNDO-SEMESTRE\PROGRAMACION-ORIENTADA-OBJETOS\PROYECTOS\POO-NORMAN-ERAS\2525---PROGRAMACION-ORIENTADA-A-OBJETOS-D----UEA-L-UFB-030\UNIDAD 1\2.1.Programacion-tradicional-frente-a-POO'
            if os.path.exists(tradicional_dir):
                for root, dirs, files in os.walk(tradicional_dir):
                    for file in files:
                        if file.endswith('.py'):
                            ruta_completa = os.path.join(root, file)
                            archivos['UNIDAD 1']['Programación Tradicional vs POO'].append((file, ruta_completa))
            
            # Características de la POO
            caracteristicas_dir = r'c:\Users\Norman\Desktop\UNIVERSIDAD-DOCUMENTOS\SEGUNDO-SEMESTRE\PROGRAMACION-ORIENTADA-OBJETOS\PROYECTOS\POO-NORMAN-ERAS\2525---PROGRAMACION-ORIENTADA-A-OBJETOS-D----UEA-L-UFB-030\UNIDAD 1\2.2.Caracteristicas-de-la-POO'
            if os.path.exists(caracteristicas_dir):
                for root, dirs, files in os.walk(caracteristicas_dir):
                    for file in files:
                        if file.endswith('.py'):
                            ruta_completa = os.path.join(root, file)
                            archivos['UNIDAD 1']['Características de la POO'].append((file, ruta_completa))
        
        # UNIDAD 2
        unidad2_dir = r'c:\Users\Norman\Desktop\UNIVERSIDAD-DOCUMENTOS\SEGUNDO-SEMESTRE\PROGRAMACION-ORIENTADA-OBJETOS\PROYECTOS\POO-NORMAN-ERAS\2525---PROGRAMACION-ORIENTADA-A-OBJETOS-D----UEA-L-UFB-030\UNIDAD 2'
        if os.path.exists(unidad2_dir):
            # Tipos de Datos
            tipos_dir = r'c:\Users\Norman\Desktop\UNIVERSIDAD-DOCUMENTOS\SEGUNDO-SEMESTRE\PROGRAMACION-ORIENTADA-OBJETOS\PROYECTOS\POO-NORMAN-ERAS\2525---PROGRAMACION-ORIENTADA-A-OBJETOS-D----UEA-L-UFB-030\UNIDAD 2\1.1.Tipos-de-Datos-e-Identificadores'
            if os.path.exists(tipos_dir):
                for root, dirs, files in os.walk(tipos_dir):
                    for file in files:
                        if file.endswith('.py'):
                            ruta_completa = os.path.join(root, file)
                            archivos['UNIDAD 2']['Tipos de Datos e Identificadores'].append((file, ruta_completa))
            
            # Clases, Objetos, etc.
            clases_dir = r'c:\Users\Norman\Desktop\UNIVERSIDAD-DOCUMENTOS\SEGUNDO-SEMESTRE\PROGRAMACION-ORIENTADA-OBJETOS\PROYECTOS\POO-NORMAN-ERAS\2525---PROGRAMACION-ORIENTADA-A-OBJETOS-D----UEA-L-UFB-030\UNIDAD 2\1.2.Clases,Objetos,Herencia,Encapsulamiento-y-Polimorfismo'
            if os.path.exists(clases_dir):
                for root, dirs, files in os.walk(clases_dir):
                    for file in files:
                        if file.endswith('.py'):
                            ruta_completa = os.path.join(root, file)
                            archivos['UNIDAD 2']['Clases, Objetos, Herencia, Encapsulamiento y Polimorfismo'].append((file, ruta_completa))
            
            # Constructores y Destructores
            constructores_dir = r'c:\Users\Norman\Desktop\UNIVERSIDAD-DOCUMENTOS\SEGUNDO-SEMESTRE\PROGRAMACION-ORIENTADA-OBJETOS\PROYECTOS\POO-NORMAN-ERAS\2525---PROGRAMACION-ORIENTADA-A-OBJETOS-D----UEA-L-UFB-030\UNIDAD 2\2.1.Constructores-y-Destructores'
            if os.path.exists(constructores_dir):
                for root, dirs, files in os.walk(constructores_dir):
                    for file in files:
                        if file.endswith('.py'):
                            ruta_completa = os.path.join(root, file)
                            archivos['UNIDAD 2']['Constructores y Destructores'].append((file, ruta_completa))
        
        return archivos
    
    def mostrar_codigo(self, ruta_script):
        """Muestra el código de un archivo con formato mejorado"""
        try:
            with open(ruta_script, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
                nombre_archivo = os.path.basename(ruta_script)
                
                print("\n" + "─" * 80)
                print(f" ARCHIVO: {nombre_archivo}")
                print(f" RUTA: {ruta_script}")
                print("─" * 80)
                
                # Numeración de líneas
                lineas = contenido.split('\n')
                for i, linea in enumerate(lineas, 1):
                    print(f"{i:3d}: {linea}")
                
                print("─" * 80)
                
                # Agregar a archivos recientes
                if ruta_script not in self.archivos_recientes:
                    self.archivos_recientes.insert(0, ruta_script)
                    if len(self.archivos_recientes) > 5:
                        self.archivos_recientes.pop()
                
        except FileNotFoundError:
            print(f"ERROR: El archivo no se encontró: {ruta_script}")
        except UnicodeDecodeError:
            try:
                with open(ruta_script, 'r', encoding='latin-1') as archivo:
                    contenido = archivo.read()
                    print("AVISO: Archivo leído con codificación latin-1")
                    print(contenido)
            except Exception as e:
                print(f"ERROR: Error de codificación: {e}")
        except Exception as e:
            print(f"ERROR: Error al leer el archivo: {e}")
    
    def ejecutar_archivo(self, ruta_script):
        """Ejecuta un archivo Python"""
        try:
            print(f"\nEjecutando: {os.path.basename(ruta_script)}")
            print("─" * 60)
            
            # Cambiar al directorio del archivo para ejecutarlo correctamente
            directorio_archivo = os.path.dirname(ruta_script)
            resultado = subprocess.run([sys.executable, ruta_script], 
                                     cwd=directorio_archivo,
                                     capture_output=False, 
                                     text=True)
            
            print("─" * 60)
            if resultado.returncode == 0:
                print("EXITO: Ejecución completada exitosamente")
            else:
                print(f"ERROR: Error en la ejecución (código: {resultado.returncode})")
                
        except Exception as e:
            print(f"ERROR: Error al ejecutar el archivo: {e}")
    
    def mostrar_menu_archivos(self, categoria, subcategoria=None):
        """Muestra el menú de archivos para una categoría específica"""
        archivos = self.obtener_archivos_python()
        
        if subcategoria:
            archivos_mostrar = archivos[categoria][subcategoria]
            titulo = f"{categoria} - {subcategoria}"
        else:
            archivos_mostrar = archivos[categoria]
            titulo = categoria
        
        while True:
            self.limpiar_pantalla()
            self.mostrar_cabecera()
            
            print(f"\n {titulo}")
            print("─" * 50)
            
            if not archivos_mostrar:
                print("AVISO: No hay archivos disponibles en esta categoría")
                input("\nPresiona Enter para continuar...")
                return
            
            for i, (nombre, ruta) in enumerate(archivos_mostrar, 1):
                print(f"{i:2d}. {nombre}")
            
            print("\nOpciones:")
            print("V + número - Ver código")
            print("E + número - Ejecutar archivo")
            print("0 - Volver al menú principal")
            
            eleccion = input("\nSelecciona una opción: ").strip()
            
            if eleccion == '0':
                break
            elif eleccion.upper().startswith('V') and len(eleccion) > 1:
                try:
                    num = int(eleccion[1:]) - 1
                    if 0 <= num < len(archivos_mostrar):
                        self.mostrar_codigo(archivos_mostrar[num][1])
                        input("\nPresiona Enter para continuar...")
                    else:
                        print("ERROR: Número inválido")
                        input("\nPresiona Enter para continuar...")
                except ValueError:
                    print("ERROR: Formato inválido")
                    input("\nPresiona Enter para continuar...")
            elif eleccion.upper().startswith('E') and len(eleccion) > 1:
                try:
                    num = int(eleccion[1:]) - 1
                    if 0 <= num < len(archivos_mostrar):
                        self.ejecutar_archivo(archivos_mostrar[num][1])
                        input("\nPresiona Enter para continuar...")
                    else:
                        print("ERROR: Número inválido")
                        input("\nPresiona Enter para continuar...")
                except ValueError:
                    print("ERROR: Formato inválido")
                    input("\nPresiona Enter para continuar...")
            else:
                print("ERROR: Opción inválida")
                input("\nPresiona Enter para continuar...")
    
    def mostrar_submenu_unidad(self, unidad):
        """Muestra el submenú para una unidad específica"""
        archivos = self.obtener_archivos_python()
        subcategorias = archivos[unidad]
        
        while True:
            self.limpiar_pantalla()
            self.mostrar_cabecera()
            
            print(f"\n {unidad}")
            print("─" * 50)
            
            opciones = list(subcategorias.keys())
            for i, subcategoria in enumerate(opciones, 1):
                count = len(subcategorias[subcategoria])
                print(f"{i}. {subcategoria} ({count} archivos)")
            
            print("0. Volver al menú principal")
            
            eleccion = input("\nSelecciona una subcategoría: ").strip()
            
            if eleccion == '0':
                break
            elif eleccion.isdigit():
                num = int(eleccion) - 1
                if 0 <= num < len(opciones):
                    self.mostrar_menu_archivos(unidad, opciones[num])
                else:
                    print("ERROR: Opción inválida")
                    input("\nPresiona Enter para continuar...")
            else:
                print("ERROR: Opción inválida")
                input("\nPresiona Enter para continuar...")
    
    def mostrar_archivos_recientes(self):
        """Muestra los archivos recientemente visualizados"""
        if not self.archivos_recientes:
            print("AVISO: No hay archivos recientes")
            input("\nPresiona Enter para continuar...")
            return
        
        while True:
            self.limpiar_pantalla()
            self.mostrar_cabecera()
            
            print("\n ARCHIVOS RECIENTES")
            print("─"*50)
            
            for i, archivo in enumerate(self.archivos_recientes, 1):
                nombre = os.path.basename(archivo)
                print(f"{i}. {nombre}")
            
            print("\nOpciones:")
            print("V + número - Ver código")
            print("E + número - Ejecutar archivo")
            print("0 - Volver al menú principal")
            
            eleccion = input("\nSelecciona una opción: ").strip()
            
            if eleccion == '0':
                break
            elif eleccion.upper().startswith('V') and len(eleccion) > 1:
                try:
                    num = int(eleccion[1:]) - 1
                    if 0 <= num < len(self.archivos_recientes):
                        self.mostrar_codigo(self.archivos_recientes[num])
                        input("\nPresiona Enter para continuar...")
                    else:
                        print("ERROR: Número inválido")
                        input("\nPresiona Enter para continuar...")
                except ValueError:
                    print("ERROR: Formato inválido")
                    input("\nPresiona Enter para continuar...")
            elif eleccion.upper().startswith('E') and len(eleccion) > 1:
                try:
                    num = int(eleccion[1:]) - 1
                    if 0 <= num < len(self.archivos_recientes):
                        self.ejecutar_archivo(self.archivos_recientes[num])
                        input("\nPresiona Enter para continuar...")
                    else:
                        print("ERROR: Número inválido")
                        input("\nPresiona Enter para continuar...")
                except ValueError:
                    print("ERROR: Formato inválido")
                    input("\nPresiona Enter para continuar...")
            else:
                print("ERROR: Opción inválida")
                input("\nPresiona Enter para continuar...")
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas del proyecto"""
        archivos = self.obtener_archivos_python()
        
        self.limpiar_pantalla()
        self.mostrar_cabecera()
        
        print("\n ESTADÍSTICAS DEL PROYECTO")
        print("─"*50)
        
        total_archivos = 0
        total_lineas = 0
        
        for categoria, contenido in archivos.items():
            if isinstance(contenido, dict):
                count = sum(len(subcategoria) for subcategoria in contenido.values())
                print(f" {categoria}: {count} archivos")
                total_archivos += count
                
                for subcategoria, archivos_sub in contenido.items():
                    if archivos_sub:
                        print(f"   |- {subcategoria}: {len(archivos_sub)} archivos")
            else:
                count = len(contenido)
                print(f" {categoria}: {count} archivos")
                total_archivos += count
        
        # Contar líneas de código
        for categoria, contenido in archivos.items():
            if isinstance(contenido, dict):
                for subcategoria, archivos_sub in contenido.items():
                    for _, ruta in archivos_sub:
                        try:
                            with open(ruta, 'r', encoding='utf-8') as f:
                                total_lineas += len(f.readlines())
                        except:
                            try:
                                with open(ruta, 'r', encoding='latin-1') as f:
                                    total_lineas += len(f.readlines())
                            except:
                                pass
            else:
                for _, ruta in contenido:
                    try:
                        with open(ruta, 'r', encoding='utf-8') as f:
                            total_lineas += len(f.readlines())
                    except:
                        try:
                            with open(ruta, 'r', encoding='latin-1') as f:
                                total_lineas += len(f.readlines())
                        except:
                            pass
        
        print("\n RESUMEN TOTAL:")
        print(f"• Total de archivos Python: {total_archivos}")
        print(f"• Total de líneas de código: {total_lineas}")
        print(f"• Archivos recientes visitados: {len(self.archivos_recientes)}")
        
        input("\nPresiona Enter para continuar...")
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal del dashboard"""
        while True:
            self.limpiar_pantalla()
            self.mostrar_cabecera()
            
            print("\n MENÚ PRINCIPAL")
            print("─"*50)
            
            opciones = [
                ("UNIDAD 1", "Explorar archivos de la Unidad 1"),
                ("UNIDAD 2", "Explorar archivos de la Unidad 2"),
                ("EJEMPLOS MUNDO REAL", "Ver ejemplos prácticos de POO"),
                ("ARCHIVOS RAÍZ", "Ver archivos del directorio raíz"),
                ("ARCHIVOS RECIENTES", "Ver archivos visitados recientemente"),
                ("ESTADÍSTICAS", "Ver estadísticas del proyecto"),
                ("SALIR", "Cerrar el dashboard")
            ]
            
            for i, (titulo, descripcion) in enumerate(opciones, 1):
                print(f"{i}. {titulo}")
                print(f"   {descripcion}")
            
            eleccion = input(f"\nSelecciona una opción (1-{len(opciones)}): ").strip()
            
            if eleccion == '1':
                self.mostrar_submenu_unidad('UNIDAD 1')
            elif eleccion == '2':
                self.mostrar_submenu_unidad('UNIDAD 2')
            elif eleccion == '3':
                self.mostrar_menu_archivos('EJEMPLOS MUNDO REAL')
            elif eleccion == '4':
                self.mostrar_menu_archivos('ARCHIVOS RAÍZ')
            elif eleccion == '5':
                self.mostrar_archivos_recientes()
            elif eleccion == '6':
                self.mostrar_estadisticas()
            elif eleccion == '7':
                print("\n¡Gracias por usar el Dashboard POO!")
                break
            else:
                print(f"ERROR: Opción inválida. Por favor, selecciona un número del 1 al {len(opciones)}.")
                input("\nPresiona Enter para continuar...")


def main():
    """Función principal para ejecutar el dashboard"""
    try:
        dashboard = DashboardPOO()
        dashboard.mostrar_menu_principal()
    except KeyboardInterrupt:
        print("\n\nDashboard cerrado por el usuario")
    except Exception as e:
        print(f"\n\nERROR: Error inesperado: {e}")


if __name__ == "__main__":
    main()
