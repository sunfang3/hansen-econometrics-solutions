# Hansen《Econometrics》第 25 章习题完整解答

**章节：** Chapter 25 Binary Choice  
**出版版：** `hansen/manuscripts/Econometrics_Fullbook.pdf`，PDF 第 880–881 页（印刷页 845–846），§25.15 Exercises（**25.1–25.19 全部**）

**阅读提示（`AGENTS.md`）：** 默认读者熟悉 LPM / logit 入门，但不默认掌握潜变量尺度、Mills 比、Hessian 全局凹、异方差二元选择识别。下文逐步补齐。

**本科搭桥：**  
- LPM：$\mathbb{E}[Y\mid X]=X'\beta$，可 OLS，但拟合概率可能越出 $[0,1]$；  
- Probit/Logit：$P(Y=1\mid X)=G(X'\beta)$，$G=\Phi$ 或 $\Lambda$，用 **MLE**；  
- 系数 $\beta$ 的尺度与误差方差绑在一起，**比系数更宜报边际效应 AME**。

---

## Exercise 25.1　翻转 $Y$ 的 probit 斜率

### 题意

Emily：$Y=1$ 表示购买。Jacob：$Y^*=1-Y$（$Y^*=1$ 表示不买）。同一 $X$，都估 probit。

### 推导

Emily：$\mathbb{P}(Y=1\mid X)=\Phi(X'\beta_E)$。  
Jacob：$\mathbb{P}(Y^*=1\mid X)=\mathbb{P}(Y=0\mid X)=1-\Phi(X'\beta_E)=\Phi(-X'\beta_E)$  
（正态对称：$\Phi(-u)=1-\Phi(u)$）。  
故 Jacob 的模型是 $\Phi(X'\beta_J)$ 且 $\beta_J=-\beta_E$。

### 结论

**斜率（及全部系数）恰好反号：** $\hat\beta_J=-\hat\beta_E$。  
截距同样反号。拟合的“购买概率”与“不买概率”互补，经济含义一致。

---

## Exercise 25.2　回归元单位从“元”改为“千元”

Julie 的回归元 $X_J=X_E/1000$（美元 → 千美元）。

Logit：$P=\Lambda(X'\beta)$。指数里 $X_E\beta_E=X_J\beta_J$，故
$$
\beta_J=1000\,\beta_E
$$
（对该回归元的斜率系数；其他未改单位的变量不变）。

**直觉：** 变量缩小 1000 倍，系数放大 1000 倍，使 **指数 $X'\beta$ 不变**，概率与边际效应（对原美元单位）不变。

---

## Exercise 25.3　证明 (25.1) 与 (25.2)

$Y=P(X)+e$，$\mathbb{E}[e\mid X]=0$，$P(X)=\mathbb{P}(Y=1\mid X)$。

### (25.1) 误差两点分布

给定 $X$：

- 以概率 $P(X)$，$Y=1$，则 $e=1-P(X)$；  
- 以概率 $1-P(X)$，$Y=0$，则 $e=0-P(X)=-P(X)$。

即
$$
e=\begin{cases}
1-P(X), & \text{概率 }P(X),\\
-P(X), & \text{概率 }1-P(X).
\end{cases}
\tag{25.1}
$$
（教材把第二支写成 $P(X)$ 并配概率 $1-P$，符号约定为 $e=Y-P$ 时第二支为 $-P$；方差推导用 $e\in\{1-P,-P\}$。）

检验 $\mathbb{E}[e\mid X]=P(1-P)+(1-P)(-P)=0$。

### (25.2) 条件方差

$$
\mathrm{Var}(e\mid X)=\mathbb{E}[e^2\mid X]=P(1-P)^2+(1-P)P^2=P(1-P).
\tag{25.2}
$$

**回扣：** 二元选择误差 **必然异方差**（除非 $P$ 为常数），LPM 的同方差 SE 不可靠。

---

## Exercise 25.4　验证 (25.5)：$\pi(Y\mid X)=G(Z'\beta)$

Bernoulli：$Y\in\{0,1\}$，$p=G(X'\beta)$（对称 link：$G(-u)=1-G(u)$）。

$$
\pi(y\mid X)=p^y(1-p)^{1-y}=G(X'\beta)^y\,G(-X'\beta)^{1-y}.
$$

定义
$$
Z=\begin{cases}X,& Y=1,\\ -X,& Y=0,\end{cases}
$$
则 $G(X'\beta)^Y G(-X'\beta)^{1-Y}=G(Z'\beta)$。故
$$
\pi(Y\mid X)=G(Z'\beta). \tag{25.5}
$$

---

## Exercise 25.5　Logistic 的 $h,H$

$\Lambda(x)=(1+e^{-x})^{-1}$。

### (a)

$$
\Lambda'(x)=\frac{e^{-x}}{(1+e^{-x})^2}=\Lambda(x)\bigl(1-\Lambda(x)\bigr).
$$

### (b)

$$
h_{\mathrm{logit}}(x)=\frac{d}{dx}\log\Lambda(x)=\frac{\Lambda'(x)}{\Lambda(x)}=1-\Lambda(x).
$$

### (c)

$$
\frac{d^2}{dx^2}\log\Lambda=\frac{d}{dx}(1-\Lambda)=-\Lambda'=-\Lambda(1-\Lambda),
$$
故
$$
H_{\mathrm{logit}}(x)=-\frac{d^2}{dx^2}\log\Lambda(x)=\Lambda(x)(1-\Lambda(x)).
$$

### (d)

$0\le\Lambda\le 1\Rightarrow 0\le\Lambda(1-\Lambda)\le 1/4\le 1$，故 $|H_{\mathrm{logit}}(x)|\le 1$。

---

## Exercise 25.6　Normal 的 $h,H$

### (a)

$$
h_{\mathrm{probit}}(x)=\frac{d}{dx}\log\Phi(x)=\frac{\phi(x)}{\Phi(x)}=\lambda(x)
$$
（逆 Mills 比）。

### (b)

令 $\lambda=\phi/\Phi$。则
$$
\lambda'=\frac{\phi'\Phi-\phi^2}{\Phi^2}=\frac{(-x\phi)\Phi-\phi^2}{\Phi^2}=-x\lambda-\lambda^2,
$$
故
$$
\frac{d^2}{dx^2}\log\Phi=\lambda'=-x\lambda-\lambda^2,
$$
$$
H_{\mathrm{probit}}(x)=-\frac{d^2}{dx^2}\log\Phi=\lambda(x)\bigl(x+\lambda(x)\bigr).
$$

---

## Exercise 25.7　Score、Hessian、全局凹

### (a) (25.6)(25.7)

$\ell_n(\beta)=\sum_i\log G(Z_i'\beta)$。  
$\partial\log G(Z'\beta)/\partial\beta=Z\,h(Z'\beta)$，故
$$
S_n(\beta)=\sum_i Z_i h(Z_i'\beta). \tag{25.6}
$$
再对 $\beta'$ 求导，并用 $H=-\frac{d^2}{dx^2}\log G$ 以及 $Z_iZ_i'=X_iX_i'$：
$$
H_n(\beta)=-\frac{\partial^2\ell_n}{\partial\beta\partial\beta'}=\sum_i X_iX_i'\,H(Z_i'\beta). \tag{25.7}
$$

### (b)

若 $H(x)>0$ 对所有 $x$，则每个 $X_iX_i'H(Z_i'\beta)$ 半正定，和 $H_n(\beta)\succeq 0$；在满秩条件下 $H_n(\beta)>0$（正定）对所有 $\beta$。

### (c)

Hessian 的负定（$\partial^2\ell_n/\partial\beta\partial\beta'=-H_n<0$）$\Rightarrow$ $\ell_n$ **全局严格凹**，MLE 唯一。

---

## Exercise 25.8　总体问题 (25.8) 的一阶条件

$\beta_0=\arg\max_\beta \ell(\beta)$，$\ell(\beta)=\mathbb{E}[\log G(Z'\beta)]$。  
FOC：
$$
\frac{\partial\ell}{\partial\beta}=\mathbb{E}\bigl[Z\,h(Z'\beta_0)\bigr]=0.
$$
（正确设定时等价于 $\mathbb{E}[X(Y-G(X'\beta_0))]$ 型矩，视 $h,G$ 而定。）

---

## Exercise 25.9　Logit MLE 的一阶条件

$h_{\mathrm{logit}}(t)=1-\Lambda(t)$，$Z=(2Y-1)X$ 形式下可化为熟悉形式。  
由 $S_n(\beta)=\sum Z_i(1-\Lambda(Z_i'\beta))=0$。  
等价地（常用写法）：
$$
\sum_{i=1}^n X_i\bigl(Y_i-\Lambda(X_i'\hat\beta_{\mathrm{logit}})\bigr)=0.
$$

---

## Exercise 25.10　Probit MLE 的一阶条件

$h_{\mathrm{probit}}=\lambda=\phi/\Phi$：
$$
\sum_{i=1}^n Z_i\,\lambda(Z_i'\hat\beta_{\mathrm{probit}})=0,
$$
或
$$
\sum_{i=1}^n X_i\left(Y_i\frac{\phi_i}{\Phi_i}-(1-Y_i)\frac{\phi_i}{1-\Phi_i}\right)=0,
$$
其中 $\Phi_i=\Phi(X_i'\hat\beta)$，$\phi_i=\phi(X_i'\hat\beta)$。

---

## Exercise 25.11　证明 (25.14) 并在 logit 下化简

一般 index 模型，记 $G=G(X'\beta)$，$g=G'$。可以验证
$$
h(Z'\beta)^2=\frac{g^2}{G^2}Y+\frac{g^2}{(1-G)^2}(1-Y)
=\frac{g(X'\beta)^2\bigl(Y-G(X'\beta)\bigr)^2}{G(X'\beta)^2\bigl(1-G(X'\beta)\bigr)^2}. \tag{25.14}
$$

**Logit：** $g=\Lambda(1-\Lambda)$，故 $g/G=1-\Lambda$，$g/(1-G)=\Lambda$，分子分母相消得
$$
h_{\mathrm{logit}}(Z'\beta)^2=\bigl(Y-\Lambda(X'\beta)\bigr)^2.
$$

---

## Exercise 25.12　用 NLLS 估 probit

正确设定下 $\mathbb{E}[Y\mid X]=\Phi(X'\beta)$，故
$$
\hat\beta=\arg\min_\beta\sum_i\bigl(Y_i-\Phi(X_i'\beta)\bigr)^2
$$
即对 $m(X,\beta)=\Phi(X'\beta)$ 做 **NLLS**。  

与 MLE 一般 **不同**（除非在特殊情形）；MLE 更常用且在正确正态 latent 下更有效。NLLS 不要求似然，但需数值优化且渐近方差按第 23 章 sandwich。

---

## Exercise 25.13　内生 probit (25.16)

结构：
$$
Y_1^*=X'\beta_1+Y_2\beta_2+e_1,\quad
Y_2=X'\gamma_1+Z'\gamma_2+e_2,\quad
Y_1=1\{Y_1^*>0\},
$$
$(e_1,e_2)\mid(X,Z)\sim$ 联合正态。

### (a) 验证 (25.16)

$e_1=\rho e_2+\varepsilon$，$\rho=\sigma_{12}/\sigma_2^2$，$\varepsilon\sim N(0,\sigma_\varepsilon^2)$ 与 $e_2$ 独立。  
代入：
$$
Y_1^*=X'\beta_1+Y_2\beta_2+\rho(Y_2-X'\gamma_1-Z'\gamma_2)+\varepsilon=\mu(\theta)+\varepsilon.
$$

### (b) 为何 $\varepsilon$ 独立于 $e_2$ 与 $Y_2$

联合正态下，回归残差 $\varepsilon=e_1-\rho e_2$ 与 $e_2$ **不相关且正态 ⇒ 独立**。  
$Y_2$ 是 $(X,Z,e_2)$ 的函数，故 $\varepsilon\perp(X,Z,e_2)$ 时 $\varepsilon\perp Y_2$。

### (c) $Y_1^*$ 的条件分布

给定 $(X,Z,Y_2)$（因而给定 $\mu(\theta)$），$Y_1^*=\mu(\theta)+\varepsilon$ 与 $\varepsilon$ 同分布：
$$
Y_1^*\mid(X,Z,Y_2)\sim N(\mu(\theta),\sigma_\varepsilon^2).
$$

---

## Exercise 25.14　异方差非参二元选择

$$
Y^*=m(X)+e,\quad e\mid X\sim N(0,\sigma^2(X)),\quad Y=1\{Y^*>0\}.
$$

### (a) 响应概率

$$
\mathbb{P}(Y=1\mid X=x)=\mathbb{P}\bigl(e>-m(x)\mid X=x\bigr)
=\Phi\Bigl(\frac{m(x)}{\sigma(x)}\Bigr).
$$

### (b) $m$ 与 $\sigma^2$ 是否都识别？

**否。** 观测只识别比值 $m(x)/\sigma(x)$（或 $\Phi(m/\sigma)$）。对任意 $a(x)>0$，
$(m,\sigma)\mapsto(a m, a\sigma)$ 给出同一 $P(x)$。

### (c) 识别用的规范化

例如：

- $\sigma(x)\equiv 1$（同方差 probit 非参指标）；或  
- $\sigma(x_0)=1$ 在某点；或  
- $\|m\|=1$ 等尺度约束。  

规范化后可谈 $m$ 的形状（在选定尺度下）。

### (d) “允许异方差”是否有意义？

在 **纯非参** $m(x)$ 下，异方差已被 $\Phi(m/\sigma)$ 吸收，**再单独“加异方差”没有额外可识别内容**。  
有意义的情形是 **参数化指标** $m(x)=x'\beta$ 时，可设 $\sigma(x)=\exp(z'\gamma)$ 等，用额外结构分开 $\beta$ 与 $\gamma$。  
否则应直接非参估计 $P(x)=\mathbb{P}(Y=1\mid X=x)$。

---

## Exercise 25.15　男性：工会 membership 的 probit

### 设定

- 样本：`cps09mar` 中 `female==0`（$n=29140$）；  
- $Y=1\{\texttt{union}=1\}$（本样本均值约 **2.3%**，工会比例偏低，解读宜谨慎）；  
- $X$：常数、age、education、Black（`race==2`）、Hispanic（`hisp`）；  
- Probit MLE（Fisher scoring），报告 robust/sandwich SE 与 AME。

### 估计

| 变量 | 系数 | SE | AME |
|------|-----:|---:|----:|
| age | 0.0079 | 0.0013 | 0.0004 |
| education | −0.0255 | 0.0056 | −0.0014 |
| Black | −0.054 | 0.060 | −0.003 |
| Hispanic | −0.298 | 0.060 | −0.016 |
| 截距 | −1.95 | 0.10 | — |

### 解释

- 年龄略增加工会概率（AME 很小：每年约 +0.04 个百分点）。  
- 教育系数为负：更高学历略降低参与率（本样本）。  
- 西班牙裔显著更低；黑人系数不显著。  
- 因 $Y$ 极不平衡，拟合概率整体很低；**系数尺度仍受 probit 标准化**，看 AME 更合适。

---

## Exercise 25.16　女性：同上

$n=21602$，工会均值约 2.0%。

| 变量 | 系数 | SE | AME |
|------|-----:|---:|----:|
| age | 0.010 | 0.0017 | 0.0005 |
| education | 0.044 | 0.008 | 0.0021 |
| Black | −0.047 | 0.062 | −0.002 |
| Hispanic | −0.148 | 0.071 | −0.007 |
| 截距 | −3.09 | 0.14 | — |

### 与男性对比

- 女性 **教育为正**（男性为负）：高学历女性参与工会的条件概率略高。  
- 年龄效应同向、都小。  
- 西班牙裔仍为负。  
- 整体参与率极低，推断精度有限。

---

## Exercise 25.17　大学学历女性：婚姻对年龄的非线性

### 设定动机（对照 Figure 25.1）

- 样本：女性且 `education≥16`（大学及以上）；  
- $Y=1\{\texttt{marital}\in\{1,2,3\}\}$（已婚/丧偶等，与正文一致）；  
- 年龄与婚姻呈 **先升后平/略降**，线性 probit 不够 → 使用  
  $\Phi(\beta_0+\beta_1\mathrm{age}+\beta_2\mathrm{age}^2/100)$。

### 结果（$n=8030$，均值 0.65）

| | 系数 | SE |
|--|-----:|---:|
| age | 0.178 | 0.010 |
| age²/100 | −0.195 | 0.012 |

| 年龄 | $\hat P$ |
|-----:|---------:|
| 25 | 0.43 |
| 35 | 0.67 |
| 45 | 0.74 |
| 55 | 0.69 |
| 65 | 0.47 |

### 与大学男性（Figure 25.1 类）

男性同规格：$P(25)\approx0.45$，$P(35)\approx0.75$，$P(45)\approx0.86$，$P(55)\approx0.87$，之后仍高。  
**女性峰值更早、高年龄回落更明显**；男性中年平台更高更宽。

---

## Exercise 25.18　男性：婚姻 ~ age, educ, Black, Hispanic

线性指数 probit（全年龄男性，$n=29140$，婚姻率 0.72）。

| 变量 | 系数 | SE | AME |
|------|-----:|---:|----:|
| age | 0.031 | 0.0008 | **0.0097** |
| education | 0.038 | 0.003 | 0.012 |
| Black | −0.489 | 0.028 | **−0.15** |
| Hispanic | 0.004 | 0.024 | 0.001 |
| 截距 | −1.16 | 0.05 | — |

### 解释

- 年龄每岁约 +1 个百分点（全样本线性是对全局的粗糙平均；青年子样本会更大，见正文 Table 25.1）。  
- 教育提高婚姻概率。  
- 黑人男性显著更低（AME 约 −15%）；西班牙裔与基组差异小。

---

## Exercise 25.19　女性：同 25.18

$n=21602$，婚姻率 0.59。

| 变量 | 系数 | SE | AME |
|------|-----:|---:|----:|
| age | 0.013 | 0.0008 | **0.0047** |
| education | 0.033 | 0.0035 | 0.012 |
| Black | −0.617 | 0.027 | **−0.23** |
| Hispanic | −0.123 | 0.026 | −0.046 |
| 截距 | −0.67 | 0.06 | — |

### 与男性对比

- 年龄 AME 约为男性一半（女性全样本年龄剖面更平、或更早完成婚姻）。  
- 教育效应相近。  
- 黑人、西班牙裔负效应 **更大**（种族差距在女性中更突出）。  
- 再次强调：线性 age 在全年龄段是近似；精细分析宜用 25.17 类非线性。

---

## 小结

| 题 | 要点 |
|:--:|------|
| 25.1–25.2 | 翻转 $Y$ 反号；改 $X$ 单位则 $\beta$ 反比缩放 |
| 25.3–25.11 | 误差两点分布、似然、$h/H$、FOC、全局凹 |
| 25.12–25.14 | NLLS-probit；IV probit；异方差下 $m/\sigma$ 识别 |
| 25.15–25.19 | CPS 工会与婚姻 probit 实证 |

代码：`docs/ch25/Hansen_Ch25_Exercises_Solutions.ipynb`。
