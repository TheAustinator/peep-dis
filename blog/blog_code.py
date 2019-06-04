from collections import OrderedDict
from copy import deepcopy
from inspect import getfullargspec
from types import BuiltinMethodType


def main():
    # show dir
    rect = Rectangle(3., 4.)
    print(dir(rect))
    # builtin filtering
    print(magic_filter(rect))
    print(builtin_type_filter(rect))
    dir_filtered = magic_filter(rect)
    # attribute and method separation
    attrs = filter_attrs(rect, dir_filtered)
    print(attrs)
    methods = filter_methods(rect, dir_filtered)
    print(methods)
    # evaluate attributes
    attr_outputs = {x: getattr(rect, x) for x in attrs}
    print(attr_outputs)
    # evaluate methods: leap before you look
    outputs = {x: attempt_call(get_callable(rect, x)) for x in methods}
    print(outputs)
    # getfullargspec
    print(getfullargspec(rect.scale))
    # evaluate methods: check for positionals
    outputs = {x: call_if_no_positionals(get_callable(rect, x))
               for x in methods}
    print(outputs)
    # infer args
    method_arg_types = {x: infer_arg_types(get_callable(rect, x))
                        for x in methods}
    print(method_arg_types)
    # forge args
    forged_outputs = forge_call_all(rect, _sample_args)
    print(forged_outputs)
    # state comparator
    outputs_incl_state = call_all_tracked(rect)
    print(outputs_incl_state)


class Rectangle:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def area(self) -> float:
        return self.a * self.b

    def scale(self, factor: float, ratio=1.0):
        """ scale the side lengths by `factor` """
        self.a = factor * self.a
        self.b = factor * self.b * ratio

    def take_half(self):
        """ cut in half and return the "other half" """
        self.a /= 2
        return Rectangle(self.a, self.b)

    def __str__(self):
        return self.__class__.__name__ + str({'a': self.a, 'b': self.b})


def magic_filter(obj):
    is_magic = lambda x: (x.startswith('__') and x.endswith('__'))
    return [x for x in dir(obj) if not is_magic(x)]


def builtin_type_filter(obj):
    is_builtin = lambda x: isinstance(getattr(obj, x), BuiltinMethodType)
    return [x for x in dir(obj) if not is_builtin(x)]


def filter_attrs(obj, name_list):
    return [x for x in name_list if not callable(getattr(obj, x))]


def filter_methods(obj, name_list):
    return [x for x in name_list if callable(getattr(obj, x))]


def get_callable(obj, name: str):
    return getattr(deepcopy(obj), name)


def attempt_call(func):
    try:
        return str(func())
    except:
        return '(failed to evaluate method)'


def _remove_self(arg_list):
    """ remove implicit `self` argument from list of arg names """
    if 'self' in arg_list:
        arg_list.remove('self')


def call_if_no_positionals(func):
    try:
        spec = getfullargspec(func)
    except TypeError:
        return '(unsupported callable)'
    args = spec.args
    if 'self' in args:
        args.remove('self')
    n_defaults = len(spec.defaults) if spec.defaults else 0
    if len(args) == n_defaults:
        return str(func())
    else:
        return '(requires positional args)'


def infer_arg_types(func):
    try:
        spec = getfullargspec(func)
    except TypeError:
        return '(unsupported callable)'
    arg_types = OrderedDict()
    args = spec.args
    _remove_self(args)
    # infer types from type hints
    for arg in args:
        type_ = spec.annotations.get(arg, None)
        arg_types[arg] = type_.__name__ if type_ is not None else None
    # infer types from default args
    if spec.defaults:
        for i, v in enumerate(spec.defaults):
            arg_i = - len(spec.defaults) + i
            arg = args[arg_i]
            arg_types[arg] = type(v).__name__
    if not arg_types:
        return None
    return arg_types


_sample_args = {
    'float': 1.5,
    'int': 2,
    'str': 'abc',
    'typing.List[int]': [1, 2, 3],
}


class ForgeError(ValueError):
    pass


def forge_args(func, sample_dict=_sample_args):
    arg_types = infer_arg_types(func)
    # If no positional arguments
    if not arg_types:
        return {}
    # If not all types could be inferred
    if not all(arg_types.values()):
        raise ForgeError(f'Some arguments have unknown types')

    arg_dict = OrderedDict()
    for i, (arg, type_) in enumerate(arg_types.items()):
        # check for default values if keyword arg
        defaults = getfullargspec(func).defaults
        n_args_remaining = len(arg_types) - i
        if len(defaults) >= n_args_remaining:
            arg_dict[arg] = defaults[- n_args_remaining]
        # if no defaults, attempt to forge from _sample_dict
        elif type_ in _sample_args:
            arg_dict[arg] = sample_dict[type_]
        else:
            raise ForgeError(
                f'Unsupported argument type ({type_}) for argument: {arg}')
    return arg_dict


def forge_call_all(obj, sample_dict=_sample_args):
    dir_filtered = magic_filter(obj)
    method_names = filter_methods(obj, dir_filtered)
    output_dict = {}
    for name in method_names:
        method = get_callable(obj, name)
        try:
            arg_dict = forge_args(method, sample_dict)
            output_dict[name] = str(method(**arg_dict))
        except ForgeError:
            output_dict[name] = "(Failed to forge args)"
        except Exception:
            output_dict[name] = "(Failed to run method with forged args)"
    return output_dict


class StateComparator:
    def __init__(self, obj):
        self.state = deepcopy(obj.__dict__)

    def compare(self, other):
        state_1 = self.state
        state_2 = deepcopy(other.__dict__)
        new_attrs = {k: v for k, v in state_2.items() if k not in state_1}
        del_attrs = {k: v for k, v in state_1.items() if k not in state_2}
        mod_attrs = {k: (v, state_2[k]) for k, v in state_1.items()
                     if v != state_2[k]}
        change_dict = {}
        if new_attrs:
            change_dict['new'] = new_attrs,
        if del_attrs:
            change_dict['deleted'] = del_attrs
        if mod_attrs:
            change_dict['modified'] = mod_attrs
        return change_dict


def call_all_tracked(obj, sample_dict=_sample_args, forge=True):
    dir_filtered = magic_filter(obj)
    method_names = filter_methods(obj, dir_filtered)
    output_dict = {}
    for name in method_names:
        obj_2 = deepcopy(obj)
        # store initial state
        state = StateComparator(obj_2)
        method = getattr(obj_2, name)
        try:
            if forge is True:
                arg_dict = forge_args(method, sample_dict)
            else:
                arg_dict = {}
            output_dict[name] = str(method(**arg_dict))
        except ForgeError:
            output_dict[name] = "(Failed to forge args)"
        except Exception:
            output_dict[name] = "(Failed to run method with forged args)"
        # check for state changes
        change_dict = state.compare(obj_2)
        if change_dict:
            output_dict[name] = {
                'output': output_dict[name],
                'state changes': change_dict,
            }
        # remove 'output' entry in `output_dict` if no output
        if isinstance(output_dict[name], dict):
            if output_dict[name]['output'] == 'None':
                del output_dict[name]['output']
    return output_dict


class StateWrapperMeta(type):
    def __new__(cls, arg):
        pass


if __name__ == '__main__':
    main()
