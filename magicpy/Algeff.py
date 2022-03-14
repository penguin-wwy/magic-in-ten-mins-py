from typing import Callable, List

CE: List[Callable[[Exception, Callable], None]] = list()


def try_fun(body: Callable, handler: Callable[[Exception, Callable], None], cont: Callable):
    CE.append(handler)
    body(cont)
    CE.pop()


def throw_fun(e: Exception, cont: Callable):
    CE[-1](e, cont)


def try_run(t: int):
    try_fun(
        lambda cont: cont() if t != 0 else throw_fun(ArithmeticError("t==0"), cont),
        lambda e, c: print(f"catch {e} and resumed") or c(),
        lambda: print('final')
    )
