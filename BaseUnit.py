class BaseUnit():

    def update_t(self, t_list, dt_list, dt):
        t_list.append(t_list[-1] + dt_list[-1] * dt)


    def print_error(self, func_name):
        raise NotImplementedError(f'В классе {self.__class__.__name__} не реализована функция {func_name}')


    def step_d(self):
        self.print_error('step_d')


    def step_t(self):
        self.print_error('step_t')
        

    def update_params(self):
        self.print_error('undate_params')

    
    def get_full_t(self):
        self.print_error('get_full_t')

    
    def get_last_t(self):
        self.print_error('get_last_t')
    

    def get_out(self):
        self.print_error('get_out')

    
    def get_st(self):
        return self.t_list_st


class SplittedBaseUnit():
    pass
