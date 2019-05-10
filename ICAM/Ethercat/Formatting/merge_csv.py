# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 14:34:40 2019

@author: exprivia
"""

import pandas as pd
import os

directory_in_str = r"C:\Users\exprivia\Desktop\DF\ICAM\Dati_Rielaborati\MasterData\06-03-2019DATA\Full DataSet\Calculated_tables"
directory = os.fsencode(directory_in_str)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    print(filename)
    if filename.endswith(".csv"):
        if os.path.getsize(directory_in_str+'\\'+filename) > 0:
            data = pd.read_csv(directory_in_str+'\\'+filename, sep=',')
            try:
                with open(r'C:\Users\exprivia\Desktop\DF\ICAM\Dati_Rielaborati\MasterData\06-03-2019DATA\Full DataSet_03052019\joint_full_dataset.csv', 'a') as f:
                    data.to_csv(f, header=None, index=True)
            except:
                print('Parsing mismatch')
                continue
        else:
            print('Empty file')