# 十分钟魔法练习：单子

### By 「玩火」改写 「penguin」

> 前置技能：Python基础，HKT

## 单子

单子(Monad)是指一种有一个类型参数的数据结构，拥有 `pure` （也叫 `unit` 或者 `return` ）和 `flatMap` （也叫 `bind` 或者 `>>=` ）两种操作：

```python
from typing import Generic, TypeVar, Callable

from magicpy.HKT import HKT

A = TypeVar("A")
B = TypeVar("B")
M = TypeVar("M")

class Monad(Generic[M]):

    def pure(self, v: A) -> HKT[M, A]:
        ...

    def flat_map(self, ma: HKT[M, A], f: Callable[[A], HKT[M, B]]) -> HKT[M, B]:
        ...
```

其中 `pure` 要求返回一个包含参数类型内容的数据结构， `flatMap` 要求把 `ma` 中的值经过 `f` 以后再串起来。

举个最经典的例子：

## List Monad

```python
class BoxM(Monad[Box]):

    def pure(self, v: A) -> HKT[Box, A]:
        return Box.with_value(v)

    def flat_map(self, ma: HKT[Box, A], f: Callable[[A], HKT[Box, B]]) \
            -> HKT[Box, B]:
        return f(ma.value())
```

简单来说 `pure(v)` 将得到 `Box{ v }` ，而 `flat_map(1, v -> [v, v + 1]})` 将得到 `Box{ [1, 2] }` 。这都是 Python 里面非常常见的操作了，并没有什么新意。

## Maybe Monad

Python 不是一个空安全的语言，也就是说任何对象类型的变量都有可能为 `null` 。对于一串可能出现空值的逻辑来说，判空常常是件麻烦事：

```python
def add_i(ma: Maybe[int], mb: Maybe[int]) -> Maybe[int]:
    return Maybe.with_value(ma.value() + ma.value()) \
        if ma.value() is not None and mb.value() is not None \
        else Maybe.with_value()
```

其中 `Maybe` 是个 `HKT` 的包装类型(注意与单位半群定义的Maybe区别)：

```python
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
```

像这样定义 `Maybe Monad` ：

```python
class MaybeM(Monad[Maybe]):

    def pure(self, v: A) -> HKT[Maybe, A]:
        return Maybe(v)

    def flat_map(self, ma: HKT[Maybe, A], f: Callable[[A], HKT[Maybe, B]]) -> HKT[Maybe, B]:
        return f(ma.value()) if ma.value() is not None else Maybe()
```

上面 `addI` 的代码就可以改成：

```python
def add_mi(ma: Maybe[int], mb: Maybe[int]) -> Maybe[int]:
    m = MaybeM()
    return m.flat_map(ma, lambda a: m.flat_map(mb, lambda b: m.pure(a + b)))
```

这样看上去就比上面的连续 `if-return` 优雅很多。在一些有语法糖的语言 (`Haskell`) 里面 Monad 的逻辑甚至可以像上面右边的注释一样简单明了。

> 我知道会有人说，啊，我有更简单的写法：
>
> ```java
> static Maybe<Integer>
> addE(Maybe<Integer> ma, 
>      Maybe<Integer> mb) {
>     try { return new Maybe<>(
>             ma.value + mb.value);
>     } catch (Exception e) {
>         return new Maybe<>();
>     }
> }
> ```
>
> 确实，这样写也挺简洁直观的， `Maybe Monad` 在有异常的 Java 里面确实不是一个很好的例子，不过 `Maybe Monad` 确实是在其他没有异常的函数式语言里面最为常见的 Monad 用法之一。而之后我也会介绍一些异常也无能为力的 Monad 用法。
