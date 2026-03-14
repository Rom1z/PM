import tkinter as tk
from tkinter import ttk
import mysql.connector

DB = {"host": "localhost", "user": "root", "password": "12543hRGB2001", "database": "furniture_factory"}

def q(sql, params=(), one=False):
    with mysql.connector.connect(**DB) as c:
        cur = c.cursor(); cur.execute(sql, params)
        if sql.lstrip().upper().startswith("SELECT"): return cur.fetchone() if one else cur.fetchall()
        c.commit()

def materials():
    return q("SELECT m.id,m.name,mt.name,m.stock_quantity,m.min_quantity FROM materials m JOIN material_types mt ON mt.id=m.type_id")

def material_types(): return q("SELECT id,name FROM material_types")
def products(material_id): return q("SELECT p.name FROM products p JOIN product_materials pm ON p.id=pm.product_id WHERE pm.material_id=%s", (material_id,))
def required_qty(material_id): return round((q("SELECT SUM(quantity) FROM product_materials WHERE material_id=%s", (material_id,), True) or [0])[0] or 0, 2)

class MaterialForm:
    def __init__(self, parent, refresh, material=None):
        self.refresh, self.material, self.types = refresh, material, material_types()
        self.w = tk.Toplevel(parent); self.w.title("Материал")
        for txt in ("Название", "Тип", "Количество", "Минимум"): tk.Label(self.w, text=txt).pack()
        self.name = tk.Entry(self.w); self.name.pack()
        self.type_box = ttk.Combobox(self.w, values=[t[1] for t in self.types]); self.type_box.pack()
        self.stock = tk.Entry(self.w); self.stock.pack()
        self.min = tk.Entry(self.w); self.min.pack()
        tk.Button(self.w, text="Сохранить", command=self.save).pack(pady=10)
        if material:
            self.name.insert(0, material[1]); self.stock.insert(0, material[3]); self.min.insert(0, material[4])

    def save(self):
        args = (self.name.get(), self.types[self.type_box.current()][0], self.stock.get(), self.min.get())
        if self.material: q("UPDATE materials SET name=%s,type_id=%s,stock_quantity=%s,min_quantity=%s WHERE id=%s", (*args, self.material[0]))
        else: q("INSERT INTO materials(name,type_id,stock_quantity,min_quantity) VALUES(%s,%s,%s,%s)", args)
        self.refresh(); self.w.destroy()

class App:
    def __init__(self, root):
        self.root = root; root.title("Склад материалов"); root.geometry("900x600"); root.configure(bg="#FFF")
        f = tk.Frame(root, bg="#FFF"); f.pack(fill="both", expand=True)
        tk.Label(f, text="Материалы на складе", font=("Constantia", 16), bg="#BFD6F6").pack(fill="x")
        self.tree = ttk.Treeview(f, columns=("id", "name", "type", "stock", "min"), show="headings")
        for c, t in (("id", "ID"), ("name", "Материал"), ("type", "Тип"), ("stock", "На складе"), ("min", "Минимум")): self.tree.heading(c, text=t)
        self.tree.pack(fill="both", expand=True)
        b = tk.Frame(f); b.pack(pady=10)
        for txt, cmd in (("Добавить", self.add), ("Редактировать", self.edit), ("Показать продукцию", self.show_products), ("Рассчитать количество", self.calc)):
            tk.Button(b, text=txt, command=cmd, bg="#405C73" if txt == "Добавить" else None, fg="white" if txt == "Добавить" else None).pack(side="left", padx=5)
        self.load()

    def selected(self):
        s = self.tree.focus(); return self.tree.item(s)["values"] if s else None

    def load(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for m in materials(): self.tree.insert("", "end", values=m)

    def add(self): MaterialForm(self.root, self.load)
    def edit(self):
        if v := self.selected(): MaterialForm(self.root, self.load, v)

    def show_products(self):
        if not (v := self.selected()): return
        w = tk.Toplevel(self.root); w.title("Продукция"); lb = tk.Listbox(w); lb.pack(fill="both", expand=True)
        for p in products(v[0]): lb.insert(tk.END, p[0])

    def calc(self):
        if not (v := self.selected()): return
        w = tk.Toplevel(self.root); w.title("Расчет")
        tk.Label(w, text=f"Требуемое количество: {required_qty(v[0])}").pack(padx=20, pady=20)

if __name__ == "__main__":
    root = tk.Tk(); App(root); root.mainloop()
