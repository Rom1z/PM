import tkinter as tk
from tkinter import ttk
import database


class MaterialForm:

    def __init__(self, parent, refresh, material=None):

        self.refresh = refresh
        self.material = material

        self.window = tk.Toplevel(parent)
        self.window.title("Материал")

        tk.Label(self.window, text="Название").pack()

        self.name_entry = tk.Entry(self.window)
        self.name_entry.pack()

        tk.Label(self.window, text="Тип").pack()

        self.types = database.get_material_types()

        self.type_box = ttk.Combobox(
            self.window,
            values=[t[1] for t in self.types]
        )
        self.type_box.pack()

        tk.Label(self.window, text="Количество").pack()

        self.stock_entry = tk.Entry(self.window)
        self.stock_entry.pack()

        tk.Label(self.window, text="Минимум").pack()

        self.min_entry = tk.Entry(self.window)
        self.min_entry.pack()

        tk.Button(
            self.window,
            text="Сохранить",
            command=self.save
        ).pack(pady=10)

        if material:
            self.fill_data()

    def fill_data(self):

        self.name_entry.insert(0, self.material[1])
        self.stock_entry.insert(0, self.material[3])
        self.min_entry.insert(0, self.material[4])

    def save(self):

        name = self.name_entry.get()
        stock = self.stock_entry.get()
        minimum = self.min_entry.get()

        type_index = self.type_box.current()

        type_id = self.types[type_index][0]

        if self.material:

            database.update_material(
                self.material[0],
                name,
                type_id,
                stock,
                minimum
            )

        else:

            database.add_material(
                name,
                type_id,
                stock,
                minimum
            )

        self.refresh()

        self.window.destroy()