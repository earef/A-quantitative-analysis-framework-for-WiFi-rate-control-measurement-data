
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import axes3d
import plotly.graph_objects as go

from process import success,attempt,time_index,time_conv

NSS= {'0': 1 ,'1': 1,"2":1 ,"3":1 ,"4":1 ,"5":1 ,"6":1,"7":1,
        "10" : 2 ,"11": 2,"12":2 ,"13":2 ,"14":2 ,"15":2 ,"16":2,"17":2,
        "80" : 1 ,"81": 1,"82":1 ,"83":1 ,"84":1 ,"85":1 ,"86":1,"87":1,
        "90" : 2 ,"91": 2,"92":2 ,"93":2 ,"94":2 ,"95":2 ,"96":2,"97":2,
        "c0" : 1 ,"c1": 1,"c2":1 ,"c3":1 ,"c4":1 ,"c5":1 ,"c6":1,"c7":1,
        "d0" : 2 ,"d1": 2,"d2":2 ,"d3":2 ,"d4":2 ,"d5":2 ,"d6":2,"d7":2
        }

GI= {'0': 800 ,'1': 800,"2":800 ,"3":800 ,"4":800 ,"5":800 ,"6":800,"7":800,
        "10" : 800 ,"11": 800,"12":800 ,"13":800 ,"14":800 ,"15":800 ,"16":800,"17":800,
        "80" : 800 ,"81": 800,"82":800 ,"83":800 ,"84":800 ,"85":800 ,"86":800,"87":800,
        "90" : 800 ,"91": 800,"92":800 ,"93":800 ,"94":800 ,"95":800 ,"96":800,"97":800,
        "c0" : 400 ,"c1": 400,"c2":400 ,"c3":400 ,"c4":400 ,"c5":400 ,"c6":400,"c7":400,
        "d0" : 400 ,"d1": 400,"d2":400 ,"d3":400 ,"d4":400 ,"d5":400 ,"d6":400,"d7":400
        }

# ModulationCoding= {'0': 0 ,'1': 1,"2":2 ,"3":3 ,"4":4 ,"5":5 ,"6":6,"7":7,
#                     "10" : 0 ,"11": 1,"12":2 ,"13":3 ,"14":4 ,"15":5 ,"16":6,"17":7,
#                     "80" : 0 ,"81": 1,"82":2 ,"83":3 ,"84":4 ,"85":5 ,"86":6,"87":7,
#                     "90" : 0 ,"91": 1,"92":2 ,"93":3 ,"94":4 ,"95":5 ,"96":6,"97":7,
#                     "c0" : 0 ,"c1": 1,"c2":2 ,"c3":3 ,"c4":4 ,"c5":5 ,"c6":6,"c7":7,
#                     "d0" : 0 ,"d1": 1,"d2":2 ,"d3":3 ,"d4":4 ,"d5":5 ,"d6":6,"d7":7
#         }
ModulationCoding= {'0': "BPSK.1/2" ,'1': "QPSK.1/2","2":"QPSK.3/4" ,"3":"16.QAM.1/2" ,"4":"16.QAM.3/4" ,"5":"64.QAM.2/3" ,"6":"64.QAM.3/4","7":"64.QAM.5/6",
                    "10" : "BPSK.1/2" ,"11": "QPSK.1/2","12":"QPSK.3/4" ,"13":"16.QAM.1/2" ,"14":"16.QAM.3/4" ,"15":"64.QAM.2/3" ,"16":"64.QAM.3/4","17":"64.QAM.5/6",
                    "80" : "BPSK.1/2" ,"81": "QPSK.1/2","82":"QPSK.3/4" ,"83":"16.QAM.1/2" ,"84":"16.QAM.3/4" ,"85":"64.QAM.2/3" ,"86":"64.QAM.3/4","87":"64.QAM.5/6",
                    "90" : "BPSK.1/2" ,"91": "QPSK.1/2","92":"QPSK.3/4" ,"93":"16.QAM.1/2" ,"94":"16.QAM.3/4" ,"95":"64.QAM.2/3" ,"96":"64.QAM.3/4","97":"64.QAM.5/6",
                    "c0" : "BPSK.1/2" ,"c1": "QPSK.1/2","c2":"QPSK.3/4" ,"c3":"16.QAM.1/2" ,"c4":"16.QAM.3/4" ,"c5":"64.QAM.2/3" ,"c6":"64.QAM.3/4","c7":"64.QAM.5/6",
                    "d0" : "BPSK.1/2" ,"d1": "QPSK.1/2","d2":"QPSK.3/4" ,"d3":"16.QAM.1/2" ,"d4":"16.QAM.3/4" ,"d5":"64.QAM.2/3" ,"d6":"64.QAM.3/4","d7":"64.QAM.5/6"
        }

BW= {'0': 20 ,'1': 20,"2":20 ,"3":20 ,"4":20 ,"5":20 ,"6":20,"7":20,
        "10" : 20 ,"11": 20,"12":20 ,"13":20 ,"14":20 ,"15":20 ,"16":20,"17":20,
        "80" : 40 ,"81": 40,"82":40 ,"83":40 ,"84":40 ,"85":40 ,"86":40,"87":40,
        "90" : 40 ,"91": 40,"92":40 ,"93":40 ,"94":40 ,"95":40 ,"96":40,"97":40,
        "c0" : 40 ,"c1": 40,"c2":40 ,"c3":40 ,"c4":40 ,"c5":40 ,"c6":40,"c7":40,
        "d0" : 40 ,"d1": 40,"d2":40 ,"d3":40 ,"d4":40 ,"d5":40 ,"d6":40,"d7":40
        }

ycm= ["BPSK.1/2","QPSK.1/2","QPSK.3/4","16.QAM.1/2","16.QAM.3/4","64.QAM.2/3","64.QAM.3/4","64.QAM.5/6"]
ynss= [1,2]
ybw=  [20,40]
ygi=  [800,400]

# # # # Successful probability
attempt_p = attempt(time_conv)
attempt_p.columns=["Fullattempt_count","rates","group","offset"]
success_p = success(time_conv)
success_p.columns=["FullSuccess_count","rates","group","offset"]
Success_probability = pd.merge(attempt_p,success_p,on="rates",how="left")
Success_probability = Success_probability.replace("", 0)
Success_probability = Success_probability.fillna(0)
Success_probability["Success_Probability"]= Success_probability["FullSuccess_count"]/Success_probability["Fullattempt_count"]

Success_probability["Spatial_Stream"]= Success_probability['rates'].map(NSS)
Success_probability["Guard_Interval"]= Success_probability['rates'].map(GI)
Success_probability["Modulation_Coding"]= Success_probability['rates'].map(ModulationCoding)
Success_probability["Band_Width"]= Success_probability['rates'].map(BW)

# fig = px.scatter_3d(Success_probability, x='Band_Width', y='Success_Probability', z='Spatial_Stream', symbol='Guard_Interval',
#   hover_name='Modulation_Coding',color='Modulation_Coding')
# fig.update_layout(scene = dict(
#                     xaxis = dict(
#                         ticktext= ['20MHz','40MHz'],
#                         tickvals= [20,40]),
#                     zaxis = dict(
#                         ticktext= ['1Nss','2Nss'],
#                         tickvals= [1,2]),)
#
#                   )
# fig.update_traces(marker_size = 4)
# fig.show()


fig = px.scatter_3d(Success_probability, x='Band_Width', y='Success_Probability', z='Spatial_Stream', symbol='Guard_Interval',
hover_name='Modulation_Coding',color='Modulation_Coding',color_discrete_sequence= px.colors.sequential.Plasma_r,
                   title="5-dimensional MCS Index success probability")
fig.update_layout(scene = dict(
                    xaxis = dict(
                        ticktext= ['20MHz','40MHz'],
                        tickvals= [20,40]),
                    zaxis = dict(
                        ticktext= ['1Nss','2Nss'],
                        tickvals= [1,2]),)

                  )
fig.write_html("plot/Bestplots/5D-bc:a8:a6:9c:6f:53.html")
fig.show()
