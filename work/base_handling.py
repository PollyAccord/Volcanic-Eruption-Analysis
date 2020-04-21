import pandas as pd
import globals as glob

# ['Year', 'Month', 'Day', 'Name', 'Location', 'Country', 'Latitude', 'Longitude', 'Elevation', 'Type', 'VEI', 'Agent', 'DEATHS', 'INJURIES', 'MISSING', 'DAMAGE_MILLIONS_DOLLARS', 'HOUSES_DESTROYED']
bd = pd.read_csv('base/volcano.csv', header=0)[['Year', 'Month', 'Day', 'Name', 'Location',
                                                'Country', 'Latitude', 'Longitude', 'Elevation',
                                                'Type', 'VEI', 'Agent', 'DEATHS', 'INJURIES', 'MISSING',
                                                'DAMAGE_MILLIONS_DOLLARS', 'TSU', 'EQ']]

glob.work_list['Volcano Eruption'] = bd

def read_base(path):
    base = pd.read_csv(path, header=0)[['Year', 'Month', 'Day', 'Name', 'Location', 'Country', 'Latitude', 'Longitude',
                                        'Elevation', 'Type', 'VEI', 'Agent', 'DEATHS', 'MISSING',
                                        'DAMAGE_MILLIONS_DOLLARS',
                                        'HOUSES_DESTROYED']]
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

