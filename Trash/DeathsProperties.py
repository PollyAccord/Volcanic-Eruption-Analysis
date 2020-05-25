import math as m

import pandas as pd

bd = pd.read_csv('../volcano.csv', header=(0))

sortedSample = bd['DEATHS'].sort_values()[bd['DEATHS'] == bd['DEATHS']]  # get rid of nan
average = m.ceil(sortedSample.mean())
med = sortedSample.median()
print('Среднее число смертей за одно извержение: ', average)
print('Медиана: ', med)
print('Мода: ', sortedSample.mode().values[0])
if average == med:
    s = 'симметрия'
elif average > med:
    s = 'acимметрия вправо'
else:
    s = 'acимметрия влево'
print('Форма плотности распределения: ', s)
print('Нижняя квартиль: ', sortedSample.quantile(0.25))
print('Врехняя квартиль: ', sortedSample.quantile(0.75))

disp = (sortedSample.apply(lambda x: (x-average)**2).sum())/(len(sortedSample) - 1)
print('Выборочная дисперсия: ', disp)

