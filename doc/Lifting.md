# 十分钟魔法练习：提升

### By 「玩火」改写 「penguin」

> 前置技能：Python基础，HKT，Monad

## 概念

提升（Lifting）指的是把一个通用函数变成容器映射函数的操作。

比如把 `Callable[[A], B]` 变成 `Callable[[M[A]], M[B]]` 就是一种提升操作。而由于被操作的函数有一个参数所以这个操作也叫 `lift1` 。

注意被提升的函数可以有不止一个参数，我们也可以把 `Callable[[A, B], C]` 提升为 `Callable[[M[A], M[B]], M[C]]` 。这样两个参数的提升可以称为 `lift2` 。

同样，被提升的函数可以没有参数，这时候我们可以看成没有这个函数，也就是把 `A` 提升为 `M[A]` 。这样的提升可以称为 `lift0` 。实际上它也和 `Monad` 中的 `pure` 是同构的。

也就是说：

```python
from typing import TypeVar, Callable


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
```

## fmap

看到这个函数签名肯定有人会拍案而起：这不就是 fmap 么？

fmap is a lifting surly. 因为它符合 lifting 的函数签名，但是 lifting 并不一定是 fmap 。只要符合这样的函数签名就可以说是一个 lifting 。

比如对于 list 来说 `f -> x -> x.tail().map(f)` 也符合 lifting 的函数签名但很显然它不是一个 `fmap` 函数。或者说很多改变结构的函数和 `fmap` 组合还是一个 lifting 函数。

## 除此之外呢

回到上面那个函数签名，里面有个非泛型的参数 `M` ，这个 `M` 可以是个泛型参数，可以是个包装器比如 `Maybe` ，也可以是个线性容器比如 `List` ，可以是个非线性的容器比如 `Set` ，甚至可以是抽象容器比如 `Function` 。

同时提升操作也可能对容器结构做出一些改变，尤其是对于多参函数的提升可能会对函数的参数做出一些组合。比如对于 `List` 来说 `lift2` 既可以是 `zipMap` 也可也是以 `f` 为操作的卷积。

## liftM

对于 Monad 来说，存在一种通用的提升操作叫 `liftM` ，比如对于 `Box` 来说 `liftM2` 就是：

```python
def lift_m2box(f: Callable[[A, B], C]) -> Callable[[Box[A], Box[B]], Box[C]]:
    m: BoxM = BoxM()
    return lambda ma, mb: m.flat_map(Box(ma), 
                                     lambda a: m.flat_map(Box(mb), 
                                                          lambda b: m.pure(f(a, b)))).value()
```

再比如 `liftM5` 在 `Haskell` 中的表述为：

```haskell
liftM5 f ma mb mc md me = do
  a <- ma
  b <- mb
  c <- mc
  d <- md
  e <- me
  pure (f a b c d e)
```

也就是 `liftM[n]` 就相当于嵌套 `n` 层 `flatMap` 提取 `Monad` 中的值然后应用给被提升的函数。