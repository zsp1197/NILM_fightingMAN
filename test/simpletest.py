# Created by zhai at 2018/1/17
# Email: zsp1197@163.com
from sklearn.cluster import KMeans
import numpy as np
X = np.array([[1, 2], [1, 4], [1, 0],
              [4, 2], [4, 4], [4, 0]])
kmeans = KMeans(n_clusters=2, random_state=0)

kmeans.cluster_centers_=np.array([[1],[5]])
x=np.array([8]).reshape(-1,1)
print(kmeans.predict(x))