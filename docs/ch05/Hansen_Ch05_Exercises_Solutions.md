# Hansen《Econometrics》第 5 章习题解答

**章节：** Chapter 5 Normal Regression  
**书稿页码：** PDF 第 172–173 页（印刷页 152–153），§5.15 Exercises

---

## Exercise 5.1

$Q=\sum_{j=1}^r Z_j^2$，$Z_j\stackrel{iid}{\sim}N(0,1)$。  
$E[Z_j^2]=1\Rightarrow E[Q]=r$。  
$\mathrm{var}(Z_j^2)=E[Z^4]-1=3-1=2\Rightarrow\mathrm{var}(Q)=2r$。

---

## Exercise 5.2

$e\sim N(0,\sigma^2 I)$，$H'H=I_n$。$u=H'e$ 为正态线性变换，  
$E[u]=0$，$\mathrm{var}(u)=\sigma^2 H'H=\sigma^2 I$。

---

## Exercise 5.3

$e\sim N(0,\Sigma)$，$\Sigma=AA'$。$u=A^{-1}e$：$E[u]=0$，$\mathrm{var}(u)=A^{-1}\Sigma A^{-1'}=I$。

---

## Exercise 5.4

$\ell_n=\log L_n$（严格增变换）⇒ $\arg\max\ell_n=\arg\max L_n$。

---

## Exercise 5.5

$\hat Y_i=X_i'\hat\beta$，$\hat\beta\mid X\sim N(\beta,\sigma^2(X'X)^{-1})$（正态回归）。  
$\hat Y_i\mid X\sim N(X_i'\beta,\sigma^2 X_i'(X'X)^{-1}X_i)=N(X_i'\beta,\sigma^2 h_{ii})$。

---

## Exercise 5.6

$\tilde e_i$ 与标准化残差是 $e$ 的线性变换，且由 (3.45)(4.24) 与 $\hat\beta$ 的联合正态结构，  
协方差为零（投影几何：残差空间 $\perp$ 系数估计方向）⇒ 条件独立（联合正态）。

---

## Exercise 5.7

HC 协方差是 $\hat e_i^2$（或 $\tilde e_i^2$）的函数；在正态回归中残差向量与 $\hat\beta$ 独立（给定 $X$），  
故 $\hat V_{\mathrm{HC}\cdot}$ 与 $\hat\beta$ 条件独立。

---

## Exercise 5.8

密度关于 0 对称 ⇒ $P(X\le -u)=P(X\ge u)=1-P(X<u)$。  
连续时 $F(-u)=1-F(u)$。

---

## Exercise 5.9

$g$ 严格增：$\beta\in[L,U]\Leftrightarrow g(\beta)\in[g(L),g(U)]$。覆盖概率相同。  
对 $\sigma>0$ 用 $g=\sqrt{\cdot}$ 作用于 $\sigma^2$ 的区间。

---

## Exercise 5.10

LR 与 $F$ 为严格单调变换关系：$F=(\mathrm{e}^{LR/n}-1)(n-k)/q$。  
临界值按 $c_2=(\mathrm{e}^{c_1/n}-1)(n-k)/q$ 匹配时 **拒绝域相同** ⇒ 决策等价。  
（渐近上二者均可用；有限样本 $F$ 精确性依赖正态。）

---

## Exercise 5.11　证明 (5.20)

正态回归 score：  
$s_\beta=\sigma^{-2}X'e$，$s_{\sigma^2}=\frac{1}{2\sigma^4}\sum(e_i^2-\sigma^2)$。  
$E[s_\beta s_{\sigma^2}'\mid X]=0$（$e$ 与 $e^2-\sigma^2$ 在正态下正交于线性项）。  
$\mathrm{var}(s_\beta\mid X)=\sigma^{-2}X'X$，$\mathrm{var}(s_{\sigma^2}\mid X)=n/(2\sigma^4)$。  
故信息阵为对角块 (5.20)。

---

## Exercise 5.12

**(a)** 正态同方差：$(n-k)s^2/\sigma^2\sim\chi^2_{n-k}$ ⇒ $\mathrm{var}(s^2)=2\sigma^4/(n-k)$。  
**(b)** CRLB 为 $2\sigma^4/n$；因 $n-k<n$，$2\sigma^4/(n-k)>2\sigma^4/n$。$s^2$ 无偏但 **非 CRLB 有效**。

---
