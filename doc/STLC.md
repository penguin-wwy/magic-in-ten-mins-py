# 十分钟魔法练习：简单类型 λ 演算

### By 「玩火」改写 「penguin」

> 前置技能：Python 基础，ADT，λ 演算

## 简单类型 λ 演算

简单类型 λ 演算（Simply-Typed Lambda Calculus）是在无类型 λ 演算（Untyped Lambda Calculus）的基础上加了个非常简单的类型系统。

这个类型系统包含两种类型结构，一种是内建的基础类型 `T` ，一种是函数类型 `A → B` ，其中函数类型由源类型 `A` 和目标类型 `B` 组成：

```
Type = BaseType + FunctionType
FunctionType = Type * Type
```

注意函数类型的符号是右结合的，也就是说 `A → A → A` 等价于 `A → (A → A)` 。

用 Python 代码可以表示为：

```python
# 构造函数， equals 已省去
class Type:

    def __eq__(self, other):
        return str(self) == str(other)

# BaseType
class TVal(Type):
    name: str
    
    def __str__(self):
        return self.name
    
# FunctionType
class TArr(Type):
    src: Type
    tar: Type
    
    def __str__(self):
        return f"({self.src} -> {self.tar})"
```

## 年轻人的第一个 TypeChecker

然后需把类型嵌入到 λ 演算的语法树中：

```python
# 构造函数， toString 已省去
class Val(Expr):
    x: str
    t: Type
    

class Fun(Expr):
    x: Val
    e: Expr
    
    
class App(Expr):
    f: Expr
    x: Expr
```

注意只有函数定义的变量需要标记类型，表达式的类型是可以被简单推导出的。同时还需要一个环境来保存定义变量的类型（其实是一个不可变链表）：

```python
class Env:

    def lookup(self, s: str) -> Type:
        ...


class NilEnv(Env):

    def lookup(self, s: str) -> Type:
        raise TypeError()


class ConsEnv(Env):
    v: Val
    n: Env  # next

    def lookup(self, s: str) -> Type:
        return self.v.t if s == self.v.x else self.n.lookup(s)
```

而对于这样简单的模型，类型检查只需要判断 `F X` 中的 `F` 需要是函数类型，并且 `(λ x. F) E` 中 `x` 的类型和 `E` 的类型一致。

而类型推导也很简单：变量的类型就是它被标记的类型；函数定义的类型就是以它变量的标记类型为源，它函数体的类型为目标的函数类型；而函数应用的类型就是函数的目标类型，在能通过类型检查的情况下。

以上用 Python 代码描述就是：

```python
# 构造函数， toString 已省去
class Expr:

    def check_type(self, env: Env) -> Type:
        ...


class Val(Expr):
    x: str
    t: Type

    def check_type(self, env: Env) -> Type:
        return self.t if self.t is not None else env.lookup(self.x)


class Fun(Expr):
    x: Val
    e: Expr

    def check_type(self, env: Env) -> Type:
        return TArr(self.x.t, self.e.check_type(ConsEnv(self.x, env)))


class App(Expr):
    f: Expr
    x: Expr
    
    def check_type(self, env: Env) -> Type:
        tf: Type = self.f.check_type(env)
        if isinstance(tf, TArr) and tf.src == self.x.check_type(env):
            return tf.tar
        raise TypeError()
```

下面的测试代码对

 ````
(λ (x: int). (λ (y: int → bool). (y x)))
 ````

进行了类型检查，会打印输出 `(int → ((int → bool) → bool))` ：

```python
print(Fun(Val("x", TVal("int")),
          Fun(Val("y", TArr(TVal("int"), TVal("bool"))),
              App(Val("y"), Val("x")))).check_type(NilEnv()))
```

而如果对

```
(λ (x: bool). (λ (y: int → bool). (y x)))
```

进行类型检查就会抛出 `BadTypeException` 。