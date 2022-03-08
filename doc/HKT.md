# 十分钟魔法练习：高阶类型

### By 「玩火」 改写 「penguin」

> 前置技能：Python基础

## 常常碰到的困难

写代码的时候常常会碰到语言表达能力不足的问题，比如下面这段用来给 `F` 容器中的值进行映射的代码：

```python
from typing import TypeVar, Callable

F = TypeVar("F")
A = TypeVar("A")
B = TypeVar("B")


def from_to(a: F[A], f: Callable[[A], B]) -> F[B]:
    pass
```

Python会告诉你`TypeError: 'TypeVar' object is not subscriptable`。

最简单粗暴的解决方案就是把type hint都删掉，如：

```python
def from_to(a, f):
    pass
```

## 高阶类型

假设类型的类型是 `Type` ，比如 `int` 和 `String` 类型都是 `Type` 。

而对于 `List` 这样带有一个泛型参数的类型来说，它相当于一个把类型 `T` 映射到 `List<T>` 的函数，其类型可以表示为 `Type -> Type` 。

同样的对于 `Dict` 来说它有两个泛型参数，类型可以表示为 `(Type, Type) -> Type` 。

像这样把类型映射到类型的非平凡类型就叫高阶类型（HKT, Higher Kinded Type）。

虽然Python中存在这样的高阶类型但是我们并不能用一个泛型参数表示出来，也就不能写出如上 `F<A>` 这样的代码了，因为 `F` 是个高阶类型。

> 如果加一层解决不了问题，那就加两层。

虽然在Python中不能直接表示出高阶类型，但是我们可以通过加一个中间层来在保留完整信息的情况下强类型地模拟出高阶类型。

首先，我们需要一个中间层：

```python
from typing import Generic, TypeVar

BoxType = TypeVar('BoxType', covariant=True)
ValueType = TypeVar('ValueType', covariant=True)

class HKT(Generic[BoxType, ValueType]):
    """ Higher Kinded Type """
```

然后我们就可以用 `HKT[BoxType, ValueType]` 来表示 `F<A>` ，这样操作完 `HKT` 后我们仍然有完整的类型信息来还原 `F<A>` 的类型。

这样，上面 `from_to` 就可以写成：

```python
from abc import abstractmethod
from typing import Generic, TypeVar, Callable

A = TypeVar("A")
B = TypeVar("B")
BoxType = TypeVar("BoxType", covariant=True)
ValueType = TypeVar("ValueType", covariant=True)

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

```

举个例子：

```python
int_box = Box(1)
assert from_to(int_box, lambda x: str(x)).value == "1"
```
