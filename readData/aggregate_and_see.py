# Created by zhai at 2018/1/12
# Email: zsp1197@163.com
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Tools import *
from BeeTools import *
import os
path = '/home/uftp/hubei/ori'
users_list = os.listdir(path)

has_meter=False
has_normal=False

for user in users_list:
    user_path=os.path.join(path,user)
    appliances_list = os.listdir(user_path)
    appliances_list=[appliance for appliance in appliances_list if appliance.split(sep='.')[-1]=='xls']
    print(appliances_list)
    for appliance_file_name in appliances_list:
        if('meter' in appliance_file_name):
            if(not has_meter):
                meter=read_xls_fill(filepath=os.path.join(path,user,appliance_file_name))
                has_meter=True
            else:
                meter=aggregate_with_resample([meter,read_xls_fill(filepath=os.path.join(path,user,appliance_file_name))])
        else:
            if(not has_normal):
                normal=read_xls_fill(filepath=os.path.join(path,user,appliance_file_name))
                has_normal=True
            else:
                normal=aggregate_with_resample([normal,read_xls_fill(filepath=os.path.join(path,user,appliance_file_name))])
    meter.plot(label='meter')
    normal.plot(label='sum of appliances')
    print(user)
    normal_consumption=ps_consumption(normal)
    meter_consumption=ps_consumption(meter)
    print(normal_consumption)
    print(meter_consumption)
    print(normal_consumption/meter_consumption)
    plt.title(user)
    plt.legend()
    # plt.show()
    plt.show(block=False)
print()