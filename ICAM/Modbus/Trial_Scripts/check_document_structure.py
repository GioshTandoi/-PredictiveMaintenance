import pandas as pd
import os
import numpy as np
import pprint


def get_fields(df):
    columns_present = list()
    for column in df.columns:
        if df[column].dtype == object:
            columns_present.append(str(df[column].values[0]))
    return columns_present


directory_in_str = r"C:\Users\exprivia\PycharmProjects\untitled\ICAM\Modbus\Original_Data"
directory = os.fsencode(directory_in_str)

file_map = {}

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        print(filename)
        try:
            data = pd.read_csv(directory_in_str+'\\'+filename, sep=' ', header=None).rename(columns = lambda x: f'col_{x + 1}')
            data = np.array(data.values)
            description = {}
            n = 0
            for raw in data:
                raw_description = {}
                i = 0
                for i in range(len(raw)):
                    if not isinstance(raw[i], float) and not isinstance(raw[i], int):
                        c = 0
                        if i+1 < len(raw):
                            j = i + 1
                            while isinstance(raw[j], float) or isinstance(raw[j], int):
                                c = c + 1
                                j = j + 1
                                if j >= len(raw):
                                    break;
                        raw_description[raw[i]] = c

                description[n] = raw_description
                n = n + 1

            file_map[filename] = description[0]
        except:
            file_map[filename] = 'ERROR'
            print('error'+filename)


with open('output.txt', 'wt') as out:
    pp = pprint.PrettyPrinter(indent=4,stream=out)
    pp.pprint(file_map)
