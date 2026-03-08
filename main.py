import tkinter as tk
from materials_window import MaterialsWindow


root = tk.Tk()

root.title("Склад материалов")

root.geometry("900x600")

root.configure(bg="#FFFFFF")

app = MaterialsWindow(root)

root.mainloop()