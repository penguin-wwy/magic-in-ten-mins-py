from typing import Callable, List


def cont1():
    i = 1
    cont2(i)


def cont2(i: int):
    i += 1
    cont3(i)


def cont3(i: int):
    print(i)


def logic1(f: Callable[[int], None]):
    i = 1
    f(i)


def logic2(i: int, f: Callable[[int], None]):
    i += 1
    f(i)


def login3(i: int, f: Callable[[int], None]):
    print(i)
    f(i)


CE: List[Callable[[Exception], None]] = list()


def try_fun(body: Callable, handler: Callable[[Exception], None], cont: Callable):
    CE.append(handler)
    body(cont)
    CE.pop()


def throw_fun(e: Exception):
    CE[-1](e)


def try_run(t: int):
    try_fun(
        lambda cont: cont() if t != 0 else throw_fun(ArithmeticError("t==0")),
        lambda e: print(f"catch {e}"),
        lambda: print('final')
    )
