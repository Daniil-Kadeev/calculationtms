import pandas as pd
import numpy as np

from HermeVolume import HermeVolum, SplittedHermeVolume
from HeatExchanger import HeatExchanger
from HeatGenerator import HeatGenerator
from RadiationHeatExchanger import RadiationHeatExchanger, SplittedRadiationHeatExchanger
from regulator import Regulator
from support_class import Flatten


class Multistructure():

    def __init__(self):
        self.he = HermeVolum(4)
        self.gl = HeatExchanger(type_exchanger='gas_liq')
        self.gg = HeatExchanger(type_exchanger='liq_liq')
        self.ro = RadiationHeatExchanger(10)
        self.rg = Regulator()

        self.flatten = (self.he, self.gl, self.gg, self.ro)

    
    def step_d(self, params):
        self.he.step_d(self.gl.get_out()[0], params)
        self.gl.step_d(
            (self.he.get_out(), self.gg.get_out()[0]),
            params
            )

        inp_gg = self.ro.get_out() * self.rg.get_out() + self.gg.get_out()[1] * (1 -self.rg.get_out())
        # input((inp_gg, self.gg.get_out()[1], self.rg.get_out()))
        self.gg.step_d(
            (self.gl.get_out()[1], self.ro.get_out()),
            params
        )
        self.rg.step_d(self.he.get_out(), params)

        self.ro.g_cold = self.ro.g_cold_main * 1 #self.rg.get_out()
        self.ro.step_d(self.gg.get_out()[1], params)
        # input()


    def step_t(self):
        self.rg.step_t()
        for obj in self.flatten:
            obj.step_t()


    def get_structure(self):
        return self.flatten


    def get_data_xls(self, heat, time, step):
        title = [
                'Время',
                'ГО',
                'ГО ст',
                'ГЖТ Г',
                'ГЖТ Ж1',
                'ГЖТ ст',
                'ЖЖТ Ж1',
                'ЖЖТ Ж2',
                'ЖЖТ ст',
                'РТО Ж2',
                'РТО ст',
                'Генерируема теплота в ГО',
                'Падающий тепловой поток',
                'Регулятор положение',
                'Регулятор скорость'
            ]

        data = [
            time,
            self.he.get_full_t(),
            self.he.get_st(),
            self.gl.get_full_t(),
            self.gl.get_st(),
            self.gg.get_full_t(),
            self.gg.get_st(),
            self.ro.get_full_t(),
            self.ro.get_st(),
            heat,
            self.rg.get_full_t(),
            self.rg.get_speed(),
        ]
        f = Flatten()
        data = f.start(data)
        self.export_to_excel((title, data), 'out2.xlsx')


    def export_to_excel(self, tuple_data, filename, step=50):
        """
        Экспортирует данные из кортежа ([заголовки], [данные]) в Excel файл
        
        Параметры:
        tuple_data (tuple): Кортеж с двумя элементами:
                        - список заголовков столбцов
                        - список списков с числовыми данными
        filename (str): Имя файла для сохранения (например, 'data.xlsx')
        """
        # Создаем DataFrame из переданных данных
        data = np.array(tuple_data[1]).T
        sampled_data = data[::step]
        df = pd.DataFrame(sampled_data, columns=tuple_data[0])
        print(df)

    
        
        # Сохраняем в Excel
        df.to_excel(filename, index=False, engine='openpyxl')
        print(f"Данные успешно сохранены в файл {filename}")