# Created by zhai at 2018/1/22
# Email: zsp1197@163.com
import Infer_result
import Tools
import pandas as pd

class Performance():
    # @Tools.check_func_input_output_type_static
    def __init__(self,infer_result:Infer_result,appliance_truth):
        self.appliance_truth=appliance_truth
        self.infer_result=infer_result

        print()

    def dissagga_metric(self):
        self.infer_result.get_estimated_ps_dict()
        total = None
        diff = None
        for key, val in self.appliance_truth.items():
            if key not in self.infer_result.ps_dict.keys():
                difftempt = self.aligned(val)
            else:
                difftempt = abs(self.aligned(val) - self.aligned(self.infer_result.ps_dict[key]))
            if not isinstance(diff, pd.Series):
                diff = difftempt
            else:
                diff += difftempt
            if not isinstance(total, pd.Series):
                total = self.aligned(val)
            else:
                total += self.aligned(val)
            if total.hasnans or diff.hasnans:
                print('got nan')
        for key, val in self.infer_result.ps_dict.items():
            if key not in self.appliance_truth.keys():
                diff += self.aligned(val)
        acc = sum(diff) / sum(total) / 2
        esttotal = None
        for key, val in self.infer_result.ps_dict.items():
            if not isinstance(esttotal, pd.Series):
                esttotal = self.aligned(val)
            else:
                esttotal += self.aligned(val)
        return acc


    def dissagga_metric2(self):
        self.infer_result.get_estimated_ps_dict()
        truthdf = pd.DataFrame()
        estidf = pd.DataFrame()
        for key, val in self.appliance_truth.items():
            truthdf[key] = self.aligned(val)
            if key not in self.infer_result.ps_dict.keys():
                estidf[key] = pd.Series(index=truthdf[key].index, data=[0] * len(truthdf))
            else:
                estidf[key] = self.aligned(self.infer_result.ps_dict[key])
        for key, val in self.infer_result.ps_dict.items():
            if key not in self.appliance_truth.keys():
                estidf[key] = self.aligned(val)
                truthdf[key] = pd.Series(index=estidf[key].index, data=[0] * len(truthdf))
        return truthdf, estidf




    def aligned(self,ps):
        return Tools.up_sample_ps(ps)

    def power_consumption_metric(self):
        pass