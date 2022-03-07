from typing import Generic, TypeVar

T = TypeVar("T")


class Expr(Generic[T]):
    pass


class IVal(Expr[int]):
    value: int


class BVal(Expr[bool]):
    value: bool


class Add(Expr[int]):
    e1: Expr[int]
    e2: Expr[int]


class Eq(Expr[bool]):
    e1: Expr[T]
    e2: Expr[T]
