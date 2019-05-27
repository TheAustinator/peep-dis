from copy import deepcopy
from termcolor import colored
import sys


def peep(obj, builtins=False, privates=False, truncate_len=250):
    obj = deepcopy(obj)
    obj_dir = dir(obj)
    output = ''
    if builtins is False:
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
        def out_func(*args):
            nonlocal output
            for str_ in args:
                str_ = shorten(str_, truncate_len)
                output += str_ + '\n'
    else:
        def out_func(*args):
            for arg in args:
                print(shorten(arg, truncate_len))

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


def shorten(item, max_len):
    str_ = str(item)
    if max_len:
        if len(str_) > max_len:
            str_ = str_[:max_len] + ' ...'
    return str_
