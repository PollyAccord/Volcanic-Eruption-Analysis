import pandas as pd

from Scripts import constants
from Scripts import globalvars as glob

# ['Year', 'Month', 'Day', 'Name', 'Location', 'Country', 'Latitude', 'Longitude', 'Elevation', 'Type', 'VEI', 'Agent', 'DEATHS', 'INJURIES', 'MISSING', 'DAMAGE_MILLIONS_DOLLARS', 'TSU', 'EQ']
bd = pd.read_csv('../Data/volcano.csv', header=0)[['Year', 'Month', 'Day', 'Name', 'Location',
                                                   'Country', 'Latitude', 'Longitude', 'Elevation',
                                                   'Type', 'VEI', 'Agent', 'DEATHS', 'INJURIES', 'MISSING',
                                                   'DAMAGE_MILLIONS_DOLLARS', 'TSU', 'EQ']]
glob.work_list['Volcano Eruption'] = glob.correct_base_values(bd)


def read_base(path: str) -> str:
    """
    Автор: Ковязин В.
    Цель: загружает базу из файла
    Вход: путь
    Выход: новая база
    """
    # если при создании базы возникло исключение, то перебрасываем исключение дальше
    try:
        # в прочитанной базе может не оказаться всех нужных нам столбцов
        base = pd.read_csv(path, header=0)[constants.origin_columns]
    except Exception:
        raise
    base_name = path[path.rfind('\\') + 1:path.rfind('.')]
    i = 0
    # если база уже загружена в программу, то в программу добавляется ее копию с постфиксом
    if base_name in glob.work_list.keys():
        while base_name + "(" + str(i) + ")" in glob.work_list.keys():
            i += 1
        base_name += "(" + str(i) + ")"
    base = glob.correct_base_values(base)
    glob.work_list[base_name] = base
    return base_name


def create_base(path: str) -> str:
    """
    Автор: Ковязин В.
    Цель: создает новую чистую базу
    Вход: путь
    Выход: новая база
    """
    # на всякий случай добавил проверку на наличие расширения в пути
    if ".csv" in path:
        base_name = path[path.rfind('/') + 1:path.rfind('.')]
    else:
        base_name = path[path.rfind('/') + 1:]
        path += ".csv"
    new_base = pd.DataFrame(columns=constants.origin_columns)
    new_base = glob.correct_base_values(new_base)
    glob.work_list[base_name] = new_base
    new_base.to_csv(path, index=False)
    return base_name


def save_base() -> None:
    """
        Автор: Ковязин В.
        Цель: сохраняем текущую базу
        Вход: нет
        Выход: нет
        """
    glob.work_list[glob.current_base_name].to_csv("../Data/" + glob.current_base_name + ".csv", index=False)


def search_name(data_base, value):
    result = {}
    i = 0
    for base in data_base:
        if value in data_base[base]["Name"]:
            result[i] = data_base[base]
            i += 1
    return result


def search_type(data_base, value):
    """
    Автор:
    Цель: Функция ищет в базе данных вулканы типа type
    Вход: DataFrame
    Выход: DataFrame по фильтрам
    """
    result = {}
    i = 0
    for base in data_base:
        if value in data_base[base]["Type"]:
            result[i] = data_base[base]
            i += 1
    return result


def search_country(data_base, value):
    """
    Автор:
    Цель: Ищет в базе данных вулканы страны Country
    Вход: DataFrame
    Выход: DataFrame по фильтрам
    """
    result = {}
    i = 0
    for base in data_base:
        if value in data_base[base]["Country"]:
            result[i] = data_base[base]
            i += 1
    return result


def search_location(data_base, value):
    """
    Автор:
    Цель: Ищет в базе данных вулканы расположения Location
    Вход: DataFrame
    Выход: DataFrame по фильтрам
    """
    result = {}
    i = 0
    for base in data_base:
        if value in data_base[base]["Country"]:
            result[i] = data_base[base]
            i += 1
    return result


def search_TSU(data_base, value):
    result = {}
    i = 0
    for base in data_base:
        if value in data_base[base]["TSU"]:
            result[i] = data_base[base]
            i += 1
    return result


def search_EQ(data_base, value):
    result = {}
    i = 0
    for base in data_base:
        if value in data_base[base]["EQ"]:
            result[i] = data_base[base]
            i += 1
    return result
