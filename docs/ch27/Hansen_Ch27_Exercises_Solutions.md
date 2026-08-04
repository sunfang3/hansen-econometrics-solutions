# Hansen《Econometrics》第 27 章习题完整解答

**章节：** Chapter 27 Censoring and Selection  
**出版版：** `hansen/manuscripts/Econometrics_Fullbook.pdf`，PDF 第 921–923 页（印刷页 886–888），§27.13 Exercises（**27.1–27.11 全部**）

**阅读提示（`AGENTS.md`）：** 默认读者熟悉 OLS 与截断/删失的口头说法，但不默认掌握 Tobit 似然、Mills 比、CLAD、Heckman 两步法。下文逐步补齐。

**本科搭桥：**
- **删失（censoring）**：$Y^*$ 生成后被“顶住”边界（如 $Y=\max(Y^*,0)$），**边界点仍在样本中**。  
- **截断（truncation）**：边界外的观测被**整行丢掉**，只剩 $Y^*>0$ 的子样本。  
- **选择（selection）**：$Y$ 是否被观测由另一过程 $S$ 决定（就业→工资）；与删失不同，非选中时 $Y$ 为 missing，且 $S$ 可依赖另一套 $Z$。  
- OLS 在删失/截断/内生选择下一般 **不一致**；Tobit 靠正态+独立，CLAD 靠中位数等变，Heckman 靠联合正态与（最好有）排除约束。

---

## Exercise 27.1　推导 (27.2) 与 (27.3)

### 设定

$Y^*=X'\beta+e$，$e\mid X\sim N(0,\sigma^2)$，$Y=\max(Y^*,0)$。记 $\mu=X'\beta$，$z=\mu/\sigma$，$\lambda(z)=\phi(z)/\Phi(z)$（逆 Mills 比）。  
截断变量 $Y^\#$ 为在 $Y^*>0$ 条件下的 $Y^*$。

### 预备（截断正态矩）

对 $W\sim N(\mu,\sigma^2)$，左截断在 0（即条件 $W>0$）：

$$
\mathbb{E}[W\mid W>0]=\mu+\sigma\lambda(z),\qquad
\mathbb{P}(W>0)=\Phi(z).
$$

（对应 Introduction to Econometrics 中截断正态定理；也可由密度 $\phi((w-\mu)/\sigma)/(\sigma\Phi(z))$ 直接积分。）

### (27.3) 截断条件均值

$Y^\#\stackrel{d}{=}(Y^*\mid Y^*>0)$，故
$$
m^\#(X)=\mathbb{E}[Y^\#\mid X]=\mu+\sigma\lambda(z)
=X'\beta+\sigma\lambda\!\left(\frac{X'\beta}{\sigma}\right).
\tag{27.3}
$$

### (27.2) 删失条件均值

$$
\begin{aligned}
m(X)=\mathbb{E}[Y\mid X]
&=\mathbb{E}[Y^*\mathbf{1}\{Y^*>0\}\mid X]
=\mathbb{P}(Y^*>0\mid X)\,\mathbb{E}[Y^*\mid Y^*>0,X]\\
&=\Phi(z)\bigl(\mu+\sigma\lambda(z)\bigr)
=\mu\Phi(z)+\sigma\phi(z),
\end{aligned}
$$
其中用了 $\Phi(z)\lambda(z)=\phi(z)$。即
$$
m(X)=X'\beta\,\Phi\!\left(\frac{X'\beta}{\sigma}\right)+\sigma\phi\!\left(\frac{X'\beta}{\sigma}\right).
\tag{27.2}
$$

### 排序

因 $Y^*\le Y\le Y^\#$（在“删失点填 0、截断丢掉负值”的常规构造下），有 $m^*\le m\le m^\#$，删失/截断均值都偏向 latent 均值的一侧。

---

## Exercise 27.2　上顶（capped from above）与 OLS

$$
Y=\begin{cases}Y^*&Y^*\le\tau,\\ \text{missing}&Y^*>\tau,\end{cases}
\quad Y^*=X'\beta+e,\ e\sim N(0,\sigma^2).
$$

题述“regress $Y$ on $X$”应理解为：**观测到的是上删失** $Y^c=\min(Y^*,\tau)$（或丢掉 $Y^*>\tau$ 的截断样本）。两种情形 OLS 都 **不一致**。

### 上删失 $Y^c=\min(Y^*,\tau)$

$$
\mathbb{E}[Y^c\mid X]=\mu\bigl(1-\Phi(z_\tau)\bigr)+\tau\Phi(-z_\tau')+\cdots
$$
（$z_\tau=(\tau-\mu)/\sigma$）**不是** $\mu=X'\beta$。高 $Y^*$ 被压到 $\tau$，若 $X'\beta$ 与越过 $\tau$ 的概率正相关，斜率通常被 **压扁（attenuation）**。

### 若丢掉 $Y^*>\tau$

变成上截断，条件均值是截断正态，同样 $\ne X'\beta$。

**误测方向：** 大的 latent 结果被压低或剔除 → 拟合线在 $X$ 使 $\mu$ 较大处被拉向 $\tau$，斜率绝对值常偏小。

---

## Exercise 27.3　按 $X$ 与按 $Y$ 的选样

模型 $Y=X'\beta+e$，$e\sim N(0,\sigma^2)$（与 $X$ 独立），$\hat\beta$ 为可用样本上的 OLS。

### (a) 仅当 $X_1>0$ 时入样

这是 **外生选样**（只依赖回归元）。  
$\mathbb{E}[e\mid X,X_1>0]=\mathbb{E}[e\mid X]=0$，故
$$
\mathbb{E}[Y\mid X,X_1>0]=X'\beta.
$$
在选样子总体上 CEF 仍正确，OLS 对 **该子总体** 的 $\beta$ **一致**（若 $\mathbb{E}[XX'\mid X_1>0]$ 满秩）。  
$\mathrm{plim}\,\hat\beta=\beta$（子总体参数与全总体相同，因条件均值线性且误差均值独立于 $X$）。

### (b) 仅当 $Y>0$ 时入样

**内生截断**。条件均值
$$
\mathbb{E}[Y\mid X,Y>0]=X'\beta+\sigma\lambda\!\left(\frac{X'\beta}{\sigma}\right)\ne X'\beta.
$$
OLS 一致到 **截断回归的 BLP**，一般 $\mathrm{plim}\,\hat\beta\ne\beta$。在正态回归元等特殊情形可有类似 Greene 的比例萎缩；一般只有上式中的非线性 CEF。

---

## Exercise 27.4　删失均值的 NLLS

由 (27.2)，正确设定下
$$
\mathbb{E}[Y\mid X]=m(X;\beta,\sigma)
=X'\beta\,\Phi\!\left(\frac{X'\beta}{\sigma}\right)+\sigma\phi\!\left(\frac{X'\beta}{\sigma}\right).
$$
**NLLS：**
$$
(\hat\beta,\hat\sigma)=\arg\min_{\beta,\sigma>0}\sum_{i=1}^n\bigl(Y_i-m(X_i;\beta,\sigma)\bigr)^2.
$$
数值优化即可（可参数化 $\sigma=e^\nu$）。在正确设定下对 $(\beta,\sigma)$ 一致，但一般 **不及 Tobit MLE 有效**；若正态/独立不成立，二者都可能偏误，CLAD 更稳健。

---

## Exercise 27.5　截断均值的 NLLS

由 (27.3)，在 $Y^\#>0$ 的截断样本上
$$
\mathbb{E}[Y^\#\mid X]=X'\beta+\sigma\lambda\!\left(\frac{X'\beta}{\sigma}\right).
$$
**NLLS：**
$$
(\hat\beta,\hat\sigma)=\arg\min\sum_{i:Y_i>0}\Bigl(Y_i-X_i'\beta-\sigma\lambda(X_i'\beta/\sigma)\Bigr)^2.
$$
同样可用；截断正态 MLE 更常用且在正确设定下更有效。

---

## Exercise 27.6　异方差 Tobit 的对数似然

$Y^*=\beta_0+X\beta_1+e$，$e\mid X\sim N(0,\sigma^2(X))$，$\sigma^2(X)=\gamma_0+X^2\gamma_1$，$Y=\max(Y^*,0)$，$\gamma_0,\gamma_1>0$。

给定 $X=x$，令 $\mu(x)=\beta_0+x\beta_1$，$\sigma(x)=\sqrt{\gamma_0+x^2\gamma_1}$。

- 若 $Y=0$：贡献 $\log\Phi\!\bigl(-\mu(x)/\sigma(x)\bigr)$；  
- 若 $Y=y>0$：贡献 $\log\phi\!\bigl((y-\mu(x))/\sigma(x)\bigr)-\log\sigma(x)$。

故
$$
\ell_n(\beta,\gamma)
=\sum_{Y_i=0}\log\Phi\!\left(-\frac{\mu_i}{\sigma_i}\right)
+\sum_{Y_i>0}\left[-\log\sigma_i-\tfrac12\log(2\pi)-\frac{(Y_i-\mu_i)^2}{2\sigma_i^2}\right],
$$
其中 $\mu_i=\beta_0+X_i\beta_1$，$\sigma_i=\sqrt{\gamma_0+X_i^2\gamma_1}$。

---

## Exercise 27.7　选择下的条件均值

$$
S=\mathbf{1}\{X'\gamma+u>0\},\quad
Y=\begin{cases}X'\beta+e&S=1,\\ \text{missing}&S=0,\end{cases}
\quad
\begin{pmatrix}e\\u\end{pmatrix}\sim N\!\left(0,\begin{pmatrix}\sigma^2&\sigma_{21}\\\sigma_{21}&1\end{pmatrix}\right).
$$

### 推导

$$
\mathbb{E}[Y\mid X,S=1]=X'\beta+\mathbb{E}[e\mid u>-X'\gamma].
$$
联合正态：$e=\sigma_{21}u+\varepsilon$，$\varepsilon\perp u$。故
$$
\mathbb{E}[e\mid u>-X'\gamma]=\sigma_{21}\,\mathbb{E}[u\mid u>-X'\gamma].
$$
标准正态左截断：$\mathbb{E}[u\mid u>-c]=\lambda(c)=\phi(c)/\Phi(c)$（$c=X'\gamma$）。因此
$$
\mathbb{E}[Y\mid X,S=1]=X'\beta+\sigma_{21}\lambda(X'\gamma).
$$

---

## Exercise 27.8　证明 (27.7)

Heckman 模型中选择指数为 $Z'\gamma$（可含与 $X$ 不同的变量），与 27.7 相同计算：
$$
\mathbb{E}[Y\mid X,Z,S=1]=X'\beta+\sigma_{21}\lambda(Z'\gamma).
\tag{27.7}
$$
（$u\sim N(0,1)$，$e$ 与 $u$ 相关 $\sigma_{21}$。）这是 Heckman 两步法第二步回归 $Y$ 于 $(X,\hat\lambda)$ 的总体目标。

---

## Exercise 27.9　CHJ2004：实物转移 `tinkind`

### 设定

- `tinkind`、`income` 均除以 1000；  
- `Dincome=(income-1)\times 1\{income>1\}`（在标准化后收入 $=1$ 处的线性样条结点）；  
- $n=8684$。

### 结果（HC1 SE）

| 方法 | 截距 | income | Dincome | 备注 |
|------|-----:|-------:|--------:|------|
| (a) OLS 全样本 | 2.70 | −1.53 | 1.55 | |
| (c) OLS 仅 tinkind>0 | 3.56 | −2.14 | 2.16 | $n=6481$ |
| (d) Tobit（下删失 0） | 2.04 | −1.87 | 1.88 | $\hat\sigma\approx 5.99$ |
| (e) CLAD | 1.17 | −0.77 | 0.77 | 中位数口径 |

(b) **删失比例** $\mathbb{P}(\texttt{tinkind}=0)\approx\mathbf{25.4\%}$。按 Greene 经验法则，斜率可萎缩约 $1-\pi\approx 75\%$ 量级——**删失偏误值得处理**。

### 解释

- 低段：income 斜率约 **−1.5**（收入高 → 收到的实物转移少）；  
- 高段：income+Dincome $\approx 0$，**近乎平坦**——与教材“低收入陡、高收入平”的转移模式一致。  
- 丢掉 0 值（截断）把斜率绝对值 **放大**，偏误方向与删失不同。  
- Tobit 在正态假设下校正水平/斜率；CLAD 水平更低（右偏因变量：均值≫中位数），斜率形状仍呈“先降后平”。  
- **优选：** 若关心条件中位数且怀疑非正态 → CLAD；若坚持正态 latent → Tobit；两者都优于盲目 OLS。

---

## Exercise 27.10　CPS：工资上顶（cap at \$30/h）

### 设定

- `education`≥12；$wage=\mathrm{earnings}/(\mathrm{hours}\times\mathrm{week})$，$lwage=\log(wage)$；  
- $n=46943$；约 **23.5%** 的 $lwage\ge 3.4$（即工资约 ≥\$30/h）。  
- `cwage=\min(lwage,3.4)`。

### 结果

| 方法 | 截距 | educ | educ² |
|------|-----:|-----:|------:|
| (a) OLS 真 $lwage$ | 1.30 | 0.118 | ≈0 |
| (b) OLS on $cwage$ | 0.57 | 0.239 | −0.0053 |
| (c) 丢掉顶上观测 | 0.84 | 0.211 | −0.0052 |
| (d) Tobit 上删失 3.4 | 0.99 | 0.162 | −0.0015 |
| (e) CLAD 上删失 3.3 | **1.36** | **0.116** | ≈0 |

### 解释

- 不知封顶时，(b) 会把教育回报的 **曲率/斜率读错**（线性项被抬高、二次项变负），截距被压低——典型 **上删失衰减/扭曲**。  
- (c) 删掉高工资观测 **不能** 恢复真 CEF（截断偏误）。  
- **Tobit** 把 educ 从 0.24 拉回 0.16，朝 (a) 的 0.12 **部分校正**，但不会等于 (a)：真实 $lwage$ 并非“正态 latent + 上删失”的 Tobit DGP，MLE 拟合的是最佳 Tobit 近似。  
- **CLAD**（习题提示顶可取 **3.3**）对中位数更稳健，educ 斜率约 0.116，**非常接近** 真 OLS。顶恰好取 3.4 时数值优化更易陷入局部解。  
- 教训：封顶数据不要只做 OLS；Tobit/CLAD 都优于盲目 OLS，非正态时 CLAD 往往更贴近关注的 latent 斜率。

---

## Exercise 27.11　DDK2011：测验分下删失

### 设定

- `testscore` = 标准化 `totalscore`（均值 0、方差 1）；  
- 回归：tracking、percentile、percentile²；**按 school 聚类** SE；  
- $n=5304$；约 **57%** 的 testscore $<0$（下删失于 0 后大量堆在边界）。

### 结果（cluster by school）

| 方法 | tracking | percentile | percentile² |
|------|--------:|-----------:|------------:|
| (a) OLS 真分数 | **0.162** | 0.0104 | ≈0.0001 |
| (b) OLS on $ctest=\max(ts,0)$ | **0.089** | −0.0020 | 0.0001 |
| (c) 仅 $ctest>0$ | **0.075** | −0.0061 | 0.0001 |

### 解释

- 真模型中 tracking 约 **+0.16** 标准差（与跟踪教学文献同向）。  
- 人为下删失后，OLS 把 tracking 效应 **几乎减半**，percentile 剖面也被扭曲（甚至变号）。  
- 丢掉删失点（截断）进一步偏离，**不能**“修掉”删失。  
- 与 27.9–27.10 同一课：堆在边界的 OLS 读的是删失 CEF，不是 latent 政策效应；高删失率（57%）时偏误很大。

---

## 小结

| 题 | 要点 |
|:--:|------|
| 27.1–27.5 | 删失/截断均值；NLLS；按 $X$ 外生选样 vs 按 $Y$ 截断 |
| 27.6–27.8 | 异方差 Tobit 似然；Heckman Mills 项 (27.7) |
| 27.9–27.11 | CHJ/CPS/DDK：OLS 偏、截断更糟；Tobit/CLAD 校正 |

代码：`docs/ch27/Hansen_Ch27_Exercises_Solutions.ipynb`。
