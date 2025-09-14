"""
Aplicación GUI Básica - Gestor de Tareas
========================================

Esta aplicación implementa una interfaz gráfica de usuario (GUI) básica utilizando Tkinter
que permite a los usuarios gestionar una lista de tareas de manera visual e interactiva.

Autor: Norman Eras
Fecha: Septiembre 2025
Materia: Programación Orientada a Objetos

Funcionalidades:
- Agregar nuevas tareas a la lista
- Mostrar tareas en una lista visual
- Eliminar tareas seleccionadas
- Limpiar el campo de entrada
- Limpiar toda la lista de tareas
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class GestorTareasGUI:
    """
    Clase principal para la aplicación GUI de gestión de tareas.
    
    Esta clase encapsula toda la lógica de la interfaz gráfica y manejo de eventos,
    siguiendo los principios de programación orientada a objetos.
    """
    
    def __init__(self):
        """
        Constructor de la clase. Inicializa la ventana principal y todos los componentes.
        """
        # Crear la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Gestor de Tareas - Aplicación GUI Básica")
        self.ventana.geometry("600x500")
        self.ventana.resizable(True, True)
        
        # Configurar el estilo y colores
        self.ventana.configure(bg='#f0f0f0')
        
        # Lista para almacenar las tareas (modelo de datos)
        self.tareas = []
        
        # Crear y configurar todos los componentes de la GUI
        self.crear_componentes()
        
        # Configurar la ventana para que se centre en la pantalla
        self.centrar_ventana()
    
    def centrar_ventana(self):
        """
        Centra la ventana en la pantalla del usuario.
        """
        # Actualizar la ventana para obtener las dimensiones reales
        self.ventana.update_idletasks()
        
        # Obtener dimensiones de la pantalla
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        
        # Obtener dimensiones de la ventana
        ancho_ventana = self.ventana.winfo_width()
        alto_ventana = self.ventana.winfo_height()
        
        # Calcular posición centrada
        pos_x = (ancho_pantalla - ancho_ventana) // 2
        pos_y = (alto_pantalla - alto_ventana) // 2
        
        # Aplicar la posición
        self.ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{pos_x}+{pos_y}")
    
    def crear_componentes(self):
        """
        Crea y organiza todos los componentes visuales de la interfaz.
        Utiliza un diseño jerárquico con frames para mejor organización.
        """
        # Frame principal que contiene toda la interfaz
        frame_principal = tk.Frame(self.ventana, bg='#f0f0f0', padx=20, pady=20)
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Título de la aplicación
        titulo = tk.Label(
            frame_principal,
            text="🗂️ Gestor de Tareas",
            font=("Arial", 18, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        titulo.pack(pady=(0, 20))
        
        # Frame para la entrada de datos
        frame_entrada = tk.LabelFrame(
            frame_principal,
            text="Agregar Nueva Tarea",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#34495e',
            padx=10,
            pady=10
        )
        frame_entrada.pack(fill=tk.X, pady=(0, 20))
        
        # Etiqueta para el campo de texto
        etiqueta_tarea = tk.Label(
            frame_entrada,
            text="Descripción de la tarea:",
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        etiqueta_tarea.pack(anchor=tk.W, pady=(0, 5))
        
        # Campo de texto para ingresar nuevas tareas
        self.entrada_tarea = tk.Entry(
            frame_entrada,
            font=("Arial", 11),
            width=50,
            relief=tk.RAISED,
            bd=2
        )
        self.entrada_tarea.pack(fill=tk.X, pady=(0, 10))
        
        # Vincular la tecla Enter al campo de texto para agregar tareas rápidamente
        self.entrada_tarea.bind('<Return>', lambda event: self.agregar_tarea())
        
        # Frame para los botones de acción
        frame_botones = tk.Frame(frame_entrada, bg='#f0f0f0')
        frame_botones.pack(fill=tk.X)
        
        # Botón para agregar tareas
        self.btn_agregar = tk.Button(
            frame_botones,
            text="➕ Agregar Tarea",
            command=self.agregar_tarea,
            bg='#27ae60',
            fg='white',
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.btn_agregar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para limpiar el campo de entrada
        self.btn_limpiar_entrada = tk.Button(
            frame_botones,
            text="🗑️ Limpiar Campo",
            command=self.limpiar_entrada,
            bg='#f39c12',
            fg='white',
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.btn_limpiar_entrada.pack(side=tk.LEFT)
        
        # Frame para la lista de tareas
        frame_lista = tk.LabelFrame(
            frame_principal,
            text="Lista de Tareas",
            font=("Arial", 12, "bold"),
            bg='#f0f0f0',
            fg='#34495e',
            padx=10,
            pady=10
        )
        frame_lista.pack(fill=tk.BOTH, expand=True)
        
        # Frame para contener la lista y scrollbar
        frame_listbox = tk.Frame(frame_lista, bg='#f0f0f0')
        frame_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Lista (Listbox) para mostrar las tareas
        self.lista_tareas = tk.Listbox(
            frame_listbox,
            font=("Arial", 10),
            height=10,
            selectmode=tk.SINGLE,
            relief=tk.SUNKEN,
            bd=2,
            bg='white',
            fg='#2c3e50',
            selectbackground='#3498db',
            selectforeground='white'
        )
        self.lista_tareas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar vertical para la lista
        scrollbar = tk.Scrollbar(frame_listbox, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Conectar el scrollbar con la lista
        self.lista_tareas.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lista_tareas.yview)
        
        # Frame para botones de gestión de la lista
        frame_botones_lista = tk.Frame(frame_lista, bg='#f0f0f0')
        frame_botones_lista.pack(fill=tk.X)
        
        # Botón para eliminar tarea seleccionada
        self.btn_eliminar = tk.Button(
            frame_botones_lista,
            text="❌ Eliminar Seleccionada",
            command=self.eliminar_tarea,
            bg='#e74c3c',
            fg='white',
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.btn_eliminar.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botón para limpiar toda la lista
        self.btn_limpiar_todo = tk.Button(
            frame_botones_lista,
            text="🗑️ Limpiar Todo",
            command=self.limpiar_todo,
            bg='#8e44ad',
            fg='white',
            font=("Arial", 10, "bold"),
            relief=tk.RAISED,
            bd=2,
            padx=15,
            pady=5,
            cursor='hand2'
        )
        self.btn_limpiar_todo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Etiqueta para mostrar estadísticas
        self.etiqueta_estadisticas = tk.Label(
            frame_botones_lista,
            text="Tareas: 0",
            font=("Arial", 10),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.etiqueta_estadisticas.pack(side=tk.RIGHT)
    
    def agregar_tarea(self):
        """
        Evento: Agregar una nueva tarea a la lista.
        
        Esta función obtiene el texto del campo de entrada, lo valida,
        y si es válido, lo agrega tanto a la lista visual como al modelo de datos.
        """
        # Obtener el texto del campo de entrada y eliminar espacios en blanco
        texto_tarea = self.entrada_tarea.get().strip()
        
        # Validar que el campo no esté vacío
        if not texto_tarea:
            messagebox.showwarning(
                "Advertencia",
                "Por favor, ingrese una descripción para la tarea."
            )
            self.entrada_tarea.focus()  # Devolver el foco al campo de entrada
            return
        
        # Crear una tarea con timestamp para mejor organización
        timestamp = datetime.now().strftime("%H:%M:%S")
        tarea_completa = f"[{timestamp}] {texto_tarea}"
        
        # Agregar a la lista visual
        self.lista_tareas.insert(tk.END, tarea_completa)
        
        # Agregar al modelo de datos
        self.tareas.append({
            'texto': texto_tarea,
            'timestamp': timestamp,
            'texto_completo': tarea_completa
        })
        
        # Limpiar el campo de entrada después de agregar
        self.entrada_tarea.delete(0, tk.END)
        
        # Hacer scroll automático para mostrar la última tarea agregada
        self.lista_tareas.see(tk.END)
        
        # Actualizar estadísticas
        self.actualizar_estadisticas()
        
        # Mostrar mensaje de confirmación
        self.ventana.bell()  # Sonido de confirmación del sistema
    
    def eliminar_tarea(self):
        """
        Evento: Eliminar la tarea seleccionada de la lista.
        
        Esta función obtiene el índice de la tarea seleccionada y la elimina
        tanto de la vista como del modelo de datos.
        """
        # Obtener el índice de la tarea seleccionada
        seleccion = self.lista_tareas.curselection()
        
        # Verificar que haya una tarea seleccionada
        if not seleccion:
            messagebox.showinfo(
                "Información",
                "Por favor, seleccione una tarea para eliminar."
            )
            return
        
        # Obtener el índice seleccionado
        indice = seleccion[0]
        
        # Confirmar la eliminación
        tarea_a_eliminar = self.tareas[indice]['texto']
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar la tarea:\n\n'{tarea_a_eliminar}'?"
        )
        
        if confirmar:
            # Eliminar de la lista visual
            self.lista_tareas.delete(indice)
            
            # Eliminar del modelo de datos
            del self.tareas[indice]
            
            # Actualizar estadísticas
            self.actualizar_estadisticas()
            
            # Mostrar mensaje de confirmación
            messagebox.showinfo("Éxito", "Tarea eliminada correctamente.")
    
    def limpiar_entrada(self):
        """
        Evento: Limpiar el campo de entrada de texto.
        
        Esta función borra todo el contenido del campo de entrada y
        devuelve el foco al campo para facilitar la entrada de nuevos datos.
        """
        self.entrada_tarea.delete(0, tk.END)
        self.entrada_tarea.focus()
    
    def limpiar_todo(self):
        """
        Evento: Limpiar toda la lista de tareas.
        
        Esta función elimina todas las tareas de la lista después de
        confirmar la acción con el usuario.
        """
        # Verificar que haya tareas para limpiar
        if not self.tareas:
            messagebox.showinfo(
                "Información",
                "No hay tareas para limpiar."
            )
            return
        
        # Confirmar la acción
        confirmar = messagebox.askyesno(
            "Confirmar Limpieza",
            f"¿Está seguro de que desea eliminar todas las {len(self.tareas)} tareas?"
        )
        
        if confirmar:
            # Limpiar la lista visual
            self.lista_tareas.delete(0, tk.END)
            
            # Limpiar el modelo de datos
            self.tareas.clear()
            
            # Actualizar estadísticas
            self.actualizar_estadisticas()
            
            # Mostrar mensaje de confirmación
            messagebox.showinfo("Éxito", "Todas las tareas han sido eliminadas.")
    
    def actualizar_estadisticas(self):
        """
        Actualiza la etiqueta de estadísticas con el número actual de tareas.
        """
        cantidad = len(self.tareas)
        texto_stats = f"Tareas: {cantidad}"
        if cantidad == 1:
            texto_stats = f"Tarea: 1"
        elif cantidad > 1:
            texto_stats = f"Tareas: {cantidad}"
        else:
            texto_stats = "Sin tareas"
        
        self.etiqueta_estadisticas.config(text=texto_stats)
    
    def ejecutar(self):
        """
        Inicia el bucle principal de la aplicación GUI.
        
        Este método debe ser llamado para mostrar la ventana y comenzar
        a escuchar los eventos del usuario.
        """
        # Colocar el foco inicial en el campo de entrada
        self.entrada_tarea.focus()
        
        # Configurar el protocolo de cierre de ventana
        self.ventana.protocol("WM_DELETE_WINDOW", self.al_cerrar_ventana)
        
        # Iniciar el bucle principal de la GUI
        self.ventana.mainloop()
    
    def al_cerrar_ventana(self):
        """
        Maneja el evento de cierre de la ventana.
        
        Si hay tareas pendientes, pregunta al usuario si desea cerrar la aplicación.
        """
        if self.tareas:
            confirmar = messagebox.askyesno(
                "Confirmar Salida",
                f"Hay {len(self.tareas)} tareas en la lista.\n¿Está seguro de que desea salir?"
            )
            if confirmar:
                self.ventana.destroy()
        else:
            self.ventana.destroy()


def main():
    """
    Función principal que inicia la aplicación.
    
    Esta función crea una instancia de la clase GestorTareasGUI
    y ejecuta la aplicación.
    """
    # Crear la aplicación
    app = GestorTareasGUI()
    
    # Ejecutar la aplicación
    app.ejecutar()


# Punto de entrada del programa
if __name__ == "__main__":
    """
    Punto de entrada principal del programa.
    
    Este bloque se ejecuta solo cuando el archivo se ejecuta directamente,
    no cuando se importa como módulo.
    """
    print("🚀 Iniciando Gestor de Tareas - Aplicación GUI Básica")
    print("=" * 50)
    print("Aplicación desarrollada con Tkinter")
    print("Autor: Norman Eras")
    print("Materia: Programación Orientada a Objetos")
    print("=" * 50)
    
    # Ejecutar la aplicación
    main()
