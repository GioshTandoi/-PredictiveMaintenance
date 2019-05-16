#Create a "QQ" chart for each Chunk against the total dataset
#Different colors on the chart represent movement on the different axes
#You need to close a couple of figures before the QQ chart appears
#Indicate which Chunk to test with the variable 'test' below

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


#Chunk to test against others
test = 9

chunk_n = test

file=os.path.join('..','..','..','..','chunks','ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')

#print(file)

df = pd.read_csv(file)
#df = pd.read_csv(r'..\..\..\..\chunks\ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')
df.sort_values(by=['timestamp_'], inplace=True)
    #df.describe()

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

bin_vec=np.linspace(-50000, 30000, 100)


"""n, bins, patches = plt.hist(x=new_df_Z['spread1'], bins='auto', color='#0504aa',
alpha=0.7, rwidth=0.85)"""
plt.figure(chunk_n)
nZ, binsZ, patchesZ = plt.hist(new_df_Z['spread1'], bins=bin_vec, cumulative=True, alpha=0.5, label='moving_in_Z')
nY, binsY, patchesY = plt.hist(new_df_Y['spread1'], bins=bin_vec, cumulative=True, alpha=0.5, label='moving_in_Y')
nX, binsX, patchesX = plt.hist(new_df_X['spread1'], bins=bin_vec, cumulative=True, alpha=0.5, label='moving_in_X')

nZtest=nZ
nYtest=nY
nXtest=nX

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



#Begin the CUMSUM of the other chunks

if test ==4:
    chunk_n = 5
    first = 5
else:
    chunk_n = 4
    first = 4


file=os.path.join('..','..','..','..','chunks','ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')

#print(file)

df = pd.read_csv(file)
#df = pd.read_csv(r'..\..\..\..\chunks\ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')
df.sort_values(by=['timestamp_'], inplace=True)
    #df.describe()

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

bin_vec=np.linspace(-50000, 30000, 100)


"""n, bins, patches = plt.hist(x=new_df_Z['spread1'], bins='auto', color='#0504aa',
alpha=0.7, rwidth=0.85)"""
plt.figure(chunk_n)
nZ, binsZ, patchesZ = plt.hist(new_df_Z['spread1'], bins=bin_vec, cumulative=True, alpha=0.5, label='moving_in_Z')
nY, binsY, patchesY = plt.hist(new_df_Y['spread1'], bins=bin_vec, cumulative=True, alpha=0.5, label='moving_in_Y')
nX, binsX, patchesX = plt.hist(new_df_X['spread1'], bins=bin_vec, cumulative=True, alpha=0.5, label='moving_in_X')

totZ=nZ
totY=nY
totX=nX

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



#Continue CUMSUM of other chunks
 
for chunk_n in range(4, 9):

    if chunk_n != test or chunk_n != first:

    #chunk_n = 4

        file=os.path.join('..','..','..','..','chunks','ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')

#print(file)

        df = pd.read_csv(file)
#df = pd.read_csv(r'..\..\..\..\chunks\ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')
        df.sort_values(by=['timestamp_'], inplace=True)
    #df.describe()

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
    
        bin_vec=np.linspace(-50000, 30000, 100)
    
    

    
        """n, bins, patches = plt.hist(x=new_df_Z['spread1'], bins='auto', color='#0504aa',
        alpha=0.7, rwidth=0.85)"""
    #plt.figure(chunk_n)
        nZ, binsZ, patchesZ = plt.hist(new_df_Z['spread1'], bins=bin_vec, cumulative=True, alpha=0.5, label='moving_in_Z')
        nY, binsY, patchesY = plt.hist(new_df_Y['spread1'], bins=bin_vec, cumulative=True, alpha=0.5, label='moving_in_Y')
        nX, binsX, patchesX = plt.hist(new_df_X['spread1'], bins=bin_vec, cumulative=True, alpha=0.5, label='moving_in_X')
        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('Spread1 (10^-4 mm)')
        plt.ylabel('Frequency')
        plt.title('Spread1 Histogram (chunk '+str(chunk_n)+')')
        plt.legend(loc='upper right')
    #plt.show()
    

        totZ=totZ+nZ
        totY=totY+nY
        totX=totX+nX


        print('Freqeuncies')
        print(nZ.shape)
        print('bins')
        print(binsZ.shape)
#maxfreq = n.max()
# Set a clean upper y-axis limit.
#plt.ylim(ymax=np.ceil(maxfreq / 10) * 10.5 if maxfreq % 10 else maxfreq + 20)

plt.figure("QQ"+str(test))
plt.title('QQ for Chunk '+str(test))
plt.legend(loc='upper right')
plt.xlabel('CUMSUM for each bin for Chunk'+str(test))
plt.ylabel('CUMSUM for each bin for other Chunks')
plt.plot(nZtest, totZ, 'bo', label='moving in Z')
plt.plot(nYtest, totY, 'r+', label='moving in Y')
plt.plot(nXtest, totX, 'k*', label='moving in X')
plt.show()
