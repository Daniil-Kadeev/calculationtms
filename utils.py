from math import sin
import time

from HemreVolume import SplittedHermeVolume
from Plotter import Plotter


def get_sin():
    t = 0
    while True:
        params = yield 
        t += params['dt']
        yield params['A'] * sin(t / params['T']) + params['bias']


def get_sin2():
    t = 0
    while True:
        params = yield 
        t += params['dt']
        yield (params['A'] * sin(t / params['T']) + params['bias'] + 
        params['A2'] * sin(t / params['T2']) + params['bias'])


def get_sin3():
    t = 0
    while True:
        params = yield 
        t += params['dt']
        yield (params['A'] * sin(t / params['T']) + params['bias'] + 
        params['A2'] * sin(t / params['T2']) + params['bias'] + 
        params['A3'] * sin(t / params['T3']) + params['bias'])


def calc_step():
    my_sin = get_sin()
    my_sin2 = get_sin2()
    my_sin3 = get_sin3()

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

        old_q = params['q_go']
        for obj in structure:
            # params['q_go'] *= -1
            obj.step(last.get_out(), params)
            last = obj
        params['q_go'] = old_q    



def calc_animated():
    plotter = Plotter().animated_plot3d()
    plotter.send(None)

    structure = (
        SplittedHermeVolume(4, 2),
        SplittedHermeVolume(4, 2),
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
