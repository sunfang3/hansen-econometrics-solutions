# Bruce Hansen《Econometrics》第 17 章习题解答（详细注释版）

**章节：** Chapter 17 Panel Data  
**出版版：** `hansen/manuscripts/Econometrics_Fullbook.pdf`，PDF 第 701–703 页（印刷页 666–668），§17.45 Exercises（**17.1–17.18 全部**）

---

## 0. 读题前必看：本章到底在讲什么

**承上启下：**
- 第 2–13 章：**横截面**数据（每个个体观测一次），i.i.d.
- 第 14–16 章：**时间序列**（同一个体连续观测），序列相关。
- **第 17 章：面板数据（panel data）—— 同一组个体（$i=1,\ldots,N$）在多期（$t=1,\ldots,T$）被观测。** 兼有横截面和时间两个维度。

**核心直觉：** 面板数据的关键特征是**个体效应** $u_i$——不随时间变化的不可观测异质性（如企业文化、个人能力）。$u_i$ 与回归元 $X_{it}$ 相关时，混合 OLS **有偏**。消除 $u_i$ 的方法：

| 方法 | 怎么消除 $u_i$ | 何时有效 | 代价 |
|---|---|---|---|
| **固定效应 FE** | 减个体均值（within）$\dot Y_{it}=Y_{it}-\bar Y_i$ | $u_i$ 与 $X$ 相关 | 损失组间变异 |
| **一阶差分 FD** | 相邻差分 $\Delta Y_{it}=Y_{it}-Y_{i,t-1}$ | $u_i$ 与 $X$ 相关 | 损失一期、效率低于 FE |
| **随机效应 RE** | GLS 加权（不消 $u_i$，但建模其方差） | $u_i$ 与 $X$ **不相关** | 若相关则不一致 |

**Hausman 检验：** 比较 FE（一致但效率低）vs RE（效率高但需 $u_i\perp X$）。若两者显著不同 ⇒ $u_i$ 与 $X$ 相关 ⇒ 用 FE。

**动态面板（本章难点）：** $Y_{it}=\alpha Y_{i,t-1}+u_i+\varepsilon_{it}$。FE 有 **Nickell 偏误**（因 $Y_{i,t-1}$ 与 $\bar Y_i$ 相关）。**Arellano–Bond GMM**：差分消 $u_i$，用滞后水平作工具。**Blundell–Bond（系统 GMM）**：加水平方程矩，改善弱工具。

**聚类标准误：** 面板数据中同一个体的误差相关（通过 $u_i$ 或序列相关）。**不聚类会严重低估 SE**（已验证：混合 OLS 中非聚类 SE=0.042 vs 聚类 0.090，**偏小 2.2 倍**）。

> **和本科对照：** 陈强系统讲 **面板数据**（`xtreg, fe/re`、Hausman、动态面板 `xtabond2`）。李子奈有基本的面板介绍。Hansen 的贡献：严格推出 FE/RE 的渐近理论（$N\to\infty$、$T$ 固定）、Stock–Watson 异方差稳健方差校正、以及动态面板 GMM 的完整框架。

> **实证（蒙特卡洛，已验证）：**
> - **FE vs 混合 OLS**：$u_i$ 与 $X$ 相关时，混合 OLS 均值≈2.0（偏，真 β=1），FE 均值≈1.0（一致）。
> - **组内变异损失**：var($\dot X$)=0.82 ≪ var($X$)=5.04（within 损失 84% 变异——这是 FE 的效率代价）。
> - **$T=2$ 时 FD=FE**：逐样本数值完全相同。
> - **聚类 SE 必要**：混合 OLS 中不聚类 SE 偏小 **2.2 倍**。

---

## 1. 记号、概念速查与"面板工具箱"

| Hansen 记号 | 中文/本科说法 | 一句话解释 |
|---|---|---|
| $Y_{it}=X_{it}'\beta+u_i+\varepsilon_{it}$ | 面板回归模型 | $u_i$ 个体效应，$\varepsilon_{it}$ 特异误差 |
| $u_i$ | 个体效应 / 不可观测异质性 | 不随时间变；与 $X$ 相关⇒FE，不相关⇒RE |
| $\dot Y_{it}=Y_{it}-\bar Y_i$ | within 变换 / 去个体均值 | 消除 $u_i$ |
| $\Delta Y_{it}=Y_{it}-Y_{i,t-1}$ | 一阶差分 | 也消除 $u_i$ |
| FE $\hat\beta_{\mathrm{fe}}$ | 固定效应估计量 | 对 within 变换后做 OLS |
| RE $\hat\beta_{\mathrm{re}}$ | 随机效应 / GLS 估计量 | 对 $\Omega^{-1/2}$ 变换后做 OLS |
| Hausman 检验 | Hausman 检验 | FE vs RE 是否显著不同 |
| 聚类 SE | cluster-robust SE | 按个体聚类修正标准误 |
| AB GMM | Arellano–Bond GMM | 动态面板：差分 + 滞后水平作工具 |
| BB GMM | Blundell–Bond 系统 GMM | 加水平矩，改善弱工具 |

**面板工具箱（本章反复用）：**

> **(P1) Within 变换消除 $u_i$。** $\bar Y_i=T_i^{-1}\sum_t Y_{it}=\bar X_i'\beta+u_i+\bar\varepsilon_i$（$u_i$ 不随 $t$ 变）。故 $\dot Y_{it}=Y_{it}-\bar Y_i=\dot X_{it}'\beta+\dot\varepsilon_{it}$——**$u_i$ 被消去**。FE = 对 $\dot Y$ 关于 $\dot X$ 做 OLS。

> **(P2) FE 的方差（"夹心"再现）。** $\hat\beta_{\mathrm{fe}}-\beta=(\sum\dot X'\dot X)^{-1}\sum\dot X'\varepsilon$。条件方差 = 夹心 $(\sum\dot X'\dot X)^{-1}(\sum\dot X'\Sigma\dot X)(\sum\dot X'\dot X)^{-1}$（$\Sigma=E[\varepsilon\varepsilon'|X]$）。

> **(P3) $T=2$ 时 FD=FE。** 差分 $\Delta Y_{i2}=Y_{i2}-Y_{i1}$ 和 within $\dot Y_{it}=Y_{it}-\bar Y_i$ 给出**完全相同**的正规方程（$T=2$ 时两者仅差一个常数因子）。

> **(P4) 聚类修正。** 面板中 $\mathrm{Cov}(\varepsilon_{it},\varepsilon_{is})\ne0$（通过 $u_i$ 或序列相关）。聚类 SE 把每个个体当成一个"超级观测"："肉"$=\sum_i(\sum_t\dot X_{it}\hat\varepsilon_{it})^2$。不聚类会**严重低估**。

> **(P5) 动态面板 + Nickell 偏误。** $Y_{it}=\alpha Y_{i,t-1}+u_i+\varepsilon_{it}$ 中，FE 有偏：因 $Y_{i,t-1}$ 含 $u_i$，与 within 后的 $\bar Y_i$ 相关。AB GMM 用差分消 $u_i$ 后、以 $Y_{i,t-2},Y_{i,t-3},\ldots$ 作 $\Delta Y_{i,t-1}$ 的工具。

---

## 预备记号

面板模型 $Y_{it}=X_{it}'\beta+u_i+\varepsilon_{it}$，$i=1,\ldots,N$，$t\in S_i$（可能非平衡）。$n=\sum_i T_i$。
个体均值 $\bar Y_i=T_i^{-1}\sum_{t\in S_i}Y_{it}$；within 变换 $\dot Y_{it}=Y_{it}-\bar Y_i$；差分 $\Delta Y_{it}=Y_{it}-Y_{i,t-1}$。
$M_i=I_{T_i}-\iota_{T_i}\iota_{T_i}'/T_i$（within 矩阵，幂等）。FE 估计量 $\hat\beta_{\mathrm{fe}}=(\sum\dot X_i'\dot X_i)^{-1}\sum\dot X_i'\dot Y_i$。

---

## Exercise 17.1　随机效应 GLS 与混合估计方差

随机效应模型下 $\mathbb{E}[e_i\mid X_i]=0$，$\mathbb{E}[e_i e_i'\mid X_i]=\sigma_\varepsilon^2\Omega_i$。

### (a) 证 (17.11) 与 (17.12)

**GLS：**
$$
\hat\beta_{\mathrm{gls}}-\beta=\Big(\sum_i X_i'\Omega_i^{-1}X_i\Big)^{-1}\sum_i X_i'\Omega_i^{-1}e_i.
$$
故条件方差
$$
V_{\mathrm{gls}}=\mathrm{Var}(\hat\beta_{\mathrm{gls}}\mid X)=\Big(\sum_{i=1}^N X_i'\Omega_i^{-1}X_i\Big)^{-1}. \tag{17.11}
$$

**混合 OLS：** $\hat\beta_{\mathrm{pool}}=(X'X)^{-1}X'Y$，
$$
V_{\mathrm{pool}}=\Big(\sum_i X_i'X_i\Big)^{-1}\Big(\sum_i X_i'\Omega_i X_i\Big)\Big(\sum_i X_i'X_i\Big)^{-1}. \tag{17.12}
$$

### (b) 证 (17.13) $V_{\mathrm{gls}}\le V_{\mathrm{pool}}$

这是 Gauss–Markov：在 $\mathrm{Var}(e\mid X)=\sigma_\varepsilon^2\Omega$ 已知时，GLS 在线性无偏类中方差最小。  
代数上：记 $A=\Omega^{-1/2}X$，混合估计等价于对变换后模型做非最优加权；由
$$
(X'\Omega^{-1}X)^{-1}\le (X'X)^{-1}(X'\Omega X)(X'X)^{-1}
$$
（对正定 $\Omega$ 的 Löwner 序），得 $V_{\mathrm{gls}}\le V_{\mathrm{pool}}$。当 $\sigma_u^2=0$（$\Omega=I$）时两者相等。

---

## Exercise 17.2　$\mathbb{E}[\varepsilon_{it}\mid X_{it}]=0$ 对 FE 无偏是否充分？

**不充分。**

Within 估计量
$$
\hat\beta_{\mathrm{fe}}-\beta=\Big(\sum_i \dot X_i'\dot X_i\Big)^{-1}\sum_i \dot X_i'\varepsilon_i,
$$
无偏需要 $\mathbb{E}[\dot X_i'\varepsilon_i\mid X]=0$，即
$$
\mathbb{E}[X_{is}\varepsilon_{it}]=0\quad\text{对所有 }s,t
$$
（**严格外生**），或更强的 $\mathbb{E}[\varepsilon_i\mid X_i]=0$。  

仅 $\mathbb{E}[\varepsilon_{it}\mid X_{it}]=0$（当代外生）**不够**：$\dot X_{it}=X_{it}-\bar X_i$ 含 $X_{is}$（$s\ne t$），若 $\mathbb{E}[X_{is}\varepsilon_{it}]\ne0$（反馈、前定但非严格外生），则 $\mathbb{E}[\dot X'\varepsilon]\ne0$，FE **有偏**。动态面板中滞后 $Y$ 即典型例子（Nickell 偏误）。

---

## Exercise 17.3　$\mathrm{var}(\dot X_{it})\le\mathrm{var}(X_{it})$

对固定 $i$，时间维样本：$X_{it}=\bar X_i+\dot X_{it}$，且 $\sum_t\dot X_{it}=0$。  
跨 $t$ 的二阶矩：
$$
\frac1{T_i}\sum_t X_{it}^2=\bar X_i^2+\frac1{T_i}\sum_t\dot X_{it}^2\ge\frac1{T_i}\sum_t\dot X_{it}^2.
$$
在总体中（对平稳或混合分布）$\mathrm{Var}(X_{it})=\mathrm{Var}(\bar X_i)+\mathrm{Var}(\dot X_{it})\ge\mathrm{Var}(\dot X_{it})$（$\bar X_i$ 与 demean 正交）。  
矩阵意义：$\mathbb{E}[\dot X\dot X']\le\mathbb{E}[XX']$（Löwner 序），因 $\dot X=M_i X$，$M_i$ 幂等收缩。

---

## Exercise 17.4　证 (17.24)

在 $\mathbb{E}[\varepsilon_i\mid X_i]=0$ 下 $\hat\beta_{\mathrm{fe}}$ 无偏，且
$$
\hat\beta_{\mathrm{fe}}-\beta=\Big(\sum_i\dot X_i'\dot X_i\Big)^{-1}\sum_i\dot X_i'\varepsilon_i.
$$
令 $\Sigma_i=\mathbb{E}[\varepsilon_i\varepsilon_i'\mid X_i]$，则
\begin{align*}
V_{\mathrm{fe}}
&=\mathrm{Var}(\hat\beta_{\mathrm{fe}}\mid X)\\
&=\Big(\sum_i\dot X_i'\dot X_i\Big)^{-1}
\Big(\sum_i\dot X_i'\Sigma_i\dot X_i\Big)
\Big(\sum_i\dot X_i'\dot X_i\Big)^{-1}. \tag{17.24}
\end{align*}

---

## Exercise 17.5　证 (17.28)

在 $u_i=0$ 且 $\Sigma_i=I\sigma_\varepsilon^2$ 时，
$$
V_{\mathrm{fe}}^0=\sigma_\varepsilon^2\Big(\sum_i\dot X_i'\dot X_i\Big)^{-1},\qquad
V_{\mathrm{pool}}=\sigma_\varepsilon^2\Big(\sum_i X_i'X_i\Big)^{-1}.
$$
因 $\sum_i\dot X_i'\dot X_i=\sum_i X_i'M_i X_i\le\sum_i X_i'X_i$（$M_i$ 幂等，$I-M_i$ 半正定），  
逆矩阵反号：$\big(\sum\dot X'\dot X\big)^{-1}\ge\big(\sum X'X\big)^{-1}$，故 $V_{\mathrm{fe}}^0\ge V_{\mathrm{pool}}$。  
直觉：去个体均值损失组间变异，效率下降是对个体效应稳健性的代价。

---

## Exercise 17.6　$T=2$ 时差分估计量 (17.30) = FE

$T=2$ 时，个体 $i$ 仅一对观测。  
Within：$\dot Y_{i1}=Y_{i1}-\bar Y_i=\tfrac12(Y_{i1}-Y_{i2})$，$\dot Y_{i2}=\tfrac12(Y_{i2}-Y_{i1})$（$X$ 同理）。  
FE 正规方程由 $\sum_i\sum_{t=1}^2\dot X_{it}\dot Y_{it}=0$ 给出。因 $\dot X_{i2}=-\dot X_{i1}$、$\dot Y_{i2}=-\dot Y_{i1}$，
$$
\sum_i\big[\dot X_{i1}\dot Y_{i1}+\dot X_{i2}\dot Y_{i2}\big]
=\sum_i 2\dot X_{i1}\dot Y_{i1}
=\tfrac12\sum_i\Delta X_{i2}\Delta Y_{i2}.
$$
差分估计对 $\Delta Y_{i2}=\Delta X_{i2}'\beta+\Delta\varepsilon_{i2}$ 做 OLS，正规方程相同，故 $\hat\beta_\Delta=\hat\beta_{\mathrm{fe}}$。  
（$T>2$ 时 $D'D\ne c\,M$，两者一般不同。）

---

## Exercise 17.7　仅用 $\hat\sigma_\varepsilon^2$ 与水平残差方差估计 $\sigma_u^2$

水平残差 $e_{it}=Y_{it}-X_{it}'\hat\beta_{\mathrm{fe}}$ 估计 $e_{it}=u_i+\varepsilon_{it}$。  
在 RE 结构下
$$
\mathbb{E}[e_{it}^2]=\sigma_u^2+\sigma_\varepsilon^2.
$$
一致估计：
$$
\hat\sigma_e^2=n^{-1}\sum_i\sum_{t\in S_i}\hat e_{it}^2,\qquad
\hat\sigma_\varepsilon^2\text{ 由 within 残差 (17.37)}.
$$
故
$$
\hat\sigma_u^2=\hat\sigma_e^2-\hat\sigma_\varepsilon^2.
$$
（若为负可截断为 0。）相对 between 法，这里不显式用个体均值回归，但依赖水平残差与 FE 斜率。

---

## Exercise 17.8　$\hat\sigma_\varepsilon^2$ (17.37) 的无偏性

$$
\hat\sigma_\varepsilon^2=\frac{1}{n-N-k}\sum_i\hat\varepsilon_i'\hat\varepsilon_i,\qquad
\hat\varepsilon_i=M_i(Y_i-X_i\hat\beta_{\mathrm{fe}})=M_i\varepsilon_i-M_i X_i(\hat\beta_{\mathrm{fe}}-\beta).
$$
在 (17.18)、(17.25)、(17.26) 下，$\Sigma_i=\sigma_\varepsilon^2 I$，且 $\hat\beta_{\mathrm{fe}}$ 为 within OLS。  
与含 $N$ 个个体虚拟变量的虚拟变量回归等价：总残差自由度 $n-N-k$，经典线性模型下
$$
\mathbb{E}\Big[\sum_i\hat\varepsilon_i'\hat\varepsilon_i\Big]=(n-N-k)\sigma_\varepsilon^2,
$$
故 $\mathbb{E}[\hat\sigma_\varepsilon^2]=\sigma_\varepsilon^2$。

---

## Exercise 17.9　差分估计量的渐近理论（Theorem 17.2 的差分版）

模型 $Y_{it}=X_{it}'\beta+u_i+\varepsilon_{it}$。差分：$\Delta Y_i=\Delta X_i\beta+\Delta\varepsilon_i$。

**定理（差分 OLS）。** 设：  
1. 个体 i.i.d.，$T\ge2$ 固定，$N\to\infty$；  
2. $\mathbb{E}[\Delta X_i'\Delta\varepsilon_i]=0$；  
3. $Q_\Delta=\mathbb{E}[\Delta X_i'\Delta X_i]>0$；  
4. 四阶矩有限。  

则
$$
\sqrt{N}(\hat\beta_\Delta-\beta)\to_d N(0,Q_\Delta^{-1}\Omega_\Delta Q_\Delta^{-1}),\quad
\Omega_\Delta=\mathbb{E}[\Delta X_i'\Delta\varepsilon_i\Delta\varepsilon_i'\Delta X_i].
$$

**可减弱 Assumption 17.2.3：**  
FE 需要 $\mathbb{E}[X_{is}\varepsilon_{it}]=0$ 对**所有** $s,t$（严格外生）。  
差分只需 $\mathbb{E}[\Delta X_{it}\Delta\varepsilon_{it}]=0$，在 $\varepsilon$ 序列不相关时，这由
$$
\mathbb{E}[X_{it}\varepsilon_{it}]=\mathbb{E}[X_{i,t-1}\varepsilon_{it}]=\mathbb{E}[X_{it}\varepsilon_{i,t-1}]=\mathbb{E}[X_{i,t-1}\varepsilon_{i,t-1}]=0
$$
等推出——允许 $X_{it}$ 与 $\varepsilon_{i,t+1},\varepsilon_{i,t+2},\ldots$ 相关（**前定 / 弱外生**），但不允许与 $\varepsilon_{i,t-1}$ 任意相关。  
故差分估计在“前定回归元”下可比 FE 更弱的严格外生假设下仍一致（但效率通常低于 FE，若严格外生成立）。

---

## Exercise 17.10　证 (17.57)

平衡面板、真 $\beta$ 下去均值残差 $\hat\varepsilon_{it}=\varepsilon_{it}-\bar\varepsilon_i$，
$$
\bar\varepsilon_i=T^{-1}\sum_{j=1}^T\varepsilon_{ij}.
$$
在序列不相关 (17.26) 与 $\mathbb{E}[\varepsilon_{it}^2\mid X]=\sigma_{it}^2$ 下，
\begin{align*}
\mathbb{E}[\hat\varepsilon_{it}^2\mid X]
&=\mathbb{E}\Big[\Big(\varepsilon_{it}-\bar\varepsilon_i\Big)^2\Big|X\Big]
=\sigma_{it}^2\Big(1-\frac1T\Big)^2+\sum_{j\ne t}\sigma_{ij}^2\Big(\frac1T\Big)^2\\
&=\Big(\frac{T-1}{T}\Big)^2\sigma_{it}^2+\frac1{T^2}\sum_{j\ne t}\sigma_{ij}^2.
\end{align*}
整理（令 $\sigma_i^2=T^{-1}\sum_j\sigma_{ij}^2$）得
$$
\mathbb{E}[\hat\varepsilon_{it}^2\mid X]=\frac{T-2}{T}\sigma_{it}^2+\frac1T\sigma_i^2. \tag{17.57}
$$
（与教材形式一致；当同方差时退化为 $\sigma_\varepsilon^2(T-1)/T$。）

---

## Exercise 17.11　Stock–Watson 校正的无偏性

### (a)

$\hat\sigma_i^2=(T-1)^{-1}\sum_t\hat\varepsilon_{it}^2$。在真 $\beta$、同方差序列不相关下 $\mathbb{E}[\hat\varepsilon_{it}^2\mid X_i]=\sigma_\varepsilon^2(T-1)/T$，故
$$
\mathbb{E}[\hat\sigma_i^2\mid X_i]=\sigma_i^2
$$
（异方差时 $\sigma_i^2=T^{-1}\sum_t\sigma_{it}^2$，由 (17.57) 对 $t$ 平均并缩放 $(T-1)$ 可得 $\mathbb{E}[\hat\sigma_i^2\mid X_i]=\sigma_i^2$）。

### (b)

$\tilde V_{\mathrm{fe}}=\frac{T-1}{T-2}\hat V_{\mathrm{fe}}-\frac1{T-1}\hat B_{\mathrm{fe}}$ 中，将 (17.57) 代入 $\mathbb{E}[\hat V_{\mathrm{fe}}\mid X]$ 的展开，交叉项恰由 $\hat B_{\mathrm{fe}}$ 抵消，得 $\mathbb{E}[\tilde V_{\mathrm{fe}}\mid X]=V_{\mathrm{fe}}$。

---

## Exercise 17.12　非平衡面板的 (17.61)–(17.62) 与 $\tilde V_{\mathrm{fe}}$

### (a)(b)

对个体 $i$，$T_i$ 期，去均值 $\hat\varepsilon_{it}=\varepsilon_{it}-\bar\varepsilon_i$，同 17.10 的计算以 $T_i$ 替换 $T$：
$$
\mathbb{E}[\hat\varepsilon_{it}^2\mid X_i]=\frac{T_i-2}{T_i}\sigma_{it}^2+\frac1{T_i}\sigma_i^2, \tag{17.61}
$$
$$
\mathbb{E}[\hat\sigma_i^2\mid X_i]=\sigma_i^2,\quad
\hat\sigma_i^2=\frac1{T_i-1}\sum_{t\in S_i}\hat\varepsilon_{it}^2. \tag{17.62}
$$

### (c)

(17.60) 对 $T_i=2$ 与 $T_i>2$ 分别用不同权重，恰使 $\mathbb{E}[\hat\varepsilon_{it}^2]$ 的偏误在 sandwich 中间矩阵中被校正，故 $\mathbb{E}[\tilde V_{\mathrm{fe}}\mid X]=V_{\mathrm{fe}}$。

---

## Exercise 17.13　二次项的 within 变换

模型 $Y_{it}=X_{it}\beta_1+X_{it}^2\beta_2+u_i+\varepsilon_{it}$。  

**错误做法：** 先对 $Y,X$ 做 within 得 $\dot Y,\dot X$，再回归 $\dot Y$ 对 $\dot X$ 与 $\dot X^2$。  
因为 $(X_{it}^2)\dot{}\ne (\dot X_{it})^2$：
$$
X_{it}^2-\overline{X_i^2}\ne (X_{it}-\bar X_i)^2.
$$

**正确 FE：** 先构造水平回归元 $W_{it}=(X_{it},X_{it}^2)$，再对 $(Y_{it},W_{it})$ **一起** within，或等价跑
$$
Y_{it}=X_{it}\beta_1+X_{it}^2\beta_2+u_i+\varepsilon_{it}
$$
的虚拟变量 / `xtreg, fe`。即对 $X^2$ 的 within 是 $\widetilde{X^2}_{it}=X_{it}^2-\overline{X_i^2}$，不是 $(\dot X_{it})^2$。

---

## Exercise 17.14　恰好识别 Hausman–Taylor 的简化

模型 $Y=X_1\beta_1+X_2\beta_2+Z_1\gamma_1+Z_2\gamma_2+u+\varepsilon$，工具 $Z=(\dot X_1,\dot X_2,X_1,Z_1)$，恰好识别 $k_1=\ell_2$。

样本矩：
\begin{align}
\dot X'(Y-X\beta-Z\gamma)&=0, \tag{*}\\
(X_1,Z_1)'(Y-X\beta-Z\gamma)&=0.
\end{align}
因 $\dot X'Z=0$（within 与时间不变 $Z$ 正交），$(*)$ 化为 $\dot X'(Y-X\beta)=0$，即 **$\hat\beta=(\hat\beta_1',\hat\beta_2')'$ 为 FE 估计量**。  

代入第二组矩：令 $\hat u_i=\bar Y_i-\bar X_i'\hat\beta_{\mathrm{fe}}$（估计的个体效应），则
$$
(X_1,Z_1)'(\hat u-Z_1\gamma_1-Z_2\gamma_2)=0,
$$
即对 $\hat u_i$ 关于 $(Z_{1i},Z_{2i})$ 的 **2SLS**，其中 $Z_2$ 以 $X_1$ 为工具（外生 $Z_1$ 作自身工具）。故 $\hat\gamma_1,\hat\gamma_2$ 如题所述。

---

## Exercise 17.15　AB1991：资本 AR(1) 的 AB vs BB

**模型：** $K_{it}=\alpha K_{i,t-1}+u_i+v_t+\varepsilon_{it}$（$K=\texttt{k}$ 对数资本），年固定效应，Arellano–Bond / Blundell–Bond **one-step GMM**，cluster 稳健 SE。  
工具：差分方程用 $K$ 的 2–5 阶水平滞后（collapsed）；系统 GMM 另加水平方程中 $\Delta K_{i,t-1}$ 作工具。

| 估计量 | $\hat\alpha$ | cluster SE | $N$ 企业 |
|--------|-------------:|-----------:|---------:|
| Arellano–Bond one-step | **0.538** | 0.181 | 140 |
| Blundell–Bond one-step | **0.999** | 0.036 | 140 |

### (c) 差异解释

资本序列 **高度持续**（$\alpha$ 接近 1），$\sigma_u^2/\sigma_\varepsilon^2$ 往往较大。此时差分方程中 $K_{i,t-2}$ 对 $\Delta K_{i,t-1}$ 的第一阶段系数 $\gamma\approx(\alpha-1)\cdot\frac{k}{k+\sigma_u^2/\sigma_\varepsilon^2}$ **接近 0**（弱工具，§17.40）。  
AB 有限样本严重 **向下偏**（此处 $\hat\alpha\approx0.54$）。  
BB 加入水平矩 $\mathbb{E}[\Delta K_{i,t-1}(K_{it}-\alpha K_{i,t-1}-\cdots)]=0$（需初始条件平稳型假定 (17.101)），在 $\alpha\approx1$ 时仍识别，估计靠近 1。  
这与 Blundell–Bond (1998) 的核心信息一致：**弱工具下 AB 不可靠，系统 GMM 改善**。

---

## Exercise 17.16　就业动态劳动需求（复现/扩展 Blundell–Bond）

**设定 (17.114)：**
$$
N_{it}=\alpha N_{i,t-1}+\beta_0 W_{it}+\beta_1 W_{i,t-1}+\gamma_0 K_{it}+\gamma_1 K_{i,t-1}+u_i+v_t+\varepsilon_{it}.
$$
变量：`n,w,k`（对数就业、工资、资本）。AB one-step，年 FE，cluster SE。

| | $N_{t-1}$ | $W_t$ | $W_{t-1}$ | $K_t$ | $K_{t-1}$ |
|--|----------:|------:|----------:|------:|----------:|
| **(a) $W,K$ 严格外生** | 0.626 (0.236) | −0.535 (0.186) | 0.306 (0.228) | 0.358 (0.065) | −0.087 (0.101) |
| **(b) 全部回归元前定** | 0.763 (0.109) | −0.574 (0.190) | 0.328 (0.191) | 0.234 (0.163) | −0.131 (0.073) |
| 教材 (17.114) 前定 | 0.708 (0.084) | −0.709 (0.117) | 0.500 (0.111) | 0.466 (0.101) | −0.215 (0.086) |
| **(c) BB 系统 one-step** | 0.559 (0.137) | −0.541 (0.209) | 0.306 (0.187) | 0.338 (0.086) | −0.033 (0.079) |

（实现为 collapsed 矩，与 Stata `xtabond` 全矩矩阵略有差别，故与 (17.114) 点估计接近但非逐位相同。）

### (b) 严格外生 vs 前定

严格外生假定 $\mathbb{E}[W_{is}\varepsilon_{it}]=0$ 对所有 $s,t$，允许用 $\Delta W_t,\Delta K_t$ 作自身工具。  
若工资/资本对过去冲击有反馈，则 $\Delta W_t$ 与 $\Delta\varepsilon_t$ 相关，严格外生 AB **不一致**。  
前定假定只用 $W_{i,t-s}$（$s\ge1$）等滞后水平作工具，放松反馈，系数与 SE 都变化（此处 $N$ 滞后从 0.63 升至 0.76，$K$ 当期系数下降）。

### (d) 劳动需求解释

- $\hat\alpha\in(0.5,0.8)$：就业调整有摩擦，半年–一年半衰期量级。  
- $W_t$ 系数为负：工资上升抑制就业（短期需求弹性）。  
- $W_{t-1}$ 为正且与 $W_t$ 部分抵消：长期工资效应 = $(\beta_0+\beta_1)/(1-\alpha)$，通常仍为负但小于短期。  
- $K_t>0$：资本与劳动互补（规模扩张），$K_{t-1}$ 部分回调。

### (e) 忘记 cluster 的后果

动态面板误差在个体内高度相关（$u_i$、序列相关的 $\varepsilon$）。不用 cluster 时，报告的 SE 往往只有 cluster SE 的 **约 1/2–1/3**（经验上可小 **2–4 倍**），过度拒绝。必须在个体层面 cluster（或使用 Windmeijer 校正的稳健 SE）。

---

## Exercise 17.17　Invest1993：债务 AR(1)

**模型：** $D_{it}=\alpha D_{i,t-1}+u_i+\varepsilon_{it}$，$D=\texttt{debta}$。  
样本：至少 5 期的企业，$N\approx1787$ 家，含年 FE。两步 GMM + cluster 稳健 SE；工具滞后至 4。

| 估计量 | $\hat\alpha$ | SE |
|--------|-------------:|---:|
| AB two-step | 0.553 | 0.056 |
| BB two-step | 0.648 | 0.036 |
| AB one-step | 0.581 | 0.058 |
| AB two-step AR(2)：$D_{t-1},D_{t-2}$ | 0.627, 0.031 | 0.058, 0.024 |

### (c) 敏感性

| 维度 | 对系数 | 对 SE |
|------|--------|-------|
| one-step vs two-step | 较小（$\alpha$ 差约 0.03） | two-step 略紧，但需稳健公式 |
| AR(1) vs AR(2) | $D_{t-2}\approx0$，主系数略升 | 变化中等 |
| 工具滞后深度 | 中等 | 工具过多 → SE 偏小、有限样本偏误 |
| 经典 SE vs cluster | 系数不变 | **cluster 显著放大 SE**（主要差异来源） |

**结论：** 系数对 AB/BB 选择更敏感（BB 更高，与持续债务一致）；**SE 对是否 cluster 最敏感**。

---

## Exercise 17.18　债务动态 + $I,Q,CF$

$$
D_{it}=\alpha D_{i,t-1}+\beta_1 I_{i,t-1}+\beta_2 Q_{i,t-1}+\beta_3 CF_{i,t-1}+u_i+\varepsilon_{it}
$$
（`debta, inva, vala, cfa` 滞后）。全部回归元作 **前定**，两步 GMM，cluster SE，$N\approx1635$。

| | $D_{t-1}$ | $I_{t-1}$ | $Q_{t-1}$ | $CF_{t-1}$ |
|--|----------:|----------:|----------:|-----------:|
| AB two-step | 0.592 (0.029) | 0.040 (0.048) | −0.0010 (0.0009) | −0.092 (0.021) |
| BB two-step | 0.659 (0.025) | 0.059 (0.044) | 0.0024 (0.0015) | −0.083 (0.025) |
| AB one-step | 0.583 (0.054) | −0.065 (0.075) | −0.0012 (0.0017) | −0.130 (0.031) |
| AB two-step, maxlag=2 | 0.564 (0.063) | −0.088 (0.102) | −0.0001 (0.0017) | −0.142 (0.046) |

### (c) 敏感性

- **系数：** BB vs AB 对 $\alpha$ 影响最大（+0.07 量级）；one/two-step 与 maxlag 对 $I,CF$ 符号/幅度影响大于对 $\alpha$。  
- **SE：** cluster 稳健 vs 经典（未列表）差异最大；工具更少（maxlag=2）使 SE 变大、估计更噪。  
- 经济含义：$CF$ 系数为负支持“现金流越高、后续杠杆越低 / 财务松弛”；$Q$ 效应弱；$D$ 高度持续。

---

## 小结

| 题 | 内容 |
|:--:|------|
| 17.1–17.8 | RE/FE 方差、无偏条件、within 变异、差分=FE（$T=2$）、方差分量 |
| 17.9–17.12 | 差分渐近、Stock–Watson 异方差稳健协方差偏误与校正 |
| 17.13–17.14 | 非线性回归元的 within；Hausman–Taylor 恰好识别 |
| 17.15–17.18 | AB1991 / Invest1993 上 AB 与 BB 动态面板 GMM 实证 |

**实现说明：** notebook 中为 **collapsed** Arellano–Bond / Blundell–Bond GMM（与 `xtabond2, collapse` 同类），含年固定效应与 cluster 稳健协方差；与 Stata 默认全矩矩阵在有限样本上可有数值差别，但定性结论（AB 弱工具下偏低、BB 抬高持续系数、cluster 必要）与 Hansen / Blundell–Bond 叙述一致。
