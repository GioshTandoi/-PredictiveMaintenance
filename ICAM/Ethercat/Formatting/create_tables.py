# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 15:58:56 2019

@author: Utente
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime

def to_Calculated_Table(data):
    columns = ['MachineInRun', 'XDiagnosis', 'XActualPosition', 'XVelocityFeedbackValue',
           'YDiagnosis', 'YActualPosition', 'YActualCurrent', 'YVelocityFeedbackValue',
           'YPositionFeedback1Value', 'ZEncoder_Counter', 'FenceUpDiagnosis',
           'FenceUpActualPosition', 'FenceUpVelocityFeedbackValue',
           'FenceDownDiagnosis','FenceDownActualPosition', 'FenceDownVelocityFeedbackValue', 
           'YResistiveLoad','XThermalLoad', 'XResistiveLoad', 'ZFrequencyMonitor',
           'ZCurrentMonitor','ZVoltageMonitor', 'XActualCurrent', 'ZFaultMonitor', 
           'FenceUpActualCurrent','YDCBusVoltage', 'FenceDownActualCurrent',
           'YThermalLoad', 'TFrequencyMonitor','TCurrentMonitor', 
           'TVoltageMonitor', 'TFaultMonitor', 'Slot2DoorMFeedBack1',
           'Slot2DoorMFeedBack2', 'Slot2DoorMFeedBack3', 'Slot2DoorMFeedBack4',
           'Slot2DoorMFeedBack5','Slot2DoorMFeedBack6', 'Slot2DoorMFeedBack7',
           'Slot2DoorMFeedBack8', 'ColumnCenteringSide1Pos','ColumnCenteringSide1Neg',
           'ColumnCenteringSide2Pos', 'ColumnCenteringSide2Neg','XDCBusVoltage', 
           'AxisTilting_LimitSwitch', 'PresenceInCell_OnBoard', 'Slot2DoorOpenCh1', 
           'Slot2DoorOpenCh2', 'YZAxis', 'TrayAlignment', 'Xaxis', 
           'RowColumnPresence', 'Various1', 'date','timestamp']
    etherCat_table = pd.DataFrame(columns=columns)
    
    etherCat_table['MachineInRun'] = data[:,0]
    j = 1
    for i in range(1, 16):
        header = columns[i]
        cols = []
        col1 = np.array(data[:, j]).reshape(len(data[:, i]), 1)
        col2 = np.array(data[:, j+1]).reshape(len(data[:, i+1]), 1)
        col3 = np.array(data[:, j+2]).reshape(len(data[:, i+2]), 1)
        col4 = np.array(data[:, j+3]).reshape(len(data[:, i+3]), 1)

        j = j+3+1
        cols = np.concatenate((col1, col2, col3, col4), axis=1)
        value = []
        for row in cols: 
            value.append(row[0]+ 256*row[1] +65536*row[2] +16777216*row[3])
        etherCat_table[header] = value
    
    for i in range(16, 45):
        header = columns[i]
        cols = []
        col1 = np.array(data[:, j]).reshape(len(data[:, i]), 1)
        col2 = np.array(data[:, j+1]).reshape(len(data[:, i+1]), 1)
        j = j+1+1
        cols = np.concatenate((col1, col2), axis=1)
        value = []
        for row in cols: 
            value.append(row[0]+ 256*row[1])
        etherCat_table[header] = value
    
    for i in range(45, 54):
        header = columns[i]
        col1 = np.array(data[:, j])
        etherCat_table[header] = col1
        j = j+1
    etherCat_table['date'] = data[:,-1]
    return etherCat_table

def calculate_timestamps(dates):
    timestamps = []
    for date in etherCat_table['date']:
        separated_fields = date.split(':')
        if len(separated_fields[3]) == 2: 
            milliseconds='0'+separated_fields[3]
        else: 
            milliseconds=separated_fields[3]
        temp1 = separated_fields[0]+':'+separated_fields[1]+':'+separated_fields[2]+'.'+milliseconds
        datetime_object = datetime.strptime(temp1, '%Y-%m-%d %H:%M:%S.%f')
        timestamp = datetime_object.timestamp()*1000
        timestamps.append(timestamp)
    
    return timestamps
    

directory_in_str = r"C:\Users\exprivia\Desktop\DF\ICAM\Dati Forniti da ICAM\06-03-2019DATA\Trials\masterData_trial4"
directory = os.fsencode(directory_in_str) 

for file in os.listdir(directory): 
    filename = os.fsdecode(file) 
    print(filename)
    if filename.endswith(".csv"):
        if os.path.getsize(directory_in_str+'\\'+filename) > 0:
            data = pd.read_csv(directory_in_str+'\\'+filename, sep=',', header=None)
            data = np.array(data.values)
            try: 
                etherCat_table = to_Calculated_Table(data)
                etherCat_table['timestamp'] = calculate_timestamps(etherCat_table['date'].values)
                etherCat_table.to_csv(r"C:\Users\exprivia\Desktop\DF\ICAM\Dati Forniti da ICAM\06-03-2019DATA\Trials\masterData_trial4_calculated_tables\\"+filename, index=False)
                with open(r'C:\Users\exprivia\Desktop\DF\ICAM\Dati Forniti da ICAM\06-03-2019DATA\Trials\joint_full_dataset.csv', 'a') as f:
                    etherCat_table.to_csv(f, header=False)
            except:
                print('Parsing mismatch')
                continue
        else: 
            print('Empty file')
        #frames.append(etherCat_table)

#Add header row