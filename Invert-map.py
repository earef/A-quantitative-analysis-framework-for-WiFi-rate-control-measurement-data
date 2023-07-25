import pandas as pd
import numpy as np
import seaborn as sns
pd.set_option('display.max_rows', None, 'display.max_columns', None)


import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

from process import success,time_conv,attempt
from cleaning import to_int,dataset,index_range_str,label_str
pd.options.mode.use_inf_as_na = True


for mac,macdata in time_conv.groupby(["macaddr"],sort=False):
    fig, ax = plt.subplots(figsize=(40, 15))


    rate_table = pd.read_csv ("dict_airtime.csv",low_memory=False,sep=",")
    rate_table = rate_table[['full group']]
    attempt_check=attempt(macdata)
    print(attempt_check)
    attempt_series = attempt_check['attempt_rates'].squeeze()
    rate_table["placement"] = rate_table["full group"].isin(attempt_series)
    invert = rate_table.loc[rate_table["placement"] == False, 'full group']
    invert = pd.DataFrame(invert)
    invert.columns = ["invert_rates"]
    invert["group"] = invert['invert_rates'].astype(str).str.slice(stop=-1)
    invert["offset"]= invert['invert_rates'].astype(str).str.slice(start=-1)
    invert["group"]  = invert.group.apply(to_int)
    invert["offset"] = invert.offset.apply(to_int)
    invert = invert.replace("", 0)
    invert['static'] = 1
    #
    x_ticks = [i for i in range(10)]
    y_ticks = [i for i in range(0, 0x2a)]
    #
    x_labels = ["BPSK,1/2","QPSK,1/2","QPSK,3/4","16-QAM,1/2","16-QAM,3/4","64-QAM,2/3","64-QAM,3/4","64-QAM,5/6","256-QAM,3/4","256-QAM5/6"]
    y_labels = ["HT-20MHz,LG,1 Nss","HT-20MHz,LG,2 Nss","HT-20MHz,LG,3 Nss","HT-20MHz,LG,4 Nss",
                "HT-20MHz,SG,1 Nss","HT-20MHz,SG,2 Nss","HT-20MHz,SG,3 Nss","HT-20MHz,SG,4 Nss",
                "HT-40MHz,LG,1 Nss","HT-40MHz,LG,2 Nss","HT-40MHz,LG,3 Nss","HT-40MHz,LG,4 Nss",
                "HT-40MHz,SG,1 Nss","HT-40MHz,SG,2 Nss","HT-40MHz,SG,3 Nss","HT-40MHz,SG,4 Nss",
                "CCK-20MHz,LG,1 Nss","OFDM-20MHz,LG,1 Nss",
                "VHT-20MHz,LG,1 Nss","VHT-20MHz,LG,2 Nss","VHT-20MHz,LG,3 Nss","VHT-20MHz,LG,4 Nss",
                "VHT-20MHz,SG,1 Nss","VHT-20MHz,SG,2 Nss","VHT-20MHz,SG,3 Nss","VHT-20MHz,SG,4 Nss",
                "VHT-40MHz,LG,1 Nss","VHT-40MHz,LG,2 Nss","VHT-40MHz,LG,3 Nss","VHT-40MHz,LG,4 Nss",
                "VHT-40MHz,SG,1 Nss","VHT-40MHz,SG,2 Nss","VHT-40MHz,SG,3 Nss","VHT-40MHz,SG,4 Nss",
                "VHT-80MHz,LG,1 Nss","VHT-80MHz,LG,2 Nss","VHT-80MHz,LG,3 Nss","VHT-80MHz,LG,4 Nss",
                "VHT-80MHz,SG,1 Nss","VHT-80MHz,SG,2 Nss","VHT-80MHz,SG,3 Nss","VHT-80MHz,SG,4 Nss"]


    InvertMap = pd.pivot_table(invert , index='group', columns='offset' , values= "static")
    InvertMap.fillna(0, inplace=True)
    InvertMap_data = np.zeros((42,10))
    #
    for idx,row in InvertMap.iterrows():
            for offs in row.index:
                InvertMap_data[idx][offs] = row[offs]
    plt.figure(figsize=(17, 15))
    ax = sns.heatmap(InvertMap_data,cmap="binary" ,vmin=0,vmax=1, annot_kws={"size":3},square=True, linewidths=.5)
    ax.set_ylabel("Bandwith-GuardInterval-Number of Spatial Stream", fontsize=10)
    ax.set_xlabel("Modulation - Coding", fontsize=10)
    ax.set_yticks(np.arange(len(y_labels)) + 0.5)  # Shift y-ticks by 0.5 to align with center of squares
    ax.set_yticklabels(y_labels, rotation=0, ha='right', va='center')  # Use ha='right' to align labels to the right
    # ax.tick_params(axis='y', which='both', length=0)  # Remove tick lines
    ax.set_xticks(np.arange(len(x_labels)) + 0.5)  # Shift x-ticks by 0.5 to align with center of squares
    ax.set_xticklabels(x_labels, rotation=-30, ha='left', va='top')  # Use ha='center' to align labels to the center
    # ax.tick_params(axis='x', which='both', length=0)  # Remove tick lines

    # ax.set_title("Success Rate heatmap")
    plt.savefig(f"plot/April/{label_str}-invertmap-{mac}-22-{index_range_str}.png" ,dpi=300)
