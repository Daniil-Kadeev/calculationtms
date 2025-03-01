import numpy as np

from HemreVolume import SplittedHermeVolume
from Plotter import Plotter


def main():
    params = {}

    params['dt'] = 0.5
    params['q_go'] = 200
    params['speed'] = 1

    dt = params['dt']
    t_list = [0, ]
    go = SplittedHermeVolume(10, 10)
    t_in_list = np.linspace(0, 20, 1000) 
    t_in_list = 10 * np.sin(t_in_list) + 293
    t_in_list = np.append(t_in_list, np.full(200, 293))
    t_in_list = np.full(2000, 300)


    for t_in in t_in_list:
        go.step(t_in, params)
        t_list.append(t_list[-1] + params['dt'])

    plotter = Plotter()
    plotter.plot3d([go, ], t_list)



if __name__ == '__main__':
    main()