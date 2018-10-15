import pandas as pd
import numpy as np
import os


fpath = './data/wuhan/'
hauses = ['zhouqi/', 'xusuqian/', 'xiayurong/']
hauses_name = {'zhouqi/':'周琪', 'xusuqian/':'徐素倩', 'xiayurong/':'夏玉蓉'}

def merge(app_time):
    apps = set(app_time.index)
    merged_df = []
    for app in apps:
        if not isinstance(app_time.loc[app, 'interval'], pd.Series):
            merged_df.append(pd.DataFrame(index=[app], data=[list(app_time.loc[app, 'interval'])], columns=['start', 'end']))
            continue
        merged_interval = []
        start = app_time.loc[app, 'interval'].iloc[0][0]
        end = app_time.loc[app, 'interval'].iloc[0][1]
        for interval in app_time.loc[app, 'interval']:
            if interval[0] > end + pd.Timedelta('1h10m'):
                merged_interval.append((start, end))
                start = interval[0]
            end = interval[1]
        merged_interval.append((start, app_time.loc[app, 'interval'].iloc[-1][1]))
        merged_df.append(pd.DataFrame(index=[app] * len(merged_interval),
                                      data=merged_interval, columns=['start', 'end']))
    if len(merged_df) > 0:
        merged_df = pd.concat(merged_df)
    else:
        merged_df = pd.DataFrame()
    return merged_df



for hause in hauses:
    appliances = []
    app_time_dict = pd.DataFrame(columns=['start', 'interval', 'file'])
    app_power_dict = {}
    files = os.listdir(fpath + hause)
    for file in files:
        df = pd.read_excel(fpath + hause + file, header=0, index_col=3)  # 3rd column is time stamp
        df.index = pd.to_datetime(df.index)
        if df.ix[1,'楼层名称'] != hauses_name[hause]:
            print(df.ix[1,'楼层名称'])
            print('Wrong file %s in %s path' % (file, hause))
            exit(0)
        appliance_id = df.ix[1,'插座编号']
        df = df['正向有功功率(W)']
        if appliance_id not in appliances:
            appliances.append(appliance_id)
            app_time_dict = app_time_dict.append(
                pd.DataFrame({'start':[df.index[-1]], 'interval':[(df.index[-1], df.index[0])],
                              'file':[file]}, index=[appliance_id]))
            app_power_dict[appliance_id] = df
        else:
            if (df.index[-1], df.index[0]) in list(app_time_dict.loc[appliance_id, 'interval']):
                print('duplicate file %s in %s path' % (file, hause))
            else:
                app_time_dict = app_time_dict.append(
                    pd.DataFrame({'start':[df.index[-1]], 'interval': [(df.index[-1], df.index[0])],
                                  'file': [file]}, index=[appliance_id]))
                app_power_dict[appliance_id] = pd.concat([app_power_dict[appliance_id], df])
        for key,ps in app_power_dict.items():
            ps.sort_index(inplace=True)
        app_time_dict = app_time_dict.sort_values('start')

    print(hause)
    print(app_time_dict)
    print(merge(app_time_dict))
    # print(app_power_dict)

