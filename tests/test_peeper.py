"""

"""
from peepdis.core import CallablePeeper, Peeper
import pytest

# TODO: test idempotency of Peeper.peep


class AttrClass:
    def __init__(self, foo):
        self.foo = foo


class MethodClass:
    def method(self):
        return 5


class MethodArgClass:
    def method(self, c):
        return c


class MethodAnnotationsClass:
    def method_annotations(self, a: int, b: int) -> int:
        return a + b


class StaticMethodClass:
    @staticmethod
    def method_static(a):
        return a + 5


class ClassMethodClass(AttrClass):
    @classmethod
    def method_class(cls, foo):
        return cls(foo)


@pytest.fixture
def attr_peeper():
    obj = AttrClass('bar')
    return Peeper(obj)


@pytest.fixture
def annotation_peeper():
    obj = MethodAnnotationsClass().method_annotations
    return CallablePeeper(obj)


class TestArg:
    def test_null_args(self):
        pass

    def test_is_full(self):
        pass

    def test_getter_setter(self):
        pass

    def test_colored(self):
        pass


class TestOutput:
    def test_builtins(self):
        pass

    def test_str(self):
        pass


class TestAttr:
    def test_attrs(self, attr_peeper):
        attr_peeper.peep()
        assert attr_peeper.attrs == {'foo': 'bar'}
        assert not attr_peeper.methods
        assert not attr_peeper.errors
        # test that state updated to verbose
        attr_peeper.peep()


class TestForging:
    def test_infer_types(self, annotation_peeper):
        types_ = annotation_peeper._infer_types()
        expected = {'a': int, 'b': int}
        assert types_ == expected

    def test_forge(self, annotation_peeper):
        args = annotation_peeper.forge_args()
        expected = {'a': 0, 'b': 0}
        assert args == expected
        assert annotation_peeper.args.returns == 0

    def test_args_overwrite(self):
        pass

    def test_kwargs_overwrite(self):
        pass

    def test_partial_args_overwrite(self):
        pass

    def test_mixed_overwrite(self):
        pass


class ColorSchemeTest:
    def test_color_scheme_update(self):
        pass

