import tkinter as tk
from tkinter import ttk
import mysql.connector

DB = dict(host="localhost", user="root", password="12543hRGB2001", database="furniture_factory")


def q(sql, p=(), one=False):
    c = mysql.connector.connect(**DB)
    cur = c.cursor()
    cur.execute(sql, p)
    r = cur.fetchone() if one else cur.fetchall() if sql.lstrip().upper().startswith("SELECT") else None
    c.commit(); c.close()
    return r


class MaterialForm:
    def __init__(s, p, refresh, m=None):
        s.r, s.m, s.t = refresh, m, q("SELECT id,name FROM material_types")
        w = s.w = tk.Toplevel(p); w.title("Материал")
        s.e = [tk.Entry(w) for _ in range(3)]
        for t in ("Название", "Тип", "Количество", "Минимум"): tk.Label(w, text=t).pack()
        s.e[0].pack(); s.cb = ttk.Combobox(w, values=[x[1] for x in s.t]); s.cb.pack(); s.e[1].pack(); s.e[2].pack()
        tk.Button(w, text="Сохранить", command=s.save).pack(pady=10)
        if m:
            s.e[0].insert(0, m[1]); s.e[1].insert(0, m[3]); s.e[2].insert(0, m[4])
            for i, (_, n) in enumerate(s.t):
                if n == m[2]: s.cb.current(i); break

    def save(s):
        n, st, mn = (x.get() for x in s.e); tid = s.t[s.cb.current()][0]
        q("UPDATE materials SET name=%s,type_id=%s,stock_quantity=%s,min_quantity=%s WHERE id=%s", (n, tid, st, mn, s.m[0])) if s.m else q(
            "INSERT INTO materials(name,type_id,stock_quantity,min_quantity) VALUES(%s,%s,%s,%s)", (n, tid, st, mn))
        s.r(); s.w.destroy()


class App:
    def __init__(s, root):
        s.root = root; root.title("Склад материалов"); root.geometry("900x600")
        tk.Label(root, text="Материалы на складе", font=("Constantia", 16), bg="#BFD6F6").pack(fill="x")
        s.t = ttk.Treeview(root, columns=("id", "name", "type", "stock", "min"), show="headings")
        for c, h in (("id", "ID"), ("name", "Материал"), ("type", "Тип"), ("stock", "На складе"), ("min", "Минимум")): s.t.heading(c, text=h)
        s.t.pack(fill="both", expand=True)
        b = tk.Frame(root); b.pack(pady=10)
        for txt, cmd in (("Добавить", s.add), ("Редактировать", s.edit), ("Продукция", s.products), ("Расчёт", s.calc), ("Обновить", s.load)):
            tk.Button(b, text=txt, command=cmd, bg="#405C73", fg="white").pack(side="left", padx=5)
        s.load()

    def load(s):
        [s.t.delete(i) for i in s.t.get_children()]
        for r in q("SELECT m.id,m.name,mt.name,m.stock_quantity,m.min_quantity FROM materials m JOIN material_types mt ON mt.id=m.type_id"):
            s.t.insert("", tk.END, values=r)

    def sel(s):
        i = s.t.focus()
        return s.t.item(i)["values"] if i else None

    def add(s): MaterialForm(s.root, s.load)
    def edit(s):
        v = s.sel()
        if v: MaterialForm(s.root, s.load, v)

    def products(s):
        v = s.sel()
        if not v: return
        w = tk.Toplevel(s.root); w.title("Продукция")
        l = tk.Listbox(w); l.pack(fill="both", expand=True)
        for (n,) in q("SELECT p.name FROM products p JOIN product_materials pm ON p.id=pm.product_id WHERE pm.material_id=%s", (v[0],)): l.insert(tk.END, n)

    def calc(s):
        v = s.sel()
        if not v: return
        x = q("SELECT SUM(quantity) FROM product_materials WHERE material_id=%s", (v[0],), one=True)
        tk.Label(tk.Toplevel(s.root), text=f"Требуемое количество: {round(x[0] or 0, 2)}").pack(padx=20, pady=20)


if __name__ == "__main__":
    App(tk.Tk()).root.mainloop()
