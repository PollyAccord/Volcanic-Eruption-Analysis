import math as m
import tkinter as tk

from Scripts import globalvars as glob


def statistics_base(root: tk.Toplevel, string):
    """
    Автор:
    Цель: Формирует и сохраняет отчёт по основным статистикам для количественных переменных
    Вход: dataframe
    Выход: Нет (файл)
    """
    win = tk.Toplevel(root)
    win.title("Статистические данные: " + string)
    win.geometry('600x300+500+300')
    # bd = pd.read_csv('volcano.csv', header=(0))
    bd = glob.current_base
    # string = 'DEATHS'
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

    average_label = tk.Label(win, text="Среднее арифметическое: %5f" % (average), font=('Arial', 11, 'italic'))
    average_label.grid(row=0, column=0, sticky="e")

    med_label = tk.Label(win, text="Медиана: %5f" % (med), font=('Arial', 11, 'italic'))
    med_label.grid(row=1, column=0, sticky="e")

    s_label = tk.Label(win, text="Форма плотности распределения: %s" % (s), font=('Arial', 11, 'italic'))
    s_label.grid(row=2, column=0, sticky="w")

    disp_label = tk.Label(win, text="Выборочная дисперсия: %4f" % (disp), font=('Arial', 11, 'italic'))
    disp_label.grid(row=3, column=0, sticky="w")

    quartLow_label = tk.Label(win, text="Нижняя квартиль: %4f" % (sortedSample.quantile(0.25)),
                              font=('Arial', 11, 'italic'))
    quartLow_label.grid(row=4, column=0, sticky="w")

    quartHigh_label = tk.Label(win, text="Верхняя квартиль: %4f" % (sortedSample.quantile(0.75)),
                               font=('Arial', 11, 'italic'))
    quartHigh_label.grid(row=5, column=0, sticky="w")

    quartrazm_label = tk.Label(win, text="Межквартильный размах: %5d" % (
            sortedSample.quantile(0.75) - sortedSample.quantile(0.25)),
                               font=('Arial', 11, 'italic'))
    quartrazm_label.grid(row=6, column=0, sticky="w")

    max_label = tk.Label(win, text="Максимум: %5d" % (sortedSample.max()), font=('Arial', 11, 'italic'))
    max_label.grid(row=7, column=0, sticky="w")

    min_label = tk.Label(win, text="Минимум: %5d" % (sortedSample.min()), font=('Arial', 11, 'italic'))
    min_label.grid(row=8, column=0, sticky="w")

    razm_label = tk.Label(win, text="Размах: %5d" % (sortedSample.max() - sortedSample.min()),
                          font=('Arial', 11, 'italic'))
    razm_label.grid(row=9, column=0, sticky="w")

    sko_label = tk.Label(win, text="Стандартное отклонение (СКО): %5f" % (sortedSample.std()),
                         font=('Arial', 11, 'italic'))
    sko_label.grid(row=10, column=0, sticky="w")

    kvar_label = tk.Label(win, text="Коэффициент вариации: %5d" % (sortedSample.std() / sortedSample.mean()),
                          font=('Arial', 11, 'italic'))
    kvar_label.grid(row=11, column=0, sticky="w")
    value_button = tk.Button(win, text="Ok")
    value_button.bind("<Button-1>", lambda *args: win.destroy())
    value_button.grid(row=12, column=0)

# общий вид графиков и диаграмм в окнах (на вход подаются соответсвующие подходящие строки, которые пользователь
# выбирает в отдельном окне (как я вижу))
