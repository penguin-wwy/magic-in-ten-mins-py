from uuid import UUID, uuid4


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


expr = App(
    Fun(
        Val("x"),
        App(Val("x"), Fun("x", Val("x")))
    ),
    Val("y")
)
