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

pd.set_option('display.max_rows', 200, 'display.max_columns', 30)
from process import success,success_timestamp,cal_failure,attempt,time_index
from cleaning import read_data,to_int,clean_data


time_rolling=time_index(clean_data)

print(time_rolling.first_valid_index())
print(time_rolling.last_valid_index())
time_rolling.index = pd.DatetimeIndex(time_rolling["timestamp"])
time_rolling=time_rolling.sort_index()
conditions = [time_rolling['macaddr'] == "bc:a8:a6:9c:6f:53",
            time_rolling['macaddr'] == "0c:19:f8:a0:08:b3",
            time_rolling['macaddr'] == "b0:f1:d8:50:92:c1",
            time_rolling['macaddr'] == "9c:b6:d0:89:32:89",
            time_rolling['macaddr'] == "b2:02:4d:19:ea:92",
            time_rolling['macaddr'] == "32:3b:67:22:c4:16",
            time_rolling['macaddr'] == "8c:85:90:a6:71:e4",
            time_rolling['macaddr'] == "a6:35:6c:31:2a:5c",
            time_rolling['macaddr'] == "46:a7:f6:29:55:10",
            time_rolling['macaddr'] == "78:7b:8a:59:55:02",
            time_rolling['macaddr'] == "80:2b:f9:1d:0b:4d",
            time_rolling['macaddr'] == "72:63:85:2b:6c:cf",
            time_rolling['macaddr'] == "8a:56:b1:91:2e:73",
            time_rolling['macaddr'] == "88:b1:11:ea:ab:96"
            ]
values = [48,48,48,48,48,48,48,24,48,48,48,24,48,48]
time_rolling["capability"] = np.select(conditions,values)

fig = plt.figure()
#"1T","10s","500ms",
for t1 in (["50ms","10ms","5ms","1ms"]):
    Agg=[]
    for mac,macdata in time_rolling.groupby(["macaddr"],sort=False):
        fig, axs = plt.subplots(2)
        Time= []
        Miu=[]
        Tetha=[]

        for time_rolling_subset in macdata.rolling(t1):
            # Calculating overlap/attemp and drop in in the miu
            last_index = time_rolling_subset['timestamp'].iat[-1]
            first_index = time_rolling_subset['timestamp'].iat[0]
            last_index=last_index.to_pydatetime()
            Time.append(last_index)
            # print(time_rolling_subset, last_index,first_index,delta)
            rolling_success=success(time_rolling_subset)
            rolling_attempt=attempt(time_rolling_subset)
            rolling_fail=cal_failure(rolling_attempt,rolling_success)
            overlap = pd.concat([rolling_success,rolling_fail],axis=1)
            overlap = overlap[['FullSuccess_count','successful_rates',"failed_counts","rates"]]
            overlap.columns = ["fullsuccess_count","fullsuccess_rate","failed_count","failed_rate"]
            overlap["overlap"]=overlap['fullsuccess_rate'].isin(overlap['failed_rate'])
            overlap = overlap[['overlap','fullsuccess_rate']]
            overlap.columns = ['overlap','rate']
            overlap=overlap.dropna()
            overlap_mu= overlap.loc[overlap['overlap'] == True, 'rate']
            attempt_mu = rolling_attempt[["attempt_rates"]]
            attempt_mu.columns = ['rate']
            attempt_mu=len(attempt_mu)
            overlap_mu=len(overlap_mu)
            mu=overlap_mu/attempt_mu
            Miu.append(mu)
            # Calculation capability/attempt
            attempt_tetha = rolling_attempt[["attempt_rates"]]
            attempt_tetha.columns = ['rate']
            attempt_tetha=len(attempt_tetha)
            capability_tetha = time_rolling["capability"]
            tetha=attempt_tetha/capability_tetha
            Tetha.append(tetha)
    #     summation= sum(Miu)
    #     lenght=len(macdata)
    #     aggregate = summation/lenght
    #     Agg.append(aggregate)
    # plt.plot(t1,Agg,marker=".",color='C4', markersize=10)
    # plt.yticks(size=10,rotation=45)
    # plt.ylim([0, 1])
    # plt.savefig(f"plot/Disjoint/Dis-{mac}-set3.png",format='png',dpi=300 ,bbox_inches='tight')

        axs[0].plot(Time,Tetha,"o",markersize=1.2,alpha=1)
        axs[1].plot(Time,Miu,"o",markersize=1.2,alpha=1)
        axs[1].set_xlabel("Time",fontsize=9)
        axs[0].set_ylabel("Attempt/capability",fontsize=9)
        axs[1].set_ylabel("Overlap/Attempt",fontsize=9)
        axs[0].set_ylim(0, 1)
        axs[1].set_ylim(0, 1)
        fig.suptitle(f"device: {mac}")
        plt.savefig(f"plot/Bestplots/overlap-{mac}-Rolling on{t1}-set1.png",format='png',dpi=200 ,bbox_inches='tight')
        plt.clf()
