#!/usr/bin/env python

import matplotlib

matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import glob
import datetime

day = datetime.datetime(2017, 11, 19, 0, 0)


fig, ax = plt.subplots()

hours = mdates.HourLocator()   # every hour
hoursFmt = mdates.DateFormatter('%H:%M')

path = 'csv'
all_files = glob.glob(os.path.join(path, "*.log"))

df = pd.concat(
    (pd.read_csv(f) for f in all_files),
    ignore_index=True
)
df = df[df['Ip'] != '???']
df['Start_Time'] = pd.to_datetime(df['Start_Time'],unit='s')

mask = (df['Start_Time'] > day) & \
    (df['Start_Time'] <= day + datetime.timedelta(days=1))
df = df.loc[mask]

df.set_index('Start_Time', inplace=True)
df = df.loc[:,['Avg']]

df_router = df.groupby('Start_Time').nth(0)
df_router.columns = ['Router']
df_router.plot(ax=ax)
df_plusnet = df.groupby('Start_Time').nth(1)
df_plusnet.columns = ['Plusnet']
df_plusnet.plot(ax=ax)
df_google = df.groupby('Start_Time').nth(-1)
df_google.columns = ['Google']
df_google.plot(ax=ax)

plt.title(f'Network Response {day:%d %B %Y}')
plt.ylabel('Response Time (ms)')
plt.xlabel('Time of Day')

ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(hoursFmt)

ylabs = [pow(10, i) for i in range(0, 5)]
ax.set_yscale('log')
ax.set_yticklabels(ylabs)
ax.set_yticks(ylabs)

fig.savefig("netstats.png")
