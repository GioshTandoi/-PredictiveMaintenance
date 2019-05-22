import pandas as pd
import numpy as np

chunks_directory = r'..\Data\chunks\\'
spread1_all = []
spread1_all_abs = []
timestamps_all = []
dates_all = []

for i in range(2, 9):
    # Load Chunk
    chunk = pd.read_csv(chunks_directory + 'ethercat_icam_v7_chunk' + str(i + 1) + '_events.csv')
    chunk.sort_values(by=['timestamp_'], inplace=True)
    # Filter records with not normal velocity
    #chunk.drop(chunk[chunk.yvelocityfeedbackvalue > 10 ** 9].index, inplace=True)
    # Take only the spread 1, timestamps, dates and add them to a single vector that contains all the timestamps
    spread1 = np.array(chunk['yactualposition'].values) - np.array(chunk['ypositionfeedback1value'].values)
    spread1_abs = abs(np.array(chunk['yactualposition'].values) - np.array(chunk['ypositionfeedback1value'].values))
    timestamps = chunk['timestamp_'].values
    dates = chunk['date'].values

    spread1_all.extend(spread1)
    spread1_all_abs.extend(spread1_abs)
    timestamps_all.extend(timestamps)
    dates_all.extend(dates)


df = pd.DataFrame(columns=['spread1', 'spread1_abs', 'timestamp_', 'date'])
df['spread1'] = spread1_all
df['spread1_abs'] = spread1_all_abs
df['timestamp_'] = timestamps_all
df['date'] = dates_all

df.to_csv(r'..\Data\spread\spread1.csv')
