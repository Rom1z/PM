import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "manufacturing"
}


def connect_db():
    return mysql.connector.connect(**DB_CONFIG)


class App:

    def __init__(self, root):

        self.root = root
        self.root.title("Учет материалов")
        self.root.geometry("1000x600")

        self.create_widgets()
        self.load_materials()

    def create_widgets(self):

        columns = ("name","type","price","stock","min","unit","required")

        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")

        self.tree.heading("name", text="Наименование")
        self.tree.heading("type", text="Тип материала")
        self.tree.heading("price", text="Цена")
        self.tree.heading("stock", text="На складе")
        self.tree.heading("min", text="Мин количество")
        self.tree.heading("unit", text="Ед")
        self.tree.heading("required", text="Требуется")

        self.tree.pack(fill="both", expand=True)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame,text="Добавить",command=self.add_material).pack(side=tk.LEFT,padx=5)
        tk.Button(btn_frame,text="Редактировать",command=self.edit_material).pack(side=tk.LEFT,padx=5)
        tk.Button(btn_frame,text="Просмотр продукции",command=self.show_products).pack(side=tk.LEFT,padx=5)
        tk.Button(btn_frame,text="Обновить",command=self.load_materials).pack(side=tk.LEFT,padx=5)

    def load_materials(self):

        for i in self.tree.get_children():
            self.tree.delete(i)

        db = connect_db()
        cursor = db.cursor()

        query = """
        SELECT 
        m.id,
        m.name,
        mt.name,
        m.price,
        m.quantity_in_stock,
        m.min_quantity,
        m.unit_of_measure,
        IFNULL(SUM(mp.required_quantity),0)
        FROM Material m
        JOIN MaterialType mt ON mt.id=m.material_type_id
        LEFT JOIN MaterialProduct mp ON mp.material_id=m.id
        GROUP BY m.id
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        for r in rows:

            self.tree.insert("", "end", values=(
                r[1],
                r[2],
                f"{r[3]:.2f}",
                f"{r[4]:.2f}",
                f"{r[5]:.2f}",
                r[6],
                f"{r[7]:.2f}"
            ))

        db.close()

    def get_selected(self):

        selected = self.tree.focus()

        if not selected:
            messagebox.showwarning("Ошибка","Выберите материал")
            return None

        return self.tree.item(selected)["values"][0]

    def add_material(self):

        MaterialForm(self.root,self.load_materials)

    def edit_material(self):

        name = self.get_selected()

        if name:
            MaterialForm(self.root,self.load_materials,name)

    def show_products(self):

        name = self.get_selected()

        if not name:
            return

        db = connect_db()
        cursor = db.cursor()

        query = """
        SELECT p.name,p.article,mp.required_quantity
        FROM MaterialProduct mp
        JOIN Material m ON m.id=mp.material_id
        JOIN Product p ON p.id=mp.product_id
        WHERE m.name=%s
        """

        cursor.execute(query,(name,))
        rows = cursor.fetchall()

        win = tk.Toplevel(self.root)
        win.title("Продукция")

        tree = ttk.Treeview(win, columns=("name","article","qty"),show="headings")

        tree.heading("name",text="Продукция")
        tree.heading("article",text="Артикул")
        tree.heading("qty",text="Количество")

        tree.pack(fill="both",expand=True)

        for r in rows:
            tree.insert("",tk.END,values=(r[0],r[1],f"{r[2]:.2f}"))

        db.close()


class MaterialForm:

    def __init__(self,parent,refresh,name=None):

        self.refresh = refresh
        self.name = name

        self.win = tk.Toplevel(parent)
        self.win.title("Материал")

        labels = [
            "Название",
            "Тип id",
            "Цена",
            "На складе",
            "Мин количество",
            "Упаковка",
            "Единица"
        ]

        self.entries = []

        for i,l in enumerate(labels):

            tk.Label(self.win,text=l).grid(row=i,column=0)

            e = tk.Entry(self.win)
            e.grid(row=i,column=1)

            self.entries.append(e)

        tk.Button(self.win,text="Сохранить",command=self.save).grid(row=7,column=0,columnspan=2)

    def save(self):

        data = [e.get() for e in self.entries]

        db = connect_db()
        cursor = db.cursor()

        query = """
        INSERT INTO Material
        (name,material_type_id,price,quantity_in_stock,min_quantity,package_quantity,unit_of_measure)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(query,data)

        db.commit()
        db.close()

        self.refresh()
        self.win.destroy()


root = tk.Tk()
app = App(root)
root.mainloop()x    