from types import NoneType
from typing import Generic, TypeVar, Callable

from magicpy.HKT import HKT, Box

A = TypeVar("A")
B = TypeVar("B")
M = TypeVar("M")


class Monad(Generic[M]):

    def pure(self, v: A) -> HKT[M, A]:
        ...

    def flat_map(self, ma: HKT[M, A], f: Callable[[A], HKT[M, B]]) -> HKT[M, B]:
        ...


class BoxM(Monad[Box]):

    def pure(self, v: A) -> HKT[Box, A]:
        return Box.with_value(v)

    def flat_map(self, ma: HKT[Box, A], f: Callable[[A], HKT[Box, B]]) \
            -> HKT[Box, B]:
        return f(ma.value())


class Maybe(HKT['Maybe', A]):

    def __init__(self, v: A = None):
        self._value = v

    def value(self) -> A:
        return self._value

    @staticmethod
    def with_value(v: A | NoneType = None) -> 'Maybe':
        return Maybe(v)

    def __repr__(self):
        return f"Maybe{{ {self._value} }}"


def add_i(ma: Maybe[int], mb: Maybe[int]) -> Maybe[int]:
    return Maybe.with_value(ma.value() + ma.value()) \
        if ma.value() is not None and mb.value() is not None \
        else Maybe.with_value()


class MaybeM(Monad[Maybe]):

    def pure(self, v: A) -> HKT[Maybe, A]:
        return Maybe(v)

    def flat_map(self, ma: HKT[Maybe, A], f: Callable[[A], HKT[Maybe, B]]) -> HKT[Maybe, B]:
        return f(ma.value()) if ma.value() is not None else Maybe()


def add_mi(ma: Maybe[int], mb: Maybe[int]) -> Maybe[int]:
    m = MaybeM()
    return m.flat_map(ma, lambda a: m.flat_map(mb, lambda b: m.pure(a + b)))
