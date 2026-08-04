# Bruce Hansen《Econometrics》第 5 章习题解答（详细注释版）

**章节：** Chapter 5 Normal Regression
**出版版：** `hansen/manuscripts/Econometrics_Fullbook.pdf`，PDF 第 189–193 页（印刷页 154–158），§5.15 Exercises（**5.1–5.12 全部**）
**数值验证：** `Hansen_Ch05_Exercises_Solutions.ipynb`（Exercise 5.1 有可运行模拟）

> **写给谁看：** 假设你学过李子奈/陈强，知道"在经典假定（含正态性）下，$t$ 统计量服从 $t$ 分布、$F$ 统计量服从 $F$ 分布"，但对**为什么是这些分布**、**正态性到底扮演什么角色**理得不够清。
> Hansen 第 5 章做的事情：在**正态误差**假设 $e\mid X\sim N(0,\sigma^2 I)$ 下，推出 $\hat\beta$、残差、$s^2$、$t$、$F$、LR 的**精确有限样本分布**。本章是"把第 4 章只给了前两阶矩的 $\hat\beta$，升级成完整的概率分布"。

---

## 0. 读题前必看：本章到底在讲什么

**承上启下：**
- 第 4 章在很弱的假设下（$E[e|X]=0$）证明了 $\hat\beta$ **无偏**，并给出它的**方差**（夹心公式）——但只有前两阶矩，不知道完整分布。
- 第 5 章加上**最强**的假设——**误差正态** $e\mid X\sim N(0,\sigma^2 I)$——换取**完整的精确分布**：$\hat\beta\mid X\sim N$、$T\sim t_{n-k}$、$F\sim F_{q,n-k}$。
- 第 7 章会"还债"：**去掉正态性**，用大数定律/中心极限定理把同样的 $t$、$F$ 检验在**大样本下**重新建立起来（渐近分布）。

**正态性的代价与回报（务必记住）：**
- **代价**：正态误差是个**很强、通常不现实**的假设（经济数据很少严格正态）。
- **回报**：得到**精确的有限样本**分布（小样本也准），而不只是大样本近似。

> **和本科对照：** 李子奈在"经典假定"下推导 $t$、$F$ 检验——其中就包含"误差正态"。陈强进一步指出：现代实证多不用正态假定，而靠大样本（稳健 $t$）。**Hansen 把这件事讲透：正态性是"花钱买精确分布"，不花钱就只能要渐近分布（Ch7）。**

**本章的四个核心工具（90% 的题靠它们）：**

1. **正态的线性变换仍是正态**：若 $e\sim N(0,\Sigma)$，则 $Ae\sim N(0,A\Sigma A')$。
   → 一举推出 $\hat\beta=(X'X)^{-1}X'e$、$\hat e=Me$、$\hat Y=PY$ 的分布（它们都是 $e$ 的线性函数）。
2. **联合正态下"不相关 ⟺ 独立"**（正态**独有**，一般不成立——回顾 Ch2"均值独立≠独立"！）。
   → 由 $X'M=0$（系数方向 ⊥ 残差空间）推出 $\hat\beta\perp\hat e$，进而 $\hat\beta\perp s^2$、$\hat\beta\perp$ 任何 HC 矩阵。
3. **幂等二次型 ⟹ 卡方**：若 $Z\sim N(0,I)$、$A$ 幂等秩 $r$，则 $Z'AZ\sim\chi^2_r$。
   → 推出 $(n-k)s^2/\sigma^2\sim\chi^2_{n-k}$。
4. **比值构造 $t$、$F$**：$t=\frac{N(0,1)}{\sqrt{\chi^2_\nu/\nu}}$；$F=\frac{\chi^2_q/q}{\chi^2_\nu/\nu}$（分子分母**独立**时）。
   → 这就是 $t$、$F$ 分布的来源。

---

## 1. 记号与概念速查（对照李子奈/陈强）

| Hansen 记号 | 中文/本科说法 | 一句话解释 |
|---|---|---|
| $e\mid X\sim N(0,\sigma^2 I_n)$ | 正态回归模型 | 误差独立同分布正态（同方差+正态） |
| $\hat\beta\mid X\sim N(\beta,\sigma^2(X'X)^{-1})$ | OLS 的精确分布 | Theorem 5.4；线性函数 of 正态 |
| $\hat e\mid X\sim N(0,\sigma^2 M)$ | 残差的精确分布 | Theorem 5.6；$M$ 幂等 |
| $\hat\beta\perp\hat e\mid X$ | 系数与残差独立 | 不相关+正态 ⟹ 独立（因 $X'M=0$） |
| $(n-k)s^2/\sigma^2\sim\chi^2_{n-k}$ | 方差估计的分布 | Theorem 5.7；幂等二次型 |
| $T=\frac{\hat\beta_j-\beta_j}{s(\hat\beta_j)}\sim t_{n-k}$ | $t$ 统计量 | Theorem 5.8；**仅限同方差 SE** |
| $F=\frac{(SSE_R-SSE_U)/q}{SSE_U/(n-k)}\sim F_{q,n-k}$ | $F$ 统计量 | Theorem 5.13；排除性约束检验 |
| $LR=2(\ell_U-\ell_R)$ | 似然比统计量 | (5.18)；渐近 $\chi^2_q$ |
| CRLB $\sigma^2(X'X)^{-1}$ | Cramér–Rao 下界 | OLS 的 β̂ 达到此界（有效） |

**最常用的"线性变换方差"公式（反复用）：** 若 $u=Ae$，$e\sim N(0,\Sigma)$，则 $u\sim N(0,A\Sigma A')$。本章几乎每题都是"写出统计量 = $e$ 的某线性变换 → 套这个公式"。

---

## 2. 预备记号

正态回归模型：$Y=X\beta+e$，$e\mid X\sim N(0,\sigma^2 I_n)$（即独立、同方差、正态）。
OLS：$\hat\beta=(X'X)^{-1}X'Y$，残差 $\hat e=MY$，$M=I-X(X'X)^{-1}X'$（Ch3 的零化矩阵，幂等）。
杠杆值 $h_{ii}=X_i'(X'X)^{-1}X_i$。无偏方差估计 $s^2=\frac1{n-k}\sum\hat e_i^2$（(4.26)）。
留一残差 $\tilde e=M^*\hat e$（(3.45)），标准化残差 $\bar e$（(4.24)）——都是 $\hat e$ 的线性函数。

---

## Exercise 5.1　$\chi^2_r$ 的均值与方差

**题：** $Q\sim\chi^2_r$，证 $E[Q]=r$，$\mathrm{var}(Q)=2r$。

**考点：** $\chi^2$ 分布最基础的矩，是 $s^2$ 的分布（Theorem 5.7）和 $t$、$F$ 的基石。

**证明（用定义 $Q=\sum_{j=1}^r Z_j^2$，$Z_j\stackrel{iid}{\sim}N(0,1)$）：**

**均值：** $E[Z_j^2]=\mathrm{var}(Z_j)+(E[Z_j])^2=1+0=1$（标准正态方差为 1，均值为 0）。故
$$E[Q]=\sum_{j=1}^r E[Z_j^2]=r.$$

**方差：** 需要 $Z_j$ 的**四阶矩**。标准正态 $E[Z^4]=3$（正态峰度为 3，故四阶矩 $=3$）。于是
$$\mathrm{var}(Z_j^2)=E[Z_j^4]-(E[Z_j^2])^2=3-1^2=2.$$
由 $Z_j$ **独立**（方差可加）：
$$\mathrm{var}(Q)=\sum_{j=1}^r\mathrm{var}(Z_j^2)=2r.$$

> **记忆：** $\chi^2_r$ 的均值 $=$ 自由度 $r$，方差 $=2r$。后面 5.12 直接用：$(n-k)s^2/\sigma^2\sim\chi^2_{n-k}$ ⇒ $\mathrm{var}(s^2)=2\sigma^4/(n-k)$。

---

## Exercise 5.2　正交变换保持 $N(0,\sigma^2 I)$

**题：** $e\sim N(0,I_n\sigma^2)$，$H'H=I_n$（$H$ 正交）。证 $u=H'e\sim N(0,I_n\sigma^2)$。

**考点：** 工具 1（正态的线性变换仍是正态）+ 正交变换不改变 $N(0,\sigma^2 I)$。

**证明：**
- **正态性**：$u=H'e$ 是 $e$ 的线性函数，$e$ 正态 ⇒ $u$ 正态。
- **均值**：$E[u]=H'E[e]=0$。
- **方差**：$\mathrm{var}(u)=H'\mathrm{var}(e)H=H'(\sigma^2 I_n)H=\sigma^2 H'H=\sigma^2 I_n$（用 $H'H=I$）。

> **用途：** 这是 Theorem 5.7（$s^2$ 的分布）证明的关键一步——用谱分解 $M=H\Lambda H'$ 把 $M$ 对角化，$u=H'e$ 把误差"旋转"到 $M$ 对角的主轴系，化简二次型 $e'Me$。

---

## Exercise 5.3　"白化"变换：$e\sim N(0,\Sigma)\Rightarrow A^{-1}e\sim N(0,I)$

**题：** $e\sim N(0,\Sigma)$，$\Sigma=AA'$。证 $u=A^{-1}e\sim N(0,I_n)$。

**考点：** 工具 1。这是"球化/白化"（whitening）——把相关/异方差的正态变成独立标准正态。

**证明：**
- $u=A^{-1}e$ 是 $e$ 的线性函数 ⇒ 正态。
- $E[u]=A^{-1}E[e]=0$。
- $\mathrm{var}(u)=A^{-1}\Sigma(A^{-1})'=A^{-1}AA'A^{-1'}=(A^{-1}A)(A^{-1}A)'=I\cdot I'=I_n$（用 $\Sigma=AA'$）。

> **和本科对照：** 这正是 Ch4 GLS 的几何——预乘 $\Sigma^{-1/2}=A^{-1}$ 把"椭圆"误差（相关/异方差）拉成"圆球"（独立同方差）。在正态下，它把一般正态变成标准正态，从而能用 $\chi^2$ 工具。

---

## Exercise 5.4　似然与对数似然有相同的最大点

**题：** 证 $\arg\max_\theta\ell_n(\theta)=\arg\max_\theta L_n(\theta)$。

**考点：** 为什么实际中总是最大化**对数**似然而非似然。

**证明：** $\ell_n=\log L_n$，对数是**严格单调递增**函数。故 $L_n(\theta_1)>L_n(\theta_2)\Leftrightarrow\log L_n(\theta_1)>\log L_n(\theta_2)$，排序不变 ⇒ 最大点相同。

> **和本科对照：** 陈强讲 MLE 时总用对数似然，原因：(1) 乘积变求和（$L=\prod f_i\Rightarrow\ell=\sum\log f_i$），导数好算；(2) 数值上避免下溢（许多小概率相乘→0）；(3) 渐近理论（CLT 作用于 $\sum\log f_i$）天然适用。本题确认这样做不改变估计量。

---

## Exercise 5.5　拟合值的分布 $\hat Y_i\mid X\sim N(X_i'\beta,\sigma^2 h_{ii})$

**考点：** 工具 1。$\hat Y_i$ 是 $\hat\beta$ 的线性函数，$\hat\beta$ 正态 ⇒ $\hat Y_i$ 正态，方差含杠杆值。

**证明：** $\hat Y_i=X_i'\hat\beta$（$X_i$ 给定，视作常数向量）。$\hat\beta\mid X\sim N(\beta,\sigma^2(X'X)^{-1})$（Theorem 5.4），故线性变换
$$\hat Y_i\mid X\sim N\big(X_i'\beta,\;X_i'\,\sigma^2(X'X)^{-1}\,X_i\big)=N(X_i'\beta,\sigma^2 h_{ii}).$$
（用了 $h_{ii}=X_i'(X'X)^{-1}X_i$。）

> **和本科对照：** 回归线在 $X_i$ 处的**预测方差**是 $\sigma^2 h_{ii}$——**高杠杆点**（$h_{ii}$ 大）的拟合值更不确定。这就是为什么预测区间/置信带在极端 $X$ 处变宽（喇叭形）。杠杆值同时影响：拟合值方差（5.5）、残差方差（Ch4：$E[\hat e_i^2|X]=\sigma^2(1-h_{ii})$）、留一残差（Ch3：$\tilde e_i=\hat e_i/(1-h_{ii})$）、HC2/HC3 权重——一根线串起多章。

---

## Exercise 5.6　留一残差、标准化残差与 $\hat\beta$ 独立

**考点：** 工具 2（联合正态下不相关 ⟹ 独立）。提示用 (3.45)（$\tilde e=M^*\hat e$）和 (4.24)（标准化残差）。

**证明思路：**
- 留一残差 $\tilde e=M^*\hat e$（(3.45)，$M^*=\mathrm{diag}((1-h_{ii})^{-1})$）和标准化残差 $\bar e$（(4.24)）都是 **$\hat e$ 的线性函数**（因而也是误差 $e$ 的线性函数）。
- $\hat\beta-\beta=(X'X)^{-1}X'e$ 也是 $e$ 的线性函数。
- 所以 $(\hat\beta,\tilde e)$（或 $(\hat\beta,\bar e)$）**联合正态**。算它们的协方差：涉及 $\mathrm{cov}(\hat\beta,\hat e)=(X'X)^{-1}X'E[ee'|X]M'=\sigma^2(X'X)^{-1}\underbrace{X'M}_{=0}=0$（用 Ch3 的 $X'M=0$；类似地 $X'M^*=0$ 因 $M^*$ 是 $M$ 的对角函数）。
- **协方差为 0 + 联合正态 ⟹ 独立**。

> **和本科对照：** 这把 Ch3 的几何事实"系数方向 ⊥ 残差空间"（$X'M=0$，纯代数）升级为**统计独立**（正态的功劳）。意义：残差的各种变换（留一、标准化）不携带关于 $\beta$ 的信息，可以"分开看"。

---

## Exercise 5.7　HC 协方差矩阵与 $\hat\beta$ 独立

**考点：** 工具 2 的延伸——HC0–HC3 都是残差向量的函数，故与 $\hat\beta$ 独立。

**证明：** HC 矩阵是 $\hat e_i^2$（HC0–HC3）或 $\tilde e_i^2$ 的函数（见 Ch4，"肉"$=\sum X_iX_i'\hat e_i^2 c_i$），即**残差向量的函数**。由 Theorem 5.6，$\hat e\perp\hat\beta\mid X$。**独立的随机变量的任何函数仍独立**，故 HC 矩阵 $\perp\hat\beta\mid X$。

> **重要警示（书上 §5.9 强调）：** 虽然 $\hat\beta$ 与稳健 SE 独立，但**稳健 $t$ 统计量 $\hat\beta_j/\sqrt{HC}$ 并不服从精确 $t$ 分布**——因为分母虽与分子独立，却不是干净的 $\chi^2$（它是异方差加权和）。**精确 $t$ 只对同方差 SE 成立**。稳健 $t$ 的大样本合法性要等到 Ch7。这就是为什么"正态 + 同方差"是 $t$ 检验精确性的两块基石。

---

## Exercise 5.8　对称分布：$F(-u)=1-F(u)$

**考点：** 对称密度的基本性质，给出双侧 $p$ 值公式。

**证明：** 密度关于 0 对称 ⇒ $P(X\le-u)=P(X\ge u)$。对**连续**分布 $F$：
$$F(-u)=P(X\le-u)=P(X\ge u)=1-P(X<u)=1-F(u)$$
（连续性使 $P(X<u)=P(X\le u)=F(u)$）。

> **和本科对照：** 标准正态、$t$、均匀、Cauchy 都对称。这给出双侧检验 $p$ 值 $=2(1-F(|T|))$，以及"对称置信区间" $\hat\beta\pm c\cdot\mathrm{SE}$。

---

## Exercise 5.9　单调变换保持置信区间的覆盖概率

**题：** $\hat C_\beta=[L,U]$ 是 $\beta$ 的 $1-\alpha$ CI，$\theta=g(\beta)$，$g$ 严格递增。$\hat C_\theta=[g(L),g(U)]$。证 $P(\theta\in\hat C_\theta)=P(\beta\in\hat C_\beta)$。并据此构造 $\sigma$ 的 CI。

**考点：** 覆盖概率在单调重参数化下不变。

**证明：** $g$ 严格递增 ⇒ $\beta\in[L,U]\Leftrightarrow g(\beta)\in[g(L),g(U)]$（两端点同时变换，包含关系不变）。故两个事件等价，概率相同：
$$P(\theta\in\hat C_\theta)=P(g(\beta)\in[g(L),g(U)])=P(\beta\in[L,U])=1-\alpha.$$

**构造 $\sigma$ 的 CI：** 取 $g(\cdot)=\sqrt{\cdot}$（严格递增，作用于 $\sigma^2\to\sigma$）。若 $[L,U]$ 是 $\sigma^2$ 的 CI（由 $(n-k)s^2/\sigma^2\sim\chi^2_{n-k}$ 构造），则 $[\sqrt L,\sqrt U]$ 是 $\sigma$ 的 CI，覆盖概率同为 $1-\alpha$。

> **和本科对照：** "先对 $\sigma^2$ 做 CI，再开方"得到 $\sigma$ 的 CI——这在陈强/李子奈里是标准操作。本题给出其理论依据：**单调变换保持覆盖**。对递减变换则要把端点交换。

---

## Exercise 5.10　LR 检验与 $F$ 检验的决策等价性

**题：** "拒绝若 $LR\ge c_1$"（(5.18)）与"拒绝若 $F\ge c_2$"（(5.19)）在 $c_2=(e^{c_1/n}-1)(n-k)/q$ 时决策相同。二者是否等价？

**考点：** LR 与 $F$ 是**严格单调**变换关系，故拒绝域可对齐。

**证明：** 在正态回归中，$LR=n\log(SSE_R/SSE_U)$（(5.18)，两次对数似然之差），$F=\frac{(SSE_R-SSE_U)/q}{SSE_U/(n-k)}$（(5.19)）。两者关系：
$$F=\frac{(SSE_R/SSE_U-1)(n-k)}{q}=\frac{(e^{LR/n}-1)(n-k)}{q}.$$
这是 $LR$ 的**严格递增**函数。故 $LR\ge c_1\Leftrightarrow F\ge c_2$（$c_2$ 即上式取 $LR=c_1$）——**拒绝域完全相同** ⇒ 决策相同。

**是否"等价"？** 决策（在同一临界值匹配下）相同，但**两者不同**：
- $F$ 在正态下有**精确** $F_{q,n-k}$ 零分布（Theorem 5.13）；
- $LR$ 的零分布是**渐近** $\chi^2_q$（大样本），有限样本下与 $\chi^2$ 有偏差。
- 大样本下 $F_{q,n-k}\to\chi^2_q/q$，二者趋同。

> **和本科对照：** 陈强讲三大检验 LR / Wald / LM（都渐近 $\chi^2$），以及精确的 $F$/$t$。本题说明：在正态模型里，排除性约束既可用 $F$（精确）也可用 LR（渐近），决策可对齐。实践中大样本用 LR/Wald，小样本正态用 $F$/$t$。

---

## Exercise 5.11　信息矩阵 (5.20)

**考点：** 正态回归的对数似然得分（score）的方差 = 信息矩阵。关键是 β 与 σ² "**正交**"（信息阵对角块）。

**铺垫：** 正态回归对数似然 $\ell=-\frac n2\log(2\pi\sigma^2)-\frac1{2\sigma^2}\sum e_i^2$。得分（对参数的偏导）：
$$s_\beta=\frac{\partial\ell}{\partial\beta}=\frac1{\sigma^2}\sum_{i=1}^n X_ie_i=\frac1{\sigma^2}X'e,\qquad s_{\sigma^2}=\frac{\partial\ell}{\partial\sigma^2}=\frac1{2\sigma^4}\sum_{i=1}^n(e_i^2-\sigma^2).$$
信息矩阵 $I=\mathrm{var}\big[(s_\beta',s_{\sigma^2})'\mid X\big]$（因 $E[\text{score}]=0$，方差 = 信息）。

**证明：**

**(1) $\mathrm{var}(s_\beta|X)$：**
$$\mathrm{var}(s_\beta|X)=\frac1{\sigma^4}X'\underbrace{\mathrm{var}(e|X)}_{=\sigma^2 I}X=\frac1{\sigma^2}X'X.\quad\checkmark$$

**(2) $\mathrm{var}(s_{\sigma^2}|X)$：** $e_i\sim N(0,\sigma^2)$ ⇒ $e_i^2/\sigma^2\sim\chi^2_1$ ⇒ $\mathrm{var}(e_i^2)=2\sigma^4$（用 Ex 5.1）。独立 ⇒ 方差相加：
$$\mathrm{var}(s_{\sigma^2}|X)=\frac1{4\sigma^8}\sum_i\mathrm{var}(e_i^2)=\frac1{4\sigma^8}\cdot n\cdot 2\sigma^4=\frac{n}{2\sigma^4}.\quad\checkmark$$

**(3) 交叉项 $E[s_\beta s_{\sigma^2}|X]=0$：**
$$E[s_\beta s_{\sigma^2}|X]\propto\sum_i X_i\,E\big[e_i(e_i^2-\sigma^2)\big].$$
正态的**奇数阶矩为 0**：$E[e_i^3]=0$，且 $E[e_i]=0$，故 $E[e_i(e_i^2-\sigma^2)]=E[e_i^3]-\sigma^2E[e_i]=0-0=0$。交叉项消失。

合起来：
$$I=\begin{pmatrix}\frac1{\sigma^2}X'X&0\\0&\frac{n}{2\sigma^4}\end{pmatrix}.\qquad\checkmark$$

> **和本科对照：** 信息阵**对角**意味着 β 与 σ² "**正交**"——估计其中一个不增进/损害另一个的信息。CRLB $=I^{-1}$ 给出 β 的下界 $\sigma^2(X'X)^{-1}$（恰为 OLS 方差 ⇒ **OLS 对 β 是 Cramér–Rao 有效的**，比 Gauss–Markov 更强：在**所有**无偏估计里最优，不止线性），σ² 的下界 $2\sigma^4/n$。

---

## Exercise 5.12　$\mathrm{var}(s^2)=2\sigma^4/(n-k)$，且大于 CRLB

**题：** $s^2=\frac1{n-k}\sum\hat e_i^2$（(4.26)，无偏）。(a) 证 $\mathrm{var}(s^2)=2\sigma^4/(n-k)$；(b) 证它严格大于 σ² 的 CRLB。

**考点：** 用 Theorem 5.7（$(n-k)s^2/\sigma^2\sim\chi^2_{n-k}$）+ Ex 5.1。

**(a) 证明：** 由 Theorem 5.7，$W:=\frac{(n-k)s^2}{\sigma^2}\sim\chi^2_{n-k}$。用 Ex 5.1，$\mathrm{var}(W)=2(n-k)$。而 $\mathrm{var}(W)=\frac{(n-k)^2}{\sigma^4}\mathrm{var}(s^2)$，故
$$\mathrm{var}(s^2)=\frac{2(n-k)\sigma^4}{(n-k)^2}=\frac{2\sigma^4}{n-k}.\quad\checkmark$$

**(b) 与 CRLB 比较：** σ² 的 CRLB 是 $2\sigma^4/n$（(5.20) 之逆的右下块）。因 $n-k<n$，
$$\mathrm{var}(s^2)=\frac{2\sigma^4}{n-k}>\frac{2\sigma^4}{n}=\text{CRLB}.$$
故 $s^2$ **无偏但非 Cramér–Rao 有效**。

> **和本科对照（重要对比）：**
> - **β̂（OLS）达到 CRLB**（对 β 有效）——因为估计 β 时"顺便"用了全部信息。
> - **$s^2$ 达不到 CRLB**——因为它用了 $n-k$ 个自由度（先花掉 $k$ 个去估 β）。
> - **MLE** $\hat\sigma^2_{\text{MLE}}=\frac1n\sum\hat e_i^2$（除以 $n$）**有偏**（偏小 $(n-k)/n$ 倍），但方差**更小**、更接近 CRLB。这是 σ² 估计的**偏差-方差权衡**：$s^2$ 无偏但方差大，MLE 方差小但有偏。

---

## 附录 A：正态回归的精确分布总表

| 量 | 分布（给定 $X$） | 来源工具 |
|---|---|---|
| $\hat\beta$ | $N(\beta,\sigma^2(X'X)^{-1})$ | 线性 of 正态（Thm 5.4） |
| $\hat Y_i=X_i'\hat\beta$ | $N(X_i'\beta,\sigma^2 h_{ii})$ | 同上（Ex 5.5） |
| $\hat e=Me$ | $N(0,\sigma^2 M)$ | 线性 of 正态（Thm 5.6） |
| $\hat\beta$ 与 $\hat e$ | **独立** | 不相关+正态（$X'M=0$） |
| $(n-k)s^2/\sigma^2$ | $\chi^2_{n-k}$ | 幂等二次型（Thm 5.7） |
| $T=\frac{\hat\beta_j-\beta_j}{s(\hat\beta_j)}$ | $t_{n-k}$ | $N/\sqrt{\chi^2/\nu}$，**仅同方差 SE**（Thm 5.8） |
| $F$（排除性约束） | $F_{q,n-k}$ | $(\chi^2_q/q)/(\chi^2_\nu/\nu)$（Thm 5.13） |

**关键提醒：** 上表的**精确性依赖两条**——(1) 误差正态；(2) 用**同方差** SE。去掉任一条，都只能退到 Ch7 的**渐近**结果。

---

## 附录 B：正态回归 vs 大样本（第 7 章预告）

| | 第 5 章（正态回归） | 第 7 章（渐近） |
|---|---|---|
| 假设 | 误差**正态** + 同方差 | 仅 $E[e|X]=0$ + 矩条件 |
| $\hat\beta$ 分布 | 精确正态 | **渐近**正态（CLT） |
| $t$ 检验 | 精确 $t_{n-k}$（同方差 SE） | 渐近 $N(0,1)$（可用稳健 SE） |
| $F$ 检验 | 精确 $F_{q,n-k}$ | 渐近 $\chi^2_q$（Wald/LR/LM） |
| 适用 | 小样本、误差近正态 | 大样本、任意分布 |

**一句话：** 第 5 章"花钱（正态假定）买精确分布"；第 7 章"不花钱，靠样本量 $n\to\infty$ 换渐近分布"。现代实证多走第 7 章路线（稳健推断），但理解第 5 章是理解"经典 $t$/$F$ 从哪来"的必经之路。

---

## 附录 C：notebook 单元对应

| 习题 | notebook 内容 |
|------|----------------|
| 5.1 | $\chi^2_r$ 的均值/方差模拟 code cell |
| 5.2–5.12 | 证明，详见本 .md |
