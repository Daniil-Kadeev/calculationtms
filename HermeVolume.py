import math

from BaseUnit import BaseUnit, SplittedBaseUnit


class HermeVolum(BaseUnit):

    def __init__(self, l, params):
        self.init_temp = params['herme_init_temp']
        g = params['herme_g']
        ro_air = params['herme_ro_air']
        cp_air = params['herme_cp_air']
        alfa = params['herme_alfa']
        r = params['herme_r']
        delta = params['herme_delta']

        self.alfa = alfa
        self.f = math.pi * r * l
        self.CpG_air = cp_air * g
        self.cm_air = ro_air * self.f / 2 * r
        self.cm_st = 920 * self.f * delta * 2700

        self.__init_start()


    def __init_start(self):
        self.t_list_air = [self.init_temp, ]
        self.t_list_st = [self.init_temp, ]
        self.dt_list_air = [0, ]
        self.dt_list_st = [0, ]


    def step_d(self, t_in: float, params):
        self.dt = params['dt']
        self.q = params['q_go']
        self.t_in = t_in

        self.dt_list_air.append(self.equation_air())
        self.dt_list_st.append(self.equation_st())


    def step_t(self):
        self.update_t(self.t_list_air, self.dt_list_air, self.dt)
        self.update_t(self.t_list_st, self.dt_list_st, self.dt)

    
    def equation_air(self):
        return (self.alfa * self.f * (self.t_list_st[-1] - self.t_list_air[-1]) + 
        self.CpG_air * (self.t_in - self.t_list_air[-1]) + self.q) / self.cm_air


    def calc_print(self):
        print('Herme')
        print(f'({self.alfa} * {self.f} * ({self.t_list_st[-1]} - {self.t_list_air[-1]}) + {self.CpG_air} * ({self.t_in} - {self.t_list_air[-1]}) + {self.q}) / {self.cm_air}')
        print((self.alfa * self.f * (self.t_list_st[-1] - self.t_list_air[-1]) + 
        self.CpG_air * (self.t_in - self.t_list_air[-1]) + self.q) / self.cm_air)


    def equation_st(self):
        return (self.alfa * self.f * (self.t_list_air[-1] - self.t_list_st[-1])) / self.cm_st
    

    def get_full_t(self):
        return self.t_list_air

    
    def get_last_t(self):
        return self.t_list_air[-1]


    def get_out(self):
        return self.t_list_air[-1]



class SplittedHermeVolume(SplittedBaseUnit):

    def __init__(self, n: int, l, params):
        self.objs = [HermeVolum(l / n, params) for _ in range(n)]
        self.n = n


    def step_d(self, t_in, params):
        old_q = params['q_go'] 
        params['q_go'] /= self.n

        self.objs[0].step_d(t_in, params)
        pred_obj = self.objs[0]
        for obj in self.objs[1:]:
            obj.step_d(pred_obj.get_last_t(), params)
            pred_obj = obj
        params['q_go'] = old_q


    def step_t(self):
        self.objs[0].step_t()
        pred_obj = self.objs[0]
        for obj in self.objs[1:]:
            obj.step_t()
            pred_obj = obj


    def get_full_t(self):
        return [obj.t_list_air for obj in self.objs]


    def get_last_t(self):
        return [obj.t_list_air[-1] for obj in self.objs]

    
    def get_out(self):
        return self.objs[-1].get_out()
