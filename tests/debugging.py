from peepdis.core import peep, Peeper, CallablePeeper
import numpy as np


class AttrClass:
    def __init__(self, foo):
        self.foo = foo


class MethodAnnotationsClass:
    def method_annotations(self, a: int, b: int) -> int:
        return a + b


if __name__ == '__main__':
    obj = np.array([1, 2, 3])
    peep(obj)
    # attr_peeper = Peeper(obj)
    # attr_peeper.peep(forge=True)
    # attr_peeper.print(verbose=True)
