from typing import Callable, TypeVar

T = TypeVar("T")
Supplier = Callable[[], T]


class InfIntList:
    InfIntList = TypeVar("InfIntList")
    head: int
    next_one: Supplier[InfIntList]

    def __init__(self, head: int, next_one: Supplier[InfIntList]):
        self.head = head
        self.next_one = next_one


def inf_alt():
    return InfIntList(1, lambda: InfIntList(2, inf_alt))
