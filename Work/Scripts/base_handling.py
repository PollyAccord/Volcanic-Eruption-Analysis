from Work.Scripts import globals as glob
import numpy as np
import pandas as pd
from Work.Scripts import constants

# ['Year', 'Month', 'Day', 'Name', 'Location', 'Country', 'Latitude', 'Longitude', 'Elevation', 'Type', 'VEI', 'Agent', 'DEATHS', 'INJURIES', 'MISSING', 'DAMAGE_MILLIONS_DOLLARS', 'TSU', 'EQ']
bd = pd.read_csv('../Data/volcano.csv', header=0)[['Year', 'Month', 'Day', 'Name', 'Location',
                                                   'Country', 'Latitude', 'Longitude', 'Elevation',
                                                   'Type', 'VEI', 'Agent', 'DEATHS', 'INJURIES', 'MISSING',
                                                   'DAMAGE_MILLIONS_DOLLARS', 'TSU', 'EQ']]
bd[['Year', 'Month', 'Day']] = bd[['Year', 'Month', 'Day']].replace(np.nan, 0)
bd[['Name', 'Location', 'Country', 'Type', 'Agent', 'TSU', 'EQ']] = bd[
    ['Name', 'Location', 'Country', 'Type', 'Agent', 'TSU', 'EQ']].replace(np.nan, "")
bd = bd.astype({'Year': 'int64', 'Month': 'int64', 'Day': 'int64'})
bd = bd.astype({'Latitude': 'float64', 'Longitude': 'float64', 'VEI': 'float64',
                'DEATHS': 'float64', 'INJURIES': 'float64', 'MISSING': 'float64',
                'DAMAGE_MILLIONS_DOLLARS': 'float64'})
glob.work_list['Volcano Eruption'] = bd


def read_base(path: str) -> str:
    """

    :param path:
    :return:
    """
    base = pd.read_csv(path, header=0)[['Year', 'Month', 'Day', 'Name', 'Location',
                                        'Country', 'Latitude', 'Longitude', 'Elevation',
                                        'Type', 'VEI', 'Agent', 'DEATHS', 'INJURIES', 'MISSING',
                                        'DAMAGE_MILLIONS_DOLLARS', 'TSU', 'EQ']]
    base = glob.correct_base_values(base)
    base_name = path[path.rfind('\\') + 1:path.rfind('.')]
    i = 0
    if base_name in glob.work_list.keys():
        while base_name + "(" + str(i) + ")" in glob.work_list.keys():
            i += 1
        base_name += "(" + str(i) + ")"

    glob.work_list[base_name] = base
    return base_name


def create_base(path: str) -> str:
    """

    :param path:
    :return:
    """
    if ".csv" in path:
        base_name = path[path.rfind('/') + 1:path.rfind('.')]
    else:
        base_name = path[path.rfind('/') + 1:]
        path += ".csv"
    new_base = pd.DataFrame(columns=constants.origin_columns)
    glob.work_list[base_name] = new_base
    new_base.to_csv(path, index=False)
    return base_name


def save_base(data_base):
    pass


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
