import types
from typing import TypeVar, Optional, List, Dict, Generic


class Student:
    name: str
    id: int


class Teacher:
    name: str
    office: str


SchoolPerson = Student | Teacher
assert isinstance(SchoolPerson, types.UnionType)


class TrueTy:
    pass


class FalseTy:
    pass


Bool = TrueTy | FalseTy

t = TrueTy()
assert isinstance(t, Bool)
assert isinstance(t, TrueTy)
assert not isinstance(t, FalseTy)
match t:
    case TrueTy():
        assert isinstance(t, TrueTy)
    case FalseTy():
        assert isinstance(t, FalseTy)
    case _:
        assert False


class Nat:
    pass


class Z(Nat):
    """ Zero """


class S(Nat):
    value: Nat

    def __init__(self, v):
        self.value = v


T = TypeVar("T")


class Node(Generic[T]):
    pass


class Nil(Node):
    pass


class Cons(Node):
    value: T
    next: Node

    def __init__(self, v, n):
        self.value = v
        self.next = n


class JsonValue:
    """ json value type """


class JsonBool(JsonValue):
    def __init__(self, v: bool):
        self.value: bool = v


class JsonInt(JsonValue):
    def __init__(self, v: int):
        self.value: int = v


class JsonString(JsonValue):
    def __init__(self, v: str):
        self.value: str = v


class JsonArray(JsonValue):
    def __init__(self, v: List[JsonValue]):
        self.value: List[JsonValue] = v


class JsonMap(JsonValue):
    def __init__(self, v: Dict[str, JsonValue]):
        self.value: Dict[str, JsonValue] = v
