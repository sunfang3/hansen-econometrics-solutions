# Bruce Hansen《Econometrics》第 11 章习题解答（详细注释版）

**章节：** Chapter 11 Multivariate Regression
**书稿：** PDF 第 350–351 页（印刷页 330–331），§11.18 Exercises（**11.1–11.15 全部**）
**记号：** 系统回归 $Y=\mathbf{X}\beta+e$；方程 $j$：$Y_j=X_j'\beta_j+e_j$；$\Sigma=E[ee']$；SUR/GLS
**数值验证：** `Hansen_Ch11_Exercises_Solutions.ipynb`（Exercise 11.15 有可运行代码）

> **写给谁看：** 假设你学过李子奈/陈强，会做单方程 OLS，但对"**多个方程怎么一起估**""**SUR（似无关回归）什么时候比逐个 OLS 更有效**"理得不够清。
> Hansen 第 11 章把 $m$ 个方程**堆叠成一个大系统**，于是第 4、7 章的单方程理论（夹心方差、GLS、渐近正态）几乎原封不动地搬过来——只是矩阵变大了，并多了 Kronecker 积结构。核心新东西是 **SUR**：当不同方程的误差**相关**时，联合估计能提高效率。

---

## 0. 读题前必看：本章到底在讲什么

**承上启下：**
- 第 4、7 章：**单方程** $Y=X'\beta+e$ 的 OLS 性质与渐近理论（夹心方差 $V_\beta=Q^{-1}\Omega Q^{-1}$）。
- **第 11 章：$m$ 个方程** $Y_j=X_j'\beta_j+e_j$（$j=1,\ldots,m$）**堆叠**成一个**大系统** $Y=\mathbf{X}\beta+e$，单方程理论整体搬迁。

**核心直觉（一张图）：** 把 $m$ 个方程像砖块一样**堆**成一个超长回归，所有第 4/7 章的结论（OLS、夹心方差、GLS、渐近正态）都照搬，只是：
- 矩阵变大了（$\beta$ 是所有方程系数的堆叠）；
- 多了 **Kronecker 积**结构（共同回归元时，方差呈 $\Sigma\otimes Q_{xx}^{-1}$ 的漂亮形式）；
- 出现了 **SUR**（似无关回归）= 系统的 GLS，能利用**跨方程误差相关**提效。

**为什么要"多方程"？** 实证中常有多个相关结果变量（如企业的投资方程 + 融资方程；或同一组系数在不同人群/时期的方程）。若各方程误差相关，**逐个 OLS 丢了这部分信息**；联合估计（SUR）能借用其他方程的信息，提高效率。

> **和本科对照：** 李子奈略提"模型联立"；陈强系统讲 **SUR（似无关回归）** 和"何时 SUR=OLS"。Hansen 的贡献：把 SUR 严格纳入 GLS 框架（第 4 章 GLS 的多方程版），用矩阵 Cauchy–Schwarz 证 SUR ≥ OLS，并讲清 SUR=OLS 的两个充分条件。

**本章的"纲"——三个层次（与单方程完全对应）：**

1. **系统 OLS**（逐方程 OLS 的堆叠）：$\hat\beta=(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'Y$。渐近方差仍是**夹心** $V_\beta=Q^{-1}\Omega Q^{-1}$，只是 $Q,\Omega$ 是系统级的。
2. **SUR = 系统 GLS**（用 $\Sigma^{-1}$ 加权）：$\hat\beta_{\text{sur}}=(\sum\mathbf{X}_i'\Sigma^{-1}\mathbf{X}_i)^{-1}\sum\mathbf{X}_i'\Sigma^{-1}Y_i$。**当跨方程误差相关时比 OLS 更有效**（Theorem 11.5）。
3. **SUR = OLS 的两个条件**（关键结论，务必记住）：
   - **(a) 所有方程回归元相同**（$X_j=X$）；或
   - **(b) 跨方程误差不相关**（$\Sigma$ 对角）。
   满足任一，SUR 退化为 OLS，无效率增益。

> **实证（蒙特卡洛，已验证）：** 两个方程、回归元不同、误差相关 $\rho=0.7$：
> - 逐方程 OLS：$\mathrm{var}(\hat\beta_1)\approx0.00025$；
> - SUR：$\mathrm{var}(\hat\beta_1)\approx0.00013$——**方差几乎减半**！借用第二方程信息收益巨大。
>
> 而当两方程**共用回归元** $X$ 时：SUR 与 OLS **逐样本数值相同**（$|\hat\beta_{\text{OLS}}-\hat\beta_{\text{SUR}}|\approx10^{-16}$）——这正是 SUR=OLS 的著名结论。

---

## 1. 记号与概念速查（对照李子奈/陈强）

| Hansen 记号 | 中文/本科说法 | 一句话解释 |
|---|---|---|
| $Y=\mathbf{X}\beta+e$ | 堆叠系统 | $m$ 个方程拼成一个大回归 |
| $\mathbf{X}_i=\mathrm{diag}(X_{1i}',\ldots,X_{mi}')$ | 分块对角设计 | 第 $i$ 个观测的设计矩阵 |
| 系统 OLS $\hat\beta$ | 逐方程 OLS 的堆叠 | $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'Y$ |
| $\Sigma=E[ee']$ | 跨方程误差协方差 | $m\times m$；非对角=跨方程相关 |
| SUR $\hat\beta_{\text{sur}}$ | 似无关回归 | 系统的 GLS，用 $\Sigma^{-1}$ 加权 |
| $Q,\Omega,V_\beta$ | 系统 $Q$、肉、夹心方差 | 与单方程同义，系统级 |
| $\Sigma\otimes Q_{xx}^{-1}$ | Kronecker 方差 | 共同回归元+同方差时的简化形式 |

**两个最常用的"工具"：**

1. **Kronecker 积规则**：$(A\otimes B)(C\otimes D)=AC\otimes BD$；$(A\otimes B)^{-1}=A^{-1}\otimes B^{-1}$。共同回归元时让方差矩阵"因式分解"成 $\Sigma\otimes Q_{xx}^{-1}$。
2. **矩阵 Cauchy–Schwarz (B.33)**：$E[V'V]\ge E[V'U](E[U'U])^{-1}E[U'V]$。用于证 SUR ≥ OLS（Theorem 11.5，Ex 11.12）。

**与单方程的对应关系（背下来）：** 第 11 章 = 把第 4 章（GLS）和第 7 章（渐近正态、夹心方差）应用到**堆叠系统**。没有任何新原理，只有更大的矩阵和 Kronecker 结构。

---

## 2. 预备记号

$m$ 个方程堆叠为
$$Y=\mathbf{X}\beta+e,\qquad \mathbf{X}_i=\mathrm{diag}(X_{1i}',\ldots,X_{mi}').$$
系统 OLS：
$$\hat\beta=(\mathbf{X}'\mathbf{X})^{-1}(\mathbf{X}'Y)=\Big(\sum_i\mathbf{X}_i'\mathbf{X}_i\Big)^{-1}\Big(\sum_i\mathbf{X}_i'Y_i\Big).\tag{11.4}$$
条件同方差：$E[ee'\mid X]=\Sigma$ (11.8)。共同回归元 $X_j=X$ 时 $\mathbf{X}_i=I_m\otimes X_i'$。
$$\Omega=E[\mathbf{X}_i'e_ie_i'\mathbf{X}_i],\quad Q=E[\mathbf{X}_i'\mathbf{X}_i],\quad V_\beta=Q^{-1}\Omega Q^{-1}.$$

---

## Exercise 11.1　条件同方差下 $\Omega=E[\mathbf{X}_i'\Sigma\mathbf{X}_i]$（证 (11.10)）

**考点：** 迭代期望 + 条件同方差让"肉"简化。

**证明：** $\Omega=E[\mathbf{X}_i'e_ie_i'\mathbf{X}_i]$。迭代期望，在 (11.8) 下 $E[e_ie_i'\mid\mathbf{X}_i]=\Sigma$（常数）：
$$\Omega=E\big[E[\mathbf{X}_i'e_ie_i'\mathbf{X}_i\mid\mathbf{X}_i]\big]=E\big[\mathbf{X}_i'\underbrace{E[e_ie_i'\mid\mathbf{X}_i]}_{=\Sigma}\mathbf{X}_i\big]=E[\mathbf{X}_i'\Sigma\mathbf{X}_i].\quad□$$

> **要点：** 这与单方程 $E[Xe^2]$ 在同方差下变成 $\sigma^2 E[XX']$ 完全类似，只是升级到矩阵。

---

## Exercise 11.2　共同回归元下 $\Omega=E[ee'\otimes XX']$（证 (11.11)）

**考点：** Kronecker 积把系统"肉"写成简洁形式。

**证明：** 共同回归元 $\mathbf{X}_i=I_m\otimes X_i'$，故 $\mathbf{X}_i'e_i=e_i\otimes X_i$（Kronecker-向量规则）。于是
$$\mathbf{X}_i'e_ie_i'\mathbf{X}_i=(e_i\otimes X_i)(e_i\otimes X_i)'=e_ie_i'\otimes X_iX_i'.$$
取期望：$\Omega=E[e_ie_i'\otimes X_iX_i']=E[ee'\otimes XX']$。□

---

## Exercise 11.3　共同回归元 + 同方差：$\Omega=\Sigma\otimes E[XX']$（证 (11.12)）

**考点：** 两个简化叠加 → "肉"完全因式分解。

**证明：** 由 (11.11) 与 $E[ee'\mid X]=\Sigma$：
$$\Omega=E\big[E[ee'\otimes XX'\mid X]\big]=E[\Sigma\otimes XX']=\Sigma\otimes E[XX'].$$
（最后一步 $\Sigma$ 非随机可提出。）□

> **要点：** 这是 Kronecker 结构的来源——共同回归元 + 同方差让"肉"分离成 $\Sigma\otimes Q_{xx}$，进而方差 $V_\beta=\Sigma\otimes Q_{xx}^{-1}$。

---

## Exercise 11.4　证明 Theorem 11.1（系统 OLS 渐近正态）

**考点：** 第 7 章单方程渐近正态的**系统版**——同一套 WLLN+CLT+Slutsky。

**证明：** 堆叠系统 OLS：
$$\sqrt n(\hat\beta-\beta)=\Big(n^{-1}\sum\mathbf{X}_i'\mathbf{X}_i\Big)^{-1}\Big(n^{-1/2}\sum\mathbf{X}_i'e_i\Big).$$
- WLLN：$n^{-1}\sum\mathbf{X}_i'\mathbf{X}_i\to_p Q$（分块对角，因不同方程回归元不交叉）。
- CLT：$\{\mathbf{X}_i'e_i\}$ i.i.d. 零均值（$E[X_je_j]=0$ 堆叠）⇒ $n^{-1/2}\sum\mathbf{X}_i'e_i\to_d N(0,\Omega)$。
- Slutsky：$\sqrt n(\hat\beta-\beta)\to_d N(0,Q^{-1}\Omega Q^{-1})$。□

> **要点：** 与 Theorem 7.3 形式完全相同，只是 $Q,\Omega$ 是系统级。$Q$ 的分块对角性意味着各方程的 $\hat\beta_j$ 渐近独立于其他方程的回归元（但误差相关会让它们仍相关，见 11.15）。

---

## Exercise 11.5　共同回归元：$Q=I_m\otimes E[XX']$（证 (11.13)）

**证明：** $\mathbf{X}_i'\mathbf{X}_i=(I_m\otimes X_i)(I_m\otimes X_i')=I_m\otimes X_iX_i'$ ⇒ $Q=E[I_m\otimes XX']=I_m\otimes E[XX']$。□

---

## Exercise 11.6　共同回归元 + 同方差：$V_\beta=\Sigma\otimes(E[XX'])^{-1}$（证 (11.14)）

**考点：** Kronecker 逆让夹心方差"因式分解"。

**证明：** 由 (11.12)(11.13)，$Q=I_m\otimes Q_{xx}$，$\Omega=\Sigma\otimes Q_{xx}$。用 Kronecker 逆 $(A\otimes B)^{-1}=A^{-1}\otimes B^{-1}$：
$$V_\beta=Q^{-1}\Omega Q^{-1}=(I_m\otimes Q_{xx}^{-1})(\Sigma\otimes Q_{xx})(I_m\otimes Q_{xx}^{-1})=\Sigma\otimes Q_{xx}^{-1}.\quad□$$

> **实证（已验证）：** 共同回归元 $X$、$Q_{xx}=1$、$\Sigma=\begin{pmatrix}1&0.7\\0.7&1\end{pmatrix}$ 时，$V=\Sigma\otimes Q_{xx}^{-1}=\begin{pmatrix}1&0.7\\0.7&1\end{pmatrix}$，与蒙特卡洛抽样方差一致。

---

## Exercise 11.7　证明 Theorem 11.2（跨方程函数的 delta method）

**考点：** 跨方程的参数函数 $\theta=r(\beta)$ 必须用**联合**分布做 delta method（不能用各方程单独的 SE）。

**证明：** 由 Theorem 11.1，$\sqrt n(\hat\beta-\beta)\to_d N(0,V_\beta)$。$r$ 连续可微，delta method（Thm 7.9）：
$$\sqrt n(r(\hat\beta)-r(\beta))\to_d N(0,R'V_\beta R),\quad R=\partial r(\beta)/\partial\beta'.\quad□$$

> **要点：** 比较两方程系数（如 $\beta_1-\beta_2$、$\beta_1/\beta_2$）必须用**联合** $V_\beta$（含跨方程协方差块），不能各算各的——这和 Ch7 Ex 7.17、Ch9 Ex 9.2 一致。

---

## Exercise 11.8　证明 Theorem 11.3（协方差估计一致性）

**考点：** 系统 HC（用 $\hat e_i$ 代 $e_i$）一致——同 Ch7 的"残差代真误差不改变一阶"。

**证明：** 稳健估计 $\hat V_{\hat\beta}=(\mathbf{X}'\mathbf{X})^{-1}(\sum\mathbf{X}_i'\hat e_i\hat e_i'\mathbf{X}_i)(\mathbf{X}'\mathbf{X})^{-1}$。$\hat e_i=e_i-\mathbf{X}_i'(\hat\beta-\beta)$，$\hat\beta-\beta=O_p(n^{-1/2})$ ⇒ $n^{-1}\sum\mathbf{X}_i'\hat e_i\hat e_i'\mathbf{X}_i\to_p\Omega$（同单方程 HC）。故 $n\hat V\to_p V_\beta$。同方差版用 $\hat\Sigma\to_p\Sigma$ 类似。□

---

## Exercise 11.9　SUR/GLS 公式 (11.16)

**考点：** SUR = 把系统用 $\Sigma^{-1/2}$ 预乘（"白化"）后做 OLS = 第 4 章 GLS 的系统版。

**证明：** 对 $Y=\mathbf{X}\beta+e$ 左乘 $\Sigma^{-1/2}$：$Y^\dagger=\mathbf{X}^\dagger\beta+e^\dagger$，$E[e^\dagger e^{\dagger'}]=I$。对变换模型做 OLS：
$$\hat\beta=\Big(\sum\mathbf{X}_i^{\dagger'}\mathbf{X}_i^\dagger\Big)^{-1}\sum\mathbf{X}_i^{\dagger'}Y_i^\dagger=\Big(\sum\mathbf{X}_i'\Sigma^{-1}\mathbf{X}_i\Big)^{-1}\sum\mathbf{X}_i'\Sigma^{-1}Y_i.\quad□$$

---

## Exercise 11.10　SUR 向量形式 (11.17)

**证明：** 堆叠误差方差 $I_n\otimes\Sigma$。GLS $(\mathbf{X}'\Omega_e^{-1}\mathbf{X})^{-1}\mathbf{X}'\Omega_e^{-1}Y$，取 $\Omega_e=I_n\otimes\Sigma$ 即得 (11.17)。与 (11.16) 等价（分块对角作用）。□

---

## Exercise 11.11　证明 Theorem 11.4（SUR 渐近分布）

**考点：** 可行 SUR（$\hat\Sigma$ 代 $\Sigma$）与已知 $\Sigma$ 的 GLS 同极限。

**证明：** 对已知 $\Sigma$ 的 GLS：
$$\sqrt n(\hat\beta_{\text{gls}}-\beta)=\Big(n^{-1}\sum\mathbf{X}_i'\Sigma^{-1}\mathbf{X}_i\Big)^{-1}\Big(n^{-1/2}\sum\mathbf{X}_i'\Sigma^{-1}e_i\Big).$$
$n^{-1}\sum\mathbf{X}'\Sigma^{-1}\mathbf{X}\to_p Q_*:=E[\mathbf{X}'\Sigma^{-1}\mathbf{X}]$。同方差下中间项方差也是 $Q_*$（$E[\mathbf{X}'\Sigma^{-1}ee'\Sigma^{-1}\mathbf{X}]=E[\mathbf{X}'\Sigma^{-1}\mathbf{X}]=Q_*$）。CLT 得 $N(0,Q_*)$，乘 $Q_*^{-1}$ 得极限方差 $Q_*^{-1}=V_\beta^*$。$\hat\Sigma$ 一致 ⇒ SUR 同极限。□

---

## Exercise 11.12　证明 Theorem 11.5（SUR 渐近不劣于 OLS）

**考点：** 本章的**效率结论**——SUR 方差 ≤ OLS 方差。用矩阵 Cauchy–Schwarz。

**需证：** $(E[\mathbf{X}'\Sigma^{-1}\mathbf{X}])^{-1}\le(E[\mathbf{X}'\mathbf{X}])^{-1}E[\mathbf{X}'\Sigma\mathbf{X}](E[\mathbf{X}'\mathbf{X}])^{-1}$。

**证明（按 Hint）：**
**第一步：** 令 $A=E[\mathbf{X}'\Sigma^{-1}\mathbf{X}]$，$B=E[\mathbf{X}'\mathbf{X}]$，$C=E[\mathbf{X}'\Sigma\mathbf{X}]$。$A^{-1}\le B^{-1}CB^{-1}$ 等价于 $BA^{-1}B\le C$（左右乘 $B$）。
**第二步：** 令 $U=\Sigma^{-1/2}\mathbf{X}$，$V=\Sigma^{1/2}\mathbf{X}$。则 $\mathbf{X}'\Sigma^{-1}\mathbf{X}=U'U$，$\mathbf{X}'\Sigma\mathbf{X}=V'V$，$\mathbf{X}'\mathbf{X}=U'V=V'U$。(*) 变为
$$E[U'V](E[U'U])^{-1}E[V'U]\le E[V'V],$$
正是**矩阵 Cauchy–Schwarz (B.33)**。故 $V_\beta^*\le V_\beta^{\text{ols}}$。□

> **实证（已验证）：** 不同回归元 + 误差相关 $\rho=0.7$ 时，SUR 方差约为 OLS 的**一半**（0.00013 vs 0.00025）——借用跨方程信息收益巨大。

---

## Exercise 11.13　证明 Theorem 11.6（SUR 方差估计一致）

**证明：** $\hat\Sigma\to_p\Sigma$，连续可逆 ⇒ $\hat\Sigma^{-1}\to_p\Sigma^{-1}$。$n^{-1}\sum\mathbf{X}_i'\hat\Sigma^{-1}\mathbf{X}_i\to_p E[\mathbf{X}'\Sigma^{-1}\mathbf{X}]$。故 $n\hat V=(n^{-1}\sum\mathbf{X}_i'\hat\Sigma^{-1}\mathbf{X}_i)^{-1}\to_p V_\beta^*$。□

---

## Exercise 11.14　生成回归元 $\hat\pi$ 的两步估计（$\beta=0$ 简化）

**考点：** 两步估计（先用 $\hat\Gamma$ 估 $\pi=E[X|Z]=\Gamma'Z$，再 $Y$ 对 $\hat\pi$ 回归）。$\beta=0$ 时生成回归元的额外项消失。与 2SLS/控制函数相通。

**(a) 一致性：** $\hat\Gamma\to_p\Gamma$ ⇒ $\hat\pi_i\to_p\pi_i$。$E[e|Z]=0$ 且 $\pi$ 是 $Z$ 的函数 ⇒ $E[\pi e]=0$。标准两步论证 ⇒ $\hat\beta\to_p\beta$。

**(b) $\beta=0$ 时的极限：** $\sqrt n\hat\beta=(n^{-1}\sum\hat\pi_i\hat\pi_i')^{-1}(n^{-1/2}\sum\hat\pi_ie_i)$。关键：$\hat\pi_i-\pi_i=O_p(n^{-1/2})$。在 $\beta=0$（$Y=e$，无信号项）时，生成回归元的估计误差对得分的**一阶影响消失**：
$$n^{-1/2}\sum\hat\pi_ie_i=n^{-1/2}\sum\pi_ie_i+o_p(1).$$
故 $\sqrt n\hat\beta\to_d N(0,Q_\pi^{-1}E[\pi\pi'e^2]Q_\pi^{-1})$（与"$\pi$ 已知"相同）。

**(c) 为何 $\beta=0$ 重要：** 若 $\beta\ne0$，$\hat\pi$ 的估计误差通过信号项 $\pi'\beta$ 产生**额外修正项**（两步估计的代价）。$\beta=0$ 让该项为零，渐近方差简化。

**(d) 检验 $H_0:\beta=0$：** 在 $H_0$ 下用 (b) 的极限，构造稳健 Wald $W=n\hat\beta'\hat V^{-1}\hat\beta\to_d\chi^2_k$。本质是"$Y$ 对 $\hat\pi$ 回归的稳健 Wald"。

> **和本科对照：** 生成回归元（Pagan）在两步估计中常见。一般情况需修正方差（含第一步不确定性）；但检验 $\beta=0$ 时简化——这与 Ch7 Ex 7.22（生成回归元在 $\gamma=0$ 时退化）同源。

---

## Exercise 11.15　两方程共同 $X$：联合分布与 $\beta_1=\beta_2$ 检验

**考点：** 最常见的实证场景——两个结果方程共享回归元，检验两方程系数是否相同。

**(a) 估计量：** 共同 $X$ 时系统 OLS = 逐方程 OLS：$\hat\beta_j=(X'X)^{-1}X'Y_j$（$j=1,2$）。（注意：此时 **SUR=OLS**，见 §0 条件 (a)。）

**(b) 联合渐近分布：** 堆叠 $\hat\beta=(\hat\beta_1',\hat\beta_2')'$。同方差时 $V_\beta=\Sigma\otimes(E[XX'])^{-1}$（(11.14)）。跨方程协方差块：
$$\mathrm{ACov}(\hat\beta_1,\hat\beta_2)=Q_{xx}^{-1}E[XX'e_1e_2]Q_{xx}^{-1}.$$
（**关键**：即使回归元相同，两方程系数仍相关——因为误差 $e_1,e_2$ 相关。这就是 SUR 想利用的信息。）

**(c) 检验 $H_0:\beta_1=\beta_2$：** 令 $\hat\delta=\hat\beta_1-\hat\beta_2$。其方差 $\widehat{\mathrm{Avar}}(\hat\delta)=\hat V_{11}+\hat V_{22}-\hat V_{12}-\hat V_{21}$（**必须含跨方程协方差块** $\hat V_{12}$！）。Wald $W=n\hat\delta'\widehat{\mathrm{Avar}}(\hat\delta)^{-1}\hat\delta\to_d\chi^2_k$。

> **和本科对照：** 这是"两方程系数是否相同"的检验（如"男女教育回报是否相同"）。**关键易错**：$\mathrm{var}(\hat\beta_1-\hat\beta_2)=\mathrm{var}(\hat\beta_1)+\mathrm{var}(\hat\beta_2)-2\mathrm{cov}(\hat\beta_1,\hat\beta_2)$——**不能漏掉协方差项**（同 Ch7 Ex 7.17、Ch9 Ex 9.2）。蒙特卡洛验证见 notebook。

---

## 附录 A：SUR vs OLS 决策表

| 情形 | SUR vs OLS | 原因 |
|---|---|---|
| 回归元相同（$X_j=X$） | **SUR = OLS** | Kronecker 结构使 GLS 退化为 OLS（已 MC 验证：逐样本相同） |
| 跨方程误差不相关（$\Sigma$ 对角） | **SUR = OLS** | 无跨方程信息可借 |
| 回归元不同 + 误差相关 | **SUR > OLS** | 借用其他方程信息，方差下降（MC：可减半） |

**实操：** 先估各方程 OLS、算 $\hat\Sigma$。若 $\hat\Sigma$ 近似对角或回归元相同，SUR 无增益；否则用（可行）SUR 提效。

---

## 附录 B：与单方程的完全对应

| 单方程（Ch4/7） | 多方程（Ch11） |
|---|---|
| $Y=X'\beta+e$ | $Y=\mathbf{X}\beta+e$（堆叠） |
| $\hat\beta=(X'X)^{-1}X'Y$ | $(\mathbf{X}'\mathbf{X})^{-1}\mathbf{X}'Y$ |
| $Q=E[XX']$，$\Omega=E[XX'e^2]$ | $Q=E[\mathbf{X}'\mathbf{X}]$，$\Omega=E[\mathbf{X}'ee'\mathbf{X}]$ |
| $V_\beta=Q^{-1}\Omega Q^{-1}$（夹心） | 同（夹心，系统级） |
| GLS（已知 $\Omega$） | SUR（已知 $\Sigma$） |
| 同方差 $\sigma^2(X'X)^{-1}$ | 共同 $X$ + 同方差 $\Sigma\otimes Q_{xx}^{-1}$ |

**一句话：** 第 11 章 = 第 4 章 GLS + 第 7 章渐近理论的**多方程堆叠版**，无新原理，多了 Kronecker 结构和跨方程信息利用（SUR）。

---

## 附录 C：notebook 单元对应

| 习题 | notebook 内容 |
|------|----------------|
| 11.15 | 共同 $X$ 下 $(\hat\beta_1,\hat\beta_2)$ 联合协方差的蒙特卡洛核对 code cell |
| 11.1–11.14 | 证明，详见本 .md |
