import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


bd = pd.read_csv('volcano.csv', header=(0))
dictionary = {}
dictionary['others'] = 0
for x in set(bd.Type):
    deaths = bd['DEATHS'][bd['Type'] == x].sum()
    if deaths > 5000:
        dictionary[x] = deaths
    else:
        dictionary['others'] += deaths
plt.pie(dictionary.values(), labels=dictionary.keys())
plt.title("Deaths caused by different volcanos' types")
plt.show()
