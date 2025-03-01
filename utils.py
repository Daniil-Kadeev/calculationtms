from HemreVolume import SplittedHermeVolume
from Plotter import Plotter


def calc_step(structure, params):
    last = structure[-1]
    i = 0
    for obj in structure:
        if i == 2:
            params['q_go'] = -params['q_go']
        obj.step(last.get_out(), params)
        last = obj
        i += 1
    params['q_go'] = -params['q_go']


def calc_animated():
    plotter = Plotter().animated_plot3d()
    plotter.send(None)

    structure = (
        SplittedHermeVolume(3, 10),
        SplittedHermeVolume(3, 10),
        SplittedHermeVolume(3, 10),
        SplittedHermeVolume(3, 10)
    )

    t_list = [0, ]
    while True:
        params = yield
        calc_step(structure, params)
        t_list.append(t_list[-1] + params['dt'])
        plotter.send((structure, t_list, params))
