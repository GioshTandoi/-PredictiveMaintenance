import pandas as pd
import numpy as np


def get_fields(df):
    columns_present = list()
    for column in df.columns:
        print(df[column].dtype)
        if df[column].dtype == object:
            columns_present.append(str(df[column].values[0]))
    return columns_present 


def get_columns(fies):
    columns = ['timestamp']
    for fi in fies:
        if 'Z-8NTC' in fi:
            columns.extend(('Z8NTC_Temp1', 'Z8NTC_Temp2', 'Z8NTC_Temp3'))
        elif 'IMU' in fi:
            columns.extend((fi + '_Temp', fi + '_AccX', fi + '_AccY', fi + '_AccZ',
                            fi + '_DpsX', fi + '_DpsY', fi + '_DpsZ'))
        elif 'NT50' in fi:
            columns.extend(('NT50_Slope_long', 'NT50_Slope_lateral'))

        elif 'Z4RTD2' in fi:
            columns.extend(('Z4RTD2_Temp_Motor_Z', 'Z4RTD2_Temp_Motor_X', 'Z4RTD2_Temp_Motor_Y',))
    return columns


def add_signs(Z8NTC_values):
    df = pd.DataFrame(data=Z8NTC_values).rename(columns=lambda x: f'col_{x + 1}')
    print(df)
    neg1 = df['col_1'] == 1
    df1 = np.array(df['col_2'].where(neg1, -df['col_2'], axis=0).values)
    neg2 = df['col_3'] == 1
    df2 = np.array(df['col_4'].where(neg2, -df['col_4'], axis=0).values)
    neg3 = df['col_5'] == 1
    df3 = np.array(df['col_6'].where(neg3, -df['col_6'], axis=0).values)
    Z8NTC_values = np.concatenate((df1, df2, df3), axis=1)
    return Z8NTC_values


f = r"C:\Users\exprivia\PycharmProjects\untitled\ICAM\Modbus\Original_Data\20181115_144455.csv"
data = pd.read_csv(f, sep=' ', header=None).rename(columns = lambda x: f'col_{x + 1}')

fields = get_fields(data)
print(fields)

cols = get_columns(fields)
print(cols)

timestamp = data['col_1']
data = np.array(data.values)
print('Dataaaa')
print(data)
j = 0
column_values = np.array([])

for field in fields:
    if 'Z-8NTC' in field:
        Z8NTC_columns = add_signs(data[:, 2:8])
        column_values = np.concatenate((column_values,Z8NTC_columns), axis=1)

    if 'IMU' in field:
        start = 9+(j*7)+1
        end = 16+(j*7)+1
        IMU_Fields = data[:, start:end]
        j = j + 1
        column_values = np.concatenate((column_values, IMU_Fields), axis=1)

    if 'Z4RTD2' in field:
        Z4RTD2_columns = data[:, -3:]
        column_values = np.concatenate((column_values, Z4RTD2_columns), axis=1)

    if 'NT50' in field and 'Z4RTD2' in fields[-1]:
        NT50_columns = data[:, -6:-8]
        column_values = np.concatenate((column_values, NT50_columns), axis=1)
    elif 'NT50' in field and 'Z4RTD2' not in fields[-1]:
        NT50_columns = data[:, -2]
        column_values = np.concatenate((column_values, NT50_columns), axis=1)


converted_df = pd.DataFrame(data=column_values, columns=cols)
print(converted_df)