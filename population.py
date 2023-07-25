import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md
import seaborn as sns
import datetime
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

pd.options.mode.use_inf_as_na = True
# pd.set_option('display.max_rows', 10, 'display.max_columns', 2)
# pd.set_option('display.max_rows', None, 'display.max_columns', None)

TXS_Columns = ["radio","timestamp",
    "txs","macaddr","num_frames",
    "num_acked","probe","rate0",
    "count0","rate1","count1",
    "rate2","count2","rate3",
    "count3",'P','Q','R','S']
read_data = pd.read_csv ("dataset/22.csv",low_memory=False,sep=";",names=TXS_Columns)
to_drop = ['P','Q','R','S']

#distorted data filter
clean_data=read_data.drop(to_drop, axis=1)
clean_data=clean_data.loc[clean_data['timestamp'].str.len() == 16]
clean_data=clean_data.loc[clean_data['num_frames'].str.len() > 0]
clean_data=clean_data.loc[clean_data['num_acked'].str.len() < 4]
clean_data=clean_data.loc[clean_data['count0'].str.len() == 1]
clean_data=clean_data.loc[clean_data['count1'].str.len() == 1]
clean_data=clean_data.loc[clean_data['count2'].str.len() == 1]
clean_data=clean_data.loc[clean_data['count3'].str.len() == 1]
clean_data=clean_data[clean_data['txs'].str.contains('txs').fillna(False)]
# clean_data=clean_data[clean_data['macaddr'].str.contains("b0:f1:d8:50:92:c1").fillna(False)]


#conversion
def twos_complement(hexstr, bits):
	val = int(hexstr, 16)
	return val - (1 << bits) if val & (1 << (bits-1)) else val
clean_data["num_acked"]=clean_data["num_acked"].astype(str).apply(lambda x: int(x, 16))
clean_data["num_frames"]=clean_data["num_frames"].astype(str).apply(lambda x: int(x, 16))
clean_data["count0"]=clean_data["count0"].apply(lambda x: int(x, 16))
clean_data["count1"]=clean_data["count1"].apply(lambda x: int(x, 16))
clean_data["count2"]=clean_data["count2"].apply(lambda x: int(x, 16))
clean_data["count3"]=clean_data["count3"].apply(lambda x: int(x, 16))
clean_data["rate0"]=clean_data["rate0"].apply(lambda x: int(x, 16))
clean_data["rate1"]=clean_data["rate1"].apply(lambda x: int(x, 16))
clean_data["rate2"]=clean_data["rate2"].apply(lambda x: int(x, 16))
clean_data["rate3"]=clean_data["rate3"].apply(lambda x: int(x, 16))

def to_int(s):
    if len(s) == 0:
        return 0
    else:
        return int(s, 16)
#
start_index = 6300
end_index =1001812 
clean_data = clean_data.iloc[start_index:end_index]
index_range_str = f"{start_index}-{end_index}"


print(clean_data.shape[0])
def time_index(t):
    t = t.reset_index(drop=True)
    t["timestamp"] = t["timestamp"].fillna(0)
    t["timestamp"] = t["timestamp"].apply(lambda x: int(x, 16))
    t['timestamp'] = pd.to_datetime([x for x in t['timestamp'].squeeze().tolist()],format="%Y-%m-%d %H:%M:%S.%f")
    datetime_series = pd.to_datetime(t['timestamp'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    t=t.set_index(datetime_index)
    return(t)
time_rolling=time_index(clean_data)
print(time_rolling.first_valid_index())
print(time_rolling.last_valid_index())
time_rolling.index = pd.DatetimeIndex(time_rolling["timestamp"])
def pltcolor(lst):
    cols=[]
    for l in lst:
        if l=='phy0':
            cols.append('#ff7f0e')  # orange color
        elif l=='phy1':
            cols.append('#1f77b4')  # blue color
    return cols

sns.set_style('whitegrid')
sns.set_palette(['#ff7f0e', '#1f77b4'])  # set custom colors for the palette
cols = pltcolor(time_rolling['radio'])
fig, ax = plt.subplots(figsize=(15, 8))
ax.scatter(x='timestamp', y='macaddr', s=1.5, c=cols, data=time_rolling)
ax.xaxis.set_major_formatter(md.DateFormatter('%d-%H:%M:%S'))
plt.xticks(rotation=30, fontsize=12)
plt.yticks(fontsize=12)
ax.set_xlabel('Time (Day-Hour:Minute:Second)', fontsize=14)
ax.set_ylabel('Mac Address', fontsize=14)
ax.grid(True, alpha=0.5)

# add legend
handles = [plt.Line2D([], [], color='#ff7f0e', marker='o', linestyle=''),
           plt.Line2D([], [], color='#1f77b4', marker='o', linestyle='')]
labels = ['phy0', 'phy1']
plt.legend(handles, labels, loc='upper left', fontsize=12)

plt.tight_layout()

# add figure caption
fig.text(0.5, -0.07, 'Scatter plot of transmission (txs) of STA vs Time, color-coded by radio type (phy0 and phy1).',
         ha='center', fontsize=12)

plt.savefig(f"plot/April/G1-22.png", format='png', dpi=200, bbox_inches='tight')
