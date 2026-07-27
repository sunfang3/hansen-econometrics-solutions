# Hansen《Econometrics》第 4 章习题解答

**章节：** Chapter 4 Least Squares Regression  
**书稿页码：** PDF 第 152–156 页（印刷页 132–136），§4.27 Exercises  
**记号：** $Y=X\beta+e$，$E[e\mid X]=0$，$\Omega=E[ee'\mid X]$，$\hat\beta=(X'X)^{-1}X'Y$

计算复现见：`Hansen_Ch04_Exercises_Solutions.ipynb`

---

## Exercise 4.1

$\mu_k=E[Y^k]$。

**(a)** $\hat\mu_k=n^{-1}\sum_{i=1}^n Y_i^k$。  
**(b)** $E[\hat\mu_k]=\mu_k$（i.i.d. 或同分布）。  
**(c)** $\mathrm{var}(\hat\mu_k)=n^{-1}\mathrm{var}(Y^k)$；需 $E|Y|^{2k}<\infty$。  
**(d)** $\widehat{\mathrm{var}}=n^{-1}s_k^2$，其中 $s_k^2=n^{-1}\sum(Y_i^k-\hat\mu_k)^2$（或 $n/(n-1)$ 无偏形式）。

---

## Exercise 4.2

$E[(Y-\mu)^3]=\mu_3$（三阶中心矩）。对称分布（关于 $\mu$）时为 0。

---

## Exercise 4.3

- $Y$：随机变量/观测；$\mu=E[Y]$：总体矩。  
- $n^{-1}\sum X_iX_i'$：样本二阶矩；$E[X_iX_i']$：总体二阶矩。前者是后者的估计。

---

## Exercise 4.4

**False。** 正规方程给出 $\sum X_i\hat e_i=0$，**不是** $\sum X_i^2\hat e_i=0$（除非 $X_i^2$ 也是回归元，或特殊情形）。

---

## Exercise 4.5　证明 (4.15)–(4.16)

$Y=X\beta+e$，$E[e\mid X]=0$，$E[ee'\mid X]=\Omega$。  
$\hat\beta=\beta+(X'X)^{-1}X'e$。  
$$E[\hat\beta\mid X]=\beta+(X'X)^{-1}X'E[e\mid X]=\beta. \tag{4.15}$$
$$\mathrm{var}(\hat\beta\mid X)=(X'X)^{-1}X'\Omega X(X'X)^{-1}. \tag{4.16}$$

---

## Exercise 4.6　Theorem 4.6（广义 Gauss–Markov）

设 $\tilde\beta=AY$ 线性且 $E[\tilde\beta\mid X]=\beta\Rightarrow AX=I_k$。  
$\mathrm{var}(\tilde\beta\mid X)=A\Omega A'$。  
令 $B=(X'\Omega^{-1}X)^{-1}X'\Omega^{-1}$（GLS 矩阵），$A=B+D$，$DX=0$。  
则 $A\Omega A'=B\Omega B'+D\Omega D'\ge B\Omega B'=(X'\Omega^{-1}X)^{-1}$。□

---

## Exercise 4.7　GLS 与 $\tilde c^2$

$\Omega=c^2\Sigma$，$\tilde\beta=(X'\Sigma^{-1}X)^{-1}X'\Sigma^{-1}Y$。

**(a)(b)** $E[\tilde\beta\mid X]=\beta$，$\mathrm{var}(\tilde\beta\mid X)=c^2(X'\Sigma^{-1}X)^{-1}$（即 (4.18)(4.19) 在 $\Omega=c^2\Sigma$ 时）。  

**(c)** $\tilde e=Y-X\tilde\beta=M_1e$，$M_1=I-X(X'\Sigma^{-1}X)^{-1}X'\Sigma^{-1}$。  

**(d)** 直接矩阵代数：$M_1'\Sigma^{-1}M_1=\Sigma^{-1}-\Sigma^{-1}X(X'\Sigma^{-1}X)^{-1}X'\Sigma^{-1}$。  

**(e)** $\tilde e'\Sigma^{-1}\tilde e=e'M_1'\Sigma^{-1}M_1e$。在 $e\mid X\sim(0,c^2\Sigma)$ 且正态或二阶矩下，  
$E[\tilde e'\Sigma^{-1}\tilde e\mid X]=c^2\,\mathrm{tr}(M_1)=c^2(n-k)$，故 $E[\tilde c^2\mid X]=c^2$。  

**(f)** 是：无偏（在标准条件下）且为 GLS 残差尺度的自然估计。

---

## Exercise 4.8　WLS $w_i=X_{ji}^{-2}$

**(a)** 当 $\mathrm{var}(e_i\mid X)\propto X_{ji}^2$ 时接近 GLS（如某些规模/异方差设定）。  
**(b)** 大 $|X_j|$ 观测噪声大时，WLS 降权可改进效率；误设权重时可能差于 OLS。

---

## Exercise 4.9　证明 (4.27)

同方差下 $E[\hat e_i^2\mid X]=\sigma^2(1-h_{ii})$。  
标准化 $e_i=(1-h_{ii})^{-1/2}\hat e_i$ 后 $E[e_i^2\mid X]=\sigma^2$，故  
$\bar\sigma^2=n^{-1}\sum e_i^2$ 满足 $E[\bar\sigma^2\mid X]=\sigma^2$。

---

## Exercise 4.10　证明 (4.35)

HC0/HC2/HC3 的 meat 为 $\sum X_iX_i'\hat e_i^2\cdot c_i$，其中 $c_i^{\mathrm{HC0}}=1$，$c_i^{\mathrm{HC2}}=(1-h_{ii})^{-1}$，$c_i^{\mathrm{HC3}}=(1-h_{ii})^{-2}$。  
因 $0\le h_{ii}<1$ 时 $1<(1-h_{ii})^{-1}<(1-h_{ii})^{-2}$，meat 按 Loewner 序增大（在通常满秩设计下），故  
$\hat V_{\mathrm{HC0}}<\hat V_{\mathrm{HC2}}<\hat V_{\mathrm{HC3}}$（差为正定，当存在 $h_{ii}>0$ 且 $\hat e_i\neq0$）。

---

## Exercise 4.11　证明 (4.36)

同方差下 $E[\hat e_i^2\mid X]=\sigma^2(1-h_{ii})$。HC2 用权重 $(1-h_{ii})^{-1}$：  
$E[\hat e_i^2/(1-h_{ii})\mid X]=\sigma^2$。从而  
$E[\sum X_iX_i'\hat e_i^2/(1-h_{ii})\mid X]=\sigma^2 X'X$，  
$E[\hat V_{\mathrm{HC2}}\mid X]=\sigma^2(X'X)^{-1}$。

---

## Exercise 4.12

i.i.d. 时 $E[(\bar Y-\mu)^3]=n^{-2}\mu_3$（因交叉项在独立下消失）。  
更一般：$E[(\bar Y-\mu)^3]=n^{-2}E[(Y_1-\mu)^3]$。

---

## Exercise 4.13

$\hat\beta-\beta=(\sum X_i^2)^{-1}\sum X_ie_i$。条件三阶矩在给定 $X$ 且独立误差下：  
$$E[(\hat\beta-\beta)^3\mid X]=\frac{\sum_i X_i^3\mu_{3i}}{(\sum_i X_i^2)^3}.$$

---

## Exercise 4.14　$\theta=\beta^2$

**(a)** $E[\hat\theta\mid X]=E[\hat\beta^2\mid X]=\beta^2+\mathrm{var}(\hat\beta\mid X)=\theta+V_{\hat\beta}$ ⇒ **有偏**（向上，若 $V>0$）。  
**(b)** $\hat\theta^*=\hat\beta^2-\hat V_{\hat\beta}$。  
**(c)** 需 $\hat V$ 对 $V$ 条件无偏；同方差下 HC2 或 $s^2/(\sum X_i^2)$ 合适。无偏性还要求更高矩/正态等使 $E[\hat\beta^2-\hat V]=\beta^2$。

---

## Exercise 4.15　$n^{-1}X'X=I_k$

**(a)** $\mathrm{var}(\hat\beta\mid X)=n^{-1}\Omega^*$ 型；无条件 $\mathrm{var}(\hat\beta)=n^{-1}E[XXee']$ 在 $n^{-1}X'X=I$ 时  
$V_{\hat\beta}=n^{-1}E[ee'XX']$ 的结构简化为 $n^{-1}E[e_i^2X_iX_i']$ 的平均。  
精确：$\hat\beta-\beta=n^{-1}X'e$ 当 $X'X=nI$，故 $\mathrm{var}(\hat\beta\mid X)=n^{-2}X'\Omega X$。  
**(b)** 一般 **相关**（若 $\Omega$ 非对角或回归元相关）。  
**(c)** 同方差 $\Omega=\sigma^2I$ 且设计正交时 $\mathrm{var}(\hat\beta\mid X)=(\sigma^2/n)I$ ⇒ 分量不相关。

---

## Exercise 4.16　$Y$ 的经典测量误差（因变量）

**(a)** $Y=X'\beta+(e+u)$，$E[e+u\mid X]=0$。CEF 仍线性，斜率仍为 $\beta$。  
**(b)** OLS 仍一致、无偏（给定条件）；**效率下降**（误差方差变大）。  
**(c)** 稳健 SE 仍有效（基于合成误差 $e+u$）；同方差公式中 $\sigma^2$ 变为 $\sigma_e^2+E[\sigma_u^2(X)]$。

---

## Exercise 4.17

**(a)** $u=Y-(\gamma+\theta X)^{1/2}$，$E[u\mid X]=0$ 由 CEF 定义。  
**(b)** $Y^2=(\gamma+\theta X)+2u(\gamma+\theta X)^{1/2}+u^2$，  
$E[Y^2\mid X]=\gamma+\theta X+E[u^2\mid X]$。  
故 (4.63) 中 $E[e\mid X]=E[u^2\mid X]\neq0$ 一般 ⇒ **截距/斜率混淆**。  
**(c)** 仅当 $E[u^2\mid X]$ 为常数时，$\beta=\theta$ 可识别，$\gamma$ 与该常数不可分；一般 **不能** 恢复 $(\gamma,\theta)$。  
**(d)** **不合理**（除非强加同方差于 $u$ 且只关心 $\theta$）。

---

## Exercise 4.18

长模型真，短回归残差 $\hat e=M_1(X_2\beta_2+e)$。  
同方差下 $E[s^2\mid X]=\sigma^2+\beta_2'Q\beta_2$ 型（正的 omitted variable 贡献）：  
$$E[s^2\mid X]=\sigma^2+\frac{\beta_2'X_2'M_1X_2\beta_2}{n-k_1}.$$
故 $s^2$ **高估** $\sigma^2$（除非 $\beta_2=0$ 或 $M_1X_2=0$）。

---

## Exercise 4.19

$X^*=XC$，$\hat\beta^*=C^{-1}\hat\beta$，$\widehat{\mathrm{Avar}}(\hat\beta^*)=C^{-1}\hat V C^{-1'}$。

---

## Exercise 4.20

$\hat\beta-\beta=(X'X)^{-1}X'e$，$\tilde\beta-\beta=(X'\Omega^{-1}X)^{-1}X'\Omega^{-1}e$。  
$$\mathrm{Cov}(\hat\beta,\tilde\beta\mid X)=(X'X)^{-1}X'E[ee'\mid X]\Omega^{-1}X(X'\Omega^{-1}X)^{-1}=(X'X)^{-1}.$$
（因 $E[ee'\mid X]=\Omega$。）  
$\hat\beta-\tilde\beta=Ae$ 适当 $A$，  
$$\mathrm{var}(\hat\beta-\tilde\beta\mid X)=\mathrm{var}(\hat\beta\mid X)-\mathrm{var}(\tilde\beta\mid X)$$
（因为 $\mathrm{Cov}(\hat\beta,\tilde\beta)=\mathrm{var}(\tilde\beta)$，GLS 投影性质）。

---

## Exercise 4.21

$R^2$ 用 **未加权 SSE**。GLS 最小化加权 SSE，不保证 $\tilde e'\tilde e\le\hat e'\hat e$。  
异方差下 **两者无必然大小关系**；$\hat R^2$ 与 $\tilde R^2$ 不可直接比较优劣。

---

## Exercise 4.22

**不同意。** i.i.d. $(Y_i,X_i)$ 允许 $E[e_i^2\mid X_i]=\sigma^2(X_i)$ 随 $X$ 变（边缘同分布但条件异方差）。  
i.i.d. ≠ 同方差。

---

## Exercise 4.23　Ridge

$\hat\beta_{\mathrm{ridge}}=(X'X+\lambda I)^{-1}X'Y$，  
$E[\hat\beta\mid X]=(X'X+\lambda I)^{-1}X'X\beta\neq\beta$（$\lambda>0,\beta\neq0$）⇒ **有偏**。

---

## Exercise 4.24（续 3.24）

样本：亚裔单身男性、experience$<45$，$n=267$。

|  | education | experience | exp2/100 | intercept |
|--|----------:|----------:|---------:|----------:|
| $\hat\beta$ | 0.1443 | 0.0426 | −0.0951 | 0.5309 |
| SE hom | 0.0116 | 0.0122 | 0.0349 | 0.1898 |
| HC0 | 0.0117 | 0.0124 | 0.0338 | 0.2001 |
| HC1 | 0.0118 | 0.0125 | 0.0341 | 0.2016 |
| HC2 | 0.0119 | 0.0126 | 0.0346 | 0.2027 |
| HC3 | 0.0121 | 0.0128 | 0.0354 | 0.2054 |

HC 族接近；HC3 略大。同方差 SE 与 HC 有可见差别。

---

## Exercise 4.25（续 3.26）

白人男性西班牙裔，$n=4230$，HC3 SE（节选）：  
education 0.0029，experience 0.0028，married 0.0250，South 0.0297 等（见 notebook 全表）。

---

## Exercise 4.26（DDK2011）

$Y=$ 标准化 `totalscore`；回归 tracking, age, girl, etpteacher, percentile。  
$n\approx5269$（完整协变量），学校聚类。

|  | $\hat\beta$ | robust SE | cluster SE | cluster/robust |
|--|------------:|----------:|-----------:|---------------:|
| tracking | 0.173 | 0.024 | **0.076** | **3.16** |
| age | −0.041 | 0.009 | 0.013 | 1.56 |
| girl | 0.081 | 0.024 | 0.028 | 1.18 |
| etpteacher | 0.180 | 0.024 | 0.037 | 1.57 |
| percentile | 0.017 | 0.0004 | 0.0007 | 1.69 |

**(a)** **tracking** 的 SE 聚类后膨胀最多；girl 相对最少。  
**(b)** 仅 tracking：$\hat\gamma\approx0.138$（书 (4.41)/(4.55)）；加控制后 $\approx0.173$（略升）。

---
