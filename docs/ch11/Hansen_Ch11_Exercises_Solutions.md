# Hansen《Econometrics》第 11 章习题完整解答

**章节：** Chapter 11 Multivariate Regression  
**书稿：** PDF 第 350–351 页（印刷页 330–331），§11.18 Exercises（**11.1–11.15 全部**）  
**记号：** 系统回归 $Y=\mathbf{X}\beta+e$；方程 $j$：$Y_j=X_j'\beta_j+e_j$；$\Sigma=E[ee']$；SUR/GLS

---

## 预备记号（Hansen）

$m$ 个方程堆叠为
$$
Y=\mathbf{X}\beta+e,\qquad
\mathbf{X}_i=\mathrm{diag}(X_{1i}',\ldots,X_{mi}'),
$$
系统 OLS：
$$
\hat\beta=(\mathbf{X}'\mathbf{X})^{-1}(\mathbf{X}'\mathbf{Y})
=\Bigl(\sum_i\mathbf{X}_i'\mathbf{X}_i\Bigr)^{-1}\Bigl(\sum_i\mathbf{X}_i'Y_i\Bigr). \tag{11.4}
$$
条件同方差：$E[ee'\mid X]=\Sigma$ (11.8)。  
共同回归元：$X_j=X$，$\mathbf{X}_i=I_m\otimes X_i'$。

$$
\Omega=E[\mathbf{X}_i'e_ie_i'\mathbf{X}_i],\quad
Q=E[\mathbf{X}_i'\mathbf{X}_i],\quad
V_\beta=Q^{-1}\Omega Q^{-1}.
$$

---

## Exercise 11.1

在条件同方差 (11.8) 下证明 (11.10)：$\Omega=E[\mathbf{X}_i'\Sigma\mathbf{X}_i]$。

### 证明

由定义
$$
\Omega=E[\mathbf{X}_i'e_ie_i'\mathbf{X}_i].
$$
迭代期望，并在 (11.8) 下 $E[e_ie_i'\mid \mathbf{X}_i]=\Sigma$（常数）：
\begin{align*}
\Omega
&=E\bigl[E[\mathbf{X}_i'e_ie_i'\mathbf{X}_i\mid \mathbf{X}_i]\bigr]
=E\bigl[\mathbf{X}_i'\,E[e_ie_i'\mid\mathbf{X}_i]\,\mathbf{X}_i\bigr]
=E[\mathbf{X}_i'\Sigma\mathbf{X}_i].
\end{align*}
即 (11.10)。□

---

## Exercise 11.2

共同回归元 $X_j=X$ 时证明 (11.11)：$\Omega=E[ee'\otimes XX']$。

### 证明

此时 $\mathbf{X}_i=I_m\otimes X_i'$，故
$$
\mathbf{X}_i'e_i=(I_m\otimes X_i)e_i=e_i\otimes X_i
$$
（Kronecker 混合积规则：$(A\otimes B)\mathrm{vec}=B\mathrm{vec}\cdot A'$ 等；更直接：第 $j$ 块为 $X_ie_{ji}$，堆叠为 $e_i\otimes X_i$）。  
因此
$$
\mathbf{X}_i'e_ie_i'\mathbf{X}_i
=(e_i\otimes X_i)(e_i\otimes X_i)'
=e_ie_i'\otimes X_iX_i'.
$$
取期望：
$$
\Omega=E[e_ie_i'\otimes X_iX_i']=E[ee'\otimes XX'].
$$
即 (11.11)。□

---

## Exercise 11.3

共同回归元 **且** 条件同方差时证明 (11.12)：$\Omega=\Sigma\otimes E[XX']$。

### 证明

由 (11.11) 与 $E[ee'\mid X]=\Sigma$：
\begin{align*}
\Omega
&=E\bigl[E[ee'\otimes XX'\mid X]\bigr]
=E\bigl[E[ee'\mid X]\otimes XX'\bigr]
=E[\Sigma\otimes XX']
=\Sigma\otimes E[XX'],
\end{align*}
最后一步因 $\Sigma$ 非随机可提出。即 (11.12)。□

---

## Exercise 11.4　证明 Theorem 11.1

**定理：** 在 Assumption 7.2 下，$\sqrt{n}(\hat\beta-\beta)\to_d N(0,V_\beta)$，$V_\beta=Q^{-1}\Omega Q^{-1}$，  
$Q=E[\mathbf{X}'\mathbf{X}]$（分块对角，$Q_{jj}=E[X_jX_j']$）。

### 证明

堆叠系统 OLS：
$$
\sqrt{n}(\hat\beta-\beta)
=\Bigl(n^{-1}\sum_i\mathbf{X}_i'\mathbf{X}_i\Bigr)^{-1}
\Bigl(n^{-1/2}\sum_i\mathbf{X}_i'e_i\Bigr).
$$
- WLLN：$n^{-1}\sum\mathbf{X}_i'\mathbf{X}_i\to_p Q=E[\mathbf{X}'\mathbf{X}]$（Ass. 7.2 保证矩存在与可逆）。  
- CLT：$\{\mathbf{X}_i'e_i\}$ i.i.d. 零均值（投影条件 $E[X_je_j]=0$ 堆叠），  
  $n^{-1/2}\sum\mathbf{X}_i'e_i\to_d N(0,\Omega)$，$\Omega=E[\mathbf{X}'ee'\mathbf{X}]$。  
- Slutsky：$\sqrt{n}(\hat\beta-\beta)\to_d Q^{-1}N(0,\Omega)=N(0,Q^{-1}\Omega Q^{-1})$。  

$Q$ 的分块对角结构来自 $\mathbf{X}_i'\mathbf{X}_i$ 的分块对角性（不同方程回归元互不交叉）。□

---

## Exercise 11.5

共同回归元时证明 (11.13)：$Q=I_m\otimes E[XX']$。

### 证明

$\mathbf{X}_i=I_m\otimes X_i'$ ⇒  
$$
\mathbf{X}_i'\mathbf{X}_i=(I_m\otimes X_i)(I_m\otimes X_i')=I_m\otimes X_iX_i'.
$$
取期望：$Q=E[I_m\otimes XX']=I_m\otimes E[XX']$。□

---

## Exercise 11.6

共同回归元 + 同方差时证明 (11.14)：$V_\beta=\Sigma\otimes(E[XX'])^{-1}$。

### 证明

由 (11.12)(11.13)，$Q=I_m\otimes Q_{xx}$，$Q_{xx}=E[XX']$，$\Omega=\Sigma\otimes Q_{xx}$。  
Kronecker 逆：$(A\otimes B)^{-1}=A^{-1}\otimes B^{-1}$（可逆时）。  
\begin{align*}
V_\beta
&=Q^{-1}\Omega Q^{-1}
=(I_m\otimes Q_{xx}^{-1})(\Sigma\otimes Q_{xx})(I_m\otimes Q_{xx}^{-1})\\
&=(\Sigma\otimes I_k)(I_m\otimes Q_{xx}^{-1})
=\Sigma\otimes Q_{xx}^{-1}
=\Sigma\otimes(E[XX'])^{-1}.
\end{align*}
□

---

## Exercise 11.7　证明 Theorem 11.2

**定理：** $\theta=r(\beta)$，$R=\partial r(\beta)/\partial\beta'$，则 $\sqrt{n}(\hat\theta-\theta)\to_d N(0,R'V_\beta R)$（在 7.2、7.3 下）。

### 证明

由 Theorem 11.1，$\sqrt{n}(\hat\beta-\beta)\to_d N(0,V_\beta)$。  
Delta 法（Thm 7.x / 标准）：$r$ 在 $\beta$ 连续可微 ⇒  
$\sqrt{n}(r(\hat\beta)-r(\beta))\to_d N(0,R'V_\beta R)$。□  

（此即跨方程函数推断必须 **联合** 处理多方程估计量的原因。）

---

## Exercise 11.8　证明 Theorem 11.3

**定理：** $n\hat V_{\hat\beta}\to_p V_\beta$，$n\hat V^0_{\hat\beta}\to_p V_\beta^0$（同方差公式极限）。

### 证明

稳健估计量
$$
\hat V_{\hat\beta}
=(\mathbf{X}'\mathbf{X})^{-1}
\Bigl(\sum_i\mathbf{X}_i'\hat e_i\hat e_i'\mathbf{X}_i\Bigr)
(\mathbf{X}'\mathbf{X})^{-1}.
$$
$n^{-1}\mathbf{X}'\mathbf{X}\to_p Q$。  
$\hat e_i=e_i-\mathbf{X}_i'(\hat\beta-\beta)$，$\hat\beta-\beta=O_p(n^{-1/2})$，标准展开得  
$n^{-1}\sum\mathbf{X}_i'\hat e_i\hat e_i'\mathbf{X}_i\to_p\Omega$  
（与单方程 HC 证明相同，见 Ch.7）。  
故 $n\hat V\to_p Q^{-1}\Omega Q^{-1}=V_\beta$。  

同方差版用 $\hat\Sigma=n^{-1}\sum\hat e_i\hat e_i'\to_p\Sigma$，  
$n^{-1}\sum\mathbf{X}_i'\hat\Sigma\mathbf{X}_i\to_p E[\mathbf{X}'\Sigma\mathbf{X}]$，得 $n\hat V^0\to_p V_\beta^0$。□

---

## Exercise 11.9　证明 (11.16)

GLS 在 $E[e\mid X]=0$、$E[ee'\mid X]=\Sigma$ 下为
$$
\hat\beta_{\mathrm{gls}}
=\Bigl(\sum_i\mathbf{X}_i'\Sigma^{-1}\mathbf{X}_i\Bigr)^{-1}
\Bigl(\sum_i\mathbf{X}_i'\Sigma^{-1}Y_i\Bigr). \tag{11.16}
$$

### 证明

对 $Y=\mathbf{X}\beta+e$ 左乘 $\Sigma^{-1/2}$：$Y^\dagger=\mathbf{X}^\dagger\beta+e^\dagger$，$E[e^\dagger e^{\dagger'}]=I_m$。  
对变换后模型做 OLS：
$$
\hat\beta
=\Bigl(\sum_i\mathbf{X}_i^{\dagger'}\mathbf{X}_i^\dagger\Bigr)^{-1}
\Bigl(\sum_i\mathbf{X}_i^{\dagger'}Y_i^\dagger\Bigr).
$$
$\mathbf{X}_i^\dagger=\Sigma^{-1/2}\mathbf{X}_i$，$Y_i^\dagger=\Sigma^{-1/2}Y_i$，故  
$\mathbf{X}_i^{\dagger'}\mathbf{X}_i^\dagger=\mathbf{X}_i'\Sigma^{-1}\mathbf{X}_i$，  
$\mathbf{X}_i^{\dagger'}Y_i^\dagger=\mathbf{X}_i'\Sigma^{-1}Y_i$，即 (11.16)。□

---

## Exercise 11.10　证明 (11.17)

向量形式 $E[ee']=I_n\otimes\Sigma$ 时
$$
\hat\beta_{\mathrm{gls}}
=\bigl(\mathbf{X}'(I_n\otimes\Sigma^{-1})\mathbf{X}\bigr)^{-1}
\bigl(\mathbf{X}'(I_n\otimes\Sigma^{-1})\mathbf{Y}\bigr). \tag{11.17}
$$

### 证明

堆叠误差方差 $I_n\otimes\Sigma$。GLS 为  
$(X'\Omega_e^{-1}X)^{-1}X'\Omega_e^{-1}Y$，取 $\Omega_e=I_n\otimes\Sigma$ 即得 (11.17)。  

与 (11.16) 等价：因
$$
\mathbf{X}'(I_n\otimes\Sigma^{-1})\mathbf{X}=\sum_i\mathbf{X}_i'\Sigma^{-1}\mathbf{X}_i
$$
（分块对角作用），右侧同理。□

---

## Exercise 11.11　证明 Theorem 11.4

**定理：** Ass. 7.2 + (11.8) 下 $\sqrt{n}(\hat\beta_{\mathrm{sur}}-\beta)\to_d N(0,V_\beta^*)$，  
$V_\beta^*=(E[\mathbf{X}'\Sigma^{-1}\mathbf{X}])^{-1}$。

### 证明

可行 SUR 用 $\hat\Sigma\to_p\Sigma$，与已知 $\Sigma$ 的 GLS 同极限。  
对已知 $\Sigma$ 的 GLS：
$$
\sqrt{n}(\hat\beta_{\mathrm{gls}}-\beta)
=\Bigl(n^{-1}\sum\mathbf{X}_i'\Sigma^{-1}\mathbf{X}_i\Bigr)^{-1}
\Bigl(n^{-1/2}\sum\mathbf{X}_i'\Sigma^{-1}e_i\Bigr).
$$
$n^{-1}\sum\mathbf{X}'\Sigma^{-1}\mathbf{X}\to_p E[\mathbf{X}'\Sigma^{-1}\mathbf{X}]=:Q_*$。  
$E[\mathbf{X}'\Sigma^{-1}e\mid X]=0$，$E[\mathbf{X}'\Sigma^{-1}ee'\Sigma^{-1}\mathbf{X}]=E[\mathbf{X}'\Sigma^{-1}\mathbf{X}]=Q_*$  
（同方差）。CLT 得中间项 $\to_d N(0,Q_*)$。  
故极限方差 $Q_*^{-1}Q_*Q_*^{-1}=Q_*^{-1}=V_\beta^*$。  
$\hat\Sigma$ 一致 ⇒ SUR 同极限。□

---

## Exercise 11.12　证明 Theorem 11.5（SUR 渐近优于 OLS）

需证
$$
\bigl(E[\mathbf{X}'\Sigma^{-1}\mathbf{X}]\bigr)^{-1}
\le
\bigl(E[\mathbf{X}'\mathbf{X}]\bigr)^{-1}
E[\mathbf{X}'\Sigma\mathbf{X}]
\bigl(E[\mathbf{X}'\mathbf{X}]\bigr)^{-1}.
$$

### 证明（按教材 Hint）

**第一步：** 矩阵 Loewner 序 $A^{-1}\le B^{-1}CB^{-1}$（$A,B>0$）在两边左乘右乘 $B$ 后，等价于证明  
$$
B A^{-1}B \le C
$$
（在 $B$ 可逆时）。取  
$A=E[\mathbf{X}'\Sigma^{-1}\mathbf{X}]$，$B=E[\mathbf{X}'\mathbf{X}]$，$C=E[\mathbf{X}'\Sigma\mathbf{X}]$，  
即需
$$
E[\mathbf{X}'\mathbf{X}]\,(E[\mathbf{X}'\Sigma^{-1}\mathbf{X}])^{-1}\,E[\mathbf{X}'\mathbf{X}]
\le E[\mathbf{X}'\Sigma\mathbf{X}]. \tag{*}
$$

**第二步：** 令 $U=\Sigma^{-1/2}\mathbf{X}$，$V=\Sigma^{1/2}\mathbf{X}$（Hint 中第二个写 $\Sigma^{1/2}\mathbf{X}$）。  
则 $\mathbf{X}'\Sigma^{-1}\mathbf{X}=U'U$，$\mathbf{X}'\Sigma\mathbf{X}=V'V$，$\mathbf{X}'\mathbf{X}=U'V=V'U$。  
(*) 变为
$$
E[U'V]\,(E[U'U])^{-1}\,E[V'U]\le E[V'V].
$$
这正是 **矩阵 Cauchy–Schwarz (B.33)**：  
对适当维随机矩阵，
$E[V'V]-E[V'U](E[U'U])^{-1}E[U'V]\ge 0$（半正定）。  

因此 $V_\beta^*\le V_\beta^{\mathrm{ols}}$，SUR 渐近不劣于系统 OLS。等号当 $\Sigma\propto I$ 或回归元跨方程特殊结构时。□

---

## Exercise 11.13　证明 Theorem 11.6

**定理：** $n\hat V_{\hat\beta_{\mathrm{sur}}}\to_p V_\beta^*$，其中 $\hat V=(\sum_i\mathbf{X}_i'\hat\Sigma^{-1}\mathbf{X}_i)^{-1}$。

### 证明

$\hat\Sigma\to_p\Sigma$，$\Sigma$ 连续可逆 ⇒ $\hat\Sigma^{-1}\to_p\Sigma^{-1}$。  
$n^{-1}\sum\mathbf{X}_i'\hat\Sigma^{-1}\mathbf{X}_i\to_p E[\mathbf{X}'\Sigma^{-1}\mathbf{X}]$。  
故
$$
n\hat V
=\Bigl(n^{-1}\sum\mathbf{X}_i'\hat\Sigma^{-1}\mathbf{X}_i\Bigr)^{-1}
\to_p\bigl(E[\mathbf{X}'\Sigma^{-1}\mathbf{X}]\bigr)^{-1}=V_\beta^*.
$$
□

---

## Exercise 11.14　两步：$\pi=E[X\mid Z]=\Gamma'Z$，$Y=\pi'\beta+e$

$Y=\pi'\beta+e$，$E[e\mid Z]=0$，$\pi$ 不可观测；  
$\hat\Gamma$ 为 $X$ 对 $Z$ 的多元 OLS，$\hat\pi=\hat\Gamma'Z$，再 $Y$ 对 $\hat\pi$ 做 OLS 得 $\hat\beta$。

### (a) 一致性

多元 OLS：$\hat\Gamma\to_p\Gamma$（投影/条件均值线性时）。  
$\hat\pi_i=\hat\Gamma'Z_i\to_p\Gamma'Z_i=\pi_i$。  
第二步是生成回归元的 OLS。因 $E[e\mid Z]=0$ 且 $\pi$ 是 $Z$ 的函数，  
$E[\pi e]=0$，真回归 $Y=\pi'\beta+e$ 满足投影条件。  
标准两步论证（生成回归元一致 + 矩条件）：$\hat\beta\to_p\beta$。  
（亦可视作 2SLS / 控制函数极限。）

### (b) $\beta=0$ 时 $\sqrt{n}(\hat\beta-\beta)$ 的极限

当 $\beta=0$ 时 $Y=e$，$E[e\mid Z]=0$。  
$\hat\beta=(\hat\Pi'\hat\Pi)^{-1}\hat\Pi'Y$（$\hat\Pi$ 为 $\hat\pi_i$ 的设计阵）。  
$$
\sqrt{n}\hat\beta
=\Bigl(n^{-1}\sum\hat\pi_i\hat\pi_i'\Bigr)^{-1}
\Bigl(n^{-1/2}\sum\hat\pi_ie_i\Bigr).
$$
$n^{-1}\sum\hat\pi\hat\pi'\to_p E[\pi\pi']=E[\Gamma'ZZ'\Gamma]=:\ Q_\pi$。  
关键：$\hat\pi_i-\pi_i=(\hat\Gamma-\Gamma)'Z_i=O_p(n^{-1/2})\|Z_i\|$。  
$$
n^{-1/2}\sum\hat\pi_ie_i
=n^{-1/2}\sum\pi_ie_i
+n^{-1/2}\sum(\hat\pi_i-\pi_i)e_i.
$$
第二项：因 $E[e\mid Z]=0$ 且 $\hat\Gamma-\Gamma$ 是 $Z$ 与 $X$ 的函数，在 $\beta=0$ 时  
$n^{-1/2}\sum Z_ie_i\to_d$ 正态，与 $\sqrt{n}(\hat\Gamma-\Gamma)$ 的联合结构使  
$n^{-1/2}\sum(\hat\pi_i-\pi_i)e_i=o_p(1)$  
（生成回归元在 **真系数 $\beta=0$** 时对得分的一阶影响消失——因为 $Y$ 的信号项 $\pi'\beta=0$）。  

故
$$
\sqrt{n}\hat\beta\to_d N\bigl(0,\ Q_\pi^{-1}E[\pi\pi'e^2]Q_\pi^{-1}\bigr).
$$
同方差时 $= \sigma_e^2 Q_\pi^{-1}$。

### (c) 为何 $\beta=0$ 重要

若 $\beta\neq 0$，则 $Y=\pi'\beta+e$，$\hat\pi$ 的估计误差通过  
$\sqrt{n}(\hat\beta-\beta)$ 的展开产生 **额外项**（两步估计的修正项，取决于 $\mathrm{Avar}(\hat\Gamma)$ 与 $\beta$）。  
$\beta=0$ 使该修正项为零，渐近方差与“$\pi$ 已知”时相同，大大简化。

### (d) $H_0:\beta=0$ 的检验

在 $H_0$ 下用 (b) 的极限：  
$$
W=n\hat\beta'\hat V^{-1}\hat\beta,\qquad
\hat V=\hat Q_\pi^{-1}\Bigl(n^{-1}\sum\hat\pi_i\hat\pi_i'\hat e_i^2\Bigr)\hat Q_\pi^{-1}
$$
（$\hat e_i=Y_i-\hat\pi_i'\hat\beta$，或在 $H_0$ 下 $\hat e_i=Y_i$）。  
$W\to_d\chi^2_k$，拒绝大 $W$。  
这本质上是 **$Y$ 对 $\hat\pi$ 回归的稳健 Wald**，在 $H_0$ 下渐近有效。

---

## Exercise 11.15　两方程共同 $X$

$$
Y_1=X'\beta_1+e_1,\ E[Xe_1]=0;\qquad
Y_2=X'\beta_2+e_2,\ E[Xe_2]=0.
$$

### (a)

方程各自 OLS（共同 $X$ 时系统 OLS = 方程 OLS）：  
$$
\hat\beta_j=(X'X)^{-1}X'Y_j,\quad j=1,2.
$$

### (b) 联合渐近分布

堆叠 $\hat\beta=(\hat\beta_1',\hat\beta_2')'$。由 Thm 11.1 与 (11.14)（同方差时）  
$V_\beta=\Sigma\otimes(E[XX'])^{-1}$，$\Sigma=\mathrm{Var}((e_1,e_2)')$。  
一般异方差：
$$
\sqrt{n}\begin{pmatrix}\hat\beta_1-\beta_1\\ \hat\beta_2-\beta_2\end{pmatrix}
\to_d N(0,V),\quad
V=Q_{xx}^{-1}\Omega Q_{xx}^{-1}\ \text{（适当 Kronecker/分块）},
$$
其中
$$
\Omega=E\begin{pmatrix}
XXe_1^2 & XXe_1e_2\\
XXe_2e_1 & XXe_2^2
\end{pmatrix}
=E[ee'\otimes XX'].
$$
直观：$\sqrt{n}(\hat\beta_j-\beta_j)=Q_{xx}^{-1}n^{-1/2}\sum Xe_j+o_p(1)$，联合正态，  
$\mathrm{ACov}(\hat\beta_1,\hat\beta_2)=Q_{xx}^{-1}E[XX'e_1e_2]Q_{xx}^{-1}$。

### (c) $H_0:\beta_1=\beta_2$

令 $\hat\delta=\hat\beta_1-\hat\beta_2$，  
$\widehat{\mathrm{Avar}}(\hat\delta)=\hat V_{11}+\hat V_{22}-\hat V_{12}-\hat V_{21}$（取自联合 $\hat V$）。  
Wald：
$$
W=n\hat\delta'\widehat{\mathrm{Avar}}(\hat\delta)^{-1}\hat\delta\to_d\chi^2_k.
$$
或约束 SUR/系统估计：施加 $\beta_1=\beta_2$ 与无约束比较（MD/LR 型）。

**同方差特例：**  
$\mathrm{Avar}(\hat\delta)=(\sigma_1^2+\sigma_2^2-2\sigma_{12})(E[XX'])^{-1}$，  
用 $\hat\Sigma$ 的元素构造即可。

---

## 小结

| 题 | 结论 |
|:--:|------|
| 11.1–11.3 | $\Omega$ 在同方差/共同 $X$ 下的简化 |
| 11.4–11.8 | 系统 OLS 渐近理论与协方差一致 |
| 11.9–11.10 | SUR/GLS 两等价公式 |
| 11.11–11.13 | SUR 极限、相对 OLS 有效、方差估计 |
| 11.14 | 生成 $\hat\pi$ 的两步估计；$\beta=0$ 简化渐近 |
| 11.15 | 两方程联合分布与 $\beta_1=\beta_2$ 的 Wald |

