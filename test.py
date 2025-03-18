print('start')
import json

from HermeVolume import *
from RadiationHeatExchanger import *
from HeatExchanger import HeatExchanger
import test_animated
import utils
import HeatGenerator
import Plotter
from multistruct import Multistructure
from regulator import Regulator


def parse_value(value):
    if isinstance(value, (int, float)):
        return float(value)
    elif isinstance(value, str):
        try:
            # Пытаемся преобразовать строку напрямую в float
            return float(value)
        except ValueError:
            # Если не получается - вычисляем выражение
            return eval(value)
    else:
        raise TypeError(f"Unsupported type for value: {type(value)}")

with open('input_data.json', 'r') as f:
    data = json.load(f)

parameters = {key: parse_value(value) for key, value in data.items()}

parameters['clear'] = 'False' # не работает, нужно продумать логику изменения
parameters['step'] = 30         # отрисовывает график раз в n шагов
parameters['stop'] = 'False'    # останавливает счёт
parameters['plot'] = 'True'     # останавливает отрисовку графика
parameters['inventor'] = 1 # инвентирует подводимое тепло для каждого объекта структуры
parameters['input'] = 'True'      # есть ли вход? Если False - структура закольцована сама на себя
parameters['dt'] = 0.1
parameters['q_go'] = 2000      # генерация тепла в начальный момент (после применения rule, этот параметр остаётся последним значением из rule)
parameters['q'] = 0 
parameters['speed'] = 1     # устарело
parameters['ws'] = -1      # сколько последних тактов отображать
parameters['t_max'] = -1
parameters['t_min'] = 290
parameters['rs'] = 1        # частокол по длине структуры
parameters['cs'] = 100      # частоокол по времени
parameters['loop'] = 'True' # устарел
parameters['rule'] = 'sin_1'  # sin_1, sin_2, sin_3, orbit, any rule - устарел, теперь rule_q and rule_q_gi
parameters['rule_q'] = 'orbit'
parameters['rule_q_go'] = '0'

parameters['bias'] = 50
parameters['A'] = 340
parameters['T'] = 3600

parameters['A1'] = 340
parameters['T1'] = 3600 

parameters['A2'] = 1500 
parameters['T2'] = 3
parameters['A3'] = 900
parameters['T3'] = 1


def test_2d(structure, plotter, generator):
    t = 0
    t_list = [t, ]
    heat_q_go = []
    heat_q = []
    t_lim = 7200
    dt = parameters['dt']
    deq = []

    while t < t_lim:
        t += dt
        t_list.append(t)
        utils.calc(structure, generator, parameters, deq)
        heat_q_go.append(parameters['q_go'])
        heat_q.append(parameters['q'])

    heat_q_go.append(parameters['q_go'])
    heat_q.append(parameters['q'])
    plotter.plot2d(structure, t_list, [ heat_q])


def test_2d_animated(structure, plotter, generator):
    pass


def test_3d(structure, plotter, generator):
    t = 0
    t_list = [t, ]
    heat = []
    t_lim = 100
    dt = parameters['dt']
    deq = []

    while t < t_lim:
        t += dt
        t_list.append(t)
        utils.calc(structure, generator, parameters, deq)
        heat.append(parameters['q_go'])
    heat.append(parameters['q_go'])
    plotter.plot3d(structure, t_list, parameters)


def test_3d_animated(structure, plotter, generator):
    test_animated.start(structure, parameters, generator)


def test_multistruct_2d(structure, plotter, generator):
    t = 0
    t_list = [t, ]
    heat_q_go = []
    heat_q = []
    t_lim = 2000
    dt = parameters['dt']
    deq = []
 
    while t < t_lim:
        t += dt
        t_list.append(t)
        utils.calc_multistruct(structure, generator, parameters, deq)
        heat_q_go.append(parameters['q_go'])
        heat_q.append(parameters['q'])
        
    heat_q_go.append(parameters['q_go'])
    heat_q.append(parameters['q'])
    structure.calc_print()
    structure.get_data_xls([heat_q_go, heat_q], t_list, step=50)
    plotter.plot2d(structure.get_structure(), t_list)


def test_multistruct_3d(structure, plotter, generator):
    t = 0
    t_list = [t, ]
    heat = []
    t_lim = 100
    dt = parameters['dt']
    deq = []

    while t < t_lim:
        t += dt
        t_list.append(t)
        utils.calc_multistruct(structure, generator, parameters, deq)
        heat.append(parameters['q_go'])
    heat.append(parameters['q_go'])
    plotter.plot3d(structure.get_structure(), t_list, parameters)


test = 4
tests = {
    2: test_2d,
    20: test_2d_animated,
    3: test_3d,
    30: test_3d_animated,
    4: test_multistruct_2d,
    5: test_multistruct_3d
}

structure = 9
structures = {
    -1: (Regulator(parameters),),
    0: (HermeVolum(2, parameters), ),
    1: (SplittedHermeVolume(50, 2, parameters), ),

    2: (
        SplittedHermeVolume(5, 2, parameters),
        SplittedHermeVolume(5, 2, parameters),
    ),

    3: (HeatExchanger(parameters), ),
    4: (HeatExchanger(parameters, 'liq_liq'), ),
    5: (RadiationHeatExchanger(6, parameters), ),
    6: (SplittedRadiationHeatExchanger(12, 6, parameters), ),

    7: (
        HermeVolum(2, parameters), 
        RadiationHeatExchanger(1, parameters),
    ),

    8: (
        SplittedHermeVolume(10, 2, parameters), 
        SplittedRadiationHeatExchanger(10, 6, parameters),
    ),

    9: Multistructure(parameters)
}

plotter = Plotter.Plotter()
generator = (
    HeatGenerator.HeatGenerator(tip='q_go'),
    HeatGenerator.HeatGenerator(tip='q')
)

tests[test](structures[structure], plotter, generator)
