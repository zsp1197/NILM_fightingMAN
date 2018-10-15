# Created by zhai at 2018/1/16
# Email: zsp1197@163.com
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from Appliance_class import Appliance_state
from Tools import *
import os
def getUserStates(thepath, unknown=True):
    df = pd.read_csv(os.path.join(thepath, 'states.txt'), header=None, index_col=0)
    appliance_names = list(df.index)
    if not unknown:
        df.drop('unknown_1')
    # instance
    states = []
    for appliance_name in appliance_names:
        appliance_type,instance=appliance_name.split('_')
        states_series = df.loc[appliance_name][1:]
        states_np=states_series.values
        states_np=states_np.astype(np.float64)
        states_np = states_np[~np.isnan(states_np)]
        states.append(list(states_np))
    return dict(zip(appliance_names,states))

def feed_states(states_dict):
    result=[]
    for name,centers in states_dict.items():
        appliance_name,instance=name.split('_')
        for center in centers:
            if(center==0): continue
            result.append(Appliance_state(appliance_type=appliance_name,instance=instance,state=center,PROPERTIES=None,thedict=None,dataset='xusuqian'))
    return result

# thepath='D:\SJTU\湖北项目\数据/ori/xusuqian'
# states_dict=getUserStates(thepath=thepath)
# states_list=feed_states(states_dict)
# print(states_list)
#
