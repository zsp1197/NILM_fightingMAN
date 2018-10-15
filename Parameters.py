# Created by zhai at 2018/1/22
# Email: zsp1197@163.com
class Parameters():
    def __init__(self):
        # 时间序列n阶假设
        self.n_order=2
        # 根据其董事兼削减r2数量，每个r3拥有多少个r2
        self.num_of_r2=70
        # distrbitution_type
        self.distrbitution_type='gaussian_discrete'

    def __str__(self):
        string=str(self.n_order)+' '+str(self.num_of_r2)
        return string