# 十分钟魔法练习：代数作用

### By 「玩火」改写 「penguin」

> 前置技能：Python基础，续延

## 可恢复异常

有时候我们希望在异常抛出后经过保存异常信息再跳回原来的地方继续执行。

显然Python默认异常处理无法直接实现这样的需求，因为在异常抛出时整个调用栈的信息全部被清除了。

但如果我们有了异常抛出时的续延那么可以同时抛出，在 `catch` 块中调用这个续延就能恢复之前的执行状态。

下面是实现可恢复异常的 `try-catch` ：

```python
from typing import Callable, List

CE: List[Callable[[Exception, Callable], None]] = list()


def try_fun(body: Callable, handler: Callable[[Exception, Callable], None], cont: Callable):
    CE.append(handler)
    body(cont)
    CE.pop()


def throw_fun(e: Exception, cont: Callable):
    CE[-1](e, cont)
```

然后就可以像下面这样使用：

```python
def try_run(t: int):
    try_fun(
        lambda cont: cont() if t != 0 else throw_fun(ArithmeticError("t==0"), cont),
        lambda e, c: print(f"catch {e} and resumed") or c(),
        lambda: print('final')
    )
```

而调用 `test(0)` 就会得到：

```
catch t==0 and resumed
final
```

## 代数作用

如果说在刚刚异常恢复的基础上希望在恢复时修补之前的异常错误就需要把之前的 `resume` 函数加上参数，这样修改以后它就成了代数作用（Algebaic Effect）的基础工具：

```python
from typing import Callable, List

CE: List[Callable[[Exception, Callable], None]] = list()


def try_fun(body: Callable, handler: Callable[[Exception, Callable[[int], None]], None], cont: Callable):
    CE.append(handler)
    body(cont)
    CE.pop()


def throw_fun(e: Exception, cont: Callable):
    CE[-1](e, cont)
```

使用方式如下：

```python
def try_run(t: int):
    try_fun(
        lambda cont: cont() if t != 0 else throw_fun(ArithmeticError("t==0"), cont),
        lambda e, c: print(f"catch {e} and resumed") or c(1),
        lambda: print('final')
    )
```

而这个东西能实现不只是异常的功能，从某种程度上来说它能跨越函数发生作用（Perform Effect）。

比如说现在有个函数要记录日志，但是它并不关心如何记录日志，输出到标准流还是写入到文件或是上传到数据库。这时候它就可以调用

```python
perform(LogIt(INFO, "test"), ...)
```

来发生（Perform）一个记录日志的作用（Effect）然后再回到之前调用的位置继续执行，而具体这个作用产生了什么效果就由调用这个函数的人实现的 `try` 中的 `handler` 决定。这样发生作用和执行作用（Handle Effect）就解耦了。

进一步讲，发生作用和执行作用是可组合的。对于需要发生记录日志的作用，可以预先写一个输出到标准流的的执行器（Handler）一个输出到文件的执行器然后在调用函数的时候按需组合。这也就是它是代数的（Algebiac）的原因。

细心的读者还会发现这个东西还能跨函数传递数据，在需要某个量的时候调用

```python
perform(Ask("config"), ...)
```

就可以获得这个量而不用关心这个量是怎么来的，内存中来还是读取文件或者 HTTP 拉取。从而实现获取和使用的解耦。

而且这样的操作和状态单子非常非常像，实际上它就是和相比状态单子来说没有修改操作的读取器单子（Reader Monad）同构。

也就是说把执行器函数作为读取器单子的状态并在发生作用的时候执行对应函数就可以达到和用续延实现的代数作用相同的效果，反过来也同样可以模拟。
