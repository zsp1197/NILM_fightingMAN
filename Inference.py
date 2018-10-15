# Created by zhai at 2018/1/22
# Email: zsp1197@163.com
from BeeDescription import BeeDescription
from Clustering import Clustering
from Data_store import Data_store
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

from Infer_result import Infer_result
from Parameters import Parameters
from readData.feedState_r2 import getState_r2_list, getStates_list
from superStates import State_r3, State_r2
import pandas as pd
from BeeTools import aggregate_with_resample
import itertools
import datetime
import Tools


class Inference(object):
    @Tools.check_func_input_output_type_static
    def __init__(self, total_ps: pd.Series, states_list: list,centers_list:list=None):
        self.total_ps = total_ps
        self.states_list = states_list
        if(centers_list is None):
            self.centers_list = self.getCenters(ps=total_ps)
        else:
            self.centers_list=centers_list
        print('centers: ')
        print(self.centers_list)
        self.para=Parameters()

    def getCenters(self, ps):
        clustering = Clustering()
        # centers_list = clustering.deal_with_ps(ps=ps, not_deal_off=False)
        centers_list = clustering.deal_with_ps_b(ps=ps, not_deal_off=False)
        centers_list.append(0)
        return centers_list

    def getState_r3_list(self):
        # 由states_list来生成BeeDescription
        from readData.feedState_r2 import getState_r2_list

        self.state_r2_list = getState_r2_list(states_list=self.states_list)
        state_r2_values = np.array([i.value for i in self.state_r2_list]).reshape(-1, 1)
        # print(state_r2_values)

        kmeans = KMeans(n_clusters=len(self.centers_list), random_state=0)
        centers_array = np.array([[center] for center in self.centers_list]).reshape(-1, 1)
        kmeans.cluster_centers_ = centers_array
        label_idxs = kmeans.predict(state_r2_values)
        # print(kmeans.transform(state_r2_values))
        # 获得state_r3集成的list，按照centers_list中的顺序集成
        state_r3_list = []
        for center_idx, center in enumerate(self.centers_list):
            state_r3 = State_r3(value=center)
            mems_idx = list(np.where(label_idxs == center_idx)[0])
            r3_state_r2_list = [self.state_r2_list[state_r2_idx] for state_r2_idx in mems_idx]
            if(len(r3_state_r2_list)==0): continue
            state_r3_list.append(state_r3)
            state_r3.set_state_r2_list(r3_state_r2_list)
        return state_r3_list

    def getBeeDescription(self):
        '''
        如果是动态的，则self.state_r3_list并未创建，如果是静态的，则已经指定了self.state_r3_list
        :return:
        '''
        dynamic = False
        try:
            self.state_r3_list
            print('静态')
        except:
            print('动态')
            self.state_r3_list = self.getState_r3_list()
            dynamic = True

        bees = BeeDescription(ps=self.total_ps, state_r3_list=self.state_r3_list,para=self.para)
        bees.set_States_list(states_list=self.states_list)
        if dynamic:
            bees.set_State_r2_list(self.state_r2_list)
        self.bees = bees

    def getOperatingList(self):
        '''
        获取整个时间序列描述
        :return: operating_list: list of tuples (starttime(pd.timestamp),endtime(pd.timestamp), cluster center value,state_r3,pd.Timedelta)
        '''
        self.getBeeDescription()
        self.operating_list = self.bees.get_operating_list()

    def infer_operating_list_to_chunks_dynamic(self):
        '''
        首先将operating_list按照数字n分为多个list，在对每一个调用self.getOpt_r2_by_chunk
        :return: infer_result
        '''
        try:
            self.operating_list
        except:
            print('no operating_list, find one!')
            self.getOperatingList()
        chunks_list = Tools.split_list_to_chunks(self.operating_list, self.para.n_order)
        long_opt_t2 = []
        timelist = []
        for chunk in chunks_list:
            opt_r2, thetimelist = self.getOpt_r2_by_chunk(chunk)
            long_opt_t2 += opt_r2
            timelist += thetimelist
        infer_result = Infer_result(state_r2_tuple=long_opt_t2, time_list=timelist)
        infer_result.getApplianceConsumption()
        return infer_result

    def infer_operating_list_to_chunks_static(self,state_r3_list):
        '''
        除了state_r3_list并非自动生成，剩下的都一样
        :return:
        '''
        self.state_r3_list=state_r3_list
        return self.infer_operating_list_to_chunks_dynamic()
        # self.state_r2_list=self.getState_r2_list_by_r3(state_r3_list)

    def getOpt_r2_by_chunk(self, chunk):
        '''

        :param chunk: [(starttime(pd.timestamp),endtime(pd.timestamp), cluster center value,state_r3,pd.Timedelta)]
        :return:opt_r2 [state_r2...]
        :return:timelist [(start_1, end_1), ......]
        '''
        combination, timelist = self.bees.get_superstate_combination(chunk)
        print('length combination:', len(combination))
        if len(combination) == 0:
            null_State_r2=State_r2(states_tuple=None)
            return [null_State_r2 for i in chunk], timelist
        max = -1
        opt_r2 = None
        for r2 in combination:
            app_opperationg_mode = self.bees.one_superstate_dict(r2, timelist)
            prob = self.bees.get_probability(app_opperationg_mode)
            if max < prob:
                max = prob
                opt_r2 = r2
        if(opt_r2 is None):
            print()
        return opt_r2, timelist