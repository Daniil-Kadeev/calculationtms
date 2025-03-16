import utils
#condaenv_antonov

parameters = {}
parameters['dt'] = 0.05
parameters['q_go'] = 2000
parameters['speed'] = 1
parameters['ws'] = 100
parameters['t_max'] = -1
parameters['t_min'] = -1
parameters['rs'] = 1
parameters['cs'] = 100
parameters['loop'] = True
parameters['rule'] = 'non'

parameters['bias'] = 0
parameters['A'] = 3000
parameters['T'] = 1 # умножаем на 6 - получаем истинный период

parameters['A2'] = 1500 
parameters['T2'] = 100 / 10
parameters['A3'] = 900
parameters['T3'] = 10 / 10


def calculation():
    calc = utils.calc_animated()
    calc.send(None)
    while True:

        params = parameters.copy()
        calc.send(params)

calculation()