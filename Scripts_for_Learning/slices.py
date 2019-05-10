import pandas as pd
import numpy as np


directory_src_in_str = r"C:\Users\exprivia\PycharmProjects\untitled\ICAM\Modbus\New_Data\compliant_tables"
data = pd.read_csv(directory_src_in_str + '\\' + '20181210_144305.csv', sep='\t')

neg1 = data['Z8NTC_Temp1_sign'] == 0
df1 = data['Z8NTC_Temp1'].where(neg1, -data['Z8NTC_Temp1'], axis=0).values
df1 = np.array(df1).reshape(len(df1), 1)