import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from Work.Scripts import base_handling as hand_base
from Work.Scripts import globals as glob
from Work.Scripts import interface as ui


def setup() -> tk.Tk:
    """
    Автор:
    Цель: создание главного окна и расстановка всех его компонентов
    Вход: Нет
    Выход: объект главного окна
    """
    win = tk.Tk()
    ui.save_icon = tk.PhotoImage(file="../Graphics/save_icon.gif")
    ui.add_icon = tk.PhotoImage(file="../Graphics/add_icon.gif")
    ui.edit_icon = tk.PhotoImage(file="../Graphics/edit_icon.gif")
    ui.load_icon = tk.PhotoImage(file="../Graphics/load_icon.gif")
    win.title('Volcano Analyse')

    pane = ttk.Panedwindow(win, orient=tk.HORIZONTAL, width=1)

    # создаем и заполняем строчку меню
    ui.create_menu(win)

    # фрейм кнопочек
    ui.create_toolbar(win)

    # лист для баз данных
    frame = ui.create_list4db(pane)

    # label приглашение к выбору
    pls_select_frame = tk.Frame(pane, bg="white")
    lbl_select_pls = tk.Label(pls_select_frame, text="Пожалуйста, выберете базу данных", bg="white")
    lbl_select_pls.pack(expand=True, fill="both")
    # pls_select_frame.grid(row=1, column=1, rowspan=2, sticky="NSEW")

    pane.add(frame, weight=1)
    pane.add(pls_select_frame, weight=9)
    pane.grid(row=1, column=0, columnspan=3, sticky="NSEW")

    win.grid_rowconfigure(0, weight=1)
    win.grid_rowconfigure(1, weight=99)
    win.grid_rowconfigure(3, weight=1)

    win.grid_columnconfigure(0, weight=1, minsize=150)
    win.grid_columnconfigure(1, weight=99)
    return win


def load_event(*args):
    path = filedialog.askopenfilename(initialdir="../Data/",
                                      filetypes=(("Database files", "*.csv"), ("All files", "*.*")))
    path = path.replace('/', "\\")
    if os.path.exists(path):
        base_name = hand_base.read_base(path)
        glob.base_list.insert(tk.END, base_name)
    else:
        # кидаем exception
        pass
    return "break"


def create_event(*args):
    new_base_path = filedialog.asksaveasfilename(initialdir="../Data/",
                                                 filetypes=(("Database files", "*.csv"), ("All files", "*.*")))
    new_base_name = hand_base.create_base(new_base_path)
    if new_base_name not in glob.base_list.get(0, tk.END):
        glob.base_list.insert(tk.END, new_base_name)
    if glob.current_base_name == new_base_name:
        glob.clear_workspace()
        glob.current_base = glob.work_list[new_base_name]

    return "break"


ui.load_event = load_event
ui.create_event = create_event
root = setup()
root.config(background="white")
root.minsize(400, 400)
root.maxsize(1800, 1000)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
widthRatio = 1200 / 1920
heightRatio = 800 / 1080
app_width = int(screen_width * widthRatio)
app_height = int(screen_height * heightRatio)
geometry = str(app_width) + "x" + str(app_height) + "+" + str(screen_width // 2 - app_width // 2) + "+" + str(
    screen_height // 2 - app_height // 2)
root.geometry(geometry)
root.mainloop()
