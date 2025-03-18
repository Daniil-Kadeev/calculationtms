import threading
import time
import sys
import json

import utils
#condaenv_antonov


parameters_lock = threading.Lock()
print_lock = threading.Lock()


def calculation(structure, parameters, generator):
    calc = utils.calc_animated(structure, generator)
    calc.send(None)

    while True:
        with parameters_lock:
            params = parameters.copy()
        calc.send(params)


def input_parameters(parameters):
    while True:
        with print_lock:
            # sys.stdout.write('\x1b[2;0H')
            # sys.stdout.write('\x1b[2K')
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
            if key.lower() not in ['rule', 'loop', 'input', 'stop', 'plot']:
                value = float(value) if '.' in value else int(value)
            
            with parameters_lock:
                parameters[key] = value

        except Exception as e:
            with print_lock:
                sys.stdout.write('\x1b[2;0H')
                sys.stdout.write('\x1b[2KОшибка: {}\n'.format(e))
                sys.stdout.flush()


def start(structure, parameters, generator):
    sys.stdout.write('\x1b[2J')  # Очищаем экран
    sys.stdout.write('\x1b[1;0H')  # Позиция для строки состояния
    sys.stdout.write('\n')  # Создаем место для ввода
    
    calcul_thread = threading.Thread(target=input_parameters, args=(parameters, ))
    calcul_thread.daemon = True
    calcul_thread.start()

    calculation(structure, parameters, generator)
    



if __name__ == '__main__':
    main()