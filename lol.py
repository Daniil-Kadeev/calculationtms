import math 

import numpy as np 
import matplotlib.pyplot as plt


def get_temperature(end, A, T=1, clip_min=None):
    in_array = np.arange(0, end, 1)
    t_ce_list = A * np.sin(in_array / T) + 293

    if clip_min:
        t_ce_list = np.clip(t_ce_list, clip_min, None)
    return t_ce_list
def var_1():
    global p
    p_list = []
    for t_ce in t_ce_list:
        if (abs(t_ce - t_ust) < dt) or (p >= 1 and (t_ce > t_ust + dt)) or (p <= 0 and (t_ce < t_ust - dt)):
           dpdt = 0
        else:
            dpdt = (t_ce - t_ust) / (abs(t_ce - t_ust) + 0.0001) * b  
    
        p += dpdt
        if p > 1:
            p = 1
        elif p < 0:
            p = 0
        p_list.append(p)
    return p_list

t_ust = 293
t_ce_list = get_temperature(90, 10, 1)

dt = 5
b = 1 / 15
p = 2

dpdt = 0
p_list = var_1()





plt.plot(p_list)
plt.grid()
plt.show()