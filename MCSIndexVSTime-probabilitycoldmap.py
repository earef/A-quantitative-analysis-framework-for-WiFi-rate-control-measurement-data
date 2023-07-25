import pandas as pd
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
from itertools import cycle
import matplotlib.colors as colors


import seaborn as sns
from matplotlib.ticker import MaxNLocator
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize


pd.set_option('display.max_rows', None, 'display.max_columns', None)


from process import time_conv,success,attempt,cal_failure,time_index
from cleaning import to_int,index_range_str,label_str,clean_data

dict= {'0': "0-BPSK.1/2.20MHz.LG.1Nss" ,'1': "1-QPSK.1/2.20MHz.LG.1Nss","2":"2-QPSK.3/4.20MHz.LG.1Nss" ,"3":"3-16.QAM.1/2.20MHz.LG.1Nss" ,"4":"4-16.QAM.3/4.20MHz.LG.1Nss" ,"5":"5-64.QAM.2/3.20MHz.LG.1Nss" ,"6":"6-64.QAM.3/4.20MHz.LG.1Nss","7":"7-64.QAM.5/6.20MHz.LG.1Nss",
    "10" : "10-BPSK.1/2.20MHz.LG.2Nss" ,"11": "11-QPSK.1/2.20MHz.LG.2Nss","12":"12-QPSK.3/4.20MHz.LG.2Nss" ,"13":"13-16.QAM.1/2.20MHz.LG.2Nss" ,"14":"14-16.QAM.3/4.20MHz.LG.2Nss" ,"15":"15-64.QAM.2/3.20MHz.LG.2Nss" ,"16":"16-64.QAM.3/4.20MHz.LG.2Nss","17":"17-64.QAM.5/6.20MHz.LG.2Nss",
    "80" : "80-BPSK.1/2.40MHz.LG.1Nss" ,"81": "81-QPSK.1/2.40MHz.LG.1Nss","82":"82-QPSK.3/4.40MHz.LG.1Nss" ,"83":"83-16.QAM.1/2.40MHz.LG.1Nss" ,"84":"84-16.QAM.3/4.40MHz.LG.1Nss" ,"85":"85-64.QAM.2/3.40MHz.LG.1Nss" ,"86":"86-64.QAM.3/4.40MHz.LG.1Nss","87":"87-64.QAM.5/6.40MHz.LG.1Nss",
    "90" : "90-BPSK.1/2.40MHz.LG.2Nss" ,"91": "91-QPSK.1/2.40MHz.LG.2Nss","92":"92-QPSK.3/4.40MHz.LG.2Nss" ,"93":"93-16.QAM.1/2.40MHz.LG.2Nss" ,"94":"94-16.QAM.3/4.40MHz.LG.2Nss" ,"95":"95-64.QAM.2/3.40MHz.LG.2Nss" ,"96":"96-64.QAM.3/4.40MHz.LG.2Nss","97":"97-64.QAM.5/6.40MHz.LG.2Nss",
    "c0" : "c0-BPSK.1/2.40MHz.SG.1Nss" ,"c1": "c1-QPSK.1/2.40MHz.SG.1Nss","c2":"c2-QPSK.3/4.40MHz.SG.1Nss" ,"c3":"c3-16.QAM.1/2.40MHz.SG.1Nss" ,"c4":"c4-16.QAM.3/4.40MHz.SG.1Nss" ,"c5":"c5-64.QAM.2/3.40MHz.SG.1Nss" ,"c6":"c6-64.QAM.3/4.40MHz.SG.1Nss","c7":"c7-64.QAM.5/6.40MHz.SG.1Nss",
    "d0" : "d0-BPSK.1/2.40MHz.SG.2Nss" ,"d1": "d1-QPSK.1/2.40MHz.SG.2Nss","d2":"d2-QPSK.3/4.40MHz.SG.2Nss" ,"d3":"d3-16.QAM.1/2.40MHz.SG.2Nss" ,"d4":"d4-16.QAM.3/4.40MHz.SG.2Nss" ,"d5":"d5-64.QAM.2/3.40MHz.SG.2Nss" ,"d6":"d6-64.QAM.3/4.40MHz.SG.2Nss","d7":"d7-64.QAM.5/6.40MHz.SG.2Nss",
    "110" :"110-BPSK.1/2.20MHz.LG.1Nss"}
NSS= {'0': "1Nss" ,'1': "1Nss","2":"1Nss" ,"3":"1Nss" ,"4":"1Nss" ,"5":"1Nss" ,"6":"1Nss","7":"1Nss",
        "10" : "2Nss" ,"11": "2Nss","12":"2Nss" ,"13":"2Nss" ,"14":"2Nss" ,"15":"2Nss" ,"16":"2Nss","17":"2Nss",
        "80" : "1Nss" ,"81": "1Nss","82":"1Nss" ,"83":"1Nss" ,"84":"1Nss" ,"85":"1Nss" ,"86":"1Nss","87":"1Nss",
        "90" : "2Nss" ,"91": "2Nss","92":"2Nss" ,"93":"2Nss" ,"94":"2Nss" ,"95":"2Nss" ,"96":"2Nss","97":"2Nss",
        "c0" : "1Nss" ,"c1": "1Nss","c2":"1Nss" ,"c3":"1Nss" ,"c4":"1Nss" ,"c5":"1Nss" ,"c6":"1Nss","c7":"1Nss",
        "d0" : "2Nss" ,"d1": "2Nss","d2":"2Nss" ,"d3":"2Nss" ,"d4":"2Nss" ,"d5":"2Nss" ,"d6":"2Nss","d7":"2Nss"
        }

GI= {'0': "LG" ,'1': "LG","2":"LG" ,"3":"LG" ,"4":"LG" ,"5":"LG" ,"6":"LG","7":"LG",
        "10" : "LG" ,"11": "LG","12":"LG" ,"13":"LG" ,"14":"LG" ,"15":"LG" ,"16":"LG","17":"LG",
        "80" : "LG" ,"81": "LG","82":"LG" ,"83":"LG" ,"84":"LG" ,"85":"LG" ,"86":"LG","87":"LG",
        "90" : "LG" ,"91": "LG","92":"LG" ,"93":"LG" ,"94":"LG" ,"95":"LG" ,"96":"LG","97":"LG",
        "c0" : "SG" ,"c1": "SG","c2":"SG" ,"c3":"SG" ,"c4":"SG" ,"c5":"SG" ,"c6":"SG","c7":"SG",
        "d0" : "SG" ,"d1": "SG","d2":"SG" ,"d3":"SG" ,"d4":"SG" ,"d5":"SG" ,"d6":"SG","d7":"SG"
        }

ModulationCoding= {'0': "BPSK.1/2" ,'1': "QPSK.1/2","2":"QPSK.3/4" ,"3":"16.QAM.1/2" ,"4":"16.QAM.3/4" ,"5":"64.QAM.2/3" ,"6":"64.QAM.3/4","7":"64.QAM.5/6",
                    "10" : "BPSK.1/2" ,"11": "QPSK.1/2","12":"QPSK.3/4" ,"13":"16.QAM.1/2" ,"14":"16.QAM.3/4" ,"15":"64.QAM.2/3" ,"16":"64.QAM.3/4","17":"64.QAM.5/6",
                    "80" : "BPSK.1/2" ,"81": "QPSK.1/2","82":"QPSK.3/4" ,"83":"16.QAM.1/2" ,"84":"16.QAM.3/4" ,"85":"64.QAM.2/3" ,"86":"64.QAM.3/4","87":"64.QAM.5/6",
                    "90" : "BPSK.1/2" ,"91": "QPSK.1/2","92":"QPSK.3/4" ,"93":"16.QAM.1/2" ,"94":"16.QAM.3/4" ,"95":"64.QAM.2/3" ,"96":"64.QAM.3/4","97":"64.QAM.5/6",
                    "c0" : "BPSK.1/2" ,"c1": "QPSK.1/2","c2":"QPSK.3/4" ,"c3":"16.QAM.1/2" ,"c4":"16.QAM.3/4" ,"c5":"64.QAM.2/3" ,"c6":"64.QAM.3/4","c7":"64.QAM.5/6",
                    "d0" : "BPSK.1/2" ,"d1": "QPSK.1/2","d2":"QPSK.3/4" ,"d3":"16.QAM.1/2" ,"d4":"16.QAM.3/4" ,"d5":"64.QAM.2/3" ,"d6":"64.QAM.3/4","d7":"64.QAM.5/6"
        }

BW= {'0': "20MHZ" ,'1': "20MHZ","2":"20MHZ" ,"3":"20MHZ" ,"4":"20MHZ" ,"5":"20MHZ" ,"6":"20MHZ","7":"20MHZ",
        "10" : "20MHZ" ,"11": "20MHZ","12":"20MHZ" ,"13":"20MHZ" ,"14":"20MHZ" ,"15":"20MHZ" ,"16":"20MHZ","17":"20MHZ",
        "80" : "40MHZ" ,"81": "40MHZ","82":"40MHZ" ,"83":"40MHZ" ,"84":"40MHZ" ,"85":"40MHZ" ,"86":"40MHZ","87":"40MHZ",
        "90" : "40MHZ" ,"91": "40MHZ","92":"40MHZ" ,"93":"40MHZ" ,"94":"40MHZ" ,"95":"40MHZ" ,"96":"40MHZ","97":"40MHZ",
        "c0" : "40MHZ" ,"c1": "40MHZ","c2":"40MHZ" ,"c3":"40MHZ" ,"c4":"40MHZ" ,"c5":"40MHZ" ,"c6":"40MHZ","c7":"40MHZ",
        "d0" : "40MHZ" ,"d1": "40MHZ","d2":"40MHZ" ,"d3":"40MHZ" ,"d4":"40MHZ" ,"d5":"40MHZ" ,"d6":"40MHZ","d7":"40MHZ"
        }




time_rolling=time_index(clean_data)
time_rolling.index = pd.DatetimeIndex(time_rolling["timestamp"])
time_rolling=time_rolling.sort_index()

t1=time_rolling.first_valid_index()
t2=time_rolling.last_valid_index()

print(time_rolling.first_valid_index())
print(time_rolling.last_valid_index())

for t1 in (["100ms"]):
    for mac,macdata in time_rolling.groupby(["macaddr"],sort=False):
        fig = plt.figure(figsize=(35,15))
        airtime = []
        probability=[]
        Time=[]

        for time_rolling_subset in macdata.rolling(t1):
            last_index = time_rolling_subset['timestamp'].iat[-1]
            first_index = time_rolling_subset['timestamp'].iat[0]
            delta=last_index-first_index
            last_index=last_index.to_pydatetime()
            Time.append(last_index)
            # print(time_rolling_subset)
            attempt_p = attempt(time_rolling_subset)
            success_p = success(time_rolling_subset)
            fail_p = cal_failure(attempt_p,success_p)
            attempt_p.columns=["Fullattempt_count","rates","group","offset"]
            fail_p.columns=["Fullfail_count","rates","group","offset"]
            fail_probability = pd.merge(attempt_p,fail_p,on="rates",how="left")
            fail_probability = fail_probability.replace("", 0)
            fail_probability = fail_probability.fillna(0)
            fail_probability["fail_probability"]= fail_probability["Fullfail_count"]/fail_probability["Fullattempt_count"]
            probability_cur = fail_probability["fail_probability"].astype(float)
            probability.append(probability_cur)

### Coding,Modulation,Nss,GI,BW
            index=fail_probability.replace({"rates": dict})
            index =index['rates']
            airtime.append(index)
# # ### Coding,Modulation
#             index=Success_probability.replace({"rates": ModulationCoding})
#             index =index['rates']
#             airtime.append(index)
# ### NSS
            # index=Success_probability.replace({"rates": NSS})
            # index =index['rates']
            # airtime.append(index)
# ### BW
#             index=Success_probability.replace({"rates": BW})
#             index =index['rates']
#             airtime.append(index)
### GI
            # index=Success_probability.replace({"rates": GI})
            # index =index['rates']
            # airtime.append(index)


        yv =['0-BPSK.1/2.20MHz.LG.1Nss' ,'1-QPSK.1/2.20MHz.LG.1Nss','2-QPSK.3/4.20MHz.LG.1Nss' ,'3-16.QAM.1/2.20MHz.LG.1Nss' ,'4-16.QAM.3/4.20MHz.LG.1Nss' ,'5-64.QAM.2/3.20MHz.LG.1Nss' ,'6-64.QAM.3/4.20MHz.LG.1Nss','7-64.QAM.5/6.20MHz.LG.1Nss',
            '10-BPSK.1/2.20MHz.LG.2Nss' ,'11-QPSK.1/2.20MHz.LG.2Nss','12-QPSK.3/4.20MHz.LG.2Nss' ,'13-16.QAM.1/2.20MHz.LG.2Nss' ,'14-16.QAM.3/4.20MHz.LG.2Nss' ,'15-64.QAM.2/3.20MHz.LG.2Nss' ,'16-64.QAM.3/4.20MHz.LG.2Nss','17-64.QAM.5/6.20MHz.LG.2Nss',
            '80-BPSK.1/2.40MHz.LG.1Nss' ,'81-QPSK.1/2.40MHz.LG.1Nss','82-QPSK.3/4.40MHz.LG.1Nss' ,'83-16.QAM.1/2.40MHz.LG.1Nss' ,'84-16.QAM.3/4.40MHz.LG.1Nss' ,'85-64.QAM.2/3.40MHz.LG.1Nss' ,'86-64.QAM.3/4.40MHz.LG.1Nss','87-64.QAM.5/6.40MHz.LG.1Nss',
            '90-BPSK.1/2.40MHz.LG.2Nss' ,'91-QPSK.1/2.40MHz.LG.2Nss','92-QPSK.3/4.40MHz.LG.2Nss' ,'93-16.QAM.1/2.40MHz.LG.2Nss' ,'94-16.QAM.3/4.40MHz.LG.2Nss' ,'95-64.QAM.2/3.40MHz.LG.2Nss' ,'96-64.QAM.3/4.40MHz.LG.2Nss','97-64.QAM.5/6.40MHz.LG.2Nss',
            'c0-BPSK.1/2.40MHz.SG.1Nss' ,'c1-QPSK.1/2.40MHz.SG.1Nss','c2-QPSK.3/4.40MHz.SG.1Nss' ,'c3-16.QAM.1/2.40MHz.SG.1Nss' ,'c4-16.QAM.3/4.40MHz.SG.1Nss' ,'c5-64.QAM.2/3.40MHz.SG.1Nss' ,'c6-64.QAM.3/4.40MHz.SG.1Nss','c7-64.QAM.5/6.40MHz.SG.1Nss',
            'd0-BPSK.1/2.40MHz.SG.2Nss' ,'d1-QPSK.1/2.40MHz.SG.2Nss','d2-QPSK.3/4.40MHz.SG.2Nss' ,'d3-16.QAM.1/2.40MHz.SG.2Nss' ,'d4-16.QAM.3/4.40MHz.SG.2Nss' ,'d5-64.QAM.2/3.40MHz.SG.2Nss' ,'d6-64.QAM.3/4.40MHz.SG.2Nss','d7-64.QAM.5/6.40MHz.SG.2Nss',
            '110-BPSK.1/2.20MHz.LG.1Nss']

        ycm= ["BPSK.1/2","QPSK.1/2","QPSK.3/4","16.QAM.1/2","16.QAM.3/4","64.QAM.2/3","64.QAM.3/4","64.QAM.5/6"]
        ynss= ["1Nss","2Nss"]
        ybw= ["20MHz","40MHz"]
        ygi=["LG","SG"]

        # #
        colors_list = plt.cm.ocean_r(np.linspace(0.3, 1, 256))
        custom_cmap = colors.LinearSegmentedColormap.from_list('custom_ocean_r', colors_list)
        dummy,=plt.plot([Time[0]]*len(yv),yv)
        dummy.remove()
        for ii, (xe,ye) in enumerate(zip(Time,airtime)):
            plt.scatter([xe]*len(ye),ye, c=probability[ii],marker="s",cmap=custom_cmap,vmin=0,vmax=1, s=4)


        ax=plt.gca()
        xfmt = md.DateFormatter("%Y-%m-%d %H:%M:%S.%f")
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.grid(which='major',axis ='x', color='grey', linewidth=0.8,linestyle='--')
        ax.grid(which='major', axis='y', color='grey', linewidth=0.2, linestyle='--', alpha=0.5)

        plt.xticks(rotation=-35,fontsize=12 , ha='left')
        plt.xlabel('Time (DD-HH:MM:SS:ms)', fontsize=18)
        # Set ticks labels for x-axis
        plt.ylabel('Data Rate ',fontsize=18)
        # plt.title(f"Station: {mac} -fail probability map" ,fontsize=16 )
        plt.colorbar(matplotlib.cm.ScalarMappable(cmap=custom_cmap,norm=plt.Normalize(vmin=0,vmax=1)))
        plt.savefig(f"plot/{label_str}-MCS.vs.Time-coldprobabilitymap-{mac}-22-{index_range_str}-{t1}.png",format='png',dpi=500, bbox_inches='tight')
        plt.clf()
