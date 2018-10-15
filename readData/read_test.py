# Created by zhai at 2018/1/11
# Email: zsp1197@163.com
import pandas as pd
import matplotlib.pyplot as plt

from Tools import up_sample_ps

# path='D:\SJTU\湖北项目\数据\\xusuqian/'
path='C:\\Users\zhai\Desktop\\temp/'
file='负荷数据_01142052.xls'
# file='computer_1_Sck-20-2d9bec07004b1200.xls'
df=pd.read_excel(path+file)
print(df)
index=df['日期'].values
index=[pd.Timestamp(idx) for idx in index]
ps=pd.Series(index=index,data=df['正向有功功率(W)'].values)
ps=up_sample_ps(ps=ps,freq='S')
ps.resample('30S')
print('hi')
ps.plot()
plt.show()