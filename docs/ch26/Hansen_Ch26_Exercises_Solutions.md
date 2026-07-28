# Hansen《Econometrics》第 26 章习题完整解答

**章节：** Chapter 26 Multiple Choice  
**书稿：** PDF 第 860–861 页（印刷页约 840–841），§26.14 Exercises（**26.1–26.18 全部**）

**阅读提示（`AGENTS.md`）：** 默认读者熟悉二元 logit，但不默认掌握 MNL / conditional logit / IIA / nested–mixed logit 的识别与边际效应。下文逐步补齐。

**本科搭桥：**
- 二元 logit：$P(Y=1)=\Lambda(X'\beta)$；多元时需 **$J$ 个概率且和为 1**。
- **MNL**：类别特征 $X$ 不随选项变，系数 $\beta_j$ 随选项变（相对 base）。
- **Conditional logit**：选项特征 $X_j$（价格、时间）随选项变，系数 $\gamma$ 常跨选项共用。
- **IIA**：任意两选项的概率比与第三选项无关——红蓝巴士悖论说明其过强。
- 系数尺度依赖误差标准化；解释优先用 **概率 / AME**。

---

## Exercise 26.1　$0\le P_j\le 1$ 且 $\sum_j P_j=1$

### 题意

对 multinomial logit (26.2)
$$
P_j(x)=\frac{\exp(x'\beta_j)}{\sum_{\ell=1}^J\exp(x'\beta_\ell)},
$$
证明概率落在 $[0,1]$ 且对 $j$ 求和为 1。

### 推导

1. 对任意实数 $a$，有 $\exp(a)>0$，故分子、分母均严格为正，于是 $P_j(x)>0$。  
2. 分母是 $J$ 个正项之和，故 $P_j(x)=\dfrac{\text{正}}{\text{更大的正}}<1$，即 $P_j(x)<1$。  
3. 对 $j$ 求和：
$$
\sum_{j=1}^J P_j(x)
=\frac{\sum_j\exp(x'\beta_j)}{\sum_\ell\exp(x'\beta_\ell)}=1.
$$

### 结论

$0<P_j(x)<1$ 且 $\sum_j P_j=1$（边界 0/1 仅在系数趋于 $\pm\infty$ 的极限意义下可取到）。

---

## Exercise 26.2　只依赖系数差 $\beta_j-\beta_J$

### 推导

把分子分母同除以 $\exp(x'\beta_J)$：
$$
P_j(x)
=\frac{\exp\bigl(x'(\beta_j-\beta_J)\bigr)}{\sum_{\ell=1}^J\exp\bigl(x'(\beta_\ell-\beta_J)\bigr)}.
$$
右边只出现差 $\beta_\ell-\beta_J$。若把所有 $\beta_j$ 同时加上同一向量 $\gamma$，则 $x'(\beta_j+\gamma)=x'\beta_j+x'\gamma$，指数上公共因子 $\exp(x'\gamma)$ 在分子分母约掉，**选择概率不变**。故只能识别相对 base 的系数差；常取 $\beta_J=0$。

---

## Exercise 26.3　边际效应等于 (26.4)

$$
\delta_j(x)=\frac{\partial}{\partial x}P_j(x)=P_j(x)\Bigl(\beta_j-\sum_{\ell=1}^J\beta_\ell P_\ell(x)\Bigr).
\tag{26.4}
$$

### 推导

记 $s_\ell=\exp(x'\beta_\ell)$，$S=\sum_m s_m$，则 $P_j=s_j/S$。对向量 $x$ 求梯度（用乘积法则）：
$$
\frac{\partial P_j}{\partial x}
=\frac{(\partial s_j/\partial x)\,S-s_j\,(\partial S/\partial x)}{S^2}.
$$
$\partial s_j/\partial x=s_j\beta_j$，$\partial S/\partial x=\sum_m s_m\beta_m$，故
$$
\frac{\partial P_j}{\partial x}
=\frac{s_j\beta_j\,S-s_j\sum_m s_m\beta_m}{S^2}
=P_j\beta_j-P_j\sum_m P_m\beta_m
=P_j\Bigl(\beta_j-\sum_m\beta_m P_m\Bigr).
$$

**直觉：** 边际效应 = 本选项系数减去“概率加权平均系数”——提高 $x$ 既抬升选项 $j$ 的效用，也抬升其他选项。

---

## Exercise 26.4　条件 logit 概率 (26.8)

模型 $U_j^*=W'\beta_j+X_j'\gamma+\varepsilon_j$，$\varepsilon_j$ i.i.d. Type I extreme value。由 Theorem 26.1（GEV 在 $\tau=1$ 时化为独立极值），
$$
P_j(w,x)=\frac{\exp(w'\beta_j+x_j'\gamma)}{\sum_{\ell}\exp(w'\beta_\ell+x_\ell'\gamma)}.
\tag{26.8}
$$
（证明骨架同 Theorem 26.1：选 $j$ 当且仅当 $\varepsilon_\ell\le\varepsilon_j+\mu_{j\ell}$，对 GEV 密度积分得 softmax 形式。）

---

## Exercise 26.5　条件 logit 边际效应 (26.9)(26.10)

记 $V_j=w'\beta_j+x_j'\gamma$，$P_j=e^{V_j}/\sum e^{V_\ell}$。

### 自身效应 $\partial P_j/\partial x_j$

$x_j$ 只进入 $V_j$，且 $\partial V_j/\partial x_j=\gamma$。与 26.3 相同结构：
$$
\frac{\partial P_j}{\partial x_j}=\gamma\,P_j(1-P_j).
\tag{26.9}
$$

### 交叉效应 $\partial P_j/\partial x_\ell$（$j\neq\ell$）

$x_\ell$ 只进入 $V_\ell$：
$$
\frac{\partial P_j}{\partial x_\ell}=-\gamma\,P_j P_\ell.
\tag{26.10}
$$

**符号：** 若 $\gamma$ 的某分量（如成本）为负，则 **自身 AME 为负、交叉 AME 为正**（替代品变贵 → 本选项概率上升）。且 $\delta_{j\ell}=\delta_{\ell j}$（对称）。

---

## Exercise 26.6　只依赖 $\beta_j-\beta_J$ 与 $x_j-x_J$

同 26.2：分子分母同除 $\exp(w'\beta_J+x_J'\gamma)$，
$$
P_j=\frac{\exp\bigl(w'(\beta_j-\beta_J)+(x_j-x_J)'\gamma\bigr)}{\sum_\ell\exp\bigl(w'(\beta_\ell-\beta_J)+(x_\ell-x_J)'\gamma\bigr)}.
$$
故只依赖系数差与 **选项特征差** $x_j-x_J$。

---

## Exercise 26.7　$\mathrm{AME}_{jj}$ 的估计

由 (26.9)，
$$
\mathrm{AME}_{jj}=\mathbb{E}\bigl[\gamma\,P_j(W,X)\bigl(1-P_j(W,X)\bigr)\bigr].
$$
样本估计：用 MLE $\hat\theta$ 算 $\hat P_{ij}=P_j(W_i,X_i\mid\hat\theta)$，
$$
\widehat{\mathrm{AME}}_{jj}=\hat\gamma\cdot\frac1n\sum_{i=1}^n\hat P_{ij}(1-\hat P_{ij}).
$$
（$\gamma$ 为向量时对每个分量分别做。）

---

## Exercise 26.8　证明 (26.11)（IIA 比值）

由 (26.8)，
$$
\frac{P_j(w,x)}{P_\ell(w,x)}
=\frac{\exp(w'\beta_j+x_j'\gamma)}{\exp(w'\beta_\ell+x_\ell'\gamma)}.
\tag{26.11}
$$
右边 **不含** 任何 $m\notin\{j,\ell\}$ 的 $x_m$ 或 $\beta_m$。这就是 IIA：两选项概率比与“其他选项是否存在/如何定价”无关。

---

## Exercise 26.9　无 $W$ 时的比值

若无 alternative-invariant 的 $W$，则 $\beta_j$ 项消失（或并入不可识别的常数），(26.11) 化为
$$
\frac{P_j(x)}{P_\ell(x)}=\exp\bigl((x_j-x_\ell)'\gamma\bigr).
$$

---

## Exercise 26.10　嵌套 logit：同组内 $P_{jk}/P_{j\ell}$

### 结论

若 $k,\ell$ 同属组 $j$，则
$$
\frac{P_{jk}}{P_{j\ell}}=\frac{P_{k\mid j}}{P_{\ell\mid j}}
=\frac{\exp(\mu_{jk}/\tau_j)}{\exp(\mu_{j\ell}/\tau_j)},
$$
**与其他组的变量无关**（$P_j$ 在比值中约掉）。

### 含义

**组内仍有 IIA**：组内两选项的相对选择不受组外价格影响。嵌套 logit 只放松 **跨组** 的 IIA，不放松组内 IIA。因此同组选项应是“相近替代”，否则分组错误。

---

## Exercise 26.11　嵌套 logit：组间 $P_j/P_\ell$

$$
\frac{P_j}{P_\ell}
=\frac{I_j^{\tau_j}}{I_\ell^{\tau_\ell}},
\quad
I_g=\sum_{m\in g}\exp(\mu_{gm}/\tau_g).
$$
$I_g$ 只依赖组 $g$ 内效用。故 $P_j/P_\ell$ **不依赖其他组变量**——在“组”这一层仍有 IIA。含义：嵌套把“强替代集”收进同一组后，组与组之间仍像条件 logit 那样相对独立。

---

## Exercise 26.12　男性：婚姻状态 MNL ~ 年龄

### 设定

- 数据：`cps09mar`，`female==0`，$n=29140$。  
- 四分类（与 Figure 26.1 一致）：  
  - married：`marital∈{1,2,3,4}`（含丧偶，同正文脚注）；  
  - divorced：5；separated：6；never：7（**base**）。  
- 指数：常数 + age + age²/100（呼应图中非线性年龄剖面）。

### 预测概率（男性）

| 年龄 | Married | Divorced | Separated | Never |
|-----:|--------:|---------:|----------:|------:|
| 25 | 0.39 | 0.02 | 0.01 | **0.58** |
| 35 | 0.74 | 0.06 | 0.02 | 0.19 |
| 45 | 0.82 | 0.10 | 0.02 | 0.07 |
| 55 | 0.83 | 0.11 | 0.02 | 0.05 |
| 65 | 0.82 | 0.10 | 0.02 | 0.06 |
| 75 | 0.76 | 0.07 | 0.02 | 0.15 |

$\log L\approx -20332$。

### 与大学学历女性对比（同规格）

| 年龄 | 男 Married | 女 Married | 男 Never | 女 Never |
|-----:|----------:|----------:|---------:|---------:|
| 25 | 0.39 | 0.39 | 0.58 | 0.58 |
| 45 | 0.82 | 0.74 | 0.07 | 0.10 |
| 65 | 0.82 | 0.63 | 0.06 | 0.13 |
| 75 | 0.76 | 0.47 | 0.15 | 0.35 |

**解读：** 青年段相近；中年后 **男性已婚概率更高、更“粘”**，女性离婚与 never 回升更明显（与 Ch.25 二次 probit 婚姻结论一致）。

---

## Exercise 26.13　年龄≤35 女性：MNL ~ age + education

$n=6645$，$\log L\approx -6020$。Base = never。相对 never 的系数：

| 选项 | 截距 | age | education |
|------|-----:|----:|----------:|
| married | −5.74 | **0.195** | **0.023** |
| divorced | −7.65 | 0.249 | −0.100 |
| separated | −4.06 | 0.154 | −0.224 |

在样本平均年龄下，教育对已婚概率的预测：

| education | P(married) | P(divorced) | P(separated) | P(never) |
|----------:|-----------:|------------:|-------------:|---------:|
| 12 | 0.47 | 0.07 | 0.04 | 0.41 |
| 16 | 0.52 | 0.05 | 0.02 | 0.41 |
| 18 | 0.54 | 0.04 | 0.01 | 0.41 |

**解读：** 年龄提高已婚（相对 never）；教育略提高已婚、降低离婚/分居概率。青年女性中 never 仍约占 41%。

---

## Exercise 26.14　女性：婚姻 nested logit ~ age

### 分组理由

- **{divorced, separated}** 同属“曾进入婚姻后退出/破裂”的相近状态，替代性强 → 放同一 nest。  
- **{married}**、**{never}** 各为单点 nest（$\tau$ 不可识别，固定为 1）。  
- 这样放松“离婚 vs 分居”之间的 IIA，同时保留与已婚/未婚的跨组结构。

### 估计（女性全样本，指数仅含常数+age）

| | Nested | MNL（同效用设定） |
|--|------:|------------------:|
| $\log L$ | **−20105.1** | −20108.7 |
| $\tau_{\{\mathrm{div},\mathrm{sep}\}}$ | **0.36** | （≡1） |

$\tau\approx 0.36\Rightarrow$ 离婚与分居效用冲击正相关（$1-\tau^2\approx 0.87$），嵌套略优于 MNL。  
改进幅度远小于 Koppelman 中 air–car 嵌套（那里 $\Delta\log L$ 约 56），说明婚姻四分类的“强替代对”存在但不极端。

**实务：** 分组应基于经济可替代性，而非“先选组再选内选项”的时间叙事（正文强调 nested logit 是相关结构，不是真正的序贯决策）。

---

## Exercise 26.15　Koppelman：条件 logit 变体

数据：$n=2779$ 商务旅客，四选项 train / air / bus / car。Base = **train**。  
$X_j$：cost, intime（及变体）；$W$：income, urban（air/bus/car 的 ASC + 交互）。

### (a) 复现 Table 26.1 Cond. Logit

| | 估计 | SE | 表 26.1 |
|--|-----:|---:|-------:|
| cost | **−0.0218** | 0.0033 | −0.022 (0.003) |
| intime | **−0.0149** | 0.0007 | −0.015 (0.001) |
| $\log L$ | **−2100.6** | | −2100.6 |

与教材一致。成本、车内时间系数为负：更贵/更久的选项被选概率下降。

### (b) 加入 outtime

| | 估计 | SE |
|--|-----:|---:|
| cost | −0.0150 | 0.003 |
| intime | −0.0178 | 0.001 |
| outtime | **−0.0309** | 0.003 |
| $\log L$ | **−2026.8** | |

$\log L$ 大幅改善。**车外时间**系数更负：换乘/到站时间的负效用强于车内时间（单位分钟）。

### (c) `time = intime + outtime`

| | 估计 | SE |
|--|-----:|---:|
| cost | −0.0153 | 0.003 |
| time | −0.0176 | 0.001 |
| $\log L$ | **−2040.8** | |

总时间合并后拟合介于 (a)(b) 之间：强制车内/车外同系数，**损失** outtime 更强负效用的信息。

### (d) $\log(\mathrm{cost}),\log(\mathrm{intime})$

| | 估计 | SE |
|--|-----:|---:|
| log cost | −4.67 | — |
| log intime | −0.44 | — |
| $\log L$ | **−2082.3** | |

弹性型设定仍显著为负；$\log L$ 略优于线性 (a)，但不及显式拆出 outtime 的 (b)。

---

## Exercise 26.16　Koppelman：嵌套 logit 变体

默认嵌套（表 26.1）：**{train, bus}** 与 **{air, car}**；约束 $\tau_{\mathrm{train,bus}}=1$（教材：无约束估计顶在边界）。

### (a) 复现

| | 本实现 | 表 26.1 |
|--|------:|-------:|
| intime | −0.0055 | −0.005 |
| $\tau(\mathrm{air,car})$ | **0.24** | 0.24 |
| $\log L$ | **−2044.4** | −2044.4 |

$\tau\approx0.24\Rightarrow$ 组内相关约 $1-\tau^2\approx0.94$：**air 与 car 高度相关**，独立误差的条件 logit 设定偏误。  
（cost 点估计对嵌套尺度/参数化较敏感；**似然与 $\tau$ 与教材一致**，解读以 $\tau$ 与相对 $\log L$ 为主。）

### (b) 对数 cost / intime

$\log L\approx -2012$（优于线性嵌套）；$\tau$ 仍显著小于 1 时，同样支持 air–car 相关。对数设定改变系数尺度，比较幅度用 AME/弹性更稳妥。

### (c) 嵌套 {car} vs {train, bus, air}

把三种“非自驾”放一组：$\tau_{\mathrm{public}}\approx 0.66$，$\log L\approx -2091$。  
**可能合理：** 有车族 vs 公共交通/航空的一阶分割。  
**可能不合理：** air 与 train/bus 替代性并不均匀（商务走廊上 air 更贴近 car），强行同组可能不如 {air,car}|{train,bus}。

### (d) 嵌套 {air} vs {train, bus, car}

$\tau_{\mathrm{ground}}\approx 1$，$\log L\approx -2100.6$（几乎退回条件 logit）。  
**含义：** “地面交通”并非高度相关的一类；把 car 与 train/bus 捆在一起 **不符合** 数据中的替代模式（表 26.1 与一般 MNP 都显示 air–car 相关更强）。

---

## Exercise 26.17　Koppelman：混合 logit 变体

设定：intime 系数 $\eta\sim N(\gamma,\sigma^2)$（模拟 $G=100$ 次积分），其余同条件 logit。

### (a) 复现 Table 26.1 Mixed Logit

| | 估计 | 表 26.1 |
|--|-----:|-------:|
| cost | −0.022 | −0.023 |
| $\mathbb{E}[\eta_{\mathrm{intime}}]$ | −0.016 | −0.014 |
| $\sigma(\mathrm{intime})$ | **0.0056** | 0.0048 |
| $\log L$ | **−2096.6** | −2095.5 |

与教材接近。$\sigma$ 约为均值的 1/3：旅行时间负效用 **有异质性，但不极端**。

### (b) 总时间 `intime+outtime`

$\log L\approx -2001$（明显更好）；时间均值更负、$\sigma$ 更大——总时间下异质性更突出（不同旅客对“门到门时间”敏感度差更大）。

### (c) $\eta$ 为 lognormal（对 `-intime`）

令系数 $=-\exp(\mu+\sigma Z)$，保证时间系数为负。  
$\mathbb{E}[\eta]\approx -0.017$，$\log L\approx -2097$（与正态混合相近）。  
**比较：** 对数正态限制符号，避免正态混合下部分人“喜欢更长时间”的正尾；若关心 VOT 分布的右尾，对数正态更常见。均值层面与 (a) 接近，选择可用 LR / 信息准则与经济约束共同决定。

---

## Exercise 26.18　Koppelman：多项 probit

### (a) 简单多项 probit（独立 $N(0,1)$ 误差）

Gauss–Hermite 积分数值似然：

| | 估计 | 表 26.1 Simple MNP |
|--|-----:|------------------:|
| cost | **−0.0184** | −0.018 |
| intime | **−0.0110** | −0.011 |
| $\log L$ | **−2109.3** | −2109.3 |

与教材 **Simple Multi. Probit** 一致。独立正态与 logit 类似，**几乎仍有 IIA 型限制**。

教材 **一般 MNP**（自由相关，$\log L=-2017.4$）给出 cost/intime 幅度更小（约 −0.005），且估计 $\mathrm{Corr}(\mathrm{air},\mathrm{car})\approx 0.99$，与 nested 的 air–car 高相关一致。一般 MNP 需 GHK 模拟极大似然，计算沉重；探索性分析可用 clogit/nested，最终报告可用一般 MNP。

### (b) $\log(\mathrm{cost}),\log(\mathrm{intime})$

简单 MNP：$\log L\approx -2083.9$；对数成本/时间系数仍显著为负，拟合优于线性简单 MNP， qualitatively 与条件 logit 的对数设定一致。

---

## 小结

| 题 | 要点 |
|:--:|------|
| 26.1–26.3 | MNL 概率合法；只识别 $\beta_j-\beta_J$；ME 为 (26.4) |
| 26.4–26.9 | 条件 logit、自身/交叉 ME、IIA 比值 |
| 26.10–26.11 | 嵌套：组内/组间仍保留部分 IIA |
| 26.12–26.14 | CPS 婚姻 MNL / nested：男中年已婚更稳；教育助已婚 |
| 26.15–26.18 | Koppelman：复现表 26.1；outtime 关键；air–car 高相关 |

代码：`docs/ch26/Hansen_Ch26_Exercises_Solutions.ipynb`。
