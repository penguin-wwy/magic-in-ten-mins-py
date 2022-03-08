# 十分钟魔法练习：单位半群

### By 「玩火」 改写 「penguin」

> 前置技能：Python基础

## 半群（Semigroup）

半群是一种代数结构，在集合 `A` 上包含一个将两个 `A` 的元素映射到 `A` 上的运算即 `<> : (A, A) -> A` ，同时该运算满足**结合律**即 `(a <> b) <> c == a <> (b <> c)` ，那么代数结构 `{<>, A}` 就是一个半群。

比如在自然数集上的加法或者乘法可以构成一个半群，再比如字符串集上字符串的连接构成一个半群。

## 单位半群（Monoid）

单位半群是一种带单位元的半群，对于集合 `A` 上的半群 `{<>, A}` ， `A` 中的元素 `a` 使 `A` 中的所有元素 `x` 满足 `x <> a` 和 `a <> x` 都等于 `x`，则 `a` 就是 `{<>, A}` 上的单位元。

举个例子， `{+, 自然数集}` 的单位元就是 0 ， `{*, 自然数集}` 的单位元就是 1 ， `{+, 字符串集}` 的单位元就是空串 `""` 。

用 Python 代码可以表示为：

```python
from functools import reduce
from typing import Generic, TypeVar, Iterator

T = TypeVar("T")


class Monoid(Generic[T]):
    def empty(self) -> T:
        ...

    def append(self, a: T, b: T) -> T:
        ...

    def appends(self, x: Iterator[T]) -> T:
        return reduce(lambda a, b: self.append(a, b), x)
```

## 应用：~~Optional~~Maybe

本质上Type hint只是个标签而已，所以如果需要Optional的效果的话需要先造一个，并且对它定义一个 Monoid ：

```python
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
```

这样对于 appends 来说我们将获得一串 Maybe 中第一个不为空的值，对于需要进行一连串尝试操作可以这样写：

```python
assert MaybeM[int]().appends([Maybe.of_nullable(x) for x in [None, 2, 3]]).get() == 2
```

## 应用：Ordering

对于 `Comparable` 接口可以构造出：

```python
class OrderingM(Monoid[int]):

    def empty(self) -> int:
        return 0

    def append(self, a: int, b: int) -> int:
        return a if a != 0 else b
```

同样如果有一串带有优先级的比较操作就可以用 appends 串起来，比如：

```python
def int_tup_greater(a: tuple[int, ...], b: tuple[int, ...]):
    return a if OrderingM().appends([
        a[i] - b[i] for i in range(0, min(len(a), len(b)))
    ]) >= 0 else b


assert int_tup_greater((5, 6, 7), (5, 4, 3, 2)) == (5, 6, 7)
```

这样的写法比一连串 `if-else` 优雅太多。

## 扩展

在 Monoid 接口里面加 default 方法可以支持更多方便的操作：

```python
import functools
from typing import Callable


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
```

然后就可以像下面这样使用上面的定义:

```python
Todo().appends([
    lambda: print(1),
    lambda: print(2),
    lambda: print(3),
])()
```
