import pandas as pd
import numpy as np

# ['Year', 'Month', 'Day', 'Name', 'Location', 'Country', 'Latitude', 'Longitude', 'Elevation', 'Type', 'VEI', 'Agent', 'DEATHS', 'MISSING', 'DAMAGE_MILLIONS_DOLLARS', 'HOUSES_DESTROYED']
bd = pd.read_csv('base/volcano.csv', header=0)[['Year', 'Month', 'Day', 'Name', 'Location',
                                                'Country', 'Latitude', 'Longitude', 'Elevation',
                                                'Type', 'VEI','Agent', 'DEATHS', 'MISSING',
                                                'DAMAGE_MILLIONS_DOLLARS', 'HOUSES_DESTROYED']]
columns = ['Year', 'Month', 'Day', 'Name', 'Location', 'Country', 'Latitude', 'Longitude',
           'Elevation', 'Type', 'VEI', 'Agent', 'DEATHS', 'MISSING', 'DAMAGE_MILLIONS_DOLLARS',
           'HOUSES_DESTROYED']
work_list = {'Volcano Eruption1': bd, 'Volcano Eruption2': bd, 'Volcano Eruption3': bd, }
current_base = np.array([])

def read_base(path):
    base = pd.read_csv(path, header=0)[['Year', 'Month', 'Day', 'Name', 'Location', 'Country', 'Latitude', 'Longitude',
                                        'Elevation', 'Type', 'VEI', 'Agent', 'DEATHS', 'MISSING', 'DAMAGE_MILLIONS_DOLLARS',
                                        'HOUSES_DESTROYED']]
    base_name = path[path.rfind('\\') + 1:path.rfind('.')]
    work_list[base_name] = base
    return base_name



def save_base(base):
    pass
