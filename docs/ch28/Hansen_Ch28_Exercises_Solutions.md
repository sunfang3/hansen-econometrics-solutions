# Hansen《Econometrics》第 28 章习题完整解答

**章节：** Chapter 28 Model Selection, Stein Shrinkage, and Model Averaging  
**出版版：** `hansen/manuscripts/Econometrics_Fullbook.pdf`，PDF 第 974–975 页（印刷页 939–940），§28.33 Exercises（**28.1–28.12 全部**）

**阅读提示（`AGENTS.md`）：** 默认读者会用 $t$/$F$ 做“逐步回归”，但不默认掌握 AIC/BIC/CV/FIC 的目标函数差异、选择后推断扭曲、James–Stein 可容许性、以及模型平均。下文逐步补齐。

**本科搭桥：**
- “哪个回归更好？”在本科常靠 $t$ 显著 → Hansen 用 **可估的 MSE/预测风险** 做标准。  
- **BIC** ≈ 后验模型概率；**AIC/Mallows/CV** ≈ 预测/密度拟合；**FIC** ≈ **焦点参数** 的 MSE。  
- 选出模型后再当“真模型”做 $t$ 检验，覆盖率可以严重失真（§28.17）。

---

## Exercise 28.1　验证 (28.1)–(28.2)

### 设定

$\hat\theta$ 均值 $\theta$、协方差 $V$；$\tilde\theta=0$。权矩阵 $W=V^{-1}$。加权 MSE
$$
\mathrm{wmse}[\hat\theta]=\mathbb{E}\bigl[(\hat\theta-\theta)'V^{-1}(\hat\theta-\theta)\bigr].
$$

### (28.1)

$$
\mathbb{E}\bigl[(\hat\theta-\theta)'V^{-1}(\hat\theta-\theta)\bigr]
=\mathrm{tr}\!\bigl(V^{-1}\mathbb{E}[(\hat\theta-\theta)(\hat\theta-\theta)']\bigr)
=\mathrm{tr}(V^{-1}V)=\mathrm{tr}(I_K)=K.
$$

### (28.2)

$\tilde\theta-\theta=-\theta$，故
$$
\mathrm{wmse}[\tilde\theta]=\theta'V^{-1}\theta\stackrel{\mathrm{def}}{=}\lambda.
$$

**含义：** 无约束估计付 $K$ 的方差成本；压成 0 付平方偏误 $\lambda$。当 $\lambda<K$ 时压成 0 的 WMSE 更小。

---

## Exercise 28.2　加权最小二乘的 Mallows 准则

模型 $Y_i=X_i'\beta+e_i$，WLS 权重 $\omega_i$，条件同方差 $\sigma^2$（相对加权残差）。

### 线性估计结构

令 $W=\mathrm{diag}(\omega_i)$，$\hat\beta=(X'WX)^{-1}X'WY$，$\hat m=X\hat\beta$。则
$$
\hat m=A Y,\qquad A=X(X'WX)^{-1}X'W.
$$
（$A$ 是加权投影，幂等但一般非对称。）

### Mallows

对线性估计 $\hat m=AY$，
$$
C_p=\hat e'\hat e+2\tilde\sigma^2\,\mathrm{tr}(A).
$$
此处 $\hat e=Y-\hat m$，且
$$
\mathrm{tr}(A)=\mathrm{tr}\bigl(X(X'WX)^{-1}X'W\bigr)=\mathrm{tr}\bigl((X'WX)^{-1}X'WX\bigr)=K
$$
（$K=\mathrm{rank}$，满列秩时为参数个数）。故
$$
C_p^{\mathrm{WLS}}=\sum_{i=1}^n\hat e_i^2+2K\tilde\sigma^2
$$
与 OLS 形式相同；**注意** $\hat e_i$ 是 **未加权水平残差** $Y_i-X_i'\hat\beta_{\mathrm{WLS}}$。若准则改用加权 SSE $\hat e'W\hat e$，则惩罚项仍是 $2\tilde\sigma^2\mathrm{tr}(A)=2K\tilde\sigma^2$，但拟合项变为加权残差平方和（与“风险在加权内积下度量”一致时需统一内积）。

在教材同方差 + 标准 Mallows 叙述下，报告
$$
C_p=n\hat\sigma^2_{\mathrm{WLS}}+2K\tilde\sigma^2
$$
即可，其中 $\hat\sigma^2_{\mathrm{WLS}}$ 由 WLS 残差定义。

---

## Exercise 28.3　Backward stepwise + AIC $\Leftrightarrow$ 最小 $|t|$

### 题意

AIC 选择下，向后逐步的一步：在当前 **active** 回归元中去掉一个，使 AIC 降得最多。需证：这等价于去掉 **经典同方差 $|t|$ 最小** 的那个回归元。

### 推导

正态同方差下（可差一个不随模型变化的常数）
$$
\mathrm{AIC}=n\log\hat\sigma^2+2K,\qquad \hat\sigma^2=\mathrm{SSE}/n.
$$
从模型 $M$（$K$ 个参数，SSE）删掉第 $j$ 个回归元得 $M_{(j)}$（$K-1$ 个参数，SSE$_j$）：
$$
\Delta\mathrm{AIC}_j
=\mathrm{AIC}(M_{(j)})-\mathrm{AIC}(M)
=n\log\frac{\mathrm{SSE}_j}{\mathrm{SSE}}+2(-1)
=n\log\Bigl(1+\frac{\mathrm{SSE}_j-\mathrm{SSE}}{\mathrm{SSE}}\Bigr)-2.
$$
$\mathrm{SSE}_j-\mathrm{SSE}$ 是“加上 $X_j$ 所减少的 SSE”。对 **单个** 系数，
$$
F_j=t_j^2=\frac{(\mathrm{SSE}_j-\mathrm{SSE})/1}{\mathrm{SSE}/(n-K)}
\quad\Rightarrow\quad
\mathrm{SSE}_j-\mathrm{SSE}=\hat\sigma^2_{\mathrm{u}}\,t_j^2,
$$
其中 $\hat\sigma^2_{\mathrm{u}}=\mathrm{SSE}/(n-K)$ 来自 **未删** 模型（LR/$F$/Wald 在线性正态下对单约束等价）。

因而 $\Delta\mathrm{AIC}_j$ 是 $t_j^2$ 的严格增函数（$\log(1+c\,t_j^2)$ 增）。  
**最小化 $\mathrm{AIC}(M_{(j)})$**（使 $\Delta\mathrm{AIC}$ 尽可能负/最小）$\Leftrightarrow$ **最小化 $t_j^2$** $\Leftrightarrow$ 去掉 **$|t_j|$ 最小** 的回归元。

---

## Exercise 28.4　Forward stepwise + AIC $\Leftrightarrow$ 与残差最相关

### 目标

当前残差 $\hat e=M_ZX\,Y$（已对 active 集 $Z$ 投影正交）。加入 inactive 中的 $x_j$ 后 SSE 降幅最大者，使 AIC 最优。

### 几何

新回归是在 $\mathrm{span}(Z,x_j)$ 上投影。由 Frisch–Waugh，$x_j$ 的额外贡献取决于其 **对 $Z$ 净尽** 后的 $\tilde x_j=M_Zx_j$：
$$
\Delta\mathrm{SSE}_j=\frac{(\tilde x_j'\hat e)^2}{\tilde x_j'\tilde x_j}
$$
（因 $\hat e\perp Z$ 故 $\tilde x_j'\hat e=x_j'\hat e$）。故
$$
\Delta\mathrm{SSE}_j=\|x_j\|^2_{\mathrm{net}}\cdot \mathrm{corr}^2(x_j,\hat e)
\quad\text{（在净尽后的尺度上）}.
$$
若先把候选回归元 **标准化**（或比较的是与 $\hat e$ 的相关系数），则 **$|\mathrm{Corr}(x_j,\hat e)|$ 最大** $\Leftrightarrow$ $\Delta\mathrm{SSE}$ 最大。

AIC 改善随 SSE 下降而改善；在每次只加 **一个** 回归元、惩罚同为 $+2$ 时，**SSE 降最多** 者即 AIC 最优。几何上：与 $\hat e$ 最平行的方向最能缩短 $\|\hat e\|$。

---

## Exercise 28.5　“其他设定系数都不显著”后的报告

### 应如何解读？

1. **选择诱导的偏误：** 报告的是 **post-model-selection** 估计量，不是事先指定模型的 OLS。系数分布是“只在被选中时才报告”的条件分布，**不是** $N(\beta,\sigma^2(X'X)^{-1})$。  
2. **$t$ 值膨胀：** 能进最终式的变量，往往已通过“在竞争设定中显得显著”的筛选，$t$ 的绝对水平 **系统性偏大**，名义 5% 检验实际 size 失真。  
3. **未报告的设定：** “不显著故丢掉”等于做了数据驱动的预检验；与真模型不一致时，保留变量的估计可有 **预检验偏误**（§28.16–28.17）。  
4. **覆盖率：** 尤其当保留变量与被删变量相关时，对焦点系数的名义 95% 区间实际覆盖可远低于 95%（图 28.2(c)）。

**稳妥做法：** 报告选择程序与候选集；对焦点参数用 **FIC/样本分割/选择性推断** 或诚实展示多设定；勿把最终式 $t$ 当作独立确认的“发现”。

---

## Exercise 28.6　验证 Theorem 28.11 与 (28.21)–(28.23)

$\hat\theta\sim(\theta,V)$，$\tilde\theta=(1-w)\hat\theta$，$w\in[0,1]$，$W=V^{-1}$，$\lambda=\theta'V^{-1}\theta$。

### (28.21) 偏误

$$
\mathbb{E}[\tilde\theta]-\theta=(1-w)\theta-\theta=-w\theta.
$$

### (28.22) 方差

$$
\mathrm{Var}(\tilde\theta)=(1-w)^2V.
$$

### (28.23) WMSE

$$
\begin{aligned}
\mathrm{wmse}[\tilde\theta]
&=\mathbb{E}\bigl[(\tilde\theta-\theta)'V^{-1}(\tilde\theta-\theta)\bigr]\\
&=\mathrm{tr}\bigl(V^{-1}\mathrm{Var}(\tilde\theta)\bigr)+\mathrm{bias}'V^{-1}\mathrm{bias}\\
&=(1-w)^2K+w^2\lambda.
\end{aligned}
$$

### Theorem 28.11

1. $\mathrm{wmse}[\hat\theta]=K$。差
$$
K-\bigl[(1-w)^2K+w^2\lambda\bigr]=w\bigl(2K-w(K+\lambda)\bigr).
$$
当 $0<w<2K/(K+\lambda)$ 时为正 ⇒ $\mathrm{wmse}[\tilde\theta]<\mathrm{wmse}[\hat\theta]$。  

2. 对 $w$ 求导：$-2(1-w)K+2w\lambda=0\Rightarrow w_0=K/(K+\lambda)$。  

3. 代入得 $\mathrm{wmse}=K\lambda/(K+\lambda)$。

---

## Exercise 28.7　$\hat\lambda=\hat\theta'V^{-1}\hat\theta-K$ 无偏估 $\lambda$

在 $\mathbb{E}\hat\theta=\theta$、$\mathrm{Var}(\hat\theta)=V$ 下（不必正态）：
$$
\begin{aligned}
\mathbb{E}[\hat\theta'V^{-1}\hat\theta]
&=\mathbb{E}\bigl[(\hat\theta-\theta+\theta)'V^{-1}(\hat\theta-\theta+\theta)\bigr]\\
&=\theta'V^{-1}\theta+\mathbb{E}\bigl[(\hat\theta-\theta)'V^{-1}(\hat\theta-\theta)\bigr]\\
&=\lambda+\mathrm{tr}(V^{-1}V)=\lambda+K.
\end{aligned}
$$
故 $\mathbb{E}[\hat\theta'V^{-1}\hat\theta-K]=\lambda$。

---

## Exercise 28.8　Theorem 28.14 的简化情形（未修正 Stein，$V=I_K$，$r=0$）

### 设定

$\hat\theta\sim N(\theta,I_K)$，$R$ 为 $K\times q$ 满列秩限制矩阵（此处 $r=0$ 表示 $R'\theta=0$ 类限制的 Stein 形式），教材简化为 **朝 0 收缩** 的未修正 Stein：
$$
\tilde\theta=\Bigl(1-\frac{c}{\hat\theta'\hat\theta}\Bigr)\hat\theta,\qquad c=q-2
$$
（与经典 James–Stein 在 $V=I$ 时一致，$q$ 扮演 $K$ 的角色；完整限制形式见 (28.27)）。

### 思路（经典 Stein 恒等式）

对 $\hat\theta\sim N(\theta,I)$，若 $g$ 弱可微，
$$
\mathbb{E}\bigl[(\hat\theta-\theta)'g(\hat\theta)\bigr]=\mathbb{E}\bigl[\nabla\cdot g(\hat\theta)\bigr].
$$
取 $g(\hat\theta)=-\dfrac{c}{\|\hat\theta\|^2}\hat\theta$，则
$$
\mathrm{mse}[\tilde\theta]
=\mathbb{E}\|\tilde\theta-\theta\|^2
=K+\mathbb{E}\bigl[\|g\|^2+2\nabla\cdot g\bigr].
$$
计算得 $\nabla\cdot g=-c(K-2)/\|\hat\theta\|^2$（$K>2$），$\|g\|^2=c^2/\|\hat\theta\|^2$，故
$$
\mathrm{mse}[\tilde\theta]=K-\mathbb{E}\Bigl[\frac{c\bigl(2(K-2)-c\bigr)}{\|\hat\theta\|^2}\Bigr].
$$
当 $0<c<2(K-2)$ 时花括号为正 ⇒ **严格优于** $\hat\theta$。$c=K-2$ 时
$$
\mathrm{mse}=K-(K-2)^2\mathbb{E}[Q_K^{-1}],\quad Q_K\sim\chi^2_K(\lambda).
$$

### Extra challenge（朝限制收缩）

对 $\tilde\theta=\hat\theta-\dfrac{q-2}{J}(\hat\theta-\hat\theta_R)$，$J=(\hat\theta-\hat\theta_R)'(\hat\theta-\hat\theta_R)$（$V=I$），类似计算给出
$$
\mathrm{wmse}[\tilde\theta]=K-(q-2)^2\mathbb{E}[J_q(\lambda_R)^{-1}],
$$
其中 $\lambda_R=\theta'R(R'R)^{-1}R'\theta$ 为限制方向上的非中心度；$J_q(\lambda_R)$ 为相应非中心 $\chi^2$。等价写法
$$
\mathrm{wmse}[\tilde\theta]=K-(q-2)^2 J_q(\lambda_R)
$$
在教材记号下把 $J_q$ 理解为该期望倒数因子（与 Theorem 28.12 平行）。

---

## Exercise 28.9　不相关无偏估计的最优加权

$\hat\theta_m$ 无偏，$\mathrm{Var}=\ V_m$，彼此不相关；目标最小化 $\mathrm{tr}\,\mathrm{Var}$（未加权 MSE）。

### (a) 两个估计量

$\tilde\theta=w\hat\theta_1+(1-w)\hat\theta_2$（或一般 $w_1+w_2=1$）。不相关 ⇒
$$
\mathrm{tr}\,\mathrm{Var}(\tilde\theta)=w_1^2\mathrm{tr}V_1+w_2^2\mathrm{tr}V_2.
$$
在 $w_1+w_2=1$ 下最优
$$
w_m^*\propto \frac{1}{\mathrm{tr}V_m}
\quad\Rightarrow\quad
\tilde\theta=\frac{\frac{1}{\mathrm{tr}V_1}\hat\theta_1+\frac{1}{\mathrm{tr}V_2}\hat\theta_2}{\frac{1}{\mathrm{tr}V_1}+\frac{1}{\mathrm{tr}V_2}}.
$$

### (b) $M$ 个

$$
\tilde\theta=\sum_{m=1}^M w_m\hat\theta_m,\quad
w_m=\frac{1/\mathrm{tr}V_m}{\sum_{j=1}^M 1/\mathrm{tr}V_j}.
$$

### (c) 解释

权重与 **总方差（迹）成反比**：更精确的估计量权更大。这是标量逆方差加权在“用 $\mathrm{tr}V$ 标量化协方差”时的版本；若目标是 $W$-加权 MSE 且 $V_m$ 可交换结构，应换成 $w_m\propto 1/\mathrm{tr}(WV_m)$。

---

## Exercise 28.10　Mallows 平均准则

### (a)

模型平均拟合 $\hat m(w)=\sum_m w_m\hat m_m=\sum_m w_m P_m Y$，残差
$$
\hat e(w)=Y-\sum_m w_m\hat Y_{\cdot m}=\sum_m w_m\hat e_m
$$
（因 $\sum w_m=1$）。Mallows
$$
C(w)=\|\hat e(w)\|^2+2\tilde\sigma^2\mathrm{tr}\Bigl(\sum_m w_m P_m\Bigr)
=\sum_{i=1}^n\Bigl(Y_i-\sum_m w_m\hat Y_{mi}\Bigr)^2+2\tilde\sigma^2\sum_m w_m K_m.
$$

### (b) 嵌套、无惩罚、最大模型为 $M$

无惩罚时 $C(w)=\|Y-\sum w_m\hat m_m\|^2$。因嵌套，$P_1\le\cdots\le P_M$（投影嵌套），$\hat m_M$ 落在所有较小模型拟合的仿射组合所能张成的空间之“最丰富”端，且
$$
\min_{w\in\Delta}\Bigl\|Y-\sum_m w_m P_m Y\Bigr\|
=\|Y-P_M Y\|
$$
在 $w=(0,\ldots,0,1)$ 达到：任何平均 $\sum w_m P_m$ 的列空间含于 $P_M$ 的列空间，而 $P_MY$ 是 $Y$ 在该最大空间上的投影，平方残差最小。  
**答案：全部权重放在最大模型 $M$ 上**，$\hat w=(0,\ldots,0,1)$。

---

## Exercise 28.11　JMA 准则

Leave-one-out 预测 $\tilde Y_{mi}=X_{mi}'\hat\beta_{m(-i)}$。固定权重 $w$ 的 LOO 残差
$$
\tilde e_i(w)=Y_i-\sum_m w_m\tilde Y_{mi}=\sum_m w_m\tilde e_{mi},
$$
其中 $\tilde e_{mi}=Y_i-\tilde Y_{mi}$。故
$$
\mathrm{CV}(w)=\sum_{i=1}^n\tilde e_i(w)^2
=\sum_{i=1}^n\Bigl(Y_i-\sum_{m=1}^M w_m\tilde Y_{mi}\Bigr)^2.
$$
这就是 JMA（jackknife / stacking）目标函数。

---

## Exercise 28.12　Hispanic women：与 §28.18 平行的选择

### 设定

| 项目 | 取值 |
|------|------|
| 样本 | `cps09mar`，女性且 Hispanic，$n=3003$ |
| 因变量 | $\log(\mathrm{earnings}/(\mathrm{hours}\times\mathrm{week}))$ |
| 共同控制 | 已婚（`marital==1`）、region 2/3/4 虚拟 |
| 经验 | $\mathrm{exp}=\mathrm{age}-\mathrm{educ}-6$ 的 2/4/6 次多项式 |
| 教育 | (1) college≥16；(2) 结点 9 的线性样条；(3) 学历虚拟 12/13/14/16/18/20 |
| 焦点 | $\Delta=\mathbb{E}[\log w\mid\mathrm{exp}=30]-\mathbb{E}[\log w\mid\mathrm{exp}=0]$（同控制） |

九模型网格与 Table 28.1 相同（Model 1–9）。

### 信息准则结果（摘要）

| Model | 教育 | 经验阶 | $100\Delta$（log 点） | se | $100(e^\Delta-1)$ | BIC | AIC | CV | FIC\* |
|------:|------|------:|---------------------:|---:|------------------:|----:|----:|---:|-----:|
| 1 | college | 2 | 24.3 | 3.8 | 27.5 | −3709 | −3757 | 859 | 164 |
| **2** | **spline** | **2** | **35.0** | 3.7 | 41.9 | **−4088** | −4142 | 756 | 52 |
| 3 | dummy | 2 | 35.1 | 3.7 | 42.0 | −4055 | −4133 | 759 | 52 |
| 4 | college | 4 | 36.6 | 4.6 | 44.2 | −3706 | −3766 | 856 | 46 |
| **5** | **spline** | **4** | **46.3** | 4.6 | 58.8 | −4086 | **−4152** | **753** | **13** |
| 6 | dummy | 4 | 46.4 | 4.7 | 59.1 | −4053 | −4143 | 756 | 13 |
| 7 | college | 6 | 37.4 | 6.7 | 45.4 | −3690 | −3762 | 857 | 55 |
| 8 | spline | 6 | 46.7 | 6.8 | 59.5 | −4070 | −4148 | 754 | 28 |
| 9 | dummy | 6 | 47.1 | 7.4 | 60.1 | −4037 | −4139 | 757 | 33 |

（BIC/AIC 为 $n\log(\mathrm{SSE}/n)+(\log n\text{ or }2)k$ 形式，水平仅用于排序；FIC\* 以 Model 9 的 $\Delta$ 为无约束基准，(28.20) 型。）

### 谁被选中？

| 准则 | 入选 | 要点 |
|------|------|------|
| **BIC** | **Model 2** | 样条教育 + 二次经验；最省 |
| **AIC** | **Model 5** | 样条 + 4 次经验 |
| **CV** | **Model 5** | 与 AIC 一致 |
| **FIC\***（焦点 $\Delta$） | **Model 5** | 与 AIC/CV 一致 |

### 解释与优选

1. **与亚洲女性（§28.18）对照：** 那里 BIC→样条+二次，AIC/CV→dummy+4 次，FIC→样条+4 次。Hispanic 样本上 **BIC 仍偏省（Model 2）**，而 **AIC/CV/FIC 齐指 Model 5**（样条+4 次），结构非常相似，只是教育“全虚拟”相对样条的优势在本样本中较弱（Model 5 vs 6 的 CV 接近）。  
2. **效应大小：** 仅 college 虚拟时经验回报明显偏低（Model 1/4/7）；引入教育样条/虚拟后，$100\Delta$ 大约 **35（二次经验）→ 46（四次）**。六次多项式 SE 变大、准则不再改善。  
3. **优选报告：** 综合预测型准则与焦点 FIC，**优先 Model 5**：0→30 年经验约 **46 log 点**（约 **59%** 工资水平差），HC1 se（log 点）约 4.6。同时报告 Model 2（BIC）作为简洁对照，并说明选择后推断的名义 SE 未纠选择不确定性。  
4. **实务：** 多准则一致时（本样本 AIC=CV=FIC）可信度高；若像亚洲女性样本 CV 平坦，则应强调设定不确定性而非单一点估计。

---

## 小结

| 题 | 要点 |
|:--:|------|
| 28.1–28.2 | WMSE 分解；WLS 的 Mallows |
| 28.3–28.4 | AIC 逐步 ↔ $\|t\|$ / 与残差相关 |
| 28.5 | 选择后 $t$ 不可原样解读 |
| 28.6–28.8 | 收缩 WMSE；Stein 改进 |
| 28.9–28.11 | 逆方差加权；MMA/JMA 公式 |
| 28.12 | Hispanic 女性：BIC→M2；AIC/CV/FIC→M5 |

代码：`docs/ch28/Hansen_Ch28_Exercises_Solutions.ipynb`。
