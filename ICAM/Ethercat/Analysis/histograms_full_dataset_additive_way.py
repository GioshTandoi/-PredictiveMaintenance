import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from operator import add

statistics_spread = pd.read_csv('chunks_statistics_spread.csv')
min = statistics_spread['min'].values.min()
max = statistics_spread['max'].values.max()

bins = np.linspace(min, max, num=200, endpoint=True)
print(bins)
chunks_directory = r'C:\Users\exprivia\Desktop\DF\ICAM\Dati_Rielaborati\MasterData\chunks\ethercat_icam_v7_chunk'
Z_frequencies = [0] * 199
Y_frequencies = [0] * 199
X_frequencies = [0] * 199
n_rows = 0
sumZ = 0
sumY = 0
sumX = 0

z_y_x = pd.DataFrame(columns=['is_moving_Z', 'is_moving_Y', 'new_df_X'])
z_y_x = pd.DataFrame(columns=['zfrequencymonitor', 'yvelocityfeedbackvalue', 'xvelocityfeedbackvalue'])
for i in range(2, 9):
    df = pd.read_csv(chunks_directory+str(i+1)+'_events.csv')
    df.sort_values(by=['timestamp_'], inplace=True)

    spread1 = (np.array(df['yactualposition'].values) - np.array(df['ypositionfeedback1value'].values)).reshape(
        len(df['ypositionfeedback1value'].values), 1)
    ZFrequencyMonitor = np.array(df['zfrequencymonitor'].values).reshape(len(df['zfrequencymonitor'].values), 1)
    YVelocityFeedbackValue = np.array(df['yvelocityfeedbackvalue'].values).reshape(
        len(df['yvelocityfeedbackvalue'].values), 1)
    XVelocityFeedbackValue = np.array(df['xvelocityfeedbackvalue'].values).reshape(
        len(df['xvelocityfeedbackvalue'].values), 1)

    new_df = pd.DataFrame(
        data=np.concatenate((spread1, ZFrequencyMonitor, YVelocityFeedbackValue, XVelocityFeedbackValue), axis=1),
        columns=['spread1', 'zfrequencymonitor', 'yvelocityfeedbackvalue', 'xvelocityfeedbackvalue'])

    is_moving_Z = new_df['zfrequencymonitor'] != 0
    is_moving_Y = new_df['yvelocityfeedbackvalue'] != 0
    is_moving_X = new_df['xvelocityfeedbackvalue'] != 0


    new_df_Z = new_df[is_moving_Z]
    new_df_Y = new_df[is_moving_Y]
    new_df_X = new_df[is_moving_X]

    sumZ = sumZ + sum(new_df_Z['spread1'].values)
    sumY = sumY + sum(new_df_Y['spread1'].values)
    sumX = sumX + sum(new_df_X['spread1'].values)

    plt.figure(i)
    nZ, binsZ, patchesZ = plt.hist(new_df_Z['spread1'], bins=bins, alpha=0.5, label='moving_in_Z')
    nY, binsY, patchesY = plt.hist(new_df_Y['spread1'], bins=bins, alpha=0.5, label='moving_in_Y')
    nX, binsX, patchesX = plt.hist(new_df_X['spread1'], bins=bins, alpha=0.5, label='moving_in_X')
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Spread1 (10^-4 mm)')
    plt.ylabel('Frequency')
    plt.title('Spread1 Histogram (chunk ' + str(i+1) + ')')
    plt.legend(loc='upper right')
    plt.show()

    print('nZ.shape')
    print(nZ.shape)
    print('nZ******************************')
    print(nZ)
    print('len-----------Z_frequencies')
    print(len(Z_frequencies))
    Z_frequencies = list(map(add, Z_frequencies, nZ))
    Y_frequencies = list(map(add, Y_frequencies, nY))
    X_frequencies = list(map(add, X_frequencies, nX))
    n_rows = n_rows + len(df['ypositionfeedback1value'].values)

print('******************* Z_Frequencies *****************')
print(Z_frequencies)
print('******************* Y_Frequencies *****************')
print(Y_frequencies)
print('******************* X_Frequencies *****************')
print(X_frequencies)
print('n_rows')
print(n_rows)

Z_frequencies.append(0)
Y_frequencies.append(0)
X_frequencies.append(0)
plt.figure(i+1)
plt.bar(bins, Z_frequencies, width=456.43216081, align='edge', label='moving_in_Z')
plt.bar(bins, Y_frequencies,  width=456.43216081, align='edge', label='moving_in_Y')
plt.bar(bins, X_frequencies, width=456.43216081, align='edge', label='moving_in_X')
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Spread1 (10^-4 mm)')
plt.ylabel('Frequency')
plt.title('Spread1 Histogram (Full Dataset)')
plt.legend(loc='upper right')
plt.show()

mean_Z = sumZ/sum(Z_frequencies)
mean_Y = sumY/sum(Y_frequencies)
mean_X = sumX/sum(X_frequencies)





