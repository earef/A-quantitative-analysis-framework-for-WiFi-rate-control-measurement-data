# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 16:29:37 2022

@author: pawarsp
"""

import linecache
import pandas as pd

def add_supp_rates(group_ind, group_info, supp_rates):
    if group_ind not in supp_rates:
        supp_rates.update({group_ind: group_info})

    return supp_rates

def parse_group_info(fields):
    """
    Obtain maximum offset for a given MCS rate group available for an AP.

    Parameters
    ----------
    fields : list
        Fields obtained by spliting a data line received from the AP
        over the Rate Control API.

    Returns
    -------
    group_idx : str
        Index of MCS rate group.
    max_offset : str
        Maximum allowable offset - determines which rates are available
        in the group for the AP.

    """
    fields = list(filter(None, fields))
    group_ind = fields[3]

    airtimes_hex = fields[9:]
    rate_offsets = [str(ii) for ii in range(len(airtimes_hex))]
    rate_inds = list(map(lambda jj: group_ind + jj, rate_offsets))
    airtimes_ns = [int(ii, 16) for ii in airtimes_hex]

    group_info = {
        "rate_inds": rate_inds,
        "airtimes_ns": airtimes_ns,
        "type": fields[5],
        "nss": fields[6],
        "bandwidth": fields[7],
        "guard_interval": fields[8],
    }

    return group_ind, group_info


def sta_supp_rates(fields, supp_rates_ap):
    supp_rates_sta = []
    mcs_groups = fields[7:]
    mac = fields[4]
    for ii, group_ind in enumerate(supp_rates_ap.keys()):
        mask = int(mcs_groups[ii], 16)
        for jj in range(10):
            if mask & (1 << jj):
                supp_rates_sta.append(f"{group_ind}{jj}")

    return {mac: supp_rates_sta}

#%%
filename_grp = "22.csv"

supp_rates_ap = {}
supp_rates_stas = {}
num_lines = sum(1 for line in open(filename_grp, mode="r"))

for ii in range(1,num_lines+1):
    line = linecache.getline(filename_grp, ii).strip("\n")
    fields = line.split(";")
    if len(fields) > 2:
        if fields[2] == "group":
            group_ind, group_info = parse_group_info(fields)
            supp_rates_ap = add_supp_rates(group_ind, group_info, supp_rates_ap)
        elif fields[2] == "sta" and fields[3] in ["add", "dump"]:
            supp_rates_stas.update(sta_supp_rates(fields, supp_rates_ap))
new = pd.DataFrame.from_dict(supp_rates_stas,orient='index')
# df = new.transpose()

rate_capability=new.count(axis='columns')
print(new)
new.to_csv("AvailableRatesForEachClient-22.csv")
