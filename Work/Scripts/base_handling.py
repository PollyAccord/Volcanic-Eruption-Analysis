import globals as glob
import numpy as np
import pandas as pd

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


def read_base(path):
    base = pd.read_csv(path, header=0)[['Year', 'Month', 'Day', 'Name', 'Location',
                                        'Country', 'Latitude', 'Longitude', 'Elevation',
                                        'Type', 'VEI', 'Agent', 'DEATHS', 'INJURIES', 'MISSING',
                                        'DAMAGE_MILLIONS_DOLLARS', 'TSU', 'EQ']]
    base[['Year', 'Month', 'Day']] = base[['Year', 'Month', 'Day']].replace(np.nan, 0)
    base[['Name', 'Location', 'Country', 'Type', 'Agent', 'TSU', 'EQ']] = base[
        ['Name', 'Location', 'Country', 'Type', 'Agent', 'TSU', 'EQ']].replace(np.nan, "")
    base = base.astype({'Year': 'int64', 'Month': 'int64', 'Day': 'int64'})
    base = base.astype({'Latitude': 'float64', 'Longitude': 'float64', 'VEI': 'float64',
                    'DEATHS': 'float64', 'INJURIES': 'float64', 'MISSING': 'float64',
                    'DAMAGE_MILLIONS_DOLLARS': 'float64'})
    base_name = path[path.rfind('\\') + 1:path.rfind('.')]
    glob.work_list[base_name] = base
    return base_name


def save_base(data_base):
    pass


"""
Автор: 
Цель: Функция ищет в базе данных вулканы типа type 
Вход: DataFrame 
Выход: DataFrame по фильтрам 
"""


def search_type(data_base, value):
    result = {}
    i = 0
    for base in data_base:
        if value in data_base[base]["Type"]:
            result[i] = data_base[base]
            i += 1
    return result


"""
Автор: 
Цель: Ищет в базе данных вулканы страны Country 
Вход: DataFrame 
Выход: DataFrame по фильтрам
"""


def search_country(data_base, value):
    result = {}
    i = 0
    for base in data_base:
        if value in data_base[base]["Country"]:
            result[i] = data_base[base]
            i += 1
    return result


"""
Автор: 
Цель: Ищет в базе данных вулканы расположения Location 
Вход: DataFrame 
Выход: DataFrame по фильтрам
"""


def search_location(data_base, value):
    result = {}
    i = 0
    for base in data_base:
        if value in data_base[base]["Country"]:
            result[i] = data_base[base]
            i += 1
    return result
