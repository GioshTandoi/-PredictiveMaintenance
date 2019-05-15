import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

chunk_n = 4
df = pd.read_csv(r'C:\Users\exprivia\Desktop\DF\ICAM\Dati_Rielaborati\MasterData\chunks\ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')
df.sort_values(by=['timestamp_'], inplace=True)
df.describe()

spread1 = (np.array(df['yactualposition'].values) - np.array(df['ypositionfeedback1value'].values)).reshape(len(df['ypositionfeedback1value'].values), 1)
ZFrequencyMonitor = np.array(df['zfrequencymonitor'].values).reshape(len(df['zfrequencymonitor'].values), 1)
YVelocityFeedbackValue = np.array(df['yvelocityfeedbackvalue'].values).reshape(len(df['yvelocityfeedbackvalue'].values),1)
XVelocityFeedbackValue = np.array(df['xvelocityfeedbackvalue'].values).reshape(len(df['yvelocityfeedbackvalue'].values), 1)

new_df = pd.DataFrame(data=np.concatenate((spread1, ZFrequencyMonitor, YVelocityFeedbackValue, XVelocityFeedbackValue), axis=1),
                      columns=['spread1', 'zfrequencymonitor', 'yvelocityfeedbackvalue', 'xvelocityfeedbackvalue'])

is_moving_Z = new_df['zfrequencymonitor'] != 0
is_moving_Y = new_df['yvelocityfeedbackvalue'] != 0
is_moving_X = new_df['xvelocityfeedbackvalue'] != 0

new_df_Z = new_df[is_moving_Z]
new_df_Y = new_df[is_moving_Y]
new_df_X = new_df[is_moving_X]


"""n, bins, patches = plt.hist(x=new_df_Z['spread1'], bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=0.85)"""
plt.figure(chunk_n)
nZ, binsZ, patchesZ = plt.hist(new_df_Z['spread1'], bins='auto', alpha=0.5, label='moving_in_Z')
nY, binsY, patchesY = plt.hist(new_df_Y['spread1'], bins='auto', alpha=0.5, label='moving_in_Y')
nX, binsX, patchesX = plt.hist(new_df_X['spread1'], bins='auto', alpha=0.5, label='moving_in_X')
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Spread1 (10^-4 mm)')
plt.ylabel('Frequency')
plt.title('Spread1 Histogram (chunk '+str(chunk_n)+')')
plt.legend(loc='upper right')
plt.show()

print('Freqeuncies')
print(nZ.shape)
print('bins')
print(binsZ.shape)
#maxfreq = n.max()
# Set a clean upper y-axis limit.
#plt.ylim(ymax=np.ceil(maxfreq / 10) * 10.5 if maxfreq % 10 else maxfreq + 20)