from math import sin
import time

from HeatGenerator import HeatGenerator
from HermeVolume import SplittedHermeVolume
from Plotter import Plotter


class Dummy():

    def get_out(self):
        return 293



def calc_step_d(structure, generator, params):
    params['q_go'] = generator.get_heat(params)
    old_q_go = params['q_go']
    if params['input'] == 'True':
        last = Dummy()
    else:
        last = structure[-1]

    for obj in structure:
        params['q_go'] *= int(params['inventor'])
        obj.step_d(last.get_out(), params)
        last = obj
    params['q_go'] = old_q_go


def calc_step_t(structure):
    last = structure[-1]
    for obj in structure:
        obj.step_t()
        last = obj


def calc(structure, generator, params):
    calc_step_d(structure, generator, params)
    calc_step_t(structure)


def calc_animated(structure):
    generator = HeatGenerator()
    plotter = Plotter().animated_plot3d()
    plotter.send(None)

    t_list = [0, ]

    while True:
        params = yield
        calc_step_d(structure, generator, params)
        calc_step_t(structure)
        t_list.append(t_list[-1] + params['dt'])
        plotter.send((structure, t_list, params))
