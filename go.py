import math

import numpy as np
import matplotlib.pyplot as plt


class BaseUnit():

    def update_t(self, t_list, dt_list, dt):
        t_list.append(t_list[-1] + dt_list[-1] * dt)


    def print_error(self, func_name):
        print(f'В классе {self.__class__.__name__} не реализована функция {func_name}')


    def step(self):
        self.print_error('step')


    def step_d(self):
        self.print_error('step_d')


    def step_t(self):
        self.print_error('step_t')
        

    def update_params(self):
        self.print_error('undate_params')


class HermeVolum(BaseUnit):

    def __init__(self, l):
        g = 0.25
        cp_air = 1005
        alfa = 200
        r = 1.5
        delta = 1/1000

        self.alfa = alfa
        self.f = math.pi * r * l

        self.CpG_air = cp_air * g
        self.cm_air = cp_air * self.f / 2 * r
        self.cm_st = 920 * self.f * delta * 2700

        self.q = 500

        self.__init_start()


    def __init_start(self):
        self.t_list_air = [293, ]
        self.t_list_st = [293, ]
        self.dt_list_air = [0, ]
        self.dt_list_st = [0, ]

    
    def step(self, t_in: float, params):
        self.update_params(params)
        self.t_in = t_in
        self.step_d()
        self.step_t()

    
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
        return (self.alfa * self.f * (self.t_list_st[-1] - self.t_list_air[-1]) + 
        self.CpG_air * (self.t_in - self.t_list_air[-1]) + self.q) / self.cm_air

    
    def equation_st(self):
        return (self.alfa * self.f * (self.t_list_air[-1] - self.t_list_st[-1])) / self.cm_st


class SplittingHermeVolume():

    def __init__(self, n: int, l):
        self.objs = [HermeVolum(l / n) for _ in range(n)]
        self.n = n


    def step(self, t_in, params):
        self.objs[0].step(t_in, params)
        pred_obj = self.objs[0]

        old_q = params['q_go'] 
        params['q_go'] /= self.n
        for obj in self.objs[1:]:
            obj.step(pred_obj.t_list_air[-1], params)
            pred_obj = obj
        params['q_go'] = old_q


    def get_full_t(self):
        return [obj.t_list_air for obj in self.objs]


    def get_last_t(self):
        return [obj.t_list_air[-1] for obj in self.objs]


    
def main():
    params = {}

    params['dt'] = 0.5
    params['q_go'] = 500

    dt = params['dt']
    t_list = [0, ]
    go = HermeVolum(5)
    go = SplittingHermeVolume(10, 5)
    t_in_list = np.linspace(0, 20, 1000) 
    t_in_list = 10 * np.sin(t_in_list) + 293
    t_in_list = np.append(t_in_list, np.full(200, 293))

    

    for t_in in t_in_list:
        go.step(t_in, params)
        t_list.append(t_list[-1] + params['dt'])

    time_points = t_list[-1]
    num_elements = 10

    time = np.array(t_list)
    
    length = len(t_list)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    for i, t_list_air in enumerate(go.get_full_t()):
        z_coord = np.full(length, i)
        ax.scatter(t_list, z_coord, t_list_air, s=1)
    ax.grid()
    plt.show()


if __name__ == '__main__':
    main()