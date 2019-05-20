import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import scipy.stats as ss


test_chunk_1 = 6
test_chunk_2 = 9


chunk_n = test_chunk_1

file=os.path.join('..','..','..','..','chunks','ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')

#print(file)

df = pd.read_csv(file)
#df = pd.read_csv(r'..\..\..\..\chunks\ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')
df.sort_values(by=['timestamp_'], inplace=True)
df.describe()

spread4 = (np.array(df['yactualposition'].values) - np.array(df['ypositionfeedback1value'].values)).reshape(len(df['ypositionfeedback1value'].values), 1)
spread4Shift = spread4-np.mean(spread4)
spread4=spread4Shift
ZFrequencyMonitor4 = np.array(df['zfrequencymonitor'].values).reshape(len(df['zfrequencymonitor'].values), 1)
YVelocityFeedbackValue4 = np.array(df['yvelocityfeedbackvalue'].values).reshape(len(df['yvelocityfeedbackvalue'].values),1)
XVelocityFeedbackValue4 = np.array(df['xvelocityfeedbackvalue'].values).reshape(len(df['yvelocityfeedbackvalue'].values), 1)




new_df4 = pd.DataFrame(data=np.concatenate((spread4, spread4Shift, ZFrequencyMonitor4, YVelocityFeedbackValue4, XVelocityFeedbackValue4), axis=1),
                      columns=['spread4', 'spread4Shift', 'zfrequencymonitor', 'yvelocityfeedbackvalue', 'xvelocityfeedbackvalue'])

is_moving_Z4 = new_df4['zfrequencymonitor'] != 0
is_moving_Y4 = new_df4['yvelocityfeedbackvalue'] != 0
is_moving_X4 = new_df4['xvelocityfeedbackvalue'] != 0

new_df_Z4 = new_df4[is_moving_Z4]
new_df_Y4 = new_df4[is_moving_Y4]
new_df_X4 = new_df4[is_moving_X4]



chunk_n = test_chunk_2

file=os.path.join('..','..','..','..','chunks','ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')

#print(file)

df = pd.read_csv(file)
#df = pd.read_csv(r'..\..\..\..\chunks\ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')
df.sort_values(by=['timestamp_'], inplace=True)
df.describe()

spread5 = (np.array(df['yactualposition'].values) - np.array(df['ypositionfeedback1value'].values)).reshape(len(df['ypositionfeedback1value'].values), 1)
spread5 = spread5-np.mean(spread5)
ZFrequencyMonitor5 = np.array(df['zfrequencymonitor'].values).reshape(len(df['zfrequencymonitor'].values), 1)
YVelocityFeedbackValue5 = np.array(df['yvelocityfeedbackvalue'].values).reshape(len(df['yvelocityfeedbackvalue'].values),1)
XVelocityFeedbackValue5 = np.array(df['xvelocityfeedbackvalue'].values).reshape(len(df['yvelocityfeedbackvalue'].values), 1)




new_df5 = pd.DataFrame(data=np.concatenate((spread5, ZFrequencyMonitor5, YVelocityFeedbackValue5, XVelocityFeedbackValue5), axis=1),
                      columns=['spread5', 'zfrequencymonitor', 'yvelocityfeedbackvalue', 'xvelocityfeedbackvalue'])

is_moving_Z5 = new_df5['zfrequencymonitor'] != 0
is_moving_Y5 = new_df5['yvelocityfeedbackvalue'] != 0
is_moving_X5 = new_df5['xvelocityfeedbackvalue'] != 0

new_df_Z5 = new_df5[is_moving_Z5]
new_df_Y5 = new_df5[is_moving_Y5]
new_df_X5 = new_df5[is_moving_X5]



[W, p] = ss.levene(new_df_Y4['spread4'],new_df_Y5['spread5'])

print('W')
print(W)
print('p-value')
print(p)

W2=float(format(W, '.2f'))
p2=float(format(p, '.3f'))


"""n, bins, patches = plt.hist(x=new_df_Z['spread1'], bins='auto', color='#0504aa',
                            alpha=0.7, rwidth=0.85)"""
plt.figure(test_chunk_1*test_chunk_2)
nY5, binsY5, patchesY5 = plt.hist(new_df_Y5['spread5'], density=True, bins='auto', alpha=0.5, label='moving_in_Y'+str(test_chunk_2))
#nY4Shift, binsY4Shift, patchesY4Shift = plt.hist(new_df_Y4['spread4Shift'], bins='auto', alpha=0.5, label='moving_in_Y'+str(test_chunk_2)+' Shift')
nY4, binsY4, patchesY4 = plt.hist(new_df_Y4['spread4'], density=True, bins='auto', alpha=0.5, label='moving_in_Y'+str(test_chunk_1))
#nX, binsX, patchesX = plt.hist(new_df_X['spread1'], bins='auto', alpha=0.5, label='moving_in_X')

plt.grid(axis='y', alpha=0.75)
plt.xlabel('Spread1 (10^-4 mm)')
plt.ylabel('Frequency')
plt.title('Histograms of spread moving in Y. Levene: W='+str(W2)+' p='+str(p2))
plt.legend(loc='upper right')
plt.show()

print('Freqeuncies')
print(nY4.shape)
print('bins')
print(binsY4.shape)
#maxfreq = n.max()
# Set a clean upper y-axis limit.
#plt.ylim(ymax=np.ceil(maxfreq / 10) * 10.5 if maxfreq % 10 else maxfreq + 20)
