from math import sin
import time

from HeatGenerator import HeatGenerator
from HemreVolume import SplittedHermeVolume
from Plotter import Plotter





def calc_step():
    Generator = HeatGenerator()
    my_sin = Generator.get_sin()
    my_sin2 = Generator.get_sin2()
    my_sin3 = Generator.get_sin3()

    my_sin.send(None)
    my_sin2.send(None)
    my_sin3.send(None)

    while True:
        structure, params = yield
        last = structure[-1]

        if params['rule'] == 'sin':   
            params['q_go'] = my_sin.send(params)
            next(my_sin)
        elif params['rule'] == 'sin2':
            params['q_go'] = my_sin2.send(params)
            next(my_sin2)
        elif params['rule'] == 'sin3':
            params['q_go'] = my_sin3.send(params)
            next(my_sin3)

        # old_q = params['q_go']
        for obj in structure:
            # params['q_go'] *= -1
            obj.step(last.get_out(), params)
            last = obj
        # params['q_go'] = old_q    



def calc_animated():
    plotter = Plotter().animated_plot3d()
    plotter.send(None)

    structure = (
        SplittedHermeVolume(40, 2),
        # SplittedHermeVolume(20, 2),
        # SplittedHermeVolume(3, 10),
        # SplittedHermeVolume(3, 10)
    )

    t_list = [0, ]
    calc = calc_step()
    calc.send(None)
    while True:
        params = yield
        calc.send((structure, params))
        t_list.append(t_list[-1] + params['dt'])
        plotter.send((structure, t_list, params))
