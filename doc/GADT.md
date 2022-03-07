# 十分钟魔法练习：广义代数数据类型

### By 「玩火」 改写 「penguin」

> 前置技能：Python基础，ADT

在 ADT 中可以构造出如下类型：

```python
# 构造函数已省去
class Expr:
    pass


class IVal(Expr):
    value: int
    
    
class BVal(Expr):
    value: bool
    
    
class Add(Expr):
    e1: Expr
    e2: Expr
    

class Eq(Expr):
    e1: Expr
    e2: Expr
```

但是这样构造有个问题，很显然 `BVal` 是不能相加的而这样的构造并不能防止构造出这样的东西。实际上在这种情况下ADT的表达能力是不足的。

一个比较显然的解决办法是给 `Expr` 添加一个类型参数用于标记表达式的类型：

```python
# 构造函数已省去
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

```

这样就可以避免构造出两个类型为 `Boolean` 的表达式相加，能构造出的表达式都是类型安全的。

注意到四个 `class` 的父类都不是 `Expr<T>` 而是包含参数的 `Expr` ，这和 ADT 并不一样。而这就是广义代数数据类型（Generalized Algebraic Data Type, GADT）。

