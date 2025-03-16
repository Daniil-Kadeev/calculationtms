import threading
import time
import sys
import json

import utils
#condaenv_antonov

# parameters = {}
# parameters['inventor'] = 'False' # инвентирует подводимое тепло для каждого объекта структуры
# parameters['input'] = 'True'      # есть ли вход? Если False - структура закольцована сама на себя
# parameters['dt'] = 0.4
# parameters['q_go'] = 0        # генерация тепла в начальный момент (после применения rule, этот параметр остаётся последним значением из rule)
# parameters['speed'] = 1     # устарело
# parameters['ws'] = 100      # сколько последних тактов отображать
# parameters['t_max'] = -1
# parameters['t_min'] = -1
# parameters['rs'] = 1        # частокол по длине структуры
# parameters['cs'] = 100      # частоокол по времени
# parameters['loop'] = 'True'
# parameters['rule'] = 'sin_1'  # sin_1, sin_2, sin_3, any

# parameters['bias'] = 0
# parameters['A'] = 3000
# parameters['T'] = 8 # умножаем на 6 - получаем истинный период

# parameters['A2'] = 1500 
# parameters['T2'] = 3
# parameters['A3'] = 900
# parameters['T3'] = 1


parameters_lock = threading.Lock()
print_lock = threading.Lock()


def calculation(structure, parameters):
    calc = utils.calc_animated(structure)
    calc.send(None)

    while True:
        with parameters_lock:
            params = parameters.copy()
        # print('calculation  ' + (params['inventor']))
        calc.send(params)


def input_parameters(parameters):
    while True:
        with print_lock:
            sys.stdout.write('\x1b[2;0H')
            sys.stdout.write('\x1b[2K')
            user_input = input('Введите параметр: ')
       
        try:
            if user_input.lower() == 'exit':
                sys.exit(0)
                
            key, value = user_input.split()
            print(key, value)
            if key.lower() == 'get':
                with open('parameters.json', 'w', encoding='utf-8') as f:
                    with parameters_lock:
                        json.dump(parameters, f, ensure_ascii=False, indent=4)
                continue
            elif key.lower() not in ['rule', 'loop', 'input']:
                value = float(value) if '.' in value else int(value)
            
            with parameters_lock:
                parameters[key] = value

        except Exception as e:
            with print_lock:
                sys.stdout.write('\x1b[2;0H')
                sys.stdout.write('\x1b[2KОшибка: {}\n'.format(e))
                sys.stdout.flush()


def start(structure, parameters):
    sys.stdout.write('\x1b[2J')  # Очищаем экран
    sys.stdout.write('\x1b[1;0H')  # Позиция для строки состояния
    sys.stdout.write('\n')  # Создаем место для ввода
    
    calcul_thread = threading.Thread(target=input_parameters, args=(parameters, ))
    calcul_thread.daemon = True
    calcul_thread.start()

    calculation(structure, parameters)
    



if __name__ == '__main__':
    main()