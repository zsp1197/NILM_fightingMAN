import pandas as pd
def up_sample_ps(ps: pd.Series, freq: str = 'S'):
    '''
    the data maybe compressed, pro-long the data with a fixed sample period
    :param ps:pd.Series(index=datatimeindex,data=power_read)
    :return: pd.Seires
    '''
    index = pd.to_datetime(ps.index)
    longindex = pd.date_range(start=min(index), end=max(index), freq=freq)
    pdf = pd.DataFrame(index=longindex, columns=['0'])
    pdf.ix[index, 0] = ps.values.tolist()
    pdf = pdf.fillna(method='pad')
    return pdf['0']
'''
list = [1, 2, 3, 4];
ind = pd.date_range(start='11:11:11', end='11:11:17', freq='2s')
ddd = pd.Series(index=[ind], data=list)
print(ddd)
fff = up_sample_ps(ddd, 's')
print(fff)
'''

def calculate24(nums: list, compare: int=24):
    if len(nums) >= 2:
        for i in range(len(nums)):
            cal = compare - nums[i]
            if cal >= 1:
                tempt = nums.copy()
                tempt.pop(i)
                if calculate24(tempt, cal):
                    print('+', nums[i])
                    return True
            cal = compare + nums[i]
            if cal >= 1:
                tempt = nums.copy()
                tempt.pop(i)
                if calculate24(tempt, cal):
                    print('-', nums[i])
                    return True
            cal = compare // nums[i]
            if compare % nums[i] == 0:
                tempt = nums.copy()
                tempt.pop(i)
                if calculate24(tempt, cal):
                    print('*', nums[i])
                    return True
            cal = compare * nums[i]
            tempt = nums.copy()
            tempt.pop(i)
            if calculate24(tempt, cal):
                print('/',nums[i])
                return True
        return False
    else:
        if (nums[0] == compare): print (nums[0])
        return (nums[0] == compare)

if __name__ == '__main__':
    print (calculate24([3,4,9,2], compare=24))