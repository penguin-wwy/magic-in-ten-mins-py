# magic-in-ten-mins-py

十分钟魔法练习 Python 版

纯属娱乐，不保证全部正确性、准确性，以及Python特性使用的简洁性 (｀∀´)Ψ，使用部分 Python3.10 的内容

执行所有test case
```
PYTHONPATH="${PYTHONPATH}:/path/to/project" pipenv run pytest
```

# 十分钟魔法练习

[Java 版(原版，有不清楚的内容找他) - 玩火](https://github.com/niltok/magic-in-ten-mins)

[Rust 版 - 光量子](https://github.com/PhotonQuantum/magic-in-ten-mins-rs)

[C++ 版 - 图斯卡蓝瑟](https://github.com/tusikalanse/magic-in-ten-mins-cpp)

[C# 版 - CWKSC](https://github.com/CWKSC/magic-in-ten-mins-csharp)

[Lua 版 - Ofey Chan](https://github.com/ofey404/magic-in-ten-mins-lua)

[Ocaml 版 - 光吟](https://github.com/LighghtEeloo/magic-in-ten-mins-ml)

抽象与组合

希望能在十分钟内教会你一样魔法

QQ群：1070975853 | 
[Telegram Group](https://t.me/joinchat/HZm-VAAFTrIxoxQQ)

> 目录中方括号里的是前置技能。

## 类型系统

偏易 |
[Markdown](doc/ADT.md) |
代数数据类型(Algebraic Data Type) 
[Python 基础]

偏易 |
[Markdown](doc/GADT.md) |
广义代数数据类型(Generalized Algebriac Data Type) 
[Python 基础， ADT] 

偏易 |
[Markdown](doc/CoData.md) |
余代数数据类型(Coalgebraic Data Type)
[Python 基础， ADT]

偏易 |
[Markdown](doc/Monoid.md) |
单位半群(Monoid)
[Python 基础]

较难 |
[Markdown](doc/HKT.md) |
高阶类型(Higher Kinded Type)
[Python 基础]

中等 |
[Markdown](doc/Monad.md) |
单子(Monad)
[Python 基础， HKT]

较难 |
[Markdown](doc/StateMonad.md) |
状态单子(State Monad)
[Python 基础， HKT ， Monad]

中等 |
[Markdown](doc/STLC.md) |
简单类型 λ 演算(Simply-Typed Lambda Calculus)
[Python 基础， ADT ，λ 演算]

中等 |
[Markdown](doc/SystemF.md) |
系统 F(System F)
[Python 基础， ADT ，简单类型 λ 演算]

> 中等 |
Markdown(doc/SysFO.md) | 
系统 F ω(System F ω)
[Python 基础， ADT ，系统 F]

> 较难 |
Markdown(doc/CoC.md) |
构造演算(Calculus of Construction)
[Python 基础， ADT ，系统 F ω]

> 偏易 |
Markdown(doc/PiSigma.md) |
π 类型和 Σ 类型(Pi type & Sigma type)
[ADT ，构造演算]

## 计算理论

较难 |
[Markdown](doc/Lambda.md) |
λ 演算(Lambda Calculus)
[Python 基础， ADT]

> 较难 |
Markdown(doc/DBI.md) |
De Bruijn 索引(De Bruijn index)
[Python 基础，ADT，λ 演算]

 偏易 |
[Markdown](doc/EvalStrategy.md) |
求值策略(Evaluation Strategy)
[Python 基础， λ 演算]

 较难 |
[Markdown](doc/ChurchE.md) |
丘奇编码(Church Encoding)
[λ 演算]

> 很难 |
Markdown(doc/ScottE.md) |
斯科特编码(Scott Encoding)
[构造演算， ADT ， μ]

中等 |
[Markdown](doc/YCombinator.md) |
Y 组合子(Y Combinator)
[Python 基础，λ 演算，λ 演算编码]

> 中等 |
Markdown(doc/Mu.md) |
μ(Mu)
[Python 基础，构造演算， Y 组合子]

> 中等 |
Markdown(doc/VecFin.md) |
向量和有限集(Vector & FinSet)
[构造演算， ADT ，依赖类型模式匹配]

## 形式化验证

> 偏易 |
Markdown(doc/CHIso.md) |
Curry-Howard 同构(Curry-Howard Isomorphism)
[构造演算]

> 偏难 |
Markdown(doc/LeiEq.md) |
莱布尼兹相等性(Leibniz Equality)
[构造演算]

## 编程范式

简单 |
[Markdown](doc/TableDriven.md) |
表驱动编程(Table-Driven Programming)
[简单 Python 基础]

简单 |
[Markdown](doc/Continuation.md) |
续延(Continuation)
[简单 Python 基础]

中等 |
[Markdown](doc/Algeff.md) |
代数作用(Algebraic Effect)
[简单 Python 基础，续延]

中等 |
[Markdown](doc/DepsInj.md) |
依赖注入(Dependency Injection)
[Python 基础， Monad ，代数作用]

> 中等 |
Markdown(doc/Lifting.md) |
提升(Lifting)
[Python 基础， HKT ， Monad]

## 编译原理

> 较难 |
Markdown(doc/ParserM.md) |
解析器单子(Parser Monad)
[Python 基础， HKT ， Monad]

> 中等 |
Markdown(doc/Parsec.md) |
解析器组合子(Parser Combinator)
[Python 基础， HKT ， Monad]
