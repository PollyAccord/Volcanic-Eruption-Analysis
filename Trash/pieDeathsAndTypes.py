import matplotlib.pyplot as plt
import pandas as pd

bd = pd.read_csv('../volcano.csv', header=(0))
dictionary = {}
dictionary['others'] = 0
for x in set(bd.Type):
    deaths = bd['DEATHS'][bd['Type'] == x].sum()
    if deaths > 5000:
        dictionary[x] = deaths
    else:
        dictionary['others'] += deaths
plt.pie(dictionary.values(), labels=dictionary.keys(), autopct='%1.1f%%')
plt.title("Deaths caused by different types of volcano")
plt.show()
