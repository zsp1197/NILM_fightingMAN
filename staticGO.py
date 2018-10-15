# Created by zhai at 2018/1/23
# Email: zsp1197@163.com
from Clustering import Clustering
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
from readData.getdistributions import getDistribitions
import pandas as pd
from BeeTools import aggregate_with_resample
import itertools
import datetime
import Tools
from superStates import *
from Appliance_class import Appliance_state
from sklearn.neighbors.nearest_centroid import NearestCentroid


def step_clustering(ps, minstep=10):
    clustering = Clustering()
    centers = clustering.deal_with_ps_b(ps=ps)
    centers.sort()
    diff = np.diff(centers)
    if min(diff) < minstep:
        return centers
    else:
        data = ps.values.reshape(-1, 1)
        clustering = KMeans(n_clusters=len(centers) + 1, init='k-means++', n_init=20)
        clustering.fit(data)
        centers = np.copy(clustering.cluster_centers_).reshape(-1)
        centers.sort()
    maxiter = 20
    iternum = 1
    while min(np.diff(centers))> minstep or iternum < maxiter:
        clustering = KMeans(n_clusters=len(centers) + 1, init='k-means++', n_init=20)
        clustering.fit(data)
        centers = np.copy(clustering.cluster_centers_).reshape(-1)
        centers.sort()
        iternum += 1
    return list(centers.reshape(-1))


def staticGo(datastore,datarange, home='xusuqian', unknown=True):
    def r3_get_r2(r3list, label, app_statedict: dict, psdict: dict):
        print('Using history data to extract r2 belonging to r3')
        df = pd.DataFrame(columns=list(psdict.keys()))
        r3combi = {}
        # generating dataframe
        for key, ps in psdict.items():
            app_state = app_statedict[key]
            state_num = len(app_state)
            clf = NearestCentroid()
            clf.fit(np.append([0], np.array([i.center_value for i in app_state])).reshape(-1, 1),
                    np.array(range(state_num + 1)))
            df[key] = clf.predict(ps.values.reshape(-1, 1))
        for idn, r3 in enumerate(r3list):
            idx = label == idn
            tempt = df.iloc[idx]
            combination = set([tuple(i) for i in list(tempt.values)])
            r3combi[idn] = combination
            r2list = []
            state_count = []
            for r2row in combination:
                app_state_tuple = []
                for kk, key in enumerate(df.columns):
                    if r2row[kk] > 0:
                        app_state_tuple.append(app_statedict[key][r2row[kk] - 1])
                if app_state_tuple != []:
                    r2list.append(State_r2(tuple(app_state_tuple)))
                    state_count.append(np.count_nonzero((tempt == np.array(r2row)).all(1)))
                else:
                    r2list.append(State_r2(None))
                    state_count.append(np.count_nonzero((tempt == np.array(r2row)).all(1)))
            r3.set_state_r2_list(r2list, False)
            r3.statecount = state_count
            if (len(r2list) != len(state_count)):
                print()
        print('r2 extracting finished')

    appliance_truth = {}
    appliance_consumtion = {}
    if unknown:
        ps = None
        for app in datastore.appliance_names:
            if (app in ['TVbox', 'TV']) and home == 'xusuqian': continue
            if (app in ['lamp', 'TV']) and home == 'xiayurong': continue
            if (app in ['sterilizer', 'iron', 'kitchen', 'TV']) and home == 'zhouqi': continue
            if (app == 'meter'):
                for key in datastore.keys_dict[app]:
                    meterdata = datastore.get_instance_ps(appliance_name=app,
                                                               instance=key).loc[datarange[0]: datarange[-1]]
                    if ps == None: ps = meterdata
                    else: ps += meterdata

                continue
            for key in datastore.keys_dict[app]:
                theps = datastore.get_instance_ps(appliance_name=app,
                                                       instance=key).loc[datarange[0]: datarange[-1]]
                appliance_truth[app + '_' + key] = theps
                appliance_consumtion[app + '_' + key] = Tools.ps_consumption(theps=theps)
    else:
        pss = []
        for app in datastore.appliance_names:
            if (app in ['TVbox', 'TV']) and home == 'xusuqian': continue
            if (app in ['lamp', 'TV']) and home == 'xiayurong': continue
            if (app in ['sterilizer', 'iron', 'kitchen', 'TV']) and home == 'zhouqi': continue
            if (app in ['meter', 'unknown']): continue
            for key in datastore.keys_dict[app]:
                theps = datastore.get_instance_ps(appliance_name=app,
                                                       instance=key).loc[datarange[0]:datarange[-1]]
                appliance_truth[app + '_' + key] = theps
                appliance_consumtion[app + '_' + key] = Tools.ps_consumption(theps=theps)
                pss.append(theps)
        ps = aggregate_with_resample(pss)
        del pss

    ps_dict = appliance_truth
    print('搞定了ps')

    # ps = median_filter(ps=ps)
    _, states_list = getDistribitions(ps=ps, redd_hdf5_path='/home/uftp/hubei/4test/30%s.h5' % home,
                                      center_path='/home/uftp/hubei/ori/%s' % home, load=False)
    clustering = Clustering()
    centers = clustering.deal_with_ps_b(ps=ps)
    centers = step_clustering(ps)
    print('类中心是：')
    print(centers)

    # centers=Tools.deserialize_object('centers')
    Tools.serialize_object(centers, 'centers')
    state_r3_list = [State_r3(value=center) for center in centers]
    centers_array = np.array([[center] for center in centers]).reshape(-1, 1)
    kmeans = KMeans(n_clusters=len(centers), random_state=0)
    kmeans.cluster_centers_ = centers_array
    toLabel = ps.values.reshape(-1, 1)
    label_idxs = kmeans.predict(toLabel)
    states_dict = {}
    for state in states_list:
        appliance_name = state.appliance_type
        instance = state.instance
        try:
            states_dict[appliance_name + '_' + instance].append(state)
        except KeyError:
            states_dict[appliance_name + '_' + instance] = [state]
    # states_dict, ps_dict, label_idxs, state_r3_list
    r3_get_r2(state_r3_list, label_idxs, states_dict, ps_dict)
    print('rer3')
    return appliance_truth, ps, states_list, centers, state_r3_list,appliance_consumtion

# staticGo()