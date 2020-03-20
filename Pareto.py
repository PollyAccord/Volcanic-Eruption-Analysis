import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


bd = pd.read_csv('volcano.csv', header=(0))
dictionary = {}
for x in set(bd.Type):
    deaths = bd['DEATHS'][bd['Type'] == x].sum()
    if deaths != 0 and deaths > 1000:
        dictionary[x] = deaths

plt.bar({k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}.keys(), 
        {k: v for k, v in sorted(dictionary.items(), key=lambda item: item[1], reverse=True)}.values())
plt.xlabel('volcano type')
plt.ylabel('deaths')
plt.show()
