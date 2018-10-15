# Created by zhai at 2018/1/22
from unittest import TestCase
import Tools

# Email: zsp1197@163.com
class TestSplit_list_to_chunks(TestCase):
    def test_split_list_to_chunks(self):
        a=[1,2,3,54,6,7,7,456,6453,654,65,65,65,2]
        print(Tools.split_list_to_chunks(a,3))
