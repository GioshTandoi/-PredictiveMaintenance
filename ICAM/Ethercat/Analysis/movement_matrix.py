import pandas as pd
import numpy as np

chunks_directory = r'..\Data\chunks\ethercat_icam_v7_chunk'
frames = []
columns = ['is_moving_Z', 'is_moving_Y', 'is_moving_X']

for i in range(2, 9):
    df = pd.read_csv(chunks_directory+str(i+1)+'_events.csv')
    df.sort_values(by=['timestamp_'], inplace=True)

    ZFrequencyMonitor = np.array(df['zfrequencymonitor'].values).reshape(len(df['zfrequencymonitor'].values), 1)
    YVelocityFeedbackValue = np.array(df['yvelocityfeedbackvalue'].values).reshape(
        len(df['yvelocityfeedbackvalue'].values), 1)
    XVelocityFeedbackValue = np.array(df['xvelocityfeedbackvalue'].values).reshape(
        len(df['xvelocityfeedbackvalue'].values), 1)
    timestamps = np.array(df['timestamp_'].values).reshape(len(df['timestamp_'].values), 1)
    dates = np.array(df['date'].values).reshape(len(df['date'].values), 1)
    new_df = pd.DataFrame(
        data=np.concatenate((timestamps, dates, ZFrequencyMonitor, YVelocityFeedbackValue, XVelocityFeedbackValue),
                            axis=1),
        columns=['timestamp_', 'date', 'zfrequencymonitor', 'yvelocityfeedbackvalue', 'xvelocityfeedbackvalue'])
    frames.append(new_df)

z_y_x = pd.concat(frames)

timestamps = z_y_x['timestamp_'].values
dates = z_y_x['date'].values

is_moving_Z = z_y_x['zfrequencymonitor'] != 0
z = z_y_x['zfrequencymonitor'].where(is_moving_Z, 0)
not_moving_Z = z == 0
z.where(not_moving_Z, 1, inplace=True)

is_moving_Y = z_y_x['yvelocityfeedbackvalue'] != 0
y = z_y_x['yvelocityfeedbackvalue'].where(is_moving_Y, 0)
not_moving_Y = y == 0
y.where(not_moving_Y, 1, inplace=True)

is_moving_X = z_y_x['xvelocityfeedbackvalue'] != 0
x = z_y_x['xvelocityfeedbackvalue'].where(is_moving_X, 0)
not_moving_X = x == 0
x.where(not_moving_X, 1, inplace=True)

z_y_x = pd.concat([z, y, x], axis=1)
z_y_x.rename(columns={"zfrequencymonitor": "is_moving_Z", "yvelocityfeedbackvalue": "is_moving_Y",
                              "xvelocityfeedbackvalue":"is_moving_X"}, inplace=True)
z_y_x.astype('int64', inplace=True)
z_y_x['timestamp_'] = timestamps
z_y_x['date'] = dates
z_y_x.to_csv('movement_model.csv', index=False)
