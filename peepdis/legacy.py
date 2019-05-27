from copy import deepcopy
from termcolor import colored
from types import BuiltinMethodType, BuiltinFunctionType, FunctionType,\
    MethodType, ModuleType
import sys


def peep(obj, builtins=False, privates=False, docstrings=False,
         truncate_len=250):
    if not isinstance(obj, ModuleType):
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
                str_ = _shorten(str_, max_len=truncate_len)
                output += str_
            output += '\n'
    else:
        def out_func(*args):
            print(_shorten(*args, max_len=truncate_len))

    print(colored(getattr(obj, '__name__', ''), 'red'))
    doc = getattr(obj, '__doc__', '')
    if callable(obj):
        try:
            print(obj())
        except Exception as e:
            if 'required positional argument' \
                    or 'requires positional argument' in str(e):
                msg = '(requires positional argument)'
                msg_color = 'grey'
            else:
                msg = f'RAISES EXCEPTION : {e}'
                msg_color = 'red'
            out_func(
                colored(f'{obj}(): ', 'magenta'),
                colored(msg, msg_color),
                colored(doc, 'green'))
            print(colored('(requires positional args)', 'grey'))
        print(colored(obj.__doc__, 'green'))

    for item in obj_dir:
        item_str = f'obj.{item}'
        doc = ''
        try:
            attr = eval(item_str)
            if docstrings and attr.__doc__ is not None:
                doc = '\n' + attr.__doc__
            eval_str = str(attr)
            eval_str = '' if eval_str == 'None' else eval_str
            if callable(attr) is False:
                eval_str = _fix_if_multiline(eval_str)
                out_func(
                    colored(f'{item}: ', 'cyan'), eval_str,
                    colored(doc, 'green'))
        except (Exception, BaseException) as e:
            out_func(
                colored(f'{item}: ', 'cyan'),
                colored(f'RAISES EXCEPTION : {e}', 'red'),
                colored(doc, 'green'))
            continue
        if callable(attr):
            try:
                msg = str(attr())
                msg = _fix_if_multiline(msg)
                out_func(
                    colored(f'{item}(): ', 'magenta'),
                    msg,
                    colored(doc, 'green'))
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
                    colored(msg, msg_color),
                    colored(doc, 'green'))
                continue
    if debug:
        return output


class Peeper:
    def __init__(self, obj, builtins=False, privates=False, docstrings=False,
                 truncate_len=250):
        pass


def _shorten(*args, max_len=250):
    str_ = ''.join(args)
    if max_len:
        if len(str_) > max_len:
            str_ = str_[:max_len] + ' ...'
    return str_


def _fix_if_multiline(msg):
    if '\n' in msg:
        return '\n' + msg
    else:
        return msg