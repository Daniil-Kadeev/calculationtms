from typing import List

from BaseUnit import BaseUnit


class Regulator(BaseUnit):
    
    def __init__(self, params):
        self.b = params['regulator_b']

        self.init_posn = params['regulator_init_posn']
        self.insens = params['regulator_insens']

        self.pos_list = [self.init_posn]
        self.d_pos_list = [0]

    def step_d(self, t_in: List, params):
        self.dt = params['dt']
        self.t_reg = params['regulator_t_regul']
        self.t_in = t_in

        self.d_pos_list.append(self.equation_pos())

       

    def step_t(self):
        self.update_t(self.pos_list, self.d_pos_list, self.dt)
        if self.pos_list[-1] > 1:
            self.pos_list[-1] = 1
        elif self.pos_list[-1] < 0:
            self.pos_list[-1] = 0

    
    def equation_pos(self):
        if (
            (abs(self.t_in - self.t_reg) < self.insens) or
            (self.pos_list[-1] >= 1 and (self.t_in > self.t_reg + self.insens)) or
            (self.pos_list[-1] <= 0 and (self.t_in < self.t_reg - self.insens))
        ):
           return 0
        else:
            return (self.t_in - self.t_reg) / (abs(self.t_in - self.t_reg) + 0.0001) * self.b  

    
    def get_full_t(self):
        return self.pos_list
    

    def get_speed(self):
        return self.d_pos_list

    
    def get_last_t(self):
        return self.pos_list[-1]


    def get_out(self):
        return self.pos_list[-1]



