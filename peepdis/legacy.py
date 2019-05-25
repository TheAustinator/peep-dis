from copy import deepcopy
from termcolor import colored
import sys


def peep(obj, builtins=False, privates=False):
    obj = deepcopy(obj)
    obj_dir = dir(obj)
    if builtins is False:
        builtin_dir = dir(list) + dir(str) + dir(int) + dir(dict) + dir(tuple)
        obj_dir = [x for x in obj_dir if x not in builtin_dir]
        # remove dunders
        _is_dunder = lambda x: (x.startswith('__') and x.endswith('__'))
        obj_dir = [x for x in obj_dir if not _is_dunder(x)]

    if privates is False:
        _is_private = lambda x: (x.startswith('_') and not x.endswith('_'))
        obj_dir = [x for x in obj_dir if not _is_private(x)]

    # check if debugging and define output function
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace():
        debug = True
    else:
        debug = False
    if debug:
        output = ''

        def out_func(*args):
            nonlocal output
            for str_ in args:
                output += str_ + '\n'
    else:
        out_func = print

    for item in obj_dir:
        item_str = f'obj.{item}'
        try:
            attr = eval(item_str)
            eval_str = str(attr)
            if callable(attr) is False:
                out_func(colored(f'{item}: ', 'cyan'), eval_str)
        except (Exception, BaseException) as e:
            out_func(
                colored(f'{item}: ', 'cyan'),
                colored(f'RAISES EXCEPTION : {e}', 'red'))
            continue
        if callable(attr):
            try:
                out_func(colored(f'{item}(): ', 'magenta'), attr())
            except (Exception, BaseException) as e:
                if 'required positional argument'\
                        or 'requires positional argument' in str(e):
                    msg = '(requires positional argument)'
                    msg_color = 'grey'
                else:
                    msg = f'RAISES EXCEPTION : {e}'
                    msg_color = 'red'
                out_func(
                    colored(f'{item}(): ', 'magenta'),
                    colored(msg, msg_color))
                continue
    if debug:
        return output

