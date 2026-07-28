# Hansen《Econometrics》第 14 章习题完整解答

**章节：** Chapter 14 Time Series  
**书稿：** PDF 第 525–528 页（印刷页 505–508），§14.48 Exercises（**14.1–14.22 全部**）

---

## Exercise 14.1

严格平稳、遍历、$E[Y_t^2]<\infty$。证明 $\hat\gamma(k)\to_p\gamma(k)$，$\hat\rho(k)\to_p\rho(k)$。

### 证明

记 $\mu=E[Y_t]$，$\bar Y\to_p\mu$（遍历定理）。  
$\gamma(k)=\mathrm{Cov}(Y_t,Y_{t-k})=E[(Y_t-\mu)(Y_{t-k}-\mu)]$。  

样本：
$$
\hat\gamma(k)=n^{-1}\sum_{t=k+1}^n (Y_t-\bar Y)(Y_{t-k}-\bar Y).
$$
展开：
\begin{align*}
\hat\gamma(k)
&=n^{-1}\sum_{t=k+1}^n (Y_t-\mu)(Y_{t-k}-\mu)
-(\bar Y-\mu)n^{-1}\sum(Y_{t-k}-\mu)\\
&\quad-(\bar Y-\mu)n^{-1}\sum(Y_t-\mu)+(\bar Y-\mu)^2\cdot\frac{n-k}{n}.
\end{align*}
第一项：对平稳遍历序列 $W_t=(Y_t-\mu)(Y_{t-k}-\mu)$，$E|W_t|\le E Y_t^2<\infty$，遍历定理得  
$n^{-1}\sum_{t=k+1}^n W_t\to_p E[W_1]=\gamma(k)$（边界 $k/n\to0$ 不影响）。  
其余项含 $(\bar Y-\mu)=o_p(1)$ 故 $\to_p0$。  
因此 $\hat\gamma(k)\to_p\gamma(k)$，$\hat\gamma(0)\to_p\gamma(0)$。  
连续映射：$\hat\rho(k)=\hat\gamma(k)/\hat\gamma(0)\to_p\gamma(k)/\gamma(0)=\rho(k)$（$\gamma(0)>0$）。□

---

## Exercise 14.2

$(e_t,\mathcal F_t)$ MDS，$X_t$ 为 $\mathcal F_t$-可测 ⇒ $u_t=X_{t-1}e_t$ 是 MDS。

### 证明

需 $E[u_t\mid\mathcal F_{t-1}]=0$。  
$X_{t-1}$ 对 $\mathcal F_{t-1}$ 可测，MDS 性 $E[e_t\mid\mathcal F_{t-1}]=0$，故  
$E[X_{t-1}e_t\mid\mathcal F_{t-1}]=X_{t-1}E[e_t\mid\mathcal F_{t-1}]=0$。  
（取 $\mathcal F_t^u=\mathcal F_t$ 即可。）□

---

## Exercise 14.3

$\sigma_t^2=E[e_t^2\mid\mathcal F_{t-1}]$，$u_t=e_t^2-\sigma_t^2$ 是 MDS。

### 证明

$E[u_t\mid\mathcal F_{t-1}]=E[e_t^2\mid\mathcal F_{t-1}]-\sigma_t^2=0$。□

---

## Exercise 14.4

$E[e_t^4]<\infty$ 时 $n^{-1/2}\sum(e_t^2-\sigma_t^2)\to_d N(0,v^2)$。

### 解答

$u_t=e_t^2-\sigma_t^2$ 为 MDS（上题），且 $E[u_t^2]=E[(e_t^2-\sigma_t^2)^2]<\infty$（由 $E e^4<\infty$）。  
MDS CLT：$n^{-1/2}\sum u_t\to_d N(0,v^2)$，  
$$
v^2=E[u_t^2]=E[(e_t^2-\sigma_t^2)^2]
=E[e_t^4]-2E[e_t^2\sigma_t^2]+E[\sigma_t^4].
$$
若进一步 $\sigma_t^2=\sigma^2$ 常数，则 $v^2=E[e_t^4]-\sigma^4$。  
一般也可写 $v^2=E[\mathrm{Var}(e_t^2\mid\mathcal F_{t-1})]$。

---

## Exercise 14.5　随机波动

$Y_t=\sigma_t e_t$，$\log\sigma_t^2=\omega+\beta\log\sigma_{t-1}^2+u_t$，$e_t,u_t$ 独立 i.i.d. $N(0,1)$。

**(a)** 取 $\mathcal F_{t-1}=\sigma(\sigma_s,e_s,u_s:s<t)$（或含 $\sigma_t$ 的信息）。  
因 $e_t\perp\mathcal F_{t-1}$ 且 $E[e_t]=0$，$E[Y_t\mid\mathcal F_{t-1}]=\sigma_t E[e_t\mid\mathcal F_{t-1}]=0$  
（若 $\sigma_t$ 对 $\mathcal F_{t-1}$ 可测）。故 $(Y_t,\mathcal F_t)$ 为 MDS。

**(b)** $|\beta|<1$ 时 $\log\sigma_t^2$ 为平稳遍历 AR(1)（高斯创新）。  
$\sigma_t^2=\exp(\log\sigma_t^2)$ 平稳，$Y_t=\sigma_t e_t$ 为平稳过程之乘积，在标准条件下严格平稳且遍历。

---

## Exercise 14.6　MA(1)

$Y_t=e_t+\theta e_{t-1}$，$e_t\sim\mathrm{WN}(0,\sigma^2)$。  
$\gamma(0)=(1+\theta^2)\sigma^2$，$\gamma(1)=\theta\sigma^2$，$\gamma(k)=0$ ($|k|>1$)。  
$\rho(1)=\theta/(1+\theta^2)$。□

---

## Exercise 14.7　MA($\infty$)

$Y_t=\sum_{j=0}^\infty\theta_j e_{t-j}$（因果可和）。  
$\gamma(k)=\sigma^2\sum_{j=0}^\infty\theta_j\theta_{j+k}$，$\gamma(0)=\sigma^2\sum\theta_j^2$。  
（若 MA($q$) 有限则和到 $q$。）  
$\rho(k)=\gamma(k)/\gamma(0)$ 即题给公式。

---

## Exercise 14.8

$Y_t=Y_{t-1}+e_t$，$e_t$ i.i.d.$(0,1)$，$Y_0=0$。  
$Y_t=\sum_{j=1}^t e_j$，$\mathrm{var}(Y_t)=t$。  
**非平稳**（方差随 $t$ 增；随机游走）。

---

## Exercise 14.9　AR(1) 脉冲响应

$Y_t=\alpha_1 Y_{t-1}+e_t$。

**(a)** $b_j=\partial Y_{t+j}/\partial e_t=\alpha_1^j$。  

**(b)** $\hat b_j=\hat\alpha_1^j$。  

**(c)** $\mathrm{se}(\hat b_j)\approx |j\hat\alpha_1^{j-1}|s(\hat\alpha_1)$（delta），  
95% CI：$\hat b_j\pm 1.96\,\widehat{\mathrm{se}}$。

---

## Exercise 14.10　AR(2) 脉冲

$Y_t=\alpha_1 Y_{t-1}+\alpha_2 Y_{t-2}+e_t$。（题中第二滞后写为 $Y_{t-1}$ 应为 $Y_{t-2}$。）

**(a)** $b_0=1$，$b_1=\alpha_1$，$b_2=\alpha_1^2+\alpha_2$，  
$b_j=\alpha_1 b_{j-1}+\alpha_2 b_{j-2}$（$j\ge2$）。  
$b_3=\alpha_1 b_2+\alpha_2 b_1$，$b_4=\alpha_1 b_3+\alpha_2 b_2$。  

**(b)** $\hat b_2=\hat\alpha_1^2+\hat\alpha_2$。  

**(c)** $g(\alpha)=\alpha_1^2+\alpha_2$，$\nabla g=(2\alpha_1,1)$，  
$\widehat{\mathrm{se}}=\sqrt{\nabla g'\hat V\nabla g}$，CI：$\hat b_2\pm1.96\,\widehat{\mathrm{se}}$。

---

## Exercise 14.11

$\alpha(L)Y_t=\alpha_0+e_t$ 与 $\alpha(L)Y_t=\mu+u_t$，$\alpha(L)u_t=e_t$。  

第二套：$\alpha(L)(Y_t-\mu)=u_t$，$\alpha(L)u_t=e_t\Rightarrow\alpha(L)^2(Y_t-\mu)=e_t$ 不同。  

题意：第二种是水平常数均值形式 $\alpha(L)(Y_t-\mu)=e_t$，即  
$\alpha(L)Y_t=\alpha(L)\mu+e_t=\alpha_0+e_t$，故 $\alpha_0=\alpha(1)\mu$，  
$\mu=\alpha_0/\alpha(1)$（$\alpha(1)\neq0$）。  
两种写法（截距进 AR 方程 vs 均值形式）**等价**。

---

## Exercise 14.12

$\alpha(L)Y_t=u_t$，$\beta(L)u_t=e_t$ ⇒ $\beta(L)\alpha(L)Y_t=e_t$。  
$\gamma(L)=\beta(L)\alpha(L)$ 阶数为 $p+q$。

---

## Exercise 14.13

$Y_t=e_t+u_t+\theta u_{t-1}$，$e,u$ 互相独立 i.i.d.$(0,1)$。

**(a)** $\gamma(0)=1+1+\theta^2=2+\theta^2$，  
$\gamma(1)=\theta$，$\gamma(k)=0$ ($k\ge2$) ⇒ ACF 同 MA(1)。  

**(b)** MA(1) $\rho(1)=\psi/(1+\psi^2)=\gamma(1)/\gamma(0)=\theta/(2+\theta^2)$。  
解 $\psi/(1+\psi^2)=\theta/(2+\theta^2)$ 得 $\psi$ 为合适根（$|\psi|\le1$ 可逆根）。  

**(c)** $\theta=1$：$\rho(1)=1/3$，解 $\psi/(1+\psi^2)=1/3\Rightarrow\psi^2-3\psi+1=0$，  
$\psi=(3-\sqrt5)/2\in(0,1)$（可逆根）。

---

## Exercise 14.14

$Y_t=X_t+e_t$，$X_t=\alpha X_{t-1}+u_t$，$e\perp u$ i.i.d.  

$(1-\alpha L)Y_t=u_t+e_t-\alpha e_{t-1}$。  
右侧为 MA(1)（一般），左侧 AR(1) ⇒ **ARMA(1,1)**。

---

## Exercise 14.15　高斯 AR(1)

$Y_t=\alpha_0+\alpha_1 Y_{t-1}+e_t$，$|\alpha_1|<1$，$e_t\sim N(0,\sigma^2)$ i.i.d.  

MA：
$$
Y_t=\frac{\alpha_0}{1-\alpha_1}+\sum_{j=0}^\infty\alpha_1^j e_{t-j}.
$$
正态线性组合 ⇒  
$Y_t\sim N\bigl(\alpha_0/(1-\alpha_1),\ \sigma^2/(1-\alpha_1^2)\bigr)$。□

---

## Exercise 14.16　GMM 用三阶矩识别 AR(1)？

$\mu=\alpha_0/(1-\alpha_1)$，$\sigma_Y^2=\sigma^2/(1-\alpha_1^2)$，高斯时 $\kappa=3\sigma_Y^4$。  

**缺陷：** 高斯过程的峰度由方差完全决定，$\kappa-3\sigma_Y^4=0$ **不是** 关于 $(\alpha_0,\alpha_1,\sigma^2)$ 的独立信息。  
三个“矩”实质只有两个自由（均值、方差）；$(\alpha_0,\alpha_1,\sigma^2)$ 三个参数 **不能** 仅由 $(\mu,\sigma_Y^2,\kappa)$ 识别。  
（$\alpha_1$ 与 $\sigma^2$ 在 $\sigma_Y^2$ 中缠结，需自协方差 $\gamma(1)$ 等。）

---

## Exercise 14.17

$Y_t=Y_{t-1}^\alpha u_t^{1-\alpha}$，$u_t>0$ i.i.d.

**(a)** 取对数：$y_t=\log Y_t$，$y_t=\alpha y_{t-1}+(1-\alpha)\log u_t$。  
$|\alpha|<1$ 时 $y_t$ 平稳遍历 ⇒ $Y_t=e^{y_t}$ 严格平稳遍历（在适当矩下）。  

**(b)** $y_t=(1-\alpha)\sum_{j=0}^\infty\alpha^j\log u_{t-j}$（$|\alpha|<1$），  
$Y_t=\exp(y_t)=\prod_{j=0}^\infty u_{t-j}^{(1-\alpha)\alpha^j}$。

---

## Exercise 14.18　FRED-QD：`pnfix` 季度增长率 AR(4)

**(a)** $g_t=100(pnfi_t/pnfi_{t-1}-1)$。  

**(b)(c)** $n\approx231$：

|  | 估计 | HC SE | NW($M=5$) SE |
|--|-----:|------:|-------------:|
| $g_{t-1}$ | 0.502 | 0.075 | 0.083 |
| $g_{t-2}$ | 0.168 | 0.070 | 0.069 |
| $g_{t-3}$ | −0.026 | 0.062 | 0.065 |
| $g_{t-4}$ | −0.068 | 0.052 | 0.051 |
| const | 0.491 | 0.146 | 0.141 |

**(d)** 一阶持续性强（~0.5），二阶仍正；3–4 阶弱。投资增长有惯性。  
NW 与 HC 接近（$M=5$ 时略增一阶 SE）。  

**(e)** IRF（对 $e_t=1$）：约 0.50, 0.42, 0.27, 0.12, 0.06, … 后衰减近 0。

---

## Exercise 14.19　`oilpricex` 一阶差分 AR(4)

**(a)** $\Delta oil_t$。  

**(b)** AR 系数约 $(0.27,-0.26,0.03,-0.07)$。  

**(c)** $H_0$：四 AR 系数 $=0$：Wald≈10.70，$\chi^2_4$，$p≈0.030$ **拒绝** 纯随机游走（在差分序列上 AR 系数联合显著）。  

**(d)** 差分后仍有短记忆相关；**不是** 简单 $\Delta oil_t=$ 白噪声。实际油价水平常近单位根，但差分动态非平凡。

---

## Exercise 14.20　FRED-MD：`unrate` AR 选阶（1960m1 起同一样本）

| $p$ | AIC（约） |
|----:|----------:|
| 1 | −3.445 |
| 2 | −3.456 |
| 3 | −3.527 |
| 4 | −3.558 |
| 5 | −3.585 |
| 6 | −3.591 |
| **7** | **−3.592**（最低） |
| 8 | −3.589 |

**(c)** **AR(7)** 最低 AIC。  
**(d)** 首项 $\hat\alpha_1≈0.98$（高持续），其余较小；失业率近单位根式持续。

---

## Exercise 14.21　失业率与 initial claims（FRED-QD）

**(a)** DL：$un_t$ 对 $claims_{t-1},\ldots,claims_{t-4}$。  
序列相关 + 可能异方差 ⇒ **HAC/Newey–West**（或至少 HC 不够时用 NW）更合适。  

**(b)** ADL(4,4)。  

**(c)** Granger：claims 四滞后联合 $=0$：Wald≈28.0，$p≈1.2\times10^{-5}$ **拒绝**。  

**(d)** 初请失业金对失业率有预测内容（Granger 因果），符合劳动力市场领先指标直觉。

---

## Exercise 14.22　GDP 增长与 housing starts

**(a)** $g_t=100(\mathrm{gdpc1}_t/\mathrm{gdpc1}_{t-1}-1)$。  

**(b)** DL 用 lags 1–4 of houst；同样宜 **HAC**。  

**(c)** ADL：GDP 增长 lag 1–2，houst lag 1–4。  

**(d)** Granger houst→$g$：Wald≈38.3，$p≈9.6\times10^{-8}$ **强烈拒绝** “无 Granger 因果”。  

**(e)** 住房开工领先 GDP 增长，与周期领先指标文献一致。

---

## 小结

| 题 | 要点 |
|:--:|------|
| 14.1–14.4 | 遍历、MDS、条件异方差 CLT |
| 14.5–14.14 | SV、MA/AR/ARMA 代数 |
| 14.15–14.17 | 高斯 AR、GMM 识别陷阱、非线性平稳 |
| 14.18–14.22 | FRED 实证：AR、AIC、Granger |
