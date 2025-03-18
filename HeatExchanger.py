from typing import List

from BaseUnit import BaseUnit


class HeatExchanger(BaseUnit):
    
    def __init__(self, params, type_exchanger='gas_liq'):
        self.init_temp = params['exchanger_init_temp']

        if type_exchanger == 'gas_liq':
            self.start_gas_liq(params)
        elif type_exchanger == 'liq_liq':
            self.start_liq_liq(params)
        else:
            raise Exception
 
        self.c_st = params['exchanger_c_st']
        self.m_st = params['exchanger_m_st']
        self.__init_start()


    def start_gas_liq(self, params):
        self.g_hot_main = params['gas_liq_exchanger_g_hot_main']
        self.cp_hot = params['gas_liq_exchanger_cp_hot']
        self.g_hot = params['gas_liq_exchanger_g_hot']
        self.alfa_hot = params['gas_liq_exchanger_alfa_hot']
        self.f_hot = params['gas_liq_exchanger_f_hot']
        self.m_hot = params['gas_liq_exchanger_m_hot']

        self.g_cold_main = params['gas_liq_exchanger_g_cold_main']
        self.cp_cold = params['gas_liq_exchanger_cp_cold']
        self.g_cold = params['gas_liq_exchanger_g_cold']
        self.alfa_cold = params['gas_liq_exchanger_alfa_cold']
        self.f_cold = params['gas_liq_exchanger_f_cold']
        self.m_cold = params['gas_liq_exchanger_m_cold']


    def start_liq_liq(self, params):
        self.g_hot_main = params['liq_liq_exchanger_g_hot_main']
        self.cp_hot = params['liq_liq_exchanger_cp_hot']
        self.g_hot = params['liq_liq_exchanger_g_hot']
        self.alfa_hot = params['liq_liq_exchanger_alfa_hot']
        self.f_hot = params['liq_liq_exchanger_f_hot']
        self.m_hot = params['liq_liq_exchanger_m_hot']

        self.g_cold_main = params['liq_liq_exchanger_g_cold_main']
        self.cp_cold = params['liq_liq_exchanger_cp_cold']
        self.g_cold = params['liq_liq_exchanger_g_cold']
        self.alfa_cold = params['liq_liq_exchanger_alfa_cold']
        self.f_cold = params['liq_liq_exchanger_f_cold']
        self.m_cold = params['liq_liq_exchanger_m_cold']


    def __init_start(self):
        self.t_list_hot = [self.init_temp, ]
        self.t_list_cold = [self.init_temp, ]
        self.t_list_st = [self.init_temp, ]
        self.dt_list_hot = [0, ]
        self.dt_list_cold = [0, ]
        self.dt_list_st = [0, ]


    def step_d(self, t_in: List, params):
        self.dt = params['dt']
        self.t_in_hot, self.t_in_cold = t_in

        self.dt_list_hot.append(self.equation_hot())
        self.dt_list_cold.append(self.equation_cold())
        self.dt_list_st.append(self.equation_st())
       

    def step_t(self):
        self.update_t(self.t_list_hot, self.dt_list_hot, self.dt)
        self.update_t(self.t_list_cold, self.dt_list_cold, self.dt)
        self.update_t(self.t_list_st, self.dt_list_st, self.dt)

    
    def equation_hot(self):
        return (self.cp_hot * self.g_hot * (self.t_in_hot - self.t_list_hot[-1]) 
                + self.alfa_hot * self.f_hot * (self.t_list_st[-1] - self.t_list_hot[-1])
                ) / (self.cp_hot * self.m_hot)
    

    def equation_cold(self):
        return (self.cp_cold * self.g_cold * (self.t_in_cold - self.t_list_cold[-1]) 
                + self.alfa_cold * self.f_cold * (self.t_list_st[-1] - self.t_list_cold[-1])
                ) / (self.cp_cold * self.m_cold)


    def equation_st(self):
        return (self.alfa_hot * self.f_hot * (self.t_list_hot[-1] - self.t_list_st[-1]) 
                + self.alfa_cold * self.f_cold * (self.t_list_cold[-1] - self.t_list_st[-1])
                ) / (self.c_st * self.m_st)

    
    def calc_print(self):
        print('exchanger')
        print('hot')
        print(f'({self.cp_hot} * {self.g_hot} * ({self.t_in_hot} - {self.t_list_hot[-1]}) + {self.alfa_hot} * {self.f_hot} * ({self.t_list_st[-1]} - {self.t_list_hot[-1]})) / ({self.cp_hot} * {self.m_hot})')
        print((self.cp_hot * self.g_hot * (self.t_in_hot - self.t_list_hot[-1]) 
                + self.alfa_hot * self.f_hot * (self.t_list_st[-1] - self.t_list_hot[-1])
                ) / (self.cp_hot * self.m_hot))
        print('cold')
        print(f'({self.cp_cold} * {self.g_cold} * ({self.t_in_cold} - {self.t_list_cold[-1]}) + {self.alfa_cold} * {self.f_cold} * ({self.t_list_st[-1]} - {self.t_list_cold[-1]})) / ({self.cp_cold} * {self.m_cold})')
        print((self.cp_cold * self.g_cold * (self.t_in_cold - self.t_list_cold[-1]) 
                + self.alfa_cold * self.f_cold * (self.t_list_st[-1] - self.t_list_cold[-1])
                ) / (self.cp_cold * self.m_cold))

    
    def get_full_t(self):
        return (self.t_list_hot, self.t_list_cold) 

    
    def get_last_t(self):
        return (self.t_list_hot[-1], self.t_list_cold[-1])


    def get_out(self):
        return (self.t_list_hot[-1], self.t_list_cold[-1])



