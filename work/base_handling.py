import pandas as pd
import numpy as np

# ['Year', 'Month', 'Day', 'Name', 'Location', 'Country', 'Latitude', 'Longitude', 'Elevation', 'Type', 'VEI', 'Agent', 'DEATHS', 'MISSING', 'DAMAGE_MILLIONS_DOLLARS', 'HOUSES_DESTROYED']
bd = pd.read_csv('volcano.csv', header=0)[
    ['Year', 'Month', 'Day', 'Name', 'Location', 'Country', 'Latitude', 'Longitude', 'Elevation', 'Type', 'VEI',
     'Agent', 'DEATHS', 'MISSING', 'DAMAGE_MILLIONS_DOLLARS', 'HOUSES_DESTROYED']]
columns = bd.columns.values.tolist()
work_list = {'Volcano Eruption1': bd, 'Volcano Eruption2': bd, 'Volcano Eruption3': bd, }


def read_base(path):
    pass


def save_base(base):
    pass
