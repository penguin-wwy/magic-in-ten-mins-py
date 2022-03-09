class Type:

    def __eq__(self, other):
        return str(self) == str(other)


class TVal(Type):
    name: str

    def __init__(self, n):
        self.name = n

    def __str__(self):
        return self.name


class TArr(Type):
    src: Type
    tar: Type

    def __init__(self, s, t):
        self.src = s
        self.tar = t

    def __str__(self):
        return f"({self.src} -> {self.tar})"


class Env:

    def lookup(self, s: str) -> Type:
        ...


class Expr:

    def check_type(self, env: Env) -> Type:
        ...


class Val(Expr):
    x: str
    t: Type

    def __init__(self, x, t = None):
        self.x = x
        self.t = t

    def check_type(self, env: Env) -> Type:
        return self.t if self.t is not None else env.lookup(self.x)


class Fun(Expr):
    x: Val
    e: Expr

    def __init__(self, x, e):
        self.x = x
        self.e = e

    def check_type(self, env: Env) -> Type:
        return TArr(self.x.t, self.e.check_type(ConsEnv(self.x, env)))


class App(Expr):
    f: Expr
    x: Expr

    def __init__(self, f, x):
        self.f = f
        self.x = x

    def check_type(self, env: Env) -> Type:
        tf: Type = self.f.check_type(env)
        if isinstance(tf, TArr) and tf.src == self.x.check_type(env):
            return tf.tar
        raise TypeError()


class NilEnv(Env):

    def lookup(self, s: str) -> Type:
        raise TypeError()


class ConsEnv(Env):
    v: Val
    n: Env  # next

    def __init__(self, v, n):
        self.v = v
        self.n = n

    def lookup(self, s: str) -> Type:
        return self.v.t if s == self.v.x else self.n.lookup(s)
