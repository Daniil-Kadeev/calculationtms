from BaseUnit import BaseUnit, SplittedBaseUnit

class RadiationHeatExchanger(BaseUnit):
    
    def __init__(self, l):
        self.init_temp = 283.0
        self.cp_cold = 1850
        self.g_cold = 1.081
        self.t_cold_inp = 288
        self.alfa_cold = 386.752
        self.f_cold = 6.009
        self.m_cold = 1.081

        self.etta = 1
        self.eps = 1
        self.sig = 5.67 * 10 ** -8
        self.f_st = 6
        self.a = 1
        self.q = 200

        self.__init_start()


    def __init_start(self):
        self.t_list_liq = [self.init_temp, ]
        self.t_list_st = [self.init_temp, ]
        self.dt_list_liq = [0, ]
        self.dt_list_st = [0, ]


    def step_d(self, t_in: float, params):
        self.dt = params['dt']
        self.q = params['q_go']
        self.t_in = t_in

        self.dt_list_liq.append(self.equation_liq())
        self.dt_list_st.append(self.equation_st())


    def step_t(self):
        self.update_t(self.t_list_liq, self.dt_list_liq, self.dt)
        self.update_t(self.t_list_st, self.dt_list_st, self.dt)

    
    def equation_liq(self):
        return (self.alfa * self.f * (self.t_list_st[-1] - self.t_list_liq[-1]) + 
        self.CpG_air * (self.t_in - self.t_list_liq[-1]) + self.q) / self.cm_air

    
    def equation_st(self):
        return (self.alfa * self.f * (self.t_list_liq[-1] - self.t_list_st[-1]) - 
        self.etta * self.eps * self.sig * self.t_list_st[-1] ** 4 * self.f_st + 
        self.a * self.q * self.f_st) / self.cm_st
    

    def get_full_t(self):
        return self.t_list_liq

    
    def get_last_t(self):
        return self.t_list_liq[-1]


    def get_out(self):
        return self.t_list_liq[-1]



class SplittedHermeVolume(SplittedBaseUnit):

    def __init__(self, n: int, l):
        self.objs = [HermeVolum(l / n) for _ in range(n)]
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
