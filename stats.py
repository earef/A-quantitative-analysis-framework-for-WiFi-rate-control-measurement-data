import pandas as pd
import numpy as np
from process import time_index
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import matplotlib as mpl


pd.options.mode.use_inf_as_na = True
# *;0;#stats;macaddr;rate;avg_prob;avg_tp;cur_success;cur_attempts;hist_success;hist_attempts
STATS_Columns = ["radio","timestamp",
    "stats","macaddr","rate",
    "avg_prob","avg_tp","cur_success",
    "cur_attempts","hist_success","hist_attempts",
    "L","M","N",
    "O",'P','Q','R','S']
read_data_stats = pd.read_csv ("dataset/24.csv",low_memory=False,sep=";",names=STATS_Columns)
to_drop_stats = ["L","M","N",
"O",'P','Q','R','S']


# read_data_stats=read_data_stats.head(3000)
# best_rates=best_rates.head(3000)

#set2
# read_data_stats=read_data_stats.head(600000)
# read_data_stats = read_data_stats.iloc[540000:,:]
# best_rates=best_rates.head(600000)
# best_rates = best_rates.iloc[540000:,:]
# set2+extention1
# read_data_stats=read_data_stats.head(600000)
# read_data_stats = read_data_stats.iloc[500000:,:]
# set2+extention2
# read_data_stats=read_data_stats.head(600000)
# # set2+extention3
# read_data_stats=read_data_stats.head(900000)
# # set2+extention4
# read_data_stats=read_data_stats.head(2000000)
# # # set2+extention5
# read_data_stats=read_data_stats.head(3000000)
# # # set2+extention6
# read_data_stats=read_data_stats.head(5000000)
# # # set2+extention7
# read_data_stats=read_data_stats.head(7000000)
# # # set2+extention8
# read_data_stats=read_data_stats.head(9000000)
# read_data_stats=read_data_stats.head(20000)
# read_data_stats=read_data_stats.head(6000)
read_data_stats=read_data_stats.head(1000000)
read_data_stats = read_data_stats.iloc[700000:,:]

#distorted data filter
read_data_stats=read_data_stats.drop(to_drop_stats, axis=1)
read_data_stats=read_data_stats[read_data_stats['stats'].str.contains('stats').fillna(False)]
read_data_stats=read_data_stats[read_data_stats['macaddr'].str.contains('bc:a8:a6:9c:6f:53').fillna(False)]
# print(read_data_stats.first_valid_index())
# print(read_data_stats.last_valid_index())

#conversion
read_data_stats["avg_tp"]=read_data_stats["avg_tp"].astype(str).apply(lambda x: int(x, 16))
read_data_stats["avg_tp"]=read_data_stats["avg_tp"].astype('float')
print(read_data_stats)
#division
read_data_stats["avg_tp"]=read_data_stats["avg_tp"]/10
# print(read_data_stats.shape[0])
# print(read_data_stats.dtypes)
# read_data_stats.to_csv("dataset/statsdiv.csv")
read_data_stats=time_index(read_data_stats)


dict= {'0': "0-BPSK.1/2.20MHz.LG.1Nss" ,'1': "1-QPSK.1/2.20MHz.LG.1Nss","2":"2-QPSK.3/4.20MHz.LG.1Nss" ,"3":"3-16.QAM.1/2.20MHz.LG.1Nss" ,"4":"4-16.QAM.3/4.20MHz.LG.1Nss" ,"5":"5-64.QAM.2/3.20MHz.LG.1Nss" ,"6":"6-64.QAM.3/4.20MHz.LG.1Nss","7":"7-64.QAM.5/6.20MHz.LG.1Nss",
    "10" : "10-BPSK.1/2.20MHz.LG.2Nss" ,"11": "11-QPSK.1/2.20MHz.LG.2Nss","12":"12-QPSK.3/4.20MHz.LG.2Nss" ,"13":"13-16.QAM.1/2.20MHz.LG.2Nss" ,"14":"14-16.QAM.3/4.20MHz.LG.2Nss" ,"15":"15-64.QAM.2/3.20MHz.LG.2Nss" ,"16":"16-64.QAM.3/4.20MHz.LG.2Nss","17":"17-64.QAM.5/6.20MHz.LG.2Nss",
    "80" : "80-BPSK.1/2.40MHz.LG.1Nss" ,"81": "81-QPSK.1/2.40MHz.LG.1Nss","82":"82-QPSK.3/4.40MHz.LG.1Nss" ,"83":"83-16.QAM.1/2.40MHz.LG.1Nss" ,"84":"84-16.QAM.3/4.40MHz.LG.1Nss" ,"85":"85-64.QAM.2/3.40MHz.LG.1Nss" ,"86":"86-64.QAM.3/4.40MHz.LG.1Nss","87":"87-64.QAM.5/6.40MHz.LG.1Nss",
    "90" : "90-BPSK.1/2.40MHz.LG.2Nss" ,"91": "91-QPSK.1/2.40MHz.LG.2Nss","92":"92-QPSK.3/4.40MHz.LG.2Nss" ,"93":"93-16.QAM.1/2.40MHz.LG.2Nss" ,"94":"94-16.QAM.3/4.40MHz.LG.2Nss" ,"95":"95-64.QAM.2/3.40MHz.LG.2Nss" ,"96":"96-64.QAM.3/4.40MHz.LG.2Nss","97":"97-64.QAM.5/6.40MHz.LG.2Nss",
    "c0" : "c0-BPSK.1/2.40MHz.SG.1Nss" ,"c1": "c1-QPSK.1/2.40MHz.SG.1Nss","c2":"c2-QPSK.3/4.40MHz.SG.1Nss" ,"c3":"c3-16.QAM.1/2.40MHz.SG.1Nss" ,"c4":"c4-16.QAM.3/4.40MHz.SG.1Nss" ,"c5":"c5-64.QAM.2/3.40MHz.SG.1Nss" ,"c6":"c6-64.QAM.3/4.40MHz.SG.1Nss","c7":"c7-64.QAM.5/6.40MHz.SG.1Nss",
    "d0" : "d0-BPSK.1/2.40MHz.SG.2Nss" ,"d1": "d1-QPSK.1/2.40MHz.SG.2Nss","d2":"d2-QPSK.3/4.40MHz.SG.2Nss" ,"d3":"d3-16.QAM.1/2.40MHz.SG.2Nss" ,"d4":"d4-16.QAM.3/4.40MHz.SG.2Nss" ,"d5":"d5-64.QAM.2/3.40MHz.SG.2Nss" ,"d6":"d6-64.QAM.3/4.40MHz.SG.2Nss","d7":"d7-64.QAM.5/6.40MHz.SG.2Nss"
        }


read_data_stats=read_data_stats.replace({"rate": dict})


ytick =['0-BPSK.1/2.20MHz.LG.1Nss' ,'1-QPSK.1/2.20MHz.LG.1Nss','2-QPSK.3/4.20MHz.LG.1Nss' ,'3-16.QAM.1/2.20MHz.LG.1Nss' ,'4-16.QAM.3/4.20MHz.LG.1Nss' ,'5-64.QAM.2/3.20MHz.LG.1Nss' ,'6-64.QAM.3/4.20MHz.LG.1Nss','7-64.QAM.5/6.20MHz.LG.1Nss',
    '10-BPSK.1/2.20MHz.LG.2Nss' ,'11-QPSK.1/2.20MHz.LG.2Nss','12-QPSK.3/4.20MHz.LG.2Nss' ,'13-16.QAM.1/2.20MHz.LG.2Nss' ,'14-16.QAM.3/4.20MHz.LG.2Nss' ,'15-64.QAM.2/3.20MHz.LG.2Nss' ,'16-64.QAM.3/4.20MHz.LG.2Nss','17-64.QAM.5/6.20MHz.LG.2Nss',
    '80-BPSK.1/2.40MHz.LG.1Nss' ,'81-QPSK.1/2.40MHz.LG.1Nss','82-QPSK.3/4.40MHz.LG.1Nss' ,'83-16.QAM.1/2.40MHz.LG.1Nss' ,'84-16.QAM.3/4.40MHz.LG.1Nss' ,'85-64.QAM.2/3.40MHz.LG.1Nss' ,'86-64.QAM.3/4.40MHz.LG.1Nss','87-64.QAM.5/6.40MHz.LG.1Nss',
    '90-BPSK.1/2.40MHz.LG.2Nss' ,'91-QPSK.1/2.40MHz.LG.2Nss','92-QPSK.3/4.40MHz.LG.2Nss' ,'93-16.QAM.1/2.40MHz.LG.2Nss' ,'94-16.QAM.3/4.40MHz.LG.2Nss' ,'95-64.QAM.2/3.40MHz.LG.2Nss' ,'96-64.QAM.3/4.40MHz.LG.2Nss','97-64.QAM.5/6.40MHz.LG.2Nss',
    'c0-BPSK.1/2.40MHz.SG.1Nss' ,'c1-QPSK.1/2.40MHz.SG.1Nss','c2-QPSK.3/4.40MHz.SG.1Nss' ,'c3-16.QAM.1/2.40MHz.SG.1Nss' ,'c4-16.QAM.3/4.40MHz.SG.1Nss' ,'c5-64.QAM.2/3.40MHz.SG.1Nss' ,'c6-64.QAM.3/4.40MHz.SG.1Nss','c7-64.QAM.5/6.40MHz.SG.1Nss',
    'd0-BPSK.1/2.40MHz.SG.2Nss' ,'d1-QPSK.1/2.40MHz.SG.2Nss','d2-QPSK.3/4.40MHz.SG.2Nss' ,'d3-16.QAM.1/2.40MHz.SG.2Nss' ,'d4-16.QAM.3/4.40MHz.SG.2Nss' ,'d5-64.QAM.2/3.40MHz.SG.2Nss' ,'d6-64.QAM.3/4.40MHz.SG.2Nss','d7-64.QAM.5/6.40MHz.SG.2Nss'
            ]
# first_index = read_data_stats['timestamp'].iat[0]


fig = plt.figure(figsize=(35,15))
ax=plt.gca()

# ax = fig.add_subplot(111)


xfmt = md.DateFormatter("%Y-%m-%d %H:%M:%S.%f")
ax.xaxis.set_major_formatter(xfmt)
ax.xaxis.set_major_locator(MaxNLocator(integer=True))

dummy,=plt.plot([read_data_stats['timestamp'].iat[0]]*len(ytick),ytick)
dummy.remove()
# ax.scatter(best_rates["timestamp"],best_rates["maxtp0"],s=10,marker="|", color='black')
plt.scatter(read_data_stats["timestamp"],read_data_stats["rate"], c=read_data_stats["avg_tp"],s=4,marker="s",cmap='PuRd')

plt.title("Average throughput map")
plt.xlabel("Time",fontsize=9)
plt.ylabel("MCSIndex",fontsize=9)
plt.xticks(fontsize=8, rotation=35,ha="right" )
plt.yticks(fontsize=10)
# plt.colorbar(mpl.cm.ScalarMappable(cmap='PuRd'))
plt.colorbar()
plt.savefig(f"plot/Bestplots/Average-tp-bc:a8:a6:9c:6f:53.png",format='png',dpi=500, bbox_inches='tight')
plt.clf()
# plt.show()
