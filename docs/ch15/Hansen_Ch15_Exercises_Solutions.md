# Bruce Hansen《Econometrics》第 15 章习题解答（详细注释版）

**章节：** Chapter 15 Multivariate Time Series
**出版版：** `hansen/manuscripts/Econometrics_Fullbook.pdf`，PDF 第 592–595 页（印刷页 557–560），§15.32 Exercises（**15.1–15.20 全部**）
**数值验证：** `Hansen_Ch15_Exercises_Solutions.ipynb`（实证 + 理论结论的蒙特卡洛验证）

> **写给谁看：** 假设你学过李子奈/陈强的入门计量，会一元 AR 和 OLS，对"**VAR（向量自回归）**""**脉冲响应**""**Granger 因果**"有印象但算不清楚。
> 本章是第 14 章（一元时间序列）的**多维推广**：$Y_t$ 从标量变成 $m\times1$ 向量，系数从 $\alpha_j$ 变成矩阵 $A_j$，自协方差从 $\gamma(k)$ 变成矩阵 $\Gamma_k$。一切第 14 章的概念（平稳、MA 表示、脉冲响应）都"矩阵化"。新难点是**正交化脉冲响应需要识别**（Cholesky 排序 / SVAR 约束）。

---

## 0. 读题前必看：本章到底在讲什么

**承上启下：**
- 第 14 章：一元 $Y_t=\alpha_1Y_{t-1}+\cdots+e_t$（AR），脉冲响应 $b_j=\alpha_1^j$。
- **第 15 章：多元向量 $Y_t=A_1Y_{t-1}+\cdots+A_pY_{t-p}+e_t$（VAR）**，脉冲响应是矩阵 $\Theta_h$。

**核心直觉：** VAR = "把一元 AR 的**每个标量换成矩阵**"。平稳条件从"$|\alpha_1|<1$"变成"**伴随矩阵特征值都在单位圆内**"；MA 表示从 $Y_t=\sum\alpha^je_{t-j}$ 变成 $Y_t=\sum\Theta_je_{t-j}$；脉冲响应从 $b_j=\alpha^j$ 变成 $\Theta_h=A_1^h$（VAR(1)）。

**本章的新难点——正交化脉冲响应（OIRF）与识别：**
- 原始 IRF $\Theta_h$ 是"对**残差向量** $e_t$ 一个单位的响应"。但 $e_t$ 的各分量**相关**（$\Sigma=E[e_te_t']$ 非对角）⇒ 你无法单独给一个分量"一个冲击"而不影响其他。
- **Cholesky 分解** $\Sigma=LL'$（$L$ 下三角）把相关残差变独立：$e_t=L\varepsilon_t$，$\varepsilon_t$ 独立。OIRF $=\Theta_hL$。**但 $L$ 依赖变量排序**——排序不同，OIRF 不同！
- **结构 VAR（SVAR）**：用经济理论施加约束（短期 $Ae=\varepsilon$ 或长期 $C$）来识别结构冲击。

**Granger 因果：** $Y_2$ 不 Granger 因果 $Y_1$ ⇔ $Y_1$ 方程中所有 $Y_2$ 滞后系数为零（用 Wald 检验）。

> **和本科对照：** 陈强系统讲 VAR、脉冲响应、方差分解、Granger 因果、SVAR。Hansen 的贡献：把 VAR 纳入第 14 章的时间序列框架（平稳/遍历/MA 表示矩阵化），并强调**正交化识别**的任意性——没有经济理论的 Cholesky 排序只是统计操作。

> **实证（蒙特卡洛，已验证）：**
> - VAR(1) MA：$\Theta_1=A$（MC 自协方差反推核对 ✓）；
> - VAR(2) 平稳：伴随矩阵最大特征值 0.852$<$1 ✓；
> - **Cholesky 排序敏感**：$\sigma_1=2\ne\sigma_2=1$ 时，变量排序不同 OIRF **明显不同** ✓；
> - **Granger 因果**：单向因果的模拟中，$Y_1\to Y_2$ Wald=158（拒绝），$Y_2\to Y_1$ Wald=1.0（不拒绝）✓。

---

## 1. 记号、概念速查与"VAR 工具箱"

**记号对照（李子奈/陈强 → Hansen）：**

| Hansen 记号 | 中文/本科说法 | 一句话解释 |
|---|---|---|
| $Y_t$（$m\times1$） | 向量时间序列 | $m$ 个变量的观测向量 |
| VAR($p$) | 向量自回归 | $Y_t=A_1Y_{t-1}+\cdots+A_pY_{t-p}+e_t$ |
| $A_j$（$m\times m$） | 自回归系数矩阵 | 第 $j$ 阶滞后 |
| $\Sigma=E[e_te_t']$ | 残差协方差矩阵 | 各方程残差的同期相关 |
| $\Theta_h$ | 脉冲响应矩阵 IRF | $e_t$ 一单位冲击对 $Y_{t+h}$ 的效应 |
| Cholesky $LL'=\Sigma$ | Cholesky 分解 | 把相关残差正交化 |
| OIRF $=\Theta_hL$ | 正交化脉冲响应 | 对**独立结构冲击**的响应（依赖排序） |
| Granger 因果 | 格兰杰因果 | $Y_2$ 的过去是否帮助预测 $Y_1$ |
| 伴随矩阵 $\mathbf A$ | companion matrix | VAR($p$)→VAR(1) 升维 |

**VAR 工具箱（本章反复用）：**

> **(V1) 平稳条件。** VAR($p$) 严平稳（因果）⇔ 伴随矩阵 $\mathbf A$ 的所有特征值 $|\lambda|<1$（在单位圆内）。VAR(1)：直接看 $A$ 的特征值；VAR($p$)：构造伴随矩阵再算。

> **(V2) MA 表示。** 平稳 VAR 有 $Y_t=\sum_{j=0}^\infty\Theta_je_{t-j}$（$\Theta_0=I$）。$\Theta_h$ 递推：VAR(1) $\Theta_h=A_1^h$；VAR($p$) $\Theta_h=A_1\Theta_{h-1}+\cdots+A_p\Theta_{h-p}$。

> **(V3) 正交化。** $\Sigma=LL'$（$L$ 下三角 Cholesky），$e_t=L\varepsilon_t$（$\varepsilon_t$ 独立），OIRF$=\Theta_hL$。**$L$ 依赖变量排序**——这就是"识别"问题。

> **(V4) Granger 因果。** "$Y_2$ 不 Granger 因果 $Y_1$"⇔ $Y_1$ 方程中所有 $Y_2$ 的滞后系数 $=0$。用 Wald 检验。

> **(V5) 维度。** VAR($p$) 每方程参数数 $=mp+1$（$m$ 变量 $\times p$ 阶滞后 + 截距），共 $m(mp+1)$ 参数。大 $m$、大 $p$ 时**过度参数化**。

---

## 2. 预备记号

VAR($p$)：$Y_t=A_1Y_{t-1}+\cdots+A_pY_{t-p}+e_t$，$Y_t\in\mathbb R^m$，$e_t\sim(0,\Sigma)$（$m\times m$）。
MA 表示：$Y_t=\sum_{j=0}^\infty\Theta_je_{t-j}$，$\Theta_0=I_m$。
脉冲响应：$\Theta_h=\partial Y_{t+h}/\partial e_t'$。
伴随矩阵（VAR($p$)→VAR(1)）：
$$\mathbf A=\begin{pmatrix}A_1&A_2&\cdots&A_p\\I&0&\cdots&0\\&\ddots&&\vdots\\&&I&0\end{pmatrix}\ (mp\times mp).$$

---

## Exercise 15.1　VAR(1) 平稳性：特征值判据

**题：** $Y_t=AY_{t-1}+e_t$，$e_t$ i.i.d.。对给定的 $A$，判断严平稳性。

**判据（V1）：** VAR(1) 严平稳（因果）⇔ $A$ 的所有特征值 $|\lambda_i|<1$。

**为什么？** 迭代 $Y_t=A^tY_0+\sum_{j=0}^{t-1}A^je_{t-j}$。若 $|\lambda_i|<1$，则 $A^t\to0$（初始值影响消失），$\sum A^j$ 收敛（MA 表示存在）⇒ 严平稳。若有 $|\lambda|\ge1$，$A^t$ 发散 ⇒ 非平稳。

**逐题计算（用特征方程 $\det(A-\lambda I)=0$）：**

**(a)** $A=\begin{bmatrix}0.7&0.2\\0.2&0.7\end{bmatrix}$。特征方程：$(0.7-\lambda)^2-0.04=0$ ⇒ $\lambda=0.7\pm0.2$ ⇒ $\lambda_1=0.9,\lambda_2=0.5$。$\max|\lambda|=0.9<1$ ⇒ **平稳**。

**(b)** $A=\begin{bmatrix}0.8&0.4\\0.4&0.8\end{bmatrix}$。$(0.8-\lambda)^2-0.16=0$ ⇒ $\lambda=0.8\pm0.4$ ⇒ $\lambda_1=1.2,\lambda_2=0.4$。$\max|\lambda|=1.2>1$ ⇒ **非平稳**。

**(c)** $A=\begin{bmatrix}0.8&0.4\\-0.4&0.8\end{bmatrix}$。$(0.8-\lambda)^2+0.16=0$ ⇒ $\lambda=0.8\pm0.4i$（复数）。模 $|\lambda|=\sqrt{0.8^2+0.4^2}=\sqrt{0.8}\approx0.894<1$ ⇒ **平稳**。

> **要点：** 复数特征值时看**模** $|\lambda|=\sqrt{\mathrm{Re}^2+\mathrm{Im}^2}$。$|\lambda|<1$ 即可。

---

## Exercise 15.2　VAR(2) 平稳性：伴随矩阵

**题：** $Y_t=A_1Y_{t-1}+A_2Y_{t-2}+e_t$，$A_1=\begin{bmatrix}0.3&0.2\\0.2&0.3\end{bmatrix}$，$A_2=\begin{bmatrix}0.4&-0.1\\-0.1&0.4\end{bmatrix}$。

**判据：** VAR(2) 平稳 ⇔ 伴随矩阵 $\mathbf A$ 的所有特征值 $|\lambda|<1$。

**第 1 步（构造伴随矩阵）。** 把 VAR(2) 写成 VAR(1)：
$$\begin{pmatrix}Y_t\\Y_{t-1}\end{pmatrix}=\underbrace{\begin{pmatrix}A_1&A_2\\I&0\end{pmatrix}}_{\mathbf A}\begin{pmatrix}Y_{t-1}\\Y_{t-2}\end{pmatrix}+\begin{pmatrix}e_t\\0\end{pmatrix}.$$
$\mathbf A$ 是 $4\times4$ 矩阵。

**第 2 步（算特征值）。** 数值计算（代码见 notebook）：$\max|\lambda(\mathbf A)|\approx0.852<1$ ⇒ **严平稳**。

> **要点：** VAR($p$) 通过伴随矩阵化成 VAR(1)，再用 VAR(1) 的特征值判据。伴随矩阵的维度 $mp\times mp$。

---

## Exercise 15.3　VAR(2) from nested AR(1)

**题：** $Y_t=AY_{t-1}+u_t$，$u_t=Bu_{t-1}+e_t$。推出 VAR(2) 形式。

**详细步骤（代入法）：**
**第 1 步。** 从第一式 $u_t=Y_t-AY_{t-1}$ ⇒ $u_{t-1}=Y_{t-1}-AY_{t-2}$。
**第 2 步。** 代入第二式 $u_t=Bu_{t-1}+e_t$：
$$Y_t-AY_{t-1}=B(Y_{t-1}-AY_{t-2})+e_t.$$
**第 3 步（整理成 VAR(2) 标准形式）。**
$$Y_t=AY_{t-1}+BY_{t-1}-BAY_{t-2}+e_t=(A+B)Y_{t-1}-BAY_{t-2}+e_t.$$
故 VAR(2)：$A_1=A+B$，$A_2=-BA$，误差 $e_t$。□

> **要点：** AR(1) + AR(1) 误差 ⇒ VAR(2)。这和一元情形"AR(1) 误差的 AR(1) = ARMA(1,1)"不同——向量情形由于矩阵不可交换，变成 VAR(2)。

---

## Exercise 15.4　独立 AR($p$) → 对角 VAR($p$)

**题：** $Y_{it}$（$i=1,\ldots,m$）独立 AR($p$)：$Y_{it}=\sum_{j=1}^pa_{ij}Y_{i,t-j}+e_{it}$，跨 $i$ 独立。

**解答：** 堆叠 $Y_t=(Y_{1t},\ldots,Y_{mt})'$。由于各 $Y_{it}$ 独立，$Y_i$ 的方程中不含 $Y_k$（$k\ne i$）的滞后 ⇒ **系数矩阵对角**：
$$A_j=\mathrm{diag}(a_{1j},\ldots,a_{mj}),\qquad\Sigma=\mathrm{diag}(\sigma_1^2,\ldots,\sigma_m^2)$$
（$\Sigma$ 对角因跨 $i$ 独立）。无跨方程滞后耦合。□

> **要点：** 独立的一元 AR 拼起来是对角 VAR——退化情形（无动态交互）。VAR 的价值在于 $A_j$ 非对角（跨变量互动）。

---

## Exercise 15.5　VAR(1) 的 MA 矩阵 $\Theta_h=A_1^h$

**题：** VAR(1) $Y_t=A_1Y_{t-1}+e_t$，求 MA 表示的 $\Theta_h$。

**详细步骤（迭代法）：**
**第 1 步。** 迭代 $Y_t=A_1Y_{t-1}+e_t=A_1(A_1Y_{t-2}+e_{t-1})+e_t=A_1^2Y_{t-2}+A_1e_{t-1}+e_t$。
**第 2 步。** 继续往前 $h$ 步：$Y_t=A_1^hY_{t-h}+\sum_{j=0}^{h-1}A_1^je_{t-j}$。平稳时 $A_1^h\to0$（$h\to\infty$），得
$$Y_t=\sum_{j=0}^\infty A_1^je_{t-j}.$$
**第 3 步。** 与 MA 表示 $Y_t=\sum_{j=0}^\infty\Theta_je_{t-j}$ 对比：
$$\boxed{\ \Theta_h=A_1^h\quad(\Theta_0=I=A_1^0).\ }$$

> **要点：** VAR(1) 的脉冲响应就是 $A_1$ 的幂——和一元 AR(1) $b_j=\alpha^j$ 完全平行（标量→矩阵）。MC 核对：$\Theta_1\approx A$（用 $\gamma(1)\gamma(0)^{-1}$ 反推）。

---

## Exercise 15.6　VAR(2) 的 MA 矩阵 $\Theta_h$ 递推

**题：** VAR(2) $Y_t=A_1Y_{t-1}+A_2Y_{t-2}+e_t$，求 $\Theta_1,\ldots,\Theta_4$。

**递推公式：** 代入 MA 表示 $Y_t=\sum\Theta_je_{t-j}$ 到 VAR(2) 方程，对比 $e_{t-h}$ 的系数：
$$\Theta_h=A_1\Theta_{h-1}+A_2\Theta_{h-2}\quad(h\ge2),\qquad\Theta_0=I,\ \Theta_1=A_1.$$

**逐项：**
- $\Theta_0=I$（$e_t$ 对当期 $Y_t$ 的单位效应）。
- $\Theta_1=A_1$（$Y_{t+1}=A_1Y_t+\cdots$，$e_t$ 经 $A_1$ 传递）。
- $\Theta_2=A_1\Theta_1+A_2\Theta_0=A_1^2+A_2$。
- $\Theta_3=A_1\Theta_2+A_2\Theta_1=A_1(A_1^2+A_2)+A_2A_1=A_1^3+A_1A_2+A_2A_1$。
  （注意：$A_1A_2\ne A_2A_1$，矩阵不可交换！）
- $\Theta_4=A_1\Theta_3+A_2\Theta_2$（代入上式展开）。

> **要点：** VAR(2) 脉冲响应是矩阵递推——注意**矩阵乘法不可交换**，$A_1A_2\ne A_2A_1$，故 $\Theta_3$ 含两项 $A_1A_2+A_2A_1$（不是 $2A_1A_2$）。

---

## Exercise 15.7　VAR($p$) 的伴随形式与 IRF

**题：** 把 VAR($p$) 写成 VAR(1) 伴随形式，用它求 IRF。

**第 1 步（伴随形式）。** 记 $\tilde Y_t=(Y_t',Y_{t-1}',\ldots,Y_{t-p+1}')'$（$mp\times1$），$\tilde e_t=(e_t',0,\ldots,0)'$。则
$$\tilde Y_t=\mathbf A\tilde Y_{t-1}+\tilde e_t,\quad\mathbf A=\begin{pmatrix}A_1&\cdots&A_{p-1}&A_p\\I&&&0\\&\ddots&&\vdots\\&&I&0\end{pmatrix}.$$

**第 2 步（用 15.5 的结果）。** 伴随 VAR(1) 的 MA 矩阵 $=\mathbf A^h$。

**第 3 步（提取 $Y_t$ 部分）。** $\mathbf A^h$ 是 $mp\times mp$；$e_t$ 只在前 $m$ 行有效（$\tilde e_t$ 上半 $=e_t$，下半 $=0$）。用选择矩阵 $J=(I_m,0,\ldots,0)$（$m\times mp$）提取左上 $m\times m$ 块：
$$\boxed{\ \Theta_h=J\mathbf A^h J'.\ }$$
（$J'$ 把 $e_t$ 嵌入 $\tilde e_t$ 的前 $m$ 维；$\mathbf A^h$ 传播 $h$ 步；$J$ 提取 $Y_t$ 部分。）

> **要点：** VAR($p$) 通过伴随矩阵化成 VAR(1)，IRF $=\mathbf A^h$ 的左上块——这就是计算机算脉冲响应的标准方法（notebook `companion_irf` 函数）。

---

## Exercise 15.8　$Y_2$ 不 Granger 因果 $Y_1$ 的系数约束

**题：** VAR(2) $Y_t=A_1Y_{t-1}+A_2Y_{t-2}+e_t$，$Y_t=(Y_{1t},Y_{2t})'$。$Y_2$ 不 Granger 因果 $Y_1$ ⇒ $A_1,A_2$ 的约束。

**解答：** "$Y_2$ 不 Granger 因果 $Y_1$"= $Y_2$ 的过去对预测 $Y_1$ 无帮助（控制 $Y_1$ 的过去）= $Y_1$ 方程中 $Y_2$ 的滞后系数全为 0。

$Y_1$ 方程：$Y_{1t}=A_{1,11}Y_{1,t-1}+A_{1,12}Y_{2,t-1}+A_{2,11}Y_{1,t-2}+A_{2,12}Y_{2,t-2}+e_{1t}$。

"不 Granger 因果"⇒ $Y_2$ 的系数为 0：
$$\boxed{\ A_{1,12}=0\quad\text{且}\quad A_{2,12}=0.\ }$$
（$A_{j,12}$ 是 $A_j$ 的 $(1,2)$ 元，即 $Y_1$ 方程中 $Y_2$ 滞后 $j$ 的系数。）

> **要点：** Granger 因果 = 系数约束。检验：对 $A_{j,12}$（$j=1,\ldots,p$）做 Wald（联合 $=0$）。

---

## Exercise 15.9　双向无 Granger 因果

**题：** $Y_2\nrightarrow Y_1$ **且** $Y_1\nrightarrow Y_2$。

**解答：** 两个方向的 Granger 因果都不存在 ⇒ $A_1,A_2$ **都是对角阵**：
$$A_1=\begin{pmatrix}A_{1,11}&0\\0&A_{1,22}\end{pmatrix},\quad A_2=\begin{pmatrix}A_{2,11}&0\\0&A_{2,22}\end{pmatrix}.$$
系统退化为两个**独立的一元 AR**（无跨变量滞后耦合，见 15.4）。□

---

## Exercise 15.10　维数灾难

**题：** $T=20\times12=240$ 月，$m=8$ 变量，$p=12$ 滞后。

**参数计数（V5）：**
- 每方程参数 $=mp+1=8\times12+1=97$（8 变量 $\times$ 12 滞后 + 截距）。
- 有效观测 $\approx T-p=240-12=228$。
- **过度参数化严重**：每方程 97 参数 / 228 观测（比例 ~43%）；总参数 $8\times96=768$（不含截距）。
- **不宜估满 VAR(12) 八变量**：自由度不足，估计噪声大。对策：降维（$m$ 小）、短滞后（$p$ 小）、贝叶斯收缩（Minnesota prior）、因子模型。

> **要点：** VAR 参数量 $O(m^2p)$——$m$ 或 $p$ 大时爆炸。这是 VAR "灵活但费数据"的代价。

---

## Exercise 15.11　Cholesky = 递归回归

**题：** $\hat e_t$ 为 VAR 残差，$\hat\Sigma=\hat B\hat B'$（$\hat B=\mathrm{chol}(\hat\Sigma)$ 下三角）。证 $\hat B$ 可由残差的**递归 OLS** 算出。

**详细步骤：** 将 $\hat e_t=\hat B\varepsilon_t$（$\varepsilon_t$ 独立）展开：
$$\begin{cases}\hat e_{1t}=\hat B_{11}\varepsilon_{1t}\\\hat e_{2t}=\hat B_{21}\varepsilon_{1t}+\hat B_{22}\varepsilon_{2t}\\\quad\vdots\\\hat e_{mt}=\hat B_{m1}\varepsilon_{1t}+\cdots+\hat B_{mm}\varepsilon_{mt}\end{cases}$$
- 第 1 行：$\hat B_{11}=\sqrt{\hat\Sigma_{11}}$（$\varepsilon_{1t}$ 的标准差）。
- 第 2 行：$\hat e_{2t}$ 对 $\hat e_{1t}$ 回归（OLS）⇒ $\hat B_{21}=\hat\Sigma_{21}/\hat\Sigma_{11}$（回归系数），残差方差 $\Rightarrow\hat B_{22}$。
- 第 $j$ 行：$\hat e_{jt}$ 对 $\hat e_{1t},\ldots,\hat e_{j-1,t}$ 做**递归 OLS**⇒ 系数填 $\hat B_{j,1:(j-1)}$，残差标准差 $\Rightarrow\hat B_{jj}$。

这与 Cholesky 分解**数值相同**——Cholesky 本质就是"依次消除前 $j-1$ 个变量的同期影响"。□

> **要点：** Cholesky = 递归回归 = "按排序依次正交化"。第 $j$ 个变量被"净化"掉与前 $j-1$ 个的同期相关。

---

## Exercise 15.12　Cholesky 分解（详细推导）

**(a) $\Sigma=\begin{bmatrix}\sigma_1^2&\rho\sigma_1\sigma_2\\\rho\sigma_1\sigma_2&\sigma_2^2\end{bmatrix}$（题设 $\Sigma_{22}=\sigma_1^2$ 的情形见下）。**

求下三角 $L=\begin{bmatrix}l_{11}&0\\l_{21}&l_{22}\end{bmatrix}$ 使 $LL'=\Sigma$。展开 $LL'=\begin{bmatrix}l_{11}^2&l_{11}l_{21}\\l_{11}l_{21}&l_{21}^2+l_{22}^2\end{bmatrix}$，逐项匹配：
- $l_{11}^2=\sigma_1^2\Rightarrow l_{11}=\sigma_1$。
- $l_{11}l_{21}=\rho\sigma_1\sigma_2\Rightarrow l_{21}=\rho\sigma_2$。
- $l_{21}^2+l_{22}^2=\sigma_2^2\Rightarrow l_{22}=\sigma_2\sqrt{1-\rho^2}$。

$$\boxed{\ L=\begin{bmatrix}\sigma_1&0\\\rho\sigma_2&\sigma_2\sqrt{1-\rho^2}\end{bmatrix}.\ }$$
（若 $\Sigma_{22}=\sigma_1^2$：$l_{22}=\sigma_1\sqrt{1-\rho^2}$。）

**(b) 相关阵**（$\sigma_1=\sigma_2=1$）：$L=\begin{bmatrix}1&0\\\rho&\sqrt{1-\rho^2}\end{bmatrix}$。

**(c) 上三角** $RR'=\begin{bmatrix}1&\rho\\\rho&1\end{bmatrix}$。展开 $RR'=\begin{bmatrix}r_{11}^2+r_{12}^2&r_{12}r_{22}\\r_{12}r_{22}&r_{22}^2\end{bmatrix}$（$R$ 上三角 $r_{21}=0$）：
- $r_{22}^2=1\Rightarrow r_{22}=1$。
- $r_{12}r_{22}=\rho\Rightarrow r_{12}=\rho$。
- $r_{11}^2+r_{12}^2=1\Rightarrow r_{11}=\sqrt{1-\rho^2}$。

$$R=\begin{bmatrix}\sqrt{1-\rho^2}&\rho\\0&1\end{bmatrix}.$$

**(d) OIRF。** $\Theta_h=\begin{bmatrix}1&0\\1&1\end{bmatrix}$，$\rho=0.8$，$\sigma_1=\sigma_2=1$。$L=\begin{bmatrix}1&0\\0.8&0.6\end{bmatrix}$。
$$\mathrm{OIRF}=\Theta_hL=\begin{bmatrix}1&0\\1&1\end{bmatrix}\begin{bmatrix}1&0\\0.8&0.6\end{bmatrix}=\begin{bmatrix}1&0\\1.8&0.6\end{bmatrix}.$$

**(e) 反转排序**（用上三角 $R$）：$\mathrm{OIRF}'=\Theta_hR'=\begin{bmatrix}1&0\\1&1\end{bmatrix}\begin{bmatrix}\sqrt{0.36}&0\\0.8&1\end{bmatrix}=\begin{bmatrix}0.6&0\\1.4&1\end{bmatrix}$——**与 (d) 不同**（等方差时 (d)(e) 碰巧相似，但**不等方差时明显不同**，见 MC 验证）。

**(f)** 正交 IRF **依赖排序**——无经济理论支撑的 Cholesky 排序只是统计操作，结构解释不可靠。

> **MC 已验证：** $\sigma_1=2\ne\sigma_2=1$ 时，两种排序的 OIRF 明显不同（$[[2,0],[2.8,0.6]]$ vs $[[2.6,1.2],[1,0]]$）⇒ 排序影响结构推断。

---

## Exercise 15.13　无识别说明时的 IRF 解释

**解答：** 无排序/识别说明的正交 IRF **不能**解释为结构冲击响应——它只是某一**随意 Cholesky 排序**下的统计分解。应忽略结构性叙述，或要求作者提供识别假设（经济理论依据的短期/长期约束）。

> **要点：** 这是 VAR 文献的核心警告——"Cholesky 排序不是免费的识别"。排序不同，结论可能相反。

---

## Exercise 15.14　三变量 VAR(6)：GDP、价格、联邦基金

**变量：** $\Delta\log\mathrm{GDP}$、$\Delta\log P$、`fedfunds`（增长率/水平混合）。
**排序 $(g,\pi,i)$**，**供给冲击** = Cholesky 第一冲击（GDP 方程）。
**累积 IRF**：因 GDP、价格以**增长率**进入 VAR，需**累加** IRF 得**水平**响应（水平 = 增长累积）。联邦基金已是水平，无需累积。
**结果（$n\approx229$）：** 供给冲击后水平 GDP 瞬时上升并持续为正；价格水平缓慢上升；联邦基金上升。

---

## Exercise 15.15　Kilian (2009) 正交 VAR(4)

**变量：** $(-\mathrm{oil},\mathrm{output},\mathrm{price})$（oil 乘 $-1$ 使冲击推高价格）。$n\approx415$。
**三种 Cholesky 冲击：**
- 油供给（第1）：活动短期略降；
- 需求/活动（第2）：活动大幅正向持久；
- 油特定（第3）：活动响应相对较小。
与 Kilian 叙述一致：区分供给与需求冲击对活动的含义不同。

---

## Exercise 15.16　permit, houst, realln（住房变量 VAR）

**(a)** $\Delta\log(\mathrm{realln})$。
**(b)** AIC 在 $p=1..8$ 中 **$p=6$ 最低**。
**(c)(d)** 住房开工对许可冲击正向持久；对自身冲击瞬时最大；贷款冲击下开工响应偏弱/延迟——符合"许可→开工→贷款"时序。

---

## Exercise 15.17　短约束 SVAR（参照出版版 §15.23）

**(a) 矩阵 $A$（$Ae_t=\varepsilon_t$）。** 变量序 $(I,P,Y,r)$。约束：
- 前三变量（$I,P,Y$）不响应 $r$ 冲击 ⇒ $A$ 的 $r$ 列前三行为 0。
- $I$ 不响应 $P$；$P$ 不响应 $I$。
- 投资对 GDP 单位弹性（$I$ 方程中 $Y$ 的 $A$ 系数 $=-1$）。
$$A=\begin{pmatrix}a_{II}&0&-1&0\\0&a_{PP}&a_{PY}&0\\a_{YI}&a_{YP}&a_{YY}&0\\a_{rI}&a_{rP}&a_{rY}&a_{rr}\end{pmatrix}.$$
**(b) 识别：** $\Sigma$ 提供 $m(m+1)/2=10$ 个矩；$A$ 的自由参数（减零约束后）需 ≤10 且满足秩条件。单位弹性提供额外约束 ⇒ 恰好/过度识别。
**(c)** $I$ 与 $P$ 互不同步响应 ⇒ **非**简单递归三角。
**(d)(e)** 估 VAR(6)+趋势，解 $\hat A$；报告 FF→GDP、GDP→GDP、GDP→$P$ 的结构 IRF。

---

## Exercise 15.18　Kilian 短约束 SVAR（参照出版版 §15.24）

**(a)** $(\mathrm{oil},\mathrm{output},\mathrm{price})$，$Ae=\varepsilon$：油生产不响应产出与价格；产出不响应油（一月延迟）。
$$A=\begin{pmatrix}a_{11}&0&0\\0&a_{22}&a_{23}\\a_{31}&a_{32}&a_{33}\end{pmatrix}.$$
**(b)** 约束个数匹配时恰好识别（类似递归但产出-价格可同时）。
**(c)(d)** VAR(4)，oil×($-1$)；估 $A$ 与价格对三冲击的 IRF。

---

## Exercise 15.19　货币中性检验

**(a)** Granger：GDP 增长对货币增长四滞后做 Wald（联合 $=0$）。本样本**显著**（拒绝严格短期中性）。
**(b)** 四货币系数**和**$=0$：长期中性约束检验。
**(c)** 两变量 SVAR + **长期**货币中性（Blanchard–Quah 型下三角长期 $C$）：GDP 水平对货币冲击的长期响应 $=0$。
**(d)** 累积 IRF：供给冲击抬长期 GDP；货币冲击长期 GDP$\approx0$（由约束）。

---

## Exercise 15.20　Shapiro–Watson 长期约束 SVAR

**变量：** 工时增长、GDP 增长、通胀二阶差分。**长期递归**：工时长期不受产出/通胀影响；GDP 长期不受"需求"冲击。
**(a)** 长期 $C$ 下三角 $3\times3$（(15.24)）。
**(b)** 恰好识别（$CC'=\Phi\Sigma\Phi'$ 的 Cholesky）。
**(c)** AIC 选 **$p=4$**。
**(d)** $\hat C$ 见 notebook。
**(e)** 水平 GDP 对"供给/工时"冲击持久为正；对最后冲击长期近 0（递归长期中性）。

---

## 附录 A：一元 AR → 多元 VAR（对照）

| | 一元 AR（Ch14） | 多元 VAR（Ch15） |
|---|---|---|
| 模型 | $Y_t=\alpha_1Y_{t-1}+\cdots+e_t$ | $Y_t=A_1Y_{t-1}+\cdots+e_t$（$Y_t$ 向量） |
| 平稳条件 | $|\alpha_1|<1$ | **伴随矩阵**特征值 $|\lambda|<1$ |
| MA 表示 | $Y_t=\sum\alpha^je_{t-j}$ | $Y_t=\sum\Theta_je_{t-j}$（$\Theta_j$ 矩阵） |
| 脉冲响应 | $b_j=\alpha^j$ | $\Theta_h=A^h$（VAR(1)）/ 递推 |
| 自协方差 | $\gamma(k)$（标量） | $\Gamma_k$（矩阵） |
| 标准误 | HC / HAC | 方程逐个估（HC/HAC） |
| **新概念** | — | **正交化 IRF**（Cholesky 排序/识别）、Granger 因果 |

**一句话：** VAR = "一元 AR 的矩阵化" + 两个新概念（正交化识别、Granger 因果）。

---

## 附录 B：Cholesky 与排序问题

| 排序 | 含义 | 影响 |
|---|---|---|
| $(Y_1,Y_2)$（$L$ 下三角） | $Y_1$ 先被"冲击"，$Y_2$ 的同期变化归因于 $Y_1$ | OIRF 1 |
| $(Y_2,Y_1)$（$R$ 上三角） | $Y_2$ 先被"冲击" | OIRF 2（**与 1 不同**） |

**已验证（不等方差）：** $\sigma_1=2,\sigma_2=1,\rho=0.8$ 时，OIRF(Y1先) $=\begin{bmatrix}2&0\\2.8&0.6\end{bmatrix}$，OIRF(Y2先) $=\begin{bmatrix}2.6&1.2\\1&0\end{bmatrix}$——明显不同。

**结论：** 正交化 IRF 依赖排序 ⇒ 需要**经济理论识别**（SVAR 短期/长期约束），不能随意 Cholesky。

---

## 附录 C：notebook 单元对应

| 习题 | notebook 内容 |
|------|----------------|
| 15.1–15.2 | 特征值平稳性核对 code cell |
| 15.12 | Cholesky 分解 + OIRF code cell |
| 15.14–15.16, 15.19 | FRED/Kilian VAR + IRF + Granger code cell |
| 理论验证 | VAR(1) MA、VAR(2) 平稳、Cholesky 排序敏感性、Granger 因果 code cell |
