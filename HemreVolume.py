import math

import numpy as np
import matplotlib.pyplot as plt

from BaseUnit import BaseUnit, SplittedBaseUnit


class HermeVolum(BaseUnit):

    def __init__(self, l):
        g = 0.25 * 10
        ro_air = 1.2 * 1000
        cp_air = 1005 
        alfa = 200
        r = 1.5
        delta = 1/1000

        self.alfa = alfa
        self.f = math.pi * r * l
        self.CpG_air = cp_air * g
        self.cm_air = ro_air * self.f / 2 * r
        self.cm_st = 920 * self.f * delta * 2700

        self.__init_start()


    def __init_start(self):
        self.t_list_air = [293, ]
        self.t_list_st = [293, ]
        self.dt_list_air = [0, ]
        self.dt_list_st = [0, ]

    
    def step(self, t_in: float):
        self.t_in = t_in
        self.step_d()
        self.step_t()
        # print(self.dt_list_air[-1])

    
    def update_params(self, params):
        self.dt = params['dt']
        self.q = params['q_go']


    def step_d(self):
        self.dt_list_air.append(self.equation_air())
        self.dt_list_st.append(self.equation_st())


    def step_t(self):
        self.update_t(self.t_list_air, self.dt_list_air, self.dt)
        self.update_t(self.t_list_st, self.dt_list_st, self.dt)

    
    def equation_air(self):
        # print(f'({self.alfa} * {self.f} * ({self.t_list_st[-1]} - {self.t_list_air[-1]}) + {self.CpG_air} * ({self.t_in} - {self.t_list_air[-1]}) + {self.q}) / {self.cm_air}')

        return (self.alfa * self.f * (self.t_list_st[-1] - self.t_list_air[-1]) + 
        self.CpG_air * (self.t_in - self.t_list_air[-1]) + self.q) / self.cm_air

    
    def equation_st(self):
        return (self.alfa * self.f * (self.t_list_air[-1] - self.t_list_st[-1])) / self.cm_st
    

    def get_full_t(self):
        return self.t_list_air

    
    def get_last_t(self):
        return self.t_list_air[-1]


    def get_out(self):
        return self.t_list_air[-1]


class SplittedHermeVolume(SplittedBaseUnit):

    def __init__(self, n: int, l):
        self.objs = [HermeVolum(l / n) for _ in range(n)]
        self.n = n


    def step(self, t_in, params):
        old_q = params['q_go'] 
        params['q_go'] /= self.n
        
        self.objs[0].update_params(params)
        self.objs[0].step(t_in)
        # params['q_go'] = 0
        pred_obj = self.objs[0]
        for obj in self.objs[1:]:
            obj.update_params(params)
            obj.step(pred_obj.t_list_air[-1])
            pred_obj = obj
        # for obj in self.objs:
        #     print(obj.t_list_air[-1])
        # input()
        # params['q_go'] = old_q


    def get_full_t(self):
        return [obj.t_list_air for obj in self.objs]


    def get_last_t(self):
        return [obj.t_list_air[-1] for obj in self.objs]

    
    def get_out(self):
        return self.objs[-1].get_out()
