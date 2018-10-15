# Created by zhai at 2018/1/21
# Email: zsp1197@163.com
from scipy import signal

import pandas as pd
import numpy as np
from scipy import *
import Tools

def median_filter(ps:pd.Series,size:int=21):
    value=ps.values
    values=signal.medfilt(volume=value,kernel_size=size)
    return pd.Series(index=ps.index,data=values)