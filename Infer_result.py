# Created by zhai at 2018/1/21
# Email: zsp1197@163.com
import Tools
import pandas as pd


class Infer_result():
    def __init__(self, state_r2_tuple, time_list):
        assert len(state_r2_tuple) == len(time_list)
        self.state_r2_tuple = state_r2_tuple
        self.time_list = time_list
        appliance_names = []
        for state_r2 in self.state_r2_tuple:
            if(state_r2.states_tuple is None):
                continue
            for state in state_r2.states_tuple:
                appliance_names.append(state.appliance_type + '_' + state.instance)
        self.appliance_names = Tools.list_move_duplicates(appliance_names)

    # def getStateConsumption(self):
    #     # 获得所有stateid
    #     state_ids=[]
    #     for state in self.state_r2_tuple:
    #         state_ids.append(state.id)
    #     self.state_ids=Tools.list_move_duplicates(state_ids)

    def getApplianceConsumption(self):
        appliance_consumption = {}
        for appliance_name in self.appliance_names:
            appliance_consumption[appliance_name] = 0
        for i, time_tuple in enumerate(self.time_list):
            start_time, end_time = time_tuple
            if(self.state_r2_tuple[i].states_tuple is None): continue
            for j, state in enumerate(self.state_r2_tuple[i].states_tuple):
                appliance_name = state.appliance_type + '_' + state.instance
                appliance_consumption[appliance_name] += state.center_value * Tools.timedelta_2_naive(
                    end_time - start_time, acc='second')
        self.appliance_consumption = appliance_consumption
        print(appliance_consumption)

    def get_estimated_ps_dict(self):
        ps_dict = {}
        for i, time_tuple in enumerate(self.time_list):
            start_time, end_time = time_tuple
            if(self.state_r2_tuple[i].states_tuple is None):
                continue
            for j, state in enumerate(self.state_r2_tuple[i].states_tuple):
                appliance_name = state.appliance_type+ '_' + state.instance
                try:
                    ps_dict[appliance_name] = pd.concat([ps_dict[appliance_name], pd.Series(data=state.center_value,
                                                                                            index=pd.date_range(
                                                                                                start=start_time,
                                                                                                end=end_time, freq='S'))])
                except KeyError:
                    ps_dict[appliance_name] = pd.Series(data=state.center_value,
                                                        index=pd.date_range(start=start_time, end=end_time, freq='s'))
        lastTime = self.time_list[-1][1]
        for key, value in ps_dict.items():
            # ps_dict[key] = pd.concat([value, pd.Series(index=[lastTime], data=[0])])
            ps_dict[key] = ps_dict[key].add(
                pd.Series(data=0, index=pd.date_range(start=self.time_list[0][0], end=self.time_list[-1][1],freq='S')),
                fill_value=0)
        self.ps_dict = ps_dict
