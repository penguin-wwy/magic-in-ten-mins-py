# 十分钟魔法练习：状态单子

### By 「玩火」改写 「penguin」

> 前置技能：Python基础，HKT，Monad

## 函数容器

很显然Python标准库中的各类容器都是可以看成是单子的， ~~我也不知道标准库有没有哪些给出了 `flatMap` 实现~~。不过在函数式的理论中单子不仅仅可以是实例意义上的容器，也可以是其他抽象意义上的容器，比如函数。

对于一个形如` Callable[[S], Complex[A]]` 形式的函数来说，我们可以把它看成包含了一个 `A` 的惰性容器，只有在给出 `S` 的时候才能知道 `A` 的值。对于这样形式的函数我们同样能写出对应的 `flatMap` ，这里就拿状态单子举例子。

## 状态单子

状态单子（State Monad）是一种可以包含一个“可变”状态的单子，我这里用了引号是因为尽管状态随着逻辑流在变化但是在内存里面实际上都是不变量。

其本质就是在每次状态变化的时候将新状态作为代表接下来逻辑的函数的输入。比如对于：

```python
i += 1
print(i)
```

可以用状态单子的思路改写成：

```python
(lambda v: print(v))(i + 1)
```

最简单的理解就是这样的一个包含函数的对象：

```python
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
```

这里为了好看定义了一个 `StateData` 类，包含变化后的状态和计算结果。而最核心的就是 `run_state` 函数对象，通过组合这个函数对象来使变化的状态在逻辑间传递。

`State` 是一个 Monad：

```python
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

```

`pure` 操作直接返回当前状态和给定的值， `flat_map` 操作只需要把 `ma` 中的 `A` 取出来然后传给 `f` ，并处理好 `state` 。

此外 `state` 中还定义一些常用的操作来读取写入状态：`get`、`put`、`modify`

使用的话这里举个求斐波那契数列的例子：

```python
def fib(n: int):
    sm = StateM()
    if n == 0:
        return sm.flat_map(sm.get, lambda x: sm.pure(x[0]))
    if n == 1:
        return sm.flat_map(sm.get, lambda x: sm.pure(x[1]))
    return sm.flat_map(sm.modify(lambda x: (x[1], x[0] + x[1])), lambda v: fib(n - 1))

assert fib(7).run_state((0, 1)).value == 13
```

`fib` 函数对应的 Haskell 代码是：

```haskell
fib :: Int -> State (Int, Int) Int
fib 0 = do
  (_, x) <- get
  pure x
fib n = do
  modify (\(a, b) -> (b, a + b))
  fib (n - 1)
```

~~看上去比 Java 版简单很多~~就当做跟Python也差不多简单吧 >_<

## 有啥用

看到这里肯定有人会拍桌而起：求斐波那契数列我有更简单的写法！

```python
def fib(n: int) -> int:
    a = [0, 1, 1]
    for i in range(n - 2):
        a[(i + 3) % 3] = a[(i + 2)] % 3 + a[(i + 1) % 3]
    return a[n % 3]
```

但问题是你用变量了啊， `State Monad` 最妙的一点就是全程都是常量而模拟出了变量的感觉。

更何况你这里用了数组而不是在递归，如果你递归就会需要在 `fib` 上加一个状态参数， `State Monad` 可以做到在不添加任何函数参数的情况下在函数之间传递参数。

同时它还是纯的，也就是说是**可组合**的，把任意两个状态类型相同的 `State Monad` 组合起来并不会有任何问题，比全局变量的解决方案不知道**高到哪里去**。



