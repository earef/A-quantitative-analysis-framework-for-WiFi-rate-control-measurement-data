import pandas as pd
import numpy as np
import argparse

pd.options.mode.use_inf_as_na = True
pd.set_option('display.max_rows', None, 'display.max_columns', None)

parser = argparse.ArgumentParser(description="Cleaning script")
parser.add_argument("--label", type=str, help="Label")
parser.add_argument("--start_index", type=int, help="Start index")
parser.add_argument("--end_index", type=int, help="End index")
args = parser.parse_args()

label = args.label
start_index = args.start_index
end_index = args.end_index

TXS_Columns = ["radio","timestamp",
    "txs","macaddr","num_frames",
    "num_acked","probe","rate0",
    "count0","rate1","count1",
    "rate2","count2","rate3",
    "count3"]
read_data = pd.read_csv ("dataset/22.csv",low_memory=False,sep=";",names=TXS_Columns)
# to_drop = ['P','Q','R','S']
