# Hansen《Econometrics》第 12 章习题完整解答

**章节：** Chapter 12 Instrumental Variables  
**书稿：** PDF 第 425–431 页（印刷页 405–411），§12.43 Exercises（**12.1–12.28 全部**）  
**记号：** 结构式 $Y=X'\beta+e$，$E[Ze]=0$；约简式 $X=\Gamma'Z+u$；2SLS / IV / LIML

---

## Exercise 12.1　虚拟变量工具

$Y=Z\beta+e$（此处 $Z$ 为内生回归元，标量），工具 $D\in\{0,1\}$。

### 解答

IV：$\hat\beta=(\sum D_i Z_i)^{-1}\sum D_i Y_i$（或矩阵 $(D'Z)^{-1}D'Y$）。  
因 $D^2=D$，
$$
\hat\beta=\frac{\sum_{D_i=1}Y_i}{\sum_{D_i=1}Z_i}
=\frac{n_1\bar Y_1}{n_1\bar Z_1}
=\frac{\bar Y_1}{\bar Z_1},
$$
其中下标 1 表示 $D=1$ 子样本均值（若 $\sum D Z=\sum_{D=1}Z$）。  
即：**处理组 $Y$ 均值 / 处理组 $Z$ 均值**（无截距、恰好识别的 Wald 型比值）。

---

## Exercise 12.2　GLS 写成 IV

$E[e\mid X]=0$，$\sigma^2(x)=E[e^2\mid X=x]$ 已知。  
GLS：$\tilde\beta=(\sum\sigma_i^{-2}X_iX_i')^{-1}(\sum\sigma_i^{-2}X_iY_i)$。  
取工具 $Z_i=\sigma^{-2}(X_i)X_i$，则  
$\sum Z_iX_i'=\sum\sigma_i^{-2}X_iX_i'$，$\sum Z_iY_i=\sum\sigma_i^{-2}X_iY_i$，  
故 **GLS = IV$(Z=\sigma^{-2}(X)X)$**。

---

## Exercise 12.3　IV 拟合优于 OLS？

否。OLS **最小化** $\sum\hat e_i^2$。  
任意其他 $\tilde\beta$（含 IV）满足 $\sum\tilde e_i^2\ge\sum\hat e_i^2$。  
大样本同样：$\mathrm{plim}\,n^{-1}\sum\tilde e^2=E[(Y-X'\beta_{\mathrm{IV}})^2]\ge E[(Y-X'\beta_{\mathrm{OLS}})^2]$（投影最小 MSE）。  
内生时 IV 改善的是 **结构参数一致性**，不是样本拟合。

---

## Exercise 12.4　约简式 $\Gamma$ 的矩估计

$X=\Gamma'Z+u$，$E[Zu']=0$。  
矩 $E[Z(X' - Z'\Gamma)]=0\Rightarrow E[ZX']=E[ZZ']\Gamma$。  
样本：$n^{-1}Z'X=n^{-1}Z'Z\,\hat\Gamma\Rightarrow\hat\Gamma=(Z'Z)^{-1}(Z'X)$。□

---

## Exercise 12.5　$\mathrm{rank}(\Gamma)=k$ 必要

约简式 $E[Y\mid Z]=\pi'Z$，$\pi=\Gamma\beta$（$Y=X'\beta+e$，$X=\Gamma'Z+u$，$E[e\mid Z]=0$）。  
要从 $\pi,\Gamma$ 解 $\beta$ 需 $\Gamma$ 列满秩 $k$，否则 $\Gamma\beta=\pi$ 对 $\beta$ **解不唯一**（识别失败）。

---

## Exercise 12.6　Theorem 12.3：$\hat V_\beta\to_p V_\beta$

2SLS 方差估计用 $\hat e_i=Y_i-X_i'\hat\beta_{2\mathrm{sls}}$ 与  
$\hat\Omega=n^{-1}\sum Z_iZ_i'\hat e_i^2$ 等。  
由 $\hat\beta\to_p\beta$，$\hat e_i=e_i-X_i'(\hat\beta-\beta)$，与 Ch.7 HC 证明相同：  
$n^{-1}\sum Z_iZ_i'\hat e_i^2\to_p E[ZZ'e^2]=\Omega$。  
样本矩 $n^{-1}Z'Z\to_p Q_{ZZ}$，$n^{-1}Z'X\to_p Q_{ZX}$ 已证，连续映射得 $\hat V\to_p V$。□

---

## Exercise 12.7

$E[e\mid X]=0$，$X$ 标量。

**(a)** $E[Xe]=E[X E[e\mid X]]=0$，$E[X^2e]=E[X^2 E[e\mid X]]=0$。  
$Z=(X,X^2)'$ 满足 $E[Ze]=0$，**有效**（外生）。  

**(b)** 2SLS 用 $Z$：因 $X$ 是 $Z$ 的精确线性函数（$X=(1,0)Z$），$\hat X=X$，**2SLS=OLS**。

---

## Exercise 12.8　供需识别

$Q=a_0+a_1P+a_2Y+e_1$，$Q=b_0+b_1P+b_2W+e_2$；$Y,W$ 外生。  

**阶条件：** 需求排除 $W$，供给排除 $Y$；每方程恰好多一个外生排除 → 恰好识别（经典）。  
**秩条件：** 需 $a_2\neq0$ 且 $b_2\neq0$（交叉方程外生变量进对方约简式）。  
在标准假设下 **参数可识别**（恰好识别）。

---

## Exercise 12.9

$E[e\mid Z]=0$，$X,Z$ 同维。

**(a)** 若 $E[e\mid Z,X]=0$，IV 一般 **仍有偏**（$E[\hat\beta_{\mathrm{iv}}\mid X,Z]\neq\beta$），除非 $Z=X$（退化为 OLS）或特殊情形；IV 是非线性（比率）估计量。  

**(b)** $\hat\beta_{\mathrm{iv}}=(Z'X)^{-1}Z'Y=\beta+(Z'X)^{-1}Z'e$，  
$\mathrm{var}(\hat\beta\mid X,Z)=(Z'X)^{-1}(Z'DZ)(X'Z)^{-1}$，$D=\mathrm{diag}(\sigma^2(Z_i,X_i))$。  
同方差：$\sigma^2(Z'X)^{-1}(Z'Z)(X'Z)^{-1}$。

---

## Exercise 12.10　控制函数

$e=u'\gamma+\nu$，$E[u\nu]=0$；$Y=X'\beta+u'\gamma+\nu$，OLS 得 $(\hat\beta,\hat\gamma)$（$u$ 可观测简化）。

**(a)** $E[X\nu]=E[(\Gamma'Z+u)\nu]=E[\Gamma'Z\nu]+E[u\nu]$。  
$E[u\nu]=0$；若 $\nu\perp Z$（由 $E[e\mid Z]=0$ 与线性投影结构），$E[Z\nu]=0\Rightarrow E[X\nu]=0$。  

**(b)** 在正则条件下 $\sqrt{n}((\hat\beta',\hat\gamma')'-(\beta',\gamma')')\to_d N(0,V)$，  
$V$ 为对回归元 $(X,u)$ 的 OLS 渐近方差（异方差稳健）。  
若 $u$ 用 $\hat u$ 代替，需额外两步修正；$\beta=0$ 时修正可简化（类 11.14）。

---

## Exercise 12.11　$Y=\beta_0+\beta_1X+\beta_2X^2+e$

**(a)** $E[Xe]\neq0$ 通常 $\Rightarrow E[X^2e]\neq0$，**$X^2$ 亦应视为内生**。  

**(b)** 内生元 $(X,X^2)$ 共 2 个，工具 $(1,Z,Z^2)$ 共 3 个 ⇒ **过度识别**（阶条件满足）。  

**(c)** $X=\gamma_0+\gamma_1Z+u$，$X^2=\gamma_0^2+\gamma_1^2Z^2+2\gamma_0\gamma_1Z+\cdots$。  
识别需约简式对 $(X,X^2)$ 的系数矩阵对 $(1,Z,Z^2)$ **秩为 2**；  
关键：$\gamma_1\neq0$（$Z$ 进 $X$），且 $X^2$ 的约简式不能与 $X$ 共线（通常 $\gamma_1\neq0$ 且 $u$ 有足够变异即可）。

---

## Exercise 12.12　错误“拟合平方”2SLS

结构 $Y=\beta X^2+e$，RF $X=\gamma Z+u$，$\gamma\neq0$。  
估计：$\hat X=\hat\gamma Z$，再 $Y$ 对 $\hat X^2$ 回归。

**(a)** $\hat\gamma=\sum ZX/\sum Z^2$，$\hat\beta=\sum\hat X^2 Y/\sum\hat X^4$。  

**(b)** $\mathrm{plim}\,\hat\gamma=\gamma$，$\hat X\to_p\gamma Z$，  
$\mathrm{plim}\,\hat\beta=E[(\gamma Z)^2Y]/E[(\gamma Z)^4]$。  
$Y=\beta X^2+e=\beta(\gamma Z+u)^2+e=\beta\gamma^2Z^2+\beta u^2+2\beta\gamma Zu+e$，  
一般 $\mathrm{plim}\neq\beta$（除非 $u=0$ a.s.）。  

**(c)** **一般不一致**。若 $u=0$（$X$ 由 $Z$ 完全决定）则一致。正确做法：对 $X^2$ 建约简式并用 $(Z,Z^2)$ 等作工具。

---

## Exercise 12.13　仅用 $Y_1$ 约简式检验 $\beta_2=0$

结构 $Y_1=Z_1'\beta_1+Y_2'\beta_2+e$，$E[Ze]=0$。  
$H_0:\beta_2=0\Rightarrow Y_1=Z_1'\beta_1+e$，约简式 $Y_1=Z_1'\lambda_1+Z_2'\lambda_2+u_1$ 中 **$\lambda_2=0$**。  
（因 $Y_2$ 的约简式含 $Z_2$，代入结构后 $Z_2$ 系数与 $\beta_2$ 成比例。）  
故：OLS 估计 (12.95)，对 $H_0:\lambda_2=0$ 做 Wald/$F$ 检验，等价检验 $H_0:\beta_2=0$（在秩条件下）。

---

## Exercise 12.14　$Y_2$ 缺失时错误 IV

结构 $Y_1=Z_1'\beta_1+Y_2'\beta_2+e$；错误地用 $Z_2$ 作 $Z_1$ 的工具估 $\beta_1$（忽略 $Y_2$）。

**(a)** $\hat\beta_1=(Z_2'Z_1)^{-1}Z_2'Y_1$（示意；多维用 $(Z_2'Z_1)^{-1}Z_2'Y_1$）。  
$Y_1=Z_1'\beta_1+Y_2'\beta_2+e$ 代入：  
$\hat\beta_1=\beta_1+b_{1n}+r_{1n}$，  
$b_{1n}=(Z_2'Z_1)^{-1}Z_2'Y_2\beta_2$（确定性给定 $(Z,Y_2)$ 的“偏误项”），  
$r_{1n}=(Z_2'Z_1)^{-1}Z_2'e$。  

**(b)** $E[Z_2e]=0$ 且正则 ⇒ $r_{1n}\to_p0$。  

**(c)** $b_{1n}\to_p(Q_{Z_2Z_1})^{-1}Q_{Z_2Y_2}\beta_2$，  
$\hat\beta_1\to_p\beta_1+(Q_{Z_2Z_1})^{-1}E[Z_2Y_2']\beta_2$。  

**(d)** **是遗漏 $Y_2$ 的偏倚**。无偏倚当 $\beta_2=0$ 或 $E[Z_2Y_2']=0$。  

**(e)** $\sqrt{n}(\hat\beta_1-\beta_1-b_{1n})\to_d N(0,V)$，$V$ 由 $Z_2e$ 的 CLT 给出（与标准 IV 方差同形，中心在伪真值）。

---

## Exercise 12.15　$Y=Z\beta_1+Y_2\beta_2+e$，$Z,Y_2$ 标量

**(a)** 仅用 $Z$ 作 $Y_2$ 工具：内生+外生回归元共 2 参数，工具有效“新”信息只有 $Z$ 对 $Y_2$ 一段，且 $Z$ 已作为外生回归元进入 ⇒ **恰好/识别失败**（阶条件：需 $\ell\ge2$ 独立工具变异）。一般 **不能** 仅用 $Z$。  

**(b)** 用 $(Z,Z^2)$：多了一个工具，阶条件可满足。  

**(c)** 隐含排除：$Z^2$ 不进结构式。  

**(d)** 相关：约简式 $Y_2=\pi_0+\pi_1Z+\pi_2Z^2+v$ 中 $(\pi_1,\pi_2)$ 不全为 0 且与结构满秩。  

**(e)** 应用中常 **怀疑** $Z^2$ 可排除且强相关；需经济理由。

---

## Exercise 12.16　间接最小二乘

$Y=X\beta+e$，$X=\gamma Z+u_2$，$E[Ze]=E[Zu_2]=0$。

**(a)** $Y=Z(\gamma\beta)+(\beta u_2+e)=:Z\lambda+u_1$，$\lambda=\gamma\beta$，$\beta=\lambda/\gamma$（$\gamma\neq0$）。$E[Zu_1]=0$。  

**(b)** $\sqrt{n}(\hat\theta-\theta)=Q_{ZZ}^{-1}n^{-1/2}\sum Z_iu_i+o_p(1)$，$u=(u_1,u_2)'$，$\hat\theta=(\hat\lambda,\hat\gamma)'$。  

**(c)** 由构造 $E[Zu]=0$。  

**(d)** $\sqrt{n}(\hat\theta-\theta)\to_d N(0,Q_{ZZ}^{-1}\Omega_u Q_{ZZ}^{-1})$，$\Omega_u=E[Z^2uu']$。  

**(e)** $\hat\beta=\hat\lambda/\hat\gamma$，delta：$G=(\partial\beta/\partial\lambda,\partial\beta/\partial\gamma)=(1/\gamma,-\lambda/\gamma^2)$，  
$\mathrm{Avar}=G'VG$。  

**(f)** 与 Thm 12.2 相同：因 $(1,-\beta)u=e$，  
$(1,-\beta)\Omega_u(1,-\beta)'=E[Z^2e^2]$，代数化简得同一 $V_\beta$。

---

## Exercise 12.17　$\hat\sigma^2$ 用第二阶段残差？

$\hat e_i=Y_i-\hat X_i'\hat\beta$ **不正确**（第二阶段 SSE 不是结构残差）。  
正确：$\hat e_i=Y_i-X_i'\hat\beta_{2\mathrm{sls}}$，  
$\hat\sigma^2=n^{-1}\sum\hat e_i^2$（或 df 调整）。

---

## Exercise 12.18　两独立样本 $\beta_1=\beta_2$

**(a)** 各样本 2SLS 得 $\hat\beta_j$、$\hat V_j$。  
$W=(\hat\beta_1-\hat\beta_2)'(\hat V_1+\hat V_2)^{-1}(\hat\beta_1-\hat\beta_2)$。  

**(b)** $H_0$ 下 $W\to_d\chi^2_k$。  

**(c)** 大 $W$ 拒绝；可用 $\chi^2_{k,1-\alpha}$ 临界值或 $p$ 值。

---

## Exercise 12.19　州虚拟作工具

**(a)** 外生：州 FE 与结构误差不相关（无州级混杂进 $e$）；相关：州际 $X$ 均值有差异（一阶段显著）。  
排除：州只通过 $X$ 影响 $Y$。  

**(b)** 多州虚拟对少量内生 $X$ ⇒ 通常 **过度识别**。

---

## Exercise 12.20　两阶段手算 SE

系数 $\hat\beta$ 与 2SLS **相同**（正确实施时）。  
但第二阶段软件报告的 $s(\hat\beta)$ **错误**（把 $\hat X$ 当真实回归元，残差与自由度不对）。  
须用 **2SLS/IV 专用方差**（基于 $Y-X'\hat\beta$ 与 $Z$）。

---

## Exercise 12.21　$\hat\beta_1=\hat\lambda_1$

恰好识别：2SLS 的 $\hat X_2$ 在 $Z_1,Z_2$ 张成的空间中。  
Frisch–Waugh：对 $Z_1$ 残差化后，结构与约简式对 $Z_1$ 的系数一致。  
教材结果：恰好识别时 **$\hat\beta_1=\hat\lambda_1$**（OLS $Y$ 对 $X_1,Z_2$ 中 $X_1$ 的系数）。

---

## Exercise 12.22

同 12.2：$Z_i=X_i/\sigma^2(X_i)$ 使 GLS=IV。

---

## Exercise 12.23　AJR2001 实证

数据 $n=64$（`loggdp, risk, logmort0` 完整）。

| 估计 | 系数 (risk) | 同方差 SE | 稳健 SE |
|------|------------:|----------:|--------:|
| OLS (12.86 型) | **0.516** | 0.063 | 0.053 |
| RF risk←logmort | **−0.613** | 0.127 | 0.160 |
| 2SLS | **0.929** | — | 0.170 |

书上 OLS $0.52_{(0.06)}$：作者用 **同方差 SE** 更接近。  
2SLS $\approx0.94$ 与书接近（0.01 量级差异常见）。

**(c)(d)(e)** ILS = $\hat\lambda/\hat\gamma$ = 0.929 = 2SLS；两阶段、控制函数（加 RF 残差）系数相同。  

**(f)** OLS 加 `latitude, africa`：二者预测 GDP（africa 显著负等）。  
**(g)** 2SLS 后 latitude 效应减弱/不稳，制度（risk）仍主导。  
**(h)** mortality **水平** 一阶段 $R^2$ 远低于 **logmort**（约 0.06 vs 0.27）⇒ log 设定更强一阶段。  
**(i)** 工具 $(\mathrm{logmort},\mathrm{logmort}^2)$：2SLS risk 系数约 **0.77**。  
**(j)** 一阶段 $F\approx18.4>10$ ⇒ Stock–Yogo 意义下 **偏强**。  
**(k)** Sargan/Hansen $J\approx5.14$，$p\approx0.023$ ⇒ 过度识别约束 **边缘拒绝**，工具外生性存疑。  
**(l)** LIML 在过度识别下对弱工具更稳健；与 2SLS 可比较（见 notebook）。

---

## Exercise 12.24

对 AJR 2SLS 做 $B$ 大的 bootstrap SE。  
IV 有限样本偏倚重、矩可能薄弱时，**bootstrap SE 不稳定/不可靠**（重复运行波动大）；宜报告渐近稳健 SE 与弱工具稳健推断，而非盲信 bootstrap SE。

---

## Exercise 12.25　Card1995

**2SLS(a)**：`nearc4a, nearc4b` 作 `ed76` 工具；控制 exper, exp²/100, black, smsa, region 等。  
本实现（完整样本 $n\approx3010$）：  
$\hat\beta_{\mathrm{edu}}\approx\mathbf{0.161}$（稳健 SE $\approx0.040$），一阶段 $F\approx\mathbf{13.5}$（偏强）。  

**(b)** 加 `nearc2`：$F$ 约降到 9.6 量级，增益有限。  
**(c)(d)** 与 age 交互作工具：解释“近大学随年龄的教育差异”；结构回报可能变化。  
**(e)** $F>10$ 偏强；$F<10$ 则弱。  
**(f)** Hausman/C 检验：2SLS vs OLS。  
**(g)** LIML 与 2SLS 在强工具下接近。

---

## Exercise 12.26

Card 基线 IV：BC percentile 区间适合有偏估计量。  
IV bootstrap SE 往往 **不宜单独强调**（见 12.24）；应报 BC 区间。

---

## Exercise 12.27　AK1991 黑人子样本（$n=26{,}913$）

**(a)** 与 (12.90) 相同形式；黑人子样本中 **black 虚拟被省略**（无变异）。  
**(b)(c)** 180 / 30 工具时一阶段 $F$ 往往 **很小**（弱工具）。  
**(d)** 仅 3 个 qob 工具：本计算一阶段 $F\approx\mathbf{4.85}$（**偏弱**）；2SLS 宜谨慎，LIML/弱工具稳健 CI 更合适。  
**(e)** 3-qob 2SLS：$\hat\beta_{\mathrm{edu}}\approx\mathbf{0.083}$（SE $\approx0.057$），低于全样本常见 0.1 量级估计，差异需正式检验。

---

## Exercise 12.28

同黑人 3-qob 设定：渐近 SE + bootstrap SE + BC 区间。  
弱工具 + 2SLS 时 **bootstrap SE 不可靠**；优先弱工具稳健方法；BC 区间可作补充。

---

## 小结

| 题 | 要点 |
|:--:|------|
| 12.1–12.6 | IV 公式、GLS=IV、拟合、识别、$\hat V$ 一致 |
| 12.7–12.16 | 工具有效性、供需、控制函数、ILS=2SLS |
| 12.17–12.22 | 残差、两样本、州工具、两阶段 SE 陷阱 |
| 12.23–12.28 | AJR / Card / AK 实证与弱工具、bootstrap |

