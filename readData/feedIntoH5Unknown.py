# Created by zhai at 2018/1/29
# Email: zsp1197@163.com
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

home = 'xiayurong'
datastore = Data_store(redd_hdf5_path='/home/uftp/hubei/4test/30%s.h5' % home)
# datarange = [pd.Timestamp('2017-12-2 00:00:00'), pd.Timestamp('2018-1-1 00:00:00')]
pss=[]
for app in datastore.appliance_names:
    if (app in ['meter', 'TVbox', 'TV','unknown']) and home == 'xiayurong':
        if app == 'meter':
            totalpower = datastore.get_instance_ps(appliance_name=app, instance='1')
        continue
    theps = datastore.get_instance_ps(appliance_name=app, instance='1')
    # appliance_truth[app] = theps
    pss.append(theps)
    # appliance_consumtion[app] = Tools.ps_consumption(theps=theps)
knownps = aggregate_with_resample(pss)
ps_unknown=totalpower.subtract(knownps,fill_value=0)
store=datastore.store

startDayStr, endDayStr = min(knownps.index)._date_repr, max(knownps.index)._date_repr
daysTimeStamp = [i._date_repr for i in list(pd.date_range(start=startDayStr, end=endDayStr, freq='D'))]

keys=[]
pss=[]
for day in daysTimeStamp:
    keys.append('/series/unknown/1/%s'%day)
    pss.append(ps_unknown[day])
print()

assert len(pss)==len(keys)
for i,key in enumerate(keys):
    store.append(key=key,value=pss[i])
store.close()