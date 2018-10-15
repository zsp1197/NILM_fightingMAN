# Created by zhai at 2018/1/16
# Email: zsp1197@163.com
import pandas as pd
import os
path='/home/uftp/hubei'
targetpath='/home/uftp/hubei/30S'
files=[i for i in os.listdir(path) if '.h5' in i]

def resample_2_30S(store,target_store):
    keys=store.keys()
    for key in keys:
        ps=store[key]
        ps.resample('30S')
        target_store[key]=ps

for file in files:
    store=pd.HDFStore(os.path.join(path,file))
    target_store=pd.HDFStore(os.path.join(targetpath,file),'w')
    resample_2_30S(store=store,target_store=target_store)
