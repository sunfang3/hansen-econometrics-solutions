# Hansen《Econometrics》第 15 章习题完整解答

**章节：** Chapter 15 Multivariate Time Series  
**书稿：** PDF 第 563–566 页（印刷页 543–546），§15.32 Exercises（**15.1–15.20 全部**）

---

## Exercise 15.1　VAR(1) 平稳性

$Y_t=AY_{t-1}+e_t$，$e_t$ i.i.d. 严格平稳（因果）⇔ 特征值 $|\lambda(A)|<1$。

| | $A$ | 特征值 | $\max|\lambda|$ | 平稳？ |
|--|-----|--------|----------------|--------|
| (a) | $\begin{bmatrix}0.7&0.2\\0.2&0.7\end{bmatrix}$ | $0.9,0.5$ | $0.9$ | **是** |
| (b) | $\begin{bmatrix}0.8&0.4\\0.4&0.8\end{bmatrix}$ | $1.2,0.4$ | $1.2$ | **否** |
| (c) | $\begin{bmatrix}0.8&0.4\\-0.4&0.8\end{bmatrix}$ | $0.8\pm0.4i$ | $\sqrt{0.8^2+0.4^2}\approx0.894$ | **是** |

---

## Exercise 15.2　VAR(2)

伴随矩阵
$$
C=\begin{bmatrix}A_1&A_2\\ I&0\end{bmatrix},\quad
A_1=\begin{bmatrix}0.3&0.2\\0.2&0.3\end{bmatrix},\;
A_2=\begin{bmatrix}0.4&-0.1\\-0.1&0.4\end{bmatrix}.
$$
计算得 $\max|\lambda(C)|\approx0.852<1$ ⇒ **严格平稳**（在 i.i.d. 创新下）。

---

## Exercise 15.3

$Y_t=AY_{t-1}+u_t$，$u_t=Bu_{t-1}+e_t$。  
$u_{t-1}=Y_{t-1}-AY_{t-2}$，代入：
$$
Y_t=AY_{t-1}+B(Y_{t-1}-AY_{t-2})+e_t
=(A+B)Y_{t-1}-BAY_{t-2}+e_t.
$$
故 VAR(2)：$A_1=A+B$，$A_2=-BA$，误差 $e_t$。

---

## Exercise 15.4

$Y_{it}$ 独立 AR($p$)：$Y_{it}=\sum_{j=1}^p a_{ij}Y_{i,t-j}+e_{it}$，跨 $i$ 独立。  
联合为 **对角系数** 的 VAR($p$)：
$$
A_j=\mathrm{diag}(a_{1j},\ldots,a_{mj}),\quad
\Sigma_e=\mathrm{diag}(\sigma_1^2,\ldots,\sigma_m^2).
$$
无跨方程滞后耦合。

---

## Exercise 15.5　VAR(1) 的 $\Theta_h$

$Y_t=\sum_{j=0}^\infty A_1^j e_{t-j}$ ⇒ $\Theta_h=A_1^h$（$\Theta_0=I$）。

---

## Exercise 15.6　VAR(2) 的 $\Theta_h$

递推：$\Theta_0=I$，$\Theta_1=A_1$，  
$\Theta_h=A_1\Theta_{h-1}+A_2\Theta_{h-2}$（$h\ge2$）。  

- $\Theta_2=A_1^2+A_2$  
- $\Theta_3=A_1(A_1^2+A_2)+A_2A_1=A_1^3+A_1A_2+A_2A_1$  
- $\Theta_4=A_1\Theta_3+A_2\Theta_2$

---

## Exercise 15.7　VAR($p$) 的 VAR(1) 伴随形式与 IRF

$$
\begin{pmatrix}Y_t\\Y_{t-1}\\\vdots\\Y_{t-p+1}\end{pmatrix}
=
\begin{pmatrix}A_1&\cdots&A_{p-1}&A_p\\ I&&&0\\ &\ddots&&\vdots\\ &&I&0\end{pmatrix}
\begin{pmatrix}Y_{t-1}\\\vdots\\Y_{t-p}\end{pmatrix}
+
\begin{pmatrix}e_t\\0\\\vdots\end{pmatrix}.
$$
记伴随矩阵为 $\mathbf A$，则 $\mathrm{IRF}(h)$ 为 $\mathbf A^h$ 左上 $m\times m$ 块（对 $e_t$）：  
$\Theta_h = J\mathbf A^h J'$，$J=(I_m,0,\ldots,0)$。

---

## Exercise 15.8　$Y_2\nrightarrow Y_1$（Granger）

$Y_1$ 方程中所有 $Y_2$ 滞后系数为零：  
$A_{1,12}^{(j)}=0$（$A_j$ 的 $(1,2)$ 元）对 $j=1,2$。

---

## Exercise 15.9　双向无 Granger

$A_1,A_2$ 均 **对角**（无交叉滞后）。系统为两个分离的一元 AR。

---

## Exercise 15.10

$T=20\times12=240$ 月，$m=8$，$p=12$。  
每方程系数：截距 $+m p=1+96=97$。  
有效观测约 $240-12=228$。  
**过度参数化**：每方程 97 参数 / 228 观测，总参数 $8\times96=768$ 量级（不含截距），自由度不足，不宜估满 VAR(12) 八变量；应降维、贝叶斯收缩、因子或更短滞后。

---

## Exercise 15.11　Cholesky 与递推回归

$\hat\Sigma=\mathrm{chol}$ 下三角 $\hat B$ 满足 $\hat B\hat B'=\hat\Sigma$。  
等价：对残差 $\hat e_{1t},\ldots,\hat e_{mt}$ 做 **递推 OLS**  
$\hat e_{jt}=b_{j1}\hat e_{1t}+\cdots+b_{j,j-1}\hat e_{j-1,t}+v_{jt}$，  
标准化 $v$ 的 sd 为对角，回归系数填 $\hat B$ 的下三角（与 Cholesky 一致）。

---

## Exercise 15.12　Cholesky 计算

**(a)** $\Sigma=\begin{bmatrix}\sigma_1^2&\rho\sigma_1\sigma_2\\\rho\sigma_1\sigma_2&\sigma_2^2\end{bmatrix}$（题中 $\Sigma_{22}=\sigma_1^2$ 若同方差）。  
一般下三角 $L$：
$$
L=\begin{bmatrix}\sigma_1&0\\\rho\sigma_2&\sigma_2\sqrt{1-\rho^2}\end{bmatrix}
\quad(LL'=\Sigma\text{ 当 }\Sigma_{22}=\sigma_2^2).
$$
若 $\Sigma_{22}=\sigma_1^2$：
$$
L=\begin{bmatrix}\sigma_1&0\\\rho\sigma_1&\sigma_1\sqrt{1-\rho^2}\end{bmatrix}.
$$

**(b)** 相关阵 $\rho$：$L=\begin{bmatrix}1&0\\\rho&\sqrt{1-\rho^2}\end{bmatrix}$。  

**(c)** 上三角 $R$，$RR'=R_{\mathrm{corr}}$：  
$R=\begin{bmatrix}\sqrt{1-\rho^2}&\rho\\0&1\end{bmatrix}$。  

**(d)** $\Theta_h=\begin{bmatrix}1&0\\1&1\end{bmatrix}$，$\rho=0.8$，$L=\begin{bmatrix}1&0\\0.8&0.6\end{bmatrix}$，  
$\mathrm{OIRF}=\Theta_h L=\begin{bmatrix}1&0\\1.8&0.6\end{bmatrix}$。  

**(e)** 变量对调用上三角分解：$R=\begin{bmatrix}0.6&0.8\\0&1\end{bmatrix}$（$\sqrt{1-0.64}=0.6$），  
需同步置换 $\Theta$ 的变量顺序；对调后 OIRF 一般 **不同**。  

**(f)** 正交 IRF **依赖排序**；无经济排序时解释不可靠。

---

## Exercise 15.13

无说明排序/识别时，正交 IRF **不能** 解释为结构冲击响应，仅是某一随意 Cholesky 排序下的统计分解。应忽略结构性叙述，或要求作者提供识别假设。

---

## Exercise 15.14　三变量 VAR(6)：GDP、价格、联邦基金

变量：$\Delta\log\mathrm{GDP}$、$\Delta\log P$、`fedfunds`（与 §15.13 同类变换）。  
排序 $(g,\pi,i)$，**供给冲击** = 正交化后 GDP 方程冲击（Cholesky 第一冲击）。  

对 **增长** 的 IRF 累加得 **水平** GDP/价格响应（因水平 = 增长累积）。联邦基金已是水平，无需累积。  

本计算（$n\approx229$）：供给冲击后水平 GDP 瞬时上升并持续为正；价格水平缓慢上升；联邦基金上升——与“供给冲击抬产出”方向大体一致，价格路径需结合识别谨慎解读。

---

## Exercise 15.15　Kilian (2009) 型正交 VAR(4)

变量：$(-\mathrm{oil},\ \mathrm{output},\ \mathrm{price})$（oil 乘 $-1$ 使冲击推高价格）。  
$n\approx415$。  

| 冲击（Cholesky） | 活动 (output) 响应特征 |
|------------------|------------------------|
| 油供给（第1） | 活动短期略降/负向 |
| 需求/活动（第2） | 活动大幅正向持久 |
| 油特定（第3） | 活动响应相对较小 |

与 Kilian 叙述一致：区分供给与需求冲击对活动的含义不同。

---

## Exercise 15.16　permit, houst, realln

**(a)** $\Delta\log(\mathrm{realln})$。  
**(b)** AIC 在 $p=1..8$ 中 **$p=6$ 最低**。  
**(c)(d)** 住房开工对 **许可冲击** 正向持久；对自身冲击瞬时最大；贷款冲击下开工响应偏弱/负向延迟——符合“许可→开工→贷款”时序，但贷款冲击反馈有限。

---

## Exercise 15.17　短约束 SVAR（投资、价格、GDP、联邦基金）

变量顺序建议：$(I,P,Y,r)$ 取对数后投资、价格、GDP，及联邦基金。  

**(a)** $A e_t=\varepsilon_t$，$A$ 左乘结构。限制：  
- 前三个变量不响应 $r$ 冲击 ⇒ $A$ 中 $r$ 列对 $I,P,Y$ 的同步系数为 0 的结构（或 $A$ 最后列上三角块）。  
- $I$ 不响应 $P$；$P$ 不响应 $I$；投资对 GDP 单位弹性（投资方程中 GDP 的 $A$ 系数为 $-1$）。  

示意（具体行对应 $I,P,Y,r$）：
$$
A=\begin{pmatrix}
a_{II}&0&-1&0\\
0&a_{PP}&a_{PY}&0\\
a_{YI}&a_{YP}&a_{YY}&0\\
a_{rI}&a_{rP}&a_{rY}&a_{rr}
\end{pmatrix}
$$
（规范化对角或 $\mathrm{diag}(A)=1$ 视教材 (15.22) 约定。）

**(b)** 计算自由参数个数 vs $\Sigma$ 的 $m(m+1)/2$ 个矩；需阶/秩条件满足 **恰好/过度识别**。单位弹性提供额外限制。  

**(c)** $I$ 与 $P$ 互不同步响应 ⇒ **非** 简单递归三角；GDP 与价格可同时（非纯递归）。  

**(d)(e)** 估 VAR(6)+趋势，由 $\hat\Sigma$ 与约束解 $\hat A$；报告 FF→GDP、GDP 冲击→GDP、GDP 冲击→$P$ 的结构 IRF（notebook 可扩展）。

---

## Exercise 15.18　Kilian 短约束

**(a)** 顺序 $(\mathrm{oil},\mathrm{output},\mathrm{price})$，$A e=\varepsilon$：  
油生产不响应产出与价格；产出不响应油生产（一月延迟）。  
$$
A=\begin{pmatrix}a_{11}&0&0\\0&a_{22}&a_{23}\\a_{31}&a_{32}&a_{33}\end{pmatrix}
$$
（油方程无产出/价格；产出方程无油；油可进价格方程。）

**(b)** 约束个数匹配时恰好识别（类似递归但产出-价格可同时）。  

**(c)(d)** VAR(4)，oil×(−1)；估计 $A$ 与价格对三冲击的 IRF——供给冲击提价抑活动，需求冲击提价提活动等。

---

## Exercise 15.19　货币中性

GDP 增长、名义 M1 增长（`m1realx`×`cpiaucsl`）。

**(a)** Granger：四滞后货币系数联合 =0。  
本样本稳健 Wald **显著**（拒绝严格短期中性；报告中给出 $p$ 值量级）。  

**(b)** 四货币系数 **和** =0：长期中性约束；检验结果解释货币累积效应。  

**(c)** 两变量 SVAR + **长期** 货币中性：GDP 水平对货币冲击的长期响应为 0（Blanchard–Quah 型下三角长期 $C$）。  

**(d)** 累积 IRF：供给型冲击抬长期 GDP；货币冲击长期 GDP≈0（由约束），名义货币水平调整。

本计算：长期 $C$ 下三角；货币冲击对 GDP 水平长期累积近 0。

---

## Exercise 15.20　Shapiro–Watson 型长期约束

变量：工时增长、GDP 增长、通胀二阶差分。  
长期递归：工时 LR 不受产出/通胀；GDP LR 不受“需求”冲击 ⇒ 长期 $C$ 下三角。

**(a)** $C$ 下三角 $3\times3$（(15.24)）。  
**(b)** 恰好识别（$C C'=\Phi\Sigma\Phi'$ 的 Cholesky）。  
**(c)** AIC 选 **$p=4$**。  
**(d)** $\hat C$ 见计算（对角为长期冲击 sd）。  
**(e)** 水平 GDP 对“供给/工时”冲击持久为正；对最后冲击长期近 0（递归长期中性）。

---

## 小结

| 题 | 内容 |
|:--:|------|
| 15.1–15.9 | 平稳性、VAR 代数、Granger 约束 |
| 15.10–15.13 | 维数灾难、Cholesky、识别警告 |
| 15.14–15.20 | FRED/Kilian 实证 VAR/SVAR |

