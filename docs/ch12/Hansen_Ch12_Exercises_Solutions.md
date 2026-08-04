# Bruce Hansen《Econometrics》第 12 章习题解答（详细注释版）

**章节：** Chapter 12 Instrumental Variables
**出版版：** `hansen/manuscripts/Econometrics_Fullbook.pdf`，PDF 第 453–458 页（印刷页 418–423），§12.43 Exercises（**12.1–12.27 全部**）
**记号：** 结构式 $Y=X'\beta+e$，$E[Ze]=0$；约简式 $X=\Gamma'Z+u$；2SLS / IV / ILS / LIML
**数值验证：** `Hansen_Ch12_Exercises_Solutions.ipynb`（12.22 AJR、12.24 Card、12.26 AK + 理论结论的蒙特卡洛验证）

> **写给谁看：** 假设你学过李子奈/陈强，知道"内生性时用工具变量""2SLS 两阶段"，但说不清"**IV/2SLS/ILS/控制函数为什么等价**""**弱工具变量到底坏在哪**""**过度识别检验检验什么**"。
> Hansen 第 12 章是计量经济学的**核心难点**：当 $E[Xe]\ne0$（内生性）破坏 OLS 一致性时，用**外生工具变量** $Z$（$E[Ze]=0$ 且与 $X$ 相关）恢复一致性。本章把 IV/2SLS/ILS/控制函数统一在一个框架里，并严肃讨论**识别、弱工具、过度识别**这些实战关键。

---

## 0. 读题前必看：本章到底在讲什么

**承上启下：**
- 第 2、7 章：OLS 一致需要 $E[Xe]=0$（外生性）。但很多场合 $E[Xe]\ne0$（遗漏变量、联立性、测量误差、自选择）⇒ **OLS 不一致**。
- **第 12 章：找工具变量 $Z$ 修复。** 工具必须满足两条：
  1. **外生性（排除约束）：** $E[Ze]=0$——$Z$ 只能**通过 $X$** 影响 $Y$，不直接进结构误差。
  2. **相关性（强工具）：** $Z$ 与 $X$ **相关**（约简式 $X=\Gamma'Z+u$ 中 $\Gamma\ne0$，即一阶段显著）。

**核心直觉（一张图）：** OLS 把 $Y$ 对 $X$ 回归，但 $X$ 里混着与 $e$ 相关的"脏"部分。IV 的做法：用 $Z$ 把 $X$ 中**与 $Z$ 相关的"干净"部分** $\hat X=P_ZX$ 提取出来，再对 $\hat X$ 回归——"脏"部分被剔除了。

**两个层次（务必分清）：**
- **恰好识别**（$\ell=k$，工具数=内生元数）：IV 估计量 $\hat\beta_{IV}=(Z'X)^{-1}Z'Y$（方阵求逆）。
- **过度识别**（$\ell>k$）：2SLS 估计量 $\hat\beta_{2SLS}=(X'P_ZX)^{-1}X'P_ZY$，$P_Z=Z(Z'Z)^{-1}Z'$。

**四大等价视角（恰好识别时数值完全相同，已 MC 验证）：**
1. **IV**：$\hat\beta=(Z'X)^{-1}Z'Y$。
2. **2SLS**：两阶段——先 $X\sim Z$ 得 $\hat X=P_ZX$，再 $Y\sim\hat X$。
3. **ILS（间接最小二乘）**：$\hat\beta=\hat\lambda/\hat\gamma$（约简式 $Y\sim Z$ 系数 / $X\sim Z$ 系数）。
4. **控制函数**：把一阶段残差 $\hat u=X-\hat X$ 作为**额外回归元**加入结构式 OLS，$\hat\beta$ 与 2SLS 相同；$\hat u$ 的系数 $\hat\gamma$ 显著 ⇒ 检测到内生性（Hausman 型）。

> **实证（蒙特卡洛，已验证）：** $Y=2X+e$，$X=0.5Z+u$，$\mathrm{corr}(u,e)=0.7$（$X$ 内生）：
> - **OLS 均值≈2.56**（偏，与理论 $\mathrm{plim}=\beta+\mathrm{cov}(X,e)/\mathrm{var}(X)=2.56$ 吻合）；
> - **2SLS 均值≈2.00**（一致）；
> - IV=2SLS=ILS 逐样本相同（1.963104=1.963104）；控制函数 $\hat\beta_X=1.963$（=2SLS）、$\hat\gamma_u=0.66$（显著⇒内生）。

**弱工具变量（实战关键，本章反复强调）：**
- 一阶段 $F<10$ ⇒ **弱工具**，2SLS **偏向 OLS**（不一致），推断失效。
- **已验证：** $\gamma=0.5$（$F\approx273$，强）⇒ 2SLS≈2.0；$\gamma=0.1$（$F\approx10$，临界）⇒≈1.88；$\gamma=0.02$（$F\approx0.4$，弱）⇒**≈3.5（严重偏向 OLS plim）**。
- **对策：** 报告一阶段 $F$；弱工具时用 **LIML** 或弱工具稳健推断（Anderson-Rubin）。

> **和本科对照：** 李子奈略提 IV；陈强系统讲 **2SLS、弱工具（$F>10$）、过度识别（Sargan/Hansen $J$）、Hausman 检验**。Hansen 的贡献：把 IV/2SLS/ILS/控制函数统一，渐近理论平行于第 7 章（夹心方差再现），并严肃处理弱工具与识别。

**本章的"夹心"再现（与第 4、7 章同构）：**
$$\sqrt n(\hat\beta_{2SLS}-\beta)\to_d N(0,V_\beta),\quad V_\beta=(Q_{XZ}Q_{ZZ}^{-1}Q_{ZX})^{-1}Q_{XZ}Q_{ZZ}^{-1}\Omega Q_{ZZ}^{-1}Q_{ZX}(Q_{XZ}Q_{ZZ}^{-1}Q_{ZX})^{-1},$$
$\Omega=E[ZZ'e^2]$。同方差下简化为 $\sigma^2(Q_{XZ}Q_{ZZ}^{-1}Q_{ZX})^{-1}$。**结构仍是面包-肉-面包**，只是"面包"换成 $Q_{XZ}Q_{ZZ}^{-1}Q_{ZX}$（反映工具的加权）。

---

## 1. 记号与概念速查（对照李子奈/陈强）

| Hansen 记号 | 中文/本科说法 | 一句话解释 |
|---|---|---|
| $E[Xe]\ne0$ | 内生性 | OLS 不一致的根源 |
| $E[Ze]=0$ | 工具外生性 / 排除约束 | $Z$ 不直接进结构误差 |
| $X=\Gamma'Z+u$（$\Gamma\ne0$） | 约简式 / 工具相关性 | $Z$ 与 $X$ 相关；一阶段显著 |
| $\mathrm{rank}(\Gamma)=k$ | 秩条件（识别） | $\Gamma$ 列满秩才能解出 $\beta$ |
| $\ell\ge k$ | 阶条件 | 工具数 ≥ 内生元数 |
| IV $\hat\beta=(Z'X)^{-1}Z'Y$ | 工具变量估计量 | 恰好识别（$\ell=k$） |
| 2SLS $(X'P_ZX)^{-1}X'P_ZY$ | 两阶段最小二乘 | 过度识别通用 |
| ILS $\hat\lambda/\hat\gamma$ | 间接最小二乘 | 恰好识别时 = IV/2SLS |
| 控制函数 | 控制函数 | 加一阶段残差 $\hat u$，$\hat\gamma$ 检测内生 |
| 一阶段 $F$ | 弱工具诊断 | $F>10$ 偏强；$F<10$ 弱 |
| Sargan/Hansen $J$ | 过度识别检验 | 检验 $E[Ze]=0$；过度识别时可用 |
| Hausman | 外生性检验 | OLS vs 2SLS 是否显著不同 |
| LIML | 有限信息极大似然 | 对弱工具比 2SLS 稳健 |

**两个最常用的"判据"：**
1. **识别 = 阶条件 + 秩条件。** 阶条件：$\ell\ge k$（工具够多）。秩条件：$\mathrm{rank}(\Gamma)=k$（约简式系数矩阵满秩，能从约简式反解 $\beta$）。两者都满足才识别。
2. **工具好坏 = 外生 + 强。** 外生（$E[Ze]=0$）决定一致性；强（一阶段 $F$ 大）决定精度与可靠推断。二者缺一不可。

---

## 2. 预备记号

结构式 $Y=X'\beta+e$，$E[Ze]=0$（$\ell$ 个工具）。约简式 $X=\Gamma'Z+u$，$E[Zu']=0$。
$Q_{ZZ}=E[ZZ']$，$Q_{ZX}=E[ZX']$，$\Omega=E[ZZ'e^2]$。
2SLS：$\hat\beta=(X'P_ZX)^{-1}X'P_ZY$，$P_Z=Z(Z'Z)^{-1}Z'$。
渐近方差 $V_\beta=(Q_{XZ}Q_{ZZ}^{-1}Q_{ZX})^{-1}Q_{XZ}Q_{ZZ}^{-1}\Omega Q_{ZZ}^{-1}Q_{ZX}(Q_{XZ}Q_{ZZ}^{-1}Q_{ZX})^{-1}$。

---

## Exercise 12.1　虚拟变量工具的 IV = 处理组均值之比

**考点：** 最简单的 IV——二元工具 $D\in\{0,1\}$，IV 退化为"Wald 估计量"（处理组 $Y$ 均值 / 处理组 $Z$ 均值）。

**解答：** $\hat\beta=(\sum D_iZ_i)^{-1}\sum D_iY_i$。因 $D^2=D$，
$$\hat\beta=\frac{\sum_{D_i=1}Y_i}{\sum_{D_i=1}Z_i}=\frac{n_1\bar Y_1}{n_1\bar Z_1}=\frac{\bar Y_1}{\bar Z_1}.$$
即**处理组（$D=1$）$Y$ 均值与 $Z$ 均值之比**——经典 **Wald 估计量**。

> **和本科对照：** 这是 Angrist-Card 系列因果推断的起点：用"是否就近上大学"（$D$）作教育（$Z$）的工具，IV 系数就是处理组/控制组的教育回报差比。陈强讲 IV 时常用此类例子。

---

## Exercise 12.2　GLS 可写成 IV（工具 $Z=\sigma^{-2}(X)X$）

**考点：** GLS = 用 $\sigma^{-2}(X)X$ 作工具的 IV——统一视角。

**解答：** GLS $\tilde\beta=(\sum\sigma_i^{-2}X_iX_i')^{-1}\sum\sigma_i^{-2}X_iY_i$。取工具 $Z_i=\sigma^{-2}(X_i)X_i$，则 $\sum Z_iX_i'=\sum\sigma_i^{-2}X_iX_i'$，$\sum Z_iY_i=\sum\sigma_i^{-2}X_iY_i$ ⇒ **GLS = IV$(Z=\sigma^{-2}(X)X)$**。

> **要点：** 任何"加权最小二乘"都能看作"用权重作工具的 IV"。GLS 和 IV 是同一件事的两种表述。

---

## Exercise 12.3　IV 拟合不会优于 OLS

**考点：** 纠正"IV 更好"的误解——IV 改善**一致性**，不是**拟合**。

**解答：** OLS **最小化** $\sum\hat e_i^2$，故任何其他估计（含 IV）满足 $\sum\tilde e_i^2\ge\sum\hat e_i^2$。大样本同理：$\mathrm{plim}\,n^{-1}\sum\tilde e^2\ge\mathrm{plim}\,n^{-1}\sum\hat e^2$。**IV 改善的是结构参数一致性，不是样本拟合优度。**

> **要点：** 内生性下 OLS 拟合"最好"但估错对象；IV 拟合"较差"但估对对象。别用 $R^2$ 比较 OLS 和 IV（同 Ch4 Ex 4.21）。

---

## Exercise 12.4　约简式 $\Gamma$ 的矩估计 = $X$ 对 $Z$ 的 OLS

**解答：** $E[Z(X'-Z'\Gamma)]=0\Rightarrow E[ZX']=E[ZZ']\Gamma$。样本矩：$\hat\Gamma=(Z'Z)^{-1}(Z'X)$——正是 $X$ 对 $Z$ 的多元 OLS（一阶段回归）。□

---

## Exercise 12.5　$\mathrm{rank}(\Gamma)=k$ 是识别的必要条件

**考点：** **秩条件**——为什么工具相关性要用"满秩"表述。

**证明：** 约简式 $E[Y|Z]=\pi'Z$，$\pi=\Gamma\beta$。要从 $\pi,\Gamma$ 解 $\beta$ 需 $\Gamma\beta=\pi$ 有唯一解 ⇒ $\Gamma$ 列满秩 $k$。若 $\mathrm{rank}(\Gamma)<k$，方程组欠定，$\beta$ **解不唯一**（识别失败）。□

> **要点：** 阶条件（$\ell\ge k$）只是"工具够多"的计数；秩条件（$\mathrm{rank}(\Gamma)=k$）才是"真能解出 $\beta$"的实质。

---

## Exercise 12.6　Theorem 12.3：$\hat V_\beta\to_p V_\beta$

**考点：** 2SLS 方差估计一致性——同 Ch7 HC 证明（残差代真误差）。

**证明：** $\hat e_i=e_i-X_i'(\hat\beta-\beta)$，$\hat\beta-\beta=O_p(n^{-1/2})$ ⇒ $n^{-1}\sum Z_iZ_i'\hat e_i^2\to_p E[ZZ'e^2]=\Omega$。结合 $n^{-1}Z'Z\to_p Q_{ZZ}$、$n^{-1}Z'X\to_p Q_{ZX}$ 与连续映射，$\hat V\to_p V$。□

---

## Exercise 12.7　$Z=(X,X^2)$ 有效但 2SLS=OLS

**考点：** 工具"有效"不代表 2SLS≠OLS——当 $X$ 本身外生且是工具的线性组合时退化为 OLS。

**(a)** $E[e|X]=0$ ⇒ $E[Xe]=E[X^2e]=0$，故 $Z=(X,X^2)$ 满足 $E[Ze]=0$，**有效**。

**(b)** 2SLS 用 $Z$：$X$ 是 $Z$ 的精确线性函数（$X=(1,0)Z$），故 $\hat X=X$，**2SLS=OLS**。

> **要点：** 当 $X$ 外生时，把 $X$ 自己当工具 ⇒ 2SLS=OLS。2SLS≠OLS 需要工具里含 $X$ 之外的、与内生部分相关的变量。

---

## Exercise 12.8　供需联立方程的识别

**考点：** 经典**联立方程识别**——阶条件（排除约束）+ 秩条件。

**解答：** 需求 $Q=a_0+a_1P+a_2Y+e_1$（排除 $W$），供给 $Q=b_0+b_1P+b_2W+e_2$（排除 $Y$）。
- **阶条件：** 每方程恰好多排除一个外生变量 ⇒ 恰好识别。
- **秩条件：** 需 $a_2\ne0$ 且 $b_2\ne0$（收入进需求、工资进供给，交叉进对方约简式）。
标准假设下 **恰好识别**。

> **和本科对照：** 这是陈强"联立方程模型"的核心——用排除约束识别每条方程。

---

## Exercise 12.9　IV 的有偏性与条件方差

**(a)** 即便 $X$ 外生（$E[e|Z,X]=0$），IV 一般**仍有偏**（$E[\hat\beta_{IV}|X,Z]\ne\beta$），除非 $Z=X$（退化为 OLS）——IV 是非线性（比率）估计量，有限样本有偏。

**(b)** $\hat\beta_{IV}=\beta+(Z'X)^{-1}Z'e$，$\mathrm{var}(\hat\beta|X,Z)=(Z'X)^{-1}(Z'DZ)(X'Z)^{-1}$，$D=\mathrm{diag}(\sigma^2(Z_i,X_i))$。同方差：$\sigma^2(Z'X)^{-1}(Z'Z)(X'Z)^{-1}$。

> **要点：** IV 是**一致但有偏**的（小样本偏，大样本一致）。这正是 bootstrap 在 IV 上不稳的原因（出版版 12.23）。

---

## Exercise 12.10　控制函数

**考点：** 控制函数法——把内生性"显式"建模进误差，再加残差回归。

**(a)** $e=u'\gamma+\nu$，$E[u\nu]=0$。$Y=X'\beta+u'\gamma+\nu$，OLS 得 $(\hat\beta,\hat\gamma)$。$E[X\nu]=E[(\Gamma'Z+u)\nu]=E[u\nu]=0$（用 $E[Z\nu]=0$、$E[u\nu]=0$）。

**(b)** $\sqrt n((\hat\beta',\hat\gamma')'-(\beta',\gamma')')\to_d N(0,V)$，$V$ 为对 $(X,u)$ 的 OLS 渐近方差。若用 $\hat u$ 代 $u$，需两步修正；$\beta=0$ 时简化（类 11.14）。

> **和本科对照：** 控制函数（陈强、Wooldridge）= 加一阶段残差 $\hat u$，其系数显著 ⇒ 内生。它与 2SLS 给相同 $\hat\beta$（已 MC 验证）。

---

## Exercise 12.11　$X^2$ 亦内生；$(1,Z,Z^2)$ 过度识别

**(a)** $E[Xe]\ne0$ 通常 ⇒ $E[X^2e]\ne0$，**$X^2$ 亦应视为内生**。

**(b)** 内生元 $(X,X^2)$ 共 2，工具 $(1,Z,Z^2)$ 共 3 ⇒ **过度识别**（$\ell=3>k=2$，阶条件满足）。

**(c)** 识别需 $X^2$ 对 $(1,Z,Z^2)$ 的约简式与 $X$ 的不共线，关键 $\gamma_1\ne0$。

---

## Exercise 12.12　错误的"拟合平方"2SLS（不一致！）

**考点：** 2SLS 的常见**误用**——对非线性变换 $X^2$ 直接用 $\hat X^2$ 当拟合值是**错的**。

**(a)** $\hat\gamma=\sum ZX/\sum Z^2$，$\hat\beta=\sum\hat X^2Y/\sum\hat X^4$。

**(b)(c)** $\hat X\to_p\gamma Z$，$\mathrm{plim}\,\hat\beta=E[(\gamma Z)^2Y]/E[(\gamma Z)^4]$。展开 $Y=\beta(\gamma Z+u)^2+e=\beta\gamma^2Z^2+\beta u^2+\cdots$ ⇒ 一般 $\mathrm{plim}\ne\beta$（除非 $u=0$）。**不一致。**

**正确做法：** 对 $X^2$ 单独建约简式（用 $Z,Z^2$ 等作工具），而非对 $\hat X$ 取平方。

> **要点：** 2SLS 是"对**线性**投影取拟合"——非线性变换（$X^2$、$\log X$）不能先拟合再变换，要重新建约简式。

---

## Exercise 12.13　仅用 $Y_1$ 约简式检验 $\beta_2=0$

**考点：** 用约简式做结构检验——$H_0:\beta_2=0$ 等价于约简式中 $Z_2$ 系数 $\lambda_2=0$。

**解答：** 结构 $Y_1=Z_1'\beta_1+Y_2'\beta_2+e$。$H_0:\beta_2=0$ ⇒ $Y_1=Z_1'\beta_1+e$ ⇒ 约简式 $Y_1=Z_1'\lambda_1+Z_2'\lambda_2+u_1$ 中 **$\lambda_2=0$**（因 $Y_2$ 的约简式含 $Z_2$，代入结构后 $Z_2$ 系数与 $\beta_2$ 成比例）。故 OLS 估 (12.95)，对 $H_0:\lambda_2=0$ 做 Wald/$F$，等价检验 $H_0:\beta_2=0$。

> **要点：** 约简式检验避免直接估结构，在识别不确定时有用（Hausman-Wu 思想）。

---

## Exercise 12.14　遗漏 $Y_2$ 的错误 IV ⇒ 遗漏变量偏差

**(a)** $\hat\beta_1=\beta_1+b_{1n}+r_{1n}$，$b_{1n}=(Z_2'Z_1)^{-1}Z_2'Y_2\beta_2$（偏误项），$r_{1n}=(Z_2'Z_1)^{-1}Z_2'e$。
**(b)(c)** $r_{1n}\to_p0$（$E[Z_2e]=0$）；$\hat\beta_1\to_p\beta_1+(Q_{Z_2Z_1})^{-1}E[Z_2Y_2']\beta_2$。
**(d)** **是遗漏变量偏差**。无偏当 $\beta_2=0$ 或 $E[Z_2Y_2']=0$。
**(e)** $\sqrt n(\hat\beta_1-\beta_1-b_{1n})\to_d N(0,V)$（中心在伪真值）。

> **要点：** IV 估错模型（漏掉 $Y_2$）和 OLS 漏变量一样会产生偏差——工具不修模型设定错误。

---

## Exercise 12.15　仅用 $Z$ 不足；$(Z,Z^2)$ 可行

**(a)** 仅用 $Z$ 作 $Y_2$ 工具：内生+外生回归元共 2 参数，但 $Z$ 已作外生回归元进入 ⇒ **识别失败**（阶条件：需 $\ell\ge2$ 独立工具变异）。
**(b)** 用 $(Z,Z^2)$：多一个工具，阶条件满足。
**(c)** 隐含排除：$Z^2$ 不进结构式。
**(d)** 相关：约简式 $Y_2=\pi_0+\pi_1Z+\pi_2Z^2+v$ 中 $(\pi_1,\pi_2)$ 不全 0。
**(e)** 应用中常**怀疑** $Z^2$ 可排除且强相关——需经济理由。

---

## Exercise 12.16　间接最小二乘（ILS）= 2SLS

**考点：** ILS 与 2SLS 的等价——恰好识别下 $\hat\beta=\hat\lambda/\hat\gamma$。

**(a)** $Y=Z(\gamma\beta)+(\beta u_2+e)=Z\lambda+u_1$，$\lambda=\gamma\beta$，$\beta=\lambda/\gamma$（$\gamma\ne0$）。
**(d)** $\sqrt n(\hat\theta-\theta)\to_d N(0,Q_{ZZ}^{-1}\Omega_uQ_{ZZ}^{-1})$。
**(e)** delta：$G=(1/\gamma,-\lambda/\gamma^2)$，$\mathrm{Avar}=G'VG$。
**(f)** **与 Thm 12.2 相同**：$(1,-\beta)u=e$，代数化简得同一 $V_\beta$。

> **已验证：** 恰好识别下 IV=2SLS=ILS 逐样本数值相同。

---

## Exercise 12.17　$\hat\sigma^2$ 不能用第二阶段残差

**解答：** $\hat e_i=Y_i-\hat X_i'\hat\beta$（第二阶段残差）**不正确**——它不是结构残差。正确：$\hat e_i=Y_i-X_i'\hat\beta_{2SLS}$（用**原 $X$**，非 $\hat X$），$\hat\sigma^2=n^{-1}\sum\hat e_i^2$。

> **要点：** 2SLS 的方差必须用 $Y-X'\hat\beta$（原 $X$）算，不能用 $Y-\hat X'\hat\beta$（拟合 $\hat X$）——后者把内生性又放回了残差。软件的 `ivregress` 自动正确；手算两阶段会错（见 12.20）。

---

## Exercise 12.18　两独立样本 $\beta_1=\beta_2$

**(a)** 各样本 2SLS 得 $\hat\beta_j,\hat V_j$。$W=(\hat\beta_1-\hat\beta_2)'(\hat V_1+\hat V_2)^{-1}(\hat\beta_1-\hat\beta_2)$（独立⇒方差相加，同 Ch9 Ex 9.2、Ch11 Ex 11.18）。
**(b)** $H_0$ 下 $W\to_d\chi^2_k$。
**(c)** 大 $W$ 拒绝。

---

## Exercise 12.19　州虚拟作工具

**(a)** 外生：州 FE 与结构误差不相关；相关：州际 $X$ 均值有差异（一阶段显著）；排除：州只通过 $X$ 影响 $Y$。
**(b)** 多州虚拟对少量内生 $X$ ⇒ 通常**过度识别**。

---

## Exercise 12.20　两阶段手算的 SE 是错的

**解答：** 系数 $\hat\beta$ 与 2SLS **相同**（正确实施时）。但第二阶段软件报告的 $s(\hat\beta)$ **错误**（把 $\hat X$ 当真实回归元，残差与自由度不对）。须用 **2SLS/IV 专用方差**（基于 $Y-X'\hat\beta$ 与 $Z$，见 12.17）。

> **要点：** 手动两阶段（先拟合 $\hat X$，再 `lm(Y~Xhat)`）会得到正确的**系数**但错误的**标准误**。永远用 `ivregress`/`ivreg` 专用命令。

---

## Exercise 12.21　已知条件方差时 GLS=IV（同 12.2）

**题意翻译：** 标量回归 $Y_i=X_i\beta+e_i$ 中，$X_i\in\mathbb R$，且条件方差 $\sigma^2(x)=E[e_i^2\mid X_i=x]$ 已知。目标是找一个工具 $Z_i$，使恰好识别的 IV 估计量与 GLS 完全相同。

**第 1 步：写出 GLS。** 观测 $i$ 的最优权重是条件方差的倒数 $w_i=1/\sigma^2(X_i)$，所以
$$
\hat\beta_{\mathrm{gls}}
=\frac{\sum_{i=1}^n w_iX_iY_i}{\sum_{i=1}^n w_iX_i^2}
=\frac{\sum_i X_iY_i/\sigma^2(X_i)}{\sum_i X_i^2/\sigma^2(X_i)}.
$$

**第 2 步：写出标量、恰好识别 IV。** 对任意标量工具 $Z_i$，样本矩条件 $\sum_i Z_i(Y_i-X_i\beta)=0$ 给出
$$
\hat\beta_{\mathrm{iv}}=\frac{\sum_i Z_iY_i}{\sum_i Z_iX_i}.
$$

**第 3 步：逐项匹配分子与分母。** 取
$$
\boxed{Z_i=\frac{X_i}{\sigma^2(X_i)}}
$$
便有 $\sum_iZ_iY_i=\sum_iX_iY_i/\sigma^2(X_i)$，且 $\sum_iZ_iX_i=\sum_iX_i^2/\sigma^2(X_i)$。因此
$$\boxed{\hat\beta_{\mathrm{iv}}=\hat\beta_{\mathrm{gls}}}.$$

**为什么这个工具有效？** 若原模型满足 $E[e_i\mid X_i]=0$，则 $Z_i$ 是 $X_i$ 的已知函数，故迭代期望给出 $E[Z_ie_i]=E[Z_iE(e_i\mid X_i)]=0$；只要 $E[X_i^2/\sigma^2(X_i)]>0$，相关性（秩条件）也成立。本科里的“按标准差加权”在 Hansen 的矩条件语言下，正好就是选择了一个有效率的工具。

---

## Exercise 12.22（AJR2001）　制度与GDP：经典 IV 实证

数据 $n=64$（`loggdp, risk, logmort0`）。

| 估计 | 系数 (risk) | 同方差 SE | 稳健 SE |
|------|------------:|----------:|--------:|
| OLS | **0.516** | 0.063 | 0.053 |
| RF risk←logmort | **−0.613** | 0.127 | 0.160 |
| 2SLS | **0.929** | — | 0.170 |

**(c)(d)(e)** ILS=$\hat\lambda/\hat\gamma$=0.929=2SLS；两阶段、控制函数（加 RF 残差）系数相同（四大等价，已验证）。
**(f)(g)** 加 `latitude, africa`：制度（risk）仍主导。
**(h)** mortality **水平**一阶段 $R^2$≈0.06 远低于 **logmort**≈0.27 ⇒ log 设定更强一阶段。
**(i)** 工具 $(\mathrm{logmort},\mathrm{logmort}^2)$：2SLS risk≈**0.77**。
**(j)** 一阶段 $F\approx18.4>10$ ⇒ Stock–Yogo 意义下**偏强**。
**(k)** Sargan/Hansen $J\approx5.14$，$p\approx0.023$ ⇒ 过度识别约束**边缘拒绝**，工具外生性存疑。
**(l)** LIML 在过度识别下对弱工具更稳健。

> **和本科对照：** AJR（ Acemoglu-Johnson-Robinson 2001）是 IV 因果识别的标志性论文——用殖民者早期死亡率作"制度"的工具，识别制度对 GDP 的因果效应。$F>10$ 支持强工具，但 Sargan 边缘拒绝提示外生性争议。

---

## Exercise 12.23　IV 的 bootstrap SE 不稳

对 AJR 2SLS 做 bootstrap SE。IV 有限样本偏倚重、矩可能薄弱 ⇒ **bootstrap SE 不稳定/不可靠**（重复运行波动大）。宜报告渐近稳健 SE 与弱工具稳健推断，而非盲信 bootstrap SE。

> **要点（接 Ch10）：** bootstrap 对 IV 不如对 OLS 可靠——IV 是有偏非线性估计量，小样本矩薄弱。弱工具时尤其不稳。

---

## Exercise 12.24（Card1995）　教育回报：就近上大学作工具

**2SLS(a)：** `nearc4a, nearc4b` 作 `ed76` 工具；控制 exper, exp²/100, black, smsa, region 等。完整样本 $n\approx3010$：$\hat\beta_{\mathrm{edu}}\approx\mathbf{0.161}$（稳健 SE≈0.040），一阶段 $F\approx\mathbf{13.5}$（偏强）。
**(b)** 加 `nearc2`：$F$ 约降到 9.6 量级，增益有限。
**(c)(d)** 与 age 交互作工具。
**(e)** $F>10$ 偏强；$F<10$ 弱。
**(f)** Hausman/C 检验：2SLS vs OLS。
**(g)** LIML 与 2SLS 在强工具下接近。

> **和本科对照：** Card (1995) 是教育回报 IV 的经典——用"是否住在四年制大学附近"作教育的工具，IV 估计（0.16）高于 OLS，修正了 OLS 的向下偏误。

---

## Exercise 12.25　Card IV 的 BC 区间

IV 基线：BC percentile 区间适合有偏估计量。IV bootstrap SE 往往**不宜单独强调**（见出版版 12.23）；应报 BC 区间。

---

## Exercise 12.26（AK1991）　黑人子样本（3 QOB）

**(a)** 黑人子样本中 `black` 虚拟被省略（无变异）。
**(b)(c)** 180/30 工具时一阶段 $F$ 往往**很小**（弱工具）。
**(d)** 仅 3 个 qob 工具：一阶段 $F\approx\mathbf{4.85}$（**偏弱**）；2SLS 宜谨慎，LIML/弱工具稳健 CI 更合适。
**(e)** 3-qob 2SLS：$\hat\beta_{\mathrm{edu}}\approx\mathbf{0.083}$（SE≈0.057）。

> **和本科对照：** Angrist-Krueger (1991) 用出生季度（QOB）作教育工具——**经典弱工具案例**。全样本 $F$ 大但黑人子样本 $F\approx4.85<10$，2SLS 不可靠（已验证：弱工具时 2SLS 偏向 OLS）。

---

## Exercise 12.27　弱工具下的推断

同黑人 3-qob 设定：渐近 SE + bootstrap SE + BC 区间。弱工具 + 2SLS 时 **bootstrap SE 不可靠**；优先弱工具稳健方法（Anderson-Rubin CI）；BC 区间可作补充。

---

## 附录 A：IV/2SLS/ILS/控制函数等价性（恰好识别）

| 方法 | 做法 | 结果 |
|---|---|---|
| IV | $\hat\beta=(Z'X)^{-1}Z'Y$ | $\hat\beta$ |
| 2SLS | $Y$ 对 $\hat X=P_ZX$ 回归 | 同 $\hat\beta$ |
| ILS | $\hat\lambda/\hat\gamma$（两个约简式系数比） | 同 $\hat\beta$ |
| 控制函数 | 加一阶段残差 $\hat u$，OLS | 同 $\hat\beta$；$\hat\gamma$ 检测内生 |

**已验证：** 四者逐样本数值相同（蒙特卡洛 1.963104=1.963104）。控制函数的 $\hat\gamma_u$ 显著（0.66）⇒ 检测到内生性（Hausman 型）。

---

## 附录 B：弱工具诊断与对策

| 一阶段 $F$ | 状态 | 2SLS 表现 | 对策 |
|---|---|---|---|
| $F>10$ | 强工具 | 一致、推断可靠 | 报告 2SLS |
| $6<F<10$ | 中等 | 轻度偏 OLS | 报告 + LIML 对照 |
| $F<6$ | 弱工具 | **严重偏 OLS**（已验证 $F=0.4$⇒2SLS=3.5 vs β=2） | LIML / Anderson-Rubin CI |

**已验证：** $\gamma=0.5\Rightarrow F\approx273$（强, 2SLS≈2.0）；$\gamma=0.02\Rightarrow F\approx0.4$（弱, 2SLS≈3.5，偏向 OLS plim）。

---

## 附录 C：notebook 单元对应

| 习题 | notebook 内容 |
|------|----------------|
| 12.22 | AJR2001 OLS/RF/2SLS/ILS/控制函数 + 一阶段 F + Sargan code cell |
| 12.24 | Card1995 2SLS + 一阶段 F code cell |
| 12.26 | AK1991 黑人子样本 3-QOB 2SLS + 一阶段 F code cell |
| 理论验证 | 蒙特卡洛：2SLS 一致性 vs OLS 偏差、IV=2SLS=ILS、控制函数、弱工具偏差 code cell |
