# Bruce Hansen《Econometrics》第 13 章习题解答（详细注释版）

**章节：** Chapter 13 Generalized Method of Moments
**书稿：** PDF 第 455–460 页（印刷页 435–440），§13.29 Exercises（**13.1–13.28 全部**）
**记号：** $g_n(\beta)=n^{-1}\sum Z_i(Y_i-X_i'\beta)$，$J_n(\beta)=n\,g_n'W g_n$；最优权 $W=\Omega^{-1}$，$\Omega=E[ZZ'e^2]$
**数值验证：** `Hansen_Ch13_Exercises_Solutions.ipynb`（13.27 AJR、13.28 Card + 理论结论的蒙特卡洛验证）

> **写给谁看：** 假设你学过李子奈/陈强，知道 2SLS、矩估计，但说不清"**GMM 到底比 2SLS 好在哪**""**最优权矩阵怎么选**""**过度识别 $J$ 检验检验什么**"。
> Hansen 第 13 章是**作者的看家本领**（Hansen 1982 提出 GMM）。GMM 是一个**统一框架**：OLS、IV、2SLS 都是它的特例，而**有效 GMM**（用最优权 $\Omega^{-1}$）是其中**最有效**的。本章把第 12 章的 IV 推广到任意矩条件与最优加权。

---

## 0. 读题前必看：本章到底在讲什么

**承上启下：**
- 第 12 章：IV/2SLS 解决内生性，但只用了**一类**矩条件（$E[Ze]=0$）和**一个特定权重**（$W=(Z'Z)^{-1}$）。
- **第 13 章 GMM：把"矩条件 + 加权"一般化。** 任何满足 $E[g_i(\beta)]=0$ 的矩条件都能用；权重 $W$ 可选，**最优**是 $W=\Omega^{-1}$。

**核心直觉（一张图）：** GMM = "找 $\beta$ 使样本矩 $g_n(\beta)=n^{-1}\sum g_i(\beta)$ 尽量接近 0，用权重 $W$ 衡量'距离'"：
$$\hat\beta_{\mathrm{gmm}}=\arg\min_\beta\, g_n(\beta)'W g_n(\beta).$$
- 矩条件数 $\ell$ 与参数数 $k$ 的关系决定**识别**：$\ell=k$ 恰好识别（矩=参数），$\ell>k$ 过度识别（矩多，需加权取舍），$\ell<k$ 不足识别（无解）。
- 权重 $W$ 决定**效率**：$W=\Omega^{-1}$（$\Omega=\mathrm{Var}(g_i)$）最优。

**三大特例（GMM 统一视角，务必记住）：**

| 估计量 | 矩条件 | 权重 $W$ | 何时最优 |
|---|---|---|---|
| **OLS** | $E[Xe]=0$ | $(X'X)^{-1}$ | 同方差 |
| **2SLS** | $E[Ze]=0$ | $(Z'Z)^{-1}$ | 同方差（仅此时=有效GMM） |
| **有效 GMM** | $E[Ze]=0$ | $\Omega^{-1}$（$\Omega=E[ZZ'e^2]$） | **任意**（异方差也最优） |

**关键结论（本章的灵魂）：**
1. **2SLS = 同方差下的有效 GMM。** 异方差下，有效 GMM 用 $\Omega^{-1}$ 加权比 2SLS **更有效**（方差更小）。
2. **最优权 $W=\Omega^{-1}$** 使渐近方差最小（Theorem 13.4）：$V_{\mathrm{eff}}=(Q'\Omega^{-1}Q)^{-1}\le V(W)$ 对任意 $W$。
3. **过度识别 $J$ 检验**：$J=n g_n(\hat\beta)'\hat\Omega^{-1}g_n(\hat\beta)\to_d\chi^2_{\ell-k}$，检验"多出来的 $\ell-k$ 个矩条件是否都成立"——即**工具有效性**（排除约束）。

> **实证（蒙特卡洛，已验证）：** $\ell=4$ 工具、$k=2$ 系数、强异方差（$\mathrm{var}(e)\propto e^{0.6Z_1}$）：
> - **MC var(2SLS 斜率)=0.0184 > var(有效GMM)=0.0170**——有效 GMM 更有效（异方差下 $\Omega^{-1}$ 加权的收益）；
> - **$J\to\chi^2_{\ell-k=2}$**：$H_0$（工具有效）真时 size≈0.02–0.05（两步 GMM 的 $J$ 有限样本略偏低，大样本→0.05）；
> - **$J$ 的功效**：让某工具直接进 $Y$（违反排除约束），$J=12.7$（$p=0.002$）⇒ 强烈拒绝，检测到无效工具；
> - **同方差下 2SLS≈有效 GMM**（数值接近），印证"2SLS 是同方差下的有效 GMM"。

**本章的"夹心"再现（与第 4、7、12 章同构）：**
$$V_\beta=(Q'WQ)^{-1}Q'W\Omega WQ(Q'WQ)^{-1},\qquad V_{\mathrm{eff}}=(Q'\Omega^{-1}Q)^{-1}\le V_\beta.$$
（$Q=E[ZX']$。）**又是面包-肉-面包**，最优权重让"面包"和"肉"配合最好，方差最小。

> **和本科对照：** 陈强系统讲 **GMM（广义矩估计）**：2SLS 是 GMM 的特例，有效 GMM 用 $\Omega^{-1}$，$J$ 检验过度识别。Hansen 的贡献（Hansen 1982）：把所有矩条件估计纳入统一框架，证明最优权的存在性，并给出 $J$ 检验。**这是 Hansen 的本行。**

---

## 1. 记号与概念速查（对照李子奈/陈强）

| Hansen 记号 | 中文/本科说法 | 一句话解释 |
|---|---|---|
| $g_i(\beta)=Z_i(Y_i-X_i'\beta)$ | 矩函数 | 线性 IV 的矩条件 |
| $g_n(\beta)=n^{-1}\sum g_i$ | 样本矩 | 总体矩 $E[g]=0$ 的样本版 |
| $J_n(\beta)=n g_n'W g_n$ | GMM 目标函数 | 加权矩距离 |
| $W$ | 权重矩阵 | 决定效率；最优 $W=\Omega^{-1}$ |
| $\Omega=E[ZZ'e^2]$ | 矩的方差 | $\mathrm{Var}(g_i)=E[g_ig_i']$ |
| 恰好识别 $\ell=k$ | exactly identified | 矩=参数，唯一解，$J\equiv0$ |
| 过度识别 $\ell>k$ | overidentified | 矩多，需加权；$J$ 可检验 |
| 有效 GMM | efficient GMM | $W=\Omega^{-1}$，方差最小 |
| 两步 GMM | two-step GMM | 先 2SLS 得 $\tilde\beta$，估 $\hat\Omega$，再 $\hat\Omega^{-1}$ 加权 |
| $J=n g_n'\hat\Omega^{-1}g_n$ | Hansen $J$ / Sargan | 过度识别检验，$\to\chi^2_{\ell-k}$ |
| 距离统计量 $D$ | distance statistic | $D=J(\tilde\beta)-J(\hat\beta)$，= Wald（线性） |

**两个最常用的"判据"：**
1. **识别看 $\ell$ vs $k$。** $\ell\ge k$ 才能识别；$\ell=k$ 恰好识别（$J\equiv0$，无法检验过度识别）；$\ell>k$ 过度识别（可检验）。
2. **效率看权重。** $W=\Omega^{-1}$ 最优；2SLS 的 $W=(Z'Z)^{-1}$ 只在同方差下最优。异方差下报告**有效 GMM**（或至少 2SLS + 稳健 SE）。

---

## 2. 预备记号

线性 IV-GMM：矩 $g_i(\beta)=Z_i(Y_i-X_i'\beta)$，$E[g(\beta)]=0$（即 $E[Ze]=0$）。
$g_n(\beta)=n^{-1}Z'(Y-X\beta)$，目标 $J_n(\beta)=n g_n'W g_n$。
GMM 估计量 $\hat\beta=(X'ZWZ'X)^{-1}X'ZWZ'Y$。
$Q=E[ZX']$，$\Omega=E[ZZ'e^2]$，$V_\beta=(Q'WQ)^{-1}Q'W\Omega WQ(Q'WQ)^{-1}$，最优 $V_{\mathrm{eff}}=(Q'\Omega^{-1}Q)^{-1}$。

---

## Exercise 13.1　两套矩的矩估计（OLS + 方差辅助回归）

**考点：** 最朴素的矩估计（MOM）——两套矩分别给 OLS 和辅助回归。

**解答：** 矩条件 $E\begin{pmatrix}X(Y-X'\beta)\\ Z(e^2-Z'\gamma)\end{pmatrix}=0$。恰好识别时 MOM=解方程：
$$\hat\beta=(\sum X_iX_i')^{-1}\sum X_iY_i\ \text{(OLS)},\quad \hat\gamma=(\sum Z_iZ_i')^{-1}\sum Z_i\hat e_i^2\ (e^2\text{ 对 }Z\text{ 的 OLS}).$$
两步：先 $\hat\beta$（得 $\hat e$），再 $\hat\gamma$（第二套矩依赖 $\hat e$）。

> **要点：** 这预示了**可行 GMM 的两步结构**——先估参数得残差，再估 $\hat\Omega$。

---

## Exercise 13.2　同方差下 2SLS 的方差 = $\sigma^2(Q'M^{-1}Q)^{-1}$

**证明：** 2SLS 用 $W_n=(Z'Z)^{-1}\to_p M^{-1}=Q_{ZZ}^{-1}$。同方差 $\Omega=E[ZZ'e^2]=\sigma^2 M$。代入一般方差：
$$V=(Q'M^{-1}Q)^{-1}Q'M^{-1}(\sigma^2 M)M^{-1}Q(Q'M^{-1}Q)^{-1}=\sigma^2(Q'M^{-1}Q)^{-1}.\quad□$$

> **要点：** 同方差下 $\Omega\propto M=Q_{ZZ}$，故 $W=M^{-1}$ 恰是最优权——**2SLS 在同方差下就是有效 GMM**。

---

## Exercise 13.3　$\hat W\to_p\Omega^{-1}$（最优权的一致估计）

**证明：** $\tilde e_i=e_i-X_i'(\tilde\beta-\beta)$，$\tilde\beta-\beta=o_p(1)$ ⇒ $n^{-1}\sum Z_iZ_i'\tilde e_i^2\to_p\Omega$（同 Ch7/12 的 $\hat\Omega$ 证明）。连续映射 $\hat W\to_p\Omega^{-1}$。□

---

## Exercise 13.4　最优权 $W=\Omega^{-1}$ 的有效性

**考点：** 本章核心定理（Theorem 13.4）——证明 $V_{\mathrm{eff}}\le V(W)$ 对任意 $W$。

**(a)** $W=\Omega^{-1}$：$V_0=(Q'\Omega^{-1}Q)^{-1}$（肉 $=\Omega$ 与权重 $\Omega^{-1}$ 相消）。

**(b)(c)(d)** 标准分解：令 $A=WQ(Q'WQ)^{-1}$，$B=\Omega^{-1}Q(Q'\Omega^{-1}Q)^{-1}$，则 $V=A'\Omega A$，$V_0=B'\Omega B$，且 $B'\Omega(A-B)=0$。故
$$V-V_0=(A-B)'\Omega(A-B)\ge0\quad(\Omega\ge0).\quad□$$

> **要点（接 Ch4/Ch8）：** 又是"减去一个半正定项"结构——最优权让方差最小。与 Gauss-Markov、有效 MD 同构。

---

## Exercise 13.5–13.9　Theorems 13.8–13.10（Wald、约束 GMM、有效约束方差）

- **13.5（Thm 13.8 Wald）：** $\sqrt n(\hat\theta-\theta_0)\to_d N(0,V_\theta)$ ⇒ $W=n(\hat\theta-\theta_0)'\hat V_\theta^{-1}(\hat\theta-\theta_0)\to_d\chi^2_q$。
- **13.6（约束 GMM (13.16)）：** 在 $R'\beta=c$ 下最小化 $J$，Lagrange 得 $\hat\beta_{\mathrm{cgmm}}=\hat\beta_{\mathrm{gmm}}-(X'ZWZ'X)^{-1}R(R'(X'ZWZ'X)^{-1}R)^{-1}(R'\hat\beta_{\mathrm{gmm}}-c)$（同 Ch8 MD 公式）。
- **13.7：** 有效权下 (13.16)=(13.19)（即有效 MD）。
- **13.8–13.9：** 约束 GMM 渐近方差；有效权下简化为 $V-VR(R'VR)^{-1}R'V$（又减半正定项，同 Ch8）。

> **要点：** 约束 GMM = Ch8 的约束 MD——同一套"投影 + 减半正定项"代数。

---

## Exercise 13.10　非线性 $m(X,\beta)$ 的有效 GMM

**做法（两步可行有效 GMM）：**
1. 初值 $\tilde\beta$（如 2SLS/NLS）；
2. $\hat\Omega=n^{-1}\sum g_i(\tilde\beta)g_i(\tildebeta)'$；
3. $\hat\beta=\arg\min g_n(\beta)'\hat\Omega^{-1}g_n(\beta)$（数值优化）；
4. SE 用 $\hat V=(G'\hat\Omega^{-1}G)^{-1}/n$，$G=n^{-1}\sum\partial g_i/\partial\beta'$。

> **要点：** 非线性矩条件也能用 GMM——这正是 GMM 的普适性（Hansen 1982 的贡献）。

---

## Exercise 13.11　$Z=(X,X^2)$ 的有效 GMM = OLS（续 12.7）

**解答：** $E[e|X]=0$，但 $X$ 是 $Z$ 的精确线性函数 ⇒ 最优 GMM 仍落在 $X$ 方向，**退化为 OLS**。异方差时最优工具是 $X/\sigma^2(X)$，一般**不是** $(X,X^2)$ 的 GMM。

> **要点：** 工具"多"不代表"有用"——若新工具不带来新的、与内生部分相关的变异，有效 GMM 不会用它。

---

## Exercise 13.12　距离统计量 $D$ = Wald（线性假设）

**(a)** $J(\beta)=n(\beta-\hat\beta)'\hat V_\beta^{-1}(\beta-\hat\beta)$（改写为 Wald 形式），故约束 GMM = 最小距离估计（Ch8）。

**(b)** 线性约束下，$D=J(\tilde\beta)$（约束处目标值）= **Wald 统计量**（Ch8/9 标准代数）。

> **要点：** GMM 的三检验（Wald / 距离 $D$ / LM）在线性、有效权下数值等价——与 Ch9 的 trinity 同构。

---

## Exercise 13.13　$J\to_d\chi^2_{\ell-k}$（过度识别检验，逐步证明）

**考点：** Hansen $J$ 检验的分布推导——本章最重要的检验。

**证明思路（7 步）：**
- (a) $\Omega>0$ ⇒ $\Omega^{-1}=CC'$。
- (b) $J=n(C'g_n)'(C'\hat\Omega C)^{-1}C'g_n$。
- (c)(d) GMM FOC 使 $C'g_n(\hat\beta)=D_n C'g_n(\beta)$，$D_n\to_p P:=I-R(R'R)^{-1}R'$（投影阵）。
- (e) $\sqrt n C'g_n(\beta)\to_d u\sim N(0,I_\ell)$（白化后标准正态）。
- (f) $J\to_d u'Pu$。
- (g) $P$ 幂等、秩 $\ell-k$ ⇒ $u'Pu\sim\chi^2_{\ell-k}$。□

> **要点：** $J$ 检验的是 $\ell-k$ 个**过度识别约束**——多出来的矩条件是否成立（工具有效性）。恰好识别（$\ell=k$）时 $J\equiv0$，**无法**检验（13.22）。

---

## Exercise 13.14　$J(\beta_0)$ 检验（固定 $\beta$）

**(a)** $H_0:\beta=\beta_0$ 下 $J(\beta_0)$ → 加权 $\chi^2$（依赖 $W,\Omega$）。
**(b)** 有效权 $W=\Omega^{-1}$ 时 $J(\beta_0)\to_d\chi^2_\ell$（$\ell$ 个矩、无估参数）。
**(d)** 拒绝若 $J(\beta_0)>\chi^2_{\ell,1-\alpha}$。
**(e)** 置信域 $\{\beta:J(\beta)\le c\}$ 是水平集（线性时椭圆）。

---

## Exercise 13.15–13.21　约束、局部误设、加权平均

- **13.15：** $R'\beta=0$ 的有效 GMM：无约束 $\hat\beta$ 再 (13.19) 投影；方差 $V-VR(R'VR)^{-1}R'V$。
- **13.16（局部误设）：** $E[Ze]=\delta/\sqrt n$（局部偏离）⇒ $\sqrt n(\hat\beta-\beta)$ 极限为**非中心正态**（局部偏倚 $(Q'WQ)^{-1}Q'W\mu_Z\delta$）。
- **13.17–13.21：** 各种矩条件的有效 GMM；分块权时为信息矩阵加权平均。

> **要点（13.16）：** 局部误设下 GMM 估计量**有偏**但偏倚可控——这是用 $J$ 检验检测模型误设的理论基础。

---

## Exercise 13.22　恰好识别下三种检验的可用性

恰好识别 $\ell=k$：
- **Wald：** 可行。
- **距离 $D=J_c-J_u$：** $J_u\equiv0$（恰好识别），$D=J_c$，可行。
- **过度识别 $J$：** $J\equiv0$，**无法**检验过度识别。

> **要点：** 恰好识别**没有**过度识别约束可检验（$\ell-k=0$）——要用 $J$ 检验工具外生性，**必须过度识别**。

---

## Exercise 13.23–13.26　矩个数陷阱

- **13.23：** $\beta=Q\theta$ 重参数化，对 $X^*=Q'X$ 做有效 GMM。
- **13.24：** $Y=\theta+e$，$k+1$ 矩 1 参数 ⇒ 过度识别，$J\to\chi^2_k$。
- **13.25–13.26（陷阱）：** 矩个数 $\ell$ 随 $n$ 增（如 $\ell=n$ 个 $E[e_i]=0$）⇒ **GMM 理论不适用**（$J$ 不服从固定 $\ell$ 的 $\chi^2$）。定理 13.14 要求 $\ell$ **固定**。

> **要点：** GMM 的 $J\to\chi^2_{\ell-k}$ 要求矩个数 $\ell$ **固定**（不随 $n$ 增）。把每个观测当一个矩是误用。

---

## Exercise 13.27（AJR）　有效 GMM（续 12.23）

工具 $Z=(1,\log\mathrm{mort},(\log\mathrm{mort})^2)$；内生 risk。

| | risk | intercept |
|--|-----:|----------:|
| 2SLS | 0.772 | 3.019 |
| **两步 EGMM** | **0.728** | **3.336** |

**(b)** $J\approx4.02$，$\chi^2_1$，$p\approx0.045$：过度识别**边缘拒绝**。
**(c)** EGMM 与 2SLS 接近；异方差有效加权使点估计略移。$J$ 提示工具/设定需谨慎。

---

## Exercise 13.28（Card）　有效 GMM

`nearc4a, nearc4b` 工具，$n\approx3010$。

| | edu 系数 | SE |
|--|--------:|---:|
| 2SLS | 0.161 | 0.040 |
| EGMM | 0.162 | 0.040 |

**(a)(b)** 结果**几乎不变**（工具不多、异方差加权影响小）。
**(c)** $J\approx0.87$，$\mathrm{df}=1$，$p\approx0.35$：**不拒绝**过度识别（工具外生性支持）。

> **和本科对照：** 实证中**报告有效 GMM + $J$ 检验**是标准做法。$J$ 不显著 ⇒ 工具外生性支持（如 Card）；$J$ 显著 ⇒ 某工具可能违反排除约束（如 AJR 边缘）。

---

## 附录 A：GMM 统一视角

| 估计量 | 矩条件 | 权重 | 渐近方差 |
|---|---|---|---|
| OLS | $E[Xe]=0$ | $(X'X)^{-1}$ | $\sigma^2(E[XX'])^{-1}$（同方差） |
| 2SLS | $E[Ze]=0$ | $(Z'Z)^{-1}$ | $\sigma^2(Q'M^{-1}Q)^{-1}$（同方差最优） |
| 有效 GMM | $E[Ze]=0$ | $\Omega^{-1}$ | $(Q'\Omega^{-1}Q)^{-1}$（**任意**最优） |

**一句话：** GMM 是统一框架，OLS/2SLS 是特例；有效 GMM（$W=\Omega^{-1}$）是最优的，2SLS 仅在同方差下达到有效 GMM。

---

## 附录 B：$J$ 检验速查

| 情形 | $J$ 分布 | 检验什么 |
|---|---|---|
| 过度识别 $\ell>k$，$H_0:E[Ze]=0$ | $\chi^2_{\ell-k}$ | $\ell-k$ 个过度识别约束（工具外生性） |
| 恰好识别 $\ell=k$ | $\equiv0$ | **无法**检验 |
| 固定 $\beta=\beta_0$ | $\chi^2_\ell$（有效权） | $\beta=\beta_0$ |

**已验证：** $\ell=4,k=2$，$H_0$ 真 ⇒ $J\approx\chi^2_2$（size≈0.02–0.05，两步 GMM 有限样本略低）；让某工具直接进 $Y$（违反排除）⇒ $J=12.7$（$p=0.002$）拒绝。

---

## 附录 C：notebook 单元对应

| 习题 | notebook 内容 |
|------|----------------|
| 13.27 | AJR 两步有效 GMM + $J$ code cell |
| 13.28 | Card 两步有效 GMM + $J$ code cell |
| 理论验证 | 蒙特卡洛：有效 GMM≤2SLS、$J$ 的 size 与功效、同方差等价 code cell |
