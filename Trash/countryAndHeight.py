import matplotlib.pyplot as plt
import pandas as pd

bd = pd.read_csv('../volcano.csv', header=(0))
country = list(bd.Country)
heights = list(bd.Elevation)
plt.bar(country, heights)
plt.xlabel('volcano country')
plt.ylabel('volcano height')
plt.show()
