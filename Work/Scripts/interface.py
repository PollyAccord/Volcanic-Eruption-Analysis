import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb

import globals as glob
import numpy as np
import pandas as pd

from Work.Library import error_edit_windows as err

# набор глобальных переменных
sort = True  # показывает, как отсортирована таблица и dataframe
load_event = None  # глобальная переменная для передачи объекта функции загрузки базы данных
# иконки
save_icon = None
add_icon = None
edit_icon = None
load_icon = None

# events ---------------------------------------------------------------------------------------

"""
Автор:  
Цель:   обработчик события кнопки изменения поля таблицы
Вход:   корневое окно tkinter для создания окна редактирования, список активных столбцов таблицы            
Выход:  нет
"""


def edit_event(win, title_columns):
    # открыта ли база?
    if not is_db_open():
        return "break"
    # получаем изменяемую строчку
    index = glob.table4base.index(glob.table4base.selection())
    curr_item = glob.current_base.iloc[index, :]
    # создаем дочернее окно
    edit_win = tk.Toplevel(win)
    edit_win.title("Изменения данных поля таблицы")
    # распологаем все необходимые элементы в этих фреймах
    frame4labels = tk.Frame(edit_win)
    frame4entries = tk.Frame(edit_win)
    frame4button = tk.Frame(edit_win)
    list4changes = {}
    for i in title_columns:
        # все значения будут строкой, при сохранении в dataframe мы осуществим приведение чисел к числовому типу
        text = tk.StringVar()
        # если атрибут nan или 0, то вместо него отображаем пустую строчку
        if pd.isna(curr_item[i]) or (i in ['Year', 'Month', 'Day'] and curr_item[i] == 0):
            text.set("")
        else:
            text.set(curr_item[i])
        list4changes[i] = text
        tk.Label(frame4labels, text=i + ":", anchor="e").pack(side="top", fill="x", expand=True, pady=5)
        tk.Entry(frame4entries, textvariable=text).pack(side="top", fill="x", expand=True, pady=5)
    save_changes_button = tk.Button(frame4button, text="Сохранить")
    save_changes_button.pack(expand=False)
    save_changes_button.bind("<Button-1>", lambda *args: make_changes_event(edit_win, index, list4changes))
    edit_win.rowconfigure(0, pad=5)
    edit_win.rowconfigure(1, pad=5)
    edit_win.columnconfigure(0, pad=5)
    edit_win.columnconfigure(1, pad=5)
    frame4labels.grid(row=0, column=0, sticky="NSW")
    frame4entries.grid(row=0, column=1, sticky="NSW")
    frame4button.grid(row=1, column=0, columnspan=2, sticky="NSEW")


"""
Автор: 
Цель:  
Вход:   
Выход:  
"""


def add_event(*args):
    # todo: сделать добавление новой базы
    pass


"""
Автор: 
Цель:   
Вход:   
Выход:   
"""


def save_event(*args):
    # открыта ли база?
    if not is_db_open():
        return "break"
    if not is_saved():
        glob.current_base_name = glob.current_base_name.replace('*', '')
        glob.work_list[glob.current_base_name] = glob.current_base
        update_list()
    # todo: сохранение в файл БД из словаря


"""
Автор: 
Цель:   обработчик события кнопки сохранения в окне редактирования поля таблицы 
Вход:   объект окна редактирования tkinter для его закрытия после нажатия кнопки сохранить, 
        текущий индекс выбранного поля таблицы, 
        новые значения для записи в поле таблицы. 
Выход:  нет 
"""


def make_changes_event(win, index, new_values):
    # приводим все числа к числовому типу
    glob.current_base.iloc[index, :] = [pd.to_numeric(x.get(), errors="ignore") for x in new_values.values()]
    # заменяем пустые строчки на nan и приводим тип всех столбцов таблицы к нужному типу
    cast_datatypes()
    glob.work_list[glob.current_base_name] = glob.current_base
    item = glob.table4base.selection()
    for key, value in new_values.items():
        glob.table4base.set(item, column=key, value=value.get())
    glob.current_base_name += "*"
    update_list()
    win.destroy()
    update_workspace()


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
    glob.current_base, glob.current_base_name = dict4db.get(
        glob.base_list.get(selected).replace('*', '')), glob.base_list.get(selected)
    work_frame = create_workspace(win, glob.current_base, title_columns)
    # work_frame.grid(row=1, column=1, rowspan=2, sticky="NSW")
    win.forget(1)
    win.add(work_frame, weight=10000)


def workspace_onclick_event(event):
    global sort
    sort = not sort
    tree = glob.table4base
    if tree.identify_region(event.x, event.y) == "heading":
        column = tree.identify_column(event.x)
        index4column = int(column[1:])
        glob.current_base = glob.current_base.sort_values(by=glob.columns[index4column - 1], axis=0, ascending=sort,
                                                          ignore_index=True)
        update_workspace()


#  ---------------------------------------------------------------------------------------
# frames =======================================================================================

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
    load_button = tk.Button(tools_frame, image=load_icon, relief="groove", bd=0, bg="white")
    add_field_button = tk.Button(tools_frame, relief="raised", text="Добавить поле", bd=2, bg="white")

    add_button.bind("<Button-1>", add_event)
    save_button.bind("<Button-1>", save_event)
    edit_button.bind("<Button-1>", lambda *args: edit_event(win, title_columns))
    load_button.bind("<Button-1>", load_event)
    add_field_button.bind("<Button-1>", lambda *args: add_inf(win, title_columns))

    add_button.grid(row=0, column=0, padx=2, pady=2, sticky="NSEW")
    load_button.grid(row=0, column=1, padx=2, pady=2, sticky="NSEW")
    save_button.grid(row=0, column=2, padx=2, pady=2, sticky="NSEW")
    edit_button.grid(row=0, column=3, padx=2, pady=2, sticky="NSEW")
    add_field_button.grid(row=0, column=4, padx=2, pady=2, sticky="NSEW")
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
    list_frame = tk.LabelFrame(win, labelanchor='n', text='Базы данных', bd=0, padx=5, pady=5, relief=tk.RIDGE,
                               bg='white')
    lsb_base = tk.Listbox(list_frame, selectmode='browse')
    for name, base in dict4db.items():
        lsb_base.insert(tk.END, name)
    glob.base_list = lsb_base
    lsb_base.bind('<Double-Button-1>',
                  lambda *args: open_base(win, lsb_base.curselection(), dict4db, title_columns))
    lsb_base.pack(side="left", fill="both", expand=True)
    return list_frame
    # list_frame.grid(row=1, column=0, sticky="NSEW")


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
    file.add_command(label="Load", command=load_event)
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
    frame = tk.LabelFrame(win, labelanchor='n', text='Данные', bd=0, pady=5, padx=5, relief=tk.RIDGE, bg='white')
    tree = ttk.Treeview(frame, columns=title, height=30, show="headings", selectmode='browse')
    [tree.heading('#' + str(x + 1), text=title[x]) for x in range(len(title))]
    for i in range(len(selected_base.index)):
        insert = list(selected_base.iloc[i, :])
        tree.insert('', 'end', iid=i, values=insert)
    # меняем ширину столбца для красоты
    for i in range(1, len(title) + 1):
        tree.column('#' + str(i), width=100, stretch=False)
    # скроллбары для нее
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.bind("<Button-1>", lambda event: workspace_onclick_event(event))
    tree.configure(yscrollcommand=vsb.set)
    tree.configure(xscrollcommand=hsb.set)

    # пакуем все в фрейм, а его по сетке в окно

    glob.table4base = tree
    hsb.pack(side='bottom', fill='both')
    vsb.pack(side='right', fill='both')
    tree.pack(side='top')
    return frame


#  =======================================================================================
# updates =======================================================================================

"""
Автор: 
Цель:   
Вход:   
Выход:   
"""


def update_list():
    glob.base_list.delete(glob.current_base_list_id)
    glob.base_list.insert(glob.current_base_list_id, glob.current_base_name)


"""
Автор: 
Цель:   
Вход:   
Выход:   
"""


def update_workspace():
    for i in range(len(glob.current_base.index)):
        insert = glob.current_base.iloc[i, :]
        for j in glob.columns:
            glob.table4base.set(i, column=j, value=insert[j])


# =======================================================================================


def is_db_open():
    if glob.current_base is None:
        err.error("База не выбранна!")
        return False
    return True


"""
Автор: 
Цель:   
Вход:   
Выход:   
"""


def is_saved():
    flag = True
    if "*" in glob.current_base_name:
        flag = False
    return flag


"""
Автор: 
Цель:   при добавлении в таблицу измененных пользователем данных могут возникнуть nan значения, 
        их мы меняем на пустые строки или на 0, так же nan меняет типы столбцов на другой, 
        здесь мы обратно приводим тип столбцов к нужному 
Вход:  нет
Выход:  нет 
"""


def cast_datatypes():
    glob.current_base[['Year', 'Month', 'Day']] = glob.current_base[['Year', 'Month', 'Day']].replace(np.nan, 0)
    glob.current_base[['Name', 'Location', 'Country', 'Type', 'Agent', 'TSU', 'EQ']] = glob.current_base[
        ['Name', 'Location', 'Country', 'Type', 'Agent', 'TSU', 'EQ']].replace(np.nan, "")
    glob.current_base = glob.current_base.astype({'Year': 'int32', 'Month': 'int32', 'Day': 'int32',
                                                  'Latitude': 'float64', 'Longitude': 'float64', 'VEI': 'float64',
                                                  'DEATHS': 'float64', 'INJURIES': 'float64', 'MISSING': 'float64',
                                                  'DAMAGE_MILLIONS_DOLLARS': 'float64'})


"""
    Автор:Подкопаева П.
    Цель: Добавление новых элементов в базу данных (окно)
    Вход: Нет
    Выход: Нет
"""


def add_inf(win, title_columns):
    if not is_db_open():
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
        glob.current_base = glob.current_base.append(
            {k: pd.to_numeric(v.get(), errors="ignore") for k, v in list4values.items()}, ignore_index=True)
        glob.work_list[glob.current_base_name] = glob.current_base
        new_item = glob.table4base.insert('', 'end', iid=len(glob.current_base.index) - 1)
        for i in title_columns:
            glob.table4base.set(new_item, column=i, value=list4values[i].get())
        mb.showinfo("Сообщение", "Занесено в базу")
        root.destroy()
    else:
        err.error("Данные введены некорректно, повторите попытку")
