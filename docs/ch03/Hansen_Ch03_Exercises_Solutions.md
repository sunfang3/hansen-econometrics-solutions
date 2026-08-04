# Bruce Hansen《Econometrics》第 3 章习题解答（详细注释版）

**章节：** Chapter 3 The Algebra of Least Squares
**出版版：** `hansen/manuscripts/Econometrics_Fullbook.pdf`，PDF 第 129–132 页（印刷页 94–97），§3.26 Exercises（**3.1–3.26 全部**）
**体系统一：** 投影矩阵、残差代数、FWL、leave-one-out、$R^2$、CPS 实证
**数值验证：** `Hansen_Ch03_Exercises_Solutions.ipynb`（Exercise 3.24–3.26 有可运行代码）
**数据：** `hansen/econometrics/data/cps09mar/`（需自行下载，见 README）

> **写给谁看：** 假设你学过李子奈/陈强的本科计量，熟悉 $\hat\beta=(X'X)^{-1}X'Y$、$\sum\hat e_i=0$、$R^2$ 这些结论，但对**矩阵投影**的语言不熟。
> Hansen 第 3 章和国内教材的关键差别：它把 OLS **全部**写成两个矩阵 $P$（投影/hat 矩阵）和 $M$（零化矩阵）的语言。一旦记住 "$P$ 保留 $X$ 的列空间、$M$ 消灭它"，本章几乎所有题都是一两行的事。本章**没有概率/统计**（那是第 4 章起的事），纯粹是线性代数——Hansen 标题就叫 The **Algebra** of Least Squares。

---

## 0. 读题前必看：本章到底在讲什么

**承上启下：** 第 2 章讲**总体**对象（CEF $m(X)$、最佳线性预测 BLP，系数 $\beta=(E[XX'])^{-1}E[XY]$）。第 3 章是它的**样本**翻版——把总体期望 $E[\cdot]$ 换成样本均值 $\tfrac1n\sum_i$：

| 总体（第 2 章） | 样本（第 3 章 OLS） |
|---|---|
| $\beta=(E[XX'])^{-1}E[XY]$ | $\hat\beta=(X'X)^{-1}X'Y$ |
| 投影误差 $e$，$E[Xe]=0$ | 残差 $\hat e$，$X'\hat e=0$（正规方程） |
| $\sigma^2=E[e^2]$ | $\hat\sigma^2=\tfrac1n\sum\hat e_i^2$（或除以 $n-k$） |

**一个心智模型：** 第 2 章是"靶心"（总体参数 $\beta$），第 3 章是"用样本造一支箭 $\hat\beta$ 去射靶心"。本章只关心**这支箭的代数性质**（怎么算、残差正交、$R^2$ 怎么来），不关心它射得准不准（抽样分布，第 4 章再讲）。

**本章两大主角（务必吃透）：**

$$\boxed{P=X(X'X)^{-1}X'\ \text{（投影矩阵 / hat 矩阵）},\qquad M=I_n-P\ \text{（零化矩阵 / annihilator）}.}$$

它们把 OLS 的所有量一网打尽：

- **拟合值** $\hat Y=X\hat\beta=PY$（$P$ 给 $Y$ "戴上帽子"，所以叫 hat 矩阵）；
- **残差** $\hat e=Y-\hat Y=MY$（$M$ 把 $Y$ 中"能用 $X$ 解释的部分"消灭掉，只留残差，所以叫 annihilator）。

**记两句口诀，本章 90% 的题迎刃而解：**

1. **"$P$ 保留 col($X$)，$M$ 消灭 col($X$)"**：任何能写成 $X\Gamma$ 的矩阵（即落在 $X$ 的列空间里），被 $P$ 作用后不变、被 $M$ 作用后变 0。特别地 $PX=X$，$MX=0$。
2. **"$P$、$M$ 都是幂等的"**：$P^2=P$，$M^2=M$，且 $PM=MP=0$（"投影两次等于投影一次；投影与零化互相抵消"）。

> **和本科对照：** 李子奈/陈强也写 $\hat\beta=(X'X)^{-1}X'Y$，但很少强调 $P$、$M$ 这两个矩阵。Hansen 的好处是：$\sum\hat e_i=0$、$\sum X_i\hat e_i=0$、$\sum\hat Y_i\hat e_i=0$ 这些"零散"性质，用 $P$、$M$ 全部统一成"正交"这一个概念。

---

## 1. 记号与概念速查（对照李子奈/陈强）

| Hansen 记号 | 中文/本科说法 | 一句话解释 |
|---|---|---|
| $\hat\beta=(X'X)^{-1}X'Y$ | OLS 估计量 | 同本科；这里 $X$ 含常数列 |
| $\hat Y=X\hat\beta=PY$ | 拟合值 | $P$ 把 $Y$ 投影到 $X$ 的列空间 |
| $\hat e=Y-\hat Y=MY$ | 残差 | $M$ 消灭 $X$ 能解释的部分 |
| $X'\hat e=0$ | 正规方程 / 一阶条件 | 残差与每个回归元正交（含常数→$\sum\hat e_i=0$） |
| $P=X(X'X)^{-1}X'$ | 投影矩阵 / hat 矩阵 | 幂等对称；$\mathrm{tr}(P)=k$，$\mathrm{rank}(P)=k$ |
| $M=I-P$ | 零化矩阵 | 幂等对称；$\mathrm{tr}(M)=n-k$（自由度！） |
| $h_{ii}=X_i'(X'X)^{-1}X_i$ | 杠杆值 / hat 值 | 第 $i$ 个观测"多异常"；$0\le h_{ii}\le1$，$\sum h_{ii}=k$ |
| $\tilde e_i=\hat e_i/(1-h_{ii})$ | 留一预测误差 | 剔除第 $i$ 个观测后的预测误差（一 liner 公式，不用重算回归） |
| $R^2=1-\frac{\sum\hat e_i^2}{\sum(Y_i-\bar Y)^2}$ | 判定系数 / 拟合优度 | "Y 的方差被解释的比例"；含截距时 $=\mathrm{Corr}(Y,\hat Y)^2$ |
| FWL (Thm 3.5) | 偏回归 / 净化 | $\hat\beta_2$ = 先把 $Y$、$X_2$ 都对 $X_1$ 净化，再回归 |

**全章"万能恒等式"（做题时反复用）：**

- $PX=X$，$MX=0$；更一般 $X_1\subset\mathrm{col}(X)\Rightarrow PX_1=X_1,\ MX_1=0$。
- $P^2=P$，$M^2=M$，$PM=MP=0$，$P'=P$，$M'=M$。
- $\mathrm{tr}(P)=k$，$\mathrm{tr}(M)=n-k$，$\mathrm{rank}(M)=n-k$。
- 正规方程 $X'\hat e=0$ 的矩阵证明：$X'\hat e=X'MY$，而 $X'M=X'(I-P)'=X'-X'P'=X'-(PX)'=X'-X'=0$，故 $X'\hat e=0$。

---

## 2. 预备记号

OLS：$\hat\beta=(X'X)^{-1}X'Y$，$\hat e=MY$，$M=I-P$，$P=X(X'X)^{-1}X'$。
$h_{ii}=X_i'(X'X)^{-1}X_i$，$\tilde e_i=\hat e_i/(1-h_{ii})$。

方程 (3.49)（单身亚裔男性、经验 $<45$）：
$$\widehat{\log(\mathrm{wage})}=0.144\,\mathrm{edu}+0.043\,\mathrm{exp}-0.095\,\mathrm{exp}^2/100+0.531.$$

---

## Exercise 3.1　样本均值与样本方差 = 矩条件

**题：** $g(y,\mu,\sigma^2)=\begin{pmatrix}y-\mu\\(y-\mu)^2-\sigma^2\end{pmatrix}$。设 $g_n(\hat\mu,\hat\sigma^2)=0$，其中 $g_n(m,s)=\tfrac1n\sum_i g(y_i,m,s)$。证明 $\hat\mu,\hat\sigma^2$ 是样本均值与样本方差。

**考点：** 矩方法（method of moments）——"几个方程解几个未知数"。这是第 2 章 Ex 2.17 的**样本**翻版。

**证明：** $g_n(\hat\mu,\hat\sigma^2)=0$ 即两个分量同时为 0：

- 第一分量 $\tfrac1n\sum_i(y_i-\hat\mu)=0\Rightarrow\hat\mu=\bar y$；
- 第二分量 $\tfrac1n\sum_i\big[(y_i-\hat\mu)^2-\hat\sigma^2\big]=0$，代入 $\hat\mu=\bar y$ 得
$$\hat\sigma^2=\frac1n\sum_{i=1}^n(y_i-\bar y)^2.$$

> **和本科对照：** 这里的 $\hat\sigma^2$ 除以 $n$（极大似然的写法），不是本科常见的除以 $n-1$（无偏写法）。两者只差一个常数因子 $\tfrac{n}{n-1}$，大样本下无区别。要点：样本均值、样本方差本质上是**两个矩方程的解**。

---

## Exercise 3.2　回归元做可逆线性变换：拟合与残差不变

**题：** $Z=XC$，$C$ 为 $k\times k$ 可逆阵。比较 $Y$ 对 $X$ 与 $Y$ 对 $Z$ 的 OLS。

**考点：** col($Z$)=col($X$)（因 $C$ 可逆），所以投影到的列空间相同 → 拟合值、残差完全一样，只是系数被"换算"。

**证明：**
$$\hat\beta_Z=(Z'Z)^{-1}Z'Y=\big((XC)'XC\big)^{-1}(XC)'Y=(C'X'XC)^{-1}C'X'Y=C^{-1}(X'X)^{-1}\underbrace{(C')^{-1}C'}_{=I}X'Y=C^{-1}\hat\beta_X.$$
拟合值 $\hat Y_Z=Z\hat\beta_Z=XC\cdot C^{-1}\hat\beta_X=X\hat\beta_X=\hat Y_X$，残差 $\hat e_Z=Y-\hat Y_Z=\hat e_X$。

> **和本科对照：** 把教育单位从"年"换成"学期"（$C=2$），或把 $(X_1,X_2)$ 换成 $(X_1,X_2-X_1)$（差分），**回归线不变**，只是系数跟着换算。这就是"量纲改变只变系数、不变拟合"的严格说法（见 3.23 的应用）。

---

## Exercise 3.3　正规方程 $X'\hat e=0$

**题：** 用矩阵证明 $X'\hat e=0$。

**考点：** OLS 的**一阶条件 / 正规方程**。用万能恒等式 "$X'M=0$" 一行搞定。

**证明：**
$$X'\hat e=X'(Y-X\hat\beta)=X'Y-X'X(X'X)^{-1}X'Y=X'Y-X'Y=0.$$
（或直接：$X'\hat e=X'MY$，而 $X'M=0$，故为 0。）

> **和本科对照：** 这就是李子奈里 $\sum_i X_{ji}\hat e_i=0\ (j=1,\dots,k)$，特别当 $X$ 含常数列时 $\sum_i\hat e_i=0$。它是 OLS 残差的**定义性**性质（只要是最小二乘就成立），不是额外假设。

---

## Exercise 3.4　$X=[X_1\ X_2]\Rightarrow X_2'\hat e=0$

**考点：** 正规方程的分块版本——残差与**每一块**回归元都正交。

**证明：** 由 3.3，$X'\hat e=\begin{pmatrix}X_1'\\X_2'\end{pmatrix}\hat e=\begin{pmatrix}X_1'\hat e\\X_2'\hat e\end{pmatrix}=0$，整个向量为零 ⇒ 每一块为零，特别 $X_2'\hat e=0$。

> **含义：** 残差与 $X$ 的**每一列**正交。这是 3.25（实证核对）的理论依据：$\sum\hat e_i=0$、$\sum(\text{edu})\hat e_i=0$、$\sum(\text{exp})\hat e_i=0$、$\sum(\text{exp}^2/100)\hat e_i=0$ 都成立，因为它们都在 $X$ 里；而 $\sum(\text{edu}^2)\hat e_i\ne0$，因为 $\text{edu}^2$ 不在 $X$ 里。

---

## Exercise 3.5　残差对 $X$ 回归 → 系数为 0

**题：** 把 $\hat e$ 对 $X$ 做 OLS，求系数。

**考点：** "OLS 残差里没有 $X$ 的线性信息"。

**证明：** 系数 $=(X'X)^{-1}X'\hat e=(X'X)^{-1}\cdot0=0$（用 3.3）。

> **直观：** 残差已被"榨干"了 $X$ 能线性解释的部分，再拿它对 $X$ 回归自然得 0 斜率。这是"线性投影已穷尽 $X$ 的解释力"的代数表述。

---

## Exercise 3.6　拟合值对 $X$ 回归 → 系数 $=\hat\beta$

**题：** $\hat Y=X(X'X)^{-1}X'Y=PY$，把 $\hat Y$ 对 $X$ 回归，求系数。

**证明：** 系数 $=(X'X)^{-1}X'\hat Y=(X'X)^{-1}X'PY$。因 $PX=X\Rightarrow X'P=X'$（$P$ 对称）：
$$(X'X)^{-1}X'PY=(X'X)^{-1}X'Y=\hat\beta.$$
（更直观：$\hat Y=X\hat\beta$ 落在 col($X$) 里，把它对 $X$ 回归当然还原出 $\hat\beta$。）

---

## Exercise 3.7　$X=[X_1\ X_2]\Rightarrow PX_1=X_1,\ MX_1=0$

**考点：** 万能恒等式的直接应用——$X_1$ 是 $X$ 的子块，落在 col($X$) 里。

**证明：** 把 $X_1$ 写成 $X\Gamma$，其中 $\Gamma=\begin{pmatrix}I\\0\end{pmatrix}$（取 $X$ 的前几列）。则 $X_1$ 在 col($X$) 中，故
$$PX_1=P(X\Gamma)=\underbrace{(PX)}_{=X}\Gamma=X\Gamma=X_1,\qquad MX_1=(I-P)X_1=X_1-X_1=0.$$

> **口诀兑现：** "$P$ 保留 col($X$)，$M$ 消灭 col($X$)"。

---

## Exercise 3.8　$M$ 幂等：$MM=M$

**考点：** 零化矩阵也是投影矩阵（投影到 col($X$) 的正交补）。

**证明：** $M=I-P$，用 $P^2=P$：
$$MM=(I-P)(I-P)=I-2P+P^2=I-2P+P=I-P=M.$$

> **含义：** 幂等 = "投影两次等于投影一次"。残差 $\hat e=MY$ 已经在 col($X$) 的正交补里，再乘一次 $M$ 不变。

---

## Exercise 3.9　$\mathrm{tr}(M)=n-k$

**考点：** 自由度 $n-k$ 的代数来源。

**证明：** $\mathrm{tr}(M)=\mathrm{tr}(I_n-P)=\mathrm{tr}(I_n)-\mathrm{tr}(P)=n-k$（用了 Theorem 3.3.3 的 $\mathrm{tr}(P)=k$）。

> **和本科对照：** 这就是"$\hat\sigma^2$ 无偏估计除以 $n-k$"里那个 $n-k$（自由度）。原因：$M$ 有 $n-k$ 个特征值为 1（$\mathrm{rank}(M)=n-k$），残差向量 $\hat e=MY$ 实际只活在 $n-k$ 维子空间里——因为估计 $k$ 个参数消耗了 $k$ 个自由度。

---

## Exercise 3.10　正交分块：$X_1'X_2=0\Rightarrow P=P_1+P_2$

**考点：** 当两块回归元正交时，投影可分解成两块之和。

**证明：** 记 $P_j=X_j(X_j'X_j)^{-1}X_j'$。先看交叉项：因 $X_1'X_2=0$，
$$P_1P_2=X_1(X_1'X_1)^{-1}\underbrace{X_1'X_2}_{=0}(X_2'X_2)^{-1}X_2'=0,\quad\text{同理 }P_2P_1=0.$$
于是 $(P_1+P_2)^2=P_1^2+P_2^2+P_1P_2+P_2P_1=P_1+P_2$（幂等），且 $P_1+P_2$ 把向量投影到 col($X_1$)⊕col($X_2$)=col($X$)。投影到同一空间的幂等对称矩阵唯一，故 $P_1+P_2=P$。

> **和本科对照：** 当回归元两两正交（如正交设计、平衡的虚拟变量），多元回归可拆成独立的一元回归（见 3.21）。一般情况下 $X_1'X_2\ne0$，$P\ne P_1+_2$，回归元之间"互相干扰"——这就是多重共线性影响系数（但不影响拟合）的根源。

---

## Exercise 3.11　含截距 $\Rightarrow\overline{\hat Y}=\bar Y$

**考点：** 截距保证残差和为 0。

**证明：** $X$ 含常数列 $\iota=(1,\dots,1)'$。由正规方程 $X'\hat e=0$ 得 $\iota'\hat e=\sum_i\hat e_i=0$，即 $\overline{\hat e}=0$。又 $Y=\hat Y+\hat e$，两边取均值：$\bar Y=\overline{\hat Y}+\overline{\hat e}=\overline{\hat Y}$。

> **和本科对照：** 含截距时残差均值必为 0（李子奈基本性质）。这也是 $R^2$ 有意义的**前提**：无截距时 $\sum\hat e_i\ne0$，方差分解不成立，$R^2$ 可能出现负数或无意义。

---

## Exercise 3.12　虚拟变量陷阱

**题：** $D_1$（男=1）、$D_2$（女=1），满足 $D_1+D_2=\iota$。$n_1$ 男 $n_2$ 女。比较三个方程：(3.52) $Y=\mu+D_1\alpha_1+D_2\alpha_2+e$；(3.53) $Y=D_1\alpha_1+D_2\alpha_2+e$；(3.54) $Y=\mu+D_1\phi+e$。能否都用 OLS 估？

**考点：** **虚拟变量陷阱**（dummy variable trap）= 截距与全部类别虚拟变量共线。

**关键观察：** $D_1+D_2=\iota$（每个人非男即女），所以 $\{\iota,D_1,D_2\}$ 线性相关。

- **(3.52) 不可估：** 列 $\iota,D_1,D_2$ 共线（$\iota=D_1+D_2$）⇒ $X'X$ 奇异 ⇒ OLS 无解。
- **(3.53) 可估：** 只用 $D_1,D_2$（去掉单独截距），二者线性独立。
- **(3.54) 可估：** 截距 + 一个虚拟变量（以"女"为基准）。

**(a) 比较 (3.53) 与 (3.54)：** col($D_1,D_2$)=col($\iota,D_1$)=col($\iota,D_2$)（因 $D_2=\iota-D_1$），**列空间相同 ⇒ 拟合完全相同**。参数关系：在 (3.53) 中 $\hat\alpha_1=\bar Y_{\text{男}}$、$\hat\alpha_2=\bar Y_{\text{女}}$；在 (3.54) 中 $\hat\mu=\bar Y_{\text{女}}=\hat\alpha_2$、$\hat\phi=\bar Y_{\text{男}}-\bar Y_{\text{女}}=\hat\alpha_1-\hat\alpha_2$。即 $\alpha_1=\mu+\phi$，$\alpha_2=\mu$。一个更一般（(3.54) 把"性别效应"压缩成一个差值 $\phi$，基准设为女性）。

**(b)** $\iota'D_1=n_1$（男人的个数），$\iota'D_2=n_2$（女人的个数）。

> **和本科对照：** 这正是陈强/李子奈反复强调的"类别变量有 $m$ 类，只能放 $m-1$ 个虚拟变量 + 截距"，否则与截距共线。这里 $D_1+D_2=\iota$ 就是共线源头。

---

## Exercise 3.13　组内去均值与 FWL（"within" 估计量）

**题：** $D_1,D_2$ 同上。
**(a)** 回归 $Y=D_1\gamma_1+D_2\gamma_2+u$，证 $\hat\gamma_1=\bar Y_1$（男均值），$\hat\gamma_2=\bar Y_2$（女均值）。
**(b)** 描述变换 $Y^*=Y-D_1\bar Y_1-D_2\bar Y_2$，$X^*=X-D_1\bar X_1'-D_2\bar X_2'$。
**(c)** 比较 $Y^*=X^*\tilde\beta+\tilde e$ 与 $Y=D_1\alpha_1+D_2\alpha_2+X\beta+e$ 中的 $\tilde\beta$ 与 $\hat\beta$。

**考点：** FWL 定理的典型应用——**组内变换（within transformation）**，这是第 17 章面板数据固定效应的雏形。

**(a)** 由正规方程 $D_1'\hat u=0$：$\sum_{\text{男 }i}(Y_i-\hat\gamma_1)=0\Rightarrow\hat\gamma_1=\bar Y_1$；同理 $\hat\gamma_2=\bar Y_2$。

**(b)** $Y^*$ 是**按性别组内去均值**的 $Y$：男人减去男人均值、女人减去女人均值。$X^*$ 同理（$D_1\bar X_1'$ 给每个男人减去男人的 $X$ 均值向量，女人类似）。即先把 $Y$、$X$ 中"组间差异"扣掉。

**(c)** 由 FWL：$Y=D_1\alpha_1+D_2\alpha_2+X\beta+e$ 中的 $\hat\beta$，等于把 $Y$ 和 $X$ 都对 $(D_1,D_2)$ 净化后、残差对残差回归的系数。而"对 $(D_1,D_2)$ 净化"恰是 (b) 的组内去均值，所以
$$\tilde\beta=\hat\beta.$$

> **和本科对照：** 这就是**固定效应 / within 估计量**（陈强 `xtreg, fe` 或先 `egen` 组内去均值再 OLS）。要点：扣掉组均值 = 控制住组（这里是性别）的效应，剩下的斜率 $\beta$ 与原含虚拟变量回归完全一致。FWL 保证了"加虚拟变量"和"组内去均值"两条路殊途同归。

---

## Exercise 3.14　Sherman–Morrison 在线更新公式

**题：** $\hat\beta_n=(X_n'X_n)^{-1}X_n'Y_n$。新增观测 $(Y_{n+1},X_{n+1})$，证
$$\hat\beta_{n+1}=\hat\beta_n+\frac{(X_n'X_n)^{-1}X_{n+1}}{1+X_{n+1}'(X_n'X_n)^{-1}X_{n+1}}\bigl(Y_{n+1}-X_{n+1}'\hat\beta_n\bigr).$$

**考点：** 矩阵求逆引理（Sherman–Morrison）的实战——加一个观测不用重算整个逆矩阵。

**工具（Sherman–Morrison）：** 对可逆 $A$ 与列向量 $u$，若 $1+u'A^{-1}u\ne0$：
$$(A+uu')^{-1}=A^{-1}-\frac{A^{-1}uu'A^{-1}}{1+u'A^{-1}u}.$$

**证明：** 记 $A_n=X_n'X_n$，$c_n=X_n'Y_n$。新增观测使 $A_{n+1}=A_n+X_{n+1}X_{n+1}'$，$c_{n+1}=c_n+X_{n+1}Y_{n+1}$。对 $A_{n+1}$ 用 SM（$u=X_{n+1}$）：
$$A_{n+1}^{-1}=A_n^{-1}-\frac{A_n^{-1}X_{n+1}X_{n+1}'A_n^{-1}}{1+X_{n+1}'A_n^{-1}X_{n+1}}.$$
于是（注意 $A_n^{-1}c_n=\hat\beta_n$）
\begin{align*}
\hat\beta_{n+1}&=A_{n+1}^{-1}(c_n+X_{n+1}Y_{n+1})\\
&=\Big(A_n^{-1}-\frac{A_n^{-1}X_{n+1}X_{n+1}'A_n^{-1}}{1+X_{n+1}'A_n^{-1}X_{n+1}}\Big)(c_n+X_{n+1}Y_{n+1})\\
&=\hat\beta_n+A_n^{-1}X_{n+1}Y_{n+1}-\frac{A_n^{-1}X_{n+1}X_{n+1}'\hat\beta_n}{1+X_{n+1}'A_n^{-1}X_{n+1}}-\frac{A_n^{-1}X_{n+1}X_{n+1}'A_n^{-1}X_{n+1}Y_{n+1}}{1+X_{n+1}'A_n^{-1}X_{n+1}}.
\end{align*}
把含 $Y_{n+1}$ 的两项合并（提取 $A_n^{-1}X_{n+1}Y_{n+1}/(1+X_{n+1}'A_n^{-1}X_{n+1})$，分子凑出 $1+$ 那一项），整理得
$$\hat\beta_{n+1}=\hat\beta_n+\frac{A_n^{-1}X_{n+1}}{1+X_{n+1}'A_n^{-1}X_{n+1}}\bigl(Y_{n+1}-X_{n+1}'\hat\beta_n\bigr).$$

> **直观：** 新估计 = 旧估计 + 一个**修正项**；修正方向是 $A_n^{-1}X_{n+1}$，幅度正比于**预测误差** $Y_{n+1}-X_{n+1}'\hat\beta_n$（旧模型对新观测预测得越差，修正越大）。分母里的 $1+X_{n+1}'A_n^{-1}X_{n+1}$ 是杠杆的调整。
> **和本科对照：** 这是**递归最小二乘（RLS）/ 在线学习**的基础。本科一般不细讲，但思想朴素：来一个新数据，不必推翻重来，只需小修。

---

## Exercise 3.15　$R^2=$ Corr$(Y,\hat Y)^2$（含截距）

**考点：** $R^2$ 的两种定义等价——"被解释方差比"与"Y 和拟合值的相关系数平方"。

**证明：** 含截距时 $\overline{\hat Y}=\bar Y$（3.11），且 $\hat Y'\hat e=0$（正交分解）。先证一个关键等式：
$$\sum_i(Y_i-\bar Y)(\hat Y_i-\bar Y)=\sum_i(\hat Y_i+\hat e_i-\bar Y)(\hat Y_i-\bar Y)=\underbrace{\sum_i(\hat Y_i-\bar Y)^2}_{=:ESS}+\underbrace{\sum_i\hat e_i(\hat Y_i-\bar Y)}_{=0}.$$
交叉项 $\sum\hat e_i\hat Y_i-\bar Y\sum\hat e_i=0-0=0$（正交 + 残差和为 0）。所以 $\sum(Y_i-\bar Y)(\hat Y_i-\bar Y)=ESS$。
于是样本协方差 $\widehat{\mathrm{Cov}}(Y,\hat Y)=ESS/n$，而 $\widehat{\mathrm{Var}}(\hat Y)=ESS/n$，$\widehat{\mathrm{Var}}(Y)=\mathrm{TSS}/n$（$\mathrm{TSS}=\sum(Y_i-\bar Y)^2$）。故
$$\widehat{\mathrm{Corr}}(Y,\hat Y)^2=\frac{\widehat{\mathrm{Cov}}(Y,\hat Y)^2}{\widehat{\mathrm{Var}}(Y)\widehat{\mathrm{Var}}(\hat Y)}=\frac{ESS^2}{\mathrm{TSS}\cdot ESS}=\frac{ESS}{\mathrm{TSS}}=R^2.$$

> **和本科对照：** 李子奈给出过 $R^2$ 的两个等价定义。此题严格证明二者相等**需要截距**（无截距时残差和 $\ne0$，等式失效）。

---

## Exercise 3.16　嵌套回归 $R_2^2\ge R_1^2$

**题：** 短回归 $Y=X_1\tilde\beta_1+\tilde e$，长回归 $Y=X_1\hat\beta_1+X_2\hat\beta_2+\hat e$。证 $R_2^2\ge R_1^2$，何时相等？

**考点：** $R^2$ 单调性——加变量只会让 SSE 更小（或不变）。

**证明：** 长回归的最小化是在更大范围内取最小：它至少能取到 $\hat\beta_2=0$ 从而复现短回归的 SSE，所以 $\mathrm{SSE}_{\text{长}}\le\mathrm{SSE}_{\text{短}}$。SST 不变（都是 $Y$ 的方差），故 $R_2^2=1-\mathrm{SSE}_{\text{长}}/\mathrm{TST}\ge1-\mathrm{SSE}_{\text{短}}/\mathrm{TST}=R_1^2$。

**相等的充要条件：** 长回归中新增变量的系数恰为 0（$\hat\beta_2=0$），即 $X_2$ 在控制 $X_1$ 后对 $Y$ **无额外解释力**（等价于 $X_2'M_1Y=0$，也即 $\hat\beta_2=0$）。

> **和本科对照：** 这正是"$R^2$ 不能直接比较解释变量个数不同的模型"的原因——加变量必使 $R^2$ 上升，哪怕加的是无关变量。由此引出**调整 $R^2$**（$\bar R^2$，对变量个数施加惩罚）。

---

## Exercise 3.17　$\tilde\sigma^2\ge\hat\sigma^2$

**题：** $\tilde\sigma^2=\tfrac1n\sum_i\tilde e_i^2=\tfrac1n\sum_i(1-h_{ii})^{-2}\hat e_i^2$，证 $\tilde\sigma^2\ge\hat\sigma^2=\tfrac1n\sum\hat e_i^2$。能否相等？

**考点：** 留一预测误差 ≥ 样本内残差——因为留一是"诚实"预测（不用第 $i$ 个观测预测自己）。

**证明：** 由 Theorem 3.6，$0\le h_{ii}\le1$，故 $1-h_{ii}\in(0,1]$（只要 $h_{ii}<1$），$(1-h_{ii})^{-1}\ge1$，$(1-h_{ii})^{-2}\ge1$。于是每项 $(1-h_{ii})^{-2}\hat e_i^2\ge\hat e_i^2$，求和得 $\tilde\sigma^2\ge\hat\sigma^2$。

**相等的情形：** 当且仅当凡 $\hat e_i\ne0$ 处都有 $h_{ii}=0$。但 $\sum h_{ii}=k>0$（只要 $k\ge1$），所以一般严格成立 "$>$"；唯一的相等特例是**完全拟合** $\hat e_i\equiv0$（此时两边都为 0）。

> **和本科对照：** $\hat\sigma^2$（样本内）偏乐观，$\tilde\sigma^2$（留一/样本外）更接近真实预测误差。高杠杆点（$h_{ii}$ 大）被放大更多，这正是**交叉验证**衡量泛化误差的思想。

---

## Exercise 3.18　$\hat\beta_{(-i)}=\hat\beta$ 何时成立？

**考点：** 哪个观测"删了也不影响回归线"。

**证明：** 由 Theorem 3.7，$\hat\beta_{(-i)}=\hat\beta-(X'X)^{-1}X_i\tilde e_i$。因 $X_i$ 含常数分量 1（非零），$\hat\beta_{(-i)}=\hat\beta$ 当且仅当 $\tilde e_i=0$；而 $\tilde e_i=(1-h_{ii})^{-1}\hat e_i=0$ 当且仅当 $\hat e_i=0$。

**结论：** 第 $i$ 个观测**残差为 0**（恰好落在拟合平面上）时，删掉它回归线纹丝不动。

> **和本科对照：** 这定义了**影响点（influential observation）**——删掉会改变 $\hat\beta$ 的观测。残差大 **且** 杠杆高（$\tilde e_i$ 大）的点才真正有影响（Cook 距离正是用 $\tilde e_i$ 和 $h_{ii}$ 构造）。

---

## Exercise 3.19　截距模型的留一预测误差

**题：** $Y_i=\beta+e_i$，证 $\tilde e_i=\frac{n}{n-1}(Y_i-\bar Y)$。

**考点：** 在最简单的模型上把留一公式走一遍，建立直觉。

**证明：** 截距模型中 $X=\iota$（$n\times1$ 全 1），$\hat\beta=\bar Y$。杠杆值
$$h_{ii}=X_i'(X'X)^{-1}X_i=1\cdot(\iota'\iota)^{-1}\cdot1=\frac1n.$$
于是
$$\tilde e_i=(1-h_{ii})^{-1}\hat e_i=\Big(1-\frac1n\Big)^{-1}(Y_i-\bar Y)=\frac{n}{n-1}(Y_i-\bar Y).$$

> **直观：** 截距模型里，所有观测杠杆都等于 $1/n$（完全平衡），留一残差只是把普通残差放大 $\frac{n}{n-1}$ 倍。

---

## Exercise 3.20　留一方差估计量公式

**题：** $\hat\sigma^2_{(-i)}=\frac{1}{n-1}\sum_{j\ne i}(Y_j-X_j'\hat\beta_{(-i)})^2$。证
$$\hat\sigma^2_{(-i)}=\frac{n}{n-1}\hat\sigma^2-\frac{\hat e_i^2}{(n-1)(1-h_{ii})}.$$

**考点：** 把"留一平方和"用全样本量表示出来——综合运用幂等性、杠杆值。这是本章最考验代数功力的一题，下面逐步推导。

**关键引理（两个恒等式，都用幂等性）：**

1. **$\sum_{j\ne i}h_{ji}\hat e_j=-h_{ii}\hat e_i$。** 证：$\sum_j h_{ji}\hat e_j=X_i'(X'X)^{-1}\underbrace{X'\hat e}_{=0}=0$，拆出 $j=i$ 项即得。
2. **$\sum_{j\ne i}h_{ji}^2=h_{ii}(1-h_{ii})$。** 证：$\sum_j h_{ji}^2=(P^2)_{ii}=P_{ii}=h_{ii}$（$P$ 幂等且对称），减去 $h_{ii}^2$ 即得。

**主推导：** 由 Theorem 3.7，$\hat\beta_{(-i)}=\hat\beta-(X'X)^{-1}X_i\tilde e_i$。对 $j\ne i$：
$$Y_j-X_j'\hat\beta_{(-i)}=\underbrace{Y_j-X_j'\hat\beta}_{=\hat e_j}+\underbrace{X_j'(X'X)^{-1}X_i}_{=h_{ji}}\tilde e_i=\hat e_j+h_{ji}\tilde e_i.$$
平方求和（$j\ne i$）：
$$\mathrm{SSE}_{(-i)}=\sum_{j\ne i}(\hat e_j+h_{ji}\tilde e_i)^2=\underbrace{\sum_{j\ne i}\hat e_j^2}_{=\mathrm{SSE}-\hat e_i^2}+2\tilde e_i\underbrace{\sum_{j\ne i}h_{ji}\hat e_j}_{=-h_{ii}\hat e_i}+\tilde e_i^2\underbrace{\sum_{j\ne i}h_{ji}^2}_{=h_{ii}(1-h_{ii})}.$$
代入 $\tilde e_i=\hat e_i/(1-h_{ii})$，后两项合并：
$$2\tilde e_i(-h_{ii}\hat e_i)+\tilde e_i^2 h_{ii}(1-h_{ii})=-\frac{2h_{ii}\hat e_i^2}{1-h_{ii}}+\frac{h_{ii}\hat e_i^2}{1-h_{ii}}=-\frac{h_{ii}\hat e_i^2}{1-h_{ii}}.$$
故
$$\mathrm{SSE}_{(-i)}=(\mathrm{SSE}-\hat e_i^2)-\frac{h_{ii}\hat e_i^2}{1-h_{ii}}=\mathrm{SSE}-\hat e_i^2\frac{1-h_{ii}+h_{ii}}{1-h_{ii}}=\mathrm{SSE}-\frac{\hat e_i^2}{1-h_{ii}}.$$
最后 $\hat\sigma^2_{(-i)}=\frac{1}{n-1}\mathrm{SSE}_{(-i)}=\frac{1}{n-1}\Big(n\hat\sigma^2-\frac{\hat e_i^2}{1-h_{ii}}\Big)$，即
$$\boxed{\ \hat\sigma^2_{(-i)}=\frac{n}{n-1}\hat\sigma^2-\frac{\hat e_i^2}{(n-1)(1-h_{ii})}\ }.$$

> **直观：** 留一方差 = 全样本方差放大 $\frac{n}{n-1}$ 倍，再扣掉第 $i$ 个观测的贡献 $\frac{\hat e_i^2}{(n-1)(1-h_{ii})}$。残差大、杠杆高的观测被扣得最多——再次说明高杠杆点对误差估计影响大。

---

## Exercise 3.21　正交回归元 → "逐个回归"可行

**题：** 联合回归 $Y_i=X_{1i}\hat\beta_1+X_{2i}\hat\beta_2+\hat e_i$ 与"逐个"回归 $Y_i=X_{1i}\tilde\beta_1+\tilde e_{1i}$、$Y_i=X_{2i}\tilde\beta_2+\tilde e_{2i}$。何时 $\tilde\beta_1=\hat\beta_1$ 且 $\tilde\beta_2=\hat\beta_2$？

**考点：** FWL 的反面——当回归元正交时，多元回归可拆成多个一元回归。

**证明：** 条件是 $X_1'X_2=0$（两块正交）。由 FWL，$\hat\beta_2=(X_2'M_1X_2)^{-1}X_2'M_1Y$，其中 $M_1X_2=X_2-P_1X_2=X_2-X_1(X_1'X_1)^{-1}\underbrace{X_1'X_2}_{=0}=X_2$。于是
$$\hat\beta_2=(X_2'X_2)^{-1}X_2'(Y-P_1Y)=(X_2'X_2)^{-1}X_2'Y-\underbrace{(X_2'X_2)^{-1}X_2'X_1}_{=0}(\cdots)=\tilde\beta_2.$$
对称地 $\hat\beta_1=\tilde\beta_1$。

> **和本科对照：** 多重共线性（$X_1'X_2\ne0$）时，"逐个回归"会丢掉变量间的相互影响，得到不同的系数；只有正交（如正交设计、主成分回归）时才相等。这是 3.22 的反面对照。

---

## Exercise 3.22　"残差对残差"的常见错误

**题：** 先回归 $Y_i=X_{1i}'\tilde\beta_1+\tilde u_i$，再把残差 $\tilde u_i$ 回归到 $X_{2i}$：$\tilde u_i=X_{2i}'\tilde\beta_2+\tilde e_i$。是否有 $\tilde\beta_2=\hat\beta_2$（联合回归 $Y=X_1\hat\beta_1+X_2\hat\beta_2+\hat e$）？

**考点：** FWL 的正确用法 vs 常见误用。

**答案：一般不相等。** FWL 要求把 $Y$ **和** $X_2$ **都**对 $X_1$ 净化；这里只净化了 $Y$，$X_2$ 还带着与 $X_1$ 相关的部分，于是 $\tilde\beta_2$ 混入了 $X_1$ 的影响。

**代数：** $\tilde\beta_2=(X_2'X_2)^{-1}X_2'M_1Y$，而正确的 $\hat\beta_2=(X_2'M_1X_2)^{-1}X_2'M_1Y$。两者分母不同（$X_2'X_2\ne X_2'M_1X_2$，除非 $X_1'X_2=0$），故一般不等。

> **和本科对照：** 陈强明确警告过的常见错误——"先回归 Y 于 X₁，再回归残差于 X₂"**是错的**。正确做法（FWL）：把 Y 和 X₂ **都**先对 X₁ 回归取残差，再残差对残差回归。

---

## Exercise 3.23　差分变换不改变残差方差

**题：** $X=[X_1,X_2]$，$Z=[X_1,X_2-X_1]$。$Y$ 对 $X$、$Y$ 对 $Z$ 回归，残差方差 $\hat\sigma^2$ 与 $\tilde\sigma^2$ 有何关系？

**考点：** Ex 3.2 的应用——$Z$ 是 $X$ 的可逆线性变换，列空间相同。

**证明：** $Z=XC$，其中 $C=\begin{pmatrix}I&-I\\0&I\end{pmatrix}$ 可逆（$C^{-1}=\begin{pmatrix}I&I\\0&I\end{pmatrix}$）。由 Ex 3.2，两回归**拟合值、残差完全相同**，故
$$\hat\sigma^2=\tilde\sigma^2.$$

> **和本科对照：** 把 $X_2$ 换成 $X_2-X_1$（如"差分"、或把水平换成变化量）不改变残差/拟合，只改变系数的**解读**（新系数是相对 $X_1$ 的增量效应）。R²、SSE、$\hat\sigma^2$ 这些"整体拟合"量都不变。

---

## Exercise 3.24（CPS，方程 3.49）　实证 + FWL 演示

**样本：** Asian（race=4）、never married（marital=7）、male、experience $<45$；$n=267$。

**(a) 估计 (3.49)：**

| 系数 | 估计 |
|------|------|
| education | 0.1443 |
| experience | 0.0426 |
| exp$^2$/100 | $-0.0951$ |
| intercept | 0.5309 |

$R^2\approx0.389$，$\mathrm{SSE}\approx82.505$（与书 3.49 一致）。

**(b) FWL 两步法重估教育斜率：**
1. 把 log(wage) 对 (experience, exp², 截距) 回归，取残差 $\tilde Y$；
2. 把 education 对 (experience, exp², 截距) 回归，取残差 $\tilde X_1$；
3. 把 $\tilde Y$ 对 $\tilde X_1$ 回归 → 斜率恰为 **0.1443**，与 (a) 一致；该残差回归的 SSE 也等于 82.505。

这正是 FWL：教育的偏效应 = "剥掉经验影响后的 wage 残差" 对 "剥掉经验影响后的 education 残差" 的斜率。

**(c) R² 与 SSE 是否相等？** **SSE 相等**（FWL 保证），但 **R² 不同**：两步法第三步的 SST 是 $\tilde Y$（净化后）的方差，不是 $Y$ 的方差，故 $R^2$ 的分母变了。

> **和本科对照：** 这就是陈强讲的**偏回归系数 / partial regression** 的实证操作。FWL 把"多元回归中某变量的系数"还原成一个可视化的两步净化 + 残差散点图。

---

## Exercise 3.25　数值核对 OLS 性质

估计 (3.49) 后，数值计算七个求和：

| 量 | 结果 | 解释 |
|----|------|------|
| $\sum\hat e_i$ | $\approx0$ | 截距在 $X$ 中（正规方程） |
| $\sum X_{1i}\hat e_i$ | $\approx0$ | education 在 $X$ 中 |
| $\sum X_{2i}\hat e_i$ | $\approx0$ | experience 在 $X$ 中 |
| $\sum X_{1i}^2\hat e_i$ | $\approx133.1\ne0$ | **edu² 不在 $X$ 中** |
| $\sum X_{2i}^2\hat e_i$ | $\approx0$ | exp²/100 在 $X$ 中（差常数倍） |
| $\sum\hat Y_i\hat e_i$ | $\approx0$ | $\hat Y\in\mathrm{col}(X)$，正交分解 |
| $\sum\hat e_i^2$ | $82.505$ | 即 SSE |

> **与第 2 章的呼应（重要）：** 这与 Ch2 的 $E[Xe]=0$ vs $E[X^2e]$（Ex 2.11）**完全对应**，只是这里是**样本**版：残差与 $X$ 的每一列正交（$\Rightarrow$ 与 $X$ 不相关），但与 $X^2$（不在 $X$ 中）未必。OLS 只保证 $X'\hat e=0$，不保证高阶正交。

---

## Exercise 3.26　白人男性西班牙裔工资回归（含地区/婚姻虚拟变量）

**样本：** race=1（White）、female=0、hisp=1，$n\approx4230$，$R^2\approx0.249$。

| 变量 | 系数 |
|------|------|
| education | 0.088 |
| experience | 0.028 |
| exp$^2$/100 | $-0.036$ |
| Northeast | 0.062 |
| South | $-0.068$ |
| West | 0.020 |
| married | 0.178 |
| widowed/divorced | 0.086 |
| separated | 0.017 |
| intercept | 1.193 |

**基准组：** 地区排除 **Midwest**；婚姻排除 **never married**（widowed 与 divorced 合并）。

**(b)** `numpy.linalg.lstsq` 与 `statsmodels.OLS` 系数一致（不同软件包给同一 OLS 解，验证实现无误）。

> **和本科对照：** 这是陈强/李子奈里典型的"含虚拟变量的多元回归"。每个虚拟变量系数 = 该组相对基准组的工资差（控制其他变量后）。注意"基准组选择"只改变系数解读，不改变整体拟合（与 Ex 3.12 同理）。

---

## 复现

运行 `Hansen_Ch03_Exercises_Solutions.ipynb` 全部代码单元（需先下载 `cps09mar` 数据）。

---

## 附录 A：两个矩阵 $P$、$M$ 的性质总表

| 性质 | $P=X(X'X)^{-1}X'$ | $M=I-P$ |
|---|---|---|
| 对称 | $P'=P$ | $M'=M$ |
| 幂等 | $P^2=P$ | $M^2=M$ |
| 乘积 | $PM=MP=0$ | 同左 |
| 作用 | $PX=X$，$PY=\hat Y$ | $MX=0$，$MY=\hat e$ |
| 迹 | $\mathrm{tr}(P)=k$ | $\mathrm{tr}(M)=n-k$ |
| 秩 | $\mathrm{rank}(P)=k$ | $\mathrm{rank}(M)=n-k$ |
| 特征值 | $k$ 个 1，$n-k$ 个 0 | $n-k$ 个 1，$k$ 个 0 |

**FWL 定理（Theorem 3.5）核心：** 分块 $X=[X_1\ X_2]$，记 $M_1=I-X_1(X_1'X_1)^{-1}X_1'$。则
$$\hat\beta_2=(X_2'M_1X_2)^{-1}X_2'M_1Y,$$
且 $\hat\beta_2$ 等于"把 $Y$ 和 $X_2$ 都对 $X_1$ 取残差后、残差对残差回归"的系数。这是偏回归、固定效应（Ch.17）、差分变换的统一工具。

---

## 附录 B：样本构造（与书 §3.21–3.25 一致）

`cps09mar` 列：age, female, hisp, education, earnings, hours, week, union, uncov, region, race, marital。

- **(3.49)：** `race==4`, `marital==7`, `female==0`, `experience=age-education-6 < 45`；`wage=earnings/(hours*week)`。
- **3.26：** `race==1`（White）, `female==0`, `hisp==1`；地区虚拟排除 Midwest；婚姻 married={1,2,3}，widowed/divorced={4,5}，separated={6}，排除 never married={7}。

---

## 附录 C：notebook 单元对应

| 习题 | notebook 内容 |
|------|----------------|
| 3.1–3.23 | Markdown 摘要（详见本 .md） |
| 3.24(a) | 估计 (3.49) 的 code cell |
| 3.24(b)(c) | FWL 残差回归 code cell |
| 3.25 | 七个求和 code cell |
| 3.26 | 工资回归 + statsmodels 对照 |
