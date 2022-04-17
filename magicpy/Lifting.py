from typing import TypeVar, Callable, List

from magicpy.HKT import Box
from magicpy.Monad import BoxM

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")
M = TypeVar("M")


def lift0(f: A) -> M[A]:
    pass


def lift1(f: Callable[[A], B]) -> Callable[[M[A]], M[B]]:
    pass


def lift2(f: Callable[[A, B], C]) -> Callable[[M[A], M[B]], M[C]]:
    pass


def lift_m2box(f: Callable[[A, B], C]) -> Callable[[Box[A], Box[B]], Box[C]]:
    m: BoxM = BoxM()
    return lambda ma, mb: m.flat_map(Box(ma),
                                     lambda a: m.flat_map(Box(mb),
                                                          lambda b: m.pure(f(a, b)))).value()
