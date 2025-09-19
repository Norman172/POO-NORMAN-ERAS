
# Importar Tkinter y ttk para la interfaz gráfica
import tkinter as tk
from tkinter import ttk

# Crear ventana principal de la agenda
root = tk.Tk()
root.title("Agenda Personal")
root.geometry("600x400")

# Frame para la lista de eventos


# Frame para mostrar la lista de eventos
frame_lista = tk.Frame(root)
frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


# TreeView para mostrar los eventos agendados
tree = ttk.Treeview(frame_lista, columns=("Fecha", "Hora", "Descripción"), show="headings")
tree.heading("Fecha", text="Fecha")
tree.heading("Hora", text="Hora")
tree.heading("Descripción", text="Descripción")
tree.pack(fill=tk.BOTH, expand=True)

# Frame para la entrada de datos


# Frame para la entrada de datos de nuevos eventos
frame_entrada = tk.Frame(root)
frame_entrada.pack(fill=tk.X, padx=10, pady=5)

# Label y Entry para Fecha


# DatePicker para seleccionar la fecha del evento
from tkcalendar import DateEntry
label_fecha = tk.Label(frame_entrada, text="Fecha:")
label_fecha.grid(row=0, column=0, padx=5, pady=5)
date_picker = DateEntry(frame_entrada, date_pattern='yyyy-mm-dd')
date_picker.grid(row=0, column=1, padx=5, pady=5)


# Label y Entry para la hora del evento
label_hora = tk.Label(frame_entrada, text="Hora (HH:MM):")
label_hora.grid(row=0, column=2, padx=5, pady=5)
entry_hora = tk.Entry(frame_entrada)
entry_hora.grid(row=0, column=3, padx=5, pady=5)


# Label y Entry para la descripción del evento
label_desc = tk.Label(frame_entrada, text="Descripción:")
label_desc.grid(row=0, column=4, padx=5, pady=5)
entry_desc = tk.Entry(frame_entrada, width=30)
entry_desc.grid(row=0, column=5, padx=5, pady=5)

# Frame para los botones de acción


# Frame para los botones de acción de la agenda
frame_botones = tk.Frame(root)
frame_botones.pack(fill=tk.X, padx=10, pady=5)

# Botón para agregar evento


# Función para agregar un evento a la lista
def agregar_evento():
	fecha = date_picker.get()
	hora = entry_hora.get()
	desc = entry_desc.get()
	# Verifica que todos los campos estén llenos
	if fecha and hora and desc:
		tree.insert("", "end", values=(fecha, hora, desc))
		entry_hora.delete(0, tk.END)
		entry_desc.delete(0, tk.END)

# Botón para agregar evento
btn_agregar = tk.Button(frame_botones, text="Agregar Evento", command=agregar_evento)
btn_agregar.pack(side=tk.LEFT, padx=10, pady=5)

# Botón para eliminar evento seleccionado


# Función para eliminar el evento seleccionado de la lista
def eliminar_evento():
	seleccionado = tree.selection()
	if seleccionado:
		# Diálogo de confirmación antes de eliminar
		respuesta = tk.messagebox.askyesno("Confirmar eliminación", "¿Desea eliminar el evento seleccionado?")
		if respuesta:
			for item in seleccionado:
				tree.delete(item)

# Importar messagebox para diálogos
from tkinter import messagebox

# Botón para eliminar evento seleccionado
btn_eliminar = tk.Button(frame_botones, text="Eliminar Evento Seleccionado", command=eliminar_evento)
btn_eliminar.pack(side=tk.LEFT, padx=10, pady=5)


# Botón para salir de la aplicación
btn_salir = tk.Button(frame_botones, text="Salir", command=root.quit)
btn_salir.pack(side=tk.RIGHT, padx=10, pady=5)


# (Aquí se agregaron los widgets principales de la agenda)

# Iniciar el loop principal de la aplicación
root.mainloop()
