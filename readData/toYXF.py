# Created by zhai at 2018/1/18
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
from readData.feedState_r2 import getState_r2_list, getStates_list
from superStates import State_r3
import pandas as pd
from BeeTools import aggregate_with_resample
import itertools
import datetime
import Tools

#select total power data in a period
datastore = Data_store(redd_hdf5_path='/home/uftp/hubei/30xusuqian.h5')
pss = []
datarange = [pd.Timestamp('2017-12-15 00:00:00'), pd.Timestamp('2017-12-15 22:00:00')]

appliance_consumtion={}
for app in datastore.appliance_names:
    if(app in ['meter',]): continue
    # if(app in ['meter','TVbox']): continue
    theps=datastore.get_instance_ps(appliance_name=app, instance='1').loc[datarange[0]: datarange[-1]]
    pss.append(theps)
    appliance_consumtion[app]=Tools.ps_consumption(theps=theps)
ps = aggregate_with_resample(pss)
del pss

# 获得states_list
from readData.getdistributions import getDistribitions

centers_list, states_list=getDistribitions(ps=ps)

# 由states_list来生成BeeDescription
from readData.feedState_r2 import getState_r2_list

state_r2_list = getState_r2_list(states_list=states_list)
state_r2_values = np.array([i.value for i in state_r2_list]).reshape(-1, 1)
# print(state_r2_values)

kmeans = KMeans(n_clusters=len(centers_list), random_state=0)
centers_array = np.array([[center] for center in centers_list]).reshape(-1, 1)
kmeans.cluster_centers_ = centers_array
label_idxs = kmeans.predict(state_r2_values)
# print(kmeans.transform(state_r2_values))
# 获得state_r3集成的list，按照centers_list中的顺序集成
state_r3_list = []
for center_idx, center in enumerate(centers_list):
    state_r3 = State_r3(value=center)
    mems_idx = list(np.where(label_idxs == center_idx)[0])
    r3_state_r2_list = [state_r2_list[state_r2_idx] for state_r2_idx in mems_idx]
    state_r3.set_state_r2_list(r3_state_r2_list)
    state_r3_list.append(state_r3)





bees = BeeDescription(ps=ps, state_r3_list=state_r3_list)
operating_list = bees.get_operating_list()
bees.set_States_list(states_list=states_list)
bees.set_State_r2_list(state_r2_list)
r3list = bees.get_operating_list()[:2]
print('length r3 list:', len(r3list))
combination, timelist = bees.get_superstate_combination(r3list)
print('length combination:', len(combination))
max = 0
opt_r2 = None
time_consume=[]
starttime = datetime.datetime.now()
for r2 in combination:
    app_opperationg_mode = bees.one_superstate_dict(r2, timelist)
    prob = bees.get_probability(app_opperationg_mode)
    if max < prob:
        max = prob
        opt_r2 = r2
        print(prob)
endtime = datetime.datetime.now()
delta_time=float((endtime - starttime).seconds)
print('平均时长 '+str(delta_time/len(combination))+'s')
print('总时长 '+str(delta_time)+'s')


infer_result=Infer_result(state_r2_tuple=opt_r2,time_list=timelist)
infer_result.getApplianceConsumption()
print(appliance_consumtion)
print(opt_r2)