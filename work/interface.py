import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb
import numpy as np
import error_edit_windows as err
import globals as glob
import pandas as pd

load_event = None
list4ComboBox = ['Month', 'VEI', 'Agent']
list4RadioButton = ['TSU', 'EQ']
save_icon = None
add_icon = None
edit_icon = None

"""
Автор:  
Цель:   обработчик события кнопки изменения поля таблицы
Вход:   корневое окно tkinter для создания окна редактирования, список активных столбцов таблицы            
Выход:  нет
"""


def edit_event(win, title_columns):
    if not err.is_db_open():
        return "break"
    index = glob.table4base.index(glob.table4base.selection())
    curr_item = glob.current_base.iloc[index, :]
    edit_win = tk.Toplevel(win)
    edit_win.title("Изменения данных поля таблицы")
    frame4labels = tk.Frame(edit_win)
    frame4entries = tk.Frame(edit_win)
    frame4button = tk.Frame(edit_win)
    list4changes = {}
    for i in title_columns:
        text = tk.StringVar()
        text.set(curr_item[i])
        list4changes[i] = text
        tk.Label(frame4labels, text=i + ":", anchor="e").pack(side="top", fill="x", expand=True, pady=5)
        tk.Entry(frame4entries, textvariable=text).pack(side="top", fill="x", expand=True, pady=5)
    save_changes_button = tk.Button(frame4button, text="Сохранить")
    save_changes_button.pack(expand=False)
    save_changes_button.bind("<Button-1>", lambda *args: save_changes_event(edit_win, index, list4changes))
    edit_win.rowconfigure(0, pad=5)
    edit_win.rowconfigure(1, pad=5)
    edit_win.columnconfigure(0, pad=5)
    edit_win.columnconfigure(1, pad=5)
    frame4labels.grid(row=0, column=0, sticky="NSW")
    frame4entries.grid(row=0, column=1, sticky="NSW")
    frame4button.grid(row=1, column=0, columnspan=2, sticky="NSEW")


"""
Автор: 
Цель:   обработчик события кнопки сохранения в окне редактирования поля таблицы 
Вход:   объект окна редактирования tkinter для его закрытия после нажатия кнопки сохранить, 
        текущий индекс выбранного поля таблицы, 
        новые значения для записи в поле таблицы. 
Выход:  нет 
"""


def save_changes_event(win, index, new_values):
    glob.current_base.iloc[index, :] = [x.get() for x in new_values.values()]
    item = glob.table4base.selection()
    for key, value in new_values.items():
        glob.table4base.set(item, column=key, value=value.get())
    win.destroy()


"""
Автор: 
Цель:   создание панели инструментов в главном окне
Вход:   объект главного окна, 
        список активных столбцов таблицы.
Выход:  нет 
"""


def create_toolbar(win, title_columns):
    global load_event
    tools_frame = tk.Frame(win, bg="white")
    add_button = tk.Button(tools_frame, image=add_icon, relief="groove", bd=0, bg="white")
    save_button = tk.Button(tools_frame, image=save_icon, relief="groove", bd=0, bg="white")
    edit_button = tk.Button(tools_frame, image=edit_icon, relief="groove", bd=0, bg="white")
    add_field_button = tk.Button(tools_frame, relief="raised", text="Добавить поле", bd=2, bg="white")

    add_button.bind("<Button-1>", load_event)
    edit_button.bind("<Button-1>", lambda *args: edit_event(win, title_columns))
    add_field_button.bind("<Button-1>", lambda *args: add_inf(win, title_columns))

    add_button.grid(row=0, column=0, padx=2, pady=2, sticky="NSEW")
    save_button.grid(row=0, column=1, padx=2, pady=2, sticky="NSEW")
    edit_button.grid(row=0, column=2, padx=2, pady=2, sticky="NSEW")
    add_field_button.grid(row=0, column=3, padx=2, pady=2, sticky="NSEW")
    tools_frame.grid(row=0, column=0, columnspan=12, sticky="NSEW")


"""
Автор: 
Цель:   создание виджета Listbox для выбора загруженных баз даннных
Вход:   объект главного окна,
        словарь для хранения текущих загруженных баз данных (имя: база данных),
        список активных столбцов таблицы.
Выход:  нет 
"""


def create_list4db(win, dict4db, title_columns):
    list_frame = tk.Frame(win)
    lsb_base = tk.Listbox(list_frame, selectmode='browse')
    for name, base in dict4db.items():
        lsb_base.insert(tk.END, name)
    glob.base_list = lsb_base
    lsb_base.bind('<Double-Button-1>',
                  lambda *args: open_base(win, lsb_base.curselection(), dict4db, title_columns))
    lsb_base.pack(side="left", fill="y", expand=True)
    list_frame.grid(row=1, column=0, sticky="NSW")


"""
Автор: 
Цель:   открывает загруженную базу данных и создает для нее таблицу с полями, добавляя ее на главный экран
Вход:   объект главного окна,
        ключ (имя) выбранной базы,
        словарь текущий загруженных баз данных (имя: база данных),
        список активных столбцов таблицы.
Выход:  нет 
"""


def open_base(win, selected, dict4db, title_columns):
    glob.current_base_list_id = selected
    glob.current_base, glob.current_base_name = dict4db.get(glob.base_list.get(selected)), glob.base_list.get(selected)
    work_frame = create_workspace(win, glob.current_base, title_columns)
    work_frame.grid(row=1, column=1, rowspan=2, sticky="NSW")


"""
Автор: 
Цель:   создает меню на главном окне
Вход:   объект главного окна.
Выход:  нет 
"""


def create_menu(win):
    global load_event
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


"""
    Автор: 
    Цель:   создает рабочее пространство с таблицей 
    Вход:   объект главного окна,
            выбранная база,
            активные столбцы.
    Выход:  нет 
"""


def create_workspace(win, selected_base, title_columns):
    # создаем и заполняем нашу таблицу
    title = title_columns
    frame = tk.Frame(win)
    tree = ttk.Treeview(frame, columns=title, height=30, show="headings", selectmode='browse')
    [tree.heading('#' + str(x + 1), text=title[x]) for x in range(len(title))]
    for i in range(len(selected_base.index)):
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

    glob.table4base = tree
    hsb.pack(side='bottom', fill='both')
    vsb.pack(side='right', fill='both')
    tree.pack(side='top', expand=True, fill="y")
    return frame


"""
    Автор:Подкопаева П.
    Цель: Добавление новых элементов в базу данных (окно)
    Вход: Нет
    Выход: Нет
"""


def add_inf(win, title_columns):
    if not err.is_db_open():
        return "break"
    root = tk.Toplevel(win)
    root.title("Окно ввода данных")

    Year = tk.IntVar()
    Year_label = tk.Label(root, text="Год извержения:")
    Year_label.grid(row=0, column=0, sticky="w")
    Year_entry = tk.Entry(root, textvariable=Year)
    Year_entry.grid(row=0, column=1, padx=5, pady=5)

    cmb_month = ttk.Combobox(root)
    Month_label = tk.Label(root, text="Месяц извержения:")
    Month_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    cmb_month['values'] = ('1', '2', '3', '4', '5', '6', '7',
                           '8', '9', '10', '11', '12')
    cmb_month.current(0)
    cmb_month.grid(column=1, row=1)

    Day = tk.IntVar()
    Day_label = tk.Label(root, text="День извержения:")
    Day_label.grid(row=2, column=0, sticky="w")
    Day_entry = tk.Entry(root, textvariable=Day)
    Day_entry.grid(row=2, column=1, padx=5, pady=5)

    name = tk.StringVar()
    name_label = tk.Label(root, text="Название вулкана:")
    name_label.grid(row=3, column=0, sticky="w")
    name_entry = tk.Entry(root, textvariable=name)
    name_entry.grid(row=3, column=1, padx=5, pady=5)

    Type = tk.StringVar()
    Type_label = tk.Label(root, text="Тип вулкана:")
    Type_label.grid(row=4, column=0, sticky="w")
    Type_entry = tk.Entry(root, textvariable=Type)
    Type_entry.grid(row=4, column=1, padx=5, pady=5)

    Height = tk.IntVar()
    Height_label = tk.Label(root, text="Высота вулкана (в метрах):")
    Height_label.grid(row=5, column=0, sticky="w")
    Height_entry = tk.Entry(root, textvariable=Height)
    Height_entry.grid(row=5, column=1, padx=5, pady=5)

    country = tk.StringVar()
    country_label = tk.Label(root, text="Страна:")
    country_label.grid(row=6, column=0, sticky="w")
    country_entry = tk.Entry(root, textvariable=country)
    country_entry.grid(row=6, column=1, padx=5, pady=5)

    location = tk.StringVar()
    location_label = tk.Label(root, text="Расположение вулкана:")
    location_label.grid(row=7, column=0, sticky="w")
    location_entry = tk.Entry(root, textvariable=location)
    location_entry.grid(row=7, column=1, padx=5, pady=5)

    Latitude = tk.IntVar()
    Latitude_label = tk.Label(root, text="Широта:")
    Latitude_label.grid(row=8, column=0, sticky="w")
    Latitude_entry = tk.Entry(root, textvariable=Latitude)
    Latitude_entry.grid(row=8, column=1, padx=5, pady=5)

    Longtitude = tk.IntVar()
    Longtitude_label = tk.Label(root, text="Долгота:")
    Longtitude_label.grid(row=9, column=0, sticky="w")
    Longtitude_entry = tk.Entry(root, textvariable=Longtitude)
    Longtitude_entry.grid(row=9, column=1, padx=5, pady=5)

    cmb_VEI = ttk.Combobox(root)
    VEI_label = tk.Label(root, text="Индекс взрывоопасности:")
    VEI_label.grid(row=10, column=0, sticky="w", padx=5, pady=5)
    cmb_VEI['values'] = ('0', '1', '2', '3', '4', '5', '6', '7', '8')
    cmb_VEI.current(0)
    cmb_VEI.grid(column=1, row=10)

    cmb_agent = ttk.Combobox(root)
    Agent_label = tk.Label(root, text="Причина извержения:")
    Agent_label.grid(row=10, column=3, sticky="w", padx=5, pady=5)
    cmb_agent['values'] = ('A', 'E', 'F', 'G', 'I', 'L', 'M', 'm', 'P', 'S', 'T', 'W')
    # inf_button = Button(root, text="Информация о причинах", command=mb.showinfo(
    # "Информация", "Здесь будет информация с расшифровкой причин").grid(row = 11, column = 5, padx=5, pady=5, sticky="e"))
    cmb_agent.current(0)
    cmb_agent.grid(column=4, row=10)

    Deaths = tk.IntVar()
    Deaths_label = tk.Label(root, text="Количество смертей:")
    Deaths_label.grid(row=13, column=0, sticky="w")
    Deaths_entry = tk.Entry(root, textvariable=Deaths)
    Deaths_entry.grid(row=13, column=1, padx=5, pady=5)

    Injured = tk.IntVar()
    Injured_label = tk.Label(root, text="Количество пострадавших:")
    Injured_label.grid(row=14, column=0, sticky="w")
    Injured_entry = tk.Entry(root, textvariable=Injured)
    Injured_entry.grid(row=14, column=1, padx=5, pady=5)

    Lost = tk.IntVar()
    Lost_label = tk.Label(root, text="Количество пропавших:")
    Lost_label.grid(row=15, column=0, sticky="w")
    Lost_entry = tk.Entry(root, textvariable=Lost)
    Lost_entry.grid(row=15, column=1, padx=5, pady=5)

    Damage = tk.IntVar()
    Damage_label = tk.Label(root, text="Ущерб в млн долларов:")
    Damage_label.grid(row=16, column=0, sticky="w")
    Damage_entry = tk.Entry(root, textvariable=Damage)
    Damage_entry.grid(row=16, column=1, padx=5, pady=5)

    TSU = tk.BooleanVar()
    TSU.set(False)
    TSU1 = ttk.Checkbutton(root, text="Было цунами?", var=TSU)
    TSU1.grid(column=0, row=17)

    EQ = tk.BooleanVar()
    EQ.set(False)
    EQ1 = ttk.Checkbutton(root, text="Было землетрясение?", var=EQ)
    EQ1.grid(column=2, row=17)

    list4values = {'Year': Year, 'Month': cmb_month, 'Day': Day, 'Name': name, 'Location': location, 'Country': country,
                   'Latitude': Latitude, 'Longitude': Longtitude, 'Elevation': Height, 'Type': Type, 'VEI': cmb_VEI,
                   'Agent': cmb_agent, 'DEATHS': Deaths, 'INJURIES': Injured, 'MISSING': Lost,
                   'DAMAGE_MILLIONS_DOLLARS': Damage, 'TSU': TSU, 'EQ': EQ}
    message_button = tk.Button(root, text="Ввести",
                               command=lambda *args: accept(root, list4values, title_columns))
    message_button.grid(row=19, column=3, padx=5, pady=5, sticky="e")


def accept(root, list4values, title_columns):
    flag = True
    if (list4values['Day'].get() > 29) and (list4values['Month'].get() == 2):
        flag = False
    elif list4values['Day'].get() > 31 or list4values['Day'].get() < 1:
        flag = False
    if list4values['Elevation'].get() > 6887:
        flag = False
    if (list4values['Latitude'].get() > 180) or (list4values['Latitude'].get() < -180):
        flag = False
    if (list4values['Longitude'].get() > 180) or (list4values['Longitude'].get() < -180):
        flag = False
    if flag:
        glob.current_base = glob.current_base.append({k: v.get() for k, v in list4values.items()}, ignore_index=True)
        glob.work_list[glob.current_base_name] = glob.current_base

        new_item = glob.table4base.insert('', 'end')
        for i in title_columns:
            glob.table4base.set(new_item, column=i, value=list4values[i].get())
        mb.showinfo("Сообщение", "Занесено в базу")
        root.destroy()
    else:
        err.error("Данные введены некорректно, повторите попытку")

def db_is_not_saved():
    pass