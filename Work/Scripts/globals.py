from tkinter import Listbox
from tkinter import Tk
from tkinter.ttk import PanedWindow
from tkinter.ttk import Treeview

import numpy as np
from pandas import DataFrame

from Work.Scripts import constants

columns: list = constants.origin_columns
"""
    В columns будут храниться все столбцы, отображаемые в данный момент в программе.
    Программа будет автоматически отображать новые столбцы и убирать удаленные.  
"""

work_list: dict = {}
"""
    Словарь со значениями (Имя БД: объект БД).
    В нем хранятся все базы данных, которые были загруженны в программу.
    При сохранении будет сохраняться именно базы из словаря.
"""

current_base: DataFrame = None
"""Текущий dataframe, с которым работает пользователь."""

current_base_name: str = None
"""Имя текущего dataframe, с которым работает пользователь."""

current_base_list_id: int = None
"""id текущего dataframe в ListBox, с которым работает пользователь."""

table4base: Treeview = None
"""
    Объект TreeView, данные из которого отображаются в workspace.
    В TreeView хранятся все данные из выбранной базы данных.
"""

base_list: Listbox = None
"""
    Объект Listbox, который отображается в программе.
    в нем хранятся все имена загруженных баз
    с помощью него осуществляется выбор пользователем
"""

root: Tk = None
pane: PanedWindow = None
tree_rows_number: int = 40


def is_saved() -> bool:
    """
    Автор:
    Цель:
    Вход:
    Выход:
    """
    global current_base_name
    if "*" in current_base_name:
        return False
    return True


def delete_current_base():
    global work_list, current_base_name, current_base_list_id, current_base
    del work_list[current_base_name]
    current_base = None
    current_base_name = None
    base_list.delete(current_base_list_id)
    current_base_list_id = None


def mark_changes():
    global current_base_name
    if is_saved():
        current_base_name += "*"


def unmark_changes():
    global current_base_name
    if not is_saved():
        current_base_name = current_base_name.replace('*', '')


def correct_base_values(base: DataFrame) -> DataFrame:
    """
    Автор:
    Цель:   при добавлении в таблицу измененных пользователем данных могут возникнуть nan значения,
            их мы меняем на пустые строки или на 0, так же nan меняет типы столбцов на другой,
            здесь мы обратно приводим тип столбцов к нужному
    Вход:  нет
    Выход:  нет
    """
    base[['Year', 'Month', 'Day']] = base[['Year', 'Month', 'Day']].replace(np.nan, 0)
    base[['Name', 'Location', 'Country', 'Type', 'Agent', 'TSU', 'EQ']] = base[
        ['Name', 'Location', 'Country', 'Type', 'Agent', 'TSU', 'EQ']].replace(np.nan, "")
    base = base.astype({'Year': 'int32', 'Month': 'int32', 'Day': 'int32',
                        'Latitude': 'float64', 'Longitude': 'float64', 'VEI': 'float64',
                        'DEATHS': 'float64', 'INJURIES': 'float64', 'MISSING': 'float64',
                        'DAMAGE_MILLIONS_DOLLARS': 'float64'})
    return base


def update_workspace():
    """
    Автор:
    Цель:
    Вход:
    Выход:
    """
    global current_base
    global columns
    assert current_base is not None
    for i in range(len(current_base.index)):
        insert = current_base.iloc[i, :]
        for j in columns:
            table4base.set(i, column=j, value=insert[j])


def clear_workspace():
    """
    Автор:
    Цель:
    Вход:
    Выход:
    """

    global current_base
    global columns
    assert current_base is not None
    table4base.delete(*list(range(len(current_base.index))))


def update_list():
    """
    Автор:
    Цель:
    Вход:
    Выход:
    """
    global current_base
    global current_base_list_id
    base_list.delete(current_base_list_id)
    base_list.insert(current_base_list_id, current_base_name)
