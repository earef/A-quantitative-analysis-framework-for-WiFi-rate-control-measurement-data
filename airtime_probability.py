import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from process import success,attempt,time_index,time_conv
from cleaning import to_int,dataset,index_range_str,label_str

plt.style.use('seaborn')

dict= {'0': '168980', '1': 'b44c0', '2': '783c0', '3': '5a260', '4': '3c1e0', '5': '2d1a0', '6': '28180', '7': '24120',
'10': 'b44c0', '11': '5a260', '12': '3c1e0', '13': '2d1a0', '14': '1e170', '15': '16950', '16': '14140', '17': '12110',
'40': '1448c0', '41': 'a2460', '42': '6c3a0', '43': '51240', '44': '361e0', '45': '289a0', '46': '241a0', '47': '207a0',
'50': 'a2470', '51': '51250', '52': '361e0', '53': '289b0', '54': '1b170', '55': '14560', '56': '12150', '57': '10450',
'80': 'ada50', '81': '56da0', '82': '39ec0', '83': '2b750', '84': '1cfd0', '85': '15ba0', '86': '13590', '87': '11650',
'90':'56da0' , '91':'2b750' ,'92':'1cfd8' ,'93':'15ba8' ,'94' :'e868', '95' :'add0','96' :'9b40','97':'8ba0',
'c0': '9c4a0', 'c1': '4e2e0', 'c2': '34240', 'c3': '271f0', 'c4': '1a1a0', 'c5': '13910', 'c6': '116c0', 'c7': 'faa0',
'd0': '4e2e0', 'd1': '271f8', 'd2': '1a1a8', 'd3': '13910', 'd4': 'd160', 'd5': '9ca0', 'd6': '8bf0', 'd7': '7de0','110':'190640'}

airtime= ['7de0', '8ba0', '8bf0', '9b40', '9ca0', 'add0', 'd160', 'e868', 'faa0', '10450', '11650', '116c0', '12110',
 '12150', '13590', '13910', '13910', '14140', '14560', '15ba0', '15ba8', '16950', '1a1a0', '1a1a8', '1b170',
 '1cfd0', '1cfd8', '1e170', '207a0', '24120', '241a0', '271f0', '271f8', '28180', '289a0', '289b0', '2b750',
  '2b750', '2d1a0', '2d1a0', '34240', '361e0', '361e0', '39ec0', '3c1e0', '3c1e0', '4e2e0', '4e2e0', '51240',
  '51250', '56da0', '56da0', '5a260', '5a260', '6c3a0', '783c0', '9c4a0', 'a2460', 'a2470', 'ada50', 'b44c0',
   'b44c0', '1448c0', '168980','190640']


#
#
# print(sorted(a, key=lambda h: int(h, 16))
# )
# print(time_conv)
print(time_conv.first_valid_index())
print(time_conv.last_valid_index())
for mac,macdata in time_conv.groupby(["macaddr"],sort=False):

# # # # # Successful probability
    fig = plt.figure(figsize=(24,10))
    attempt_p = attempt(macdata)
    attempt_p.columns=["Fullattempt_count","rates","group","offset"]
    attempt_p=attempt_p[["Fullattempt_count","rates"]]
    success_p = success(macdata)
    success_p.columns=["FullSuccess_count","rates","group","offset"]
    success_p=success_p[["FullSuccess_count","rates"]]

    Success_probability = pd.merge(attempt_p,success_p,how="outer")
    Success_probability = Success_probability.fillna(0)
    Success_probability["Success_probability"]= Success_probability["FullSuccess_count"]/Success_probability["Fullattempt_count"]
    Success_probability=Success_probability.replace({"rates": dict})
    # Success_probability=Success_probability.groupby('rates', as_index=False)['Success_probability'].mean()
    # print(Success_probability)
    # # # # # plot barplot for success probability
    dummy,=plt.plot(airtime,[Success_probability["Success_probability"].iat[0]]*len(airtime))
    dummy.remove()
    # plot the scatter plot with the "viridis" colormap
    plt.scatter(Success_probability['rates'],Success_probability['Success_probability'], c='navy', s=30, alpha=0.6, edgecolors='none')
    # plt.title("Success probability over Airtime")
    plt.xlabel("Airtime(hex)",fontsize=9)
    plt.ylabel("Probability of Successful Transmission",fontsize=10)
    plt.xticks(fontsize=12, rotation=35,ha="right" )
    plt.yticks(fontsize=10)
    plt.ylim(0,1.1)
    plt.tight_layout()
    plt.savefig(f"plot/{label_str}-probability vs airtime-{mac}-22-{index_range_str}.png" ,format='png', dpi=200 ,bbox_inches='tight')
    plt.clf()
