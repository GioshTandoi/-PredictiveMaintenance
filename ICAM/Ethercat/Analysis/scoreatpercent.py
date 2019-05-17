import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import stats

test = 6
vs=5

chunk_n = test

file=os.path.join('..','..','..','..','chunks','ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')

#print(file)                                                                    

df = pd.read_csv(file)

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

percentiles=np.linspace(1, 99, 99)

testZpercentiles=stats.scoreatpercentile(new_df_Z['spread1'], percentiles)



#################################



chunk_n = vs

file=os.path.join('..','..','..','..','chunks','ethercat_icam_v7_chunk'+str(chunk_n)+'_events.csv')

#print(file)                                                                                                                                

df = pd.read_csv(file)

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

#percentiles=np.linspace(1, 99, 1)

Zpercentiles=stats.scoreatpercentile(new_df_Z['spread1'], percentiles)





plt.figure("QQ"+str(test)+"vs"+str(vs))
plt.title('QQ for Chunk '+str(test)+' vs Chunk '+str(vs))
#plt.legend(loc='upper right')
#plt.xlabel('CUMSUM for each bin for Chunk'+str(test))
#plt.ylabel('CUMSUM for each bin for other Chunks')
plt.plot(testZpercentiles, Zpercentiles, 'bo', label='moving in Z')
plt.plot(testZpercentiles, testZpercentiles, 'k')
#plt.plot(nYtest, totY, 'r+', label='moving in Y')
#plt.plot(nXtest, totX, 'k*', label='moving in X')
plt.show()
