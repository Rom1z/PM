import tkinter as tk
from tkinter import ttk
import database
from add_edit_material import MaterialForm


class MaterialsWindow:

    def __init__(self, root):

        self.root = root

        self.frame = tk.Frame(root, bg="#FFFFFF")
        self.frame.pack(fill="both", expand=True)

        title = tk.Label(
            self.frame,
            text="Материалы на складе",
            font=("Constantia", 16),
            bg="#BFD6F6"
        )

        title.pack(fill="x")

        self.tree = ttk.Treeview(
            self.frame,
            columns=("id", "name", "type", "stock", "min"),
            show="headings"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Материал")
        self.tree.heading("type", text="Тип")
        self.tree.heading("stock", text="На складе")
        self.tree.heading("min", text="Минимум")

        self.tree.pack(fill="both", expand=True)

        buttons = tk.Frame(self.frame)
        buttons.pack(pady=10)

        tk.Button(
            buttons,
            text="Добавить",
            bg="#405C73",
            fg="white",
            command=self.add_material
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Редактировать",
            command=self.edit_material
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Показать продукцию",
            command=self.show_products
        ).pack(side="left", padx=5)

        tk.Button(
            buttons,
            text="Рассчитать количество",
            command=self.calculate_material
        ).pack(side="left", padx=5)

        self.load_materials()

    def load_materials(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        materials = database.get_materials()

        for m in materials:
            self.tree.insert("", "end", values=m)

    def add_material(self):

        MaterialForm(self.root, self.load_materials)

    def edit_material(self):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]

        MaterialForm(self.root, self.load_materials, values)

    def show_products(self):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]

        material_id = values[0]

        products = database.get_products_by_material(material_id)

        window = tk.Toplevel(self.root)
        window.title("Продукция")

        listbox = tk.Listbox(window)
        listbox.pack(fill="both", expand=True)

        for p in products:
            listbox.insert(tk.END, p[0])

    def calculate_material(self):

        selected = self.tree.focus()

        if not selected:
            return

        values = self.tree.item(selected)["values"]

        material_id = values[0]

        quantity = database.get_required_quantity(material_id)

        window = tk.Toplevel(self.root)
        window.title("Расчет")

        tk.Label(
            window,
            text=f"Требуемое количество: {quantity}"
        ).pack(padx=20, pady=20)