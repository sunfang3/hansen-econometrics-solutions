# Hansen《Econometrics》第 16 章习题完整解答

**章节：** Chapter 16 Non-Stationary Time Series  
**书稿：** PDF 第 615–616 页（印刷页 595–596），§16.23 Exercises（**16.1–16.14 全部**）

---

## Exercise 16.1　随机游走的矩与标准化

$S_t=S_{t-1}+e_t$，$S_0=0$，$e_t$ i.i.d. $(0,\sigma^2)$。

### (a)

由迭代 $S_t=\sum_{i=1}^t e_i$，

$$
\mathbb{E}[S_t]=0,\qquad
\operatorname{var}[S_t]=\sum_{i=1}^t \operatorname{var}(e_i)=t\sigma^2.
$$

### (b)

$$
Y_t=\frac{S_t-\mathbb{E}[S_t]}{\sqrt{\operatorname{var}[S_t]}}=\frac{S_t}{\sigma\sqrt{t}}.
$$

由构造 $\mathbb{E}[Y_t]=0$、$\operatorname{var}[Y_t]=1$，但 **$Y_t$ 不正平稳**：

$$
\operatorname{Cov}(Y_t,Y_{t+k})=\frac{\operatorname{Cov}(S_t,S_{t+k})}{\sigma^2\sqrt{t(t+k)}}=\frac{t\sigma^2}{\sigma^2\sqrt{t(t+k)}}=\sqrt{\frac{t}{t+k}},
$$

依赖 $t$，故联合分布不时移不变。

### (c)

对 $r\in[\delta,1]$，

$$
Y_{\lfloor nr\rfloor}
=\frac{S_{\lfloor nr\rfloor}}{\sigma\sqrt{\lfloor nr\rfloor}}
=\frac{n^{-1/2}S_{\lfloor nr\rfloor}}{\sigma\sqrt{\lfloor nr\rfloor/n}}.
$$

由 FCLT，$n^{-1/2}S_{\lfloor nr\rfloor}\to_d \sigma W(r)$，且 $\lfloor nr\rfloor/n\to r$，故

$$
Y_{\lfloor nr\rfloor}\to_d \frac{W(r)}{\sqrt{r}}\sim N(0,1)
\quad(r\ge\delta>0).
$$

（在 $\delta=0$ 附近 $\sqrt{r}$ 退化，故限制 $r\in[\delta,1]$。）

---

## Exercise 16.2　Beveridge–Nelson 分解

$\Delta Y_t=e_t+\Theta_1 e_{t-1}+\Theta_2 e_{t-2}=C(L)e_t$，其中 $C(L)=1+\Theta_1 L+\Theta_2 L^2$。

BN 恒等式：$C(L)=C(1)+(1-L)C^*(L)$，

$$
C(1)=1+\Theta_1+\Theta_2,
$$

$$
C^*(L)=-\big(\Theta_1+\Theta_2\big)-\Theta_2 L
$$

（一般地 $C^*_j=-\sum_{k=j+1}^\infty C_k$，$C_0=1,C_1=\Theta_1,C_2=\Theta_2$）。

因此

$$
\Delta Y_t=(1+\Theta_1+\Theta_2)\,e_t+(1-L)\tilde e_t,
\quad
\tilde e_t=C^*(L)e_t=-(\Theta_1+\Theta_2)e_t-\Theta_2 e_{t-1}.
$$

对水平求和（设初值合适）得

$$
Y_t=Y_0+C(1)\sum_{i=1}^t e_i+\tilde e_t-\tilde e_0
=C(1)\,S_t+\tilde e_t+\text{const},
$$

即 **永久成分** $C(1)S_t$ 与 **平稳暂时成分** $\tilde e_t$。

---

## Exercise 16.3　I(1) 加平稳噪声

$Y_t=X_t+u_t$，$X_t=X_{t-1}+e_t$，$(e_t,u_t)\sim I(0)$。

### (a)

$\Delta Y_t=e_t+\Delta u_t$。若 $e_t$ 的长期方差 $\omega_e^2>0$，则 $\Delta Y_t$ 的长期方差 $\omega_e^2>0$，故 $Y_t$ 为 **I(1)**（随机游走加 I(0) 噪声仍为 I(1)）。仅当 $e_t\equiv0$ 时退化为 I(0)。

### (b)

$n^{-1/2}Y_{\lfloor nr\rfloor}=n^{-1/2}X_{\lfloor nr\rfloor}+n^{-1/2}u_{\lfloor nr\rfloor}$。  
第二项 $o_p(1)$（$u$ 平稳），第一项 FCLT：

$$
n^{-1/2}Y_{\lfloor nr\rfloor}\to_d B(r)\sim\mathrm{BM}(\omega_e^2),
$$

其中 $\omega_e^2$ 为 $e_t$ 的长期方差。

---

## Exercise 16.4　过度差分

$Y_t=e_t$ i.i.d.，$X_t=\Delta Y_t=e_t-e_{t-1}$。

### (a)

$Y_t$ 为 i.i.d.，严格平稳且长期方差 $\operatorname{var}(e_t)=\sigma^2>0$，故 **平稳且 I(0)**。

### (b)

$X_t$ 为 MA(1)，严格平稳。但 $C(L)=1-L$，$C(1)=0$，谱密度在零频为 0，长期方差为 0。按 Hansen 定义（I(0) 要求正的长期方差 / 可逆 MA 且 $C(1)\ne0$），$X_t$ **平稳但不是 I(0)**（过度差分）。

---

## Exercise 16.5　协整向量

$U_t=U_{t-1}+e_t$，$Y_t=U_t+v_t$，$X_t=2U_t+w_t$，$(e_t,v_t,w_t)$ i.i.d.。

$$
Y_t-\tfrac12 X_t=v_t-\tfrac12 w_t\sim I(0),
$$

而 $Y_t,X_t$ 各自为 I(1)。故协整向量（可差常数倍）

$$
\beta=\begin{pmatrix}1\\ -1/2\end{pmatrix}
\quad\text{或}\quad
\begin{pmatrix}2\\ -1\end{pmatrix}.
$$

（$\beta' (Y_t,X_t)'$ 消去公共随机趋势 $U_t$。）

---

## Exercise 16.6　平稳 AR(1) 与单位根极限的调和

$|\alpha|<1$ 时 $\sqrt{n}(\hat\alpha-\alpha)\to_d N(0,1-\alpha^2)$（第 14 章）；$\alpha=1$ 时 $n(\hat\alpha-1)$ 为 Dickey–Fuller 型极限（Theorem 16.9）。

**调和：** 极限律在 $\alpha=1$ 处 **不连续**。当 $\alpha$ 固定且 $|\alpha|<1$ 时正态 $\sqrt{n}$ 极限成立，但当 $\alpha$ **接近 1** 时：

1. 渐近方差 $1-\alpha^2\to0$，正态近似在有限样本下很差；  
2. 更贴切的框架是 **local-to-unity** $\alpha_n=1-c/n$，极限为 Ornstein–Uhlenbeck 泛函，介于平稳正态与 DF 之间。

因此：$\alpha$ 远离 1 用第 14 章结果；$\alpha=1$ 用 Theorem 16.9；$\alpha\approx1$ 需局部单位根理论，不能把两种极限混用。

---

## Exercise 16.7　VECM(1) 中的 $\beta'Y_t$

$\Delta Y_t=\alpha\beta' Y_{t-1}+e_t$。令 $Z_t=\beta'Y_t$，则

\begin{align*}
Z_t
&=\beta'Y_{t-1}+\beta'\Delta Y_t
=\beta'Y_{t-1}+\beta'\alpha\,\beta'Y_{t-1}+\beta'e_t\\
&=(1+\beta'\alpha)\,Z_{t-1}+\beta'e_t.
\end{align*}

故 $Z_t$ 服从 **AR(1)**，自回归系数 $\rho=1+\beta'\alpha$。  
（协整时 $\beta'\alpha$ 的特征值在稳定域内，$\rho$ 的根模长 $<1$，$Z_t$ 平稳。）

---

## Exercise 16.8　$t$ 检验单位根？

$\hat\alpha=0.9$，$s(\hat\alpha)=0.05$，宣称 $t=(0.9-1)/0.05=-2$ 故拒绝 $\alpha=1$。

### 错误

在 $\mathrm{H}_0:\alpha=1$ 下，$t$ 统计量 **不是** 渐近 $N(0,1)$，而是 **Dickey–Fuller $T$ 分布**（Theorem 16.10–16.11）。  
临界值比正态更负（无截距约 $-1.95$，含截距约 $-2.86$，含趋势约 $-3.41$，5% 单侧）。用 $\pm1.96$ 或 $|t|>2$ 的常规规则 **无效**。  
此外点估计 $0.9$ 更支持平稳，正确做法是相对 DF 临界值报告 $p$ 值，而不是套用正态 $t$。

---

## Exercise 16.9　常规置信区间与单位根

$\hat\alpha=0.9$，$s=0.04$，常规 95% CI $[0.82,0.98]$ 不含 1，故称 $\alpha=1$ 与数据不符。

### 错误

常规 CI 基于 $\sqrt{n}$ 正态与对称分位数。在单位根 / 近单位根下：

- $\hat\alpha$ 的极限分布 **非正态、非对称**，收敛速率可为 $n$ 而非 $\sqrt{n}$；  
- 经典 SE 与 $z_{0.025}$ 构造的区间 **没有正确的渐近覆盖率**。

故“CI 不含 1 ⇒ 拒绝单位根”在逻辑与分布上都不成立。应使用 DF/ADF 检验或正确的单位根置信集（如 Stock 网格、局部单位根方法）。

---

## Exercise 16.10　去势后误用临界值

对 $Y_t$ 去势得 $Z_t$，ADF$=-2.5$，用 Stata 给出的 5% 临界值 $-1.9$ 宣称拒绝单位根。

### 错误

$-1.9$ 是 **无截距/无趋势**（Case 1）的 5% 临界值（Table 16.1）。  
对已 **线性去势** 的序列，应使用 **Case 3（截距+趋势）** 临界值：5% 约为 **$-3.4$**，1% 约 $-4.0$。  

$\mathrm{ADF}=-2.5>-3.4$，在正确临界值下 **不能** 在 5% 拒绝单位根。  
（去势后再做“无确定性项”的 DF，渐近分布仍是去势 BM 的 DF 律，必须用趋势情形临界值。）

---

## Exercise 16.11　“是单位根过程”？

对推文数序列，含截距 ADF$=-2.0$，宣称“推文数是单位根过程”。

### 错误（两层）

1. **假设检验逻辑：** 未拒绝 $\mathrm{H}_0$（单位根）**不等于** 接受“真实为单元根”。正确表述是：“不能拒绝单位根假设”。ADF$=-2.0$（Case 2）约在 30% 分位附近，$p$ 值很大，证据 **无力**。  
2. **建模：** 日推文更可能是带水平漂移、结构变化或厚尾的 **平稳/短记忆** 计数过程；单位根对有界兴趣/议题生命周期的序列往往不合理。应结合 KPSS、经济背景与水平图，而非“不拒绝 ⇒ 是单位根”。

---

## Exercise 16.12　FRED-MD 的 ADF 单位根检验

**设定：** 月度 FRED-MD；对带趋势的宏观水平/对数水平用 **截距+线性趋势（Case 3）**；对住房开工、初请等围绕水平波动的序列用 **仅截距（Case 2）**。  
AR 阶 $p$ 在 $1,\ldots,12$ 上按 **AIC** 选取（与正文 Table 16.2 一致）。  
临界值：Table 16.1；$p$ 值由相邻临界值线性插值。

| 序列 | 趋势 | $p$ | $\hat\rho-1$ | $s$ | ADF | 近似 $p$ 值 | 5% 结论 |
|------|:----:|:---:|-------------:|-----:|----:|:-----------:|:-------:|
| $\log(\mathrm{rpi})$ | ct | 9 | $-0.0075$ | 0.0036 | $-2.09$ | $\approx0.56$ | 不拒绝 |
| $\mathrm{indpro}$（水平） | ct | 12 | $-0.0109$ | 0.0036 | $-3.01$ | $\approx0.12$ | 不拒绝 |
| $\log(\mathrm{indpro})$ | ct | 12 | $-0.0055$ | 0.0028 | $-1.94$ | $\approx0.63$ | 不拒绝 |
| $\mathrm{houst}$ | c | 7 | $-0.0322$ | 0.0105 | $-3.08$ | $\approx0.03$ | **拒绝** |
| $\mathrm{hwi}$ | ct | 10 | $-0.0271$ | 0.0070 | $-3.88$ | $\approx0.01$ | **拒绝** |
| $\log(\mathrm{clf16ov})$ | ct | 12 | $+0.0016$ | 0.0018 | $+0.88$ | $>0.90$ | 不拒绝 |
| $\mathrm{claimsx}$ | c | 12 | $-0.0294$ | 0.0087 | $-3.38$ | $\approx0.01$ | **拒绝** |
| $\log(\mathrm{ipfuels})$ | ct | 7 | $-0.0213$ | 0.0085 | $-2.49$ | $\approx0.35$ | 不拒绝 |

**解读：** 劳动力、实际个人收入、工业生产（对数）等 **不能拒绝** 单位根，与 Nelson–Plosser 类宏观结论一致。住房开工、初请失业金、部分招聘指数在所选设定下 **拒绝** 单位根，更接近平稳（或趋势平稳）波动。  
（题干 (b) 写 `indpro` 未强制取对数；上表同时给出水平与对数，结论方向一致：均不在 5% 拒绝。）

---

## Exercise 16.13　KPSS 平稳性检验

**设定：** 与 16.12 相同的确定性项；滞后截断 $M=\lceil 3n^{1/3}\rceil$（正文建议，对应 Andrews 规则在 $\rho\approx0.8$ 的参照）。  
临界值：Table 16.3（右尾）；$p$ 值插值。

| 序列 | 趋势 | $M$ | KPSS | 近似 $p$ 值 | 5% 结论（$\mathrm{H}_0$ 平稳） |
|------|:----:|:---:|-----:|:-----------:|:---------------------------:|
| $\log(\mathrm{rpi})$ | ct | 27 | 0.43 | $<0.01$ | **拒绝平稳** |
| $\mathrm{indpro}$ | ct | 27 | 0.19 | $\approx0.02$ | **拒绝** |
| $\log(\mathrm{indpro})$ | ct | 27 | 0.34 | $<0.01$ | **拒绝** |
| $\mathrm{houst}$ | c | 27 | 0.44 | $\approx0.06$ | 临界（约 10% 拒绝） |
| $\mathrm{hwi}$ | ct | 27 | 0.17 | $\approx0.03$ | **拒绝** |
| $\log(\mathrm{clf16ov})$ | ct | 27 | 0.62 | $<0.01$ | **拒绝** |
| $\mathrm{claimsx}$ | c | 27 | 0.41 | $\approx0.07$ | 临界 |
| $\log(\mathrm{ipfuels})$ | ct | 27 | 0.31 | $<0.01$ | **拒绝** |

**与 ADF 对照：**

- 收入、劳动力、工业生产、燃料 IP：**ADF 不拒绝单位根 + KPSS 拒绝平稳** → 证据偏向 I(1)/强持续。  
- 住房开工、初请：**ADF 拒绝单位根，KPSS 仅 borderline** → 更支持平稳（或弱持续）。  
- `hwi`：ADF 拒绝单位根但 KPSS 也拒绝趋势平稳 → 可能结构变化/设定敏感，需稳健性检查。

---

## Exercise 16.14　Johansen 迹检验（无协整）

**数据：** FRED-MD 月度。  
**VAR 阶 $p$：** 水平 VAR 的 AIC（$p=1,\ldots,12$）。  
**趋势：** 利率对用 **Trend Model 2**（协整关系含截距，无线性趋势）；工业生产对数对用 **Trend Model 3**（无约束常数在差分方程中，协整不含趋势）并报告 Model 2 作对照。  
**迹统计量** $\mathrm{LR}(r)=-n\sum_{j=r+1}^{m}\log(1-\hat\lambda_j)$；临界值 Table 16.7。  
序贯：先 $\mathrm{H}_0:r=0$，拒绝后再看 $r=1$。

### (a) `tb3ms` 与 `gs10`（月度）

AIC 选 $p=10$，Trend Model 2，$n\approx698$。

| 原假设 | LR | $m-r$ | 5% 临界 | 1% 临界 | 结论 |
|--------|---:|:-----:|--------:|--------:|------|
| $r=0$ | 34.2 | 2 | 20.3 | 25.1 | **拒绝**（$p<0.01$） |
| $r=1$ | 2.5 | 1 | 9.2 | 12.7 | 不拒绝 |

→ 证据支持 **恰好一对协整**（利差平稳），与正文季度利率例子一致；此处为 **月度** 全样本。

### (b) `aaa` 与 `baa`

AIC 选 $p=7$，Trend Model 2，$n\approx701$。

| 原假设 | LR | $m-r$ | 5% | 1% | 结论 |
|--------|---:|:-----:|---:|---:|------|
| $r=0$ | 29.9 | 2 | 20.3 | 25.1 | **拒绝** |
| $r=1$ | 1.6 | 1 | 9.2 | 12.7 | 不拒绝 |

→ **信用利差型协整**：$r=1$ 合理（Aaa–Baa 利差近似平稳）。

### (c) $\log(\mathrm{ipdcongd})$ 与 $\log(\mathrm{ipncongd})$

AIC 选 $p=12$，$n\approx696$。

**Trend Model 3：**

| 原假设 | LR | $m-r$ | 5% | 1% | 结论 |
|--------|---:|:-----:|---:|---:|------|
| $r=0$ | 21.9 | 2 | 15.5 | 19.9 | **拒绝** |
| $r=1$ | 4.4 | 1 | 3.8 | 6.6 | 约在 5% **边缘拒绝** |

**Trend Model 2（对照）：** $\mathrm{LR}(0)=31.8$ 强拒绝；$ \mathrm{LR}(1)=4.9<9.2$ 不拒绝 $r=1$。

→ 耐用品/非耐用品工业生产对数：**拒绝无协整**；在 Model 2 下清晰支持 $r=1$。Model 3 下 $r=1$ 的迹统计量贴近 5% 临界，结论对趋势设定略敏感，实务上可报告两种并辅以经济利差/比率图。

---

## 小结

| 题 | 要点 |
|:--:|------|
| 16.1–16.5 | 随机游走矩、BN、I(0)/I(1)、过度差分、协整向量 |
| 16.6–16.7 | 极限不连续 / local-to-unity；VECM 中 $\beta'Y_t$ 为 AR(1) |
| 16.8–16.11 | 误用正态临界值、错误 CI、错误 Case 临界值、“不拒绝≠是单位根” |
| 16.12–16.14 | FRED-MD：ADF + KPSS + Johansen 迹检验完整实现 |

数值结果依赖 FRED-MD 样本终点；阶数与 $M$ 规则与 Hansen 正文一致，便于复现。
