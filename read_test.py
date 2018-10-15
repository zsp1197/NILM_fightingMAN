# Created by zhai at 2018/1/11
# Email: zsp1197@163.com
import pandas as pd
import matplotlib.pyplot as plt
import os
# from Event_detection import Event_detection, Parameters
from up_sample_ps import up_sample_ps
from scipy.signal import medfilt

fpath='./data/hubeidata/'
houses = ['zhouqi/', 'xusuqian/', 'xiayurong/']
houses_name = {'zhouqi/':'周琪', 'xusuqian/':'徐素倩', 'xiayurong/':'夏玉蓉'}

# for house in houses:
#     print(house)
#     fout= pd.HDFStore('./data/%s.h5' % house.split('/')[0], 'w')
#     files = os.listdir(fpath + house)
#
#     for file in files:
#         print(file.split('_')[0] + '_' + file.split('_')[1])
#         df = pd.read_excel(fpath + house + file, header=0, index_col=3)
#         df.index = pd.to_datetime(df.index)
#         ps=df['正向有功功率(W)']
#         ps.sort_index(inplace=True)
#
#         print('up_sampling')
#         ps = up_sample_ps(ps)
#         datarange = pd.date_range('2017-12-1', '2018-1-12')
#         for i in range(len(datarange) - 1):
#             # index = ps.index > pd.Timestamp('2017-12-11')
#             daydata = ps.loc[datarange[i]: datarange[i+1]]
#             daydata = daydata[ :-1]
#             print(datarange[i])
#             fout['/series/' + file.split('_')[0] + '/' + file.split('_')[1] + '/%s' % datarange[i].date()] = daydata
#     fout.close()

for house in houses:
    print(house)
    fout = pd.HDFStore('./data/30%s.h5' % house.split('/')[0], 'w')
    files = os.listdir(fpath + house)

    for file in files:
        print(file.split('_')[0] + '_' + file.split('_')[1])
        df = pd.read_excel(fpath + house + file, header=0, index_col=3)
        df.index = pd.to_datetime(df.index)
        ps = df['正向有功功率(W)']
        ps.sort_index(inplace=True)

        print('up_sampling')
        ps = up_sample_ps(ps)
        datarange = pd.date_range('2017-12-1', '2018-1-12')
        for i in range(len(datarange) - 1):
            # index = ps.index > pd.Timestamp('2017-12-11')
            daydata = ps.loc[datarange[i]: datarange[i + 1]]
            daydata = daydata[:-1]
            resample = daydata.index[::30]
            daydata = daydata.loc[resample]
            print(datarange[i])
            fout['/series/' + file.split('_')[0] + '/' + file.split('_')[1] + '/%s' % datarange[
                i].date()] = daydata
    fout.close()


# fin = pd.HDFStore('./data/%s.h5' % houses[1][:-1])
# print('')
#
# for house in houses:
#     print(house)
#     ttdf = pd.DataFrame()
#     files = os.listdir(fpath + house)
#
#     for file in files:
#         print(file.split('_')[0] + '_' + file.split('_')[1])
#         df = pd.read_excel(fpath + house + file, header=0, index_col=3)
#         df.index = pd.to_datetime(df.index)
#         ps=df['正向有功功率(W)']
#         ps.sort_index(inplace=True)
#
#         print('up_sampling')
#         ps = up_sample_ps(ps)
#         datarange = pd.date_range('2017-12-2', '2018-1-10')
#         ps = ps.loc[datarange[0]: datarange[-1]]
#         ttdf[file.split('_')[0] + '_' + file.split('_')[1]] = ps
#     ttdf.to_csv('beepower_%s_total.csv' % house[:-1])