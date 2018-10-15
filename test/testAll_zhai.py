import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from hmmlearn import hmm
import warnings


startTime = pd.Timestamp('2018-1-1')
endTime = pd.Timestamp('2018-1-11')

appliance_dict={'1':(10,100,200),'2':(200,500,1000),3:(100,400,600)}
for key,var in appliance_dict.items():
    pass