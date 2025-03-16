import threading
import time
import sys
import json

import utils
#condaenv_antonov

parameters = {}
parameters['dt'] = 0.05
parameters['q_go'] = 2000
parameters['speed'] = 1
parameters['ws'] = 100
parameters['t_max'] = -1
parameters['t_min'] = -1
parameters['rs'] = 1
parameters['cs'] = 100
parameters['loop'] = True
parameters['rule'] = 'non'

parameters['bias'] = 0
parameters['A'] = 3000
parameters['T'] = 1 # умножаем на 6 - получаем истинный период

parameters['A2'] = 1500 
parameters['T2'] = 100 / 10
parameters['A3'] = 900
parameters['T3'] = 10 / 10


parameters_lock = threading.Lock()
print_lock = threading.Lock()


def calculation():
    calc = utils.calc_animated()
    calc.send(None)
    while True:
        with parameters_lock:
            params = parameters.copy()
        calc.send(params)


def input_parameters():
    while True:
        with print_lock:
            sys.stdout.write('\x1b[2;0H')
            sys.stdout.write('\x1b[2K')
            user_input = input('Введите параметр: ')
       
        try:
            if user_input.lower() == 'exit':
                sys.exit(0)
                
            key, value = user_input.split(maxsplit=1)
            if key.lower() == 'get':
                with open('parameters.json', 'w', encoding='utf-8') as f:
                    with parameters_lock:
                        json.dump(parameters, f, ensure_ascii=False, indent=4)
                continue
            elif key.lower() != 'rule':
                value = float(value) if '.' in value else int(value)
            
            with parameters_lock:
                parameters[key] = value

        except Exception as e:
            with print_lock:
                sys.stdout.write('\x1b[2;0H')
                sys.stdout.write('\x1b[2KОшибка: {}\n'.format(e))
                sys.stdout.flush()


def main():
    sys.stdout.write('\x1b[2J')  # Очищаем экран
    sys.stdout.write('\x1b[1;0H')  # Позиция для строки состояния
    sys.stdout.write('\n')  # Создаем место для ввода
    
    calcul_thread = threading.Thread(target=input_parameters)
    calcul_thread.daemon = True
    calcul_thread.start()

    calculation()
    



if __name__ == '__main__':
    main()