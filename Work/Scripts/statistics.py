import math as m
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mb

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Scripts import base_handling as hand_base
from Scripts import globalvars as glob
from Scripts import new_table as tb


def statistics_base(root: tk.Toplevel, pane: ttk.Panedwindow, string):
    """
    Автор:
    Цель: Формирует и сохраняет отчёт по основным статистикам для количественных переменных
    Вход: dataframe
    Выход: Нет (файл)
    """

    win = tk.Toplevel(root, bg="#F8F8FF")
    win.title("Статистические данные: " + string)
    win.geometry('600x400+500+300')

    background = tk.Frame(win, bg="#F8F8FF")
    background.place(x=0, y=0, relwidth=1, relheight=1)

    bd = glob.current_base
    sortedSample = bd[string].sort_values()[bd[string] == bd[string]]  # get rid of nan
    average = m.ceil(sortedSample.mean())
    med = sortedSample.median()
    mode = sortedSample.mode().values[0]
    if average == med:
        s = 'симметрия'
    elif average > med:
        s = 'acимметрия вправо'
    else:
        s = 'acимметрия влево'
    disp = (sortedSample.apply(lambda x: (x - average) ** 2).sum()) / (len(sortedSample) - 1)

    average_label = tk.Label(background, text="Среднее арифметическое: %5f" % (average), bg="#F8F8FF",
                             font=('Arial', 9, 'italic'))
    average_label.place(relx=0.2, rely=0)

    med_label = tk.Label(background, text="Медиана: %5f" % (med), bg="#F8F8FF", font=('Arial', 9, 'italic'))
    med_label.place(relx=0.2, rely=0.05)

    mod_label = tk.Label(background, text="Мода: %5f" % (mode), bg="#F8F8FF", font=('Arial', 9, 'italic'))
    mod_label.place(relx=0.2, rely=0.1)

    s_label = tk.Label(background, text="Форма плотности распределения: %s" % (s), bg="#F8F8FF",
                       font=('Arial', 9, 'italic'))
    s_label.place(relx=0.2, rely=0.15)

    disp_label = tk.Label(background, text="Выборочная дисперсия: %4f" % (disp), bg="#F8F8FF",
                          font=('Arial', 9, 'italic'))
    disp_label.place(relx=0.2, rely=0.2)

    quartLow_label = tk.Label(background, text="Нижняя квартиль: %4f" % (sortedSample.quantile(0.25)),
                              font=('Arial', 9, 'italic'), bg="#F8F8FF")
    quartLow_label.place(relx=0.2, rely=0.25)

    quartHigh_label = tk.Label(background, text="Верхняя квартиль: %4f" % (sortedSample.quantile(0.75)),
                               font=('Arial', 9, 'italic'), bg="#F8F8FF")
    quartHigh_label.place(relx=0.2, rely=0.3)

    quartrazm_label = tk.Label(background, text="Межквартильный размах: %5d" % (
            sortedSample.quantile(0.75) - sortedSample.quantile(0.25)),
                               font=('Arial', 9, 'italic'), bg="#F8F8FF")
    quartrazm_label.place(relx=0.2, rely=0.35)

    max_label = tk.Label(background, text="Максимум: %5d" % (sortedSample.max()), font=('Arial', 9, 'italic'),
                         bg="#F8F8FF")
    max_label.place(relx=0.2, rely=0.4)

    min_label = tk.Label(background, text="Минимум: %5d" % (sortedSample.min()), bg="#F8F8FF",
                         font=('Arial', 9, 'italic'))
    min_label.place(relx=0.2, rely=0.45)

    razm_label = tk.Label(background, text="Размах: %5d" % (sortedSample.max() - sortedSample.min()),
                          font=('Arial', 9, 'italic'), bg="#F8F8FF")
    razm_label.place(relx=0.2, rely=0.5)

    sko_label = tk.Label(background, text="Стандартное отклонение (СКО): %5f" % (sortedSample.std()),
                         font=('Arial', 9, 'italic'), bg="#F8F8FF")
    sko_label.place(relx=0.2, rely=0.55)

    kvar_label = tk.Label(background, text="Коэффициент вариации: %5d" % (sortedSample.std() / sortedSample.mean()),
                          font=('Arial', 9, 'italic'), bg="#F8F8FF")
    kvar_label.place(relx=0.2, rely=0.6)

    value_button = tk.Button(background, text="Сохранить", font=1, bg="#B0E0E6")
    value_button.bind("<Button-1>", lambda *args: save_file(background, string))
    value_button.place(relx=0.5, rely=0.8, relheight=0.1, relwidth=0.2)

    background.pack(side="top", fill="both", expand=True, padx=10, pady=5)


def graphics_choice(root: tk.Tk, pane: ttk.Panedwindow):
    global CHOSEN_VALUE1, CHOSEN_VALUE2, CHOSEN_VALUE3, CHOSEN_VALUE4

    if not glob.is_db_open():
        return "break"

    win = tk.Toplevel(root)
    win.title("Выбор")
    win.geometry("700x500+500+200")

    background = tk.Frame(win, bg="#F8F8FF")
    background.place(x=0, y=0, relwidth=1, relheight=1)

    choice_graph = ("Год - Количество извержений", "Год - Средняя смертность")

    CHOSEN_VALUE1 = tk.StringVar(value='Фильтры для линейного графика')
    make_gr = tk.OptionMenu(background, CHOSEN_VALUE1, *choice_graph)
    make_gr.place(relx=0.1, rely=0.1)
    make_gr.pack()

    button_graph = tk.Button(background, text='Построить график', bg="#AFEEEE")

    button_graph.bind("<Button-1>", lambda *args: draw_graph(root, pane))
    button_graph.place(relx=0.1, rely=0.4, relheight=0.1, relwidth=0.2)

    choice_diagram = ("Тип вулкана - Смерти", "Страна - Средняя смертность", "Страна - Средняя высота вулкана",
                      "Страна - Количество вулканов", "Расположение - Средняя смертность",
                      "Тип вулкана - Средняя смертность", "Тип вулкана - Количество пропавших")

    CHOSEN_VALUE2 = tk.StringVar(value='Фильтры для столбчатой диаграммы')
    make_dgrm = tk.OptionMenu(background, CHOSEN_VALUE2, *choice_diagram)
    make_dgrm.place(relx=0.3, rely=0.1)
    make_dgrm.pack()

    button_diagram = tk.Button(background, text='Построить диаграмму', bg="#AFEEEE")

    button_diagram.bind("<Button-1>", lambda *args: draw_diagram())
    button_diagram.place(relx=0.3, rely=0.4, relheight=0.1, relwidth=0.2)

    choice_pie = ("Год - Количество извержений", "Год - Средняя смертность")

    CHOSEN_VALUE3 = tk.StringVar(value='Фильтры для круговой диаграммы')
    make_pie = tk.OptionMenu(background, CHOSEN_VALUE3, *choice_pie)
    make_pie.place(relx=0.5, rely=0.1)
    make_pie.pack()

    button_pie = tk.Button(background, text='Построить "пирог"', bg="#AFEEEE")

    button_pie.bind("<Button-1>", lambda *args: draw_pie(root, pane))
    button_pie.place(relx=0.5, rely=0.4, relheight=0.1, relwidth=0.2)

    choice_viskers = ("Год - Количество извержений", "Год - Средняя смертность")

    CHOSEN_VALUE4 = tk.StringVar(value='Фильтры для диаграммы Бокса-Фискерса')
    make_box = tk.OptionMenu(background, CHOSEN_VALUE3, *choice_pie)
    make_box.place(relx=0.7, rely=0.1)
    make_box.pack()

    button_box = tk.Button(background, text='Построить "Бокса-Вискерса"', bg="#AFEEEE")

    button_box.bind("<Button-1>", lambda *args: draw_box(root, pane))
    button_box.place(relx=0.7, rely=0.4, relheight=0.1, relwidth=0.2)

    background.pack(side="top", fill="both", expand=True, padx=2, pady=3)


def draw_graph(root: tk.Tk, pane: ttk.Panedwindow):
    global CHOSEN_VALUE1

    win = tk.Toplevel(root)
    win.title("График")
    win.geometry("600x500+500+200")

    background = tk.Frame(win, bg="#F8F8FF")
    background.place(x=0, y=0, relwidth=1, relheight=1)

    name_lab = tk.Label(background, text='График\n' + CHOSEN_VALUE1.get(), bg="#F5F5F5")
    name_lab.place(relx=0.01, rely=0.01, relwidth=0.95, relheight=0.1)

    if CHOSEN_VALUE1.get() == 'Фильтры для линейного графика':
        mb.showerror("Ошибка!", "Сначала выберите фильтр! (графики)")

    elif CHOSEN_VALUE1.get() == 'Год - Средняя смертность':

        fig = plt.Figure(figsize=(10, 10), dpi=80)
        ax1 = fig.add_subplot(111)
        # win.fillna(0)
        hand_base.bd = hand_base.bd.fillna(0)
        graph = FigureCanvasTkAgg(fig, background)
        graph.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
        df1 = hand_base.bd[["Year", "DEATHS"]].groupby("Year").mean()
        df1.plot(kind='line', legend=True, ax=ax1, color='r', marker='o', fontsize=1)


# elif CHOSEN_VALUE1.get() == 'Год - количество извержений':


def draw_diagram(root: tk.Tk, pane: ttk.Panedwindow):
    global CHOSEN_VALUE2

    win = tk.Toplevel(root)
    win.title("Диаграммы")
    win.geometry("600x500+500+200")

    background = tk.Frame(win, bg="#F8F8FF")
    background.place(x=0, y=0, relwidth=1, relheight=1)

    name_lab = tk.Label(background, text='Диаграмма\n' + CHOSEN_VALUE2, bg="#F5F5F5")
    name_lab.place(relx=0.01, rely=0.01, relwidth=0.95, relheight=0.1)

    if CHOSEN_VALUE2.get() == 'Фильтры для столбчатой диаграммы':
        mb.showerror("Ошибка!", "Сначала выберите фильтр (столбчатые диаграммы)!")

    elif CHOSEN_VALUE2.get() == 'Тип вулкана - Смерти':

        bd = tb.type_deaths_mean()
        fig = plt.figure(figsize=(4, 5), dpi=70)
        ax = fig.add_subplot(1, 1, 1)
        fig.suptitle('')
        bd.plot(kind='bar', ax=ax, y='Средняя смертность', x='Тип вулкана', rot=45, fontsize=9)
        # тут он вставка в интерфейс
        CANVAS = FigureCanvasTkAgg(fig, master=background)
        CANVAS.draw()
        CANVAS.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # toolbar = plt.NavigationToolbar2Tk(CANVAS_1, background)
        # toolbar.update()
        CANVAS.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    elif CHOSEN_VALUE2.get() == 'Страна - Средняя смертность':

        bd = tb.country_deaths_mean()
        fig = plt.figure(figsize=(4, 5), dpi=70)
        ax = fig.add_subplot(1, 1, 1)
        fig.suptitle('')
        bd.plot(kind='bar', ax=ax, y='Средняя смертность', x='Страна', rot=45, fontsize=9)
        # тут он вставка в интерфейс
        CANVAS = FigureCanvasTkAgg(fig, master=background)
        CANVAS.draw()
        CANVAS.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        # toolbar = NavigationToolbar2Tk(CANVAS_1, background)
        # toolbar.update()
        CANVAS.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    #  hand_base.bd= hand_base.bd.fillna(0)
    # dictionary = {}
    # dictionary['others'] = 0
    # for x in set(hand_base.bd.Type):
    #   deaths = hand_base.bd['DEATHS'][hand_base.bd['Type'] == x].sum()
    #  if deaths > 5000:
    #     dictionary[x] = deaths
    # else:
    #   dictionary['others'] += deaths

    # fig = plt.Figure(figsize=(10,10), dpi=80)
    # ax1 = fig.add_subplot(111)
    # graph = FigureCanvasTkAgg(fig, background)
    # graph.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    # df1 = dictionary.values().groupby(dictionary.keys())
    # df1.plot(kind = 'pie', legend = True)

    # plt.pie(dictionary.values(), labels=dictionary.keys(), autopct='%1.1f%%')
    # plt.title("Deaths caused by different types of volcano")
    # plt.show()


# эту функцию нужно дописать
def save_file(background, string) -> None:
    """
        Автор:
        Цель: сохраняем текущую статистику в текстовый файл
        Вход: нет
        Выход: нет
        """
    background.to_png("../Data/" + string + "_statistics" + ".png", index=False)
    mb.messagebox("Cообщение", "Файл сохранён")
