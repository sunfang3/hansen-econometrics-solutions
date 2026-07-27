# Hansen《Econometrics》第 7 章习题解答

**章节：** Chapter 7 Asymptotic Theory for Least Squares  
**书稿页码：** PDF 第 209–215 页（印刷页 189–195），Exercises 7.x  

计算（7.28）见：`Hansen_Ch07_Exercises_Solutions.ipynb`

---


## Exercise 7.1

短回归 $Y$ 对 $X_1$：$\hat\beta_1^s\to_p(E[X_1X_1'])^{-1}E[X_1Y]$。  
一般 **不一致**。一致当 $E[X_1X_2']\beta_2=0$（如 $\beta_2=0$ 或 $X_1$ 与 $X_2$ 正交）。

---

## Exercise 7.2　Ridge，$\lambda$ 固定

$$\hat\beta=\Bigl(n^{-1}\sum XX'+n^{-1}\lambda I\Bigr)^{-1}n^{-1}\sum XY\to_p Q^{-1}E[XY]=\beta,$$
因 $n^{-1}\lambda\to0$。**一致**。

---

## Exercise 7.3　$\lambda=cn$

$$\hat\beta\to_p(Q+cI)^{-1}Q\beta\neq\beta\quad(c>0).$$
**不一致**。

---

## Exercise 7.4　Section 7.4 矩核对

$P(X_1=X_2=\pm1)=3/8$，$P(X_1=-X_2)=1/8$ 各组；条件二阶矩 $5/4$（同号）与 $1/4$（异号）。

|  | 结果 |
|--|------|
| (a) $E[X_1]$ | $0$ |
| (b) $E[X_1^2]$ | $1$ |
| (c) $E[X_1X_2]$ | $1/2$ |
| (d) $E[e^2]$ | $1$ |
| (e) $E[X_1^2e^2]$ | $1$ |
| (f) $E[X_1X_2e^2]$ | $7/8$ |

(f) 计算：$(5/4)(3/4)+(1/4)(-1/4)=15/16-1/16=7/8$。

---

## Exercise 7.5

证明 (7.13)–(7.16)：标准 WLLN/CLT 下样本矩收敛与 $\hat Q_{XX}\to_p Q$、$n^{-1/2}X'e\to_d N(0,\Omega)$ 等（见教材推导；核心是 i.i.d. 有限二阶矩 + Cramér–Wold）。

---

## Exercise 7.6

矩条件 $E[X(Y-X'\beta)]=0$，$E[XX'e^2]=\Omega$。  
$$\hat\beta=(X'X)^{-1}X'Y,\qquad \hat\Omega=n^{-1}\sum X_iX_i'\hat e_i^2.$$

---

## Exercise 7.7　$Y$ 测量误差

$Y=X'\beta+e+u$，$E[X(e+u)]=0$。  
**(a)** 是：$\beta$ 仍是 $Y$ 对 $X$ 的投影系数。  
**(b)** OLS 一致。  
**(c)** $\sqrt{n}(\hat\beta-\beta)\to_d N(0,Q^{-1}\Omega Q^{-1})$，$\Omega=E[XX'(e+u)^2]$。

---

## Exercise 7.8

$\hat\sigma^2=n^{-1}\sum\hat e_i^2$。在同方差/适当矩下  
$\sqrt{n}(\hat\sigma^2-\sigma^2)\to_d N(0,\mathrm{var}(e^2))$（需展开 $\hat e_i=e_i-X_i'(\hat\beta-\beta)$ 的影响项，通常不改变一阶渐近方差若 $E[eX]=0$）。

---

## Exercise 7.9

$\hat\beta=\sum X_iY_i/\sum X_i^2$（OLS），$\tilde\beta=n^{-1}\sum Y_i/X_i$。  
**(a)** OLS 在 $E[Xe]=0$ 下一致；$\tilde\beta$ 一般要求 $E[e/X]=0$ 等更强/不同条件，**不自动一致**。  
**(b)** 同方差下 OLS 在 Gauss–Markov/渐近有效意义下更优；$\mathrm{var}(e\mid X)\propto X^2$ 时 $\tilde\beta$ 类估计可能更有效。

---

## Exercise 7.10　预测

**(a)** $\widehat Y_{n+1}=x'\hat\beta$。  
**(b)** $\widehat{\mathrm{var}}\approx x'\hat V_{\hat\beta}x+\hat\sigma^2$（参数不确定性 + 创新方差）。

---

## Exercise 7.11

**(a)** $\tilde\Omega$ 用真误差：标准 CLT，$\sqrt{n}(\tilde\Omega-\Omega)\to_d N(0,\mathrm{Avar})$。  
**(b)** $\hat e_i=e_i-X_i'(\hat\beta-\beta)$；差值 $o_p(n^{-1/2})$ 阶使 $\hat\Omega$ 与 $\tilde\Omega$ **同分布极限**。  
**(c)** $E[e\mid X]=0$ 保证 $\hat\beta$ 一致并控制交叉项。

---

## Exercise 7.12　$A=-\alpha^2/(2\beta)$

**(a)** $\hat A=-\hat\alpha^2/(2\hat\beta)$。  
**(b)** delta 法：$\sqrt{n}(\hat A-A)\to_d N(0,G'V_\theta G)$，$G=\partial A/\partial(\alpha,\beta)$；  
CI：$\hat A\pm z_{1-\eta/2}\mathrm{se}(\hat A)$。

---

## Exercise 7.13　反向回归 $\theta=1/\gamma$

**(a)** $\hat\gamma=\sum Y_iX_i/\sum Y_i^2$。  
**(b)** $\hat\theta=1/\hat\gamma$。  
**(c)(d)** delta 法 $\mathrm{se}(\hat\theta)=|\hat\theta|^2\mathrm{se}(\hat\gamma)$。

---

## Exercise 7.14　$\theta=\beta_1\beta_2$

**(a)** $\hat\theta=\hat\beta_1\hat\beta_2$。  
**(b)** $\sqrt{n}(\hat\theta-\theta)\to_d N(0,g'Vg)$，$g=(\beta_2,\beta_1,\ldots)$。  
**(c)** $\hat\theta\pm1.96\,\widehat{\mathrm{se}}$。

---

## Exercise 7.15

$\hat\beta=\sum X_i^3Y_i/\sum X_i^4$。  
由 $Y=X\beta+e$：$\hat\beta-\beta=\sum X_i^3e_i/\sum X_i^4$。  
$\sqrt{n}(\hat\beta-\beta)\to_d N\bigl(0,\,E[X^6e^2]/(E[X^4])^2\bigr)$（需矩条件）。

---

## Exercise 7.16

随机一半子样本仍 i.i.d. 来自同一总体 ⇒ OLS **仍一致**（效率损失）。

---

## Exercise 7.17

**(a)** $\widehat{\mathrm{se}}(\hat\theta)=\sqrt{s_1^2+s_2^2-2\hat\rho s_1 s_2}$，CI $\hat\beta_1-\hat\beta_2\pm1.96\,\widehat{\mathrm{se}}$。  
**(b)** **不能**仅从两个 SE 得 $\hat\rho$。  
**(c)** 作者结论 **不成立**：差 $0.2$，即便 $\rho=1$ 时 $\mathrm{se}(\mathrm{diff})$ 可为 0，但 $\rho$ 未知；$\rho=0$ 时 $z=0.2/\sqrt{2\cdot0.07^2}\approx2.02$，边界显著，但无 $\rho$ 不能断言。

---

## Exercise 7.18

**(a)** $\hat m(x)=\hat\beta_0+\hat\beta_1x+\hat\beta_2x^2$。  
**(b)** $\hat m\pm z\sqrt{x(x)'\hat V\hat x(x)}$，$x(x)=(1,x,x^2)'$。

---

## Exercise 7.19

独立折半样本 $\hat\beta_1,\hat\beta_2$ 渐近独立同分布 $N(\beta,V/n)$ 量级：  
$\sqrt{n}(\hat\beta_1-\hat\beta_2)\to_d N(0,2V)$。

---

## Exercise 7.20　加权准则

**(a)** $\hat\beta=(\sum W_iX_iX_i')^{-1}(\sum W_iX_iY_i)$。  
**(b)** 加权投影：$E[WXX']^{-1}E[WXY]$（需 $E[WXX']$ 可逆）。  
**(c)** $\hat\beta\to_p\beta_W$ 上述。  
**(d)** 若 $E[WeX]=0$ 且 $\beta_W=\beta$，则 $\sqrt{n}(\hat\beta-\beta)\to_d N(0,G^{-1}\Omega_W G^{-1})$。

---

## Exercise 7.21

估计 $\hat\beta$ 与 $\hat\gamma$（如对 $\hat e^2$ 回归 $Z$）；点预测 $x'\hat\beta$；  
区间用 $\widehat{\mathrm{var}}=x'\hat Vx+z'\hat\gamma$（或更稳健）。

---

## Exercise 7.22

**(a)** $\hat\beta\to_p\beta$，$X'\hat\beta\to_p X'\beta$，第二步回归一致得 $\gamma$。  
**(b)** $\gamma=0$ 时第二步回归元 $X'\hat\beta=O_p(n^{-1/2})$，需非标准/退化 debias 分析；$\hat\gamma$ 有非标准极限（生成回归元）。

---

## Exercise 7.23

$\tilde\beta=n^{-1}\sum Y_i/X_i$。$Y=X\beta+e\Rightarrow\tilde\beta=\beta+n^{-1}\sum e_i/X_i$。  
一致需 $E[e/X]=0$ 且 $E|e/X|<\infty$（比 $E[e\mid X]=0$ 更强的可积性）。

---

## Exercise 7.24　回归元乘性测量误差

$X=X^*v$。OLS 回归 $Y$ on $X$ 得 $\mathrm{plim}=E[XY]/E[X^2]$ 一般 $\neq\beta$。  
**(b)** 例如 $v$ 与 $X^*$ 特殊相关使 $E[X^*v e]$ 等抵消；或 $v$ 常数。非平凡条件少见。

---

## Exercise 7.25

$\tilde\beta\to_p E[w(X)XX']^{-1}E[w(X)XY]$。  
若 $E[e\mid X]=0$ 则 $=\beta$（**一致**）。仅 $E[Xe]=0$ 时一般 **不一致**，除非 $w$ 常数。

---

## Exercise 7.26　权重 $e_i^{-2}$

**(a)** 类 WLS：$\sqrt{n}(\tilde\beta-\beta)\to_d N(0,E[e^{-2}XX']^{-1})$ 形式（在权重外生/可积条件下）。  
**(b)** 不可行 GLS 用 $\sigma^{-2}(X)$；此处用 $e^{-2}$ 过度/随机，极限一般 **不同于** GLS（除非 $|e|=\sigma(X)$ a.s.）。

---

## Exercise 7.27　截断 $|X|\le c$

**(a)** 等价于加权 $w=1\{|X|\le c\}$，在 $E[e\mid X]=0$ 下 $\tilde\beta\to_p\beta$。  
**(b)** $\sqrt{n}(\tilde\beta-\beta)\to_d N(0,Q_c^{-1}\Omega_c Q_c^{-1})$，$Q_c=E[XX'1\{|X|\le c\}]$ 等。

---

## Exercise 7.28（CPS 实证）

白人男性西班牙裔；$\log(\mathrm{wage})=\beta_1\mathrm{edu}+\beta_2\mathrm{exp}+\beta_3\mathrm{exp}^2/100+\beta_4$。

|  | 估计 | HC3 SE |
|--|-----:|-------:|
| education | 0.0904 | (见 nb) |
| experience | 0.0354 | |
| exp2/100 | −0.0465 | |
| intercept | 1.185 | |

**(b)** $\theta=\dfrac{\beta_1}{\beta_2+2\beta_3\cdot 10/100}=\dfrac{\beta_1}{\beta_2+0.2\beta_3}$，$\hat\theta\approx3.47$。  
**(c)(d)** delta 法 SE$\approx0.227$，90% CI $\approx[3.09,3.84]$。  
**(e)** $m(12,20)\approx2.792$，95% CI$\approx[2.769,2.815]$。  
**(f)** 预测 edu=16,exp=5：$\widehat{\log w}\approx2.80$；80% 对数区间约 $[2.06,3.53]$；工资 $[7.9,34.3]$。

---
