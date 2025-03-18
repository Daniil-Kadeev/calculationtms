from BaseUnit import BaseUnit, SplittedBaseUnit

class RadiationHeatExchanger(BaseUnit):
    
    def __init__(self, l, params):
        self.init_temp = params['rto_init_temp']
        self.g_cold_main = params['rto_g_cold_main']
        self.cp_cold = params['rto_cp_cold']
        self.g_cold = params['rto_g_cold']
        self.alfa_cold = params['rto_alfa_cold']
        self.f_cold = params['rto_f_cold']
        self.m_cold = params['rto_m_cold']
        self.f_st = params['rto_f_cold']
        self.etta = params['rto_etta']
        self.eps = params['rto_eps']
        self.sig = params['rto_sig']
        self.a = params['rto_a']
        self.c_st = params['rto_c_st']
        self.m_st = params['rto_m_st']

        weidht = 1
        self.f = weidht * l
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
        return (self.alfa_cold * self.f_st * (self.t_list_cold[-1] - self.t_list_st[-1]) - 
        self.etta * self.eps * self.sig * self.t_list_st[-1] ** 4 * self.f + 
        self.a * self.q * self.f) / (self.c_st * self.m_st)


    def calc_print(self):
        print('RTO')
        print('liq')
        print(f'({self.cp_cold} * {self.g_cold} * ({self.t_in_cold} - {self.t_list_cold[-1]}) + {self.alfa_cold} * {self.f_cold} * ({self.t_list_st[-1]} - {self.t_list_cold[-1]})) / ({self.cp_cold} * {self.m_cold})')
        print((self.cp_cold * self.g_cold * (self.t_in_cold - self.t_list_cold[-1]) 
                + self.alfa_cold * self.f_cold * (self.t_list_st[-1] - self.t_list_cold[-1])
                ) / (self.cp_cold * self.m_cold))    
        print('st')
        print(f'({self.alfa_cold} * {self.f_st} * ({self.t_list_cold[-1]} - {self.t_list_st[-1]}) - {self.etta} * {self.eps} * {self.sig} * {self.t_list_st[-1]} ** 4 * {self.f} + {self.a} * {self.q} * {self.f}) / ({self.c_st} * {self.m_st})')
        print((self.alfa_cold * self.f_st * (self.t_list_cold[-1] - self.t_list_st[-1]) - 
        self.etta * self.eps * self.sig * self.t_list_st[-1] ** 4 * self.f + 
        self.a * self.q * self.f) / (self.c_st * self.m_st))

    def get_full_t(self):
        return self.t_list_cold

    
    def get_last_t(self):
        return self.t_list_cold[-1]


    def get_out(self):
        return self.t_list_cold[-1]



class SplittedRadiationHeatExchanger(SplittedBaseUnit):

    def __init__(self, n: int, l, params):
        self.objs = [RadiationHeatExchanger(l / n, params) for _ in range(n)]
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
