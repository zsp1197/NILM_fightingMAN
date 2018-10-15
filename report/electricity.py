# Created by zhai at 2018/3/15
# Email: zsp1197@163.com
import pandas as pd
import Tools
import numpy as np
import matplotlib.pyplot as plt

from BeeTools import aggregate_with_resample
from Data_store import Data_store

home = 'xiayurong'
datastore = Data_store(redd_hdf5_path='D:\SJTU\pythoncode\\NILM_fightingMAN\data\\30/30%s.h5' % home)
# datastore = Data_store(redd_hdf5_path='/home/uftp/hubei/30%s.h5' % home)
datarange = [pd.Timestamp('2017-12-24 00:00:00'), pd.Timestamp('2018-12-31 00:00:00')]

pss = []
# datarange = [pd.Timestamp('2017-12-15 10:00:00'), pd.Timestamp('2017-12-15 12:00:00')]
appliance_truth={}
appliance_consumtion = {}
for app in datastore.appliance_names:
    if (app in ['meter']) and home == 'xiayurong':
        if app == 'meter':
            totalpower = datastore.get_instance_ps(appliance_name=app, instance='1').loc[
                         datarange[0]: datarange[-1]]
        continue
    theps = datastore.get_instance_ps(appliance_name=app, instance='1').loc[datarange[0]: datarange[-1]]
    appliance_truth[app] = theps
    pss.append(theps)
    appliance_consumtion[app] = Tools.ps_consumption(theps=theps)
    # if(app=='lamp'):
    #     print()
knownps = aggregate_with_resample(pss)
appliance_truth['unknown'] = totalpower - knownps
appliance_consumtion['unknown'] = Tools.ps_consumption(theps=appliance_truth['unknown'])
labels=[]
fracs=[]
for key,var in appliance_consumtion.items():
    print(key+":"+str(var))
    labels.append(key)
    fracs.append(var)
# plt.subplot()

plt.pie(fracs, labels=labels,  shadow=True)
plt.show()