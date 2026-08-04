# Bruce Hansen《Econometrics》第 22 章习题解答（详细注释版）

**章节：** Chapter 22 M-Estimators
**出版版：** `hansen/manuscripts/Econometrics_Fullbook.pdf`，PDF 第 823–824 页（印刷页 788–789），§22.10 Exercises（**22.1–22.4 全部**）
**数值验证：** `Hansen_Ch22_Exercises_Solutions.ipynb`

> **写给谁看：** 假设你学过李子奈/陈强，会 OLS 和 MLE，但对"**m-估计量**是什么""$\rho$、$\psi$、$Q$、$\Omega$ 怎么算"不清楚。
> m-估计量是**最小化某个目标函数**的估计量：$\hat\theta=\arg\min\frac1n\sum\rho(Y_i,X_i,\theta)$。OLS、MLE、LAD、分位数回归都是 m-估计量的特例——区别只在 $\rho$ 的选择。本章的公式是一个**统一的夹心方差** $V=Q^{-1}\Omega Q^{-1}$，适用于所有 m-估计量。

---

## 0. m-估计量的统一框架

**定义：** m-估计量 $\hat\theta$ 最小化
$$S_n(\theta)=\frac1n\sum_{i=1}^n\rho(Y_i,X_i,\theta).$$

**四个核心函数（做题反复用）：**

| 函数 | 定义 | 直觉 |
|---|---|---|
| $\rho(Y,X,\theta)$ | 目标函数（每观测） | 最小化的对象（如 $-\log$ 似然、$(Y-X'\theta)^2/2$） |
| $\psi=\frac{\partial\rho}{\partial\theta}$ | 得分 / score | 一阶条件的核心：$E[\psi(Y,X,\theta_0)]=0$ |
| $Q=E[-\frac{\partial\psi}{\partial\theta'}]$ | Hessian（期望负二阶导） | "面包"——曲率 |
| $\Omega=E[\psi\psi']$ | 得分方差 | "肉"——得分的波动 |

**渐近分布（夹心再现）：**
$$\sqrt n(\hat\theta-\theta_0)\to_d N(0,V),\quad V=Q^{-1}\Omega Q^{-1}.$$

> **与前面章节的关系：**
> - OLS：$\rho=(Y-X'\theta)^2/2$，$Q=E[XX']$，$\Omega=E[XX'e^2]$（第 7 章夹心）。
> - MLE：$\rho=-\log f$，信息等式 $Q=\Omega$（方差简化为 $Q^{-1}$）。
> - 本章把这一切统一：**换 $\rho$ 就是换估计方法，但夹心公式不变。**

---

## 预备记号

模型 $Y=X'\theta+e$，$e\perp X$，密度 $f(e)$。
$\rho(Y,X,\theta)$：目标函数；$\psi=\partial\rho/\partial\theta$：得分；$Q=E[-\partial\psi/\partial\theta']$；$\Omega=E[\psi\psi']$。
渐近方差 $V=Q^{-1}\Omega Q^{-1}$。$e\perp X$ 时 $E[h(e)XX']=E[h(e)]E[XX']$（关键分解技巧）。

---

## Exercise 22.1　已知密度 $f(e)$ 的 MLE

**题：** $Y=X'\theta+e$，$e$ 独立于 $X$，密度 $f(e)$ 连续可微。

### (a) 条件密度 $f(y\mid x)=f(y-x'\theta)$

**证明：** $e=Y-X'\theta$，$e\perp X$。给定 $X=x$，$Y=x'\theta+e$，$e$ 的密度为 $f(e)$。$Y$ 是 $e$ 的**平移**（加常数 $x'\theta$），密度不变形状、只移位：
$$f_{Y|X}(y\mid x)=f(y-x'\theta).\quad□$$

### (b) $\rho$ 和 $\psi$

**MLE 目标**（负对数似然）：$\rho(Y,X,\theta)=-\log f(Y-X'\theta)$。

**得分：**
$$\psi=\frac{\partial\rho}{\partial\theta}=-\frac{f'(Y-X'\theta)}{f(Y-X'\theta)}\cdot\frac{\partial(Y-X'\theta)}{\partial\theta}=-\frac{f'(e)}{f(e)}\cdot(-X)=\ell(e)\,X,$$
其中 $\ell(e):=\frac{f'(e)}{f(e)}=\frac{d}{de}\log f(e)$（对数密度的导数）。

$$\boxed{\ \rho=-\log f(Y-X'\theta),\qquad \psi=\ell(Y-X'\theta)\,X.\ }$$

### (c) 渐近协方差矩阵

**第 1 步（算 $Q$）。** $\frac{\partial\psi}{\partial\theta'}=\ell'(e)\cdot(-X)\cdot X'=-\ell'(e)XX'$，故
$$Q=E[-\partial\psi/\partial\theta']=E[\ell'(e)XX']=E[\ell'(e)]\cdot E[XX']$$
（$e\perp X$ 分解）。定义 $I_f:=E[\ell'(e)]=E\!\left[\frac{d^2}{de^2}\log f(e)\right]$（Fisher 信息量的负值；注意 $\ell'(e)$ 为正因 $-\log f$ 凸）。

**第 2 步（算 $\Omega$）。**
$$\Omega=E[\psi\psi']=E[\ell(e)^2XX']=E[\ell(e)^2]\cdot E[XX'].=:J_f\cdot E[XX'].$$

**第 3 步（信息等式 $Q=\Omega$）。** 对 MLE，分部积分给出 $I_f=J_f$（$E[\ell'(e)]=E[\ell(e)^2]$），即 $Q=\Omega$。故
$$V=Q^{-1}\Omega Q^{-1}=Q^{-1}=\frac{1}{I_f}(E[XX'])^{-1}.$$

$$\boxed{\ V=\frac{1}{E[\ell'(e)]}\,(E[XX'])^{-1}=\frac{1}{I_f}\,(E[XX'])^{-1}.\ }$$

**特例（正态）：** $f(e)=\frac{1}{\sigma\sqrt{2\pi}}e^{-e^2/(2\sigma^2)}$，$\ell(e)=-e/\sigma^2$，$\ell'(e)=-1/\sigma^2$，$I_f=1/\sigma^2$。故 $V=\sigma^2(E[XX'])^{-1}$——正是 **OLS 方差**（MLE=OLS 在正态下）。

---

## Exercise 22.2　一般目标 $g(Y-X'\theta)$

**题：** $\rho(Y,X,\theta)=g(Y-X'\theta)$，$g$ 已知。

### (a) $\rho$ 和 $\psi$

$$\rho=g(Y-X'\theta),\qquad \psi=\frac{\partial\rho}{\partial\theta}=g'(Y-X'\theta)\cdot(-X)=-g'(e)X.$$

$$\boxed{\ \rho=g(Y-X'\theta),\qquad \psi=-g'(Y-X'\theta)\,X.\ }$$

### (b) 渐近协方差

**第 1 步（$Q$）。** $\partial\psi/\partial\theta'=-g''(e)(-X)X'=g''(e)XX'$（注意符号：$\partial(-g'(e)X)/\partial\theta'=-g''(e)(-X)X'=g''(e)XX'$），故
$$Q=E[g''(e)]\cdot E[XX'].$$

**第 2 步（$\Omega$）。** $\Omega=E[g'(e)^2XX']=E[g'(e)^2]\cdot E[XX']$。

**第 3 步（夹心）。**
$$\boxed{\ V=Q^{-1}\Omega Q^{-1}=\frac{E[g'(e)^2]}{(E[g''](e))^2}\,(E[XX'])^{-1}.\ }$$

> **要点：** 一般 $g$ 下信息等式**不成立**（$Q\ne\Omega$），夹心不简化。效率取决于 $E[g'^2]/(E[g''])^2$——这个比值越小越有效。

---

## Exercise 22.3　$g(u)=\frac14 u^4$（四次方损失）

### (a) 连续性 / 可微性

$g(u)=u^4/4$：连续 ✓，一阶可微 $g'(u)=u^3$ ✓，二阶可微 $g''(u)=3u^2$ ✓（光滑）。函数为 **U 形四次**（非负，最小值在 $u=0$），对大残差**惩罚极重**（四次增长远快于二次）。

### (b) $\rho$ 和 $\psi$

$$\rho=\frac14(Y-X'\theta)^4,\qquad \psi=-(Y-X'\theta)^3 X=-e^3X.$$

### (c) 渐近协方差

**$Q$：** $g''(e)=3e^2$，$E[g''(e)]=3E[e^2]=3\sigma^2$。故 $Q=3\sigma^2 E[XX']$。

**$\Omega$：** $g'(e)=e^3$，$E[g'(e)^2]=E[e^6]$（需六阶矩存在）。$\Omega=E[e^6]E[XX']$。

$$\boxed{\ V=\frac{E[e^6]}{9\sigma^4}\,(E[XX'])^{-1}.\ }$$

**与 OLS 比较：** $V_{\mathrm{OLS}}=\sigma^2(E[XX'])^{-1}$，故
$$\frac{V}{V_{\mathrm{OLS}}}=\frac{E[e^6]}{9\sigma^6}.$$

**正态特例：** $E[e^6]=15\sigma^6$，$V/V_{\mathrm{OLS}}=15/9=5/3\approx1.67$。即四次方损失估计量比 OLS **效率低 67%**——因为 OLS 是正态下的 MLE（最优），四次方损失过度惩罚大残差、偏离最优。

> **MC 验证（notebook）：** 正态误差下，四次方损失估计量的 MC 方差约为 OLS 的 1.67 倍 ✓。

---

## Exercise 22.4　$g(u)=1-\cos(u)$（余弦损失）

### (a) 连续性 / 可微性

$g(u)=1-\cos(u)$：连续 ✓，$g'(u)=\sin(u)$ ✓，$g''(u)=\cos(u)$ ✓（光滑）。函数**振荡**：$g(0)=0$（最小），$g(\pi)=2$（局部最大），$g(2\pi)=0$（又一最小），… 有**无穷多个局部最小**（$u=2k\pi$）——目标函数**非凸**，可能有多个极值。

### (b) $\rho$ 和 $\psi$

$$\rho=1-\cos(Y-X'\theta),\qquad \psi=\sin(Y-X'\theta)\cdot(-X)=-\sin(e)X.$$

（$\frac{\partial(1-\cos e)}{\partial\theta}=\sin(e)\cdot(-X)$。）

### (c) 渐近协方差

**$Q$：** $g''(e)=\cos(e)$，$Q=E[\cos(e)]\cdot E[XX']$。需要 $E[\cos(e)]>0$（否则 $Q$ 奇异）。

**$\Omega$：** $g'(e)=\sin(e)$，$\Omega=E[\sin^2(e)]\cdot E[XX']$。用 $\sin^2(e)=1-\cos^2(e)$：$\Omega=(1-E[\cos^2(e)])E[XX']$。

$$\boxed{\ V=\frac{E[\sin^2(e)]}{(E[\cos(e)])^2}\,(E[XX'])^{-1}=\frac{1-E[\cos^2(e)]}{(E[\cos(e)])^2}\,(E[XX'])^{-1}.\ }$$

> **要点（为什么 $1-\cos$ 不实用）：**
> - 若误差 $e$ 集中在 $0$ 附近（$\cos(e)\approx1$），$E[\cos(e)]>0$，公式有效——但此时 $g\approx e^2/2$（余弦展开），等价于 OLS，无优势。
> - 若误差分散（如 $\sigma$ 大），$E[\cos(e)]\approx0$，$Q$ 近奇异，估计量**不稳定**。
> - 目标函数**非凸**（多个局部最小）——数值优化可能陷入错误极值。
>
> 这题是"**不是所有光滑 $g$ 都好用**"的反例：光滑性不够，还需凸性和唯一最优。

---

## 附录：m-估计量速查表

| 估计量 | $\rho$ | $\psi$ | $Q$ | $\Omega$ | $V$ |
|---|---|---|---|---|---|
| OLS | $e^2/2$ | $-eX$ | $E[XX']$ | $E[e^2XX']$ | $Q^{-1}\Omega Q^{-1}$ |
| MLE (22.1) | $-\log f(e)$ | $\ell(e)X$ | $I_f E[XX']$ | $I_f E[XX']$ | $\frac{1}{I_f}(E[XX'])^{-1}$ |
| 四次方 (22.3) | $e^4/4$ | $-e^3X$ | $3\sigma^2 E[XX']$ | $E[e^6]E[XX']$ | $\frac{E[e^6]}{9\sigma^4}(E[XX'])^{-1}$ |
| 余弦 (22.4) | $1-\cos(e)$ | $-\sin(e)X$ | $E[\cos e]E[XX']$ | $E[\sin^2 e]E[XX']$ | $\frac{E[\sin^2 e]}{(E[\cos e])^2}(E[XX'])^{-1}$ |

**统一公式：** $\psi=-g'(e)X$，$Q=E[g''(e)]E[XX']$，$\Omega=E[g'(e)^2]E[XX']$，$V=\frac{E[g'(e)^2]}{(E[g''(e)])^2}(E[XX'])^{-1}$（当 $e\perp X$）。

---

## 附录：notebook 单元对应

| 习题 | notebook 内容 |
|------|----------------|
| 22.3 | 四次方损失 vs OLS 效率比较（MC 验证 $V/V_{\mathrm{OLS}}=5/3$）code cell |
