import pandas as pd
import os
import numpy as np
import pprint


columns = ['timestamp', 'Z8NTC_Temp1', 'Z8NTC_Temp2', 'Z8NTC_Temp3', 'IMU_1_Temp', 'IMU_1_AccX', 'IMU_1_AccY',
           'IMU_1_AccZ', 'IMU_1_DpsX', 'IMU_1_DpsY', 'IMU_1_DpsZ', 'IMU_2_Temp', 'IMU_2_AccX', 'IMU_2_AccY',
           'IMU_2_AccZ', 'IMU_2_DpsX', 'IMU_2_DpsY', 'IMU_2_DpsZ', 'NT50_Slope_long', 'NT50_Slope_lateral']


directory_src_in_str = r"C:\Users\exprivia\PycharmProjects\untitled\ICAM\Modbus\New_Data\compliant_tables"
directory_src = os.fsencode(directory_src_in_str)
directory_destination = r'C:\Users\exprivia\PycharmProjects\untitled\ICAM\Modbus\New_Data\converted_to_std_format'
bad_n = 0
for file in os.listdir(directory_src):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        try:
            print(filename)
            data = pd.read_csv(directory_src_in_str + '\\' + filename, sep='\t')
        except:
            bad_n = bad_n + 1
            with open('converter_log_2.txt', 'at') as out:
                pp = pprint.PrettyPrinter(indent=4, stream=out)
                pp.pprint('file '+filename+' not regular')
                out.close()

        neg1 = data['Z8NTC_Temp1_sign'] == 0
        df1 = data['Z8NTC_Temp1'].where(neg1, -data['Z8NTC_Temp1'], axis=0).values
        df1 = np.array(df1).reshape(len(df1), 1)

        neg2 = data['Z8NTC_Temp2_sign'] == 0
        df2 = data['Z8NTC_Temp2'].where(neg2, -data['Z8NTC_Temp2'], axis=0).values
        df2 = np.array(df2).reshape(len(df2), 1)

        neg3 = data['Z8NTC_Temp3_sign'] == 0
        df3 = data['Z8NTC_Temp3'].where(neg3, -data['Z8NTC_Temp3'], axis=0).values
        df3 = np.array(df3).reshape(len(df3), 1)

        Z8NTC_values = np.concatenate((df1, df2, df3), axis=1)

        time_stamp = np.array(data['timestamp'].values).reshape(len(data['timestamp']), 1)

        partial_values = np.array(data.drop(['timestamp', 'Z-8NTC', 'Z8NTC_Temp1_sign', 'Z8NTC_Temp1',
                                             'Z8NTC_Temp2_sign', 'Z8NTC_Temp2', 'Z8NTC_Temp3_sign', 'Z8NTC_Temp3',
                                             'IMU_1', 'IMU_2', 'NT50'], axis=1).values)

        new_values = np.concatenate((time_stamp, Z8NTC_values, partial_values), axis=1)
        data = pd.DataFrame(data=new_values, columns=columns)
        data.to_csv(directory_destination + '\\' + filename, sep='\t', index=False)
        with open(r'C:\Users\exprivia\PycharmProjects\untitled\ICAM\Modbus\New_Data\joint_full_dataset.csv','a') as f:
            data.to_csv(f, sep='\t', index=False, header=False)


print(bad_n)