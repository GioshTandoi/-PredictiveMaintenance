import pandas as pd
import numpy as np


mean = 0.708727
std = 0.192176
min_spread = 0.023400
first_quartile = 0.578619
second_quartile = 0.673631
third_quartile = 0.817184
max_spread = 1.685569

spread1_abs_mm_series_min = pd.read_csv(r'C:\Users\exprivia\PycharmProjects\-PredictiveMaintenance\ICAM\Ethercat\Data\spread\spread1_abs_mm_series_min.csv')

days_2_years = pd.date_range('2017-05-20', '2019-05-25', freq='D')
start_hour = '8:00:00'
end_hour = '20:00:00'

date_index = []
random_spread = []
for day in days_2_years:
    this_date_index = pd.date_range(str(day)[:11]+start_hour, str(day)[:11]+end_hour, freq='min')
    this_random_spread = np.random.normal(loc=0.708727, scale=0.192176, size=len(this_date_index))
    date_index.extend(this_date_index)
    random_spread.extend(this_random_spread)

fake_dataset = pd.Series(data=random_spread, index=date_index)