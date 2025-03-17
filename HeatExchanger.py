from BaseUnit import BaseUnit


class HeatExchanger(BaseUnit):
    
    def __init__(self, type_exchanger='gas_liq'):
        self.init_temp = 283.0

        # Параметры воздуха
        if type_exchanger == 'gas_liq':
            self.start_gas_liq()
        elif type_exchanger == 'liq_liq':
            self.start_liq_liq()
        else:
            raise Exception
 
        # Параметры стенки
        self.c_st = 2700
        self.m_st = 5
        self.__init_start()


    def start_gas_liq(self):
        self.cp_hot = 1005
        self.g_hot = 2.487
        self.t_hot_inp = 301
        self.alfa_hot = 457.489
        self.f_hot = 16.20183
        self.m_hot = 2.487 # Преобразование в кг/ч? (если G_hot в тоннах)

        # Параметры жидкости
        self.cp_cold = 1850
        self.g_cold = 1.081
        self.t_cold_inp = 288
        self.alfa_cold = 386.752
        self.f_cold = 6.009
        self.m_cold = 1.081 # Исправлено на G_cold


    def start_liq_liq(self):
        self.cp_hot = 1850
        self.g_hot = 1.081
        self.t_hot_inp = 288
        self.alfa_hot = 386.752
        self.f_hot = 6.009
        self.m_hot = 0.93
        # Параметры жидкости
        self.cp_cold = 1850
        self.g_cold = 1.081
        self.t_cold_inp = 288
        self.alfa_cold = 386.752
        self.f_cold = 6.009
        self.m_cold = 0.93 # Исправлено на G_cold


    def __init_start(self):
        self.t_list_hot = [self.init_temp, ]
        self.t_list_cold = [self.init_temp, ]
        self.t_list_st = [self.init_temp, ]
        self.dt_list_hot = [0, ]
        self.dt_list_cold = [0, ]
        self.dt_list_st = [0, ]


    def step_d(self, t_in: float, params):
        self.dt = params['dt']
        self.t_in_hot, self.t_in_cold = t_in

        self.dt_list_hot.append(self.equation_hot())
        self.dt_list_cold.append(self.equation_cold())
        self.dt_list_st.append(self.equation_st())
       

    def step_t(self):
        self.update_t(self.t_list_hot, self.dt_list_hot, self.dt)
        self.update_t(self.t_list_cold, self.dt_list_cold, self.dt)
        self.update_t(self.t_list_st, self.dt_list_st, self.dt)
        # input((self.t_list_hot[-1], self.t_list_cold[-1], self.t_list_st[-1]))

    
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

    
    def get_full_t(self):
        return (self.t_list_hot, self.t_list_cold) 

    
    def get_last_t(self):
        return (self.t_list_hot[-1], self.t_list_cold[-1])


    def get_out(self):
        return (self.t_list_hot[-1], self.t_list_cold[-1])



