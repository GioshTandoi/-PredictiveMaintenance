import pandas as pd
import numpy as np

chunks_directory = r'..\Data\chunks\\'
all_timestamps = []
for i in range(2, 9):
    #Load Chunk
    chunk = pd.read_csv(chunks_directory+'ethercat_icam_v7_chunk'+str(i+1)+'_events.csv')
    #Filter records with not normal velocity
    chunk.drop(chunk[chunk.yvelocityfeedbackvalue>10**9].index, inplace=True)
    # Take only the timestamps and add them to a single vector that contains all the timestamps
    timestamps = chunk['timestamp_'].values
    all_timestamps.extend(timestamps)

#Put all the timestamps to a .csv
df_all_timestamps = pd.DataFrame(data=all_timestamps, columns=['timestamps'])
df_all_timestamps.to_csv('all_timestamps.csv')