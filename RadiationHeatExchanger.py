from BaseUnit import BaseUnit, SplittedBaseUnit

class RadiationHeatExchanger(BaseUnit):
    
    def __init__(self, l):
        self.init_temp = 283.0

        self.g_cold_main = 1.081
        self.cp_cold = 1850
        self.g_cold = 1.081 * 1.26
        self.t_cold_inp = 288
        self.alfa_cold = 386.752
        self.f_cold = 6.009
        self.m_cold = 1.081 
        self.f_st = 0.3

        weidht = 1
        self.etta = 0.95
        self.eps = 0.95
        self.sig = 5.67 * 10 ** -8
        self.f = weidht * l
        self.a = 0.05

        self.c_st = 2700
        self.m_st = 5

        self.__init_start()


    def __init_start(self):
        self.t_list_cold = [self.init_temp, ]
        self.t_list_st = [self.init_temp, ]
        self.dt_list_cold = [0, ]
        self.dt_list_st = [0, ]


    def step_d(self, t_in: float, params):
        self.dt = params['dt']
        self.q = params['q']
        self.t_in_cold = t_in

        self.dt_list_cold.append(self.equation_liq())
        self.dt_list_st.append(self.equation_st())


    def step_t(self):
        self.update_t(self.t_list_cold, self.dt_list_cold, self.dt)
        self.update_t(self.t_list_st, self.dt_list_st, self.dt)

    
    def equation_liq(self):
        return (self.cp_cold * self.g_cold * (self.t_in_cold - self.t_list_cold[-1]) 
                + self.alfa_cold * self.f_cold * (self.t_list_st[-1] - self.t_list_cold[-1])
                ) / (self.cp_cold * self.m_cold)

    
    def equation_st(self):
        # print(f'({self.alfa_cold} * {self.f_st} * ({self.t_list_cold[-1]} - {self.t_list_st[-1]}) - {self.etta} * {self.eps} * {self.sig} * {self.t_list_st[-1]} ** 4 * {self.f} + {self.a} * {self.q} * {self.f}) / ({self.c_st} * {self.m_st})')
        # input(((self.alfa_cold * self.f_st * (self.t_list_cold[-1] - self.t_list_st[-1]) - 
        # self.etta * self.eps * self.sig * self.t_list_st[-1] ** 4 * self.f + 
        # self.a * self.q * self.f) / (self.c_st * self.m_st)))
        
        return (self.alfa_cold * self.f_st * (self.t_list_cold[-1] - self.t_list_st[-1]) - 
        self.etta * self.eps * self.sig * self.t_list_st[-1] ** 4 * self.f + 
        self.a * self.q * self.f) / (self.c_st * self.m_st)
    

    def get_full_t(self):
        return self.t_list_cold

    
    def get_last_t(self):
        return self.t_list_cold[-1]


    def get_out(self):
        return self.t_list_cold[-1]



class SplittedRadiationHeatExchanger(SplittedBaseUnit):

    def __init__(self, n: int, l):
        self.objs = [RadiationHeatExchanger(l / n) for _ in range(n)]
        for obj in self.objs:
            obj.m_st /= n
        self.n = n


    def step_d(self, t_in, params):
        self.objs[0].step_d(t_in, params)
        pred_obj = self.objs[0]
        for obj in self.objs[1:]:
            obj.step_d(pred_obj.get_last_t(), params)
            pred_obj = obj


    def step_t(self):
        self.objs[0].step_t()
        pred_obj = self.objs[0]
        for obj in self.objs[1:]:
            obj.step_t()
            pred_obj = obj


    def get_full_t(self):
        return [obj.t_list_cold for obj in self.objs]


    def get_last_t(self):
        return [obj.t_list_cold[-1] for obj in self.objs]

    
    def get_out(self):
        return self.objs[-1].get_out()
