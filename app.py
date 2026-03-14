import tkinter as tk
from tkinter import ttk
import mysql.connector as db

CFG=dict(host='localhost',user='root',password='1245678',database='furniture_factory')


def q(sql,p=(),one=0):
    c=db.connect(**CFG);k=c.cursor();k.execute(sql,p);r=k.fetchone() if one else k.fetchall();c.commit();c.close();return r


def materials():
    return q('''SELECT m.id,m.name,mt.name,m.stock_quantity,m.min_quantity FROM materials m JOIN material_types mt ON mt.id=m.type_id''')

def types():
    return q('SELECT id,name FROM material_types')

def save(mid,name,tid,stock,mini):
    q('UPDATE materials SET name=%s,type_id=%s,stock_quantity=%s,min_quantity=%s WHERE id=%s' if mid else 'INSERT INTO materials(name,type_id,stock_quantity,min_quantity) VALUES(%s,%s,%s,%s)',(name,tid,stock,mini,*(() if mid is None else (mid,))))


def products(mid):
    return q('SELECT p.name FROM products p JOIN product_materials pm ON p.id=pm.product_id WHERE pm.material_id=%s',(mid,))


def required(mid):
    r=q('SELECT SUM(quantity) FROM product_materials WHERE material_id=%s',(mid,),1);return round(r[0] or 0,2)


class Form:
    def __init__(s,root,refresh,row=None):
        s.refresh,s.row,s.ts=refresh,row,types();w=s.w=tk.Toplevel(root);w.title('Материал')
        for t in ('Название','Тип','Количество','Минимум'): tk.Label(w,text=t).pack()
        s.n,s.t,s.st,s.m=[tk.Entry(w) for _ in range(4)];s.n.pack();s.t=ttk.Combobox(w,values=[x[1] for x in s.ts]);s.t.pack();s.st.pack();s.m.pack()
        tk.Button(w,text='Сохранить',command=s.save).pack(pady=8)
        if row: s.n.insert(0,row[1]);s.st.insert(0,row[3]);s.m.insert(0,row[4])

    def save(s):
        save(None if not s.row else s.row[0],s.n.get(),s.ts[s.t.current()][0],s.st.get(),s.m.get());s.refresh();s.w.destroy()


class App:
    def __init__(s,root):
        s.r=root;root.title('Склад материалов');root.geometry('900x600')
        f=tk.Frame(root,bg='#fff');f.pack(fill='both',expand=1);tk.Label(f,text='Материалы на складе',font=('Constantia',16),bg='#BFD6F6').pack(fill='x')
        s.t=ttk.Treeview(f,columns=('id','name','type','stock','min'),show='headings')
        for c,h in zip(('id','name','type','stock','min'),('ID','Материал','Тип','На складе','Минимум')): s.t.heading(c,text=h)
        s.t.pack(fill='both',expand=1)
        b=tk.Frame(f);b.pack(pady=10)
        for txt,cmd in (('Добавить',s.add),('Редактировать',s.edit),('Показать продукцию',s.show),('Рассчитать количество',s.calc)):
            tk.Button(b,text=txt,command=cmd,bg='#405C73' if txt=='Добавить' else None,fg='white' if txt=='Добавить' else None).pack(side='left',padx=5)
        s.load()

    def cur(s):
        i=s.t.focus();return s.t.item(i)['values'] if i else None
    def load(s):
        [s.t.delete(i) for i in s.t.get_children()];[s.t.insert('','end',values=r) for r in materials()]
    def add(s): Form(s.r,s.load)
    def edit(s):
        r=s.cur();
        if r: Form(s.r,s.load,r)
    def show(s):
        r=s.cur();
        if not r:return
        w=tk.Toplevel(s.r);w.title('Продукция');l=tk.Listbox(w);l.pack(fill='both',expand=1)
        [l.insert(tk.END,p[0]) for p in products(r[0])]
    def calc(s):
        r=s.cur();
        if not r:return
        w=tk.Toplevel(s.r);w.title('Расчет');tk.Label(w,text=f'Требуемое количество: {required(r[0])}').pack(padx=20,pady=20)


if __name__=='__main__':
    root=tk.Tk();App(root);root.mainloop()
