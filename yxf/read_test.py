# Created by zhai at 2018/1/11
# Email: zsp1197@163.com
import pandas as pd
import matplotlib.pyplot as plt
import os
from Event_detection import Event_detection, Parameters
from up_sample_ps import up_sample_ps
from scipy.signal import medfilt

fpath='D:\SJTU\湖北项目\数据\yxf/'
houses = ['xusuqian/']
houses_name = {'zhouqi/': '周琪', 'xusuqian/': '徐素倩', 'xiayurong/': '夏玉蓉'}

for house in houses:
    print(house)
    appliances = []
    files = os.listdir(fpath + house)
    for file in files:
        print(file.split('_'[0] + file.split('_')[1]))
        df = pd.read_excel(fpath + house + file, header=0, index_col=3)
        df.index = pd.to_datetime(df.index)
        ps=df['正向有功功率(W)']
        ps.sort_index(inplace=True)
        print('up_sampling')
        ps = up_sample_ps(ps)
        print('resampling')
        # ps.resample('30s')
        resample = ps.index[::30]
        ps = ps.loc[resample]
        ps.plot()
        ps = pd.Series(index=ps.index, data=medfilt(ps.values, 5))
        ps = pd.Series(index=ps.index, data=medfilt(ps.values, 5))
        ps = pd.Series(index=ps.index, data=medfilt(ps.values, 5))
        ps = pd.Series(index=ps.index, data=medfilt(ps.values, 5))
        print('plotting')
        ps.plot()
        plt.show()
        print('Event Detecting')
        detector = Event_detection(ps, Parameters())
        result = detector.delta_based()
        result=[(mini_result[0], mini_result[1], mini_result[1] - mini_result[0], mini_result[2]) for mini_result in result]
        for line in result:
            print(line)
