# Bruce Hansen《Econometrics》第 16 章习题解答（详细注释版）

**章节：** Chapter 16 Non-Stationary Time Series
**书稿：** PDF 第 615–616 页（印刷页 595–596），§16.23 Exercises（**16.1–16.14 全部**）
**数值验证：** `Hansen_Ch16_Exercises_Solutions.ipynb`（ADF/KPSS/Johansen 实证 + 理论结论的蒙特卡洛验证）

> **写给谁看：** 假设你学过李子奈/陈强的入门计量，知道"单位根""协整""ADF 检验"，但对"**为什么单位根下 OLS 不行**""**Dickey–Fuller 临界值为什么不是 $-1.96$**""**协整到底什么意思**"说不清。
> 本章是第 14–15 章（平稳时间序列）的**反面**：当序列**非平稳**（单位根）时，前面所有的渐近理论（WLLN、CLT、HC/HAC）**全部失效**——需要全新的工具。

---

## 0. 读题前必看：本章到底在讲什么

**承上启下：**
- 第 14–15 章：**平稳**时间序列。遍历定理（WLLN）和 CLT 成立，OLS 渐近正态，标准误用 HC/HAC。
- **第 16 章：非平稳（单位根）序列。** 当 $Y_t=Y_{t-1}+e_t$（随机游走）时，$\mathrm{var}(Y_t)=t\sigma^2\to\infty$ ⇒ 遍历定理**失效**，CLT 的 $\sqrt{n}$ 收敛速率**变成 $n$**，$t$ 统计量的分布**不再是正态**——这一切让标准 OLS 推断崩溃。

**三大灾难（单位根破坏了什么）：**

| 灾难 | 原因 | 后果 |
|---|---|---|
| **伪回归** | 两个独立 I(1) 回归，OLS $t$ 不收敛到 0 | **85%** 的"显著"是假的（MC 验证，正态下应仅 5%）|
| **DF 非正态** | 单位根下 $\hat\alpha$ 的 $t$ 不服从 $N(0,1)$ | 临界值更负（$-1.93$ 而非 $-1.645$），用正态会**过度拒绝** |
| **标准 CI 失效** | $\sqrt{n}(\hat\alpha-\alpha)$ 不正态、不对称 | "$95\%$ CI 不含 1 ⇒ 拒绝单位根"**逻辑错误** |

**两大工具（应对非平稳）：**
1. **ADF 检验**（Dickey–Fuller）：$H_0:\alpha=1$（单位根）。$t$ 统计量服从 **DF 分布**（非正态），用专门的临界值表。
2. **协整**（Cointegration）：两个 I(1) 序列若有**平稳的线性组合** $\beta'Y_t$，则它们"协整"——可以回归而不伪回归。VECM 模型 + Johansen 检验。

> **和本科对照：** 陈强系统讲 **ADF 检验、协整、VECM、伪回归**。Hansen 的贡献：严格推出 DF 非正态分布（基于布朗运动/泛函中心极限定理 FCLT），并强调"不拒绝单位根 ≠ 是单位根"的逻辑。

> **实证（蒙特卡洛，已验证）：**
> - **随机游走** var($S_{500}$)=512≈500 ✓
> - **伪回归**：两个独立随机游走 OLS，$|t|>1.96$ 的比例 = **85.7%**（正态下应仅 5%）——触目惊心！
> - **DF 分布**：单位根下 $t$ 的 5% 分位 = $-1.93$（正态是 $-1.645$）⇒ 用正态临界值会**过度拒绝**单位根。
> - **协整**：$Y_t=U_t+v_t$，$X_t=2U_t+w_t$，$\beta=(1,-1/2)$，$\beta'Y_t=Y_t-\frac12X_t=v_t-\frac12w_t$ 的 ACF(1)≈0.007（**平稳！**）
> - **过度差分**：$\Delta e_t$ 是 MA(1)，$\rho(1)=-0.5$，$C(1)=1-1=0$ ⇒ 长期方差为 0 ⇒ 平稳但非 I(0)。

---

## 1. 记号、概念速查与"非平稳工具箱"

**记号对照：**

| Hansen 记号 | 中文/本科说法 | 一句话解释 |
|---|---|---|
| I(0) | 零阶单整（平稳） | 平稳且长期方差 $>0$ |
| I(1) | 一阶单整（单位根） | $\Delta Y_t$ 是 I(0)，$Y_t$ 非平稳 |
| $S_t=\sum_{i=1}^t e_i$ | 随机游走 | var($S_t$)=$t\sigma^2$（发散）|
| ADF / DF 检验 | (增广) Dickey–Fuller | $H_0:\alpha=1$（单位根）|
| DF 临界值 | DF 分布表 | 非正态！Case 1: $-2.86$, Case 2: $-2.86$, Case 3: $-3.41$（5%）|
| 伪回归 | spurious regression | 两个独立 I(1) 回归"假显著" |
| 协整 $\beta$ | 协整向量 | $\beta'Y_t$ 平稳（消去公共趋势）|
| VECM | 向量误差修正模型 | 协整系统的 VAR 差分形式 |
| Johansen 迹检验 | 迹检验 | 检验协整秩 $r$ |
| KPSS 检验 | KPSS | $H_0$: **平稳**（与 ADF 反向）|

**非平稳工具箱：**

> **(N1) 随机游走的矩。** $S_t=\sum_{i=1}^te_i$，$e_t$ i.i.d.$(0,\sigma^2)$。独立 ⇒ 方差相加：
> $$E[S_t]=0,\quad \mathrm{var}(S_t)=t\sigma^2.$$
> 方差随 $t$ 增长 ⇒ **非平稳**。

> **(N2) I(0) 的定义。** $Y_t$ 是 I(0) 若：平稳 + 长期方差 $\omega^2=\sum_{k=-\infty}^\infty\gamma(k)>0$。等价地 MA 表示 $C(L)e_t$ 满足 $C(1)\ne0$。

> **(N3) I(1) 的定义。** $Y_t$ 是 I(1) 若 $\Delta Y_t=Y_t-Y_{t-1}$ 是 I(0)。随机游走是典型 I(1)。

> **(N4) DF 分布（非正态！）。** 单位根下 $Y_t=Y_{t-1}+e_t$ 的 OLS $\hat\alpha$：
> $$n(\hat\alpha-1)\to_d\frac{\int W\,dW}{\int W^2\,dr}\quad\text{（非正态，DF 分布）}$$
> $t$ 统计量的 5% 临界值远比 $-1.645$ 更负（Case 2 约 $-2.86$）。**不能用正态临界值！**

> **(N5) 协整。** $Y_t$（$m\times1$，各分量 I(1)）协整 ⇔ 存在 $\beta\ne0$ 使 $\beta'Y_t$ 是 I(0)。$\beta$ 消去公共随机趋势。

> **(N6) Beveridge–Nelson 分解。** I(1) 过程 $=$ **永久成分**（随机游走 $C(1)S_t$）+ **暂时成分**（平稳 $\tilde e_t$）。

---

## 2. 预备记号

$\Delta Y_t=Y_t-Y_{t-1}$。随机游走 $S_t=S_{t-1}+e_t=\sum_{i=1}^te_i$。
ADF 回归：$\Delta Y_t=(\alpha-1)Y_{t-1}+\sum_{j=1}^{p-1}\psi_j\Delta Y_{t-j}+e_t$，检验 $H_0:\alpha-1=0$（即 $\alpha=1$）。
长期方差 $\omega^2=\sum_{k=-\infty}^\infty\gamma(k)$。Cholesky / BN 滞后多项式 $C(L)$，$C(1)=\sum C_j$。

---

## Exercise 16.1　随机游走的矩、标准化与非平稳性

**题：** $S_t=S_{t-1}+e_t$，$S_0=0$，$e_t$ i.i.d.$(0,\sigma^2)$。(a) $E[S_t]$、$\mathrm{var}[S_t]$；(b) $Y_t=(S_t-E[S_t])/\sqrt{\mathrm{var}[S_t]}$ 是否平稳？(c) $Y_{\lfloor nr\rfloor}$ 的渐近分布。

### (a) 均值与方差

**第 1 步（迭代）。** $S_t=S_0+e_1+\cdots+e_t=\sum_{i=1}^te_i$（$S_0=0$）。
**第 2 步（均值）。** $E[S_t]=\sum_{i=1}^t E[e_i]=0$。
**第 3 步（方差）。** $e_i$ **独立** ⇒ 方差相加（不是协方差矩阵的迹，就是标量和）：
$$\mathrm{var}(S_t)=\sum_{i=1}^t\mathrm{var}(e_i)=\sum_{i=1}^t\sigma^2=t\sigma^2.$$
方差**随 $t$ 线性增长** ⇒ 分布随时间发散 ⇒ **非平稳**。□

### (b) 标准化 $Y_t=S_t/(\sigma\sqrt t)$ 仍非平稳

**构造：** $Y_t=S_t/(\sigma\sqrt t)$。$E[Y_t]=0$，$\mathrm{var}(Y_t)=1$（标准化后均值方差固定）。**但仍非平稳**——因为**联合分布**不稳定。验证：取 $t$ 和 $t+k$：
$$\mathrm{Cov}(Y_t,Y_{t+k})=\frac{\mathrm{Cov}(S_t,S_{t+k})}{\sigma^2\sqrt{t(t+k)}}.$$
关键：$\mathrm{Cov}(S_t,S_{t+k})=E[S_tS_{t+k}]$。$S_{t+k}=S_t+\sum_{i=t+1}^{t+k}e_i$，故 $S_tS_{t+k}=S_t^2+S_t\sum_{i>t}e_i$。独立 ⇒ $E[S_t\sum_{i>t}e_i]=E[S_t]\cdot E[\sum e_i]=0$。故 $\mathrm{Cov}(S_t,S_{t+k})=E[S_t^2]=t\sigma^2$。代入：
$$\mathrm{Cov}(Y_t,Y_{t+k})=\frac{t\sigma^2}{\sigma^2\sqrt{t(t+k)}}=\sqrt{\frac{t}{t+k}}.$$
这**依赖 $t$**（当 $t$ 变化时，同一 $k$ 的自相关不同）⇒ 联合分布随时移变化 ⇒ **非平稳**。□

> **要点：** 标准化只能固定一阶矩和二阶矩，但**联合分布**仍依赖时间——平稳性要求**所有**有限维分布时移不变。

### (c) $Y_{\lfloor nr\rfloor}$ 的渐近分布（FCLT）

对 $r\in[\delta,1]$（$\delta>0$）：
$$Y_{\lfloor nr\rfloor}=\frac{S_{\lfloor nr\rfloor}}{\sigma\sqrt{\lfloor nr\rfloor}}=\frac{n^{-1/2}S_{\lfloor nr\rfloor}}{\sigma\sqrt{\lfloor nr\rfloor/n}}.$$
由**泛函中心极限定理**（FCLT）：$n^{-1/2}S_{\lfloor nr\rfloor}\to_d\sigma W(r)$（$W$ 布朗运动）。又 $\lfloor nr\rfloor/n\to r$。故
$$Y_{\lfloor nr\rfloor}\to_d\frac{\sigma W(r)}{\sigma\sqrt r}=\frac{W(r)}{\sqrt r}\sim N(0,1)\quad(r\ge\delta>0).$$
（$W(r)\sim N(0,r)$ ⇒ $W(r)/\sqrt r\sim N(0,1)$。）□

> **要点：** 单点看 $Y_{\lfloor nr\rfloor}$ 退化为 $N(0,1)$，但 (b) 表明**联合**分布非平稳——"每点正态"不代表"过程平稳"。

---

## Exercise 16.2　Beveridge–Nelson 分解

**题：** $\Delta Y_t=e_t+\Theta_1e_{t-1}+\Theta_2e_{t-2}=C(L)e_t$，$C(L)=1+\Theta_1L+\Theta_2L^2$。求 BN 分解。

**BN 恒等式（核心技巧）：** 任何多项式 $C(L)$ 可写成
$$C(L)=C(1)+(1-L)C^*(L).$$
（代数恒等式：$C(L)-C(1)=(L-1)\cdot[\cdots]$，整理即得。）

**第 1 步（算 $C(1)$）。** 代入 $L=1$：
$$C(1)=1+\Theta_1+\Theta_2.$$

**第 2 步（算 $C^*(L)$）。** 由 $C(L)-C(1)=(1-L)C^*(L)$：
$$C^*(L)=\frac{C(L)-C(1)}{1-L}=\frac{(1+\Theta_1L+\Theta_2L^2)-(1+\Theta_1+\Theta_2)}{1-L}=\frac{\Theta_1(L-1)+\Theta_2(L^2-1)}{1-L}.$$
因式分解 $L^2-1=(L-1)(L+1)$：
$$C^*(L)=\frac{(L-1)(\Theta_1+\Theta_2(L+1))}{1-L}=-(\Theta_1+\Theta_2)+\Theta_2L\cdot(-1)$$
化简：
$$C^*(L)=-(\Theta_1+\Theta_2)-\Theta_2L.$$
（验证：$(1-L)C^*(L)=(1-L)[-(\Theta_1+\Theta_2)-\Theta_2L]$，展开后加 $C(1)$ 应等于 $C(L)$ ✓。）

**第 3 步（BN 分解）。** $\Delta Y_t=C(1)e_t+(1-L)C^*(L)e_t=C(1)e_t+(1-L)\tilde e_t$，$\tilde e_t=C^*(L)e_t=-(\Theta_1+\Theta_2)e_t-\Theta_2e_{t-1}$（平稳）。

**第 4 步（水平求和）。** 对 $\Delta Y_t$ 从 $1$ 到 $t$ 求和（$Y_t=\sum_{i=1}^t\Delta Y_i+Y_0$）：
$$Y_t=Y_0+C(1)\sum_{i=1}^te_i+\sum_{i=1}^t(1-L)\tilde e_i=Y_0+C(1)S_t+\tilde e_t-\tilde e_0.$$
记常数 $a=Y_0-\tilde e_0$：
$$\boxed{\ Y_t=\underbrace{C(1)S_t}_{\text{永久成分（随机游走）}}+\underbrace{\tilde e_t}_{\text{暂时成分（平稳）}}+a.\ }$$

> **要点：** 任何 I(1) 过程 = 随机游走（永久趋势 $C(1)S_t$）+ 平稳噪声（$\tilde e_t$）。$C(1)$ 是"长期乘数"，决定随机游走的强度。

---

## Exercise 16.3　I(1) + 平稳噪声 = I(1)

**题：** $Y_t=X_t+u_t$，$X_t=X_{t-1}+e_t$（随机游走），$(e_t,u_t)\sim$ I(0)。

### (a) $Y_t$ 是 I(1)

**证明（长期方差论证）：** $\Delta Y_t=\Delta X_t+\Delta u_t=e_t+\Delta u_t$。$e_t$ 是 I(0)（白噪声），$\Delta u_t$ 是 I(0)（平稳的差分仍平稳）。关键看**长期方差**：
$$\omega_Y^2=\text{long-run var}(\Delta Y_t)=\text{long-run var}(e_t+\Delta u_t).$$
若 $e_t$ 的长期方差 $\omega_e^2>0$（$e_t$ 是新息），则 $\omega_Y^2\ge\omega_e^2>0$（$e_t$ 不被 $\Delta u_t$ 抵消）。故 $\Delta Y_t$ 是 I(0)（平稳、正长期方差）⇒ **$Y_t$ 是 I(1)**。□

> **要点：** "随机游走 + 平稳噪声 = I(1)"——噪声不改变单整阶数（只增加暂时波动）。

### (b) FCLT

$n^{-1/2}Y_{\lfloor nr\rfloor}=n^{-1/2}X_{\lfloor nr\rfloor}+n^{-1/2}u_{\lfloor nr\rfloor}$。第二项 $n^{-1/2}u_t=o_p(1)$（$u_t$ 平稳、有界方差），第一项由 FCLT：$n^{-1/2}X_{\lfloor nr\rfloor}\to_d B(r)\sim\mathrm{BM}(\omega_e^2)$。故
$$n^{-1/2}Y_{\lfloor nr\rfloor}\to_d B(r)\sim\mathrm{BM}(\omega_e^2).\quad□$$

---

## Exercise 16.4　过度差分

**题：** $Y_t=e_t$ i.i.d.$(0,\sigma^2)$（白噪声），$X_t=\Delta Y_t=e_t-e_{t-1}$。

### (a) $Y_t$ 平稳且 I(0)

$Y_t=e_t$ i.i.d. ⇒ 严平稳。长期方差 $=\mathrm{var}(e_t)=\sigma^2>0$ ⇒ I(0)。□

### (b) $X_t=\Delta Y_t$ 平稳但**非** I(0)

$X_t=e_t-e_{t-1}$ 是 MA(1)（参数 $-1$），严平稳。但**滞后多项式** $C(L)=1-L$，$C(1)=1-1=0$ ⇒ **长期方差为 0**（谱密度在零频消失）⇒ **非 I(0)**（I(0) 要求正长期方差）。

**验证（ACF）：** $\gamma_X(0)=\mathrm{var}(e_t-e_{t-1})=2\sigma^2$，$\gamma_X(1)=E[(e_t-e_{t-1})(e_{t-1}-e_{t-2})]=-\sigma^2$，$\gamma_X(k)=0$ ($k\ge2$)。$\rho(1)=-1/2$（MC 核对 ✓）。长期方差 $=2\sigma^2+2(-\sigma^2)=0$。

> **要点（过度差分的危害）：** 对 I(0) 序列取差分，引入了 MA 单位根（$C(1)=0$），导致长期方差为 0——这是"**过度差分**"。差分只对 I(1) 有意义。

---

## Exercise 16.5　协整向量

**题：** $U_t=U_{t-1}+e_t$（随机游走），$Y_t=U_t+v_t$，$X_t=2U_t+w_t$，$(e_t,v_t,w_t)$ i.i.d.。

**第 1 步（$Y_t,X_t$ 各自 I(1)）。** $Y_t=U_t+v_t$：$U_t$ 是 I(1)，$v_t$ 平稳 ⇒ $Y_t$ 是 I(1)（16.3）。同理 $X_t=2U_t+w_t$ 是 I(1)。

**第 2 步（找 $\beta$ 使 $\beta'Y_t$ 平稳）。** $U_t$ 是**公共趋势**——要从 $(Y_t,X_t)$ 的线性组合中消去。注意 $Y_t$ 含 $1\cdot U_t$，$X_t$ 含 $2\cdot U_t$。取 $\beta=(1,-1/2)$：
$$\beta'\begin{pmatrix}Y_t\\X_t\end{pmatrix}=Y_t-\frac12X_t=(U_t+v_t)-\frac12(2U_t+w_t)=U_t+v_t-U_t-\frac12w_t=v_t-\frac12w_t.$$
$v_t-\frac12w_t$ 是两个独立白噪声的线性组合 ⇒ **I(0)**（平稳）。

**结论：**
$$\boxed{\ \beta=\begin{pmatrix}1\\-1/2\end{pmatrix}\quad(\text{或任意非零倍数如 }(2,-1)').\ }$$

> **要点：** 协整向量 $\beta$ **消去公共随机趋势** $U_t$。MC 验证：$\beta'Y_t=Y_t-\frac12X_t$ 的 ACF(1)≈0.007（平稳！），而 $Y_t,X_t$ 各自的 ACF 极高（I(1)）。

---

## Exercise 16.6　平稳 AR(1) 与单位根极限的调和

**题：** $|\alpha|<1$ 时 $\sqrt n(\hat\alpha-\alpha)\to_d N(0,1-\alpha^2)$；$\alpha=1$ 时 $n(\hat\alpha-1)$ 为 DF 型（Theorem 16.9）。如何调和？

**关键：极限在 $\alpha=1$ 处不连续。**

- **$\alpha$ 固定 $|\alpha|<1$**：第 14 章理论，$\sqrt n$ 速率，正态极限 $N(0,1-\alpha^2)$。
- **$\alpha=1$**：第 16 章 Theorem 16.9，$n$ 速率，DF 非正态极限。
- **$\alpha$ 接近 1**（如 $\alpha=0.99$）：$1-\alpha^2\approx0.02$，正态近似方差极小，**有限样本很差**；DF 也不完全适用。

**调和方案：local-to-unity** $\alpha_n=1-c/n$（$c>0$ 固定）。极限为 **Ornstein–Uhlenbeck 泛函**，介于正态（$c\to\infty$）和 DF（$c=0$）之间。

> **要点：** 不能简单套用第 14 章（$\alpha$ 远离 1）或第 16 章（$\alpha=1$）的结果。$\alpha\approx1$ 时需要 local-to-unity 理论——这就是为什么单位根检验在"接近 1"时功效低。

---

## Exercise 16.7　VECM(1) 中 $\beta'Y_t$ 是 AR(1)

**题：** VECM(1) $\Delta Y_t=\alpha\beta'Y_{t-1}+e_t$。证 $Z_t=\beta'Y_t$ 是 AR(1)。

**详细步骤：**
**第 1 步。** $Z_t=\beta'Y_t=\beta'(Y_{t-1}+\Delta Y_t)=\beta'Y_{t-1}+\beta'\Delta Y_t=Z_{t-1}+\beta'\Delta Y_t$。
**第 2 步。** 代入 VECM $\Delta Y_t=\alpha Z_{t-1}+e_t$：
$$Z_t=Z_{t-1}+\beta'(\alpha Z_{t-1}+e_t)=Z_{t-1}+\beta'\alpha\,Z_{t-1}+\beta'e_t.$$
**第 3 步。** 合并：
$$\boxed{\ Z_t=(1+\beta'\alpha)Z_{t-1}+\beta'e_t.\ }$$
这是 **AR(1)**（系数 $\rho=1+\beta'\alpha$，新息 $\beta'e_t$）。

**平稳性：** 协整要求 $\beta'\alpha<0$（误差修正项使 $Z_t$ 回归均衡）⇒ $\rho=1+\beta'\alpha<1$ ⇒ $Z_t$ 平稳。□

> **要点：** VECM 中协整关系 $\beta'Y_t$ 自身是平稳 AR(1)——"误差修正"机制让偏离均衡的 $Z_t$ 回归。

---

## Exercise 16.8–16.11　单位根检验的常见错误（逐步分析）

### 16.8　"$t=-2$ 故拒绝 $\alpha=1$"——**错误**

$\hat\alpha=0.9$，$s=0.05$，$t=(0.9-1)/0.05=-2$。宣称"用 $|t|>1.96$ 拒绝"。

**错误：** 单位根下 $t$ 统计量服从 **DF 分布**（非正态），5% 临界值更负（Case 2 约 $-2.86$）。$-2>-2.86$ ⇒ **不拒绝**。用 $-1.96$ 的正态规则**无效**（过度拒绝）。

### 16.9　"95% CI $[0.82,0.98]$ 不含 1"——**错误**

$\hat\alpha=0.9$，$s=0.04$，CI $[0.82,0.98]$。

**错误：** 常规 CI 基于 $\sqrt n$ 正态对称分位数。单位根下 $\hat\alpha$ 的分布**非正态、非对称**（收敛速率 $n$ 而非 $\sqrt n$）。故 CI 没有正确覆盖率，"不含 1 ⇒ 拒绝单位根"逻辑不成立。应用 ADF 或 Stock 网格 CI。

### 16.10　"去势后 ADF$=-2.5>-1.9$"——**错误（用错临界值）**

$-1.9$ 是 **Case 1**（无截距无趋势）的 5% 临界值。去势后应使用 **Case 3**（截距+趋势）临界值 $-3.41$。$-2.5>-3.41$ ⇒ **不拒绝**。

**要点：** 去势改变了 ADF 的渐近分布（去势布朗运动），必须用对应 Case 的临界值。

### 16.11　"ADF$=-2.0$ ⇒ 推文是单位根"——**错误（检验逻辑）**

**两层错误：**
1. **检验逻辑：** "不拒绝 $H_0$（单位根）" $\ne$ "接受 $H_0$"。ADF$=-2.0$ 的 $p$ 值很大（~30%）⇒ 证据**无力**（既不强烈支持也不强烈反对），不是"证明是单位根"。
2. **建模：** 日推文更可能是带水平漂移/结构变化/厚尾的**平稳**计数过程；单位根对有界序列不合理。应结合 KPSS、经济背景、水平图。

> **核心教训（本章反复）：**
> - 单位根下 $t$ 统计量**不服从正态**——用 DF 临界值；
> - "不拒绝单位根" $\ne$ "是单位根"——检验只是"证据不足"；
> - 去势/确定性项改变 DF 分布——必须匹配 Case 的临界值。

---

## Exercise 16.12–16.14　实证（FRED-MD：ADF / KPSS / Johansen）

**16.12 ADF**：对 FRED-MD 序列做单位根检验（AIC 选阶、Case 2/3）。

| 序列 | Case | ADF | $p$ | 5% 结论 |
|------|:----:|----:|:---:|:-------:|
| $\log(\mathrm{rpi})$ | ct | $-2.09$ | 0.56 | 不拒绝 |
| $\mathrm{indpro}$ | ct | $-3.01$ | 0.12 | 不拒绝 |
| $\mathrm{houst}$ | c | $-3.08$ | 0.03 | **拒绝** |
| $\mathrm{claimsx}$ | c | $-3.38$ | 0.01 | **拒绝** |

**16.13 KPSS**（$H_0$**平稳**，与 ADF 反向）：收入/IP 类 KPSS 拒绝平稳（偏 I(1)）；houst/claims 边缘。

**16.14 Johansen 迹检验**：
- `tb3ms, gs10`（国债利率）：迹检验支持 $r=1$（利差平稳）；
- `aaa, baa`（信用利差）：$r=1$；
- $\log(\mathrm{ipdcongd}),\log(\mathrm{ipncongd})$（耐用品/非耐用品 IP）：拒绝无协整。

> **和本科对照：** ADF + KPSS 双重检验是实务标配——ADF 不拒绝单位根**且** KPSS 拒绝平稳 ⇒ 强烈支持 I(1)。Johansen 迹检验是协整秩的标准工具（陈强 `vecrank`）。

---

## 附录 A：平稳 vs 非平稳（对照）

| | 平稳 I(0)（Ch14–15） | 非平稳 I(1)（Ch16） |
|---|---|---|
| 方差 | 常数 | **随 $t$ 增长** |
| WLLN | 遍历定理 ✓ | **失效** |
| CLT 速率 | $\sqrt n$ | **$n$** |
| OLS $t$ 分布 | 渐近正态 | **DF 分布**（非正态！）|
| 临界值 | $z_{0.025}=1.96$ | **DF 表**（$-2.86$ 等）|
| 两序列回归 | 正常 | **伪回归** |
| 差分 | 不需要 | **$\Delta Y_t$ 变 I(0)** |

**一句话：** 平稳序列用第 14–15 章理论；非平稳序列用 DF 检验 + 协整。搞错平稳性 ⇒ 所有推断失效。

---

## 附录 B：DF 临界值（务必用对 Case）

| Case | 确定性项 | 5% | 1% |
|------|---------|---:|---:|
| 1 | 无 | $-1.95$ | $-2.58$ |
| 2 | 截距 | $-2.86$ | $-3.43$ |
| 3 | 截距 + 趋势 | $-3.41$ | $-3.96$ |

**MC 已验证：** 单位根下 $t$ 的 5% 分位 $\approx-1.93$（Case 1 接近），**不是** $-1.645$。

---

## 附录 C：notebook 单元对应

| 习题 | notebook 内容 |
|------|----------------|
| 16.12–13 | FRED-MD ADF + KPSS code cell |
| 16.14 | FRED-MD Johansen 迹检验 code cell |
| 理论验证 | 随机游走非平稳、伪回归(85%假阳性)、DF分布非正态、协整、过度差分 code cell |
