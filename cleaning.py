#Version: 1.3.5 pandas


import pandas as pd
import numpy as np
import argparse

pd.options.mode.use_inf_as_na = True
pd.set_option('display.max_rows', None, 'display.max_columns', None)


parser = argparse.ArgumentParser(description="Run all scripts")
parser.add_argument("--dataset", type=str, help="Path of the trace file")
parser.add_argument("--label", type=str, help="Label")
parser.add_argument("--start_index", type=int, help="Start index")
parser.add_argument("--end_index", type=int, help="End index")
args = parser.parse_args()

dataset = args.dataset
label = args.label
start_index = args.start_index
end_index = args.end_index


TXS_Columns = ["radio","timestamp",
    "txs","macaddr","num_frames",
    "num_acked","probe","rate0",
    "count0","rate1","count1",
    "rate2","count2","rate3",
    "count3"]
clean_data = pd.read_csv(dataset,low_memory=False,sep=";",names=TXS_Columns ,usecols=TXS_Columns)

#distorted data filter
# clean_data=read_data.drop(to_drop, axis=1)
clean_data=clean_data.loc[clean_data['timestamp'].str.len() == 16]
clean_data=clean_data.loc[clean_data['num_frames'].str.len() > 0]
clean_data=clean_data.loc[clean_data['num_acked'].str.len() < 4]
clean_data=clean_data.loc[clean_data['count0'].str.len() == 1]
clean_data=clean_data.loc[clean_data['count1'].str.len() == 1]
clean_data=clean_data.loc[clean_data['count2'].str.len() == 1]
clean_data=clean_data.loc[clean_data['count3'].str.len() == 1]
# sta_data=clean_data[clean_data['txs'].str.contains('sta').fillna(False)]
clean_data=clean_data[clean_data['txs'].str.contains('txs').fillna(False)]
# clean_data=clean_data[clean_data['probe'].str.contains('1').fillna(False)]
# clean_data=clean_data[clean_data['macaddr'].str.contains('b0:f1:d8:50:92:c1').fillna(False)]



########validity test
#
# d = {"radio":["phy0","phy0","phy0","phy0","phy0","phy0","phy0","phy0","phy0","phy0","phy0","phy0","phy0","phy0","phy0","phy0"],
#  "timestamp" :["16e310ed9c8d929c","16e310eda5c470b6","16e310edce43a2f9","16e310edfbf85cf8","16e310edfe9e5f9d",
#  "16e310ee092dee36","16e310ee093dee36","16e310ee094dee36","16e310ee095dee36"
# ,"16e310ee096dee36","16e310ee097dee36","16e310ee098dee36","16e310ee099dee36","16e310ee09adee36","16e310ee09bdee36","16e310ee09cdee36"],
#  "txs":["txs","txs","txs","txs","txs","txs","txs","txs","txs","txs","txs","txs","txs","txs","txs","txs"],
#  "macaddr":["b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3","b6:78:26:b9:7c:d3"],
#  "num_frames":["1c","1a","18","4","500","1d","1c","1a","18","4","500","1d","1c","1a","18","4"],
#  "num_acked" :["3","1a","12","4","500","13","3","1a","12","4","500","13","3","1a","12","4"],
#  "probe" :["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],
#  "rate0" :["d7","8","1a8","259","1e2","e5","d7","8","1a8","259","1e2","e5","d7","8","1a8","259"],
#  "count0" :["3","1","2","2","2","2","3","1","2","2","2","2","3","1","2","2"],
#   "rate1" :["e1","ffff","256","c1","259","c1","e1","ffff","256","c1","259","c1","e1","ffff","256","c1"],
#    "count1" :["2","0","4","2","3","1","2","0","4","2","3","1","2","0","4","2"],
#    "rate2" :["e1","ffff","256","ffff","291","ffff","e1","ffff","256","ffff","291","ffff","e1","ffff","256","e5"],
#     "count2" :["2","0","2","0","1","0","2","0","2","0","1","0","2","0","2","1"],
#     "rate3" :["c1","ffff","7","ffff","ffff","ffff","c1","ffff","7","ffff","ffff","ffff","c1","ffff","7","ffff"],
#      "count3" :["2","0","1","0","0","0","2","0","1","0","0","0","2","0","1","0"],
#      }
# clean_data = pd.DataFrame(data=d)

#######test

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



clean_data = clean_data.iloc[start_index:end_index]
index_range_str = f"{start_index}-{end_index}"
label_str=f"{label}"

print(clean_data.shape[0])

# Define label_str and index_range_str
label_str = f"{label}" if label else ""
index_range_str = f"{start_index}-{end_index}" if start_index is not None and end_index is not None else ""

# Print label_str and index_range_str for use in other scripts
print("Dataset path:", dataset)
print("label_str:", label_str)
print("index_range_str:", index_range_str)
