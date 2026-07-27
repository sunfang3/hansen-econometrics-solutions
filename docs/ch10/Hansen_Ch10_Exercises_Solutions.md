# Hansen《Econometrics》第 10 章习题解答

**章节：** Chapter 10 Resampling Methods  
**书稿：** PDF p321–325（印刷页 301–305），§10.32 Exercises  

计算：`Hansen_Ch10_Exercises_Solutions.ipynb`（10.28–10.31 框架；bootstrap 可调 $B$）

---

## Exercise 10.1

$\hat\mu_r=n^{-1}\sum Y_i^r$。Jackknife：删 $i$ 后 $\hat\mu_{r(-i)}$，  
$\hat V_{\mathrm{jack}}=\frac{n-1}{n}\sum_i(\hat\mu_{r(-i)}-\bar\mu_{(\cdot)})^2$。

---

## Exercise 10.2–10.5

仿射 $\theta=a+C\beta$：jack/boot 方差 $C\hat VC'$；percentile 区间仿射变换端点。

---

## Exercise 10.3

两步 $\hat A,\hat W_i=\hat A'Z_i$：jackknife 需 **每删一个观测重算 $\hat A_{(-i)}$ 与 $\hat\beta_{(-i)}$**。

---

## Exercise 10.6

$T^*=(\hat\theta^*-\hat\theta)/s(\hat\theta)$ 用 **原样本 SE**（非 $s^*$）⇒ 分位数变换后区间与 percentile 相同。

---

## Exercise 10.7–10.9

Thm 10.6–10.8：bootstrap 一致性/percentile-t 渐近 pivotal（标准证明：展开 + Polya）。

---

## Exercise 10.10

**(a)** $\hat\theta=1/\bar Y$ 一般 **有偏**（Jensen，$1/x$ 凸于 $\mu>0$）。  
**(b)** 偏倚方向通常 $E[1/\bar Y]>1/\mu$（凸）。  
**(c)** 普通 percentile **不纠偏**；宜 BC/BCa 或 delta。

---

## Exercise 10.11

成对抽 $(X_i,\hat e_i)$ 再 $Y^*=X^{*'}\hat\beta+e^*$ 与直接重抽 $(Y_i,X_i)$ 在 OLS 拟合空间上数值等价（同一经验测度支撑）。

---

## Exercise 10.12

$p^*$ 基于 $\hat\theta^*$ 与 $\hat\theta$ 的排序，严格增 $g$ 保持序 ⇒ $p^*$ 不变；$z_0^*=\Phi^{-1}(p^*)$ 亦不变。

---

## Exercise 10.13

percentile-t 对仿射 $a+c\beta$（$c>0$）端点同步仿射；注意 $c<0$ 时交换端点。

---

## Exercise 10.14

错误：bootstrap 在 **真 $H_0$ 不成立的数据** 上生成，分位数是 **备择下** 的，不是 $H_0$ 临界值。应 **强制施加 $H_0$**（约束估计残差 bootstrap）或用中心化统计量。

---

## Exercise 10.15

**(a)** percentile 95%：$[0.75,1.3]$。  
**(c)** BC/percentile-t 还需要 $\hat\theta$ 在 bootstrap 中的分位信息或 $T^*$，**信息不足**。

---

## Exercise 10.16

**(a)** 固定 $X$，抽 $e^*\sim N(0,\hat\sigma^2)$，$Y^*=X\hat\beta+e^*$。  
**(b)** $\hat\beta^*\mid F_n\sim N(\hat\beta,\hat\sigma^2(X'X)^{-1})$。  
**(c)** 同方差 $t$：$T^*\sim t_{n-k}$。

---

## Exercise 10.17–10.19

$m(x)=x'\beta$：渐近 $x'\hat\beta\pm z\sqrt{x'\hat Vx}$；percentile / percentile-t 对 $\hat m$ 或 $t_m^*$。  
$\mu_3,\sigma^2$：用残差矩 + 对 $(\hat\beta,\hat e)$ 的 bootstrap。

---

## Exercise 10.20–10.21

$H_0:\beta_2=0$ 或 $\beta_1=\beta_2$：在 **约束残差** 下重抽样，算 Wald$^*$/ $t^*$ 分位；或对无约束统计量用中心化 bootstrap。

---

## Exercise 10.22

错误同 10.14：未在 $H_0:\alpha=0$ 下生成数据，$q^*_{.95}$ 过大导致不拒绝。应约束 $\alpha=0$ 后 bootstrap。

---

## Exercise 10.23–10.24

$\theta=\beta_1\beta_2$ 或 $\beta_1/\beta_2$：delta 渐近；percentile 对 $\hat\theta^*$；percentile-t 用 $T^*=(\hat\theta^*-\hat\theta)/s^*(\hat\theta)$。

---

## Exercise 10.25

**不失效**。成对非参数 bootstrap 保留 $(Y,X)$ 联合，含异方差；不需同方差。

---

## Exercise 10.26　RESET bootstrap

所给算法在 $H_1$ 数据上抽，**不正确**。应：在 $H_0$（仅线性）估计，残差重抽或固定 $X$ 加残差，再算 RESET$^*$。

---

## Exercise 10.27

$E[Xe]\neq0$ 时 OLS 不一致，bootstrap 围绕 **错误 plim**，BC percentile **不能**修正识别错误；覆盖对真 $\beta$ 仍差。

---

## Exercise 10.28–10.29

对 Nerlove / MRW：报告 $\hat\beta$ 与 $\theta$ 的 asymptotic / jackknife / bootstrap SE；$\theta$ 的 percentile 与 BC/BCa 区间（notebook）。

---

## Exercise 10.30

小样本（$n=99$）从未结婚中西部白人男性西班牙裔：$\theta$ 的三类 SE 可差很多（杠杆/偏态）；BCa 更合适。

---

## Exercise 10.31

DDK：对学校做 **cluster bootstrap**（重抽学校块）；BCa 区间。聚类 SE 通常 > 个体稳健 SE（见 Ch.4.26）。

---
