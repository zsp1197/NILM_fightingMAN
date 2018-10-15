# Created by zhai at 2018/1/24
from unittest import TestCase
import pandas as pd
import numpy as np
import Tools
import matplotlib.pyplot as plt
# Email: zsp1197@163.com
class TestServer_ps_plot(TestCase):
    def test_server_ps_plot(self):
        index = pd.date_range(start=pd.Timestamp('2011-10-15'), end=pd.Timestamp('2011-10-16'),freq='30S')
        a=pd.Series(data=np.random.rand(len(index)),index=index)
        # a.plot()
        # plt.show()
        
        Tools.server_ps_plot(a)
