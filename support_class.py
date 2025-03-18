import numpy

from HeatExchanger import HeatExchanger


class Dummy():

    def __init__(self, obj):
        self.obj = obj


    def get_out(self):
        if type(self.obj) == HeatExchanger:
            return 301, 288
        return 293


class Flatten():

    def start(self, massive):
        self.update_lists()
        self.flatten_lists(massive)
        return self.get_lists()


    def get_lists(self):
        return self.flatten_massive


    def update_lists(self):
        self.flatten_massive = []


    def flatten_lists(self, massive):
        if type(massive[0]) == numpy.float16 or type(massive[0]) == numpy.float32 or type(massive[0]) == numpy.float64 or  type(massive[0]) == float: 
            self.flatten_massive.append(massive)
            return
        for obj in massive:
            self.flatten_lists(obj)