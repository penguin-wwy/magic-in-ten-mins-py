from typing import TypeVar
from uuid import UUID, uuid4

from magicpy.STLC import Env, ConsEnv, NilEnv

A = TypeVar("A")


def true(x: A, y: A) -> A:
    return x


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

    def __init__(self, x, uid=None):
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
        return TArr(self.a.apply(x, t), self.b.apply(x, t))

    def gen_uuid(self) -> 'Type':
        return TArr(self.a.gen_uuid(), self.b.gen_uuid())

    def apply_uuid(self, v: 'TVal') -> 'Type':
        return TArr(self.a.apply_uuid(v), self.b.apply_uuid(v))


class Expr:
    def check_type(self, env: Env) -> Type:
        ...

    def gen_uuid(self) -> 'Expr':
        ...

    def apply_uuid(self, v: TVal) -> 'Expr':
        ...


class Val(Expr):
    x: str
    t: Type

    def __init__(self, x, t=None):
        self.x = x
        self.t = t

    def check_type(self, env: Env) -> Type:
        return self.t if self.t is not None else env.lookup(self.x)

    def gen_uuid(self) -> 'Expr':
        return Val(self.x, self.t.gen_uuid())

    def apply_uuid(self, v: TVal) -> 'Expr':
        return self if self.t is not None else Val(self.x, v.gen_uuid())


class Fun(Expr):
    x: Val
    e: Expr

    def __init__(self, x, e):
        self.x = x
        self.e = e

    def check_type(self, env: Env) -> Type:
        return TArr(self.x.t, self.e.check_type(ConsEnv(self.x, env)))

    def gen_uuid(self) -> 'Expr':
        return Fun(self.x.gen_uuid(), self.e.gen_uuid())

    def apply_uuid(self, v: TVal) -> 'Expr':
        return Fun(self.x.apply_uuid(v), self.e.apply_uuid(v))


class App(Expr):
    f: Expr
    x: Expr

    def __init__(self, f, x):
        self.f = f
        self.x = x

    def check_type(self, env: Env) -> Type:
        tf: Type = self.f.check_type(env)
        if isinstance(tf, TArr) and tf.a == self.x.check_type(env):
            return tf.b
        raise TypeError()

    def gen_uuid(self) -> 'Expr':
        return App(self.f.gen_uuid(), self.x.gen_uuid())

    def apply_uuid(self, v: TVal) -> 'Expr':
        return App(self.f.apply_uuid(v), self.x.apply_uuid(v))


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
