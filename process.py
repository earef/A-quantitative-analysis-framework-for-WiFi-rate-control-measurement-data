import pandas as pd
import numpy as np
import argparse

from cleaning import clean_data,index_range_str,label_str
# pd.set_option('display.max_rows', 10, 'display.max_columns', 2)


# # # time conversion unix nanosecond
def time_index(t):
    t = t.reset_index(drop=True)
    t["timestamp"] = t["timestamp"].fillna(0)
    t["timestamp"] = t["timestamp"].apply(lambda x: int(x, 16))

    # Convert nanoseconds UNIX timestamp to datetime
    t['timestamp'] = pd.to_datetime(t['timestamp'], unit='ns')

    datetime_series = pd.to_datetime(t['timestamp'])
    datetime_index = pd.DatetimeIndex(datetime_series.values)
    t = t.set_index(datetime_index)
    return t

time_conv = time_index(clean_data)


# # # suucess value count based on num-ack
def success(s):
    SuccessRate3=s.loc[(s['count3'] > 0 , ["timestamp","num_frames","num_acked" ,"rate3"])]
    B=s.loc[(s['count3'] == 0 )]
    SuccessRate2=B.loc[(B['count2'] > 0 ,["timestamp" ,"num_frames","num_acked" ,"rate2"])]
    D=B.loc[(B['count2'] == 0 )]
    SuccessRate1=D.loc[(D['count1'] > 0 ,["timestamp" ,"num_frames","num_acked" ,"rate1"])]
    F=D.loc[(D['count1'] == 0 )]
    SuccessRate0=F.loc[(F['count0'] > 0 ,["timestamp","num_frames","num_acked"  ,"rate0"])]
    H=F.loc[(F['count0'] == 0 )]
    Success_rate_set = [SuccessRate0,SuccessRate1,SuccessRate2,SuccessRate3]
    Success_rate = pd.concat(Success_rate_set,ignore_index=True)
    Success_rate["successful_rates"]= Success_rate['rate3'].fillna(Success_rate['rate2'])
    Success_rate["successful_rates"]= Success_rate['successful_rates'].fillna(Success_rate['rate0'])
    Success_rate["successful_rates"]= Success_rate['successful_rates'].fillna(Success_rate['rate1'])
    Success_rate = Success_rate [['timestamp',"num_frames","num_acked" ,'successful_rates']]
    Success_rate["FullSuccess_count"]=1*Success_rate["num_acked"]
    Success_rate = Success_rate[['FullSuccess_count','successful_rates']]
    # # # Counting success rates
    Success_rate['successful_rates'] = Success_rate['successful_rates'].astype(int)
    Success_rate['successful_rates'] = Success_rate['successful_rates'].apply(lambda x: hex(x))
    Success_rate = Success_rate.groupby('successful_rates').sum()
    Success_rate['successful_rates'] = Success_rate.index
    Success_rate = Success_rate.reset_index(drop=True)
    Success_rate["successful_rates"] = Success_rate['successful_rates'].astype(str).str.slice(start=2)

    # # # Dividing Group and offset
    Success_rate["group"] = Success_rate['successful_rates'].astype(str).str.slice(stop=-1)
    Success_rate["offset"] = Success_rate['successful_rates'].astype(str).str.slice(start=-1)
    return(Success_rate) #return (timestamp, success_rate) -> x[]
FullSuccess=success(time_conv)
# FullSuccess.to_csv("CleanDataset/Succes1.csv")

# # # Calculating the success rates per timestamp
def success_timestamp(time):
    SuccessRate3=time.loc[(time['count3'] > 0 , ["timestamp","macaddr","num_frames","num_acked" ,"rate3"])]
    B=time.loc[(time['count3'] == 0 )]
    SuccessRate2=B.loc[(B['count2'] > 0 ,["timestamp","macaddr" ,"num_frames","num_acked" ,"rate2"])]
    D=B.loc[(B['count2'] == 0 )]
    SuccessRate1=D.loc[(D['count1'] > 0 ,["timestamp" ,"macaddr","num_frames","num_acked" ,"rate1"])]
    F=D.loc[(D['count1'] == 0 )]
    SuccessRate0=F.loc[(F['count0'] > 0 ,["timestamp","macaddr","num_frames","num_acked"  ,"rate0"])]
    H=F.loc[(F['count0'] == 0 )]
    Success_rate_set = [SuccessRate0,SuccessRate1,SuccessRate2,SuccessRate3]
    Success_rate_time = pd.concat(Success_rate_set,ignore_index=True)
    Success_rate_time["successful_rates"]= Success_rate_time['rate3'].fillna(Success_rate_time['rate2'])
    Success_rate_time["successful_rates"]= Success_rate_time['successful_rates'].fillna(Success_rate_time['rate0'])
    Success_rate_time["successful_rates"]= Success_rate_time['successful_rates'].fillna(Success_rate_time['rate1'])
    Success_rate_time = Success_rate_time [['timestamp',"macaddr","num_frames","num_acked" ,'successful_rates']]
    Success_rate_time["FullSuccess_count"]=1*Success_rate_time["num_acked"]
    Success_rate_time = Success_rate_time[["timestamp","macaddr",'FullSuccess_count','successful_rates']]
    return(Success_rate_time)
# FullSuccess_timestamped=success_timestamp(time_conv)

# # # number of tried attempts
def attempt(attempt):
    badge0 = attempt.assign(Fullattempt_count=attempt["count0"]*attempt["num_frames"])
    badge0= badge0[['Fullattempt_count', 'rate0']]
    badge1 = attempt.assign(FrameCount1=attempt["count1"]*attempt["num_frames"])
    badge1= badge1[['FrameCount1', 'rate1']]
    badge2 = attempt.assign(FrameCount2=attempt["count2"]*attempt["num_frames"])
    badge2= badge2[['FrameCount2', 'rate2']]
    badge3 = attempt.assign(FrameCount3=attempt["count3"]*attempt["num_frames"])
    badge3= badge3[['FrameCount3', 'rate3']]
    badge=[badge0,badge1,badge2,badge3]
    badge0=badge0.groupby('rate0').sum()
    badge1=badge1.groupby('rate1').sum()
    badge2=badge2.groupby('rate2').sum()
    badge3=badge3.groupby('rate3').sum()
    badge=[badge0,badge1,badge2,badge3]
    a = pd.concat(badge,axis=1)
    a=a.fillna(0)
    a=a.sum(axis=1)
    a = a.reset_index(level=0)
    a.columns=["attempt_rates","Fullattempt_count"]
    a['attempt_rates'] =a["attempt_rates"].astype(int)
    a['attempt_rates'] = a['attempt_rates'].apply(lambda x: hex(x))
    a = a.reset_index(level=0)
    a = a[['Fullattempt_count','attempt_rates']]
    a["attempt_rates"] = a['attempt_rates'].astype(str).str.slice(start=2)

    # # # Dividing Group and offset
    a["group"] = a['attempt_rates'].astype(str).str.slice(stop=-1)
    a["offset"]= a['attempt_rates'].astype(str).str.slice(start=-1)
    a = a.replace("", 0)
    a["group"] = a['group'].astype(str)
    a["offset"] = a['offset'].astype(str)
    a=a.loc[a['Fullattempt_count'] > 0]
    return(a)
attempt_check=attempt(time_conv)
### Calculating the success rates per timestamp

def attempt_timestamp(atime):
    badge0 = atime.assign(Fullattempt_count=atime["count0"]*atime["num_frames"])
    badge0= badge0[['Fullattempt_count', 'rate0']]
    badge1 = atime.assign(FrameCount1=atime["count1"]*atime["num_frames"])
    badge1= badge1[['FrameCount1', 'rate1']]
    badge2 = atime.assign(FrameCount2=atime["count2"]*atime["num_frames"])
    badge2= badge2[['FrameCount2', 'rate2']]
    badge3 = atime.assign(FrameCount3=atime["count3"]*atime["num_frames"])
    badge3= badge3[['FrameCount3', 'rate3']]
    badge=[badge0,badge1,badge2,badge3]
    attemp_time = pd.concat(badge,axis=1)
    return(attemp_time)
# attempt_timestamped=attempt_timestamp(time_conv)


### fail
def cal_failure(a,b):
    A = a[['Fullattempt_count','attempt_rates']]
    S = b[['FullSuccess_count','successful_rates']]
    A.columns=['Fullattempt_count','rates']
    S.columns=['FullSuccess_count','rates']
    fail= pd.merge(A, S,how='outer')
    fail = fail.fillna(0)
    fail["failed_counts"] = fail["Fullattempt_count"]-fail["FullSuccess_count"]
    fail = fail[['rates','failed_counts']]
    fail["group"] = fail['rates'].astype(str).str.slice(stop=-1)
    fail["offset"]= fail['rates'].astype(str).str.slice(start=-1)
    fail = fail.replace("", 0)
    fail["group"] = fail['group'].astype(str)
    fail["offset"] = fail['offset'].astype(str)
    fail=fail.loc[fail['failed_counts'] > 0]
    fail=fail[["failed_counts","rates","group","offset"]]
    return(fail)
fail = cal_failure(attempt_check,FullSuccess)
### Success attempt probability
def suc_prob(s):
    attempt_p = attempt_check
    attempt_p.columns=["Fullattempt_count","rates","group","offset"]
    success_p = FullSuccess
    success_p.columns=["FullSuccess_count","rates","group","offset"]
    Success_probability = pd.merge(attempt_p,success_p,on="rates",how="left")
    Success_probability = Success_probability.replace("", 0)
    Success_probability = Success_probability.fillna(0)
    Success_probability["Success_probability"]= Success_probability["FullSuccess_count"]/Success_probability["Fullattempt_count"]
    Success_probability=Success_probability["Success_probability"].astype(float)

        # Success_probability.to_csv("CleanDataset/SuccesProb.csv")
    return(Success_probability)
sp=suc_prob(attempt_check)
