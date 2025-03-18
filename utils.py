from math import sin
import time
import pprint

from HeatGenerator import HeatGenerator
from HermeVolume import SplittedHermeVolume
from Plotter import Plotter
from support_class import Dummy, Flatten
from multistruct import Multistructure


def calc_step_d(structure, generator, params, deq):
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
    params['q_go'] = generator[0].get_heat(params)
    params['q'] =generator[1].get_heat(params)

    calc_step_d(structure, generator, params, deq)
    calc_step_t(structure)


def calc_order(structure, generator, params, deq):
    calc(structure, generator, params, deq)
    return structure


def calc_multistruct(structure, generator, params, deq):
    params['q_go'] = generator[0].get_heat(params)
    params['q'] =generator[1].get_heat(params)
    structure.step_d(params)
    structure.step_t()
    return structure.get_structure()


def calc_animated(structure, generator):
    plotter = Plotter().animated_plot3d()
    plotter.send(None)
    deq = []

    t_list = [0, ]

    funcs = {
        tuple: calc_order,
        Multistructure: calc_multistruct
    }
    func = funcs[type(structure)]

    while True:
        params = yield
        if params['stop'] == 'True':
            time.sleep(2)
            continue

        t_list.append(t_list[-1] + params['dt'])
        plotter.send((
            func(structure, generator, params, deq),
            t_list,
            params
        ))
