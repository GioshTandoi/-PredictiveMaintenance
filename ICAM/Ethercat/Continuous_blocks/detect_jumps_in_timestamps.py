import pandas as pd
import matplotlib.pyplot as plt

all_timestamps = pd.read_csv('all_timestamps.csv')
differences = all_timestamps['timestamps'].diff()
differences = differences.pop(0)
all_timestamps['differences'] = differences
print(all_timestamps)

plt.figure(0)
nZ, binsZ, patchesZ = plt.hist(differences, bins='auto', alpha=0.5, label='time_jumps')
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Time_Jumps')
plt.ylabel('Frequency')
plt.title('Time_Jumps Distribution')
plt.legend(loc='upper right')
plt.show()