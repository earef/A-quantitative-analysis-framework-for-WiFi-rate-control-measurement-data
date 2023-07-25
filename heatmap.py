
import pandas as pd
import glob
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


from process import success,time_conv

from cleaning import to_int,dataset,index_range_str,label_str
pd.options.mode.use_inf_as_na = True


t_first=time_conv['timestamp'].iloc[0]
t_last=time_conv['timestamp'].iloc[-1]

for mac,macdata in time_conv.groupby(["macaddr"],sort=False):
    fig, ax = plt.subplots(figsize=(40, 15))

    FullSuccess=success(macdata)
    FullSuccess["group"]  = FullSuccess.group.apply(to_int)
    FullSuccess["offset"] = FullSuccess.offset.apply(to_int)
    FullSuccess = FullSuccess.replace("", 0)

    x_ticks = [i for i in range(10)]
    y_ticks = [i for i in range(0, 0x2a)]

    x_labels = ["BPSK,1/2","QPSK,1/2","QPSK,3/4","16-QAM,1/2","16-QAM,3/4","64-QAM,2/3","64-QAM,3/4","64-QAM,5/6","256-QAM,3/4","256-QAM5/6"]
    y_labels = ["0-HT-20MHz.Long-GI.1 Nss","1-HT-20MHz.Long-GI.2 Nss","NA","NA",
                "NA","NA","NA","NA",
                "8-HT-40MHz.Long-GI.1 Nss","9-HT-40MHz.Long-GI.2 Nss","NA","NA",
                "c-HT-40MHz.Short-GI.1 Nss","d-HT-40MHz.Short-GI.2 Nss","NA","NA","10-CCK-20MHz.Long-GI.1 Nss","10-OFDM-20MHz.Long-GI.1 Nss",
                "NA","NA","NA","NA",
                "NA","NA","NA","NA",
                "NA","NA","NA","NA",
                "NA","NA","NA","NA",
                "NA","NA","NA","NA",
                "NA","NA","NA","NA"]

    HeatMap = pd.pivot_table(FullSuccess, index='group', columns='offset' , values='FullSuccess_count')
    HeatMap.fillna(0, inplace=True)
    HeatMap_data = np.zeros((42,10))

    for idx,row in HeatMap.iterrows():
            for offs in row.index:
                HeatMap_data[idx][offs] = row[offs]
    plt.figure(figsize=(17, 15))
    ax = sns.heatmap(HeatMap_data,cmap="PuRd" , norm=LogNorm(),annot_kws={"size":3},square=True,linestyle="dotted", linewidths=.08,linecolor="thistle")
    ax.set_ylabel("Bandwith-GuardInterval-Number of Spatial Stream", fontsize=12)
    ax.set_xlabel("Modulation - Coding", fontsize=12)
    caption = "\n".join([
        f"MAC Address:  {mac}",
        "",
        f"Start Time:   {t_first.strftime('%Y-%m-%d %H:%M:%S')}",
        f"End Time:     {t_last.strftime('%Y-%m-%d %H:%M:%S')}",
        ""
    ])

    ax.set_yticks(np.arange(len(y_labels)) + 0.5)  # Shift y-ticks by 0.5 to align with center of squares
    ax.set_yticklabels(y_labels, rotation=0, ha='right', va='center')  # Use ha='right' to align labels to the right
    # ax.tick_params(axis='y', which='both', length=0)  # Remove tick lines
    ax.set_xticks(np.arange(len(x_labels)) + 0.5)  # Shift x-ticks by 0.5 to align with center of squares
    ax.set_xticklabels(x_labels, rotation=-30, ha='left', va='top')  # Use ha='center' to align labels to the center
    # ax.tick_params(axis='x', which='both', length=0)  # Remove tick lines

    plt.gcf().text(0.2, 0.82, caption, fontsize=12)
    plt.savefig(f"plot/{label_str}-heatmap-{mac}-22-{index_range_str}.png" ,dpi=300)
    plt.close(fig)

    # plt.show()
