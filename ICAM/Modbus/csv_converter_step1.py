import pandas as pd
import os
import numpy as np
import pprint

pd.set_option('display.max_columns', None)

# Schema definition
schema = {'col_1': 1544841854.76, 'col_2': 'Z-8NTC', 'col_3': 0,
          'col_4': 148, 'col_5': 0, 'col_6': 143, 'col_7': 0, 'col_8': 145,
          'col_9': 'IMU_1', 'col_10': 1523, 'col_11': 64563, 'col_12': 10, 'col_13': 5,
          'col_14': 57028, 'col_15': 1557, 'col_16': 857, 'col_17': 'IMU_2', 'col_18': 1523, 'col_19': 64563,
          'col_20': 10, 'col_21': 5, 'col_22': 57028, 'col_23': 1557, 'col_24': 857, 'col_25': 'NT50',
          'col_26': 64767, 'col_27': 23774}

schema_df = pd.DataFrame(data=schema, index=[0])

with open('output32.txt', 'at') as out:
    pp = pprint.PrettyPrinter(indent=4, stream=out)
    pp.pprint(schema_df)

# columns definition

columns = ['timestamp', 'Z-8NTC', 'Z8NTC_Temp1_sign', 'Z8NTC_Temp1', 'Z8NTC_Temp2_sign', 'Z8NTC_Temp2',
           'Z8NTC_Temp3_sign', 'Z8NTC_Temp3', 'IMU_1', 'IMU_1_Temp', 'IMU_1_AccX', 'IMU_1_AccY',
           'IMU_1_AccZ', 'IMU_1_DpsX', 'IMU_1_DpsY', 'IMU_1_DpsZ', 'IMU_2', 'IMU_2_Temp',
           'IMU_2_AccX', 'IMU_2_AccY', 'IMU_2_AccZ', 'IMU_2_DpsX', 'IMU_2_DpsY', 'IMU_2_DpsZ',
           'NT50', 'NT50_Slope_long', 'NT50_Slope_lateral']

# loop over .csv files to convert them into a pandas data frame
good_n = 0
bad_n = 0
directory_in_str = r"C:\Users\exprivia\PycharmProjects\untitled\ICAM\Modbus\Trial_subset_original_data"
directory = os.fsencode(directory_in_str)
directory_destination = r'C:\Users\exprivia\PycharmProjects\untitled\ICAM\Modbus\New_Data\compliant_tables'

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        try:
            print(filename)
            data = pd.read_csv(directory_in_str + '\\' + filename, sep=' ', header=None).rename(columns=lambda x: f'col_{x + 1}')
        except:
            bad_n = bad_n + 1
            with open('converter_log.txt', 'at') as out:
                pp = pprint.PrettyPrinter(indent=4, stream=out)
                pp.pprint('file '+filename+' not regular')
                out.close()

        data.dropna(axis=1, inplace=True)
        shape = schema_df.shape[1] == data.shape[1]

        if shape:
            types = schema_df.dtypes == data.dtypes
            if types.all():
                with open('converter_log.txt', 'at') as out:
                    pp = pprint.PrettyPrinter(indent=4, stream=out)
                    pp.pprint('file '+filename+' compliant to schema')
                    out.close()
                good_n = good_n + 1
                df = pd.DataFrame(data=data.values, columns=columns)
                df.to_csv(directory_destination + '\\' + filename, sep='\t', index=False)
            else:
                with open('converter_log.txt', 'at') as out:
                    pp = pprint.PrettyPrinter(indent=4, stream=out)
                    pp.pprint('file '+filename+' NOT compliant to schema')
                    out.close()
                bad_n = bad_n + 1

with open('total_count_good_bad.txt', 'at') as out:
    pp = pprint.PrettyPrinter(indent=4, stream=out)
    pp.pprint('Number of passed files: '+str(good_n)+'           Number of not passed files: '+str(bad_n))
    out.close()
