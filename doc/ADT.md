# 十分钟魔法练习：代数数据类型 (ADT)

### By 「玩火」 改写 「penguin」

> 前置技能：Python 基础


## 积类型（Product type）

积类型是指同时包括多个值的类型，Python 中最直接实现，比如 Class 就会包括多个字段：

```python
class Student:
    name: str
    id: int
```

而上面这段代码中 `Student` 的类型中既有 `str` 类型的值也有 `int` 类型的值。这种情况我们称其为 `string` 和 `int` 的「积」，即`string * int`。

## 和类型（Sum type）

和类型是指可以是某一些类型之一的类型，在 Python 中可以用继承来表示：

```python
class SchoolPerson:
    pass


class Student(SchoolPerson):
    name: str
    id: int
  

class Teacher(SchoolPerson):
    name: str
    office: str
```

SchoolPerson 可能是 Student 也可能是 Teacher ，可以表示为 Student 和 Teacher 的「和」，即 String * int + String * String 。而使用时只需要用 isinstance 就能知道当前的 StudentPerson 具体是 Student 还是 Teacher 。

在python3.10中也可以使用`UnionType`来表示：

```python
import types


class Student:
    name: str
    id: int


class Teacher:
    name: str
    office: str


SchoolPerson = Student | Teacher

assert isinstance(SchoolPerson, types.UnionType)

```

## 代数数据类型（ADT, Algebraic Data Type）

由和类型与积类型组合构造出的类型就是代数数据类型，其中代数指的就是和与积的操作。

利用和类型的枚举特性与积类型的组合特性，我们可以构造出 Python 中本来很基础的基础类型，比如枚举布尔的两个量来构造布尔类型：

然后用 `isinstance` 或者 pattern matching 就可以用来判定 t 作为 Bool 的值是不是 True 。

```python
class TrueTy:
    pass


class FalseTy:
    pass


Bool = TrueTy | FalseTy

t = TrueTy()
assert isinstance(t, Bool)
assert isinstance(t, TrueTy)
assert not isinstance(t, FalseTy)
match t:
    case TrueTy():
        assert isinstance(t, TrueTy)
    case FalseTy():
        assert isinstance(t, FalseTy)
    case _:
        assert False
```

### 自然数

比如利用S的数量表示的自然数：

```python
class Nat:
    pass


class Z(Nat):
    pass


class S(Nat):
    value: Nat

    def __init__(self, v):
        self.value = v

```

这里提一下自然数的皮亚诺构造，一个自然数要么是 0 (也就是上面的 Z ) 要么是比它小一的自然数 +1 (也就是上面的 S ) ，
例如3可以用 `S(S(S((Z())))` 来表示。

再比如链表：

```python
from typing import Generic, TypeVar


T = TypeVar("T")


class Node(Generic[T]):
    pass


class Nil(Node):
    pass


class Cons(Node):
    value: T
    next: Node

    def __init__(self, v, n):
        self.value = v
        self.next = n
```

`[1, 3, 4]` 就表示为 `Cons(1, Cons(3, Cons(4, Nil())))`

更奇妙的是代数数据类型对应着数据类型可能的实例数量。

很显然积类型的实例数量来自各个字段可能情况的组合也就是各字段实例数量相乘，而和类型的实例数量就是各种可能类型的实例数量之和。

比如 Bool 的类型是 `1+1 `而其实例只有 True 和 False ，而 Nat 的类型是 `1+1+1+...` 其中每一个1都代表一个自然数，至于 List 的类型就是`1+x(1+x(...))` 也就是 `1+x^2+x^3...` 其中 x 就是 List 所存对象的实例数量。

## 实际运用

ADT 最适合构造树状的结构，比如解析 JSON 出的结果需要一个聚合数据结构。

```python
from typing import List, Dict


class JsonValue:
    pass


class JsonBool(JsonValue):
    def __init__(self, v: bool):
        self.value: bool = v
        

class JsonInt(JsonValue):
    def __init__(self, v: int):
        self.value: int = v
        

class JsonString(JsonValue):
    def __init__(self, v: str):
        self.value: str = v


class JsonArray(JsonValue):
    def __init__(self, v: List[JsonValue]):
        self.value: List[JsonValue] = v


class JsonMap(JsonValue):
    def __init__(self, v: Dict[str, JsonValue]):
        self.value: Dict[str, JsonValue] = v

```
