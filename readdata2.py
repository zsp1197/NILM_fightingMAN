import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

fpath = './data/wuhan/'
houses = ['zhouqi/', 'xusuqian/', 'xiayurong/']
houses_name = {'zhouqi/':'周琪', 'xusuqian/':'徐素倩', 'xiayurong/':'夏玉蓉'}


def up_sample_ps(ps: pd.Series, freq: str = 'S'):
    '''
    the data maybe compressed, pro-long the data with a fixed sample period
    :param ps:pd.Series(index=datatimeindex,data=power_read)
    :return: pd.Seires
    '''
    index = pd.to_datetime(ps.index)
    longindex = pd.date_range(start=min(index), end=max(index), freq=freq)
    pdf = pd.DataFrame(index=longindex, columns=['0'])
    pdf.ix[index, 0] = ps.values.tolist()
    pdf = pdf.fillna(method='pad')
    return pdf['0']


for house in houses:
    fout = pd.HDFStore('./data/house%s.h5' % house, 'w')
    appliances = []
    app_time_dict = pd.DataFrame(columns=['start', 'interval', 'file'])
    app_power_dict = {}
    files = os.listdir(fpath + house)
    for file in files:
        df = pd.read_excel(fpath + house + file, header=0, index_col=3)  # 3rd column is time stamp
        df.index = pd.to_datetime(df.index)
        if df.ix[1,'楼层名称'] != houses_name[house]:
            print(df.ix[1,'楼层名称'])
            print('Wrong file %s in %s path' % (file, house))
            exit(0)
        appliance_id = file.split('_')[1].split('.')[0]
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
        # print(hause, key)
        # plt.plot(ps)
        # plt.title(key)
        # plt.show()
        # print(max(ps))
    print(appliances)
    app_time_dict = app_time_dict.sort_values('start')
    print(hause)
    print(app_time_dict)

    merged_df = pd.DataFrame()
    min_time = max(app_time_dict['start'])
    max_time = pd.to_datetime('2017-12-13 12:00:00')
    for key, ps in app_power_dict.items():
        print(key)

        tempt = up_sample_ps(ps).loc[min_time:max_time].copy()
        merged_df[key] = tempt
    merged_df.to_csv(fpath + hause + 'total.csv')
    print(hause,' finished')
    # print(app_power_dict)

