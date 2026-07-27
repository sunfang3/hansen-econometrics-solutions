# Bruce Hansen《Econometrics》第 3 章习题解答

**章节：** Chapter 3 The Algebra of Least Squares  
**对应书稿：** PDF 第 112–116 页（印刷页 92–96），§3.26 Exercises  
**体系统一：** 投影矩阵、残差代数、FWL、leave-one-out、$R^2$、CPS 实证

完整计算见：`Hansen_Ch03_Exercises_Solutions.ipynb`  
数据：`hansen/econometrics/data/cps09mar/`

---

## 预备记号

OLS：$\hat\beta=(X'X)^{-1}X'Y$，$\hat e=MY$，$M=I-P$，$P=X(X'X)^{-1}X'$。  
$h_{ii}=X_i'(X'X)^{-1}X_i$，$\tilde e_i=\hat e_i/(1-h_{ii})$。

方程 (3.49)（单身亚裔男性、经验 $<45$）：
$$\widehat{\log(\mathrm{wage})}=0.144\,\mathrm{edu}+0.043\,\mathrm{exp}-0.095\,\mathrm{exp}^2/100+0.531.$$

---

## Exercise 3.1

$g_n(\hat\mu,\hat\sigma^2)=0$ $\Rightarrow$ $\hat\mu=\bar y$，$\hat\sigma^2=n^{-1}\sum(y_i-\bar y)^2$。

---

## Exercise 3.2

$Z=XC$，$C$ 可逆。则 $\hat\beta_Z=C^{-1}\hat\beta_X$，**拟合与残差相同**。

---

## Exercise 3.3

$X'\hat e=X'Y-X'X\hat\beta=0$。

---

## Exercise 3.4

$X=[X_1\ X_2]$ $\Rightarrow$ $X_2'\hat e=0$。

---

## Exercise 3.5

$\hat e$ 对 $X$ 回归系数 $(X'X)^{-1}X'\hat e=0$。

---

## Exercise 3.6

$\hat Y=PY$ 对 $X$ 回归系数 $=\hat\beta$。

---

## Exercise 3.7

$X_1$ 的列 $\subset\mathrm{col}(X)$ $\Rightarrow$ $PX_1=X_1$，$MX_1=0$。

---

## Exercise 3.8

$M=I-P$，$P^2=P$ $\Rightarrow$ $M^2=M$。

---

## Exercise 3.9

$\mathrm{tr}(M)=n-\mathrm{tr}(P)=n-k$。

---

## Exercise 3.10

$X_1'X_2=0$ $\Rightarrow$ $P=P_1+P_2$。

---

## Exercise 3.11

含截距 $\Rightarrow$ $\sum\hat e_i=0$ $\Rightarrow$ $n^{-1}\sum\hat Y_i=\bar Y$。

---

## Exercise 3.12

虚拟变量 $D_1$（男）、$D_2$（女）。

- (3.52) $\mu+D_1\alpha_1+D_2\alpha_2$：**不可估**（与截距共线，$\iota=D_1+D_2$）。  
- (3.53)(3.54)：**可估**，张成同一列空间。  
- 关系：$\alpha_1=\mu+\phi$，$\alpha_2=\mu$。  
- $\iota'D_1=n_1$，$\iota'D_2=n_2$。

---

## Exercise 3.13

**(a)** $Y=D_1\hat\gamma_1+D_2\hat\gamma_2+\hat u$ $\Rightarrow$ $\hat\gamma_1=\bar Y_{\mathrm{men}}$，$\hat\gamma_2=\bar Y_{\mathrm{women}}$。  

**(b)** $Y^*,X^*$ 为按性别组内去均值。  

**(c)** $Y^*$ 对 $X^*$ 的 $\tilde\beta$ 等于 $Y=D_1\alpha_1+D_2\alpha_2+X\beta+e$ 中的 $\hat\beta$（FWL/within）。

---

## Exercise 3.14

Sherman–Morrison 更新：
$$\hat\beta_{n+1}=\hat\beta_n+\frac{(X_n'X_n)^{-1}X_{n+1}}{1+X_{n+1}'(X_n'X_n)^{-1}X_{n+1}}
\bigl(Y_{n+1}-X_{n+1}'\hat\beta_n\bigr).$$

---

## Exercise 3.15

含截距时 $R^2=\widehat{\mathrm{Corr}}(Y,\hat Y)^2$。

---

## Exercise 3.16

长回归嵌套短回归 $\Rightarrow$ $R_2^2\ge R_1^2$；相等 iff 新增变量系数全为 0。

---

## Exercise 3.17

$\tilde e_i=\hat e_i/(1-h_{ii})$ $\Rightarrow$ $\tilde\sigma^2\ge\hat\sigma^2$。完美拟合时相等（皆 0）。

---

## Exercise 3.18

$\hat\beta_{(-i)}=\hat\beta$ 当 $\hat e_i=0$（或等价 $\tilde e_i=0$）。

---

## Exercise 3.19

截距模型：$h_{ii}=1/n$，$\tilde e_i=\frac{n}{n-1}(Y_i-\bar Y)$。

---

## Exercise 3.20

$$\hat\sigma^2_{(-i)}=\frac{n}{n-1}\hat\sigma^2-\frac{\hat e_i^2}{(n-1)(1-h_{ii})}.$$
（由 LOO 残差平方和恒等式。）

---

## Exercise 3.21

$\tilde\beta_j=\hat\beta_j$ 当回归元正交（$X_1'X_2=0$）。

---

## Exercise 3.22

只把 $Y$ 对 $X_1$ 残差化再对 $X_2$ 回归 **一般不等于** 联合 $\hat\beta_2$。  
正确 FWL 需 $Y$ 与 $X_2$ 都对 $X_1$ 残差化。

---

## Exercise 3.23

$Z=[X_1,X_2-X_1]=XC$（$C$ 可逆）$\Rightarrow$ 残差相同 $\Rightarrow$ $\hat\sigma^2=\tilde\sigma^2$。

---

## Exercise 3.24（CPS，方程 3.49）

**样本：** Asian（race=4）、never married（marital=7）、male、experience $<45$；$n=267$。

| 系数 | 估计 |
|------|------|
| education | 0.1443 |
| experience | 0.0426 |
| exp$^2$/100 | $-0.0951$ |
| intercept | 0.5309 |

$R^2\approx0.389$，$\mathrm{SSE}\approx82.505$（与书 3.49 一致）。

**(b)** FWL 得相同 education 斜率 $0.1443$，SSE 相同。  
**(c)** SSE 相同；$R^2$ 不同（SST 定义不同）。

---

## Exercise 3.25

| 量 | 结果 | 解释 |
|----|------|------|
| $\sum\hat e_i$ | $\approx0$ | 含截距 |
| $\sum X_{1i}\hat e_i$ | $\approx0$ | edu 在 $X$ |
| $\sum X_{2i}\hat e_i$ | $\approx0$ | exp 在 $X$ |
| $\sum X_{1i}^2\hat e_i$ | $\approx133.1\neq0$ | edu$^2$ 不在 $X$ |
| $\sum X_{2i}^2\hat e_i$ | $\approx0$ | exp$^2/100$ 在 $X$ |
| $\sum\hat Y_i\hat e_i$ | $\approx0$ | 投影正交 |
| $\sum\hat e_i^2$ | $82.505$ | SSE |

与 OLS 理论一致。

---

## Exercise 3.26

白人男性西班牙裔（race=1, female=0, hisp=1），$n=4230$，$R^2\approx0.249$。

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

基准：Midwest；never married。  
**(b)** `numpy.linalg.lstsq` 与 `statsmodels.OLS` 系数一致。

---

## 复现

运行 `Hansen_Ch03_Exercises_Solutions.ipynb` 全部代码单元。


---

## 附录 A：Exercise 3.14 证明细节

令 $A_n=X_n'X_n$，$c_n=X_n'Y_n$，$\hat\beta_n=A_n^{-1}c_n$。  
$A_{n+1}=A_n+X_{n+1}X_{n+1}'$，$c_{n+1}=c_n+X_{n+1}Y_{n+1}$。  
Sherman–Morrison：
$$
A_{n+1}^{-1}=A_n^{-1}-\frac{A_n^{-1}X_{n+1}X_{n+1}'A_n^{-1}}{1+X_{n+1}'A_n^{-1}X_{n+1}}.
$$
于是
\begin{align*}
\hat\beta_{n+1}
&=A_{n+1}^{-1}(c_n+X_{n+1}Y_{n+1})\\
&=\hat\beta_n+\frac{A_n^{-1}X_{n+1}}{1+X_{n+1}'A_n^{-1}X_{n+1}}
\bigl(Y_{n+1}-X_{n+1}'\hat\beta_n\bigr).
\end{align*}

---

## 附录 B：样本构造（与书 §3.21–3.25 一致）

`cps09mar` 列：age, female, hisp, education, earnings, hours, week, union, uncov, region, race, marital。

- **(3.49)：** `race==4`, `marital==7`, `female==0`, `experience=age-education-6 < 45`。  
  `wage=earnings/(hours*week)`。
- **3.26：** `race==1`（White only）, `female==0`, `hisp==1`；  
  地区虚拟排除 Midwest；婚姻：married={1,2,3}，widowed/divorced={4,5}，separated={6}，排除 never married={7}。

---

## 附录 C：notebook 单元对应

| 习题 | notebook 内容 |
|------|----------------|
| 3.1–3.23 | Markdown 摘要 |
| 3.24(a) | 估计 (3.49) 的 code cell |
| 3.24(b)(c) | FWL code cell |
| 3.25 | 七个求和 code cell |
| 3.26 | 工资回归 + statsmodels 对照 |
