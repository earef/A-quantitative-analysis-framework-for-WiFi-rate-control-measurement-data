import pandas as pd
import numpy as np
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker



import seaborn as sns
from matplotlib.ticker import MaxNLocator
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize


pd.set_option('display.max_rows', None, 'display.max_columns', None)

from process import success,attempt,time_index
from cleaning import to_int,clean_data

# dict= {'0': '168980', '1': 'b44c0', '2': '783c0', '3': '5a260', '4': '3c1e0', '5': '2d1a0', '6': '28180', '7': '24120', '8': '0', '9': '0', '10': 'b44c0', '11': '5a260', '12': '3c1e0', '13': '2d1a0', '14': '1e170', '15': '16950', '16': '14140', '17': '12110', '18': '0', '19': '0', '20': '783d0', '21': '3c1e8', '22': '28198', '23': '1e170', '24': '14148', '25': 'f130', '26': 'd5d8', '27': 'c060', '28': '0', '29': '0', '30': '5a260', '31': '2d1a8', '32': '1e170', '33': '16950', '34': 'f130', '35': 'b4a8', '36': 'a120', '37': '9088', '38': '0', '39': '0', '40': '1448c0', '41': 'a2460', '42': '6c3a0', '43': '51240', '44': '361e0', '45': '289a0', '46': '241a0', '47': '207a0', '48': '0', '49': '0', '50': 'a2470', '51': '51250', '52': '361e8', '53': '289b0', '54': '1b170', '55': '14560', '56': '12150', '57': '10450', '58': '0', '59': '0', '60': '6c3a0', '61': '361e8', '62': '241a0', '63': '1b178', '64': '12158', '65': 'd948', '66': 'c0a8', '67': 'ad50', '68': '0', '69': '0', '70': '51250', '71': '289b0', '72': '1b178', '73': '14560', '74': 'd948', '75': 'a2c8', '76': '9130', '77': '8240', '78': '0', '79': '0', '80': 'ada50', '81': '56da0', '82': '39ec0', '83': '2b750', '84': '1cfd0', '85': '15ba0', '86': '13590', '87': '11650', '88': '0', '89': '0', '90': '56da0', '91': '2b750', '92': '1cfd8', '93': '15ba8', '94': 'e868', '95': 'add0', '96': '9b40', '97': '8ba0', '98': '0', '99': '0', 'a0': '39ec0', 'a1': '1cfdc', 'a2': '13590', 'a3': 'e86c', 'a4': '9b44', 'a5': '7434', 'a6': '6784', 'a7': '5cc4', 'a8': '0', 'a9': '0', 'b0': '2b750', 'b1': '15ba8', 'b2': 'e86c', 'b3': 'add4', 'b4': '7434', 'b5': '56e8', 'b6': '4e020', 'b7': '4650', 'b8': '0', 'b9': '0', 'c0': '9c4a0', 'c1': '4e2e0', 'c2': '34240', 'c3': '271f0', 'c4': '1a1a0', 'c5': '13910', 'c6': '116c0', 'c7': 'faa0', 'c8': '0', 'c9': '0', 'd0': '4e2e0', 'd1': '271f8', 'd2': '1a1a8', 'd3': '13910', 'd4': 'd160', 'd5': '9ca0', 'd6': '8bf0', 'd7': '7de0', 'd8': '0', 'd9': '0', 'e0': '34244', '0e1': '1a1ac', 'e2': '116cc', 'e3': 'd160', 'e4': '8bf0', 'e5': '68c8', 'e6': '5d5c', 'e7': '53b0', 'e8': '0', 'e9': '0', 'f0': '271f8', 'f1': '13914', 'f2': 'd160', 'f3': '9ca4', 'f4': '68c8', 'f5': '4e068', 'f6': '4680', 'f7': '3f78', 'f8': '0', 'f9': '0', '100': '960', '101': '4c910', '102': '1dcc00', '103': '106f00', '104': '949700', '105': '4b1a00', '106': '1c5500', '107': 'ef800', '108': '0', '109': '0', '110': '0', '111': '10d880', '112': 'cc1a0', '113': '8aac0', '114': '6a720', '115': '493', '116': '399', '117': '33c20', '118': '0', '119': '0', '120': '168980', '121': 'b44c0', '122': '783c0', '123': '5a260', '124': '3c1e0', '125': '2d1a0', '126': '28180', '127': '24120', '128': '1e160', '129': '1b180', '130': 'b44c0', '131': '5a260', '132': '3c1e0', '133': '2d1a0', '134': '1e170', '135': '16950', '136': '14140', '137': '12110', '138': 'f130', '139': 'd8c0', '140': '783d0', '141': '3c1e8', '142': '28198', '143': '1e170', '144': '14148', '145': 'f130', '146': 'd5d8', '147': 'c060', '148': 'a120', '149': '9088', '150': '5a260', '151': '2d1a8', '152': '1e170', '153': '16950', '154': 'f130', '155': 'b4a8', '156': 'a120', '157': '9088', '158': '7918', '159': '6c60', '160': '1448c0', '161': 'a2460', '162': '6c3a0', '163': '51240', '164': '361e8', '165': '289a0', '166': '241a0', '167': '207a0', '168': '1b160', '169': '18660', '170': 'a2470', '171': '51250', '172': '361e8', '173': '289b0', '174': '1b170', '175': '14560', '176': '12150', '177': '10450', '178': 'd940', '179': 'c350', '180': '6c3a0', '181': '361e8', '182': '241a0', '183': '1b178', '184': '12158', '185': 'd948', '186': 'c0a8', '187': 'ad50', '188': '9130', '189': '8240', '190': '51250', '191': '289b0', '192': '1b178', '193': '14560', '194': 'd948', '195': 'a2c8', '196': '9130', '197': '8240', '198': '6d28', '199': '61c0', '1a0': 'ada50', '1a1': '56da0', '1a2': '39ec0', '1a3': '2b750', '1a4': '1cfd0', '1a5': '15ba0', '1a6': '13590', '1a7': '11650', '1a8': 'e860', '1a9': 'd0f0', '1b0': '56da0', '1b1': '2b750', '1b2': '1cfd8', '1b3': '15ba8', '1b4': 'e868', '1b5': 'add0', '1b6': '9b40', '1b7': '8ba0', '1b8': '7430', '1b9': '6878', '1c0': '39ec0', '1c1': '1cfdc', '1c2': '13590', '1c3': 'e86c', '1c4': '9b44', '1c5': '7434', '1c6': '6784', '1c7': '5cc4', '1c8': '4e020', '1c9': '4650', '1d0': '2b750', '1d1': '15ba8', '1d2': 'e86c', '1d3': 'add4', '1d4': '7434', '1d5': '56e8', '1d6': '4e20', '1d7': '4650', '1d8': '3a98', '1d9': '34bc', '1e0': '9c4a0', '1e1': '4e2e0', '1e2': '34240', '1e3': '271f0', '1e4': '1a1a0', '1e5': '13910', '1e6': '116c0', '1e7': 'faa0', '1e8': 'd160', '1e9': 'bc40', '1f0': '4e2e0', '1f1': '271f8', '1f2': '1a1a8', '1f3': '13910', '1f4': 'd160', '1f5': '9ca0', '1f6': '8bf0', '1f7': '7de0', '1f8': '68c8', '1f9': '5e038', '200': '34244', '201': '1a1ac', '202': '116cc', '203': 'd160', '204': '8bf0', '205': '68c8', '206': '5d5c', '207': '53b0', '208': '4680', '209': '3f78', '210': '271f8', '211': '13914', '212': 'd160', '213': '9ca4', '214': '68c8', '215': '4e068', '216': '4680', '217': '3f78', '218': '34ec', '219': '2fa8', '220': '50238', '221': '28198', '222': '1abb8', '223': '14148', '224': 'd5d8', '225': 'a120', '226': '8e090', '227': '80e8', '228': '6b68', '229': '60a8', '230': '28198', '231': '14148', '232': 'd5dc', '233': 'a120', '234': '6b6c', '235': '510c', '236': '4748', '237': '4074', '238': '35b4', '239': '30d4', '240': '1abbc', '241': 'd5de', '242': '8e094', '243': '6b6c', '244': '474a', '245': '35b6', '246': '2fda', '247': '2af8', '248': '2422', '249': '203a', '250': '1414a', '251': 'a122', '252': '6b6c', '253': '510e', '254': '35b6', '255': '2904', '256': '2422', '257': '203a', '258': '1b58', '259': '186a', '260': '48230', '261': '241a0', '262': '18128', '263': '12158', '264': 'c0a8', '265': '9130', '266': '8080', '267': '7430', '268': '60', '269': '5730', '270': '241a0', '271': '12158', '272': 'c0ac', '273': '9134', '274': '60', '275': '4924', '276': '4058', '277': '3a34', '278': '3088', '279': '2c24', '280': '18128', '281': 'c0ac', '282': '8084', '283': '60', '284': '405a', '285': '3088', '286': '2b42', '287': '26de', '288': '20b6', '289': '1d32', '290': '1215a', '291': '9136', '292': '60', '293': '4924', '294': '3088', '295': '251c', '296': '20b6', '297': '1d32', '298': '18ce', '299': '162a'}






time_rolling=time_index(clean_data)
time_rolling.index = pd.DatetimeIndex(time_rolling["timestamp"])
time_rolling=time_rolling.sort_index()

t1=time_rolling.first_valid_index()
t2=time_rolling.last_valid_index()

print(time_rolling.first_valid_index())
print(time_rolling.last_valid_index())

for t1 in (["50ms","10ms","5ms","1ms"]):
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
            attempt_p.columns=["Fullattempt_count","rates","group","offset"]
            success_p = success(time_rolling_subset)
            success_p.columns=["FullSuccess_count","rates","group","offset"]
            Success_probability = pd.merge(attempt_p,success_p,on="rates",how="left")
            Success_probability = Success_probability.replace("", 0)
            Success_probability = Success_probability.fillna(0)
            Success_probability["Success_probability"]= Success_probability["FullSuccess_count"]/Success_probability["Fullattempt_count"]

            probability_cur = Success_probability["Success_probability"].astype(float)
            probability.append(probability_cur)
# ### mcs + airtime
            # Success_probability['mcs']=Success_probability['rates']
            # # print(fail_probability.dtypes)
            # index=Success_probability.replace({"rates": dict})
            # index['rates']=index['rates'].apply(lambda x: int(x, 16))
            # index.sort_values(['rates'], inplace=True)
            # index['mcsair'] =  index['rates'].astype(str) +"-"+ Success_probability["mcs"].astype(str)
            # index.sort_values(['mcsair'], inplace=True)
            # index =index['mcsair']
            # airtime.append(index)

# ### airtime int64
            # index=Success_probability.replace({"rates": dict})
            # index['rates']=index['rates'].apply(lambda x: int(x, 16))
            # index.sort_values(['rates'], inplace=True)
            # index =index['rates']
            # airtime.append(index)
            # print([type(i) for i in Time])
            # print([type(i) for i in probability])
            # print([type(i) for i in airtime])
        # print(airtime,probability,Time)

# # ### mcs int 64
            Success_probability['rates']=Success_probability['rates'].apply(lambda x: int(x, 16))
            index=Success_probability['rates']
            airtime.append(index)

        ax=plt.gca()
        def to_hex(x, pos):
            return '%x' % int(x)

        yfmt = ticker.FuncFormatter(to_hex)
        ax.grid(which ='major', axis ='y', linestyle ='--')
        ax.grid(which='minor',axis ='y',color='black', linewidth=0.4,linestyle =':',fillstyle="right")
        ax.grid(which='major',axis ='y', color='black', linewidth=1.2,linestyle='--')
        ax.get_yaxis().set_major_locator(ticker.MultipleLocator(8))
        ax.get_yaxis().set_major_formatter(yfmt)
        ax.get_yaxis().set_minor_locator(ticker.MultipleLocator(1))

        xfmt = md.DateFormatter("%Y-%m-%d %H:%M:%S.%f")
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.grid(which='major',axis ='x', color='blue', linewidth=0.8,linestyle='--')


        for ii, (xe,ye) in enumerate(zip(Time,airtime)):
            plt.scatter([xe]*len(ye),ye, c=probability[ii],s=60,marker="x",cmap='Reds',vmin=0,vmax=1)
        plt.xticks(rotation=-35,fontsize=18 , ha='left')
        plt.xlabel('Time',fontsize=22)
        plt.yticks(fontsize=19)
        plt.ylabel('Mcs rate - airtime',fontsize=22)
        plt.title(f"Client: {mac} -Success probability map" ,fontsize=24 )
        plt.colorbar(matplotlib.cm.ScalarMappable(cmap='Reds',norm=plt.Normalize(vmin=0,vmax=1)))
        # plt.show()
        plt.savefig(f"plot/SPA/SP-probe(0)-{mac}-Rolling on{t1}-set4.svg",format='svg', bbox_inches='tight')
        plt.clf()
