from typing import List

import matplotlib.pyplot as plt
import numpy as np

from HeatExchanger import HeatExchanger
from BaseUnit import BaseUnit, SplittedBaseUnit
from HermeVolume import HermeVolum, SplittedHermeVolume
from support_class import Flatten


class Plotter():

    def __init__(self):
        self.first = True
        self.flatten = Flatten()
        self.counter = 0


    def get_last_t(self, objects):
        for obj in objects:
            if issubclass(type(obj), SplittedBaseUnit):
                for t in obj.get_last_t():
                    self.add_temperatures.append(t)
            elif type(obj) == HeatExchanger:
                for t in obj.get_last_t():
                    self.add_temperatures.append(t)     
            elif issubclass(type(obj), BaseUnit):
                self.add_temperatures.append(obj.get_last_t())

    
    def get_num_elements(self, objects):
        count = 0
        for obj in objects:
            if issubclass(type(obj), SplittedBaseUnit):
                count += obj.n
                for t in obj.get_full_t():
                    self.temperature_data.append(t)
            elif type(obj) == HeatExchanger:
                count += 2
                for t in obj.get_full_t():
                    self.temperature_data.append(t)               
            elif issubclass(type(obj), BaseUnit):
                count += 1
                self.temperature_data.append(obj.get_full_t())
        return count

    
    def from_list_into_array(self, lst):
        return np.array(lst, dtype=np.float32)
        # return np.array(list(map(np.array, lst)))


    def get_ax(self):
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(1, 1, 1, projection='3d')

        ax.set_xlabel('\nTime (seconds)', linespacing=2)
        ax.set_ylabel('\nLength', linespacing=2)
        ax.set_zlabel('\nTemperature (°C)', linespacing=2)
        ax.set_title('Temperature Distribution\n', fontsize=14)
        ax.view_init(elev=35, azim=-30)
        return ax, fig


    def plot2d(self, objects: List, time: List, heat: List=None):
        fig = plt.figure(figsize=(6, 4))
        ax = fig.add_subplot(1, 1, 1)

        ax.set_xlabel('\nTime (seconds)', linespacing=2)
        ax.set_ylabel('\nTemperature (°C)', linespacing=2)
        ax.set_title('Temperature Distribution\n', fontsize=14)

        self.temperature_data = []
        num_elements = self.get_num_elements(objects)
        self.temperature_data = self.from_list_into_array(self.temperature_data)
        
        for temperature in self.temperature_data:
            for t in self.flatten.start(temperature):
                ax.plot(time, t)

        if type(heat[0]) != list and heat != None:
            ax2 = ax.twinx()
            ax2.plot(time, heat, color='red', linestyle='--', label='Heat')
            ax2.set_ylabel('\nHeat (W)', linespacing=2, color='red')
            ax2.tick_params(axis='y', labelcolor='red')
        elif heat == None:
            pass
        else:
            ax2 = ax.twinx()
            for h in heat:
                    ax2.plot(time, h, color='red', linestyle='--', label='Heat')
                    ax2.set_ylabel('\nHeat (W)', linespacing=2, color='red')
                    ax2.tick_params(axis='y', labelcolor='red')                

        ax.grid()
        plt.tight_layout()
        plt.show()


    def plot3d(self, objects: List, time: List, params):
        ax, fig = self.get_ax()
        self.start(objects)
        long = self.temperature_data.shape[1]
        end_idx = long
        window_size = params['ws']
        if window_size == -1:
            start_idx = 0
        else:
            start_idx = max(0, long - window_size)

        display_data = self.temperature_data[:, start_idx:end_idx]
        display_time = time[start_idx:end_idx]
        print(self.length.shape)
        input()
        T, L = np.meshgrid(display_time, self.length)
        surf = ax.plot_surface(
            T, L, display_data,
            cmap='plasma',
            rstride=params['rs'],
            cstride=params['cs'],
            linewidth=0.1,
            alpha=0.8,
        )

        cbar = fig.colorbar(surf, ax=ax, pad=0.1)
        cbar.set_label('Temperature (°C)', rotation=270, labelpad=15)

        plt.tight_layout()
        plt.show()


    def start(self, objects):
        self.first = False
        self.temperature_data = []
        num_elements = self.get_num_elements(objects)
        self.temperature_data = self.from_list_into_array(self.temperature_data)
        self.length = np.arange(num_elements)    


    
    def add_data(self, objects):
        self.add_temperatures = []
        self.get_last_t(objects)
        self.temperature_data = np.hstack([self.temperature_data, np.array(self.add_temperatures).reshape(-1, 1)])


    def animated_plot3d(self):
        plt.ion()
        ax, fig = self.get_ax()
        surf = None
        cbar = None
        try:
            while True:
                objects, time, params = yield
                if self.first or params['clear'] == 'True': 
                    self.start(objects)
                    params['clear'] = 'False'
                else: 
                    self.add_data(objects)
                self.counter += 1

                if params['plot'] == 'False':
                    continue
                if not (params['step'] != 0 and self.counter % params['step'] == 0):
                    continue
                long = self.temperature_data.shape[1]
                end_idx = long
                window_size = params['ws']
                if window_size == -1:
                    start_idx = 0
                else:
                    start_idx = max(0, long - window_size)

                display_data = self.temperature_data[:, start_idx:end_idx]
                display_time = time[start_idx:end_idx]
                
                if surf is not None:
                    surf.remove()

                T, L = np.meshgrid(display_time, self.length)
                surf = ax.plot_surface(
                    T, L, display_data,
                    cmap='plasma',
                    rstride=params['rs'],
                    cstride=params['cs'],
                    linewidth=0.1,
                    alpha=0.8,
                )
                
                min_, max_ = params['t_min'], params['t_max']
                if min_ == -1 or max_ == -1:
                    ax.autoscale(enable=True, axis='z')  # Основной способ
                    ax.relim()              # Обновляем лимиты данных
                    ax.autoscale_view(scalex=False, scaley=False, scalez=True)  # Применяем
                else:
                    ax.set_zlim(min_, max_)

                ax.set_xlim(display_time[0], display_time[-1])

                plt.draw()
                plt.gcf().canvas.flush_events()
        except KeyboardInterrupt:
            plt.ioff()
            plt.show()
