# Created by zhai at 2018/1/12
# Email: zsp1197@163.com
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from Tools import *
import os

path = '/home/uftp/hubei/'
users_list = os.listdir(path)
users_states = {}


def getUserStates(thepath):
    df = pd.read_csv(os.path.join(thepath, 'states.txt'), header=None, index_col=0)
    appliance_names = list(df.index)
    states = []
    for appliance_name in appliance_names:
        states_series = df.loc[appliance_name][1:]
        states_np=states_series.values
        states_np=states_np.astype(np.float64)
        states_np = states_np[~np.isnan(states_np)]
        states.append(list(states_np))
    return dict(zip(appliance_names,states))


for user_name in users_list:
    users_states.update({user_name: getUserStates(os.path.join(path, user_name))})

print(users_states)

for user,value in users_states.items():
    for appliance_name,states_list in value.items():
        plt.plot(states_list,'*')
    plt.title(user)
    plt.show()