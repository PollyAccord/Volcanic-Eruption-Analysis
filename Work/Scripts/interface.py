import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb

import pandas as pd

from Library import error_edit_windows as err
from Scripts import constants
from Scripts import globalvars as glob


# events ---------------------------------------------------------------------------------------

def close_event(pane: ttk.Panedwindow, save):
    """
        Автор:
        Цель:   закрывает открытую базу и показывает приглащение к открытию новой на правой стороне pane,
                save вызывается для сохранения базы, по решению пользователя
        Вход: pane - растягивающийся виджет, save - объект функции save_event из main
        Выход: нет
    """

    # открыта ли база?
    if not glob.is_db_open():
        return "break"
    # сохранена ли база?
    if not glob.is_saved():
        ans = err.yes_no("Сохранить изменения?")
        if ans:
            save()
    glob.delete_current_base()
    pane.forget(1)
    pls_select_frame = show_invitation(pane)
    pane.add(pls_select_frame, weight=9)


def remove_inf():
    """
        Автор:
        \nЦель: удаляет строку из таблицы
        \nВход: корневое окно tkinter для создания окна редактирования, список активных столбцов таблицы
        \nВыход: нет
    """
    # открыта ли база?
    if not glob.is_db_open():
        return "break"
    # пуста ли база?
    if glob.current_base.empty:
        err.error("База пуста")
        return "break"
    ans = err.yes_no("Вы точно хотите удалить строчку?")
    if ans:
        # todo: можно ли оптимизировать?
        index = glob.table4base.index(glob.table4base.selection())
        glob.table4base.delete(list(glob.current_base.index)[-1])
        glob.current_base = glob.current_base.drop(index=index)
        glob.current_base.reset_index(inplace=True, drop=True)
        glob.mark_changes()
        glob.update_workspace()
        glob.update_list()


def edit_event(root: tk.Tk):
    """
        Автор:
        Цель:   обработчик события кнопки изменения поля таблицы, открывает окно для изменения данных
        Вход:   корневое окно tkinter для создания окна редактирования
        Выход:  нет
    """
    # открыта ли база?
    if not glob.is_db_open():
        return "break"
    # пуста ли база?
    if glob.current_base.empty:
        err.error("База пуста")
        return "break"
    # получаем изменяемую строчку
    index = glob.table4base.index(glob.table4base.selection())
    curr_item = glob.current_base.iloc[index, :]
    # создаем дочернее окно
    edit_win = tk.Toplevel(root)
    edit_win.resizable(0, 0)
    edit_win.title("Изменения данных поля таблицы")
    # распологаем все необходимые элементы в этих фреймах
    frame4check4labels = tk.Frame(edit_win)
    frame4check4entries = tk.Frame(edit_win)
    frame4check4button = tk.Frame(edit_win)
    list4changes = {}
    for i in constants.origin_columns:
        # все значения будут строкой
        text = tk.StringVar()
        # если атрибут nan или 0, то вместо него отображаем пустую строчку
        if pd.isna(curr_item[i]) or (i in ['Year', 'Month', 'Day'] and curr_item[i] == 0):
            text.set("")
        else:
            text.set(curr_item[i])
        list4changes[i] = text
        label = tk.Label(frame4check4labels, text=i + ":", anchor="e")
        entry = tk.Entry(frame4check4entries, textvariable=text)
        if i not in glob.columns:
            label.configure(state=tk.DISABLED)
            entry.configure(state='readonly')
        entry.pack(side="top", fill="x", expand=True, pady=5)
        label.pack(side="top", fill="x", expand=True, pady=5)
    save_changes_button = tk.Button(frame4check4button, text="Сохранить")
    save_changes_button.pack(expand=False)
    save_changes_button.bind("<Button-1>", lambda *args: make_changes_event(edit_win, index, list4changes))
    edit_win.rowconfigure(0, pad=5)
    edit_win.rowconfigure(1, pad=5)
    edit_win.columnconfigure(0, pad=5)
    edit_win.columnconfigure(1, pad=5)
    frame4check4labels.grid(row=0, column=0, sticky="NSW")
    frame4check4entries.grid(row=0, column=1, sticky="NSW")
    frame4check4button.grid(row=1, column=0, columnspan=2, sticky="NSEW")


def make_changes_event(win: tk.Toplevel, index: int, new_values: dict):
    """
    Автор:
    Цель:   обработчик события кнопки сохранения в окне редактирования поля таблицы
    Вход:   объект окна редактирования tkinter для его закрытия после нажатия кнопки сохранить,
            текущий индекс выбранного поля таблицы,
            новые значения для записи в поле таблицы.
    Выход:  нет
    """
    # приводим все числа к числовому типу
    glob.current_base.iloc[index, :] = [x.get() for x in new_values.values()]
    # заменяем пустые строчки на nan и приводим тип всех столбцов таблицы к нужному типу
    glob.current_base = glob.correct_base_values(glob.current_base)
    glob.work_list[glob.current_base_name] = glob.current_base
    item = glob.table4base.selection()
    for key, value in new_values.items():
        glob.table4base.set(item, column=key, value=value.get())
    glob.mark_changes()
    glob.update_list()
    glob.update_workspace()
    win.destroy()


def uncheck_all_event(*args):
    """
    Автор:
    Цель:   снимает метки со всех значений columns_selection
    Вход:   нет
    Выход:  нет
    """
    [x.set(0) for x in glob.columns_selection.values()]


def check_all_event(*args):
    """
    Автор:
    Цель:   ставит метки на все значения columns_selection
    Вход:   нет
    Выход:  нет
    """
    [x.set(1) for x in glob.columns_selection.values()]


def apply_column_selection(root: tk.Tk, win: tk.Toplevel, pane: ttk.Panedwindow):
    """
    Автор:
    Цель:   применяет к программме выбор столбцов (изменяет рабочее пространство)
    Вход:   главное окно, побочное окно выбора столбцов, растягивающийся виджет
    Выход:  нет
    """
    if any(glob.columns_selection.values()):
        glob.columns = [x for x in glob.columns_selection.keys() if glob.columns_selection[x].get() == 1]
        open_base(root, pane, glob.current_base_list_id)
        win.destroy()
    else:
        err.error("Не выбран ни один столбец")
        return "break"


def select_columns_event(root: tk.Tk, pane: ttk.Panedwindow):
    """
    Автор:
    Цель:   открывает окно для выбора столбцов, которые надо показать в программе
    Вход:   главное окно, растягивающийся виджет
    Выход:  нет
    """
    # открыта ли база?
    if not glob.is_db_open():
        return "break"
    win = tk.Toplevel(root)
    win.title("Выберете стобцы")
    glob.columns_selection = {k: v
                              for k in constants.origin_columns
                              for v in [tk.BooleanVar() for x in range(len(glob.constants.origin_columns))]
                              }
    frame4check = tk.Frame(win)
    frame4button = tk.Frame(win)

    i = 0
    # раставляем checkbutton'ы и устанавливаем их в активное (отмеченное) положение по текущим показывающимся столбцам
    for text, value in glob.columns_selection.items():
        ttk.Checkbutton(frame4check, style="Selection.TCheckbutton", text=text, variable=value, onvalue=True,
                        offvalue=False).grid(row=i, column=1, sticky='NSEW')
        value.set(True) if text in glob.columns else value.set(False)
        i += 1
    apply_button = tk.Button(frame4button, text="Применить")
    uncheck_all_button = tk.Button(frame4button, text="Снять выбор")
    check_all_button = tk.Button(frame4button, text="Выбрать все")

    apply_button.bind("<Button-1>", lambda *args: apply_column_selection(root, win, pane))
    uncheck_all_button.bind("<Button-1>", uncheck_all_event)
    check_all_button.bind("<Button-1>", check_all_event)

    uncheck_all_button.grid(row=0, column=0, sticky='NSE', padx=5, pady=2)
    check_all_button.grid(row=0, column=1, sticky='NSW', padx=5, pady=2)
    apply_button.grid(row=1, column=0, columnspan=2, sticky='NS', pady=2)
    frame4check.pack(side="top", fill="both", expand=True, padx=10, pady=5)
    frame4button.pack(side="top", fill="both", expand=True, padx=10, pady=5)


def open_base(root: tk.Tk, pane: ttk.Panedwindow, selected: int):
    """
    Автор:
    Цель:   открывает загруженную базу данных и создает для нее таблицу с полями, добавляя ее на главный экран
    Вход:   объект главного окна,
            объект растягиваемого виджета,
            индекс базы в Listbox
    Выход:  нет
    """
    glob.current_base_list_id = selected
    glob.current_base, glob.current_base_name = glob.work_list.get(
        glob.base_list.get(selected).replace('*', '')), glob.base_list.get(selected)
    work_frame4check = create_workspace(root, pane)
    pane.forget(1)
    pane.add(work_frame4check, weight=10000)


def workspace_onclick_event(root, event, mode: str):
    """
        Автор:
        Цель:   обработчик события нажатия на рабочее пространство таблицы данных
        Вход:   объект главного окна,
                информация события,
                вид нажатия (одинарное, двойное)
        Выход:  нет
    """
    glob.sort = not glob.sort
    tree = glob.table4base
    # одиночное нажатие по заголовку - сортировка
    if mode == "Single":
        if tree.identify_region(event.x, event.y) == "heading":
            column = tree.identify_column(event.x)
            index4column = int(column[1:])
            glob.current_base = glob.current_base.sort_values(by=glob.columns[index4column - 1], axis=0,
                                                              ascending=glob.sort, ignore_index=True)
            glob.current_base = glob.correct_base_values(glob.current_base)
            glob.update_workspace()
    # двойное нажатие по полю - редактирование
    elif mode == "Double":
        edit_event(root)


def show_invitation(pane: ttk.Panedwindow) -> tk.Frame:
    """
        Автор:
        Цель:   создание фрейма с приглашением
        Вход:   объект растягивающегося виджета,
        Выход:  фрейм с приглашением
    """
    # label приглашение к выбору
    pls_select_frame4check = tk.Frame(pane, bg="white")
    lbl_select_pls = tk.Label(pls_select_frame4check, text="Пожалуйста, выберете базу данных", bg="white")
    lbl_select_pls.pack(expand=True, fill="both")
    return pls_select_frame4check


def show_form(root, pane, selector, form: str, save):
    if not glob.is_db_open():
        selector.current(0)
    if not glob.is_saved():
        ans = err.yes_no("Сохранить изменения?")
        if ans:
            save()
    glob.selected_form = form
    if form == "Общий вид":
        glob.columns = constants.origin_columns
    elif form == "Вид первый":
        glob.columns = constants.first_form
    elif form == "Вид второй":
        glob.columns = constants.second_form
    elif form == "Вид третий":
        glob.columns = constants.third_form

    open_base(root, pane, glob.current_base_list_id)

#  ---------------------------------------------------------------------------------------
# frame4checks =======================================================================================


def create_toolbar(root: tk.Tk, pane: ttk.Panedwindow, load, save, create, icons: glob.Icons):
    """
    Автор:
    Цель:   создание панели инструментов в главном окне
    Вход:   объект главного окна,
            объект растягивающегося виджета,
            объекты функций load_event, save_event, create_event
            словарь для иконок
    Выход:  нет
    """

    tools_frame4check = tk.Frame(root, bg="white")
    add_button = tk.Button(tools_frame4check, image=icons['add_icon'], relief="groove", bd=0, bg="white")
    save_button = tk.Button(tools_frame4check, image=icons['save_icon'], relief="groove", bd=0, bg="white")
    edit_button = tk.Button(tools_frame4check, image=icons['edit_icon'], relief="groove", bd=0, bg="white")
    load_button = tk.Button(tools_frame4check, image=icons['load_icon'], relief="groove", bd=0, bg="white")
    add_field_button = tk.Button(tools_frame4check, image=icons['add_field_icon'], relief="groove", bd=0, bg="white")
    del_field_button = tk.Button(tools_frame4check, image=icons['del_field_icon'], relief="groove", bd=0, bg="white")
    select_columns = tk.Button(tools_frame4check, text="Столбцы", relief="raised", bd=2, bg="white")
    close_button = tk.Button(tools_frame4check, image=icons['close_icon'], relief="groove", bd=0, bg="white")
    table_normal_forms_selector = ttk.Combobox(tools_frame4check, state='readonly', values=["Общий вид", "Вид первый", "Вид второй", "Вид третий"])
    table_normal_forms_selector.current(0)
    add_button.bind("<Button-1>", create)
    save_button.bind("<Button-1>", save)
    edit_button.bind("<Button-1>", lambda *args: edit_event(root))
    load_button.bind("<Button-1>", load)
    add_field_button.bind("<Button-1>", lambda *args: add_inf(root))
    del_field_button.bind("<Button-1>", lambda *args: remove_inf())
    table_normal_forms_selector.bind("<<ComboboxSelected>>",
                                     lambda event: show_form(root, pane,
                                                             table_normal_forms_selector,
                                                             table_normal_forms_selector.get(),
                                                             save))
    select_columns.bind("<Button-1>", lambda *args: select_columns_event(root, pane))
    close_button.bind("<Button-1>", lambda *args: close_event(pane, save))

    add_button.grid(row=0, column=0, padx=2, pady=2, sticky="NSEW")
    load_button.grid(row=0, column=1, padx=2, pady=2, sticky="NSEW")
    save_button.grid(row=0, column=2, padx=2, pady=2, sticky="NSEW")
    edit_button.grid(row=0, column=3, padx=2, pady=2, sticky="NSEW")
    add_field_button.grid(row=0, column=4, padx=2, pady=2, sticky="NSEW")
    del_field_button.grid(row=0, column=5, padx=2, pady=2, sticky="NSEW")
    table_normal_forms_selector.grid(row=0, column=6, padx=2, pady=2, sticky="NSEW")
    select_columns.grid(row=0, column=7, padx=2, pady=2, sticky="NSEW")
    close_button.grid(row=0, column=8, padx=2, pady=2, sticky="NSEW")
    tools_frame4check.grid_rowconfigure(0, minsize=20)
    tools_frame4check.grid(row=0, column=0, columnspan=12, sticky="NSEW")


def create_list4db(root: tk.Tk, pane: ttk.Panedwindow) -> tk.LabelFrame:
    """
    Автор:
    Цель:   создание виджета Listbox для выбора базы
    Вход:   объект главного окна,
            объект растягивающегося виджета
    Выход:  фрейм с Listbox
    """
    list_frame4check = tk.LabelFrame(root, labelanchor='n', text='Базы данных', bd=0, padx=5, pady=5, relief=tk.RIDGE,
                                     bg='white')
    lsb_base = tk.Listbox(list_frame4check, selectmode='browse')
    for name, base in glob.work_list.items():
        lsb_base.insert(tk.END, name)
    glob.base_list = lsb_base
    lsb_base.bind('<Double-Button-1>',
                  lambda *args: open_base(root, pane, lsb_base.curselection()))
    lsb_base.pack(side="left", fill="both", expand=True)
    return list_frame4check


def create_menu(win: tk.Tk, load):
    """
    Автор:
    Цель:   создает меню на главном окне
    Вход:   объект главного окна, объект функции load
    Выход:  нет
    """
    menubar = tk.Menu(win)
    file = tk.Menu(menubar, tearoff=0)
    file.add_command(label="Load", command=load)
    file.add_command(label="Exit", command=win.quit)
    menubar.add_cascade(label="File", menu=file)

    edit = tk.Menu(menubar, tearoff=0)
    edit.add_command(label="smth")
    menubar.add_cascade(label="Edit", menu=edit)

    about = tk.Menu(menubar, tearoff=0)
    about.add_command(label="smth")
    menubar.add_cascade(label="About", menu=about)
    win.config(menu=menubar)


def create_workspace(root: tk.Tk, pane: ttk.Panedwindow) -> tk.LabelFrame:
    """
        Автор:
        Цель:   создает рабочее пространство таблицы
        Вход:   объект главного окна,
                объект растягивающегося виджета,
        Выход:  фрейм с таблицей
    """

    # создаем и заполняем нашу таблицу
    title = glob.columns
    frame = tk.LabelFrame(pane, labelanchor='n', text='Данные', bd=0, pady=5, padx=5, relief=tk.RIDGE, bg='white')
    tree = ttk.Treeview(frame, columns=title, height=constants.tree_rows_number, show="headings", selectmode='browse')
    [tree.heading('#' + str(x + 1), text=title[x]) for x in range(len(title))]
    for i in list(glob.current_base.index):
        insert = list(glob.current_base[glob.columns].iloc[i, :])
        tree.insert('', 'end', iid=i, values=insert)
    # меняем ширину столбца для красоты
    for i in range(1, len(title) + 1):
        tree.column('#' + str(i), width=100, stretch=False)
    # скроллбары для нее
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.bind("<Button-1>", lambda event, mode="Single": workspace_onclick_event(root, event, mode))
    tree.bind("<Double-Button-1>", lambda event, mode="Double": workspace_onclick_event(root, event, mode))
    tree.configure(yscrollcommand=vsb.set)
    tree.configure(xscrollcommand=hsb.set)

    # пакуем все в фрейм, а его по сетке в окно
    glob.table4base = tree
    hsb.pack(side='bottom', fill='both')
    vsb.pack(side='right', fill='both')
    tree.pack(side='top', fill='x')

    return frame


#  =======================================================================================


def add_inf(win: tk.Tk):
    """
        Автор:Подкопаева П.
        Цель: Добавление новых элементов в базу данных (окно)
        Вход: Нет
        Выход: Нет
    """

    if not glob.is_db_open():
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
                               command=lambda *args: accept(root, list4values))
    message_button.grid(row=19, column=3, padx=5, pady=5, sticky="e")


def accept(root, list4values):
    """
    Автор:
    Цель:
    Вход:
    Выход:
    """
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
        glob.current_base = glob.correct_base_values(glob.current_base)
        glob.work_list[glob.current_base_name] = glob.current_base
        new_item = glob.table4base.insert('', 'end', iid=len(glob.current_base.index) - 1)
        for i in glob.columns:
            glob.table4base.set(new_item, column=i, value=list4values[i].get())
        mb.showinfo("Сообщение", "Занесено в базу")
        glob.mark_changes()
        glob.update_list()
        root.destroy()
    else:
        err.error("Данные введены некорректно, повторите попытку")
