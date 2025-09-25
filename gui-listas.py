import tkinter as tk
from tkinter import messagebox

class TaskManager:
	def __init__(self, root):
		self.root = root
		self.root.title("Lista de Tareas")
		self.tasks = []
		self.completed = set()

		self.entry = tk.Entry(root, width=40)
		self.entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)
		self.entry.bind('<Return>', self.add_task_event)

		self.add_btn = tk.Button(root, text="Añadir Tarea", command=self.add_task)
		self.add_btn.grid(row=0, column=2, padx=5)

		self.listbox = tk.Listbox(root, width=50, selectmode=tk.SINGLE)
		self.listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
		self.listbox.bind('<Double-Button-1>', self.mark_completed_event)

		self.complete_btn = tk.Button(root, text="Marcar como Completada", command=self.mark_completed)
		self.complete_btn.grid(row=2, column=0, pady=5)

		self.delete_btn = tk.Button(root, text="Eliminar Tarea", command=self.delete_task)
		self.delete_btn.grid(row=2, column=1, pady=5)

	def add_task_event(self, event):
		self.add_task()

	def add_task(self):
		task = self.entry.get().strip()
		if task:
			self.tasks.append(task)
			self.entry.delete(0, tk.END)
			self.update_listbox()
		else:
			messagebox.showwarning("Advertencia", "La tarea no puede estar vacía.")

	def mark_completed_event(self, event):
		self.mark_completed()

	def mark_completed(self):
		idx = self.listbox.curselection()
		if idx:
			i = idx[0]
			self.completed.add(i)
			self.update_listbox()
		else:
			messagebox.showinfo("Info", "Selecciona una tarea para marcar como completada.")

	def delete_task(self):
		idx = self.listbox.curselection()
		if idx:
			i = idx[0]
			del self.tasks[i]
			self.completed = {j if j < i else j-1 for j in self.completed if j != i}
			self.update_listbox()
		else:
			messagebox.showinfo("Info", "Selecciona una tarea para eliminar.")

	def update_listbox(self):
		self.listbox.delete(0, tk.END)
		for i, task in enumerate(self.tasks):
			if i in self.completed:
				self.listbox.insert(tk.END, f"✔️ {task}")
				self.listbox.itemconfig(tk.END, {'fg': 'gray'})
			else:
				self.listbox.insert(tk.END, task)

if __name__ == "__main__":
	root = tk.Tk()
	app = TaskManager(root)
	root.mainloop()
