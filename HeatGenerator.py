from collections import defaultdict
from math import sin


class HeatGenerator():

    def __init__(self):
        self.t = 0

        self.rules = {
            'sin_1': self.get_sin_1,
            'sin_2': self.get_sin_2,
            'sin_3': self.get_sin_3
        }


    
    def get_heat(self, params):
        self.t += params['dt']
        return self.rules.setdefault(params['rule'], self.non)(params)


    def non(self, params):
        self.t -= params['dt']
        return params['q_go']


    def get_sin_1(self, params):
        return params['A'] * sin(self.t / params['T']) + params['bias']


    def get_sin_2(self, params):
        return (params['A'] * sin(self.t / params['T']) + params['bias'] + 
        params['A2'] * sin(self.t / params['T2']) + params['bias'])


    def get_sin_3(self, params):
        return (params['A'] * sin(self.t / params['T']) + params['bias'] + 
        params['A2'] * sin(self.t / params['T2']) + params['bias'] + 
        params['A3'] * sin(self.t / params['T3']) + params['bias'])
