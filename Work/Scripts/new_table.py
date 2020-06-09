# -*- coding: utf-8 -*-
"""
Created on Sat May 23 23:07:38 2020

@author: User
"""
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb

import pandas as pd

from Scripts import base_handling as hand_base
from Scripts import globalvars as glob


def statoutput(bd):
    """
    Функция, создающая список из bd для использования при выводе
    Автор: 
    Входные параметры: bd 
    Возвращает: список из элементов bd 
    """
    shape = bd.shape
    row = shape[0]
    full_list = []
    for i in range(0, row):
        list_row = []
        for j in bd.iloc[i]:
            list_row.append(j)
        full_list.append(list_row)
    return full_list


def choice_table(root: tk.Tk, pane: ttk.Panedwindow):
    """
    Цель: Выбор фильтров для сводной таблицы
    Автор:
    Входные параметры:
    Выходные параметры:
    """

    global CHOSEN_VALUE

    if not glob.is_db_open():
        return "break"

    win = tk.Toplevel(root)
    win.title("Выбор")
    win.geometry("300x300+500+200")

    background = tk.Frame(win, bg="#F8F8FF")
    background.place(x=0, y=0, relwidth=1, relheight=1)

    choice = ("Выберите фильтры", "Страна - Средняя смертность", "Страна - Средняя высота вулкана",
              "Расположение - Средняя смертность",
              "Тип вулкана - Средняя смертность", "Тип вулкана - Количество пропавших",
              "Название вулкана - Количество раненных")

    # make_table = tk.Label(background)
    CHOSEN_VALUE = tk.StringVar(value='Выберите фильтры')
    make_table_op = tk.OptionMenu(background, CHOSEN_VALUE, *choice)
    make_table_op.place(relx=0.25, rely=0.25)
    make_table_op.pack()

    button_statistics = tk.Button(background, text='Посмотреть статистику', bg="#AFEEEE")

    button_statistics.bind("<Button-1>", lambda *args: stat_table_window(root, pane))
    button_statistics.place(relx=0.25, rely=0.5, relheight=0.1, relwidth=0.6)
    background.pack(side="top", fill="both", expand=True, padx=10, pady=5)


def name_injuries():
    General = pd.DataFrame(hand_base.bd)

    General['INJURIES'] = General['INJURIES'].apply(pd.to_numeric, errors='coerce')

    rat = General.groupby(['Name']).agg({'INJURIES': "sum"})

    rat.rename(columns={'Name': 'Название', 'INJURIES': 'Раненые'}, inplace=True)
    rat = rat.reset_index()
    rat = rat.round({'Injuries': 2})
    rat.fillna(0)
    # print(rat)
    return rat.fillna(0)


def country_deaths_mean():
    """
    Автор:
    Цель: Подсчёт средней смертности для каждой страны
    Входные параметры: DataFrame
    Возвращает: нет
    """

    General = pd.DataFrame(hand_base.bd)
    General['DEATHS'] = General['DEATHS'].apply(pd.to_numeric, errors='coerce')

    rat = General.groupby(['Country']).agg({'DEATHS': "mean"})

    rat.rename(columns={'Country': 'Страна', 'DEATHS': 'Средняя смертность'}, inplace=True)
    rat = rat.reset_index()
    rat = rat.round({'Average number of deaths': 2})
    rat.fillna(0)
    # print(rat)
    return rat.fillna(0)


def country_elevation_mean():
    General = pd.DataFrame(hand_base.bd)
    General['Elevation'] = General['Elevation'].apply(pd.to_numeric, errors='coerce')

    rat = General.groupby(['Country']).agg({'Elevation': "mean"})

    rat.rename(columns={'Country': 'Страна', 'Elevation': 'Средняя высота вулкана'}, inplace=True)
    rat = rat.reset_index()
    rat = rat.round({'Average elevation': 2})
    # print(rat)
    return rat.fillna(0)


def location_deaths_mean():
    General = pd.DataFrame(hand_base.bd)
    General['DEATHS'] = General['DEATHS'].apply(pd.to_numeric, errors='coerce')

    rat = General.groupby(['Location']).agg({'DEATHS': "mean"})

    rat.rename(columns={'Location': 'Местность', 'DEATHS': 'Средняя смертность'}, inplace=True)
    rat = rat.reset_index()
    rat = rat.round({'Average number of deaths': 2})
    rat.fillna(0)
    # print(rat)
    return rat.fillna(0)


def type_deaths_mean():
    General = pd.DataFrame(hand_base.bd)
    General['DEATHS'] = General['DEATHS'].apply(pd.to_numeric, errors='coerce')

    rat = General.groupby(['Type']).agg({'DEATHS': "mean"})

    rat.rename(columns={'Type': 'Тип вулкана', 'DEATHS': 'Средняя смертность'}, inplace=True)
    rat = rat.reset_index()
    rat = rat.round({'Average number of deaths': 2})
    # print(rat.fillna(0))
    return rat.fillna(0)


def type_missing_num():
    General = pd.DataFrame(hand_base.bd)
    General['MISSING'] = General['MISSING'].apply(pd.to_numeric, errors='coerce')

    num = General.groupby(['Type']).agg({'MISSING': "sum"})

    num.rename(columns={'Type': 'Тип вулкана', 'MISSING': 'Количество известных пропавших'}, inplace=True)
    num = num.reset_index()
    num = num.round({'Number of missing': 2})
    # print(num.fillna(0))
    return num


def stat_table_window(root: tk.Tk, pane: ttk.Panedwindow):
    """
    Цель: Функция, создающая окно для просмотра сводной таблицы
    Автор:
    Входные параметры: нет
    Возвращает: нет
    """
    global CHOSEN_VALUE

    win = tk.Toplevel(root)
    win.title("Таблица")
    win.geometry("600x500+500+200")

    background = tk.Frame(win, bg="#F8F8FF")
    background.place(x=0, y=0, relwidth=1, relheight=1)

    name_lab = tk.Label(background, font=1, text='Таблица по выбранному фильтру\n' + CHOSEN_VALUE.get(), bg="#F5F5F5")
    name_lab.place(relx=0.01, rely=0.01, relwidth=0.95, relheight=0.1)

    answerfr = tk.Frame(background, bg="#F5F5F5")
    answerfr.place(relx=0.025, rely=0.13, relwidth=0.95, relheight=0.8)

    answerfr_1 = tk.Frame(answerfr, bg="#F5F5F5")
    answerfr_1.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)

    if CHOSEN_VALUE.get() == 'Выберите фильтры':
        mb.showerror("Ошибка!", "Сначала выберите фильтр!")



    elif CHOSEN_VALUE.get() == 'Страна - Средняя смертность':
        # выбор параметра и строится соответствующая таблица

        bd_series = country_deaths_mean()
        bd = bd_series
        list_ = statoutput(bd)
        table = ttk.Treeview(answerfr_1, columns=('Страна', 'Средняя смертность'), height=15, show='headings')
        table.column('Страна', anchor=tk.CENTER)
        table.column('Средняя смертность', anchor=tk.CENTER)
        table.heading('Страна', text='Страна')
        table.heading('Средняя смертность', text='Средняя смертность')
        for row in list_:
            table.insert('', tk.END, values=row)

        table.place(relwidth=1, relheight=1)

        # кнопка сохранения
        button_save = tk.Button(background, font=12, text='Сохранить')
        button_save.bind("<Button-1>", lambda *args: save_button(bd))

        button_save.place(relx=0.755, rely=0.9375, relheight=0.0495, relwidth=0.22)

        scrolltable = tk.Scrollbar(answerfr_1, orient=tk.VERTICAL, command=table.yview)
        table.config(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)

    elif CHOSEN_VALUE.get() == 'Название вулкана - Количество раненных':
        # выбор параметра и строится соответствующая таблица

        bd_series = name_injuries()
        bd = bd_series
        list_ = statoutput(bd)
        table = ttk.Treeview(answerfr_1, columns=('Название', 'Раненые'), height=15, show='headings')
        table.column('Название', anchor=tk.CENTER)
        table.column('Раненые', anchor=tk.CENTER)
        table.heading('Название', text='Название')
        table.heading('Раненые', text='Раненые')
        for row in list_:
            table.insert('', tk.END, values=row)

        table.place(relwidth=1, relheight=1)

        # кнопка сохранения
        button_save = tk.Button(background, font=12, text='Сохранить')
        button_save.bind("<Button-1>", lambda *args: save_button(bd))

        button_save.place(relx=0.755, rely=0.9375, relheight=0.0495, relwidth=0.22)

        scrolltable = tk.Scrollbar(answerfr_1, orient=tk.VERTICAL, command=table.yview)
        table.config(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)


    elif CHOSEN_VALUE.get() == 'Страна - Средняя высота вулкана':
        # выбор параметра и соответсвующая параметру таблица строится

        bd_series = country_elevation_mean()

        bd = bd_series
        list_ = statoutput(bd)

        table = ttk.Treeview(answerfr_1, columns=('Страна', 'Средняя высота вулкана'), height=15, show='headings')
        table.column('Страна', anchor=tk.CENTER)
        table.column('Средняя высота вулкана', anchor=tk.CENTER)
        table.heading('Страна', text='Страна')
        table.heading('Средняя высота вулкана', text='Средняя высота вулкана')
        for row in list_:
            table.insert('', tk.END, values=row)

        table.place(relwidth=1, relheight=1)

        # кнопка сохранения
        button_save = tk.Button(background, font=12, text='Сохранить')
        button_save.bind("<Button-1>", lambda *args: save_button(bd))

        button_save.place(relx=0.755, rely=0.9375, relheight=0.0495, relwidth=0.22)

        scrolltable = tk.Scrollbar(answerfr_1, orient=tk.VERTICAL, command=table.yview)
        table.config(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)


    elif CHOSEN_VALUE.get() == 'Расположение - Средняя смертность':
        # выбор параметра и соответсвующая параметру таблица строится

        bd_series = location_deaths_mean()

        bd = bd_series
        list_ = statoutput(bd)

        table = ttk.Treeview(answerfr_1, columns=('Расположение', 'Средняя смертность'), height=15, show='headings')
        table.column('Расположение', anchor=tk.CENTER)
        table.column('Средняя смертность', anchor=tk.CENTER)
        table.heading('Расположение', text='Расположение')
        table.heading('Средняя смертность', text='Средняя смертность')
        for row in list_:
            table.insert('', tk.END, values=row)

        table.place(relwidth=1, relheight=1)

        # кнопка сохранения
        button_save = tk.Button(background, font=12, text='Сохранить')
        button_save.bind("<Button-1>", lambda *args: save_button(bd))

        button_save.place(relx=0.755, rely=0.9375, relheight=0.0495, relwidth=0.22)
        scrolltable = tk.Scrollbar(answerfr_1, orient=tk.VERTICAL, command=table.yview)
        table.config(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)

    elif CHOSEN_VALUE.get() == 'Тип вулкана - Средняя смертность':
        # выбор параметра и соответсвующая параметру таблица строится

        bd_series = type_deaths_mean()

        bd = bd_series
        list_ = statoutput(bd)

        table = ttk.Treeview(answerfr_1, columns=('Тип вулкана', 'Средняя смертность'), height=15, show='headings')
        table.column('Тип вулкана', anchor=tk.CENTER)
        table.column('Средняя смертность', anchor=tk.CENTER)
        table.heading('Тип вулкана', text='Тип вулкана')
        table.heading('Средняя смертность', text='Средняя смертность')
        for row in list_:
            table.insert('', tk.END, values=row)

        table.place(relwidth=1, relheight=1)

        # кнопка сохранения
        button_save = tk.Button(background, font=12, text='Сохранить')
        button_save.bind("<Button-1>", lambda *args: save_button(bd))

        button_save.place(relx=0.755, rely=0.9375, relheight=0.0495, relwidth=0.22)
        scrolltable = tk.Scrollbar(answerfr_1, orient=tk.VERTICAL, command=table.yview)
        table.config(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)


    elif CHOSEN_VALUE.get() == 'Тип вулкана - Количество пропавших':
        # выбор параметра и соответсвующая параметру таблица строится

        bd_series = type_missing_num()

        bd = bd_series
        list_ = statoutput(bd)

        table = ttk.Treeview(answerfr_1, columns=('Тип вулкана', 'Количество пропавших'), height=15, show='headings')
        table.column('Тип вулкана', anchor=tk.CENTER)
        table.column('Количество пропавших', anchor=tk.CENTER)
        table.heading('Тип вулкана', text='Тип вулкана')
        table.heading('Количество пропавших', text='Количество пропавших')
        for row in list_:
            table.insert('', tk.END, values=row)

        scrolltable = tk.Scrollbar(answerfr_1, orient=tk.VERTICAL, command=table.yview)
        table.config(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=tk.RIGHT, fill=tk.Y)

        table.place(relwidth=1, relheight=1)

        # кнопка сохранения
        button_save = tk.Button(background, font=12, text='Сохранить')
        button_save.bind("<Button-1>", lambda *args: save_button(bd))

        button_save.place(relx=0.755, rely=0.9375, relheight=0.0495, relwidth=0.22)


def save_button(bd):
    """
    Функция для сохранения таблицы
    Принимает: bd
    Возвращает: Ничего
    """
    global CHOSEN_VALUE
    name = CHOSEN_VALUE.get()

    if name == 'Cтрана - Средняя смертность':
        name = 'Country_Deaths_mean'
    elif name == 'Страна - Средняя высота вулкана':
        name = 'Country_elevation_mean'
    elif name == 'Страна - Количество вулканов':
        name = 'Country_number_volcanoes'
    elif name == 'Расположение - Средняя смертность':
        name = 'Location_deaths_mean'
    elif name == 'Тип вулкана - Средняя смертность':
        name = 'Type_deaths_mean'
    elif name == 'Год - Количество извержений':
        name = 'Year_num_eruptions'
    elif name == 'Тип вулкана - Количество пропавших':
        name = 'Type_Missing'
    elif name == 'Тип вулкана - Вероятность цунами':
        name = 'Type_TSU'
    elif name == 'Тип вулкана - Вероятность землетрясения':
        name = 'Type_IQ'

    bd.to_csv("../Output/" + name + ".csv", index=False)
    mb.showinfo("Информация", "Таблица " + name + " успешно сохранена")
