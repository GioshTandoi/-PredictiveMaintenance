import pandas as pd

df = pd.read_csv(r'C:\Users\exprivia\PycharmProjects\-PredictiveMaintenance\ICAM\Ethercat\Data\spread\spread1.csv')

i = 0
j = 0
chunk_indices = []
differences = df['diff'].values
ok = True

while ok:
    while differences[i]<3.6e+6:
        chunk_indices.extend(j)
        i = i + 1
    if i == len(differences)-1:
        ok = False
    else:
        j = j +1

resample = series.resample('A')
quarterly_mean_sales = resample.sum()
print(quarterly_mean_sales.head())
quarterly_mean_sales.plot()