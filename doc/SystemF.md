# 十分钟魔法练习：系统 F

### By 「玩火」改写 「penguin」

> 前置技能：Python 基础，ADT，简单类型 λ 演算

简单类型 λ 演算的类型系统非常简单，比常见的 C++, Java, Python 语言的类型系统表现力差远了。而如果往简单类型 λ 演算的表达式中加入类型函数定义和类型函数应用来联系类型和表达式就可以大大增强其表现力，这样的类型系统被称为系统 F （System F）。

类型函数定义 `Λ t. E` 定义了一个类型变量 `t` ，可以在表达式 `E` 中使用，其类型是 `∀ t. [Typeof(E)]` 。

类型函数应用 `F T` 类似于函数应用，当 `F` 的类型为 `∀ t. E` 时 `F T` 的类型是 `E(t → T)` ，也就是 `E` 中所有自由的 `t` 被替换为 `T` 。  

比如 `true` 的定义可以写成：

```
true = Λ a. λ (x: a). λ (y: a). (x: a)
```

其类型是：

```
∀ a. a → a → a
```

这就有点类似 Python 中的泛型函数：

```python
from typing import TypeVar

A = TypeVar("A")


def true(x: A, y: A) -> A:
    return x

```

而类型函数应用就像是给函数填入泛型参数的类型，像这样：

```
Λ x. true x
```

会得到 `true` 本身。

表达式中加入了新东西那么显然类型系统也需要有一些改变，系统 F 的类型系统由类型变量 `x` ，类型函数 `∀ t. E` ，函数类型 `a → b` 构成：

```python
class Type:
    ...


class TVal(Type):
    x: str
    uid: UUID

    def __str__(self):
        return self.x


class TForall(Type):
    x: Type
    e: Type
    
    def __str__(self):
        return f"(∀ {self.x}. {self.e})"
    
    
class TArr(Type):
    a: Type
    b: Type
    
    def __str__(self):
        return f"({self.a} -> {self.b})"
```

注意 `TVal` 的 `uid` 字段是像无类型 λ 演算中一样 `equals` 函数只需要比较 `uid` 字段。

既然有类型函数那就需要有类似函数应用的操作来填入类型参数，同时还需要函数来生成 `UUID` ：

```python
class Type:

    def apply(self, x: 'TVal', t: 'Type') -> 'Type':
        ...

    def gen_uuid(self) -> 'Type':
        ...

    def apply_uuid(self, v: 'TVal') -> 'Type':
        ...


class TVal(Type):
    x: str
    uid: UUID

    def __init__(self, x, uid):
        self.x = x
        self.uid = uid

    def __str__(self):
        return self.x

    def __eq__(self, other):
        return self.uid == other.uid if other is not None and isinstance(other, TVal) else False

    def apply(self, x: 'TVal', t: 'Type') -> 'Type':
        return t if self == x else self

    def gen_uuid(self) -> 'Type':
        return self

    def apply_uuid(self, v: 'TVal') -> 'Type':
        return TVal(self.x, v.uid) if self.x == v.x else self


class TForall(Type):
    x: TVal
    e: Type

    def __init__(self, x, e):
        self.x = x
        self.e = e

    def __str__(self):
        return f"(∀ {self.x}. {self.e})"

    def __eq__(self, other):
        if self is other:
            return True
        elif other is not None and isinstance(other, TForall):
            return self.e == other.e.apply(other.x, self.x)
        else:
            return False

    def apply(self, x: 'TVal', t: 'Type') -> 'Type':
        return self if self.x == x else self.e.apply(x, t)

    def gen_uuid(self) -> 'Type':
        if self.x.uid is None:
            v = TVal(self.x.x, uuid4())
            return TForall(v, self.e.apply_uuid(v).gen_uuid())
        return TForall(self.x, self.e.gen_uuid())

    def apply_uuid(self, v: 'TVal') -> 'Type':
        return self if self.x.x == v.x else TForall(self.x, self.e.apply_uuid(v))


class TArr(Type):
    a: Type
    b: Type
    
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return f"({self.a} -> {self.b})"
    
    def apply(self, x: 'TVal', t: 'Type') -> 'Type':
        return TArr(self.apply(x, t), self.b.apply(x, t))
    
    def gen_uuid(self) -> 'Type':
        return TArr(self.a.gen_uuid(), self.b.gen_uuid())

    def apply_uuid(self, v: 'TVal') -> 'Type':
        return TArr(self.a.apply_uuid(v), self.b.apply_uuid(v))

```

这里的实现和无类型 λ 演算很像。不过要注意 `TForall` 的 `equals` 函数实现，在比较前需要先把变量统一一下。

再在简单类型 λ 演算的基础上给表达式加上类型函数定义和类型函数应用，同时还需要协助类型系统生成类型的 `UUID` ：

```python
class Expr:
    def check_type(self, env: Env) -> Type:
        ...
    
    def gen_uuid(self) -> 'Expr':
        ...
    
    def apply_uuid(self, v: TVal) -> 'Expr':
        ...
    
class Val: """ 省略实现 """
class Fun: """ 省略实现 """
class App: """ 省略实现 """

# 类型函数定义
class Forall(Expr):
    x: TVal
    e: Expr

    def __init__(self, x, e):
        self.x = x
        self.e = e

    def check_type(self, env: Env) -> Type:
        return TForall(self.x, self.e.check_type(env))

    def gen_uuid(self) -> 'Expr':
        if self.x.uid is None:
            v = TVal(self.x.x, uuid4())
            return Forall(v, self.e.apply_uuid(v).gen_uuid())

    def apply_uuid(self, v: TVal) -> 'Expr':
        return self if self.x.x == v.x else Forall(self.x, self.e.apply_uuid(v))

# 类型函数应用
class AppT(Expr):
    e: Expr
    t: Type

    def __init__(self, e, t):
        self.e = e
        self.t = t

    def check_type(self, env: Env) -> Type:
        te = self.e.check_type(env)
        if isinstance(te, TForall):
            return te.e.apply(te.x, self.t)
        raise TypeError()

    def gen_uuid(self) -> 'Expr':
        return AppT(self.e.gen_uuid(), self.t.gen_uuid())

    def apply_uuid(self, v: TVal) -> 'Expr':
        return AppT(self.e.apply_uuid(v), self.t.apply_uuid(v))
```

其中 `Val`, `Fun`, `App` 的定义和简单类型 λ 演算中基本一致，这里不作展示。他们的 `UUID` 生成只需要想 `AppT` 那样递归就可以，无需特殊操作。

而测试代码

```python
T = Forall(TVal('a'), Fun(
    Val('x', TVal('a')),
    Fun(Val('y', TVal('a')), Val('x'))
)).gen_uuid()

F = Forall(TVal('a'), Fun(
    Val('x', TVal('a')),
    Fun(Val('y', TVal('a')), Val('y'))
)).gen_uuid()

Bool = TForall(TVal('x'),
               TArr(TVal('x'),
                    TArr(TVal('x'), TVal('x')))).gen_uuid()

IF = Forall(TVal('a'), Fun(
    Val('b', Bool), Fun(Val('x', TVal('a')),
                        Fun(Val('y', TVal('a')), App(App(AppT(Val('b', Bool), TVal('a')), Val('x')), Val('y'))))
)).gen_uuid()

print(T.check_type(NilEnv()))
print(IF.check_type(NilEnv()))
```

运行会输出：

```
(∀ a. (a → (a → a)))
(∀ a. ((∀ x. (x → (x → x))) → (a → (a → a))))
```

