from math import sin
import time
import pprint

from HeatGenerator import HeatGenerator
from HermeVolume import SplittedHermeVolume
from Plotter import Plotter
from support_class import Dummy, Flatten


def calc_step_d(structure, generator, params, deq):
    params['q_go'] = generator.get_heat(params)

    if params['input'] == 'True':
        last = Dummy(structure[0])
    else:
        last = structure[-1]

    for obj in structure:
        obj.step_d(last.get_out(), params)
        last = obj


def calc_step_t(structure):
    last = structure[-1]
    for obj in structure:
        obj.step_t()
        last = obj


def calc(structure, generator, params, deq):
    calc_step_d(structure, generator, params, deq)
    calc_step_t(structure)


def calc_animated(structure):
    generator = HeatGenerator()
    plotter = Plotter().animated_plot3d()
    plotter.send(None)
    deq = []

    t_list = [0, ]

    while True:
        params = yield
        if params['stop'] == 'True':
            time.sleep(2)
            continue

        calc_step_d(structure, generator, params, deq)
        calc_step_t(structure)
        t_list.append(t_list[-1] + params['dt'])
        plotter.send((structure, t_list, params))
