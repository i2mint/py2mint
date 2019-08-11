try:
    import pytest
except ImportError as err:
    import warnings

    warnings.warn("You don't seem to have pytest, so I can't use it to test. Shame. pytest is nice.")
    warnings.warn(f"Error was: {err}")


def func(obj):
    return obj.a + obj.b


class A:
    e = 2

    def __init__(self, a=1, b=0, c=1, d=10):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def target_method(self, x):
        """Accesses ['a', 'b', 'c', 'e']"""
        t = func(self)  # and this function will access some attributes!
        tt = self.other_method(t)
        return x * tt / self.e

    def other_method(self, x=1):
        """Accesses ['c', 'e']"""
        w = self.c * 2  # c is accessed first
        return self.e + self.c * x - w  # and c is accessed again

    @classmethod
    def a_class_method(cls, y):
        """Accesses ['e']"""
        return cls.e + y


class B:
    x = 1
    y = 2
    b = 'i am b'
    c = 'i am not b'

    def __init__(self, a, greeting='hello', y=3):
        self.a = a
        self.greeting = greeting
        self.y = y  # instance y overwrites class y

    def greet(self, person='world'):
        """Accesses a, x, and y"""
        return str(self.a) + ' ' + person + '! ' + 'x+y=' + str(self.x + self.y)

    @property
    def z(self):
        """Accesses x and y"""
        return self.x + self.y

    def accessing_property_method(self):
        """Accesses b and z (and through z, x, and y)"""
        return len(self.b) + self.z

    def with_f_string(self):
        """Accesses greeting and x, but through f-string"""
        return f"{self.greeting} {self.x}"

    def writing_to_an_attribute(self, x_val, a_val):
        """Accesses x (class attr) and a (instance attr), but only to write in it.
        Should it be listed as "accessed".
        I say: Yes, if not too hard to do, but only if requested (what is NECESSARY) for
        the method to be computed is what is needed the most. Therefore only attrs that are getted, not setted.
        """
        self.x = x_val
        self.a = a_val


def convert_output():
    pass


def test_attrs_used_by_method():
    from py2mint.footprints import attrs_used_by_method

    assert attrs_used_by_method(A.target_method) == {'a', 'b', 'c', 'e'}
    assert attrs_used_by_method(A.other_method) == {'c', 'e'}
    assert attrs_used_by_method(A.a_class_method) == {'e'}

    assert attrs_used_by_method(B.greet) == {'a', 'x', 'y'}
    # assert attrs_used_by_method(B.z) == {'x', 'y'}
    # assert attrs_used_by_method(B.accessing_property_method) == {'b', 'z', 'x', 'y'}  # perhaps z should not be here?
    assert attrs_used_by_method(B.with_f_string) == {'greeting', 'x'}
    # assert attrs_used_by_method(B.writing_to_an_attribute) == {'x', 'a'}


def test_attrs_used_by_method_computation():
    from py2mint.footprints import attrs_used_by_method_computation

    assert attrs_used_by_method_computation(A.target_method, {}, {'x': 3}) == {'a', 'b', 'c', 'e'}
    assert attrs_used_by_method_computation(A.other_method, {}) == {'c', 'e'}
    # assert attrs_used_by_method_computation(A.a_class_method, {}, {'y': 3}) == {'e'}  # fails (returns {})

    init_kws = dict(a=100)
    assert attrs_used_by_method_computation(B.greet, init_kws) == {'a', 'x', 'y'}
    assert attrs_used_by_method_computation(B.z, init_kws) == {'x', 'y'}
    assert attrs_used_by_method_computation(
        B.accessing_property_method, init_kws) == {'b', 'z', 'x', 'y'}  # z or not z?
    assert attrs_used_by_method_computation(B.with_f_string, init_kws) == {'greeting', 'x'}
    assert attrs_used_by_method_computation(
        B.writing_to_an_attribute, init_kws, dict(x_val=0, a_val=1)) == {'x', 'a'}


## Order conserving
# def test_attrs_used_by_method():
#     from py2mint.footprints import attrs_used_by_method
#
#     assert attrs_used_by_method(A.target_method) == ['a', 'b', 'c', 'e']
#     assert attrs_used_by_method(A.other_method) == ['c', 'e']
#     assert attrs_used_by_method(A.a_class_method) == ['e']
#
#     assert attrs_used_by_method(B.greet) == ['a', 'x', 'y']
#     assert attrs_used_by_method(B.z) == ['x', 'y']
#     assert attrs_used_by_method(B.accessing_property_method) == ['b', 'z', 'x', 'y']  # perhaps z should not be here?
#     assert attrs_used_by_method(B.with_f_string) == ['greeting', 'x']
#     assert attrs_used_by_method(B.writing_to_an_attribute) == ['x', 'a']
#
#
# def test_attrs_used_by_method_computation():
#     from py2mint.footprints import attrs_used_by_method_computation
#
#     assert attrs_used_by_method_computation(A.target_method, {}, {'x': 3}) == ['a', 'b', 'c', 'e']
#     assert attrs_used_by_method_computation(A.other_method, {}) == ['c', 'e']
#     assert attrs_used_by_method_computation(A.a_class_method, {}) == ['e']
#
#     init_kws = dict(a=100)
#     assert attrs_used_by_method_computation(B.greet, init_kws) == ['a', 'x', 'y']
#     assert attrs_used_by_method_computation(B.z, init_kws) == ['x', 'y']
#     assert attrs_used_by_method_computation(
#         B.accessing_property_method, init_kws) == ['b', 'z', 'x', 'y']  # z or not z?
#     assert attrs_used_by_method_computation(B.with_f_string, init_kws) == ['greeting', 'x']
#     assert attrs_used_by_method_computation(
#         B.writing_to_an_attribute, init_kws, dict(x_val=0, y_val=1)) == ['x', 'a']