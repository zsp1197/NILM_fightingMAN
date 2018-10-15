# Created by zhai at 2018/1/16
# Email: zsp1197@163.com
from BeeDescription import BeeDescription
from Clustering import Clustering
from Data_store import Data_store
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np
from readData.feedState_r2 import getState_r2_list, getStates_list
from superStates import State_r3

# datastore=Data_store(redd_hdf5_path='/home/uftp/hubei/30xusuqian.h5')

datastore = Data_store(redd_hdf5_path='/home/uftp/hubei/30xusuqian.h5')
ps = datastore.get_instance_ps(appliance_name='meter', instance='1')
clustering = Clustering()
# centers_list=clustering.deal_with_ps(ps=ps,not_deal_off=False)
# centers_list.append(0)

centers_list = [1310.8869965248609, 1576.0193551020407, 1756.5507647887323, 2228.0983558139533, 2851.1088421052636, 0]
print(centers_list)
# description=clustering.ps2description(ps=ps,centers=centers_list)
# print(description)
kmeans = KMeans(n_clusters=len(centers_list), random_state=0)
centers_array = np.array([[center] for center in centers_list]).reshape(-1, 1)
kmeans.cluster_centers_ = centers_array

thepath = '/home/uftp/hubei/ori/xusuqian'
states_list = getStates_list(thepath=thepath)



# 又states_list来生成BeeDescription
state_r2_list = getState_r2_list(states_list=states_list)
state_r2_values = np.array([i.value for i in state_r2_list]).reshape(-1, 1)
# print(state_r2_values)
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
print()
