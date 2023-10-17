import sqlite3
import tkinter as tk
from tkinter import ttk


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
      
    def init_main(self):
        # панель инструментов (просто цветной прямоугольник)
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # создание кнопки добавления контакта
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.add_img,
                            command=self.open_dialog)
        btn_add.pack(side=tk.LEFT)
        
        # создание кнопки редактирования контакта
        self.edit_img = tk.PhotoImage(file='./img/update.png')
        btn_edit = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.edit_img,
                            command=self.open_edit)
        btn_edit.pack(side=tk.LEFT)
        
        # создание кнопки удаления контакта
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.del_img,
                            command=self.delete_records)
        btn_del.pack(side=tk.LEFT)
        
        # создание кнопки поиска контакта
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.search_img,
                            command=self.open_search)
        btn_search.pack(side=tk.LEFT)
        
        # создание кнопки обновления таблицы
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d7d7', bd=0,
                            image=self.refresh_img,
                            command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)
        
        # создание таблицы
        self.tree = ttk.Treeview(root, 
                                 columns=('id', 'name', 'tel', 'email', 'salary'),
                                 height=45,
                                 show='headings')
        # добавляем параметры столбцам
        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)
        
        self.tree.heading('id', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Номер телефона')
        self.tree.heading('email', text='Эл.почта')
        self.tree.heading('salary', text='Зарплата')
        self.tree.pack(side=tk.LEFT)
        
        # полоса прокрутки
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        
    # метод добавления (посредник)
    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()
        
    # метод редактирования
    def edit_record(self, name, tel, email, salary):
        ind = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE сотрудники SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
        ''', (name, tel, email, salary, ind))
        self.db.conn.commit()
        self.view_records()
        
    # метод удаления записей
    def delete_records(self):
        # проходим циклом по всем выделенным строкам в таблице
        for i in self.tree.selection():
            # берём id каждой строки
            id = self.tree.set(i, '#1')
            # удаляем по id 
            self.db.cur.execute('''
                DELETE FROM сотрудники 
                WHERE id = ?
            ''', (id, ))
        self.db.conn.commit()
        self.view_records()
    
    # метод поиска записей
    def search_records(self, name):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute('SELECT * FROM сотрудники WHERE name LIKE ?',
                            ('%' + name + '%',))
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]
        
    # вызов дочернего окна    
    def open_dialog(self):
        Child()
        
    # вызов окна редактирования
    def open_edit(self):
        Update()
        

    def open_search(self):
        Search()
    
    def view_records(self):
        [self.tree.delete(i) for i in self.tree.get_children()]
        self.db.cur.execute("SELECT * FROM сотрудники ORDER BY RANDOM() LIMIT 4")
        [self.tree.insert('', 'end', values=i) for i in self.db.cur.fetchall()]
  
# класс дочернего окна
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
        
    def init_child(self):
        self.title('Добавление нового сотрудника')
        self.geometry('400x170')
        # запрет на изменение размеров
        self.resizable(False, False)
        # перезватаваеи все события приложения
        self.grab_set()
        # захватываем фокус
        self.focus_set()
        
        # создание формы
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=25)
        label_tel = tk.Label(self, text='Телефон')
        label_tel.place(x=50, y=50)
        label_email = tk.Label(self, text='Эл.почта')
        label_email.place(x=50, y=75)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=100)
        
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=150, y=25)
        self.entry_tel = tk.Entry(self)
        self.entry_tel.place(x=150, y=50)
        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=150, y=75)
        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=150, y=100)
        
        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: 
                    self.view.records(
                        self.entry_name.get(),
                        self.entry_tel.get(),
                        self.entry_email.get(),
                        self.entry_salary.get()
                        ))
        self.btn_ok.place(x=225, y=130)
        
        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=130)
        
class Update(Child):
    def __init__(self):
        super().__init__()
        self.db = db
        self.init_edit()
        self.load_data()
        
    
    def init_edit(self):
        self.title('Изменение текущего сотрудника')
        # убираем кнопку добавления
        self.btn_ok.destroy()
        # кнопка редактировать
        self.btn_ok = tk.Button(self, text='Редактировать')
        self.btn_ok.bind('<Button-1>', lambda ev: 
                    self.view.edit_record(
                        self.entry_name.get(),
                        self.entry_tel.get(),
                        self.entry_email.get(),
                        self.entry_salary.get()
                        ))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=195, y=130)

    # метод автозаполнения формы старыми данными
    def load_data(self): 
        self.db.cur.execute('''SELECT * FROM сотрудники WHERE id = ?''',
                    self.view.tree.set(self.view.tree.selection()[0], '#1'))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# класс окна поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app
        
    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('300x55')
        # запрет на изменение размеров
        self.resizable(False, False)
        # перезватаваеи все события приложения
        self.grab_set()
        # захватываем фокус
        self.focus_set()
        
        # создание формы
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=10, y=18)
        
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=45, y=20)
        
        self.btn_ok = tk.Button(self, text='Найти' )
        self.btn_ok.bind('<Button-1>', 
                         lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>',
                         lambda ev: self.deiconify(), add='+')
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=175, y=15)
        
        btn_cancel = tk.Button(self, text='Закрыть',
                               command=self.destroy)
        btn_cancel.place(x=225, y=15)
        
        
# класс бд 
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('Список сотрудников компании.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
                CREATE TABLE IF NOT EXISTS сотрудники (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    salary TEXT
                )''')
        
    # метод добавления в бд
    def insert_data(self, name, tel, email, salary):
        self.cur.execute('''
                INSERT INTO сотрудники (name, phone, email, salary)
                VALUES (?, ?, ?, ?)''', (name, tel, email, salary))
        self.conn.commit()
        
        

# действия при запуске программы    
if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    root.title('Список сотрудников компании')
    root.geometry('800x400')
    # запрет на изменение размеров
    root.resizable(False, False)
    root.mainloop()