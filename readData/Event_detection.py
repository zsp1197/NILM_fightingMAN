from copy import deepcopy

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



class Parameters(object):
    def __init__(self):
        self.penalty = 999999
        self.considered_appliances = []
        # self.considered_appliances=['dish washer','fridge']
        # self.considered_appliances=['dish wahser','fridge','microwave']
        self.max_T = pd.Timedelta('30s')

        Y = np.array([150, 100, 80, 50, 40, 30, 20, 10, 6, 5, 2])
        X = np.array([1500, 1000, 700, 500, 400, 200, 100, 50, 10, 4, 0])
        self.p = np.poly1d(np.polyfit(X, Y, 3))
        self.sax_steps = self.get_sax_step()
        self.labeling_window_size = pd.Timedelta('2S')
        self.delta_detection=10
        self.sample_T=pd.Timedelta('1S')

    def get_sax_step(self):
        step = 0
        result = []
        while (step < 7000):
            result.append(step)
            step = step + self.p(step)
        result = result[0:-1:2]
        return result




class Event_detection(object):
    def __init__(self, ps:pd.Series, parameters:Parameters):
        self.ps=ps
        self.parameters=parameters
        self.ps_diff=ps.diff()
        self.ps_diff[self.ps.index[0]]=self.parameters.penalty



    def delta_based(self):
        '''
        return: list of tuples (starttime(pd.timestamp),endtime(pd.timestamp), delta_value)
        '''
        result=[]
        event_series=self.ps_diff[abs(self.ps_diff)>=self.parameters.delta_detection]

        if (len(event_series) == 1):
            result.append((self.ps.index[-1], self.ps.index[-1], self.ps.values[0]))
            return result

        for i, (index, value) in enumerate(event_series.iteritems()):
            try:
                if(i == len(event_series)-1):
                    result.append((index, self.ps.index[-1], value))
                else:
                    result.append((index, event_series.index[i+1]-self.parameters.sample_T, value))
            except:
                print(event_series)
                print('error in delta_based')
                return [(self.ps.index[0],self.ps.index[-1],self.ps.values[0])]
        return result


    def knn_based(self):
        '''
        return: list of tuples (starttime(pd.timestamp),endtime(pd.timestamp), cluster center value)
        '''
        pass