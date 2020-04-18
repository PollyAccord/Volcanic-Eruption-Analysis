import tkinter as tk
from tkinter import filedialog
import tkinter.ttk as ttk
import interface as ui
import base_handling as hand_base
import os

save_icon = None
add_icon = None

"""
Автор: 
Цель: создание главного окна и расстановка всех его компонентов 
Вход: Нет 
Выход: объект главного окна
"""


def setup():
    win = tk.Tk()
    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(1, weight=100)
    win.grid_rowconfigure(3, weight=1)
    global save_icon
    global add_icon
    save_icon = tk.PhotoImage(file="pic/save_icon.gif")
    add_icon = tk.PhotoImage(file="pic/add_icon.gif")
    win.title('Volcano Analyse')

    # создаем и заполняем строчку меню --------------------
    # todo: придумать и заполнить до конца (возможно перенести в interface модуль)
    menubar = tk.Menu(win)
    file = tk.Menu(menubar, tearoff=0)
    file.add_command(label="New", command=load_button)
    file.add_command(label="Exit", command=win.quit)
    menubar.add_cascade(label="File", menu=file)

    edit = tk.Menu(menubar, tearoff=0)
    edit.add_command(label="smth")
    menubar.add_cascade(label="Edit", menu=edit)

    about = tk.Menu(menubar, tearoff=0)
    about.add_command(label="smth")
    menubar.add_cascade(label="About", menu=about)
    win.config(menu=menubar)
    # заканчивааем с меню ------------------------------

    # фрейм кнопочек ----------------------------------
    tools_frame = tk.Frame(win, bg="black")
    add_button = tk.Button(tools_frame, image=add_icon)
    save_button = tk.Button(tools_frame, image=save_icon)

    add_button.bind("<Button-1>", load_button)

    add_button.grid(row=0, column=0, padx=2, pady=2, sticky="NSEW")
    save_button.grid(row=0, column=1, padx=2, pady=2, sticky="NSEW")
    tools_frame.grid(row=0, column=0, columnspan=12, sticky="NSEW")
    # конец кнопочкам ----------------------------------

    # лист для баз данных -----------------------------
    list_frame = tk.Frame(win)
    lsb_base = tk.Listbox(list_frame, selectmode='browse')
    ui.base_list = lsb_base
    for name, base in hand_base.work_list.items():
        lsb_base.insert(tk.END, name)
    lsb_base.bind('<Double-Button-1>', lambda *args: open_base(lsb_base.get(lsb_base.curselection())))
    lsb_base.pack(side="left", fill="y", expand=True)
    list_frame.grid(row=1, column=0, columnspan=3, rowspan=2, sticky="NSW")
    # сделали лист ----------------------------------


    # win.grid_columnconfigure(0, weight=1)
    # win.grid_rowconfigure(0, weight=1)
    # ui.mainframe = tk.Frame(win)
    # # создание элементов
    #
    #
    # # кнопка добавления базы
    # add_button = tk.Button(ui.mainframe, text='Добавить')
    # add_button.bind('<Button-1>', load_button)
    # # раставляем по сетке
    #
    # add_button.grid(row=1, column=0, sticky="nsew")
    # ui.mainframe.grid(row=0, column=0)
    # ui.currentframe = ui.mainframe
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
    path = filedialog.askopenfilename(initialdir="base/",
                                      filetypes=(("Database files", "*.csv;"), ("All files", "*.*")))
    path = path.replace('/', "\\")
    if os.path.exists(path):
        base_name = hand_base.read_base(path)
        ui.base_list.insert(tk.END, base_name)
    else:
        # кидаем exception
        pass
    return "break"


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
    # back_button = tk.Button(frame, text='Добавить базу базу')
    # back_button.bind('<Button-1>', back)
    # back_button.grid(row=0, column=0, sticky="W")
    frame.grid(row=1, column=0)
    ui.currentframe = frame
    ui.currentframe.tkraise()


"""
новая функция
"""


def create_workspace(win, selected_base):
    # создаем и заполняем нашу таблицу
    title = hand_base.columns
    frame = tk.Frame(win)
    tree = ttk.Treeview(frame, columns=title, height=15, show="headings", selectmode='browse')
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

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
widthRatio = 1200 / 1920
heightRatio = 800 / 1080
app_width = int(screen_width * widthRatio)
app_height = int(screen_height * heightRatio)
geometry = "1000x600+" + str(screen_width // 2 - app_width // 2) + "+" + str(screen_height // 2 - app_height // 2)
root.geometry(geometry)
root.mainloop()
