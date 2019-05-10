import pandas as pd
import os
import numpy as np
import pprint

directory_in_str = r"C:\Users\exprivia\PycharmProjects\untitled\ICAM\Modbus\Original_Data"
directory = os.fsencode(directory_in_str)

file_map = {}

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        print(filename)
        try:
            data = pd.read_csv(directory_in_str+'\\'+filename, sep=' ', header=None).rename(columns=lambda x: f'col_{x + 1}')
            data = np.array(data.values)
            

        except:
            file_map[filename] = 'ERROR'
            print('error'+filename)


with open('output.txt', 'wt') as out:
    pp = pprint.PrettyPrinter(indent=4,stream=out)
    pp.pprint(file_map)