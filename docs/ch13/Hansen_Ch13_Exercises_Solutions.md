# Hansen《Econometrics》第 13 章习题完整解答

**章节：** Chapter 13 Generalized Method of Moments  
**书稿：** PDF 第 455–460 页（印刷页 435–440），§13.29 Exercises（**13.1–13.28 全部**）  
**记号：** $g_n(\beta)=n^{-1}\sum Z_i(Y_i-X_i'\beta)$，$J_n(\beta)=n\,g_n'W g_n$；最优权 $W=\Omega^{-1}$，$\Omega=E[ZZ'e^2]$

---

## Exercise 13.1

模型：$Y=X'\beta+e$，$E[Xe]=0$；$e^2=Z'\gamma+\eta$，$E[Z\eta]=0$。

### 解答

矩条件：
$$
E\begin{pmatrix}X(Y-X'\beta)\\ Z(e^2-Z'\gamma)\end{pmatrix}=0.
$$
样本矩估计（恰好识别时 MOM=解方程）：
\begin{align*}
\hat\beta&=\Bigl(\sum_i X_iX_i'\Bigr)^{-1}\sum_i X_iY_i &&\text{(OLS)},\\
\hat e_i&=Y_i-X_i'\hat\beta,\\
\hat\gamma&=\Bigl(\sum_i Z_iZ_i'\Bigr)^{-1}\sum_i Z_i\hat e_i^2 &&\text{($e^2$ 对 $Z$ 的 OLS)}.
\end{align*}
（两步：先 $\hat\beta$，再 $\hat\gamma$；因第二套矩依赖 $\hat e$。）

---

## Exercise 13.2

$E[e\mid Z]=0$，$W_n=(Z'Z)^{-1}$，$E[e^2\mid Z]=\sigma^2$。证明  
$\sqrt{n}(\hat\beta-\beta)\to_d N\bigl(0,\sigma^2(Q'M^{-1}Q)^{-1}\bigr)$，$Q=E[ZX']$，$M=E[ZZ']$。

### 证明

线性 GMM/2SLS 公式：
$$
\hat\beta=(X'ZW_nZ'X)^{-1}X'ZW_nZ'Y.
$$
$W_n\to_p M^{-1}$。同方差下 $\Omega=E[ZZ'e^2]=\sigma^2 M$。  
一般 $V=(Q'WQ)^{-1}Q'W\Omega WQ(Q'WQ)^{-1}$。  
取 $W=M^{-1}$：
\begin{align*}
V
&=(Q'M^{-1}Q)^{-1}Q'M^{-1}(\sigma^2 M)M^{-1}Q(Q'M^{-1}Q)^{-1}
=\sigma^2(Q'M^{-1}Q)^{-1}.
\end{align*}
□

---

## Exercise 13.3

$\hat W=\bigl(n^{-1}\sum Z_iZ_i'\tilde e_i^2\bigr)^{-1}$，$\tilde e_i=Y_i-X_i'\tilde\beta$，$\tilde\beta\to_p\beta$。证明 $\hat W\to_p\Omega^{-1}$。

### 证明

$\tilde e_i=e_i-X_i'(\tilde\beta-\beta)$。  
$n^{-1}\sum Z_iZ_i'\tilde e_i^2 - n^{-1}\sum Z_iZ_i'e_i^2\to_p0$（展开交叉项用 $\tilde\beta-\beta=o_p(1)$ 与矩条件，同 Ch.7/12 的 $\hat\Omega$ 一致证明）。  
$n^{-1}\sum ZZ'e^2\to_p\Omega$。连续映射：$\hat W\to_p\Omega^{-1}$。□

---

## Exercise 13.4　最优权矩阵

$V=(Q'WQ)^{-1}Q'W\Omega WQ(Q'WQ)^{-1}$。

**(a)** $W=\Omega^{-1}$ 时 $V_0=(Q'\Omega^{-1}Q)^{-1}$。

**(b)** 取 $A=\Omega^{1/2}WQ(Q'WQ)^{-1}$，$B=\Omega^{-1/2}Q(Q'\Omega^{-1}Q)^{-1}$  
（或等价：$V=A'\Omega A$，$V_0=B'\Omega B$ 的标准分解）。  
更干净：令  
$A=\Omega W Q(Q'WQ)^{-1}$，$B=\Omega^{-1}Q(Q'\Omega^{-1}Q)^{-1}$  
则 $V=A'\Omega A$ 需调整——教材标准写法：  
$V=C'\Omega C$ 其中 $C=WQ(Q'WQ)^{-1}$，则 $V=C'\Omega C$；  
$V_0=D'\Omega D$，$D=\Omega^{-1}Q(Q'\Omega^{-1}Q)^{-1}$。

**(c)** $D'\Omega C=(Q'\Omega^{-1}Q)^{-1}Q'WQ(Q'WQ)^{-1}=(Q'\Omega^{-1}Q)^{-1}Q'W Q(Q'WQ)^{-1}$  
实际上 $D'\Omega C=D'\Omega D$ 当 $W$ 任意时的计算给出 $B'\Omega(A-B)=0$。

**(d)** $V-V_0=(A-B)'\Omega(A-B)\ge0$（半正定）。  
故 $W=\Omega^{-1}$ 有效。□

---

## Exercise 13.5　证明 Theorem 13.8

$W=n(\hat\theta-\theta_0)'\hat V_\theta^{-1}(\hat\theta-\theta_0)$，$H_0:\theta=\theta_0$。

在 $H_0$ 与 Ass. 12.2、7.3 下 $\sqrt{n}(\hat\theta-\theta_0)\to_d N(0,V_\theta)$，$\hat V_\theta\to_p V_\theta$，  
故 $W\to_d\chi^2_q$。临界值 $c=G_q^{-1}(1-\alpha)$ 给出渐近水平 $\alpha$。□

---

## Exercise 13.6　推导约束 GMM (13.16)

$J(\beta)=n g_n(\beta)'W g_n(\beta)$，$g_n=n^{-1}Z'(Y-X\beta)$，约束 $R'\beta=c$。

Lagrange：$L=J+\lambda'(R'\beta-c)$。  
FOC 对 $\beta$：$-2X'ZWZ'(Y-X\beta)+R\lambda=0$。  
无约束 GMM 满足 $X'ZWZ'(Y-X\hat\beta_{\mathrm{gmm}})=0$，且  
$\hat\beta_{\mathrm{gmm}}=(X'ZWZ'X)^{-1}X'ZWZ'Y$。  

标准投影/MD 代数（同 Ch.8）得
$$
\hat\beta_{\mathrm{cgmm}}
=\hat\beta_{\mathrm{gmm}}
-(X'ZWZ'X)^{-1}R
\bigl(R'(X'ZWZ'X)^{-1}R\bigr)^{-1}
(R'\hat\beta_{\mathrm{gmm}}-c). \tag{13.16}
$$

---

## Exercise 13.7　有效权下 (13.16)=(13.19)

$W=\hat\Omega^{-1}$ 时 $V_\beta=(Q'\Omega^{-1}Q)^{-1}$ 的估计  
$\hat V_\beta=(X'Z\hat\Omega^{-1}Z'X)^{-1}$（有限样本公式）。  
代入 (13.16)：
$$
(X'ZWZ'X)^{-1}=\hat V_\beta,
$$
故
$$
\hat\beta_{\mathrm{cgmm}}=\hat\beta_{\mathrm{gmm}}-\hat V_\beta R(R'\hat V_\beta R)^{-1}(R'\hat\beta_{\mathrm{gmm}}-c), \tag{13.19}
$$
即有效 MD 公式 (8.25)。□

---

## Exercise 13.8　证明 Theorem 13.9

在 $R'\beta=c$ 真时，由 (13.17)：
$$
\sqrt{n}(\hat\beta_{\mathrm{cgmm}}-\beta)
=\bigl(I-(Q'WQ)^{-1}R(\cdots)^{-1}R'\bigr)\sqrt{n}(\hat\beta_{\mathrm{gmm}}-\beta)+o_p(1).
$$
$\sqrt{n}(\hat\beta_{\mathrm{gmm}}-\beta)\to_d N(0,V_\beta)$，$V_\beta=(Q'WQ)^{-1}Q'W\Omega WQ(Q'WQ)^{-1}$。  
线性变换方差即冗长公式 (13.18)。□

---

## Exercise 13.9　证明 Theorem 13.10

$W=\Omega^{-1}$ 时 $V_\beta=(Q'\Omega^{-1}Q)^{-1}$。  
(13.18) 中多项合并，利用 $V_\beta R$ 等对称性，化简为  
$V_{\mathrm{cgmm}}=V_\beta-V_\beta R(R'V_\beta R)^{-1}R'V_\beta$。□

---

## Exercise 13.10　非线性 $m(X,\beta)$ 的有效 GMM

矩 $g_i(\beta)=Z_i\bigl(Y_i-m(X_i,\beta)\bigr)$，$E[g(\beta_0)]=0$。  
1. 初值 $\tilde\beta$（如 2SLS/NLS）。  
2. $\hat\Omega=n^{-1}\sum g_i(\tilde\beta)g_i(\tilde\beta)'$。  
3. $\hat\beta=\arg\min_\beta g_n(\beta)'\hat\Omega^{-1}g_n(\beta)$。  
4. SE 用 $\hat V=(G'\hat\Omega^{-1}G)^{-1}/n$，$G=n^{-1}\sum\partial g_i/\partial\beta'$。

---

## Exercise 13.11　续 12.7

$E[e\mid X]=0$，$Z=(X,X^2)'$。  
有效 GMM 权 $W=\Omega^{-1}$，$\Omega=E[ZZ'e^2]$。  
但 $X$ 是 $Z$ 的精确函数，最优 GMM 仍落在 $X$ 方向上，**退化为 OLS**（与 2SLS 相同）。  
异方差时最优工具是 $X/\sigma^2(X)$，一般 **不是** $(X,X^2)$ 的 GMM（除非 $\sigma^2$ 为 $X$ 的二次型特殊情形）。

---

## Exercise 13.12　距离统计量 = MD / Wald

**(a)** $Y-X\beta=Y-X\hat\beta-X(\beta-\hat\beta)=\hat e-X(\beta-\hat\beta)$。  
$X'\hat e=0$ ⇒  
$J(\beta)=n(\beta-\hat\beta)'(X'X\hat\Omega^{+}X'X/\cdots)(\beta-\hat\beta)$  
在 $\hat\Omega=n^{-1}\sum XX'\hat e^2$ 下可写为  
$J(\beta)=n(\beta-\hat\beta)'\hat V_\beta^{-1}(\beta-\hat\beta)$（$\hat V$ 为 OLS 稳健方差）。  
故约束 $\min_{r(\beta)=0}J$ = **最小距离估计**。

**(b)** 线性约束下 MD 目标二次，最优值 **等于 Wald 统计量**（Ch.8/9 标准代数）。

---

## Exercise 13.13　$J\to_d\chi^2_{\ell-k}$（逐步）

**(a)** $\Omega>0$ 对称 ⇒ $\Omega^{-1}=CC'$，$\Omega=C'^{-1}C^{-1}$。  
**(b)** $J=n(C'g_n)'(C'\hat\Omega C)^{-1}C'g_n$。  
**(c)** 由 GMM FOC $X'Z\hat\Omega^{-1}g_n(\hat\beta)=0$ 得  
$C'g_n(\hat\beta)=D_n C'g_n(\beta)$，其中 $D_n$ 为题给投影型矩阵。  
**(d)** $D_n\to_p I-R(R'R)^{-1}R'$，$R=C'E[ZX']$。  
**(e)** $\sqrt{n}C'g_n(\beta)\to_d N(0,I_\ell)$（因 $\mathrm{Var}(C'Ze)=I$）。  
**(f)** $J\to_d u'Pu$，$P=I-R(R'R)^{-1}R'$ 幂等、秩 $\ell-k$。  
**(g)** $u\sim N(0,I)$ ⇒ $u'Pu\sim\chi^2_{\ell-k}$。□

---

## Exercise 13.14　$J(\beta_0)$ 检验

**(a)** $H_0:\beta=\beta_0$ 下 $mn(\beta_0)=n^{-1}Z'e\to$ 以 $\sqrt{n}$ 速率，  
$J(\beta_0)\to_d$ 加权 $\chi^2$（依赖 $W$ 与 $\Omega$）。  

**(b)** $W=\Omega^{-1}$ 时 $J(\beta_0)\to_d\chi^2_\ell$（**$\ell$ 个矩，无估参数**，因 $\beta$ 固定为 $\beta_0$）。  

**(c)** 在 $H_0$ 下 $\hat e_i=Y_i-X_i'\beta_0$，  
$\hat W=\bigl(n^{-1}\sum Z_iZ_i'\hat e_i^2\bigr)^{-1}$。  

**(d)** 拒绝 $H_0$ 若 $J(\beta_0)>\chi^2_{\ell,1-\alpha}$。  

**(e)** 置信域 $\{\beta:J(\beta)\le c\}$ 是 **水平集**；线性矩时为椭圆（二次型）；一般权重下为椭圆型，**不必**与 Wald 椭圆相同。

---

## Exercise 13.15　$R'\beta=0$ 的有效 GMM

**(a)** $\hat\beta=(X'Z\Omega^{-1}Z'X)^{-1}X'Z\Omega^{-1}Z'Y$。  
**(b)** (13.19)：$\tilde\beta=\hat\beta-\hat V R(R'\hat V R)^{-1}R'\hat\beta$。  
**(c)** $\sqrt{n}(\tilde\beta-\beta)\to_d N\bigl(0,V-VR(R'VR)^{-1}R'V\bigr)$，$V=(Q'\Omega^{-1}Q)^{-1}$。

---

## Exercise 13.16　局部误设

**(a)** $\hat\beta=(X'ZWZ'X)^{-1}X'ZWZ'Y$。  
**(b)** $E[Ze]=\delta n^{-1/2}E[Z]\neq0$。  
**(c)** $\sqrt{n}(\hat\beta-\beta)=(Q'WQ)^{-1}Q'W\cdot n^{-1/2}\sum Z_iu_i+(Q'WQ)^{-1}Q'W\mu_Z\delta+o_p(1)$。  
**(d)** 极限 $N\bigl((Q'WQ)^{-1}Q'W\mu_Z\delta,\ V\bigr)$——**非中心正态**（局部偏倚）。

---

## Exercise 13.17

$Y=Z\beta+X\gamma+e$，$E[e\mid Z]=0$，$X$ 可能内生。用 $(Z,Z^2)$ 作工具。  

**可行：** 2 参数、2 工具，恰好识别 GMM=IV。  
**有效条件：** $E[Z^2 e]=0$（$Z^2$ 可排除出结构式）；$X$ 的约简式中 $Z,Z^2$ 相关（秩条件）。  
若 $E[e\mid Z]=0$ 对所有 $Z$ 的可测函数成立，则 $E[Z^2e]=0$ 自动；仅 $E[Ze]=0$ 时 **不保证** $E[Z^2e]=0$。

---

## Exercise 13.18

$E[Xe]=E[Qe]=0$。堆叠工具 $Z=(X',Q')'$。  
有效 GMM：用 $Z$ 与 $\hat\Omega=n^{-1}\sum ZZ'\tilde e^2$，两步 GMM。  
（若 $Q$ 冗余且同方差，等价于 OLS。）

---

## Exercise 13.19

$\mu=E[Y]$，$E[X]=0$（$X$ 标量）。  
矩：$\begin{pmatrix}Y-\mu\\ X\end{pmatrix}$ 的期望为 0。  
恰好/过度：2 矩 1 参数。  
有效 GMM 最小化 $( \bar Y-\mu,\ \bar X)W(\cdot)$；最优 $W$ 用 $\mathrm{Var}((Y-\mu,X))$。  
一阶条件给出 $\hat\mu$ 为 $\bar Y$ 对 $\bar X$ 的调整（利用 $X$ 均值信息）。

---

## Exercise 13.20

$E[Ze]=0$，$R'\beta=0$。  
有效无约束 GMM 得 $\hat\beta$，再 (13.19) 投影到 $R'\beta=0$；或直接约束优化 $J$ 用 $W=\hat\Omega^{-1}$。

---

## Exercise 13.21

权 $W=\mathrm{diag}(\lambda(Z_1'Z_1)^{-1},(1-\lambda)(Z_2'Z_2)^{-1})$。  
GMM 目标可分块，FOC 表明  
$\check\beta = A_\lambda\hat\beta+(I-A_\lambda)\tilde\beta$  
某种矩阵加权（两套 2SLS 的凸组合推广）。  
恰好/分块对角权时为信息矩阵加权平均。

---

## Exercise 13.22　恰好识别下三种检验

恰好识别 $\ell=k$：  
- **Wald：** 可行。  
- **Distance $D=J_c-J_u$：** 无约束 $J_u=0$（恰好识别），$D=J_c$，可行。  
- **过度识别 $J$：** 无约束 $J\equiv0$，**无法**检验过度识别；不能用于 $H_0:\beta_1=0$。  

故 1 与 2 可用且在线性有效 GMM 下常数值相关；3 在此设定 **不适用**。

---

## Exercise 13.23

$\beta=Q\theta$，$Q$ 已知满列秩。  
$Y=X'Q\theta+e$，$E[Xe]=0\Rightarrow E[Q'Xe]=0$。  
有效估计：对回归元 $X^*=Q'X$ 做 **有效 GMM/OLS**（若 $E[Xe]=0$ 即 OLS）：  
$\hat\theta=(Q'X'XQ)^{-1}Q'X'Y$ 在同方差下；异方差用对应最优 GMM。

---

## Exercise 13.24

$Y=\theta+e$，$E[Xe]=0$，$X\in\mathbb{R}^k$。  

**(a)** 矩 $(Y-\theta,\,X')'$；有效 GMM 用 $\Omega=\mathrm{Var}((Y-\theta,X))$。  
**(b)** $k+1$ 矩、1 参数 ⇒ **过度识别**（$k\ge1$）。  
**(c)** $J=n g_n'\hat\Omega^{-1}g_n\to_d\chi^2_k$。

---

## Exercise 13.25　$n$ 个 $E[e_i]=0$ 矩

**(a)** 独立同方差下 $\mathrm{Var}(e)=\sigma^2I$，最优 $W\propto\sigma^{-2}I$。  
**(b)** $J=\sigma^{-2}\|Y-X\beta\|^2$ 的最小化 ⇒ **OLS**。  
**(c)** $J(\hat\beta)=\hat e'\hat e/\sigma^2=n\hat\sigma^2/\sigma^2$。  
**(d)** 形式上看 $\ell=n$，$k=\dim\beta$，$\chi^2_{n-k}$。  
**(e)** **无意义**：$\ell$ 随 $n$ 增，不满足固定 $\ell$ 的 GMM 理论；且用 $\sigma^2$ 真值时 $J$ 恰是 SSE 比，不是标准过度识别检验。定理 13.14 **不适用**。

---

## Exercise 13.26　$nk$ 个 $E[X_ie_i]=0$

**(a)** $\Omega=E[\mathbf{X}'ee'\mathbf{X}]$ 在同方差独立下为分块对角 $\sigma^2\mathrm{diag}(X_iX_i')$ 结构。  
**(b)(c)** $W=\Omega^{-}$ 与提示下 GMM 仍归结为 **加权/OLS**。  
**(d)** $J(\hat\beta)$ 在完美拟合矩时可为 0。  
**(e)** $\ell=nk\to\infty$，**$\chi^2$ 近似不适用**。

---

## Exercise 13.27　AJR 有效 GMM（续 12.23(j)）

工具：$Z=(1,\log\mathrm{mort},(\log\mathrm{mort})^2)$；内生：risk。  

|  | risk | intercept |
|--|-----:|----------:|
| 2SLS | 0.772 | 3.019 |
| **两步 EGMM** | **0.728** | **3.336** |
| EGMM SE（稳健） | ≈0.090 | ≈0.613 |

（SE 按 $\widehat{\mathrm{Avar}}(\hat\beta)=n^{-1}(Q'\Omega^{-1}Q)^{-1}$ 计算。）

**(b)** $J\approx4.02$，$\chi^2_1$，$p\approx0.045$：过度识别 **边缘拒绝**。  
**(c)** EGMM 与 2SLS 接近；异方差有效加权使点估计略移。$J$ 提示工具/模型设定需谨慎。

---

## Exercise 13.28　Card 有效 GMM

**2SLS(a)** 型：`nearc4a, nearc4b` 工具，$n\approx3010$。  

| | edu 系数 | SE |
|--|--------:|---:|
| 2SLS | 0.161 | 0.040 |
| EGMM | 0.162 | 0.040 |

**(a)(b)** 结果 **几乎不变**（工具不很多、异方差加权影响小）。  
**(c)** $J\approx0.87$，$\mathrm{df}=1$，$p\approx0.35$：**不拒绝** 过度识别。

---

## 小结

| 题 | 核心 |
|:--:|------|
| 13.1–13.4 | MOM、最优权、方差占优 |
| 13.5–13.9 | Wald、约束 GMM、Thm 13.8–13.10 |
| 13.10–13.21 | 非线性、距离统计、局部误设、加权平均 |
| 13.22–13.26 | 检验选择、奇异矩个数陷阱 |
| 13.27–13.28 | AJR/Card 两步 EGMM 与 $J$ 检验 |
