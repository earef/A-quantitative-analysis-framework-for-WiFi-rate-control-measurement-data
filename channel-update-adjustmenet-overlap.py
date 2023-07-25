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

# pd.set_option('display.max_rows', 200, 'display.max_columns', 200)
from process import success,success_timestamp,cal_failure,attempt,time_index
from cleaning import to_int,dataset,index_range_str,label_str,clean_data


time_rolling=time_index(clean_data)
#
# print(time_rolling.first_valid_index())
# print(time_rolling.last_valid_index())
time_rolling.index = pd.DatetimeIndex(time_rolling["timestamp"])
time_rolling=time_rolling.sort_index()

for t1 in (["100ms"]):
    for mac,macdata in time_rolling.groupby(["macaddr"],sort=False):
        Time=[]
        # minmax=[]
        minoveral=[]
        # intersection=[]

        for time_rolling_subset in macdata.rolling(t1):
        # Calculating overlap/attemp and drop in in the miu
            last_index = time_rolling_subset['timestamp'].iat[-1]
            first_index = time_rolling_subset['timestamp'].iat[0]
            last_index=last_index.to_pydatetime()
            Time.append(last_index)


            rolling_success=success(time_rolling_subset)
            rolling_attempt=attempt(time_rolling_subset)
            rolling_fail=cal_failure(rolling_attempt,rolling_success)

            rolling_fail = rolling_fail[['failed_counts','rates']]
            rolling_success = rolling_success[['FullSuccess_count','successful_rates']]
            rolling_success.columns = ["FullSuccess_count","rates"]

            overlap= pd.merge(rolling_fail,rolling_success,how="outer")
            overlap['FullSuccess_count'] = overlap['FullSuccess_count'].fillna(0)
            overlap['failed_counts'] = overlap['failed_counts'].fillna(0)
            # overlap["overlap_minmax"] = (overlap[["FullSuccess_count", "failed_counts"]].min(axis=1)).div(overlap[["FullSuccess_count", "failed_counts"]].max(axis=1))
            overlap["overlap_minoveral"]= (overlap[["FullSuccess_count", "failed_counts"]].min(axis=1)).div(overlap["FullSuccess_count"]+overlap["failed_counts"])
            # overlap['overlap_intersection']= ((overlap["FullSuccess_count"]).div(overlap["FullSuccess_count"]+overlap["failed_counts"])).mul((overlap["failed_counts"]).div(overlap["FullSuccess_count"]+overlap["failed_counts"]))


            # overlap["overlap_minoveral_mean_normalized"]=(overlap["overlap_minoveral"]-overlap["overlap_minoveral"].mean())/overlap["overlap_minoveral"].std()
            overlap["overlap_minoveral_minmax_normalized"]=(overlap["overlap_minoveral"])/0.5
            # overlap["overlap_intersection_minmax_normalized"]=(overlap["overlap_intersection"])/0.25

            # avg_minmax = overlap["overlap_minmax"] .mean()
            avg_minoveral = overlap["overlap_minoveral_minmax_normalized"] .mean()
            # avg_intersection = overlap["overlap_intersection_minmax_normalized"] .mean()

            # minmax.append(avg_minmax)
            minoveral.append(avg_minoveral)
            # intersection.append(avg_intersection)
        # axs[0].plot(Time,minmax,"o",c="green",markersize=2.2,alpha=1)
        # axs[0].spines["top"].set_visible(False)
        # axs[0].spines['bottom'].set_color('darkgray')
        #
        # axs[0].set_ylabel("Avg overlap for packets success & fail count\n(min count/max count)",fontsize=9)
        # axs[0].set_ylim(0, 1)
        # axs[0].tick_params(axis='x', rotation=-35)
        #
        # ax.plot(Time,minoveral,"o",c="green",markersize=2.2,alpha=1)
        # ax.spines["top"].set_visible(False)
        # ax.spines['bottom'].set_color('darkgray')
        # ax.set_xlabel("Time",fontsize=9)
        # ax.set_ylabel("Average overlap",fontsize=9)
        # ax.set_ylim(0, 1)
        #
        # # axs[2].plot(Time,intersection,"o",c="green",markersize=2.2,alpha=1)
        # # axs[2].spines["top"].set_visible(False)
        # # axs[2].spines['bottom'].set_color('darkgray')
        # #
        # # axs[2].set_xlabel("Time",fontsize=9)
        # # axs[2].set_ylabel("Avg overlap for packets success & fail count\n(probability of intersection(scaled value 0-1))",fontsize=9)
        # # axs[2].set_ylim(0, 1)
        # # axs[1].set_ylim(0, 1)
        # # fig.suptitle(f"device: {mac}")
        # # plt.savefig(f"plot/overlap/Rolling/1d/overlap-{mac}-Rolling on{t1}-1d-ath9knew.png",format='png',dpi=200 ,bbox_inches='tight')
        # plt.savefig(f"plot/April/{label_str}-overlap-{mac}-22-{index_range_str}-{t1}.png",format='png',dpi=200 ,bbox_inches='tight')
        #
        # plt.clf()
        # plt.show()

        # Create figure and axis objects
        fig, ax = plt.subplots(figsize=(40, 15))

        # Plot data with better marker style and color
        ax.plot(Time, minoveral, "o", c="steelblue", markersize=4, alpha=0.8)

        # ax=plt.gca()
        xfmt = md.DateFormatter("%Y-%m-%d %H:%M:%S.%f")
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.spines["top"].set_visible(False)
        ax.spines['bottom'].set_color('darkgray')

        # Set axis labels
        ax.set_xlabel("Time (YY-MM-DD-HH:MM:SS:ms)", fontsize=9)
        ax.set_ylabel("Average overlap", fontsize=9)

        # Set y-axis limit
        ax.set_ylim(0, 1.1)

        # Customize grid appearance
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5, color='lightgray')

        # Save the plot
        plt.savefig(f"plot/{label_str}-overlap-{mac}-22-{index_range_str}-{t1}.png", format='png', dpi=200, bbox_inches='tight')

        # Clear the plot and show it
        plt.clf()
