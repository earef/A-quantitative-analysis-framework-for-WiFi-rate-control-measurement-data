import pandas as pd
import numpy as np
from datetime import datetime
import re
import itertools
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import pylab as pl
import seaborn as sns
import matplotlib.dates as mdates
pd.options.mode.use_inf_as_na = True
pd.set_option('display.max_rows', None, 'display.max_columns', None)


RXS_Columns = ['*','timestamp','rxs','macaddr',
'last_signal','signal0','signal1','signal2','signal3',
'a','b','c','d','e','f','g','h','i','j']
Data_set = pd.read_csv("dataset/22.csv",low_memory=False,sep=";" ,names = RXS_Columns)
to_drop = ['a','b','c','d','e','f','g','h','i','j']

#distorted data filter
Data_set=Data_set.drop(to_drop, axis=1)
Data_set=Data_set.loc[Data_set['timestamp'].str.len() == 16]
Data_set=Data_set[Data_set['rxs'].str.contains('rxs').fillna(False)]
Data_set = Data_set[Data_set["last_signal"].str.contains("stats") == False]
Data_set=Data_set[Data_set['macaddr'].str.contains('0c:19:f8:a0:08:b3').fillna(False)]



# Data_set.to_csv("check.csv")
def twos_complement(hexstr, bits):
	val = int(hexstr, 16)
	return val - (1 << bits) if val & (1 << (bits-1)) else val
parse_s32 = lambda x: twos_complement(x, 32)
Data_set["RSSI"] = Data_set["last_signal"].apply(parse_s32)

def time_index(t):
    t = t.reset_index(drop=True)
    t["timestamp"] = t["timestamp"].fillna(0)
    t["timestamp"] = t["timestamp"].apply(lambda x: int(x, 16))
    t['timestamp'] = pd.to_datetime([x for x in t['timestamp'].squeeze().tolist()],format="%Y-%m-%d %H:%M:%S.%f")
    datetime_series = pd.to_datetime(t['timestamp'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    t=t.set_index(datetime_index)
    return(t)


ttime = time_index(Data_set)
ttime.index = pd.DatetimeIndex(ttime["timestamp"])
# ttime.to_csv("a.csv")
ttime = ttime.iloc[165210:166201]
groups = ttime.groupby('macaddr')

for macaddress, ttime_group in groups:
    fig, ax = plt.subplots(figsize=(40, 15))
    ttime_group.plot.scatter(x='timestamp', y='RSSI', marker='o', label=macaddress, ax=ax)
    ax.set_ylim(-100, 0)
    ax.set_title(f'Signal Strength of Device {macaddress} in a Network', fontsize=16)
    ax.legend(loc='upper right', shadow=True, fontsize=12)
    ax.set_xlabel('Time (Day-Hour:Minute:Second)', fontsize=14)
    ax.set_ylabel('RSSI (dBm)', fontsize=14)
    ax.set_prop_cycle(color=['#4C72B0', '#55A868', '#C44E52', '#8172B2', '#CCB974', '#64B5CD'], linestyle=['-', '--', ':', '-.', '-', '--'])
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(f'plot/April/RSSI/G2-RSSI-{macaddress}.png', dpi=300)
    plt.close(fig)
