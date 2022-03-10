# 十分钟魔法练习：λ 演算

### By 「玩火」改写 「penguin」

> 前置技能：Python 基础，ADT

## Intro

程序员们总是为哪种语言更好而争论不休，而强悍的大佬也为自己造出语言而感到高兴。造语言也被称为程序员的三大浪漫之一。这样一项看上去高难度的活动总是让萌新望而生畏，接下来我要介绍一种世界上最简单的**图灵完备**语言并给出 90 行Python代码的解释器实现。让萌新也能体验造语言的乐趣。

## λ演算

1936年，丘奇(Alonzo Church)提出了一种非常简单的计算模型，叫λ演算(Lambda Calculus)。

> 一些不严谨的通俗理解：
>
> λ表达式中的函数定义 `(λ x. E)` 就是定义了数学上的函数 `f(x)=E` ，只不过没有名字， `λ` 代表一个函数定义的开始，而 `.` 左边的是函数的自变量，可以是任意符号，这里用了 `x` ， `.` 的右边是函数的内容 `E` ，可以是任意 λ 表达式。
>
> 而函数应用 `F X` 就是对于一个数学上的函数 `F` 求值 `F(X)` ， `F` 就是函数， `X` 就是参数。比如 `(λ x. x)` 就是 `f(x)=x` ，比如 `(λ x. (x x))` 可以表示为 `f(x) = x(x)` ，其中 `x` 应当是个函数，不过这在数学里面是不允许的，而 `((λ x. (x x)) y)` 就可以表示为数学上的 `f(x) = x(x), f(y)` 也就是 `y(y)` 。
>
> 和传统数学函数最不一样的是λ演算里面的函数可以在任何位置被定义并且没有名字，并且可以被当作变量传递也可以作为函数的计算结果。

一个λ表达式有三种组成可能：变量 `x` 、函数定义 `(λ x. E)` 、函数应用 `(F X)` 。其中 `x` 是一个抽象的符号， `E, F, X` 是 λ 表达式。注意这是递归的定义，我们可以通过组合三种形式来构造复杂的 λ 表达式。比如 `((λ x. (x x)) y)` 整体是一个函数应用，其 `F` 是函数定义 `(λ x. (x x))` ， `X` 是 `y` ，而 `(λ x. (x x))` 函数定义的 `x` 是变量 `x` ， `E` 是 `(x x)` 。

λ表达式的计算也称为归约 (reduce) ，只需要将函数应用整体变换，变换结果为其作为函数定义的第一项 `F` (也就是 `(λ x. E)` ) 中 `E` 里出现的所有**自由**的 `x` 替换为其第二项 `X` ，也就是说 `((λ x. E) X)` 会被归约为 `E(x → X)` ，。听上去挺复杂，举个最简单的例子 `((λ x. (x x)) y)` 可以归约为 `(y y)` 。我这里提到了自由的 `x` ，意思是说它不是任何λ函数定义的自变量，比如 `(λ x. (x t))` 中的 `x` 就是不自由的， `t` 就是自由的。

函数定义有比函数应用更低的优先级，也就是说是 `(λ x. (x x))` 可以写成 `(λ x. x x)` 。函数应用是左结合的，所以 `((x x) x)` 可以写成 `(x x x)` 。

## 解释器

首先，我们要用 ADT 定义出 λ 表达式的数据结构：

```python
from uuid import UUID

class Expr:
    ...

# Value 变量
class Val(Expr):
    x: str
    uid: UUID
    
    def __init__(self, x: str, uid: UUID = None):
        self.x = x
        self.uid = uid
        
    def __str__(self):
        return self.x
    
    def __eq__(self, other):
        return isinstance(other, Val) and self.uid == other.uid
    
# Function 函数定义
class Fun(Expr):
    x: Val
    e: Expr
    
    def __init__(self, x: Val, e: Expr):
        self.x = x
        self.e = e
        
    def __str__(self):
        return f"(λ {self.x}. {self.e})"
    
# Apply 函数应用
class App(Expr):
    f: Expr
    x: Expr
    
    def __init__(self, f: Expr, x: Expr):
        self.f = f
        self.x = x
        
    def __str__(self):
        return f"({self.f} {self.x})"
```

> 注意到上面代码中 `Val` 有一个类型为 `UUID` 的字段，同时 `equals` 函数只比较 `id` 字段，这个字段是用来区分相同名字的不同变量的。如果不做区分那么对于下面的 λ 表达式：
>
> ```
> λ z. (λ x. (λ z. x)) z
> ```
>
> 会被规约成
>
> ```
> λ z. (λ z. z)
> ```
>
> 然而实际上最内层的 `z` 最开始是被最外层的函数定义定义的，而这里它被内层的函数定义错误地捕获（Capture）了，所以正确的规约结果应该是：
>
> ```
> λ z'. (λ z. z')
> ```

然后就可以构造 λ 表达式了，比如 `(λ x. x (λ x. x)) y` 就可以这样构造：

```python
expr = App(
    Fun(
        Val("x"), 
        App(Val("x"), Fun("x", Val("x")))
    ),
    Val("y")
)
```

然后就可以定义归约函数 `reduce` 和应用自由变量函数 `apply` 还有用来生成 `UUID` 的 `genUUID` 函数和 `applyUUID` 函数：

```python
class Expr:

    def reduce(self) -> 'Expr':
        ...

    def apply(self, v: 'Val', ex: 'Expr') -> 'Expr':
        ...

    def gen_uuid(self) -> 'Expr':
        ...

    def apply_uuid(self, v: 'Val') -> 'Expr':
        ...


class Val(Expr):
    x: str
    uid: UUID

    def __init__(self, x: str, uid: UUID = None):
        self.x = x
        self.uid = uid

    def __str__(self):
        return self.x

    def __eq__(self, other):
        return isinstance(other, Val) and self.uid == other.uid

    def reduce(self) -> 'Expr':
        return self

    def apply(self, v: 'Val', ex: 'Expr') -> 'Expr':
        return ex if v == self else self

    def gen_uuid(self) -> 'Expr':
        return self

    def apply_uuid(self, v: 'Val') -> 'Expr':
        return Val(self.x, v.uid) if self.x == v.x else self


class Fun(Expr):
    x: Val
    e: Expr

    def __init__(self, x: Val, e: Expr):
        self.x = x
        self.e = e

    def __str__(self):
        return f"(λ {self.x}. {self.e})"

    def reduce(self) -> 'Expr':
        return self

    def apply(self, v: 'Val', ex: 'Expr') -> 'Expr':
        return self if v == self.x else Fun(self.x, self.e.apply(v, ex))

    def gen_uuid(self) -> 'Expr':
        if self.x.uid is None:
            v = Val(self.x.x, uuid4())
            return Fun(v, self.e.apply_uuid(v).gen_uuid())
        return Fun(self.x, self.e.gen_uuid())

    def apply_uuid(self, v: 'Val') -> 'Expr':
        return self if self.x.x == v.x else Fun(self.x, self.e.apply_uuid(v))


class App(Expr):
    f: Expr
    x: Expr

    def __init__(self, f: Expr, x: Expr):
        self.f = f
        self.x = x

    def __str__(self):
        return f"({self.f} {self.x})"

    def reduce(self) -> 'Expr':
        fr: Expr = self.f.reduce()
        if isinstance(fr, Fun):
            return fr.e.apply(fr.x, self.x).reduce()
        return App(fr, self.x)

    def apply(self, v: 'Val', ex: 'Expr') -> 'Expr':
        return App(self.f.apply(v, ex), self.x.apply(v, ex))

    def gen_uuid(self) -> 'Expr':
        return Fun(self.f.gen_uuid(), self.x.gen_uuid())

    def apply_uuid(self, v: 'Val') -> 'Expr':
        return Fun(self.f.apply_uuid(v), self.x.apply_uuid(v))

```

注意在 `reduce` 一个表达式之前应该先调用 `genUUID` 来生成变量标签。

以上就是 90 行 Python 写成的解释器啦！

