# Hansen《Econometrics》第 8 章习题解答

**章节：** Chapter 8 Restricted Estimation  
**书稿：** PDF p238–240（印刷页 218–220），§8.17 Exercises  

计算：`Hansen_Ch08_Exercises_Solutions.ipynb`

---

## Exercise 8.1

约束 $\beta_2=0$ 的 CLS 即在 $\beta=(\beta_1,0)$ 上最小化 $\|Y-X_1\beta_1\|^2$，故 $\tilde\beta_1=(X_1'X_1)^{-1}X_1'Y$，$\tilde\beta_2=0$。

---

## Exercise 8.2

约束 $\beta_1=c$：最小化 $\|Y-X_1c-X_2\beta_2\|^2$ ⇒ $Y-X_1c$ 对 $X_2$ 的 OLS。

---

## Exercise 8.3

$\beta_1=-\beta_2=\gamma$ 时 $Y=X_1\gamma-X_2\gamma+e=(X_1-X_2)\gamma+e$，  
$\tilde\gamma=\bigl((X_1-X_2)'(X_1-X_2)\bigr)^{-1}(X_1-X_2)'Y$，$\tilde\beta_1=\tilde\gamma$，$\tilde\beta_2=-\tilde\gamma$。

---

## Exercise 8.4

**(a)** $\beta=0$ ⇒ $\tilde\alpha=\bar Y$。  
**(b)** EMD 在 $W=\hat V^{-1}$ 下对 $(\alpha,\beta)$ 约束 $\beta=0$；对截距，有效 MD 与样本均值在标准设定下一致（投影到 $\beta=0$ 的子空间）。

---

## Exercise 8.5

由 CLS 公式 $\tilde\beta=\hat\beta-(X'X)^{-1}R(R'(X'X)^{-1}R)^{-1}(R'\hat\beta-c)$，  
$R'\tilde\beta=R'\hat\beta-(R'\hat\beta-c)=c$。

---

## Exercise 8.6–8.9（定理纲要）

- **Thm 8.1：** CLS 显式公式（Lagrange / 分块投影）。  
- **Thm 8.2：** 约束真且 $E[e\mid X]=0$ ⇒ $E[\tilde\beta_{\mathrm{cls}}\mid X]=\beta$。  
- **Thm 8.3：** $\mathrm{var}(\tilde\beta_{\mathrm{cls}}\mid X)$ 的 sandwich/同方差公式。  
- **Thm 8.4：** 同方差下用 CLS 残差的 $s^2_{\mathrm{cls}}$ 无偏（df 调整 $n-k+q$）。

---

## Exercise 8.10–8.17

- MD：$\tilde\beta=\arg\min(\hat\beta-\beta)'W(\hat\beta-\beta)$ s.t. $R'\beta=c$。  
- $W=\hat Q_{XX}$ 时 MD = CLS。  
- $W=V_\beta^{-1}$ 时得有效 MD，渐近方差 $V_\beta-V_\beta R(R'V_\beta R)^{-1}R'V_\beta$。  
- (8.26)–(8.34) 为上述方差与 Hausman 等式的代数验证。

---

## Exercise 8.18　两独立样本 $\beta_1=\beta_2$

**(a)** $\tilde\beta=(\hat V_1^{-1}+\hat V_2^{-1})^{-1}(\hat V_1^{-1}\hat\beta_1+\hat V_2^{-1}\hat\beta_2)$。  
**(b)** $\mathrm{Avar}=(\hat V_1^{-1}+\hat V_2^{-1})^{-1}$（大样本）。  
**(c)** 用各自 $\mathrm{Avar}/n_j$；权重按信息矩阵 $V_j^{-1}$。

---

## Exercise 8.19（CPS 实证）

白人男性西班牙裔，$n=4230$。

|  | edu | exp | exp2/100 | m1 | m2 | m3 | wid | div | sep | int |
|--|-----|-----|----------|----|----|----|-----|-----|-----|-----|
| OLS | 0.087 | 0.028 | −0.037 | 0.182 | −0.479 | −0.039 | 0.237 | 0.074 | 0.017 | 1.191 |

**(b)(c)** 约束 m1=wid、div=sep：CLS 合并虚拟；EMD 与 CLS 接近（m1=wid≈0.181，div=sep≈0.052）。  
**(d)** $\partial m/\partial\mathrm{exp}=\beta_2+2\beta_3\cdot\mathrm{exp}/100\ge0$ 对 $\mathrm{exp}\in[0,50]$  
⇒ 需 $\beta_2\ge0$ 且 $\beta_2+\beta_3\ge0$（端点）。  
无约束下 $\beta_2+\beta_3\approx-0.009<0$，需施加不等式约束（二次规划 CLS）。

---

## Exercise 8.20　多项式导数

**(a)** $m$ 为 $Y$ 对 $\{1,x,\ldots,x^p\}$ 的投影；$g=m'$。  
**(b)** $\hat g(x)=\sum_{j=1}^p j\hat\beta_j x^{j-1}$。  
**(c)** delta 法：$\sqrt{n}(\hat g-g)\to_d N(0,\nabla'\beta V\nabla\beta)$。  
**(d)** $\hat g\pm1.96\,\mathrm{se}$。  
**(e)** 凹性 $p=2$：$\beta_2\le0$。  
**(f)** 在 $[x_L,x_U]$ 递增：$\min g\ge0$ ⇔ 端点约束（线性 $\beta$ 不等式）。

---

## Exercise 8.21

**(a)** 否。$\hat\sigma^2$ 最小（无约束 SSE 最小）；约束使 SSE 增大 ⇒ $\sigma^2_{\mathrm{EMD}},\tilde\sigma^2\ge\hat\sigma^2$。效率指系数，非 SSE。  
**(b)** 在 $H_0$ 下 $T_n\to_d\chi^2_q$（与 Wald/LR 同族）。  
**(c)** 同方差时与经典 $F$/似然比单调相关。

---

## Exercise 8.22　$\beta_1/\beta_2=2$

**(a)** $\beta_1=2\beta_2$：$Y=(2X_1+X_2)\beta_2+e$，  
$\tilde\beta_2=\frac{\sum(2X_1+X_2)Y}{\sum(2X_1+X_2)^2}$，$\tilde\beta_1=2\tilde\beta_2$。  
**(b)** 标准 MD/投影渐近正态，方差由 $Z=2X_1+X_2$ 的 OLS 方差×4 得 $\tilde\beta_1$。

---
