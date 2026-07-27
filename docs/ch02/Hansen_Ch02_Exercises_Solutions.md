# Bruce Hansen《Econometrics》第 2 章习题解答

**章节：** Chapter 2 Conditional Expectation and Projection  
**对应书稿：** PDF 第 80–81 页（印刷页 60–61），§2.34 Exercises  
**体系统一：** CEF、迭代期望、投影、条件方差（Hansen 记号）

完整数值验证见：`Hansen_Ch02_Exercises_Solutions.ipynb`

---

## 预备记号

条件期望（CEF）$m(X)=E[Y\mid X]$，CEF 误差 $e=Y-m(X)$ 满足 $E[e\mid X]=0$。  
最佳线性预测（投影）$P(Y\mid X)=X'\beta$，其中
$$\beta=\bigl(E[XX']\bigr)^{-1}E[XY],$$
投影误差满足 $E[Xe]=0$（不必 $E[e\mid X]=0$）。

---

## Exercise 2.1

**求** $E\bigl[E\bigl[E[Y\mid X_1,X_2,X_3]\mid X_1,X_2\bigr]\mid X_1\bigr]$。

### 解答

由迭代期望定律（Theorem 2.2）反复作用：
\begin{align*}
E\bigl[E[Y\mid X_1,X_2,X_3]\mid X_1,X_2\bigr]
&=E[Y\mid X_1,X_2],\\
E\bigl[E[Y\mid X_1,X_2]\mid X_1\bigr]
&=E[Y\mid X_1].
\end{align*}
因此
$$
E\bigl[E\bigl[E[Y\mid X_1,X_2,X_3]\mid X_1,X_2\bigr]\mid X_1\bigr]
=E[Y\mid X_1].
$$

---

## Exercise 2.2

若 $E[Y\mid X]=a+bX$，用 $X$ 的矩表示 $E[YX]$。

### 解答

$$
E[YX]=E\bigl[E[YX\mid X]\bigr]=E\bigl[X\,E[Y\mid X]\bigr]
=E\bigl[X(a+bX)\bigr]=a\,E[X]+b\,E[X^2].
$$

---

## Exercise 2.3

用迭代期望证明 Theorem 2.4.4：对任意使 $E|h(X)e|<\infty$ 的 $h$，有 $E[h(X)e]=0$。

### 证明

因 $E[e\mid X]=0$，
$$
E[h(X)e]=E\bigl[E[h(X)e\mid X]\bigr]
=E\bigl[h(X)\,E[e\mid X]\bigr]
=E\bigl[h(X)\cdot 0\bigr]=0.
$$
□

---

## Exercise 2.4

联合分布：$P(Y=0,X=0)=0.1$，$P(Y=0,X=1)=0.2$，$P(Y=1,X=0)=0.4$，$P(Y=1,X=1)=0.3$。

### 解答

$P(X=0)=P(X=1)=0.5$。  
$P(Y=1\mid X=0)=0.8$，$P(Y=1\mid X=1)=0.6$。  
因 $Y\in\{0,1\}$，$Y^2=Y$。

| $X$ | $E[Y\mid X]$ | $E[Y^2\mid X]$ | $\mathrm{var}[Y\mid X]$ |
|:---:|:------------:|:--------------:|:----------------------:|
| 0 | 0.8 | 0.8 | 0.16 |
| 1 | 0.6 | 0.6 | 0.24 |

---

## Exercise 2.5

证明 $\sigma^2(X)=E[e^2\mid X]$ 是 $e^2$ 关于 $X$ 的最佳预测。

### 解答

**(a)** $\mathrm{MSE}(h)=E[(e^2-h(X))^2]$。  
**(b)** 用 $X$ 的可测函数预测平方误差 $e^2$。  
**(c)** 由 Theorem 2.7，CEF $E[e^2\mid X]=\sigma^2(X)$ 最小化均方误差。

---

## Exercise 2.6

用 $Y=m(X)+e$ 证明 $\mathrm{var}[Y]=\mathrm{var}[m(X)]+\sigma^2$。

### 证明

$E[m(X)e]=0$，故
$$\mathrm{var}[Y]=\mathrm{var}[m(X)+e]=\mathrm{var}[m(X)]+\mathrm{var}[e]=\mathrm{var}[m(X)]+\sigma^2.$$
□

---

## Exercise 2.7

证明 $\sigma^2(X)=E[Y^2\mid X]-(E[Y\mid X])^2$。

### 证明

展开 $\mathrm{var}[Y\mid X]=E[(Y-E[Y\mid X])^2\mid X]$ 即得。□

---

## Exercise 2.8

$Y\mid X=x\sim\mathrm{Poisson}(x'\beta)$。

### 解答

$E[Y\mid X]=X'\beta$，$\mathrm{var}[Y\mid X]=X'\beta$。  
可写 $Y=X'\beta+e$ 且 $E[e\mid X]=0$（CEF 线性），但一般 **异方差**，古典同方差不成立。

---

## Exercise 2.9

$X_1\in\{0,1\}$，$X_2\in\{A,B,C\}$。把 $E[Y\mid X_1,X_2]$ 写成线性回归。

### 解答

饱和模型：
\begin{align*}
E[Y\mid X_1,X_2]
&=\beta_0+\beta_1 X_1+\beta_2 1\{X_2=B\}+\beta_3 1\{X_2=C\}\\
&\quad+\beta_4 X_1 1\{X_2=B\}+\beta_5 X_1 1\{X_2=C\}.
\end{align*}
基准：$(X_1,X_2)=(0,A)$。

---

## Exercise 2.10–2.14（True/False）

| 题 | 答案 | 理由 |
|:--:|:----:|------|
| 2.10 | **True** | Thm 2.4.4，$h(x)=x^2$ |
| 2.11 | **False** | $E[Xe]=0\not\Rightarrow E[X^2e]=0$ |
| 2.12 | **False** | 均值独立 $\neq$ 独立 |
| 2.13 | **False** | 投影正交 $\neq$ CEF 正交 |
| 2.14 | **False** | 同方差+均值独立仍可有高阶依赖 |

---

## Exercise 2.15

截距模型 $Y=\alpha+e$，$\alpha$ 为 BLP。证明 $\alpha=E[Y]$。

### 证明

FOC：$E[Y-\alpha]=0\Rightarrow\alpha=E[Y]$。□

---

## Exercise 2.16

$f(x,y)=\frac{3}{2}(x^2+y^2)$ on $[0,1]^2$。

### 解答

$E[X]=E[Y]=\frac{5}{8}$，$E[X^2]=\frac{7}{15}$，$E[XY]=\frac{3}{8}$。  
$$\beta=-\frac{15}{73},\qquad \alpha=\frac{55}{73}.$$
（数值约 $\alpha\approx0.753$，$\beta\approx-0.205$。）

$$
m(x)=E[Y\mid X=x]=\frac{\frac{1}{2}x^2+\frac{1}{4}}{x^2+\frac{1}{3}}.
$$
$m(x)$ 非 $x$ 的仿射函数（$m(0)=0.75$，$m(1)=0.5625$），**BLP 与 CEF 不同**。

---

## Exercise 2.17

$g(x,m,s)=\begin{pmatrix}x-m\\(x-m)^2-s\end{pmatrix}$。  
$E[g(X,m,s)]=0$ 当且仅当 $m=\mu$，$s=\sigma^2$。

### 证明

第一分量 $\Rightarrow m=\mu$；第二分量 $\Rightarrow s=\sigma^2$。□

---

## Exercise 2.18

$X=(1,X_2,X_3)$，$X_3=\alpha_1+\alpha_2 X_2$。

**(a)** 存在 $c\neq0$ 使 $X'c=0$ a.s. $\Rightarrow Q_{XX}$ 奇异。  

**(b)** 有效回归元为 $(1,X_2)$：
$$\begin{pmatrix}\gamma_0\\\gamma_1\end{pmatrix}
=\begin{pmatrix}1&E[X_2]\\E[X_2]&E[X_2^2]\end{pmatrix}^{-1}
\begin{pmatrix}E[Y]\\E[X_2Y]\end{pmatrix}.$$
原 $X$ 上系数不唯一。

---

## Exercise 2.19

$d(\beta)=E[(m(X)-X'\beta)^2]$ 的最小点：
$$\beta=(E[XX'])^{-1}E[Xm(X)]=(E[XX'])^{-1}E[XY].$$

### 证明

二次型 FOC 得 $E[XX']\beta=E[Xm(X)]$；LIE 得 $E[Xm(X)]=E[XY]$。□

---

## Exercise 2.20

有联合密度时 (2.57) 与 (2.6) 一致：对任意可测 $\mathcal{X}$，
$$E[1\{X\in\mathcal{X}\}Y]=E[1\{X\in\mathcal{X}\}m(X)].$$

---

## Exercise 2.21

短 $Y=X\gamma_1+e$；长 $Y=X\beta_1+X_2\beta_2+u$。

**(a)** $\gamma_1=\beta_1+(E[XX'])^{-1}E[XX_2]\beta_2$，故 $\gamma_1=\beta_1$ iff $E[XX_2]\beta_2=0$。  
**(b)** 对 $X_3$ 同理：需 $E[XX_3]\theta_2=0$。两条件一般不同。

---

## Exercise 2.22

同方差长回归中排除 $X_2$。令 $X_2=\Gamma X_1+v$，$E[v\mid X_1]=0$，则
$$Y=X_1'(\beta_1+\Gamma'\beta_2)+u,\quad u=v'\beta_2+e.$$
$$E[u^2\mid X_1]=E[(v'\beta_2)^2\mid X_1]+\sigma^2$$
一般依赖 $X_1$ $\Rightarrow$ **诱导异方差**（除非特殊结构）。

---

## 计算

见 notebook 中 Exercise 2.4 与 2.16 代码单元。


---

## 附录：与第 29 章体系统一

- 条件期望 / 投影区分贯穿全书（Ch.3 OLS 是样本投影；Ch.4 起讨论抽样）。
- True/False 题核心：**$E[e\mid X]=0$ 强于 $E[Xe]=0$**；独立更强。
- 计算题 2.4、2.16 的可运行代码见 notebook 对应 cell。
