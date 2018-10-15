# Created by zhai at 2018/1/17
# Email: zsp1197@163.com
import itertools
from copy import deepcopy

import pandas as pd
import numpy as np

import Tools
from Clustering import Clustering
from Parameters import Parameters
from superStates import State_r3


class BeeDescription():
    def __init__(self, ps, state_r3_list,para=Parameters()):
        self.para=para
        self.state_r3_list = state_r3_list
        self.centers_list = [state_r3.value for state_r3 in self.state_r3_list]
        self.clustering = Clustering()
        # list of tuples (starttime(pd.timestamp),endtime(pd.timestamp), cluster center value)
        self.description = self.clustering.ps2description(ps=ps, centers=self.centers_list)

    def description_to_states_r3(self, description):
        '''

        :param description: list of tuples (starttime(pd.timestamp),endtime(pd.timestamp), cluster center value)
        :return: list of tuples (starttime(pd.timestamp),endtime(pd.timestamp), cluster center value,state_r3,pd.Timedelta)
        '''
        result = []
        for description_mem in description:
            temp = list(description_mem)
            temp.append(self.state_r3_list[self.centers_list.index(description_mem[2])])
            temp.append(description_mem[1] - description_mem[0])
            result.append(tuple(temp))
        return result

    def states_r3_list(self):
        '''
        中间经历的了滤波
        改变state_r3，若是时间少于阈值，就认为是all_work_state_r3，即所有电器都可能开启
        :return: list of tuples (starttime(pd.timestamp),endtime(pd.timestamp), cluster center value,state_r3,pd.Timedelta)
        '''
        # see result in description_to_states_r3
        states_r3_description_list = self.description_to_states_r3(self.description)
        all_work_state_r3 = State_r3(value='all work')
        refined_states_r3_description_list = self.filtering(states_r3_description_list, all_work_state_r3)
        return refined_states_r3_description_list

    def filtering(self, states_r3_description_list, all_work_state_r3):
        '''
        滤波，时间短的认为是spike，用all_work_state_r3代替
        :param states_r3_description_list:
        :param all_work_state_r3:
        :return:
        '''
        result = states_r3_description_list
        for i, states_r3_description in enumerate(states_r3_description_list):
            if (states_r3_description[4] < pd.Timedelta('70S')):
                temp = list(states_r3_description)
                temp[3] = all_work_state_r3
                result[i] = tuple(temp)
        return result

    def get_operating_list(self):
        '''
        滤波的进一步处理，如果检测到all_work_state_r3，则认为与后面的状态相同
        :return: list of tuples (starttime(pd.timestamp),endtime(pd.timestamp), cluster center value,state_r3,pd.Timedelta)
        '''
        refined_states_r3_description_list = self.states_r3_list()
        result_no_time_considered = deepcopy(refined_states_r3_description_list)
        for i, mem in enumerate(refined_states_r3_description_list):
            idx=len(refined_states_r3_description_list)-1-i
            if (refined_states_r3_description_list[idx][3].value == 'all work'):
                try:
                    temp=list(deepcopy(result_no_time_considered[idx]))
                    temp[2]=result_no_time_considered[idx+1][2]
                    temp[3]=result_no_time_considered[idx+1][3]
                    result_no_time_considered[idx] = tuple(temp)
                    # result_no_time_considered[idx] = result_no_time_considered[idx+1]
                except Exception as e:
                    print(e)
                    # raise LookupError('第一个状态也是被滤波状态，不管了')
        # 根据时间减少state_r2数量，注意，这里state_r2节能传的是地址，需要进一步检验，免得全都是链接一个东西！
        result=[]
        for bin in result_no_time_considered:
            temp_state_r3=deepcopy(bin[3])
            time_bin=(bin[0],bin[1],bin[4])
            temp_state_r3.refine_states_r2_by_time(time_bin=time_bin,num_of_r2=self.para.num_of_r2)
            result.append((bin[0],bin[1],bin[2],temp_state_r3,bin[4]))
        # result=result_no_time_considered
        return result

    def set_State_r2_list(self, state_r2_list):
        self.state_r2_list = state_r2_list

    def set_States_list(self, states_list):
        self.states_list = states_list

    def get_superstate_combination(self, list):
        '''

        :param list: list of tuples (starttime(pd.timestamp),endtime(pd.timestamp), cluster center value,state_r3,pd.Timedelta)
        :return: result: [combination list] combination: r2 list [[state_r2...]]
        :return: timelist: timelist: [(start_1, end_1), ......]
        '''
        r2bins = []
        timelist = []
        for item in list:
            timelist.append((item[0], item[1]))
            r2bins.append(tuple(item[3].get_state_r2_list()))
        result = tuple(itertools.product(*r2bins))
        return result, timelist

    def one_superstate_dict(self, combination, timelist):
        """
        :param combination: r2_list [r2_1, r2_2, r2_3....]
        :param timelist: [(start_1, end_1), ......]
        :return: {app_state_id:[(start_1, end_1), ....]}
        """
        result = {}
        for timeid, superstate in enumerate(combination):
            if superstate.states_tuple == None: continue
            for appstate in superstate.states_tuple:
                if not appstate.id in result.keys():
                    result[appstate.id] = [timelist[timeid]]
                else:
                    if result[appstate.id][-1][-1] == timelist[timeid - 1][-1]:
                        result[appstate.id][-1] = list(result[appstate.id][-1])
                        result[appstate.id][-1][-1] = timelist[timeid][-1]
                        result[appstate.id][-1] = tuple(result[appstate.id][-1])
                    else:
                        result[appstate.id].append(timelist[timeid])
        return result

    def get_prior_distri(self, app_id, app_dict):
        return 1 / len(app_dict)

    def get_app_prob(self, app_id, app_dict):
        ontime = pd.Timedelta('0s')
        for period in app_dict[app_id]:
            ontime += period[-1] - period[0]
        ontime /= len(app_dict[app_id])
        app_state = self.getState_by_id(app_id)
        if app_state.distributions == None: return None
        tempt = app_state.distributions['delta_time'].cdf(ontime.seconds / 60)
        return 1 - tempt


    def get_probability(self, app_dict):
        objval = 0
        count = 0
        for key in app_dict:
            score = self.get_app_prob(key, app_dict)
            weight = self.get_prior_distri(key, app_dict)
            if score != None:
                objval += weight * score
                count += 1
        if count == 0: return 0
        return objval

    @Tools.check_func_input_output_type_static
    def getState_by_id(self, id: str):
        for state in self.states_list:
            if (id == state.id):
                return state
        # 找不到那个state
        raise LookupError