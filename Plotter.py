from typing import List

import matplotlib.pyplot as plt
import numpy as np

from BaseUnit import BaseUnit, SplittedBaseUnit
from HemreVolume import HermeVolum, SplittedHermeVolume

class Plotter():
    
    def get_num_elements(self, objects):
        count = 0
        for obj in objects:
            if issubclass(type(obj), SplittedBaseUnit):
                count += obj.n
                for t in obj.get_full_t():
                    self.temperature_data.append(t)
            elif issubclass(type(obj), BaseUnit):
                count += 1
                self.temperature_data.append(obj.get_full_t())
        return count

    
    def from_list_into_array(self, lst):
        return np.array(list(map(np.array, lst)))


    def plot3d(self, objects: List, time: List):
        self.temperature_data = []
        num_elements = self.get_num_elements(objects)
        temperature_data = self.from_list_into_array(self.temperature_data)
        print(len(temperature_data[0]))

        length = np.arange(num_elements)
        time = time[-1]

        T, L = np.meshgrid(time, length)

        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(1, 1, 1, projection='3d')

        surf = ax.plot_surface(
            T, L, temperature_data,
            cmap='plasma',         # Цветовая схема
            rstride=1,             # Шаг сетки по времени
            cstride=2,             # Шаг сетки по длине
            linewidth=0.1,         # Толщина линий сетки
            antialiased=False,      # Сглаживание
            alpha=0.8              # Прозрачность
        )

        # Настройка оформления
        ax.set_xlabel('\nTime (seconds)', linespacing=2)
        ax.set_ylabel('\nLength', linespacing=2)
        ax.set_zlabel('\nTemperature (°C)', linespacing=2)
        ax.set_title('Temperature Distribution\n', fontsize=14)

        # Цветовая шкала
        cbar = fig.colorbar(surf, ax=ax, pad=0.1)
        cbar.set_label('Temperature (°C)', rotation=270, labelpad=15)

        plt.tight_layout()
        plt.show()