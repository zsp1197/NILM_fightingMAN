# Created by zhai at 2018/1/21
from unittest import TestCase
import pandas as pd

# Email: zsp1197@163.com
from BeeTools import aggregate_with_resample
from Data_store import Data_store
from preprocessing import median_filter
import matplotlib.pyplot as plt


class TestMedian_filter(TestCase):

    # datastore = Data_store(redd_hdf5_path='/home/uftp/hubei/30xusuqian.h5')
    datastore = Data_store(redd_hdf5_path='D:\SJTU\湖北项目\数据\h5s/30xusuqian.h5')
    pss = []
    datarange = [pd.Timestamp('2017-12-15 10:00:00'), pd.Timestamp('2017-12-15 12:00:00')]
    for app in datastore.appliance_names:
        pss.append(datastore.get_instance_ps(appliance_name=app, instance='1').loc[datarange[0]: datarange[-1]])
    ps = aggregate_with_resample(pss)
    def test_median_filter(self):
        ps=self.ps
        ps.plot()
        ps=median_filter(ps=ps)
        ps.plot()
        plt.show()
