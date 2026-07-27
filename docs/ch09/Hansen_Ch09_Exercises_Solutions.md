# Hansen《Econometrics》第 9 章习题解答

**章节：** Chapter 9 Hypothesis Testing  
**书稿：** PDF p270–276（印刷页 250–256），§9.24 Exercises  

计算：`Hansen_Ch09_Exercises_Solutions.ipynb`

---

## Exercise 9.1

$\bar R^2$ 升 iff 新回归元 $|t|>1$（同方差 SE）。由 $\bar R^2=1-\frac{n-1}{n-k}\frac{\mathrm{SSE}}{\mathrm{SST}}$ 差分即得。

---

## Exercise 9.2

**(a)** $\sqrt{n}((\hat\beta_2-\hat\beta_1)-(\beta_2-\beta_1))\to_d N(0,V_1+V_2)$。  
**(b)** $W=n(\hat\beta_2-\hat\beta_1)'(\hat V_1+\hat V_2)^{-1}(\hat\beta_2-\hat\beta_1)$。  
**(c)** $H_0$ 下 $\to_d\chi^2_k$。

---

## Exercise 9.3–9.4

**(a)** 双侧等尾 ⇒ 渐近水平 $\alpha$。  
**(b)** **差检验**：在备择 $|\theta|$ 大时 $T$ 大应拒绝，但规则在 $|T|$ 很小时也拒绝（无功效方向错误）。应只拒绝大的 $|T|$/$W$。

---

## Exercise 9.5

$H_0:\beta_1-\beta_2=0$：Wald $W=(\hat\beta_1-\hat\beta_2)'\widehat{\mathrm{Var}}^{-1}(\cdot)$ 或约束回归 $X_1+X_2$ 合并。

---

## Exercise 9.6

不同意。多重检验下 20 个 $t$ 中出现 $|t|\approx2.5$ 并不稀有；未校正族错误率；“关键”需理论/联合检验/样本外。

---

## Exercise 9.7 / 9.22

$H_0:E[Y\mid X=40]=20$ 即 $\beta_1+40\beta_2+1600\beta_3+\cdots=20$（按设定）。  
构造 $R'\beta=20$ 的 $t$/Wald。

---

## Exercise 9.8

$Y=X_1'\gamma_1+(X_2-X_1)'\gamma_2+u$ 与原模型再参数化：$\beta_2=\gamma_2$，$\beta_1=\gamma_1-\gamma_2$。  
检验 $\gamma_2=0$ **等价于** $\beta_2=0$。

---

## Exercise 9.9

证据混合：可能功效不足、总体异质、I/II 类错误。应看效应量、CI、效力、预注册；不宜单次“不能拒绝”否定前一拒绝。

---

## Exercise 9.10

**(a)** $T=(\hat\sigma^2-1)/\sqrt{\hat V/n}$。  
**(b)** $\sqrt{n}(\hat\sigma-\sigma)\to_d N(0,V/(4\sigma^2))$。  
**(c)** $T_\sigma=(\hat\sigma-1)/\mathrm{se}$。  
**(d)** $H_0$ 在 $\sigma>0$ 时集合相同；有限样本统计量不同，可给出不同决策。

---

## Exercise 9.11

错误。经验进入线性与平方项，应 **联合** $H_0:\beta_{\mathrm{exp}}=\beta_{\mathrm{exp}^2}=0$（2 个约束）。

---

## Exercise 9.12

不完全正确。更大 $n$ 提高功效，但若 $H_0$ 真，拒绝概率 → $\alpha$ 而非 1；仅当真备择时功效 →1。

---

## Exercise 9.13

指固定非零备择下功效→1。对真 $H_0$ 并不成立。解释：统计显著≠实际显著；大样本宜报告 CI/效应。

---

## Exercise 9.14

**(a)** $\hat C=R'\hat\beta\pm1.96\sqrt{R'\hat V R}$。  
**(b)** 标准对偶：$\theta_0\notin\hat C\Leftrightarrow|T|>1.96$。

---

## Exercise 9.15

**(a)** $B=100$ 时 $\hat p\sim$ 约 $\mathrm{Bin}/B$，$\mathrm{se}\approx\sqrt{0.05\cdot0.95/100}\approx0.022$；7% 与 5% 差不显著。  
**(b)** $B=1000$，$\mathrm{se}\approx0.007$，7% 显示略超拒。

---

## Exercise 9.16

**(a)** $\hat\theta=n^{-1}\sum(e_{1i}^2-e_{2i}^2)$。  
**(b)** $\sqrt{n}(\hat\theta-\theta)\to_d N(0,\mathrm{var}(e_1^2-e_2^2))$。  
**(c)** 样本方差。  
**(d)** $|\sqrt{n}\hat\theta/\hat s|>z_{1-\alpha/2}$。  
**(e)** 未发现拟合差异，非证明两模型等价。

---

## Exercise 9.17

**(a)** $H_0:\beta_2=\beta_4=\beta_5=0$（所有含 $X_2$ 的项）。  
**(b)** 3 维 Wald。  
**(c)** $\chi^2_3$。  
**(d)** $W>\chi^2_{3,1-\alpha}$ 拒绝。

---

## Exercise 9.18

**(a)** $\gamma$ 为 $e$ 对 $Z$ 投影系数。  
**(b)** $\mathrm{plim}=(E[ZZ'])^{-1}E[Ze]$。  
**(c)** 常规 $W=\tilde\gamma'(Z'Z)\cdots$。  
**(d)** $E[ZX']=0$ 时两阶段可忽略，标准 $\chi^2$。  
**(e)** $E[ZX']\neq0$ 时 $\hat e$ 与 $Z$ 相关，极限非标准，需调整。

---

## Exercise 9.19

**(a)** $\mathrm{df}=1$。  
**(b)** 小 $W$ 落在左尾，**不拒绝** $H_0$；假设检验只拒绝右尾大值。

---

## Exercise 9.20

同方差下 $F=\frac{(106-100)/3}{100/(50-8)}\approx0.84$，不显著。需同方差/嵌套假定；异方差宜用稳健 Wald（信息不足精确算）。

---

## Exercise 9.21

$H_0:\beta_1\beta_4-\beta_2\beta_3=0$，delta 法 Wald 1 维。

---

## Exercise 9.23

$\hat p=0.07$，$B=200$，$\mathrm{se}\approx\sqrt{0.05\cdot0.95/200}\approx0.015$；0.07 与 0.05 差约 1.3 se，**证据不足断定超拒**；结论不完整。

---

## Exercise 9.24（Monte Carlo 设计）

**(a)** $\alpha$ 只进截距，斜率/$\theta=e^\beta$ 的 $t$ 对 $\alpha$ 不变。  
**(b)** $\hat\beta$ 近似无偏；$\hat\theta=e^{\hat\beta}$ 有限样本有 Jensen 偏。  
**(c)** 大样本双侧 10% 尾概率约 0.05；小样本 $T_\theta$ 可能校准差。

---

## Exercise 9.25（Invest1993，1987，$n=1028$）

|  | $\hat\beta$ | HC3 SE | 95% CI |
|--|------------:|-------:|--------|
| Q | 0.0028 | 0.0018 | [−0.0007, 0.0063] |
| C | 0.0045 | 0.0234 | [−0.041, 0.050] |
| D | 0.0123 | 0.0072 | [−0.002, 0.026] |
| int | 0.101 | 0.0074 | [0.086, 0.115] |

- $H_0:C=D=0$：Wald≈2.99，$\chi^2_2$ $p\approx0.22$ **不拒绝**  
- $H_0:Q=0$：Wald≈2.42，$p\approx0.12$ **不拒绝**  
- 与 Tobin $q$（仅 Q 显著、C,D=0）**不完全一致**（Q 也不显著）。  
- 六项二次/交互联合 Wald≈5.70，$p\approx0.46$ **不拒绝** 线性。

---

## Exercise 9.26（Nerlove，$n=145$）

**(a)** $\widehat{\log C}=-3.53+0.720\log Q+0.436\log P_L-0.220\log P_K+0.427\log P_F$  
**(b)** $H_0:\beta_3+\beta_4+\beta_5=1$：成本对要素价格 **一次齐次**（无货币幻觉/规模价格）。  
**(c)(d)** CLS/EMD 施加齐次。  
**(e)(f)** Wald≈0.59，$p\approx0.44$ **不拒绝** 齐次；MD 统计量在 $W=V^{-1}$ 时与 Wald 相同。

---

## Exercise 9.27（MRW，$N=1$，$n=98$）

$\hat\beta\approx(-0.288,0.524,-0.506,0.231,3.02)$  
$H_0:\beta_I+\beta_n+\beta_S=0$：Wald≈0.74，$p\approx0.39$ **不拒绝** Solow 约束。

---

## Exercise 9.28（非西班牙裔黑人，$n=4949$）

**(a)** 子样本固定种族 ⇒ 省略 race 虚拟；可用 edu/exp/女/婚姻/地区。  
**(b)** 婚姻虚拟（相对从未结婚）系数全 0：**6 个约束**。  
**(c)** Wald≈40.1，$\chi^2_6$，$p\approx4\times10^{-7}$。  
**(d)** **拒绝**“婚姻不影响工资”。

---

## Exercise 9.29（白人+黑人，$n=39242$）

四组教育回报交互：约 (0.117, 0.119, 0.112, 0.128)。  
共同回报 $H_0$：Wald≈5.65，$\chi^2_3$，$p\approx0.13$ **不拒绝** 共同教育回报。

---
