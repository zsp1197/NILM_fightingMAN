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
from readData.feedState_r2 import getState_r2_list, getStates_list
from Tools import *
from superStates import State_r3


def getDistribitions(ps,redd_hdf5_path='/home/uftp/hubei/30xusuqian.h5',center_path='/home/uftp/hubei/ori/xusuqian',load=False):

    # 数据读入
    # redd_hdf5_path = '/home/uftp/hubei/30xusuqian.h5'
    # datastore=Data_store(redd_hdf5_path='/home/uftp/hubei/30xusuqian.h5')
    datastore = Data_store(redd_hdf5_path=redd_hdf5_path)
    # 读取类中心
    clustering = Clustering(redd_hdf5_path)
    clustering.getCenterDict(center_path)
    # 获取空开总数据
    # ps = clustering.data_store.get_instance_ps(appliance_name='meter', instance='1')
    # 获取空开类中心（state_r3）
    # centers_list=clustering.deal_with_ps(ps=ps,not_deal_off=False)
    # centers_list=clustering.deal_with_ps_b(ps=ps,not_deal_off=False)
    # centers_list.append(0)
    # centers_list = [1310.8869965248609, 1576.0193551020407, 1756.5507647887323, 2228.0983558139533, 2851.1088421052636,
    #                 0]
    # print(centers_list)
    # description=clustering.ps2description(ps=ps,centers=centers_list)
    # print(description)
    # kmeans = KMeans(n_clusters=len(centers_list), random_state=0)
    # centers_array = np.array([[center] for center in centers_list]).reshape(-1, 1)
    # kmeans.cluster_centers_ = centers_array
    # 获取原始state_list
    thepath = center_path
    states_list = getStates_list(thepath=thepath)
    # 提取概率分布并保存为dict
    thedict=clustering.deal_all_instance()
    print(thedict)
    # 将改dict保存在硬盘，省得以后每次都要提取
    #TODO 为了加快运行速度，此处改为从硬盘上读取分布
    serialize_object(thedict,'allappliancesdict')
    # 在硬盘上读取这个dict
    # thedict = deserialize_object('allappliancesdict')
    # 调整states_list，加入distribution
    for state in states_list:
        state.thedict = thedict
        state.feed2distribution()
    return 1, states_list

# getDistribitions()