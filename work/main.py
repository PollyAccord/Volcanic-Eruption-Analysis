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
    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(1, weight=100)
    win.grid_rowconfigure(3, weight=1)

    win.grid_columnconfigure(0, weight=1)
    win.grid_columnconfigure(1, weight=100)

    ui.save_icon = tk.PhotoImage(file="pic/save_icon.gif")
    ui.add_icon = tk.PhotoImage(file="pic/add_icon.gif")
    ui.edit_icon = tk.PhotoImage(file="pic/edit_icon.gif")
    win.title('Volcano Analyse')

    # создаем и заполняем строчку меню --------------------
    # todo: придумать и заполнить до конца (возможно перенести в interface модуль)
    menubar = tk.Menu(win)
    file = tk.Menu(menubar, tearoff=0)
    file.add_command(label="New", command=load_event)
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
    tools_frame = tk.Frame(win, bg="white")
    add_button = tk.Button(tools_frame, image=ui.add_icon, relief="groove", bd=0, bg="white")
    save_button = tk.Button(tools_frame, image=ui.save_icon, relief="groove", bd=0, bg="white")
    edit_button = tk.Button(tools_frame, image=ui.edit_icon, relief="groove", bd=0, bg="white")

    add_button.bind("<Button-1>", load_event)
    edit_button.bind("<Button-1>", lambda *args: edit_event(win))

    add_button.grid(row=0, column=0, padx=2, pady=2, sticky="NSEW")
    save_button.grid(row=0, column=1, padx=2, pady=2, sticky="NSEW")
    edit_button.grid(row=0, column=2, padx=2, pady=2, sticky="NSEW")
    tools_frame.grid(row=0, column=0, columnspan=12, sticky="NSEW")
    # конец кнопочкам ----------------------------------

    # лист для баз данных -----------------------------
    list_frame = tk.Frame(win)
    lsb_base = tk.Listbox(list_frame, selectmode='browse')
    ui.base_list = lsb_base
    for name, base in hand_base.work_list.items():
        lsb_base.insert(tk.END, name)
    lsb_base.bind('<Double-Button-1>', lambda *args: open_base(win, lsb_base.get(lsb_base.curselection())))
    lsb_base.pack(side="left", fill="y", expand=True)
    list_frame.grid(row=1, column=0, sticky="NSW")
    # сделали лист ----------------------------------

    # label приглашение к выбору --------------------
    pls_select_frame = tk.Frame(win, bg="white")
    lbl_select_pls = tk.Label(pls_select_frame, text="Пожалуйста, выберете базу данных", bg="white")
    lbl_select_pls.pack(expand=True, fill="both")
    pls_select_frame.grid(row=1, column=1, rowspan=2, sticky="NSEW")
    # ----------------------------------------------

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


def load_event(*args):
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


def edit_event(win, *args):
    index = ui.table4base.index(ui.table4base.selection())
    curr_item = hand_base.current_base.iloc[index, :]
    edit_win = tk.Toplevel(win)
    edit_win.title("Change field")
    frame4labels = tk.Frame(edit_win)
    frame4entries = tk.Frame(edit_win)
    frame4button = tk.Frame(edit_win)
    list4changes = {}
    for i in hand_base.columns:
        text = tk.StringVar()
        text.set(curr_item[i])
        list4changes[i] = text
        tk.Label(frame4labels, text=i+":", anchor="e").pack(side="top", fill="x", expand=True, pady=5)
        tk.Entry(frame4entries, textvariable=text).pack(side="top", fill="x", expand=True, pady=5)
    save_changes_button = tk.Button(frame4button,  text="Save")
    save_changes_button.pack(expand=False)
    save_changes_button.bind("<Button-1>", lambda *args: save_changes_event(edit_win, index, list4changes))
    edit_win.rowconfigure(0, pad=5)
    edit_win.rowconfigure(1, pad=5)
    edit_win.columnconfigure(0, pad=5)
    edit_win.columnconfigure(1, pad=5)
    frame4labels.grid(row=0, column=0, sticky="NSW")
    frame4entries.grid(row=0, column=1, sticky="NSW")
    frame4button.grid(row=1, column=0, columnspan=2, sticky="NSEW")


def save_changes_event(win, index, new_values):
    hand_base.current_base.iloc[index, :] = [x.get() for x in new_values.values()]
    item = ui.table4base.selection()
    for key, value in new_values.items():
        ui.table4base.set(item, column=key, value=value.get())
    win.destroy()



"""
Автор:  
Цель: открытие базы данных по двойному нажатию на виджет списка 
Вход: Нет 
Выход: нет
"""


def open_base(win, selected):
    hand_base.current_base = hand_base.work_list.get(selected)
    workframe = create_workspace(win, hand_base.current_base)
    workframe.grid(row=1, column=1, rowspan=2, sticky="NSW")
    

"""
новая функция
"""


def create_workspace(win, selected_base):
    # создаем и заполняем нашу таблицу
    title = hand_base.columns
    frame = tk.Frame(win)
    tree = ttk.Treeview(frame, columns=title, height=30, show="headings", selectmode='browse')
    [tree.heading('#' + str(x + 1), text=title[x]) for x in range(len(title))]
    for i in selected_base.index:
        insert = list(selected_base.iloc[i, :])
        tree.insert('', 'end', values=insert)
    # меняем ширину столбца для красоты
    for i in range(1, len(title) + 1):
        tree.column('#' + str(i), width=100, stretch=False)
    # скроллбары для нее
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set)
    tree.configure(xscrollcommand=hsb.set)

    # пакуем все в фрейм, а его по сетке в окно
    ui.table4base = tree
    hsb.pack(side='bottom', fill='both')
    vsb.pack(side='right', fill='both')
    tree.pack(side='top', expand=True, fill="y")
    return frame


root = setup()
root.config(background="white")
root.minsize(100, 400)
root.maxsize(1800, 1000)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
widthRatio = 1200 / 1920
heightRatio = 800 / 1080
app_width = int(screen_width * widthRatio)
app_height = int(screen_height * heightRatio)
geometry = "1000x600+" + str(screen_width // 2 - app_width // 2) + "+" + str(screen_height // 2 - app_height // 2)
root.geometry(geometry)
root.mainloop()
