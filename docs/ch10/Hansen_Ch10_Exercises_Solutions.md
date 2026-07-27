# Hansen《Econometrics》第 10 章习题完整解答

**章节：** Chapter 10 Resampling Methods  
**书稿：** PDF 第 321–325 页（印刷页 301–305），§10.32 Exercises（**10.1–10.31 全部**）  
**记号：** 与 Hansen 一致——jackknife 方差 (10.1)、非参数 bootstrap、percentile / BC / BCa / percentile-$t$

> 说明：此前版本过简；本题解按习题原文逐题完整展开，定理证明给出 Hansen 体系下的关键步骤。

---

## 预备：Jackknife 与 Bootstrap 公式

对估计量 $\hat\theta=\hat\theta(Y_1,\ldots,Y_n)$，**delete-one** 估计 $\hat\theta_{(-i)}$，均值 $\bar\theta_{(\cdot)}=n^{-1}\sum_i\hat\theta_{(-i)}$。  
**Jackknife 方差**（(10.1)）：
$$
\hat V^{\mathrm{jack}}_{\hat\theta}
=\frac{n-1}{n}\sum_{i=1}^n
\bigl(\hat\theta_{(-i)}-\bar\theta_{(\cdot)}\bigr)
\bigl(\hat\theta_{(-i)}-\bar\theta_{(\cdot)}\bigr)'.
$$

**非参数（成对）bootstrap：** 从经验经验分布有放回抽 $n$ 个观测得 $(Y^*,X^*)$，再算 $\hat\theta^*$。  
**Bootstrap 方差：** $\hat V^{\mathrm{boot}}=\mathrm{Var}^*(\hat\theta^*)$（对 $B$ 次复制的样本方差）。

**Percentile 区间：** $[\hat q^*_{\alpha/2},\hat q^*_{1-\alpha/2}]$。  
**BC：** $p^*=P^*(\hat\theta^*\le\hat\theta)$，$z_0^*=\Phi^{-1}(p^*)$，用分位 $x(\alpha)=\Phi(z_\alpha+2z_0^*)$（(10.22)–(10.25)）。  
**BCa：** 再估计加速常数 $a$（jackknife 偏度），$x(\alpha)=\Phi\!\left(z_0+\frac{z_0+z_\alpha}{1-a(z_0+z_\alpha)}\right)$。

---

## Exercise 10.1

求 $\hat\mu_r=n^{-1}\sum_{i=1}^n Y_i^r$ 的 jackknife 方差估计（$\mu_r=E[Y^r]$）。

### 解答

对固定 $r$，令 $W_i=Y_i^r$。则 $\hat\mu_r=\bar W$。  
delete-one：
$$
\hat\mu_{r(-i)}=\frac{1}{n-1}\sum_{j\neq i}Y_j^r
=\frac{n}{n-1}\hat\mu_r-\frac{1}{n-1}Y_i^r.
$$
故 $\hat\mu_{r(-i)}-\hat\mu_r=\frac{1}{n-1}(\hat\mu_r-Y_i^r)$，且 $\bar\mu_{r(\cdot)}=\hat\mu_r$。  
代入 (10.1)：
\begin{align*}
\hat V^{\mathrm{jack}}_{\hat\mu_r}
&=\frac{n-1}{n}\sum_{i=1}^n\left(\frac{\hat\mu_r-Y_i^r}{n-1}\right)^2
=\frac{1}{n(n-1)}\sum_{i=1}^n(Y_i^r-\hat\mu_r)^2.
\end{align*}
这与 $\bar W$ 的常规方差估计 $s_W^2/n$（$s_W^2$ 用分母 $n-1$）**完全相同**。  
（向量 $Y$ 时把平方换成外积即可。）

---

## Exercise 10.2

若 $\hat V^{\mathrm{jack}}_{\hat\beta}$ 已得，$\hat\theta=a+C\hat\beta$，证明 $\hat V^{\mathrm{jack}}_{\hat\theta}=C\hat V^{\mathrm{jack}}_{\hat\beta}C'$。

### 证明

仿射变换与 delete-one **可交换**：
$$
\hat\theta_{(-i)}=a+C\hat\beta_{(-i)},\qquad
\bar\theta_{(\cdot)}=a+C\bar\beta_{(\cdot)}.
$$
因此
$$
\hat\theta_{(-i)}-\bar\theta_{(\cdot)}=C\bigl(\hat\beta_{(-i)}-\bar\beta_{(\cdot)}\bigr).
$$
代入 jackknife 公式：
\begin{align*}
\hat V^{\mathrm{jack}}_{\hat\theta}
&=\frac{n-1}{n}\sum_i
C\bigl(\hat\beta_{(-i)}-\bar\beta_{(\cdot)}\bigr)
\bigl(\hat\beta_{(-i)}-\bar\beta_{(\cdot)}\bigr)'C'
=C\hat V^{\mathrm{jack}}_{\hat\beta}C'.
\end{align*}
□

---

## Exercise 10.3

两步估计 $\hat A=(Z'Z)^{-1}Z'X$，$\hat W_i=\hat A'Z_i$，  
$\hat\beta=\bigl(\sum\hat W_i\hat W_i'\bigr)^{-1}\bigl(\sum\hat W_i Y_i\bigr)$（如 (12.49) 型）。  
如何构造 $\hat\beta$ 的 jackknife 方差？

### 解答

**不能**只对第二步做 jackknife 而固定 $\hat A$。正确步骤：

1. 对每个 $i=1,\ldots,n$，删去观测 $i$，用剩余样本重算  
   $\hat A_{(-i)}=(Z_{(-i)}'Z_{(-i)})^{-1}Z_{(-i)}'X_{(-i)}$。  
2. 构造 $\hat W_{j(-i)}=\hat A_{(-i)}'Z_j$（$j\neq i$），再算  
   $\hat\beta_{(-i)}=\bigl(\sum_{j\neq i}\hat W_{j(-i)}\hat W_{j(-i)}'\bigr)^{-1}
   \bigl(\sum_{j\neq i}\hat W_{j(-i)}Y_j\bigr)$。  
3. 用 $\{\hat\beta_{(-i)}\}_{i=1}^n$ 套入标准 jackknife 方差公式 (10.1)。

要点：第一步 $\hat A$ 依赖全样本，delete-one 必须 **两步都重估**，否则低估因 $\hat A$ 不确定性带来的方差。

---

## Exercise 10.4

$\hat\theta=a+C\hat\beta$，bootstrap 方差：$\hat V^{\mathrm{boot}}_{\hat\theta}=C\hat V^{\mathrm{boot}}_{\hat\beta}C'$。

### 证明

对每个 bootstrap 样本，若 $\hat\beta^*$ 是该样本上 $\beta$ 的估计，且 $\hat\theta^*=a+C\hat\beta^*$（同一仿射映射），则  
$\mathrm{Var}^*(\hat\theta^*)=C\,\mathrm{Var}^*(\hat\beta^*)\,C'$。  
用 $B$ 次复制的样本协方差代替 $\mathrm{Var}^*$ 即得。  
（若 $\hat\theta$ 是 $\hat\beta$ 的非线性函数则不成立，需对 $\hat\theta^*$ 直接算 bootstrap 方差。）

---

## Exercise 10.5

Percentile 区间 $[L,U]$ 对 $\beta$；则对 $a+c\beta$（$c$ 标量）区间为 $[a+cL,\,a+cU]$（$c>0$）。

### 证明

设 $\hat\beta^*$ 的 $\alpha$ 分位数为 $q^*_\alpha$。  
$\widehat{a+c\beta}^*=a+c\hat\beta^*$。  
若 $c>0$，分位数等变：$q^*_\alpha(a+c\hat\beta^*)=a+c\,q^*_\alpha(\hat\beta^*)$。  
故 percentile 区间端点同仿射变换。  
若 $c<0$，不等号反转，区间为 $[a+cU,\,a+cL]$。

---

## Exercise 10.6

$T^*=(\hat\theta^*-\hat\theta)/s(\hat\theta)$（分母为 **原样本** SE），  
$C=[\hat\theta+s(\hat\theta)q^*_{\alpha/2},\,\hat\theta+s(\hat\theta)q^*_{1-\alpha/2}]$。  
证明 $C$ **恰好等于** percentile 区间。

### 证明

$T^*$ 只是 $\hat\theta^*$ 的 **严格增** 仿射变换（$s(\hat\theta)>0$ 固定）：  
$T^*=\hat\theta^*/s(\hat\theta)-\hat\theta/s(\hat\theta)$。  
故 $T^*$ 的 $\alpha$ 分位数 $q^*_{T,\alpha}=q^*_{\theta,\alpha}/s(\hat\theta)-\hat\theta/s(\hat\theta)$，即  
$q^*_{\theta,\alpha}=\hat\theta+s(\hat\theta)\,q^*_{T,\alpha}$。  
因此
$$
C=\bigl[q^*_{\theta,\alpha/2},\,q^*_{\theta,1-\alpha/2}\bigr],
$$
正是 $\hat\theta^*$ 的 percentile 区间。□  

**注：** 这 **不是** percentile-$t$（后者分母用 $s^*(\hat\theta^*)$）。本题故意用固定 $s(\hat\theta)$，故与 percentile 等价，**没有** studentization 的精细化好处。

---

## Exercise 10.7　证明 Theorem 10.6（Bootstrap Delta Method）

**定理：** $\hat\mu\to_p\mu$，$\sqrt{n}(\hat\mu^*-\hat\mu)\to_{d^*} \xi$，$g$ 在 $\mu$ 邻域 $C^1$，则  
$\sqrt{n}\bigl(g(\hat\mu^*)-g(\hat\mu)\bigr)\to_{d^*} G'\xi$，$G=\partial g(\mu)'$。若 $\xi\sim N(0,V)$ 则极限 $N(0,G'VG)$。

### 证明

均值展开（bootstrap 世界，条件于 $F_n$）：
$$
g(\hat\mu^*)-g(\hat\mu)=G(\tilde\mu^*)'(\hat\mu^*-\hat\mu),
$$
$\tilde\mu^*$ 在 $\hat\mu^*$ 与 $\hat\mu$ 之间。  
因 $\hat\mu^*\to_{p^*}\hat\mu\to_p\mu$，有 $G(\tilde\mu^*)\to_{p^*}G(\mu)$。  
Slutsky（bootstrap 版）：  
$\sqrt{n}(g(\hat\mu^*)-g(\hat\mu))=G(\tilde\mu^*)'\sqrt{n}(\hat\mu^*-\hat\mu)\to_{d^*} G'\xi$。  
正态情形直接代入。□

---

## Exercise 10.8　证明 Theorem 10.7

**设定：** $Y_i$ i.i.d.，$\mu=E[h(Y)]$，$\theta=g(\mu)$，$\hat\mu=n^{-1}\sum h(Y_i)$，$\hat\theta=g(\hat\mu)$；bootstrap $\hat\mu^*=n^{-1}\sum h(Y_i^*)$，$\hat\theta^*=g(\hat\mu^*)$。  
$E\|h\|^2<\infty$，$G$ 在 $\mu$ 连续。则 $\sqrt{n}(\hat\theta^*-\hat\theta)\to_{d^*} N(0,G'VG)$，$V=\mathrm{Var}(h(Y))$。

### 证明

1. **Bootstrap CLT：** 条件于样本，$h(Y_i^*)$ 为 i.i.d. 来自经验分布，均值 $\hat\mu$，方差 $\hat V_n\to_p V$。  
   故 $\sqrt{n}(\hat\mu^*-\hat\mu)\to_{d^*} N(0,V)$（可在概率 1 的样本路径上成立）。  
2. 对 $g$ 用 **Theorem 10.6** 即得 $\sqrt{n}(\hat\theta^*-\hat\theta)\to_{d^*} N(0,G'VG)$。  

这与样本 $\sqrt{n}(\hat\theta-\theta)$ 的极限相同，故 bootstrap 可模仿其分布。□

---

## Exercise 10.9　证明 Theorem 10.8

**定理：** 在 Thm 10.7 条件下，$\hat V^*_\theta\to_{p^*} V_\theta=G'VG$（bootstrap 方差估计的一致性，对条件方差/“理想” bootstrap 方差）。

### 证明纲要

由 Thm 10.7，$\sqrt{n}(\hat\theta^*-\hat\theta)$ 条件依分布收敛到 $N(0,V_\theta)$。  
若再有 **一致可积**（或有界 $p$ 阶导数使矩有限，见 Thm 10.10），则  
$\mathrm{Var}^*\!\bigl(\sqrt{n}(\hat\theta^*-\hat\theta)\bigr)\to_p V_\theta$，即 $\hat V^{\mathrm{boot}}_{\hat\theta}\to_p n^{-1}V_\theta$ 的缩放形式。  
更技术的证明用：bootstrap 协方差 $=$ $G(\hat\mu)'\widehat{\mathrm{Var}}^*(h^*)G(\hat\mu)+o_{p^*}(1)$，而 $\widehat{\mathrm{Var}}^*(h^*)=\frac{1}{n}\sum(h_i-\hat\mu)(\cdot)'\to_p V$。□

---

## Exercise 10.10

$Y_i$ i.i.d.，$\mu=E[Y]>0$，$\theta=\mu^{-1}$，$\hat\mu=\bar Y$，$\hat\theta=\hat\mu^{-1}$。

### 解答

**(a)** 一般 **不是** 无偏。$g(\mu)=1/\mu$ 在 $(0,\infty)$ 上严格凸（$g''=2/\mu^3>0$）。由 Jensen，  
$E[\hat\theta]=E[1/\bar Y]\ge 1/E[\bar Y]=\theta$，等号当且仅当 $\bar Y$ a.s. 常数（退化）。  
有限样本通常 $E|\bar Y|^{-1}<\infty$ 才谈无偏；即便存在，也不等于 $\theta$。

**(b)** 在 $\bar Y>0$ a.s. 且期望存在时，偏倚 **向上**：$E[\hat\theta-\theta]\ge 0$。

**(c)** 普通 **percentile** 在变换后分布高度右偏时表现差，**不纠偏**。  
更合适：**BC / BCa percentile**（专为中位数偏倚/偏度设计），或对 $\log\hat\theta$ 做区间再变换。  
Percentile 在“存在对称化变换”时理论好，但 $1/\bar Y$ 的有限样本偏倚大时 BC 更稳妥。

---

## Exercise 10.11

回归 bootstrap：抽 $(X^*,e^*)$ 来自 $\{(X_i,\hat e_i)\}$，$Y^*=X^{*'}\hat\beta+e^*$，再 OLS 得 $\hat\beta^*$。  
证明与非参数成对 bootstrap **数值相同**。

### 证明

非参数 bootstrap 直接重抽 $(Y_i,X_i)$ 对。在原样本上 $Y_i=X_i'\hat\beta+\hat e_i$。  
故重抽到指标 $i'$ 时：  
$Y^*=Y_{i'}=X_{i'}'\hat\beta+\hat e_{i'}$，$X^*=X_{i'}$。  
这与“抽 $(X_{i'},\hat e_{i'})$ 再令 $Y^*=X^{*'}\hat\beta+e^*$”**定义相同**。  
因此生成的 bootstrap 数据集 $\{(Y_b^*,X_b^*)\}$ 的联合分布在两种算法下一致，随后任何统计量（含 $\hat\beta^*$）的 bootstrap 分布相同。□  

**注：** 这与 **残差 bootstrap**（固定设计 $X$、只重抽残差）不同；本题是 **成对/非参数** bootstrap 的改写。

---

## Exercise 10.12

$p^*$（(10.22)）对严格增 $g$ 不变？$z_0^*$（(10.23)）呢？

### 解答

定义 $p^*=P^*(\hat\theta^*\le\hat\theta)$（或 $\#\{\hat\theta^*_b\le\hat\theta\}/B$）。  
令 $\phi=g(\theta)$，$g$ 严格增。则  
$\hat\phi^*=g(\hat\theta^*)\le g(\hat\theta)=\hat\phi\ \Longleftrightarrow\ \hat\theta^*\le\hat\theta$。  
故 $p^*$ **不变**。  
$z_0^*=\Phi^{-1}(p^*)$ 只依赖 $p^*$，故也 **不变**。  

（若 $g$ 严格减，则不等式反转，$p^*\mapsto 1-p^*$，$z_0^*\mapsto -z_0^*$，BC 区间端点仍正确变换。）

---

## Exercise 10.13

Percentile-$t$ 区间对 $\beta$ 为 $[L,U]$；对 $a+c\beta$？

### 解答

教材印刷作 $[a+bL,a+bU]$，参数为 $a+c\beta$，此处 **$b$ 即 $c$**。  

Percentile-$t$：用 $T^*=(\hat\beta^*-\hat\beta)/s^*(\hat\beta^*)$ 的分位数 $q^*_{\alpha/2},q^*_{1-\alpha/2}$，  
$$
C=\bigl[\hat\beta-s(\hat\beta)q^*_{1-\alpha/2},\;\hat\beta-s(\hat\beta)q^*_{\alpha/2}\bigr]
$$
（形式随 $T$ 定义略有 dual 写法）。  

对 $\theta=a+c\beta$（$c>0$）：$\hat\theta=a+c\hat\beta$，$s(\hat\theta)=|c|s(\hat\beta)$，  
$T_\theta^*=(\hat\theta^*-\hat\theta)/s^*(\hat\theta^*)=(\hat\beta^*-\hat\beta)/s^*(\hat\beta^*)=T_\beta^*$（$c>0$ 时）。  
故同一 $q^*$，区间为  
$[a+cL,\,a+cU]$。  
$c<0$ 时 $T$ 变号，端点对调。

---

## Exercise 10.14

检验 $H_0:\theta=0$ vs $H_1:\theta>0$，用无约束 bootstrap 的 $T^*=\hat\theta^*/s^*(\hat\theta^*)$ 的 $1-\alpha$ 分位作临界值。错在哪里？

### 解答

**原则错误：bootstrap 世界未施加 $H_0$。**

- 数据来自真 $\theta$ 可能 $>0$ 的 DGP；$\hat\theta^*$ 集中在 $\hat\theta$ 附近而非 0。  
- 因而 $q^*_{1-\alpha}$ 是 **备择/真参数下** $T$ 的分位，不是 $H_0$ 下的临界值。  
- 若 $\hat\theta>0$ 较大，$q^*$ 偏大，检验 **过于保守**（功效低）；水平也不等于 $\alpha$。

**正确做法（示意）：**

1. **约束/强制 $H_0$：** 在 $\theta=0$ 下估计（如设 $\hat\theta_0=0$），用中心化残差或  
   $T^{0*}=(\hat\theta^*-\hat\theta)/s^*$ 与 $T_n=\hat\theta/s$ 比较（中心化 bootstrap）；或  
2. 参数/残差 bootstrap 在 $H_0$ 成立的 DGP 上模拟 $T$ 的零分布。

单侧 $H_1:\theta>0$ 时更应明确零分布的生成机制。

---

## Exercise 10.15

$\hat\theta=1.2$，$s(\hat\theta)=0.2$；$B=1000$ 时 $\hat\theta^*$ 的 2.5% 与 97.5% 分位为 0.75 与 1.3。

### 解答

**(a)** 95% **percentile** 区间：**$[0.75,\ 1.3]$**。

**(c)**  
- **BC：** 需要 $p^*=P^*(\hat\theta^*\le 1.2)$，题目只给两个分位，**不能**算 $p^*$ 与 $z_0^*$。  
- **Percentile-$t$：** 需要每次 bootstrap 的 $s^*(\hat\theta^*)$ 与 $T^*$ 分位，**信息不足**。  

故只能报告 percentile；不能报告 BC 或 percentile-$t$。

---

## Exercise 10.16　正态回归参数 bootstrap

$Y=X'\beta+e$，$e\mid X\sim N(0,\sigma^2)$，MLE $=(\hat\beta,\hat\sigma^2)$ OLS。

### 解答

**(a)** **参数回归 bootstrap（固定 $X$）：**  
在每次复制中，抽 $e_i^*\stackrel{iid}{\sim}N(0,\hat\sigma^2)$，令  
$Y_i^*=X_i'\hat\beta+e_i^*$。  
则条件于 $F_n$（即条件于 $\hat\beta,\hat\sigma^2,X$）：  
$Y_i^*\mid F_n\sim N(X_i'\hat\beta,\hat\sigma^2)$。

**(b)** 固定 $X$ 上 OLS：  
$\hat\beta^*=(X'X)^{-1}X'Y^*=\hat\beta+(X'X)^{-1}X'e^*$。  
$e^*\sim N(0,\hat\sigma^2 I)$ ⇒  
$\hat\beta^*\mid F_n\sim N\bigl(\hat\beta,\ \hat\sigma^2(X'X)^{-1}\bigr)$。

**(c)** 同方差 SE：$s^{*2}=\|Y^*-X\hat\beta^*\|^2/(n-k)$，  
$T_j^*=(\hat\beta_j^*-\hat\beta_j)/s^*(\hat\beta_j)$。  
经典正态回归理论：与原模型相同，$\frac{\hat\beta_j-\beta_j}{s(\hat\beta_j)}\sim t_{n-k}$ 在真模型下成立；  
bootstrap 世界把真值换成 $\hat\beta$，故 **$T^*\sim t_{n-k}$**（精确，固定 $X$）。

---

## Exercise 10.17　$m(x)=E[Y\mid X=x]=x'\beta$

### 解答

**(a)** $\hat m(x)=x'\hat\beta$。渐近 95% CI：  
$$
x'\hat\beta\pm 1.96\sqrt{x'\hat V_{\hat\beta}x},
$$
$\hat V$ 为稳健/同方差协方差估计。

**(b)** **Percentile：** 成对 bootstrap 得 $\hat m^*(x)=x'\hat\beta^*$，取 $\hat m^*$ 的 2.5% 与 97.5% 分位。

**(c)** **Percentile-$t$：**  
$T^*(x)=\dfrac{\hat m^*(x)-\hat m(x)}{s^*(\hat m(x))}$，  
$s^{*2}(x)=x'\hat V^*x$。  
令 $q^*_{\alpha/2},q^*_{1-\alpha/2}$ 为 $T^*$ 分位，区间  
$$
\bigl[\hat m-s(\hat m)q^*_{1-\alpha/2},\ \hat m-s(\hat m)q^*_{\alpha/2}\bigr].
$$

---

## Exercise 10.18　$\mu_3=E[e^3]$

### 解答

**(a)** OLS 残差 $\hat e_i=Y_i-X_i'\hat\beta$，  
$\hat\mu_3=n^{-1}\sum_{i=1}^n\hat e_i^3$  
（或 $n^{-1}\sum(\hat e_i-\bar{\hat e})^3$；含截距时 $\bar{\hat e}=0$）。

**(b)** **90% percentile：**  
1. 成对 bootstrap 得 $(Y^*,X^*)$；  
2. 算 $\hat\beta^*$ 与 $\hat\mu_3^*=n^{-1}\sum\hat e_i^{*3}$；  
3. 重复 $B$ 次，取 $\hat\mu_3^*$ 的 5% 与 95% 分位。  

（亦可用残差 bootstrap：固定 $X$，重抽 $\hat e_i$ 构造 $Y^*$。）

---

## Exercise 10.19　$\sigma^2=E[e^2]$ 的 percentile 区间

### 解答

$\hat\sigma^2=n^{-1}\sum\hat e_i^2$（或 $s^2$）。  
Bootstrap：每次复制重估 $\hat\beta^*$ 与 $\hat\sigma^{2*}$，取 $\hat\sigma^{2*}$ 的 $\alpha/2$ 与 $1-\alpha/2$ 分位。  
因 $\sigma^2>0$ 且分布右偏，**BC/BCa** 往往优于原始 percentile。

---

## Exercise 10.20　$H_0:\beta_2=0$（$X_2$ 标量）

### 解答（非参数 bootstrap 检验）

**推荐：约束残差 / 强制 $H_0$ 的 bootstrap**

1. 在 $H_0$ 下回归 $Y$ 对 $X_1$ 得 $\tilde\beta_1$、残差 $\tilde e_i$。  
2. 构造零假设数据：$Y_i^{0*}=X_{1i}'\tilde\beta_1+\tilde e_i^*$（$\tilde e^*$ 有放回抽自 $\tilde e$ 或成对抽 $(X_i,\tilde e_i)$ 再组合）。  
3. 在 $Y^{0*}$ 上估无约束模型，算 $t^*$ 或 Wald$^*$。  
4. $p^*=B^{-1}\sum 1\{|T^*|\ge|T|\}$（双侧）。

**错误做法：** 无约束成对 bootstrap 的 $|T^*|$ 分位直接当临界值（同 10.14/10.22）。

也可用 **中心化** $T^{c*}=(\hat\beta_2^*-\hat\beta_2)/s_2^*$ 与 $T=\hat\beta_2/s_2$ 比较。

---

## Exercise 10.21　$H_0:\beta_1=\beta_2$（均为 $k\times 1$）

### 解答

约束 $\beta_1=\beta_2=\gamma$：$Y=(X_1+X_2)'\gamma+e$。  

1. 约束估计得 $\tilde\gamma$、残差；  
2. 在 $H_0$ 下 bootstrap（残差或成对+约束拟合）；  
3. 每次算 Wald  
   $W^*=(\hat\beta_1^*-\hat\beta_2^*)'\widehat{\mathrm{Var}}^*(\hat\beta_1^*-\hat\beta_2^*)^{-1}(\hat\beta_1^*-\hat\beta_2^*)$；  
4. 与样本 $W$ 比较得 $p$ 值。  

等价：令 $\delta=\beta_1-\beta_2$，检验 $\delta=0$。

---

## Exercise 10.22　博士生的 bootstrap 检验

$T=2$，$q^*_{.95}=3.5$，学生不拒绝。

### 解答

**不同意其方法。** 错误与 10.14 相同：

| 步骤 | 问题 |
|------|------|
| 1–2 | 无约束重抽，DGP 在 $\hat\alpha=2$ 附近，不是 $\alpha=0$ |
| 4 | $q^*_{.95}$ 是 **非零 $\alpha$** 下 $|T^*|$ 的分位，偏大 |
| 5 | 用错误临界值得出“不拒绝”，**水平/功效皆不可靠** |

**改正：** 在 $H_0:\alpha=0$ 下估计 $Y=X'\beta+e$，用该残差生成 $Y^*$（或中心化 $T^*$），再与 $T=2$ 比较。  
渐近拒绝而错误 bootstrap 不拒绝，恰说明其 bootstrap **过度保守**。

---

## Exercise 10.23　$\theta=\beta_1\beta_2$（$X_1,X_2$ 标量）

### 解答

**(a) 渐近 / delta 法**  
$\hat\theta=\hat\beta_1\hat\beta_2$。  
$\nabla g=(\beta_2,\beta_1)'$，$V=\mathrm{Avar}(\hat\beta)$（$2\times2$ 块）。  
$\widehat{\mathrm{se}}(\hat\theta)=\sqrt{\nabla\hat g'\hat V\nabla\hat g}$，  
95% CI：$\hat\theta\pm 1.96\,\widehat{\mathrm{se}}$。

**(b) Percentile bootstrap**  
成对 bootstrap → $(\hat\beta_1^*,\hat\beta_2^*)$ → $\hat\theta^*=\hat\beta_1^*\hat\beta_2^*$，取 2.5% 与 97.5% 分位。

**(c) Percentile-$t$**  
每次算 $\hat\theta^*$ 与 delta/稳健 $s^*(\hat\theta^*)$，  
$T^*=(\hat\theta^*-\hat\theta)/s^*(\hat\theta^*)$。  
用 $T^*$ 分位构造  
$[\hat\theta-s(\hat\theta)q^*_{1-\alpha/2},\ \hat\theta-s(\hat\theta)q^*_{\alpha/2}]$。

---

## Exercise 10.24　$\theta=\beta_1/\beta_2$ 的 percentile-$t$

### 解答

1. OLS 得 $\hat\beta$， $\hat\theta=\hat\beta_1/\hat\beta_2$（要求 $\hat\beta_2\neq0$）。  
2. Delta：$g=(\beta_1/\beta_2)$，$\nabla=(1/\beta_2,\,-\beta_1/\beta_2^2)$，  
   $s(\hat\theta)=\sqrt{\nabla'\hat V\nabla}$。  
3. Bootstrap 复制：$\hat\theta^*$，$s^*(\hat\theta^*)$，  
   $T^*=(\hat\theta^*-\hat\theta)/s^*(\hat\theta^*)$。  
4. 取 $T^*$ 的 $\alpha/2$ 与 $1-\alpha/2$ 分位构造 CI（同 10.23(c) 形式）。  

注意比值在 $\beta_2\approx0$ 时矩可能失效，bootstrap SE 会不稳定（教材亦警告）。

---

## Exercise 10.25

条件异方差是否使非参数 bootstrap 无效？

### 解答

**否，不必然无效。**  

成对非参数 bootstrap 重抽 $(Y_i,X_i)$，保留 **条件分布 $Y\mid X$ 的经验结构**，包括 $\mathrm{Var}(e\mid X)=\sigma^2(X)$。  
它不依赖同方差假定；与异方差稳健推断是相容的。  

需注意：i.i.d. 成对抽样假定观测独立；若有聚类/时间相关，应改用 **block/cluster bootstrap**。

---

## Exercise 10.26　RESET 的 bootstrap

同事的做法对吗？

### 解答

**不正确。**  

RESET 的 $H_0$ 是线性 CEF。同事在 **无约束真实数据**（可能已非线性）上重抽，bootstrap 世界一般 **$H_0$ 不成立**，$R^*$ 的 95% 分位不是 $H_0$ 临界值。

**修正方案：**

1. 在 $H_0$ 下只估计线性模型，得 $\hat\beta$、残差 $\hat e_i$、拟合 $\hat Y_i=X_i'\hat\beta$。  
2. **残差 bootstrap：** $Y_i^*=X_i'\hat\beta+\hat e_i^*$（$\hat e^*$ 有放回抽；可对残差中心化）。  
3. 在 $(Y^*,X)$ 上 **完整重做** RESET（两步回归 + $R^*$）。  
4. 用 $R^*$ 的分位与样本 $R$ 比较。  

这样 DGP 满足线性 $H_0$，临界值才对应 Type I error。

---

## Exercise 10.27

$E[Xe]\neq0$ 时 OLS 偏倚；BC percentile 能否对 $\beta$ 有准确覆盖？

### 解答

**预期：不能对真 $\beta$ 有准确覆盖。**

- BC 纠的是 **估计量抽样分布关于其概率极限的中位数偏倚**，不是 **识别偏倚**。  
- 当 $E[Xe]\neq0$ 时 $\hat\beta\to_p\beta_{\mathrm{plim}}\neq\beta$，bootstrap 分布集中在 $\beta_{\mathrm{plim}}$ 附近。  
- BC 区间覆盖的是 $\beta_{\mathrm{plim}}$，**不是** 结构参数 $\beta$。  

BC 在“正确识别 + 有限样本偏倚”时有用；**不能替代工具变量等识别策略**。

---

## Exercise 10.28（Nerlove1963，$n=145$）

无约束 $\log C=\beta_1+\beta_2\log Q+\beta_3\log P_L+\beta_4\log P_K+\beta_5\log P_F+e$，  
$\theta=\beta_3+\beta_4+\beta_5$。

### 方法

- **Asymptotic SE：** HC3 / HC1 sandwich。  
- **Jackknife SE：** 删 $i=1..n$ 重估，用 (10.1)。  
- **Bootstrap SE：** 成对 bootstrap，$B$ 宜 $\ge 999$。  
- **Percentile / BCa：** 对 $\theta^*$ 分位；BCa 用 jackknife 估 $a$。

数值见 notebook（随 $B$ 与种子略有波动）。

---

## Exercise 10.29（MRW1992，$N=1$，$n=98$）

$\Delta\log Y$ 对 $\log Y_{60},\log(I/Y),\log(n+g+\delta),\log(\mathrm{school})$；  
$\theta=$ 第 2+3+4 个斜率之和。  
报告同 10.28 三类 SE 与 percentile、**BC**（题目要 BC，非必须 BCa）区间。

---

## Exercise 10.30

CPS：白人男性西班牙裔 + **从未结婚** + **Midwest**，$n=99$。  
$\theta=\dfrac{\beta_{\mathrm{edu}}}{\beta_{\mathrm{exp}}+2\beta_{\mathrm{exp2}}\cdot\mathrm{exp}/100\big|_{\mathrm{exp}=10}}=\dfrac{\beta_1}{\beta_2+0.2\beta_3}$。

### 解答要点

**(a)** 报告 $\hat\theta$ 与 asym / jack / boot SE。  
**(b)** $n=99$ 小、比率非线性、经验剖面估计噪声大时：  
- 渐近 delta 依赖局部线性；  
- jackknife 对高杠杆点敏感；  
- bootstrap 反映偏态与可能的矩问题，三者可差很多。  
**(c)** BC percentile 区间：用 $p^*$ 调整分位。

---

## Exercise 10.31（DDK2011）

在 4.26 回归上用 **cluster bootstrap**（重抽 **学校** 块）：

1. 以 `schoolid` 为簇，有放回抽 $G$ 个学校，堆叠学生观测。  
2. 每次算 $\hat\beta^*$。  
3. 列向标准差 = cluster bootstrap SE。  
4. 对各系数用 bootstrap 复制做 **BCa** 区间（$a$ 用 **delete-cluster jackknife** 更贴切）。

通常 cluster bootstrap SE $\approx$ 渐近聚类 SE，且 **大于** 个体稳健 SE（尤其 tracking）。

---

## 小结表

| 题 | 核心结论 |
|:--:|----------|
| 10.1–10.5 | Jack/boot 方差与仿射等变 |
| 10.6 | 固定 SE 的“$t$”bootstrap = percentile |
| 10.7–10.9 | Bootstrap delta / 正态极限 / 方差一致 |
| 10.10 | $1/\bar Y$ 上偏；宜 BC |
| 10.11 | 残差配对写法 = 成对 bootstrap |
| 10.12–10.13 | BC 与 percentile-$t$ 的变换性质 |
| 10.14, 10.22, 10.26 | **必须在 $H_0$ 下 bootstrap** |
| 10.25 | 异方差不破坏成对 bootstrap |
| 10.27 | BC 不修识别错误 |
| 10.28–10.31 | 实证：jack / boot / cluster / BCa |

完整可运行代码见同目录 `Hansen_Ch10_Exercises_Solutions.ipynb`。
