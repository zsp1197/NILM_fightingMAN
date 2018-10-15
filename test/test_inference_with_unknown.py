# Created by zhai at 2018/1/22
from unittest import TestCase
from BeeDescription import BeeDescription
from Clustering import Clustering
from Data_store import Data_store
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

from Infer_result import Infer_result
from Inference import Inference
from Parameters import Parameters
from Performance import Performance
from preprocessing import median_filter
from readData.feedState_r2 import getState_r2_list, getStates_list
from superStates import State_r3
import pandas as pd
from BeeTools import aggregate_with_resample
import itertools
import datetime
import Tools
from Clustering import Clustering
# Email: zsp1197@163.com
class TestInference(TestCase):
    def setUp(self):
        self.home = 'xusuqian'
        self.datastore = Data_store(redd_hdf5_path='/home/uftp/hubei/30%s.h5' % self.home)
        self.datarange = [pd.Timestamp('2017-12-2 00:00:00'), pd.Timestamp('2018-1-1 00:00:00')]
        print('')
    def setUp_dynamic(self):
        # select total power data in a period
        # datastore = Data_store(redd_hdf5_path='D:\SJTU\湖北项目\数据\h5s/30xiayurong.h5')
        # datastore = Data_store(redd_hdf5_path='D:\SJTU\湖北项目\数据\h5s/30xusuqian.h5')
        # datastore = Data_store(redd_hdf5_path='/home/uftp/hubei/30xusuqian.h5')
        # datastore = Data_store(redd_hdf5_path='/home/uftp/hubei/30fake.h5')
        pss = []
        # datarange = [pd.Timestamp('2017-12-15 10:00:00'), pd.Timestamp('2017-12-15 12:00:00')]
        appliance_truth={}
        appliance_consumtion = {}
        for app in self.datastore.appliance_names:
            if (app in ['meter', 'TVbox','TV']) and self.home == 'xusuqian':
                if app == 'meter':
                    totalpower = self.datastore.get_instance_ps(appliance_name=app, instance='1').loc[self.datarange[0]: self.datarange[-1]]
                continue
            theps = self.datastore.get_instance_ps(appliance_name=app, instance='1').loc[self.datarange[0]: self.datarange[-1]]
            appliance_truth[app]=theps
            pss.append(theps)
            appliance_consumtion[app] = Tools.ps_consumption(theps=theps)
            # if(app=='lamp'):
            #     print()
        knownps = aggregate_with_resample(pss)
        appliance_truth['unknown'] = totalpower - knownps
        appliance_consumtion['unknown'] =Tools.ps_consumption(theps=appliance_truth['unknown'])
        ps = totalpower
        cluster = Clustering()
        print('miaomiaomiao?')
        del pss
        # ps.plot()
        # ps=median_filter(ps=ps)
        # ps.plot()
        # plt.show()
        # 获得states_list
        from readData.getdistributions import getDistribitions
        self.appliance_truth=appliance_truth
        # centers_list, states_list = getDistribitions(ps=ps, redd_hdf5_path='D:\SJTU\湖北项目\数据\h5s/30xusuqian.h5',
        #                                              center_path='D:\SJTU\湖北项目\数据\ori\\xusuqian')
        # centers_list, states_list = getDistribitions(ps=ps)
        centers_list, states_list = getDistribitions(ps=ps, redd_hdf5_path='/home/uftp/hubei/30%s.h5' % self.home,
                                                     center_path='/home/uftp/hubei/ori/%s' % self.home, load=False)
        self.appliance_consumtion = appliance_consumtion
        self.inference = Inference(total_ps=ps, states_list=states_list)

    def test_infer_operating_list_to_chunks(self):
        self.setUp_dynamic()
        infer_result = self.inference.infer_operating_list_to_chunks_dynamic()
        infer_result.get_estimated_ps_dict()
        print(self.appliance_consumtion)
        performance = Performance(infer_result=infer_result, appliance_truth=self.appliance_truth)
        error = performance.dissagga_metric()
        print(1 - error)
        print(Parameters())
        print()

    def test_infer_operating_list_to_chunks_static(self):
        import staticGO
        appliance_truth, ps, states_list, centers, state_r3_list,appliance_consumtion=staticGO.staticGo(self.datastore,self.datarange)
        self.inference = Inference(total_ps=ps, states_list=states_list,centers_list=centers)
        infer_result = self.inference.infer_operating_list_to_chunks_static(state_r3_list=state_r3_list)
        infer_result.get_estimated_ps_dict()
        print(appliance_consumtion)
        performance = Performance(infer_result=infer_result, appliance_truth=appliance_truth)
        df1, df2 =performance.dissagga_metric2()
        error = performance.dissagga_metric()
        print(1 - error)
        print(self.inference.para)
        print()

# t=TestInference()
# t.setUp()
# t.test_infer_operating_list_to_chunks()