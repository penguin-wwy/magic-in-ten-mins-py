from typing import TypeVar, Callable, Generic, Any

from magicpy.HKT import HKT
from magicpy.Monad import Monad

A = TypeVar("A")
B = TypeVar("B")
S = TypeVar("S")

_StateType = TypeVar("_StateType", covariant=True)
_ValueType = TypeVar("_ValueType", covariant=True)


class StateData(Generic[_StateType, _ValueType]):
    state: _StateType
    value: _ValueType

    def __init__(self, s, v):
        self.state = s
        self.value = v


class StateType(Generic[_StateType]):
    ...


class State(HKT['State', _ValueType], StateType[_StateType]):
    run_state: Callable[[_StateType], StateData[_StateType, _ValueType]]

    def __init__(self, f: Callable[[_StateType], StateData[_StateType, _ValueType]]):
        self.run_state = f

    def value(self) -> A:
        ...

    @staticmethod
    def with_value(v: A) -> 'State':
        ...


class StateM(Monad[State[S, A]]):
    # 读取
    get: State[S, S] = State(lambda s: StateData(s, s))

    # 写入
    def put(self, s: S):
        return State(lambda v: StateData(s, v))

    # 修改
    def modify(self, f: Callable[[A], A]):
        return State(lambda v: StateData(f(v), v))

    def pure(self, v: A) -> State[A, Any]:
        return State(lambda s: StateData(s, v))

    def flat_map(self, ma: State[A, S], f: Callable[[A], State[B, S]]) -> State[B, S]:
        def _state(s):
            data: StateData = ma.run_state(s)
            return f(data.value).run_state(data.state)

        return State(_state)


def fib(n: int):
    sm = StateM()
    if n == 0:
        return sm.flat_map(sm.get, lambda x: sm.pure(x[0]))
    if n == 1:
        return sm.flat_map(sm.get, lambda x: sm.pure(x[1]))
    return sm.flat_map(sm.modify(lambda x: (x[1], x[0] + x[1])), lambda v: fib(n - 1))
