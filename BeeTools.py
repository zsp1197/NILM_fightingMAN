# Created by zhai at 2018/1/12
# Email: zsp1197@163.com
from Tools import *


@check_func_input_output_type_static
def read_xls_fill(filepath: str,freq='30S') -> pd.Series:
    df = pd.read_excel(filepath)
    index = df['日期'].values
    index = [pd.Timestamp(idx) for idx in index]
    ps = pd.Series(index=index, data=df['正向有功功率(W)'].values)
    ps.sort_index(inplace=True)
    ps=up_sample_ps(ps=ps)
    ps.resample(freq)
    return ps


@check_func_input_output_type_static
def aggregate_with_resample(pss, freq: str = '30S'):
    '''
    add with resample to 1Hz
    :return:
    '''
    pss = [up_sample_ps(ps=ps) for ps in pss]
    for i, ps in enumerate(pss):
        if (i == 0):
            final_ps = ps
        else:
            final_ps = final_ps.add(ps, fill_value=0)
        final_ps=final_ps.resample(freq).asfreq()
    return final_ps

if __name__ == "__main__":
    inx = pd.date_range('2018-1-1 00:00:00','2018-1-1 00:49:30',freq='30s')
    ps1 = pd.Series(data=range(100), index=inx)
    ps2 = pd.Series(data=range(0,200,2), index=inx)
    ps3 = pd.Series(data=range(0,300,3), index=inx)
    sss = aggregate_with_resample([ps1, ps2, ps3])
    print()