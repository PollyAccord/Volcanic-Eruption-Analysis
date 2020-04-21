import tkinter as tk
from tkinter import filedialog
import interface as ui
import base_handling as hand_base
import os
import globals as glob
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

    # создаем и заполняем строчку меню
    ui.create_menu(win)

    # фрейм кнопочек
    ui.create_toolbar(win, glob.columns)

    # лист для баз данных
    ui.create_list4db(win, glob.work_list, glob.columns)

    # label приглашение к выбору
    pls_select_frame = tk.Frame(win, bg="white")
    lbl_select_pls = tk.Label(pls_select_frame, text="Пожалуйста, выберете базу данных", bg="white")
    lbl_select_pls.pack(expand=True, fill="both")
    pls_select_frame.grid(row=1, column=1, rowspan=2, sticky="NSEW")
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


ui.load_event = load_event
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
