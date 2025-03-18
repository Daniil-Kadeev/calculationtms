from HermeVolume import HermeVolum, SplittedHermeVolume
from HeatExchanger import HeatExchanger
from HeatGenerator import HeatGenerator
from RadiationHeatExchanger import RadiationHeatExchanger, SplittedRadiationHeatExchanger


class Multistructure():

    def __init__(self):
        self.he = HermeVolum(4)
        self.gl = HeatExchanger(type_exchanger='gas_liq')
        self.gg = HeatExchanger(type_exchanger='liq_liq')
        self.ro = RadiationHeatExchanger(6)

        self.flatten = (self.he, self.gl, self.gg, self.ro)

    
    def step_d(self, params):
        self.he.step_d(self.gl.get_out()[0], params)
        self.gl.step_d(
            (self.he.get_out(), self.gg.get_out()[0]),
            params
            )
        self.gg.step_d(
            (self.gl.get_out()[1], self.ro.get_out()),
            params
        )
        self.ro.step_d(self.gg.get_out()[1], params)


    def step_t(self):
        for obj in self.flatten:
            obj.step_t()


    def get_structure(self):
        return self.flatten