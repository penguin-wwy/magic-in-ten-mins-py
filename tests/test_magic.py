from typing import Callable, TypeVar

import pytest
from _pytest._code import ExceptionInfo
from _pytest.capture import CaptureFixture


def test_codata():
    from magicpy.CoData import inf_alt
    assert inf_alt().next_one().head == 2


class TestMonoid:

    def test_maybe(self):
        from magicpy.Monoid import Maybe, MaybeM
        assert MaybeM[int]().appends([Maybe.of_nullable(x) for x in [None, 2, 3]]).get() == 2

    def test_ordering(self):
        from magicpy.Monoid import int_tup_greater
        assert int_tup_greater((5, 6, 7), (5, 4, 3, 2)) == (5, 6, 7)

    def test_todo(self, capsys: CaptureFixture):
        from magicpy.Monoid import Todo
        Todo().appends([
            lambda: print(1),
            lambda: print(2),
            lambda: print(3),
        ])()
        out, err = capsys.readouterr()
        assert "1\n2\n3\n" == out


class TestHKT:

    def test_type_error(self):
        e: ExceptionInfo
        with pytest.raises(TypeError) as e:
            F = TypeVar("F")
            A = TypeVar("A")
            B = TypeVar("B")

            def from_to(a: F[A], f: Callable[[A], B]) -> F[B]:
                ...
        assert "'TypeVar' object is not subscriptable" in str(e.value)

    def test_from_to(self):
        from magicpy.HKT import Box, from_to
        int_box = Box(1)
        assert from_to(int_box, lambda x: str(x)).value() == "1"


class TestMonad:

    def test_box_monad(self):
        from magicpy.Monad import BoxM, Box
        assert BoxM().pure(1).value() == 1
        assert str(BoxM().flat_map(Box.with_value(1), lambda x: Box.with_value([x, x + 1]))) == "Box{ [1, 2] }"

    def test_add_mi(self):
        from magicpy.Monad import add_mi, Maybe
        assert add_mi(Maybe.with_value(1), Maybe.with_value(2)).value() == 3
        assert add_mi(Maybe.with_value(1), Maybe.with_value(None)).value() is None


def test_state_monad():
    from magicpy.StateMonad import fib
    assert fib(0).run_state((0, 1)).value == 0
    assert fib(1).run_state((0, 1)).value == 1
    assert fib(2).run_state((0, 1)).value == 1
    assert fib(3).run_state((0, 1)).value == 2
    assert fib(4).run_state((0, 1)).value == 3
    assert fib(5).run_state((0, 1)).value == 5
    assert fib(6).run_state((0, 1)).value == 8
    assert fib(7).run_state((0, 1)).value == 13


def test_simply_typed_lambda_calculus():
    from magicpy.STLC import Val, Fun, TVal, TArr, App, NilEnv
    assert Fun(Val("x", TVal("int")),
               Fun(Val("y", TArr(TVal("int"), TVal("bool"))),
                   App(Val("y"), Val("x")))).check_type(NilEnv()) \
           == "(int -> ((int -> bool) -> bool))"

    with pytest.raises(TypeError) as e:
        Fun(Val("x", TVal("bool")),
            Fun(Val("y", TArr(TVal("int"), TVal("bool"))),
                App(Val("y"), Val("x")))).check_type(NilEnv())


def test_lambda_calculus():
    from magicpy.Lambda import App, Fun, Val
    expr = App(
        Fun(
            Val("x"),
            App(Val("x"), Fun("x", Val("x")))
        ),
        Val("y")
    )
    assert str(expr) == "((?? x. (x (?? x. x))) y)"


def test_system_f():
    from magicpy.STLC import NilEnv
    from magicpy.SystemF import Forall, Fun, App, Val, TVal, TArr, TForall, AppT
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
    assert str(T.check_type(NilEnv())) == "(??? a. (a -> (a -> a)))"
    assert str(IF.check_type(NilEnv())) == "(??? a. ((??? x. (x -> (x -> x))) -> (a -> (a -> a))))"


class TestContinuationAndAlgeff:

    def test_cont(self, capsys: CaptureFixture):
        from magicpy.Continuation import cont1
        cont1()
        out, err = capsys.readouterr()
        assert "2\n" == out

    def test_login(self, capsys: CaptureFixture):
        from magicpy.Continuation import logic1, logic2, login3
        logic1(lambda i2: logic2(i2, lambda i3: login3(i3, lambda _: None)))
        out, err = capsys.readouterr()
        assert "2\n" == out

    def test_try_run(self, capsys: CaptureFixture):
        from magicpy.Continuation import try_run
        try_run(1)
        assert "final\n" == capsys.readouterr()[0]
        try_run(0)
        assert "catch t==0\n" == capsys.readouterr()[0]

    def test_resume(self, capsys: CaptureFixture):
        from magicpy.Algeff import try_run
        try_run(0)
        out_lines = capsys.readouterr()[0].splitlines()
        assert "catch t==0 and resumed" == out_lines[0]
        assert "final" == out_lines[1]
