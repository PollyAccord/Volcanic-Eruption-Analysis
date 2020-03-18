import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


bd = pd.read_csv('volcano.csv', header=(0))
deaths = list(bd.DEATHS)
bins = [x*1000 for x in range(int(bd.Elevation.max() / 1000))]
plt.hist(deaths, bins, histtype='bar')
plt.xlabel('volcano height')
plt.ylabel('deaths')
plt.show()
