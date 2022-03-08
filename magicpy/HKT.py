from abc import abstractmethod
from typing import Generic, TypeVar, Callable

F = TypeVar("F")
A = TypeVar("A")
B = TypeVar("B")

'''
# type error code
def from_to(a: F[A], f: Callable[[A], B]) -> F[B]:
    ...
'''

'''
# no hint code
def from_to(a, f):
    pass
'''

BoxType = TypeVar('BoxType', covariant=True)
ValueType = TypeVar('ValueType', covariant=True)


class HKT(Generic[BoxType, ValueType]):
    """ Higher Kinded Type """

    @abstractmethod
    def value(self) -> ValueType:
        """ :return value """

    @staticmethod
    @abstractmethod
    def with_value(v: A) -> BoxType:
        """ :return new box instance """


class Box(HKT['Box', A]):

    def __init__(self, v: A):
        self._value = v

    @property
    def value(self) -> A:
        return self._value

    @staticmethod
    def with_value(v: B):
        return Box(v)


def from_to(a: HKT[BoxType, A], f: Callable[[A], B]) -> HKT[BoxType, B]:
    return a.with_value(f(a.value))


int_box = Box(1)
print(from_to(int_box, lambda x: x + 1).value)
assert from_to(int_box, lambda x: str(x)).value == "1"
