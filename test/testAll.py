import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from hmmlearn import hmm
import warnings

import BeeTools
import Tools
warnings.filterwarnings("ignore")
def getPS(mean, var, index):
    def output_simulation(state):
        return float(var[state] * np.random.randn(1) + mean[state])
    apphmm = hmm.GaussianHMM(n_components=len(mean), covariance_type="full")
    apphmm.means_ = np.array(mean).reshape(-1, 1)
    apphmm.covars_ = np.square(np.array(var)).reshape(-1, 1)
    initprob = np.array([0.9, 0.05, 0.05])
    apphmm.startprob_ = initprob
    tranmatrix = np.ones([len(mean), len(mean)])
    k = 10
    for i in range(len(mean)):
        tranmatrix[i, i] += k
    tranmatrix = tranmatrix / (len(mean) + k)
    tranmatrix = np.array([[0.9, 0.05, 0.05],
                           [0.07, 0.9, 0.03],
                           [0.08, 0.02, 0.9]])
    apphmm.transmat_ = tranmatrix
    _, zzz = apphmm.sample(len(index))
    del _
    ps = pd.Series(index=index, data=zzz)
    ps = ps.apply(output_simulation)
    idx = ps < 0
    ps[idx] = [0] * np.count_nonzero(idx)
    return ps

pss = []
ps_dict = {}
startTime = pd.Timestamp('2018-1-1')
endTime = pd.Timestamp('2018-1-16')
index = pd.date_range(startTime,endTime, freq='30s')
mean = [[3, 35, 50], [2, 100, 390], [2, 340, 600]]
var = [[1, 1, 1], [1, 1, 1], [1, 1, 3]]
applist=['TV', 'Box', 'Fridge']
for id, app in enumerate(applist):
    pss.append(getPS(mean[id], var[id], index))
    ps_dict[app] = pss[-1]
Tools.server_ps_plot(ps=BeeTools.aggregate_with_resample(pss))
pss.append(BeeTools.aggregate_with_resample(pss))
Tools.server_pss_plot(pss)
print('')

fout= pd.HDFStore('./30test.h5', 'w')
datarange = pd.date_range(startTime, endTime)
for app in applist:
    print(app)
    ps = ps_dict[app]
    for i in range(len(datarange)-1):
        index = ps.index > pd.Timestamp('2017-12-11')
        daydata = ps.loc[datarange[i]: datarange[i+1]]
        daydata = daydata[ :-1]
        print(datarange[i])
        fout['/series/' + app + '/1/' + '/%s' % datarange[i].date()] = daydata
fout.close()