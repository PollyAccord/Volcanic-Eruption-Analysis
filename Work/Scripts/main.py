import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog

from Work.Library import error_edit_windows as err
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
    root = tk.Tk()
    glob.root = root
    ui.save_icon = tk.PhotoImage(file="../Graphics/save_icon.gif")
    ui.add_icon = tk.PhotoImage(file="../Graphics/add_icon.gif")
    ui.edit_icon = tk.PhotoImage(file="../Graphics/edit_icon.gif")
    ui.load_icon = tk.PhotoImage(file="../Graphics/load_icon.gif")
    ui.close_icon = tk.PhotoImage(file="../Graphics/close_icon.gif")
    ui.add_field_icon = tk.PhotoImage(file="../Graphics/add_field_icon.gif")
    ui.del_field_icon = tk.PhotoImage(file="../Graphics/del_field_icon.gif")
    root.title('Volcano Analyse')

    pane = ttk.PanedWindow(root, orient=tk.HORIZONTAL, width=1)
    glob.pane = pane

    # создаем и заполняем строчку меню
    ui.create_menu(root)

    # фрейм кнопочек
    ui.create_toolbar()

    # лист для баз данных
    frame = ui.create_list4db(pane)

    pane.add(frame, weight=1)
    pls_select_frame = ui.show_invitation()
    pane.add(pls_select_frame, weight=9)
    pane.grid(row=1, column=0, columnspan=3, sticky="NSEW")

    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=99)
    root.grid_rowconfigure(3, weight=1)

    root.grid_columnconfigure(0, weight=1, minsize=150)
    root.grid_columnconfigure(1, weight=99)
    return root


def load_event(*args):
    path = filedialog.askopenfilename(initialdir="../Data/",
                                      filetypes=(("Database files", "*.csv"), ("All files", "*.*")))
    path = path.replace('/', "\\")
    try:
        base_name = hand_base.read_base(path)
        glob.base_list.insert(tk.END, base_name)
    except Exception as error:
        message = str(error)
        err.error(message[message.find('['):message.find(']') + 1] + " нет в Базе Данных")
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


def save_event(*args):
    """
    Автор:
    Цель:
    Вход:
    Выход:
    """
    # открыта ли база?
    if not ui.is_db_open():
        return "break"
    # сохранена ли база?
    if not glob.is_saved():
        glob.unmark_changes()
        glob.work_list[glob.current_base_name] = glob.current_base
        glob.update_list()
        # сохраняем в файл
        hand_base.save_base()


def close_event(*args):
    """
        Автор:
        Цель:
        Вход:
        Выход:
    """
    # открыта ли база?
    if not ui.is_db_open():
        return "break"
    # сохранена ли база?
    if not glob.is_saved():
        ans = err.yes_no("Сохранить изменения?")
        if ans:
            hand_base.save_base()
    glob.delete_current_base()
    glob.pane.forget(1)
    pls_select_frame = ui.show_invitation()
    glob.pane.add(pls_select_frame, weight=9)


ui.load_event = load_event
ui.create_event = create_event
ui.save_event = save_event
ui.close_event = close_event
root = setup()
root.config(background="white")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
widthRatio = 1200 / 1920
heightRatio = 800 / 1080
app_width = int(screen_width * widthRatio)
app_height = int(screen_height * heightRatio)
geometry = str(app_width) + "x" + str(app_height) + "+" + str(screen_width // 2 - app_width // 2) + "+" + str(
    screen_height // 2 - app_height // 2)
root.minsize(400, 400)
root.maxsize(screen_width, screen_height)
root.geometry(geometry)
root.mainloop()
