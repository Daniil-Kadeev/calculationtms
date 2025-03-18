from collections import defaultdict
from math import sin


class HeatGenerator():

    def __init__(self, tip='q_go'):
        self.t = 0
        self.tip=tip

        self.rules = {
            'sin_1': self.get_sin_1,
            'sin_2': self.get_sin_2,
            'sin_3': self.get_sin_3,
            'orbit': self.get_sin_1_2,
        }


    
    def get_heat(self, params):
        self.t += params['dt']
        return self.rules.setdefault(params['rule_' + self.tip], self.non)(params)


    def non(self, params):
        self.t -= params['dt']
        return params[self.tip]


    def get_sin_1(self, params):
        return params['A'] * sin(self.t / params['T'] * 6) + params['bias']


    def get_sin_1_2(self, params):
        var = params['A1'] * sin(self.t / params['T1'] * 6 )
        return var if var > 0 else 0


    def get_sin_2(self, params):
        return (params['A'] * sin(self.t / params['T'] * 6) + params['bias'] + 
        params['A2'] * sin(self.t / params['T2'] * 6) + params['bias'])


    def get_sin_3(self, params):
        return (params['A'] * sin(self.t / params['T'] * 6) + params['bias'] + 
        params['A2'] * sin(self.t / params['T2'] * 6) + params['bias'] + 
        params['A3'] * sin(self.t / params['T3'] * 6) + params['bias'])
