from math import sin


class HeatGenerator():

    def get_sin(self):
        t = 0
        while True:
            params = yield 
            t += params['dt']
            yield params['A'] * sin(t / params['T']) + params['bias']


    def get_sin2(self):
        t = 0
        while True:
            params = yield 
            t += params['dt']
            yield (params['A'] * sin(t / params['T']) + params['bias'] + 
            params['A2'] * sin(t / params['T2']) + params['bias'])


    def get_sin3(self):
        t = 0
        while True:
            params = yield 
            t += params['dt']
            yield (params['A'] * sin(t / params['T']) + params['bias'] + 
            params['A2'] * sin(t / params['T2']) + params['bias'] + 
            params['A3'] * sin(t / params['T3']) + params['bias'])