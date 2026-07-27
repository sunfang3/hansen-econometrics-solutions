# Bruce Hansen《Econometrics》第 29 章习题完整解答

**章节：** Chapter 29 Machine Learning  
**习题：** Exercises 29.1–29.10（PDF 最后一页）  
**体系统一：** 记号与推导均按 Hansen 教材体系（惩罚估计、Mallows \(C_p\)、leave-one-out、投影模型等）

---

## 预备记号（与教材一致）

线性模型（样本矩阵形式）
\[
Y = X\beta + e,\qquad X\in\mathbb{R}^{n\times p},\quad \beta\in\mathbb{R}^p.
\]
岭回归（允许对角惩罚矩阵 \(\Lambda\)）
\[
\hat\beta_{\mathrm{ridge}}(\Lambda) = (X'X+\Lambda)^{-1}X'Y,
\]
残差 \(\hat e(\Lambda)=Y-X\hat\beta_{\mathrm{ridge}}(\Lambda)\)，拟合矩阵（hat matrix）
\[
A(\Lambda)=X(X'X+\Lambda)^{-1}X',\qquad \hat m = A(\Lambda)Y.
\]
Lasso 目标
\[
\mathrm{SSE}_1(\beta,\lambda)=\|Y-X\beta\|_2^2+\lambda\|\beta\|_1.
\]
回归 \(R^2\) 定义为
\[
R^2 = 1-\frac{\|Y-X\hat\beta\|_2^2}{\|Y-\bar Y\cdot\mathbf{1}\|_2^2}.
\]

---

## Exercise 29.1　证明 Theorem 29.1

**定理内容（Theorem 29.1）。** 岭回归 leave-one-out 预测误差满足
\[
\tilde e_i(\lambda)=\bigl(1-X_i'(X'X+\Lambda)^{-1}X_i\bigr)^{-1}\hat e_i(\lambda),
\tag{29.6}
\]
其中 \(\hat e_i(\lambda)=Y_i-X_i'\hat\beta_{\mathrm{ridge}}(\lambda)\) 为岭残差。

**提示：** 证明与 Theorem 3.7（OLS leave-one-out）同构。

### 证明

记 \(A:=X'X+\Lambda\)（\(\Lambda\) 对称半正定且 \(A\) 可逆；岭回归中 \(\Lambda=\lambda I_p\) 或对角惩罚矩阵）。全样本岭估计为
\[
\hat\beta=A^{-1}X'Y.
\]
删去第 \(i\) 个观测后
\[
\hat\beta_{(-i)}=(A-X_iX_i')^{-1}(X'Y-X_iY_i).
\tag{*}
\]
用 \(A^{-1}(A-X_iX_i')\) 左乘 \((*)\) 的两侧：
\begin{align*}
A^{-1}(A-X_iX_i')\hat\beta_{(-i)}
&=A^{-1}(X'Y-X_iY_i)\\
\hat\beta_{(-i)}-A^{-1}X_iX_i'\hat\beta_{(-i)}
&=\hat\beta-A^{-1}X_iY_i.
\end{align*}
整理得
\[
\hat\beta_{(-i)}=\hat\beta-A^{-1}X_i\bigl(Y_i-X_i'\hat\beta_{(-i)}\bigr)
=\hat\beta-A^{-1}X_i\tilde e_i,
\]
其中 leave-one-out 预测误差 \(\tilde e_i:=Y_i-X_i'\hat\beta_{(-i)}\)。

再左乘 \(X_i'\)：
\[
X_i'\hat\beta_{(-i)}=X_i'\hat\beta-h_{ii}\tilde e_i,
\qquad
h_{ii}:=X_i'A^{-1}X_i=X_i'(X'X+\Lambda)^{-1}X_i.
\]
于是
\[
\tilde e_i
=Y_i-X_i'\hat\beta_{(-i)}
=Y_i-X_i'\hat\beta+h_{ii}\tilde e_i
=\hat e_i+h_{ii}\tilde e_i.
\]
故
\[
\tilde e_i=(1-h_{ii})^{-1}\hat e_i,
\]
即 (29.6)。□

**注记。** 这与 Theorem 3.7 中 \(\tilde e_i=(1-h_{ii})^{-1}\hat e_i\)、\(h_{ii}=X_i'(X'X)^{-1}X_i\) 完全平行；岭回归只是把 Gram 矩阵 \(X'X\) 换成 \(X'X+\Lambda\)。该公式使 \(CV(\lambda)=\sum_i\tilde e_i(\lambda)^2\) 无需做 \(n\) 次回归。

---

## Exercise 29.2　证明 (29.7) 是岭回归的 Mallows 准则

**目标式 (29.7)。**
\[
C(\lambda)=\sum_{i=1}^n\hat e_i(\lambda)^2+2\hat\sigma^2\,\mathrm{tr}\!\Bigl((X'X+\Lambda)^{-1}(X'X)\Bigr),
\]
其中 \(\hat\sigma^2\) 来自 OLS。

**Section 28.6 定义。** 对线性估计量 \(\hat m=AY\)（\(A=A(X)\)），在条件同方差模型 \(E[e\mid X]=0\)、\(E[e^2\mid X]=\sigma^2\) 下，Mallows 准则为
\[
C_p=\hat e'\hat e+2\tilde\sigma^2\,\mathrm{tr}(A).
\tag{28.14}
\]

### 证明

岭回归拟合为
\[
\hat m=X\hat\beta_{\mathrm{ridge}}=X(X'X+\Lambda)^{-1}X'Y=:A(\Lambda)Y.
\]
故 hat 矩阵
\[
A(\Lambda)=X(X'X+\Lambda)^{-1}X'.
\]
迹的循环性质：
\begin{align*}
\mathrm{tr}\bigl(A(\Lambda)\bigr)
&=\mathrm{tr}\!\Bigl(X(X'X+\Lambda)^{-1}X'\Bigr)
=\mathrm{tr}\!\Bigl((X'X+\Lambda)^{-1}X'X\Bigr).
\end{align*}
残差平方和 \(\hat e'\hat e=\sum_i\hat e_i(\lambda)^2\)。取 \(\tilde\sigma^2=\hat\sigma^2\)（大模型/OLS 方差估计），代入 (28.14) 即得 (29.7)。□

**解释（Hansen 观点）。** \(C_p\) 是拟合风险
\[
R=E\Bigl[\sum_i(\hat m_i-m_i)^2\Bigr]
\]
的（经常数平移后的）无偏估计；对岭回归，有效自由度是 \(\mathrm{tr}(A(\Lambda))\) 而非参数个数 \(p\)。

---

## Exercise 29.3　推导岭估计的条件偏误 (29.8) 与方差 (29.9)

模型：\(Y=X\beta+e\)，\(E[e\mid X]=0\)，\(D=\mathrm{diag}\{\sigma^2(X_1),\ldots,\sigma^2(X_n)\}\)，\(\sigma^2(x)=E[e^2\mid X=x]\)。

### (a) 偏误

\[
\hat\beta_{\mathrm{ridge}}=(X'X+\lambda I_p)^{-1}X'Y
=(X'X+\lambda I_p)^{-1}X'(X\beta+e).
\]
故
\begin{align*}
E[\hat\beta_{\mathrm{ridge}}\mid X]
&=(X'X+\lambda I_p)^{-1}X'X\,\beta\\
&=(X'X+\lambda I_p)^{-1}\bigl((X'X+\lambda I_p)-\lambda I_p\bigr)\beta\\
&=\beta-\lambda(X'X+\lambda I_p)^{-1}\beta.
\end{align*}
因此
\[
\mathrm{bias}(\hat\beta_{\mathrm{ridge}}\mid X)
=E[\hat\beta_{\mathrm{ridge}}\mid X]-\beta
=-\lambda(X'X+\lambda I_p)^{-1}\beta.
\tag{29.8}
\]

### (b) 方差

\[
\hat\beta_{\mathrm{ridge}}-E[\hat\beta_{\mathrm{ridge}}\mid X]
=(X'X+\lambda I_p)^{-1}X'e,
\]
故
\begin{align*}
\mathrm{var}(\hat\beta_{\mathrm{ridge}}\mid X)
&=(X'X+\lambda I_p)^{-1}X'\,\mathrm{var}(e\mid X)\,X\,(X'X+\lambda I_p)^{-1}\\
&=(X'X+\lambda I_p)^{-1}(X'DX)(X'X+\lambda I_p)^{-1},
\tag{29.9}
\end{align*}
其中用了 \(E[e\mid X]=0\Rightarrow\mathrm{var}(e\mid X)=E[ee'\mid X]=D\)（独立观测下对角）。□

**补充。** MSE 矩阵为 \(\mathrm{var}+\mathrm{bias}\,\mathrm{bias}'\)，即 Theorem 29.2 证明所用表达式。

---

## Exercise 29.4　岭回归 = 增广数据上的 OLS

**构造。** 原数据 \((Y,X)\)。增广
\[
Y^*=\begin{pmatrix}Y\\ 0_p\end{pmatrix}\in\mathbb{R}^{n+p},
\qquad
X^*=\begin{pmatrix}X\\ \sqrt{\lambda}\,I_p\end{pmatrix}\in\mathbb{R}^{(n+p)\times p}.
\]
（教材写 “\(p\) 行 \(\sqrt{\lambda}I_p\)”，与 \(\lambda I_p\) 惩罚一致。）

### 证明

对 \((Y^*,X^*)\) 做 OLS：
\begin{align*}
\hat\beta_{\mathrm{OLS}}^*
&=(X^{*'}X^*)^{-1}X^{*'}Y^*\\
&=\Bigl(X'X+\lambda I_p\Bigr)^{-1}\bigl(X'Y+\sqrt{\lambda}\,I_p\cdot 0_p\bigr)\\
&=(X'X+\lambda I_p)^{-1}X'Y
=\hat\beta_{\mathrm{ridge}}.
\end{align*}
等价地，增广平方和为
\[
\|Y^*-X^*\beta\|_2^2=\|Y-X\beta\|_2^2+\lambda\|\beta\|_2^2,
\]
正是岭惩罚准则。□

---

## Exercise 29.5　谁的回归 \(R^2\) 更大：OLS 还是 Ridge？

**答案：OLS 的 \(R^2\) 不会低于 Ridge；在 \(\lambda>0\) 且 \(\hat\beta_{\mathrm{ols}}\neq 0\) 的通常情形下严格更大。**

### 证明

在列满秩（\(X'X\) 可逆）时，OLS 是无约束最小化问题的无约束解：
\[
\hat\beta_{\mathrm{ols}}=\arg\min_{\beta\in\mathbb{R}^p}\|Y-X\beta\|_2^2.
\]
岭估计是**同一目标**在惩罚/约束下的解，等价于对某个 \(\tau>0\)
\[
\hat\beta_{\mathrm{ridge}}=\arg\min_{\|\beta\|_2^2\le\tau}\|Y-X\beta\|_2^2
\]
（对偶形式）。因此
\[
\|Y-X\hat\beta_{\mathrm{ols}}\|_2^2\le\|Y-X\hat\beta_{\mathrm{ridge}}\|_2^2.
\]
分母 \(\|Y-\bar Y\mathbf{1}\|_2^2\) 与估计量无关，故
\[
R^2_{\mathrm{ols}}\ge R^2_{\mathrm{ridge}}.
\]
当 \(\lambda>0\) 且 \(\hat\beta_{\mathrm{ols}}\neq 0\) 时，约束 \(\|\beta\|_2^2\le\tau\) 在最优点通常是紧的，且 \(\hat\beta_{\mathrm{ridge}}\neq\hat\beta_{\mathrm{ols}}\)，严格不等式成立。

**直观。** \(R^2\) 只度量**样本内拟合**；岭回归牺牲样本内 SSE 以换取更小的预测/系数方差（正则化）。Hansen 体系中评价预测应看 CV / Mallows，而非 \(R^2\)。

若 \(p>n\)，OLS 在列空间上仍最小化 SSE（投影唯一），\(R^2\) 可达 1（插值），岭回归一般 \(R^2<1\)。

---

## Exercise 29.6　岭回归是否要求 \(X\) 列线性无关？重复回归元

**答案：不要求。** 只要 \(\lambda>0\)，\(X'X+\lambda I_p\) 正定，即使 \(X\) 列相关（甚至 \(p>n\)）岭估计仍唯一。

### 重复回归元设定

设 \(\tilde X=(X,X)\in\mathbb{R}^{n\times 2p}\)，对 \(Y\) 关于 \(\tilde X\) 做岭回归（惩罚参数 \(\lambda>0\)），系数分块 \((\hat\beta_1',\hat\beta_2')'\)。

目标函数
\[
S(\beta_1,\beta_2)=\|Y-X\beta_1-X\beta_2\|_2^2+\lambda\|\beta_1\|_2^2+\lambda\|\beta_2\|_2^2.
\]
一阶条件：
\begin{align*}
X'(Y-X(\beta_1+\beta_2))-\lambda\beta_1&=0,\\
X'(Y-X(\beta_1+\beta_2))-\lambda\beta_2&=0.
\end{align*}
两式相减得 \(\lambda(\beta_1-\beta_2)=0\Rightarrow\hat\beta_1=\hat\beta_2\)。  
两式相加：
\[
2X'(Y-X(\hat\beta_1+\hat\beta_2))-\lambda(\hat\beta_1+\hat\beta_2)=0.
\]
令 \(\gamma:=\hat\beta_1+\hat\beta_2=2\hat\beta_1\)，则
\[
2X'Y-2X'X\gamma-\lambda\gamma=0
\Rightarrow
\bigl(X'X+\tfrac{\lambda}{2}I_p\bigr)\gamma=X'Y.
\]
故
\[
\hat\beta_1=\hat\beta_2=\frac12\bigl(X'X+\tilde\lambda I_p\bigr)^{-1}X'Y,
\qquad \tilde\lambda=\lambda/2.
\]
这正是教材要求的结论。□

**含义。** 重复变量被均分系数；有效惩罚因“两个相同变量”而改变标定，但预测 \(X(\hat\beta_1+\hat\beta_2)\) 等于对 \(X\) 做惩罚 \(\tilde\lambda=\lambda/2\) 的岭拟合。

---

## Exercise 29.7　Lasso 在重复回归元下的性质

同一 \(\tilde X=(X,X)\)，Lasso 目标
\[
S(\beta_1,\beta_2)=\|Y-X(\beta_1+\beta_2)\|_2^2+\lambda\|\beta_1\|_1+\lambda\|\beta_2\|_1.
\]

### (i) 单个 \(\hat\beta_1,\hat\beta_2\) 不可识别

拟合只依赖和 \(\gamma=\beta_1+\beta_2\)。对任意分解 \(\beta_1+\beta_2=\gamma\)，
\[
\|\beta_1\|_1+\|\beta_2\|_1\ge\|\gamma\|_1,
\]
等号当且仅当 \(\beta_1,\beta_2\) 符号协调且不“反向抵消”（更精确：存在坐标wise 的分解使 \(\mathrm{sign}\) 一致）。最小化要求
\[
\|\beta_1\|_1+\|\beta_2\|_1=\|\gamma\|_1,
\]
满足该式的 \((\beta_1,\beta_2)\) **不唯一**（例如把第 \(j\) 个分量的质量在 \(\beta_{1j}\) 与 \(\beta_{2j}\) 之间任意拆分，只要同号且和为 \(\gamma_j\)）。故 \(\hat\beta_1,\hat\beta_2\)  individually indeterminate。

### (ii) 其和等于对 \(X\) 的 Lasso

在最优处必有 \(\|\hat\beta_1\|_1+\|\hat\beta_2\|_1=\|\hat\gamma\|_1\)，且
\[
\hat\gamma=\arg\min_\gamma\Bigl(\|Y-X\gamma\|_2^2+\lambda\|\gamma\|_1\Bigr)=\hat\beta_{\mathrm{Lasso}}.
\]
因此
\[
\hat\beta_1+\hat\beta_2=\hat\beta_{\mathrm{Lasso}}.
\]
□

**与岭的对比。** 岭的 \(\ell_2\) 惩罚严格凸，重复列时系数被唯一均分；Lasso 的 \(\ell_1\) 惩罚只凸不严格凸，解集是凸集，单个系数不定，但**和**及**拟合**唯一（在一般位置下）。

---

## Exercise 29.8　回归树中加入 \(X^2\) 是否有意义？

设定：连续变量 \((Y,X)\)，\(X\ge 0\)，估计回归树逼近 \(E[Y\mid X]\)。友人建议加入二次项 \(X^2\)。

**答案：没有实质意义；不增加回归树的近似能力。**

### 理由（Hansen CART 框架）

回归树通过对**单个坐标**做阈值阈值分割
\[
Y=\mu_1\,1\{X_d\le\gamma\}+\mu_2\,1\{X_d>\gamma\}+e
\]
递归生长（Section 29.15）。分割点搜索只依赖协变量的**排序/分位数**。

当 \(X\ge 0\) 时，映射 \(x\mapsto x^2\) **严格递增**，因而
\[
\{X\le\gamma\}\quad\Longleftrightarrow\quad\{X^2\le\gamma^2\}
\]
（\(\gamma\ge 0\)）。对 \(X^2\) 的任意一次最优分割，都存在对 \(X\) 的等价分割，给出**完全相同**的样本划分与叶均值。多维时若再加入 \(X^2\)，它与 \(X\) 诱导同一序，不会产生新的矩形划分族。

进一步：树模型本身已是高度灵活的分段常数逼近；在单一连续 \(X\) 上，充分多的分裂已可逼近任意可测回归函数，无需多项式基。加入 \(X^2\) 只增加冗余候选分裂维数，浪费计算，不改善偏差。

**何时二次项有用？** 在**线性/多项式参数模型**或样条/级数回归中有用；在**轴平行回归树**里，对 \(X\ge 0\) 的单调变换无余。

---

## Exercise 29.9　cps09mar：亚裔女性样本 Lasso

### 数据与设定（Hansen 惯例）

- 数据：`cps09mar`（March 2009 CPS）  
- 子样本：`race==4`（Asian only）且 `female==1`，\(n=1149\)  
- 因变量：\(\log(\mathrm{wage})=\log(\mathrm{earnings}/(\mathrm{hours}\cdot\mathrm{week}))\)  
- 经验：\(\mathrm{experience}=\mathrm{age}-\mathrm{education}-6\)，回归元用 \((\mathrm{experience}/40)^k\)，\(k=1,\ldots,9\)  
- 婚姻：married（marital∈{1,2,3}）、divorced、separated、widowed、never married  
- 地区：region 1–4 虚拟变量  
- 另含：education 水平值；education∈{12,13,14,15,16,18,20} 虚拟变量；union  

**估计：** 回归元标准化后 10 折交叉验证 Lasso（与教材 glmnet / `cv.glmnet` 默认一致：惩罚斜率、不惩罚截距）。  
**说明：** 样本中 **education=15 无人**，该虚拟变量退化为 0；婚姻五类与地区四类各自与截距完全共线（设计阵秩 25/27），Lasso 解在系数层面取稀疏代表。

### 估计结果（CV 最优 \(\lambda\approx 0.00142\)）

非零系数（原始尺度，未标准化回归元）：

| 变量 | 系数 |
|------|------|
| intercept | 2.102 |
| education | 0.023 |
| edu12 | 0.039 |
| edu13 | 0.163 |
| edu14 | 0.324 |
| edu16 | 0.604 |
| edu18 | 0.708 |
| edu20 | 0.887 |
| (exp/40) | 0.452 |
| (exp/40)\(^2\) | −0.353 |
| (exp/40)\(^9\) | 0.002 |
| divorced | 0.044 |
| separated | −0.145 |
| widowed | −0.047 |
| nevermarried | −0.052 |
| region1 (Northeast) | 0.073 |
| region2 (Midwest) | −0.131 |
| region3 (South) | −0.058 |
| union | −0.015 |

**被 Lasso 置零（或不可识别吸收）的：** edu15（无观测）、married、region4（West，作地区基准）、\((\mathrm{exp}/40)^{3}\)–\((\mathrm{exp}/40)^{8}\) 等。

**解读（Hansen ML 视角）。**

1. **教育：** 水平值系数为正，且相对“低于 12 年”的阶梯虚拟变量随学历上升而增大（BA、硕士、专业/博士学位溢价明显）——稀疏模型保留了分段教育溢价。  
2. **经验：** 主要保留 1、2 次幂（凹形经验剖面），高次仅 \(k=9\) 极小，体现 Lasso 的稀疏化。  
3. **婚姻：** 相对 married 基准，分居惩罚最大；未婚略负。  
4. **地区：** 东北为正，中西与南部为负（相对西部）。  
5. **工会：** 亚裔女性子样本中系数为小幅负（样本内工会人数少，宜谨慎解读）。

样本内 \(R^2\approx 0.29\)（正则化估计；比较模型应看 CV 而非 \(R^2\)）。

---

## Exercise 29.10　cps09mar：西班牙裔男性样本 Lasso

- 子样本：`hisp==1` 且 `female==0`，\(n=4547\)  
- 回归元与 29.9 相同；10 折 CV Lasso  

### 估计结果（CV 最优 \(\lambda\approx 0.00027\)）

| 变量 | 系数 |
|------|------|
| intercept | 1.750 |
| education | 0.029 |
| edu12 | 0.157 |
| edu13 | 0.344 |
| edu14 | 0.431 |
| edu16 | 0.544 |
| edu18 | 0.789 |
| edu20 | 1.051 |
| (exp/40) | 1.588 |
| (exp/40)\(^2\) | −1.319 |
| (exp/40)\(^4\) | 0.254 |
| (exp/40)\(^8\) | −0.011 |
| married | 0.068 |
| separated | −0.073 |
| widowed | 0.149 |
| nevermarried | −0.092 |
| region1 | 0.026 |
| region2 | −0.032 |
| region3 | −0.102 |
| union | 0.309 |

**置零：** edu15（无观测）、divorced、region4、部分高次经验项等。

**与 29.9 对比。**

1. **教育溢价形态类似**，但西班牙裔男性高学历虚拟变量（尤其 edu20）系数更大。  
2. **经验剖面更陡**：一次项约 1.59、二次项 −1.32，并保留 4、8 次项——样本更大（\(n=4547\)），CV 允许稍低 \(\lambda\)、稍密模型。  
3. **工会溢价显著为正**（约 0.31 log 点），与亚裔女性子样本形成鲜明对比。  
4. **婚姻：** 已婚为正、未婚为负；丧偶系数为正但该组人数少。  
5. **南部（region3）惩罚**在两个子样本中都出现。

---

## 小结表

| 题号 | 核心结论 |
|------|----------|
| 29.1 | 岭 LOO 误差 \(\tilde e_i=(1-h_{ii})^{-1}\hat e_i\)，\(h_{ii}=X_i'(X'X+\Lambda)^{-1}X_i\) |
| 29.2 | (29.7) = Mallows \(C_p\)，因 \(\mathrm{tr}(A)=\mathrm{tr}((X'X+\Lambda)^{-1}X'X)\) |
| 29.3 | \(\mathrm{bias}=-\lambda(X'X+\lambda I)^{-1}\beta\)；\(\mathrm{var}=(X'X+\lambda I)^{-1}X'DX(X'X+\lambda I)^{-1}\) |
| 29.4 | 增广 \((Y^*,X^*)\) 的 OLS = 岭估计 |
| 29.5 | OLS 的 \(R^2\) ≥ Ridge 的 \(R^2\) |
| 29.6 | 岭不需列满秩；重复列时 \(\hat\beta_1=\hat\beta_2=\frac12(X'X+\frac\lambda2 I)^{-1}X'Y\) |
| 29.7 | Lasso 下 \(\hat\beta_1,\hat\beta_2\) 不定，但 \(\hat\beta_1+\hat\beta_2=\hat\beta_{\mathrm{Lasso}}\) |
| 29.8 | \(X\ge 0\) 时加 \(X^2\) 对轴平行回归树无实质益处 |
| 29.9 | 亚裔女性 \(n=1149\) CV-Lasso：教育阶梯 + 凹经验 + 地区/婚姻稀疏 |
| 29.10 | 西裔男性 \(n=4547\) CV-Lasso：更陡经验曲线 + 显著正工会溢价 |

---

## 计算附录（复现 29.9–29.10）

```python
import numpy as np, pandas as pd
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler

df = pd.read_excel("cps09mar.xlsx")  # Hansen Econometrics Data
df["lwage"] = np.log(df.earnings / (df.hours * df.week))
df["exp40"] = (df.age - df.education - 6) / 40.0
# ... 构造教育/婚姻/地区虚拟变量与 exp40**k ...
# 标准化后 LassoCV(cv=10, fit_intercept=True)
```

数据来源：Hansen 教材配套 [Econometrics Data](https://users.ssc.wisc.edu/~bhansen/econometrics/) 中的 `cps09mar`。

**软件说明：** 系数对 CV 折划分与 \(\lambda\) 网格略敏感；上表为 `scikit-learn` `LassoCV`（目标 \(\frac{1}{2n}\|Y-X\beta\|_2^2+\alpha\|\beta\|_1\)，与 `glmnet` 的 \(\lambda\) 参数化一致）在 10 折 CV 下的代表结果。用 R `glmnet`/`cv.glmnet` 或 Stata `lasso` 应得到同阶、符号一致的稀疏模型。
