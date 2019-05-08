from termcolor import colored
from copy import deepcopy


def peep(obj, verbose=False):
    obj = deepcopy(obj)
    obj_dir = dir(obj)
    if verbose is False:
        builtin_dir = dir(list) + dir(str) + dir(int) + ['__dict__', '__module__', '__weakref__']
        obj_dir = [item for item in obj_dir if item not in builtin_dir]
    for item in obj_dir:
        item_str = f'obj.{item}'
        try:
            eval_str = str(eval(item_str))
            if eval_str.startswith('<'):
                eval_str = colored(eval_str, 'grey')
            print(colored(f'{item}: ', 'cyan'), eval_str)
        except (Exception, BaseException) as e:
            print(colored(f'{item}: ', 'cyan'), colored(f'RAISES EXCEPTION : {e}', 'red'))
            continue
        if '__call__' in dir(eval(item_str)):
            call_str = f'obj.{item}()'
            try:
                print(colored(f'{item}(): ', 'magenta'), eval(call_str))
            except (Exception, BaseException) as e:
                if 'required positional argument' or 'requires positional argument' in str(e):
                    print(colored(f'{item}(): ', 'magenta'), colored('(requires positional argument)', 'grey'))
                else:
                    print(colored(f'{item}(): ', 'magenta'), colored(f'RAISES EXCEPTION : {e}', 'red'))
                continue
