import threading
import time
import sys

import utils


parameters = {}
parameters['dt'] = 0.5
parameters['q_go'] = 2000
parameters['speed'] = 1
parameters['ws'] = 120
parameters['t_max'] = -1
parameters['t_min'] = -1
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