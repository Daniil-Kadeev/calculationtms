from HermeVolume import *
import test_animated
import utils
import HeatGenerator
import Plotter


parameters = {}
parameters['inventor'] = 1 # инвентирует подводимое тепло для каждого объекта структуры
parameters['input'] = 'True'      # есть ли вход? Если False - структура закольцована сама на себя
parameters['dt'] = 0.4
parameters['q_go'] = 1000        # генерация тепла в начальный момент (после применения rule, этот параметр остаётся последним значением из rule)
parameters['speed'] = 1     # устарело
parameters['ws'] = 100      # сколько последних тактов отображать
parameters['t_max'] = 296
parameters['t_min'] = 290
parameters['rs'] = 1        # частокол по длине структуры
parameters['cs'] = 10      # частоокол по времени
parameters['loop'] = 'True'
parameters['rule'] = 'sin_1'  # sin_1, sin_2, sin_3, any

parameters['bias'] = 0
parameters['A'] = 3000
parameters['T'] = 8 # умножаем на 6 - получаем истинный период

parameters['A2'] = 1500 
parameters['T2'] = 3
parameters['A3'] = 900
parameters['T3'] = 1


def test_2d(structure, plotter, generator):
    t = 0
    t_list = [t, ]
    heat = []
    t_lim = 100
    dt = parameters['dt']

    while t < t_lim:
        t += dt
        t_list.append(t)
        utils.calc(structure, generator, parameters)
        heat.append(parameters['q_go'])
    heat.append(parameters['q_go'])
    plotter.plot2d(structure, t_list, heat)


def test_2d_animated(structure, plotter, generator):
    pass


def test_3d(structure, plotter, generator):
    t = 0
    t_list = [t, ]
    heat = []
    t_lim = 100
    dt = parameters['dt']

    while t < t_lim:
        t += dt
        t_list.append(t)
        utils.calc(structure, generator, parameters)
        heat.append(parameters['q_go'])
    heat.append(parameters['q_go'])
    plotter.plot3d(structure, t_list)


def test_3d_animated(structure, plotter, generator):
    print(parameters)
    test_animated.start(structure, parameters)


def fast_test():
    time = 0.0  # секунды
    shag = 0.05  # секунды
    init_temp = 283.0

    # Параметры воздуха
    cp_air = 1005
    g_air = 2.487
    t_air_inp = 301
    alfa_air = 457.489
    f_air = 5
    m_air = g_air # Преобразование в кг/ч? (если G_air в тоннах)

    # Инициализация массивов
    temperatures_air = [init_temp]
    temperatures_liq = [init_temp]
    temperatures_wall = [init_temp]
    all_time = [time]

    # Параметры жидкости
    cp_liq = 1850
    g_liq = 1.081
    t_liq_inp = 288
    alfa_liq = 386.752
    f_liq = 6.009
    m_liq = 0.93 # Исправлено на G_liq

    # Параметры стенки
    c_wall = 2700
    m_wall = 5

    while time <= 100:
        # Текущие температуры из предыдущего шага
        t_air_out = temperatures_air[-1]
        t_liq_out = temperatures_liq[-1]
        t_wall = temperatures_wall[-1]

        # Расчет производных
        dt_air = (cp_air * g_air * (t_air_inp - t_air_out) + alfa_air * f_air * (t_wall - t_air_out)) / (cp_air * m_air)
        dt_liq = (cp_liq * g_liq * (t_liq_inp - t_liq_out) + alfa_liq * f_liq * (t_wall - t_liq_out)) / (cp_liq * m_liq)
        dt_wall = (alfa_air * f_air * (t_air_out - t_wall) + alfa_liq * f_liq * (t_liq_out - t_wall)) / (c_wall * m_wall)

        # Обновление времени
        time += shag

        # Расчет новых температур
        new_temp_air = temperatures_air[-1] + dt_air * shag
        new_temp_liq = temperatures_liq[-1] + dt_liq * shag
        new_temp_wall = temperatures_wall[-1] + dt_wall * shag

        # Добавление новых значений в массивы
        temperatures_air.append(new_temp_air)
        temperatures_liq.append(new_temp_liq)
        temperatures_wall.append(new_temp_wall)
        all_time.append(time)
    plt.plot(all_time, temperatures_air)
    plt.plot(all_time, temperatures_wall)
    plt.grid()
    plt.show()

# fast_test()

num = 1
test = 2
tests = {
    2: test_2d,
    20: test_2d_animated,
    3: test_3d,
    30: test_3d_animated
}

structures = {
    0: (HermeVolum(2), ),
    1: (SplittedHermeVolume(5, 2), ),
    2: (
        SplittedHermeVolume(5, 2),
        SplittedHermeVolume(5, 2),
    )
}

plotter = Plotter.Plotter()
generator = HeatGenerator.HeatGenerator()
tests[test](structures[num], plotter, generator)
