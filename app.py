#!/usr/bin/env python

import matplotlib

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import itertools
import numpy as np


fig, ax = plt.subplots()
ax.set_yscale('log')

path = 'csv'
all_files = glob.glob(os.path.join(path, "*.log"))

df_from_each_file = (pd.read_csv(f) for f in all_files)
df_from_each_file = list((df[df['Ip'] != '???'] for df in df_from_each_file))
df_first_hops = pd.concat(
    (df.iloc[:1].loc[:,['Start_Time', 'Avg']] for df in df_from_each_file),
    ignore_index=True
)
df_first_hops['Start_Time'] = pd.to_datetime(df_first_hops['Start_Time'],unit='s')
df_first_hops.set_index('Start_Time', inplace=True)
df_first_hops.columns = ['Router']
df_first_hops.plot(ax=ax)

df_first_external_hops = pd.concat(
    (df.iloc[1:2].loc[:,['Start_Time', 'Avg']] for df in df_from_each_file),
    ignore_index=True
)
df_first_external_hops['Start_Time'] = pd.to_datetime(df_first_external_hops['Start_Time'],unit='s')
df_first_external_hops.set_index('Start_Time', inplace=True)
df_first_external_hops.columns = ['Plus Net']
df_first_external_hops.plot(ax=ax)

df_destination_hops = pd.concat(
    (df.iloc[-1:].loc[:,['Start_Time', 'Avg']] for df in df_from_each_file),
    ignore_index=True
)
df_destination_hops['Start_Time'] = pd.to_datetime(df_destination_hops['Start_Time'],unit='s')
df_destination_hops.set_index('Start_Time', inplace=True)
df_destination_hops.columns = ['Google']
df_destination_hops.plot(ax=ax)

ylabs = [pow(10,i) for i in range(0,5)]
ax.set_yticklabels(ylabs)
ax.set_yticks(ylabs)

fig.savefig("netstats.png")

'''
df_last_hop = (df.iloc[-1:].loc[:,['Start_Time', 'Avg']] for df in df_from_each_file)
df = pd.concat(df_last_hop, ignore_index=True)
df['Start_Time'] = pd.to_datetime(df['Start_Time'],unit='s')
df.set_index('Start_Time', inplace=True)

df.plot(ax=ax)
'''