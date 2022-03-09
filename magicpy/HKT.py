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

    def value(self) -> A:
        return self._value

    @staticmethod
    def with_value(v: B) -> HKT['Box', B]:
        return Box(v)

    def __repr__(self):
        return f"Box{{ {self._value} }}"


def from_to(a: HKT[BoxType, A], f: Callable[[A], B]) -> HKT[BoxType, B]:
    return a.with_value(f(a.value()))

