import functools
from functools import reduce
from typing import Generic, TypeVar, Iterator, Callable

T = TypeVar("T")


class Monoid(Generic[T]):

    def empty(self) -> T:
        ...

    def append(self, a: T, b: T) -> T:
        ...

    def appends(self, x: Iterator[T]) -> T:
        return reduce(lambda a, b: self.append(a, b), x)


class Maybe(Generic[T]):
    Maybe = TypeVar("Maybe")
    value: T

    @classmethod
    def empty(cls) -> Maybe:
        return _nil

    @classmethod
    def of_nullable(cls, v) -> Maybe:
        return Some(v) if v is not None else cls.empty()

    @classmethod
    def of(cls, v) -> Maybe:
        assert v is not None
        return Some(v)

    def is_present(self) -> bool:
        return self.value

    def get(self):
        return self.value


class Some(Maybe):

    def __init__(self, v: T):
        self.value = v


class Nil(Maybe):

    def __init__(self):
        self.value = None


_nil = Nil()


class MaybeM(Monoid[Maybe[T]]):

    def empty(self) -> Maybe[T]:
        return Maybe.empty()

    def append(self, a: Maybe[T], b: Maybe[T]) -> Maybe[T]:
        return a if a.is_present() else b


class OrderingM(Monoid[int]):

    def empty(self) -> int:
        return 0

    def append(self, a: int, b: int) -> int:
        return a if a != 0 else b


def int_tup_greater(a: tuple[int, ...], b: tuple[int, ...]):
    return a if OrderingM().appends([
        a[i] - b[i] for i in range(0, min(len(a), len(b)))
    ]) >= 0 else b


class ExtMonoid(Monoid[T]):

    def when(self, c: bool, then: T) -> T:
        return then if c else self.empty()

    def cond(self, c: bool, then: T, els: T) -> T:
        return then if c else els


class Todo(ExtMonoid[Callable]):

    def empty(self) -> Callable:
        return lambda: None

    @staticmethod
    def _lambda_call(a: Callable, b: Callable):
        a()
        b()

    def append(self, a: Callable, b: Callable) -> Callable:
        return functools.partial(Todo._lambda_call, a, b)
