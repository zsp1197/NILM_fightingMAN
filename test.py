# Created by zhai at 2017/12/14
# Email: zsp1197@163.com
from hubei.Clustering import Clustering
import pandas as pd
import numpy as np
# clustering=Clustering('D:\SJTU\pythoncode\summerTime\data\\allappliances.hdf5')
clustering=Clustering()
print(clustering.deal_with_ps(pd.Series(data=np.random.random(1000))))
