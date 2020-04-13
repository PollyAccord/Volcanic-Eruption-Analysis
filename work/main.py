import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import interface as ui
import base_handling as hand_base
import os

"""
Автор: 
Цель: создание главного окна и расстановка всех его компонентов 
Вход: Нет 
Выход: объект главного окна
"""


def setup():
    win = tk.Tk()
    win.title('Volcano Analyse')
    win.grid_columnconfigure(0, weight=1)
    win.grid_rowconfigure(0, weight=1)
    ui.mainframe = tk.Frame(win)
    # создание элементов
    lsb_base = tk.Listbox(ui.mainframe, selectmode='browse')
    ui.base_list = lsb_base
    for name, base in hand_base.work_list.items():
        lsb_base.insert(tk.END, name)
    lsb_base.bind('<Double-Button-1>', lambda *args: open_base(lsb_base.get(lsb_base.curselection())))
    # кнопка добавления базы
    add_button = tk.Button(ui.mainframe, text='Добавить')
    add_button.bind('<Button-1>', load_button)
    # раставляем по сетке
    lsb_base.grid(row=0, column=0, sticky='nsew')
    add_button.grid(row=1, column=0, sticky="nsew")
    ui.mainframe.grid(row=0, column=0)
    ui.currentframe = ui.mainframe
    return win


"""
Автор:  
Цель: обработчик кнопки закрыть базу
Вход: Нет 
Выход: объект главного окна
"""


def back(*args):
    ui.currentframe.destroy()
    ui.currentframe = ui.mainframe
    ui.currentframe.tkraise()


def load_button(*args):
    path = filedialog.askopenfilename(initialdir="base/", filetypes=(("Database files", "*.csv;"), ("All files", "*.*")))
    path = path.replace('/', "\\")
    if os.path.exists(path):
        base_name = hand_base.read_base(path)
        ui.base_list.insert(tk.END, base_name)
    else:
        # кидаем exception
        pass

"""
Автор:  
Цель: открытие базы данных по двойному нажатию на виджет списка 
Вход: Нет 
Выход: нет
"""

def open_base(selected):
    base = hand_base.work_list.get(selected)
    frame = tk.Frame(root)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    workframe = create_workspace(frame, base)
    workframe.grid(row=1, column=0)
    #back_button = tk.Button(frame, text='Добавить базу базу')
    #back_button.bind('<Button-1>', back)
    #back_button.grid(row=0, column=0, sticky="W")
    frame.grid(row=1, column=0)
    ui.currentframe = frame
    ui.currentframe.tkraise()


"""
новая функция
"""


def create_workspace(win, selected_base):
    # создаем и заполняем нашу таблицу
    title = hand_base.columns
    frame = tk.Frame(win, height=500, width=1000)
    tree = ttk.Treeview(frame, columns=title, height=20, show="headings", selectmode='browse')
    [tree.heading('#' + str(x + 1), text=title[x]) for x in range(len(title))]
    for i in selected_base.index:
        insert = list(selected_base.iloc[i, :])
        tree.insert('', 'end', values=insert)
    # меняем ширину столбца для красоты
    for i in range(1, len(title) + 1):
        tree.column('#' + str(i), width=100, stretch=False)
    # сроллбары для нее
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set)
    tree.configure(xscrollcommand=hsb.set)

    # пакуем все в фрейм, а его по сетке в окно
    vsb.pack(side='right', fill='both')
    hsb.pack(side='bottom', fill='both')
    tree.pack(side='top')
    return frame


root = setup()
root.minsize(800, 200)
root.maxsize(1200, 800)

root.mainloop()
