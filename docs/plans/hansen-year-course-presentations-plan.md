# Hansen 全年计量经济学 Quarto 讲义实施计划

**Version:** 1.0  
**Date:** 2026-08-02  
**Requirements:** `docs/plans/hansen-year-course-presentations-requirements.md`

## 1. 高层架构

`presentation/` 是与现有习题解答平行的独立 Quarto `default` project。项目根目录只负责渲染目标、输出目录、书目信息和通用语言；`sessions/_metadata.yml` 统一提供 RevealJS 课堂演示配置，`supplements/_metadata.yml` 统一提供可滚动 HTML 文档配置。这样既能让 40 次课堂讲义具有一致的讲者视图、页码和主题，也能让矩阵、概率、渐近工具等长篇补充材料保持适合课后阅读的文档形态。

内容数据流如下：

```text
Hansen 2021 书稿 ──章节/页码──┐
                              ├─> 40 次中文课件 ──> RevealJS HTML
docs/chXX 逐步习题解答 ──链接──┤        │
                              │        ├─> 中文教师备注
R companions / 本地数据 ─可选─┘        └─> 课堂检查与课后练习

Appendix A/B + Ch.6 ──> 6 份中文补充讲义 ──> 可滚动 HTML
课程覆盖表 + syllabus ──> 章节、课次、补充材料双向导航
静态检查脚本 ──> 数量、结构、链接、备注、阅读页码检查
```

渲染不得强制读取被 `.gitignore` 忽略的 `hansen/`。工作坊中的 R 代码默认展示但不执行；需要数据时给出相对仓库根目录的路径和明确的执行说明。共享 SCSS 只负责中文字体、字号、公式、表格、步骤框和溢出预防，不给各课次复制独立样式。

## 2. 40 次课程文件与覆盖映射

### 第一学期：从本科回归到现代推断（20 次）

| 次 | 类型 | 文件 | 核心内容 | Hansen 覆盖 |
|---:|---|---|---|---|
| 01 | 主课 | `presentation/sessions/01-course-orientation.qmd` | 课程诊断、计量对象、数据结构、复现规范 | Ch.1，书内 1–12；Preface |
| 02 | 主课 | `presentation/sessions/02-matrix-algebra-i.qmd` | 向量、矩阵、秩、逆、线性方程、维数检查 | Appendix A 选讲 |
| 03 | 主课 | `presentation/sessions/03-matrix-algebra-ii.qmd` | 正交投影、幂等矩阵、二次型、分块矩阵、矩阵微分 | Appendix A 选讲 |
| 04 | 主课 | `presentation/sessions/04-probability-conditioning.qmd` | 联合分布、条件期望、LIE、方差分解、常用不等式 | Ch.2 前半；Appendix B |
| 05 | 主课 | `presentation/sessions/05-cef-and-projection.qmd` | CEF、BLP、预测误差、遗漏变量与因果解释 | Ch.2，书内 14–61 |
| 06 | 主课 | `presentation/sessions/06-least-squares-algebra.qmd` | 正规方程、$P/M$、FWL、杠杆与留一法 | Ch.3，书内 62–96 |
| 07 | 工作坊 | `presentation/sessions/07-workshop-matrix-ols.qmd` | 手算与 R 验证投影、FWL、CEF/BLP 差异 | Ch.2–3 |
| 08 | 主课 | `presentation/sessions/08-ols-finite-sample.qmd` | 随机抽样、无偏性、方差、Gauss–Markov、GLS | Ch.4 前半 |
| 09 | 主课 | `presentation/sessions/09-robust-and-clustered-se.qmd` | HC 方差、聚类抽样、聚类层级与解释 | Ch.4 后半，书内 97–136 |
| 10 | 主课 | `presentation/sessions/10-normal-regression-transition.qmd` | 正态回归精确分布；从有限样本到渐近推断 | Ch.5；Ch.6 导入 |
| 11 | 主课 | `presentation/sessions/11-asymptotic-toolkit.qmd` | 收敛模式、WLLN、CLT、CMT、Slutsky、delta method | Ch.6；Appendix B |
| 12 | 工作坊 | `presentation/sessions/12-workshop-finite-vs-asymptotic.qmd` | Monte Carlo 比较精确、渐近、稳健与聚类推断 | Ch.4–7 |
| 13 | 主课 | `presentation/sessions/13-ols-asymptotics.qmd` | OLS 一致性、渐近正态、夹心方差、参数函数 | Ch.7，书内 162–195 |
| 14 | 主课 | `presentation/sessions/14-restrictions-minimum-distance.qmd` | 约束 LS、最小距离、有效权重、Hausman equality | Ch.8，书内 196–220 |
| 15 | 主课 | `presentation/sessions/15-hypothesis-testing.qmd` | 检验逻辑、功效、Wald/LM/距离/$F$、局部备择 | Ch.9，书内 221–256 |
| 16 | 主课 | `presentation/sessions/16-resampling-methods.qmd` | Jackknife、Bootstrap、BCa、零假设下重抽样 | Ch.10，书内 257–305 |
| 17 | 工作坊 | `presentation/sessions/17-workshop-testing-bootstrap.qmd` | 功效模拟、Bootstrap CI/检验、cluster bootstrap | Ch.9–10 |
| 18 | 主课 | `presentation/sessions/18-multivariate-regression.qmd` | 多方程堆叠、SUR、系统推断、PCA/因子桥接 | Ch.11，书内 307–331 |
| 19 | 主课 | `presentation/sessions/19-instrumental-variables-i.qmd` | 内生性、矩条件、识别、IV/2SLS、控制函数 | Ch.12 前半 |
| 20 | 工作坊 | `presentation/sessions/20-workshop-iv-identification.qmd` | 2SLS 手算、第一阶段、弱工具模拟、识别诊断 | Ch.12 |

### 第二学期：依赖数据、半/非参数与现代方法（20 次）

| 次 | 类型 | 文件 | 核心内容 | Hansen 覆盖 |
|---:|---|---|---|---|
| 21 | 主课 | `presentation/sessions/21-instrumental-variables-ii.qmd` | 弱/多工具、LATE、异质效应、推断陷阱 | Ch.12 后半，书内 332–411 |
| 22 | 主课 | `presentation/sessions/22-gmm.qmd` | 矩条件、两步 GMM、有效权重、$J$ 检验与内生性检验 | Ch.13，书内 412–440 |
| 23 | 主课 | `presentation/sessions/23-time-series-foundations.qmd` | 平稳、遍历、MDS、Wold、预测 | Ch.14 前半 |
| 24 | 主课 | `presentation/sessions/24-time-series-regression-hac.qmd` | ARMA、动态回归、时间序列 CLT、HAC | Ch.14 后半，书内 442–508 |
| 25 | 工作坊 | `presentation/sessions/25-workshop-time-series.qmd` | ARMA 诊断、HAC 与时间序列预测 | Ch.14 |
| 26 | 主课 | `presentation/sessions/26-var-svar.qmd` | VAR、伴随矩阵、IRF、Granger 因果、结构识别 | Ch.15，书内 509–546 |
| 27 | 主课 | `presentation/sessions/27-unit-roots.qmd` | 随机趋势、FCLT、伪回归、DF/ADF 非标准极限 | Ch.16 前半 |
| 28 | 主课 | `presentation/sessions/28-cointegration.qmd` | 协整、误差修正、Johansen 思路与谨慎表述 | Ch.16 后半，书内 547–596 |
| 29 | 工作坊 | `presentation/sessions/29-workshop-var-unit-root.qmd` | VAR/SVAR、ADF/KPSS、Johansen 的设定与解释 | Ch.15–16 |
| 30 | 主课 | `presentation/sessions/30-panel-fe-re.qmd` | 误差成分、within、FE/RE、聚类推断 | Ch.17 前半 |
| 31 | 主课 | `presentation/sessions/31-dynamic-panel-gmm.qmd` | Nickell 偏误、AB/BB GMM、工具矩阵与工具膨胀 | Ch.17 后半，书内 597–649 |
| 32 | 主课 | `presentation/sessions/32-difference-in-differences.qmd` | 潜在结果、平行趋势、TWFE 与常见错误 | Ch.18，书内 650–664 |
| 33 | 工作坊 | `presentation/sessions/33-workshop-panel-did.qmd` | FE/RE、动态面板与 DiD 的聚类和诊断 | Ch.17–18 |
| 34 | 主课 | `presentation/sessions/34-nonparametric-and-series.qmd` | 核/局部多项式、带宽、级数、部分线性与 NPIV | Ch.19、Ch.20，书内 666–738 |
| 35 | 主课 | `presentation/sessions/35-regression-discontinuity.qmd` | Sharp/Fuzzy RDD、带宽、操纵与局部推断 | Ch.21，书内 739–751 |
| 36 | 主课 | `presentation/sessions/36-m-estimators-nls.qmd` | M 估计统一框架、极值一致性、NLS 推断 | Ch.22、Ch.23，书内 753–779 |
| 37 | 主课 | `presentation/sessions/37-quantile-discrete-choice.qmd` | 分位数回归、二元/多项选择、边际效应 | Ch.24、Ch.25、Ch.26，书内 780–841 |
| 38 | 主课 | `presentation/sessions/38-censoring-selection.qmd` | Tobit、删失/截断、样本选择与识别 | Ch.27，书内 842–858 |
| 39 | 主课 | `presentation/sessions/39-model-selection-machine-learning.qmd` | 风险、选择、收缩、模型平均、正则化、树/森林、DML | Ch.28、Ch.29，书内 859–944 |
| 40 | 工作坊 | `presentation/sessions/40-workshop-integration.qmd` | 从问题、识别、估计到推断的综合项目 | Ch.19–29；全年整合 |

工作坊编号为 07、12、17、20、25、29、33、40，合计 8 次；其余 32 次为主课。

## 3. 实施单元

### Unit 1: Quarto 项目与共享视觉基础

**Goal:** 建立能同时承载 RevealJS 课件和 HTML 补充文档的独立 Quarto 项目。

**Requirements trace:** R1, R5, R7, R8

**Dependencies:** 无。

**Files:**

- `presentation/_quarto.yml` — 默认项目、渲染目标、输出目录、语言和书目。
- `presentation/_quarto-instructor.yml` — 教师版 profile，启用备注打印策略。
- `presentation/sessions/_metadata.yml` — 40 次课共享 RevealJS 配置。
- `presentation/supplements/_metadata.yml` — 补充讲义共享 HTML 配置。
- `presentation/styles/course.scss` — 中文字体、公式、表格、步骤框与溢出规则。
- `presentation/references.bib` — Hansen 书稿和课程核心文献条目。

**Approach:** 使用 `default` project；显式列出 `index.qmd`、`syllabus.qmd`、`sessions/*.qmd` 和 `supplements/*.qmd`。RevealJS 全局不启用 incremental，逐步推导局部启用；MathJax 负责公式；课件输出到 `_output/`。

**Patterns:** 继承现有 QMD 的 `lang: zh-CN` 与 MathJax 选择；遵循 Quarto directory metadata，避免逐文件复制 YAML。

**Test scenarios:**

- [ ] Happy path: 单独渲染一份 session 与一份 supplement，分别得到 RevealJS 和普通 HTML。
- [ ] Nil/empty input: 无本地教材数据、无 R 包时仍能完成默认非执行式渲染。
- [ ] Error path: 配置中引用不存在的主题或书目时构建明确失败。
- [ ] Edge case: 中文、长矩阵公式、脚注与讲者备注同时出现时不丢失内容。

**Verification:** `quarto render presentation` 能生成预期目录，课件按 `S` 打开中文备注，补充讲义可滚动阅读。

**Planning-time unknowns:** Quarto CLI 的本机版本为 **Deferred to Planning**；按当前官方语法实现，并在 Unit 10 安装便携版后确认。

### Unit 2: 课程主页、教学大纲与六份辅助讲义

**Goal:** 给学生和教师提供全年导航、先修桥梁、统一记号与复现指南。

**Requirements trace:** R1, R3, R4, R7

**Dependencies:** Unit 1。

**Files:**

- `presentation/index.qmd` — 课程定位、学习路径、版本/版权说明和入口。
- `presentation/syllabus.qmd` — 40 次课程表、32+8 标记、考核建议与覆盖矩阵。
- `presentation/supplements/01-matrix-algebra.qmd` — Appendix A 的逐步中文补充。
- `presentation/supplements/02-probability-conditioning.qmd` — 条件期望、LIE、方差分解与 Appendix B 工具。
- `presentation/supplements/03-asymptotic-toolkit.qmd` — 收敛、WLLN/CLT/CMT/Slutsky/delta method。
- `presentation/supplements/04-notation-map.qmd` — 本科教材与 Hansen 记号/术语映射。
- `presentation/supplements/05-r-data-reproducibility.qmd` — R、数据路径、执行与复现规范。
- `presentation/supplements/06-reading-exercise-guide.qmd` — 分层阅读、带星内容、现有习题解答导航。

**Approach:** 六份材料均为完整中文 Quarto 文档，使用定义—直觉—公式—维数/前提—例子—自检结构；syllabus 用表格将 31 个书稿单元（29 章 + A/B）逐项映射到课次。

**Patterns:** 复用 AGENTS.md 的“题意翻译—已知与目标—路线图—逐步推导—结论回扣”；不复制教材长段文字。

**Test scenarios:**

- [ ] Happy path: 学生从 index 能进入 syllabus、任一 session 和任一 supplement。
- [ ] Nil/empty input: 尚未填写具体校历日期和评分权重时，syllabus 使用明确的“授课教师据校历填写”而非虚构日期。
- [ ] Error path: 覆盖矩阵遗漏任一章或附录时静态检查失败。
- [ ] Edge case: 同一章跨两次课时，覆盖表明确区分前半/后半且不重复宣称完整覆盖。

**Verification:** 31 个书稿单元全部在覆盖矩阵中出现；六份补充 QMD 均有实质内容和内部导航。

**Planning-time unknowns:** 正式评分权重为 **Deferred to Planning**；只提供可调整建议，不把未确认权重写成既定政策。

### Unit 3: 第 01–06 次基础主课

**Goal:** 以六次缓起步主课完成从本科计量到 Hansen 矩阵、概率、CEF 与 OLS 代数语言的过渡。

**Requirements trace:** R2, R3, R4, R5

**Dependencies:** Unit 1–2。

**Files:**

- `presentation/sessions/01-course-orientation.qmd` — Ch.1 与全年学习方法。
- `presentation/sessions/02-matrix-algebra-i.qmd` — Appendix A 基础。
- `presentation/sessions/03-matrix-algebra-ii.qmd` — 投影与矩阵微分。
- `presentation/sessions/04-probability-conditioning.qmd` — 概率和 Appendix B 桥梁。
- `presentation/sessions/05-cef-and-projection.qmd` — Ch.2 主线。
- `presentation/sessions/06-least-squares-algebra.qmd` — Ch.3 主线。

**Approach:** 每次约 24–32 页；按 10 分钟诊断、15 分钟本科桥接、45 分钟逐步推导、15 分钟例题/检查、5 分钟总结安排。每页只推进一个非显然台阶，教师备注说明板书补充、追问与常见卡点。

**Patterns:** 与 `docs/ch02/`、`docs/ch03/` 的记号一致；所有矩阵首次出现点明维数。

**Test scenarios:**

- [ ] Happy path: 只学过本科 OLS 的学生能从 CEF 走到 BLP，再从总体投影走到样本 OLS。
- [ ] Nil/empty input: 学生忘记矩阵秩或条件期望时，可通过先修检查链接到补充讲义。
- [ ] Error path: 推导使用未定义记号或跳过矩阵维数时检查清单标红。
- [ ] Edge case: CEF 非线性但 BLP 存在、投影正交但条件均值不为零等反例被明确讲解。

**Verification:** 六份课件均包含学习目标、桥接、逐步推导、常见错误、检查题、页码和 notes；前 6 次满足缓起步要求。

**Planning-time unknowns:** 无阻塞未知项。

### Unit 4: 第 07–12 次 OLS、稳健推断与渐近桥梁

**Goal:** 将最小二乘代数推进到有限样本理论、稳健/聚类推断和渐近工具。

**Requirements trace:** R2, R3, R5, R6

**Dependencies:** Unit 3。

**Files:**

- `presentation/sessions/07-workshop-matrix-ols.qmd` — 工作坊 1。
- `presentation/sessions/08-ols-finite-sample.qmd` — Ch.4 前半。
- `presentation/sessions/09-robust-and-clustered-se.qmd` — Ch.4 后半。
- `presentation/sessions/10-normal-regression-transition.qmd` — Ch.5–6 桥梁。
- `presentation/sessions/11-asymptotic-toolkit.qmd` — Ch.6 主线。
- `presentation/sessions/12-workshop-finite-vs-asymptotic.qmd` — 工作坊 2。

**Approach:** 先用 $P/M$ 解释有限样本结果，再用 Monte Carlo 暴露正态/同方差假设失效时普通标准误的问题，最后引出 WLLN/CLT 和夹心方差。工作坊代码可复制运行但默认不执行。

**Patterns:** 使用 `scripts/r_companions/_common.R` 中已有相对路径和稳健方差思想，但不硬 source 本地文件；工作坊写清样本生成过程与重复次数理由。

**Test scenarios:**

- [ ] Happy path: 学生能区分无偏性、一致性、精确分布和渐近分布。
- [ ] Nil/empty input: 没有 Hansen 数据时，工作坊仍可用自生成数据复现。
- [ ] Error path: 聚类层级选择错误时，课件给出为何错误及推断后果。
- [ ] Edge case: 小聚类数、异方差和非正态同时出现时，不错误承诺普通 $t$ 临界值。

**Verification:** 6 份课件完成；两份工作坊均含数据生成、设定、标准误、代码、数值解读和练习。

**Planning-time unknowns:** 无阻塞未知项。

### Unit 5: 第 13–20 次现代推断、多方程与 IV

**Goal:** 建立 OLS 渐近推断、约束/检验、重抽样、多方程和 IV 识别主线。

**Requirements trace:** R2, R3, R5, R6

**Dependencies:** Unit 4。

**Files:**

- `presentation/sessions/13-ols-asymptotics.qmd` — Ch.7。
- `presentation/sessions/14-restrictions-minimum-distance.qmd` — Ch.8。
- `presentation/sessions/15-hypothesis-testing.qmd` — Ch.9。
- `presentation/sessions/16-resampling-methods.qmd` — Ch.10。
- `presentation/sessions/17-workshop-testing-bootstrap.qmd` — 工作坊 3。
- `presentation/sessions/18-multivariate-regression.qmd` — Ch.11。
- `presentation/sessions/19-instrumental-variables-i.qmd` — Ch.12 前半。
- `presentation/sessions/20-workshop-iv-identification.qmd` — 工作坊 4。

**Approach:** 用统一估计量线性化语言连接 Wald、minimum distance、bootstrap、SUR 与 IV；IV 课先讲“矩条件 + 秩”而不是机械两阶段按钮，工作坊用弱第一阶段模拟揭示普通近似的失败。

**Patterns:** 沿用 Hansen 的 $hat\beta$、$Q$、$\Omega$、$Z$ 记号；用 `docs/ch07`–`docs/ch12` 作课后逐题链接。

**Test scenarios:**

- [ ] Happy path: 学生能从估计量渐近正态推导 Wald，并识别 2SLS 是样本矩条件解。
- [ ] Nil/empty input: 没有外部数据时，Bootstrap 和弱 IV 工作坊使用自生成数据。
- [ ] Error path: 无约束 bootstrap 用于零假设检验、仅凭第一阶段显著判断工具有效等错误被点名纠正。
- [ ] Edge case: 过度识别、弱工具和异质处理效应同时存在时，区分识别对象与推断方法。

**Verification:** 8 份课件完成，第一学期恰有 16 主课 + 4 工作坊。

**Planning-time unknowns:** 无阻塞未知项。

### Unit 6: 第 21–28 次 GMM、时间序列与非平稳性

**Goal:** 从 IV 推进到一般矩条件，并建立平稳、VAR、单位根与协整的依赖数据语言。

**Requirements trace:** R2, R3, R4, R5

**Dependencies:** Unit 5。

**Files:**

- `presentation/sessions/21-instrumental-variables-ii.qmd` — Ch.12 后半。
- `presentation/sessions/22-gmm.qmd` — Ch.13。
- `presentation/sessions/23-time-series-foundations.qmd` — Ch.14 前半。
- `presentation/sessions/24-time-series-regression-hac.qmd` — Ch.14 后半。
- `presentation/sessions/25-workshop-time-series.qmd` — 工作坊 5。
- `presentation/sessions/26-var-svar.qmd` — Ch.15。
- `presentation/sessions/27-unit-roots.qmd` — Ch.16 前半。
- `presentation/sessions/28-cointegration.qmd` — Ch.16 后半。

**Approach:** 先用 IV 的矩条件进入 GMM，再明确 i.i.d. 假设为何在时间序列中失效；按“定义—可用定理前提—代入—极限—经济解释”讲 MDS/CLT/FCLT。单位根课明确普通 $t$ 临界值失效的逻辑链。

**Patterns:** 使用 Hansen Ch.12–16 的记号；用短的本科桥接区分“自相关修正”和“建模动态结构”。

**Test scenarios:**

- [ ] Happy path: 学生能由矩条件写出两步 GMM，并从平稳 AR 推进到单位根非标准极限。
- [ ] Nil/empty input: 不熟悉 MDS/FCLT 时可链接渐近补充讲义中的先修回顾。
- [ ] Error path: 把不拒绝单位根说成证明单位根、把 Cholesky 排序当作经济识别时被明确纠正。
- [ ] Edge case: 序列近单位根、HAC 带宽敏感和弱识别并存时，不给出过强结论。

**Verification:** 8 份课件完成；每个高级概率工具首次使用前均复述前提和用途。

**Planning-time unknowns:** 无阻塞未知项。

### Unit 7: 第 29–34 次时间序列工作坊、面板、DiD 与非参数入口

**Goal:** 完成非平稳实证，系统讲授静态/动态面板和 DiD，并进入非参数估计。

**Requirements trace:** R2, R3, R5, R6

**Dependencies:** Unit 6。

**Files:**

- `presentation/sessions/29-workshop-var-unit-root.qmd` — 工作坊 6。
- `presentation/sessions/30-panel-fe-re.qmd` — Ch.17 前半。
- `presentation/sessions/31-dynamic-panel-gmm.qmd` — Ch.17 后半。
- `presentation/sessions/32-difference-in-differences.qmd` — Ch.18。
- `presentation/sessions/33-workshop-panel-did.qmd` — 工作坊 7。
- `presentation/sessions/34-nonparametric-and-series.qmd` — Ch.19–20。

**Approach:** 工作坊写清趋势/常数/滞后选择和 DF 临界值；面板课点明 $N\times T$ 与工具矩阵维数；DiD 从潜在结果和反事实趋势解释回归式；非参数课用偏差—方差进入核、局部多项式和级数。

**Patterns:** 链接现有 `docs/ch16`–`docs/ch20` 的详细习题和 R companion；聚类标准误始终与处理分配层级对应。

**Test scenarios:**

- [ ] Happy path: 学生能解释 within 变换、AB 矩条件、平行趋势和带宽权衡。
- [ ] Nil/empty input: 缺少 FRED/AB/DiD 数据时课件仍渲染，并给出可选本地路径。
- [ ] Error path: Hausman 检验机械选模型、工具膨胀、TWFE 异质处理错误和未聚类标准误被纠正。
- [ ] Edge case: 非平衡面板、错位处理时间和边界点核回归分别有提示。

**Verification:** 6 份课件完成；两份工作坊符合 R6，Ch.17–20 均被覆盖。

**Planning-time unknowns:** 无阻塞未知项。

### Unit 8: 第 35–40 次识别设计、非线性与现代方法

**Goal:** 完成 RDD、M/NLS、分位数与离散选择、选择模型、模型选择和机器学习，并用综合工作坊收束全年。

**Requirements trace:** R2, R3, R5, R6

**Dependencies:** Unit 7。

**Files:**

- `presentation/sessions/35-regression-discontinuity.qmd` — Ch.21。
- `presentation/sessions/36-m-estimators-nls.qmd` — Ch.22–23。
- `presentation/sessions/37-quantile-discrete-choice.qmd` — Ch.24–26。
- `presentation/sessions/38-censoring-selection.qmd` — Ch.27。
- `presentation/sessions/39-model-selection-machine-learning.qmd` — Ch.28–29。
- `presentation/sessions/40-workshop-integration.qmd` — 工作坊 8 与全年整合。

**Approach:** 对合并短章采用“统一估计目标—识别假设—样本准则—推断—常见错误”框架；Ch.28–29 强调预测风险和因果参数的区别；最终工作坊要求学生从研究问题到识别、估计、标准误和稳健性完成闭环。

**Patterns:** 使用 Hansen Ch.21–29 的原记号；对现有习题解答只做链接，不把长解答塞进课件。

**Test scenarios:**

- [ ] Happy path: 学生能区分局部 RDD、条件分位数、选择模型和预测算法各自目标。
- [ ] Nil/empty input: 没有外部数据时综合工作坊提供可运行模拟或数据字典模板。
- [ ] Error path: 用全局高阶多项式做 RDD、把 Probit 系数当概率效应、把 CV 最优预测模型当因果识别被纠正。
- [ ] Edge case: 完全预测、严重删失、选择后推断和高维弱信号有明确限制说明。

**Verification:** 6 份课件完成；Ch.21–29 全部映射；第二学期恰有 16 主课 + 4 工作坊。

**Planning-time unknowns:** 无阻塞未知项。

### Unit 9: 静态质量检查与构建入口

**Goal:** 用自动检查保证 40 次课、结构字段、内部链接和工作坊要求不随维护漂移。

**Requirements trace:** R1, R3, R5, R6, R8

**Dependencies:** Unit 1–8。

**Files:**

- `presentation/scripts/check_course.py` — 检查课次数、文件名、32+8、必备章节、notes、阅读页码、链接和过长页风险。
- `presentation/scripts/render.sh` — 运行静态检查和 Quarto 项目渲染，错误时非零退出。
- `presentation/README.md` — 中文构建、预览、讲者视图、PDF 导出和数据说明。

**Approach:** 检查脚本只用 Python 标准库；通过文件命名和显式 YAML `session-type` 判定主课/工作坊；对每份课件检查固定标题、`.notes`、Hansen 页码和相对链接。渲染脚本先检查再渲染。

**Patterns:** 沿用仓库 Python 脚本的 `Path` 和明确根目录模式；shell 脚本使用 `set -eu`，不假定用户当前目录。

**Test scenarios:**

- [ ] Happy path: 40 份完整课件时脚本输出分项通过并返回 0。
- [ ] Nil/empty input: `sessions/` 为空或缺课次时列出缺失编号并返回非零。
- [ ] Error path: 缺 notes、错误内部链接或 8 个工作坊数量不符时给出文件级错误。
- [ ] Edge case: 代码块内出现 `##` 或链接样式文本时不误判为幻灯片或真实链接。

**Verification:** 对完整项目运行静态检查为 0；人工制造三类错误分别能被捕获。

**Planning-time unknowns:** Quarto 不在 PATH 时 render 脚本的行为为 **Deferred to Planning**；应给出明确安装提示，静态检查仍可独立运行。

### Unit 10: 仓库集成与最终验证

**Goal:** 把课程入口接入仓库，隔离构建产物，并完成静态与真实渲染验收。

**Requirements trace:** R8

**Dependencies:** Unit 9。

**Files:**

- `.gitignore` — 忽略 `presentation/_output/`、`presentation/.quarto/` 等构建产物。
- `README.md` — 增加全年课程入口、40 次结构、渲染命令并纠正过时 Quarto 描述。

**Approach:** 保留现有 README 习题解答信息，只新增课程章节并修正“仅 r-toolset 分支”的陈旧表述。若系统无 Quarto，在临时目录下载官方 CLI 进行渲染，不把二进制提交到仓库。

**Patterns:** 工作树中已有内容属于用户；只做局部补丁，不重排无关 README 段落。

**Test scenarios:**

- [ ] Happy path: 从仓库根目录按 README 命令完成检查和渲染。
- [ ] Nil/empty input: 没有 `hansen/` 时项目仍可渲染，README 清楚说明如何选择性复现实证。
- [ ] Error path: 任一 QMD 解析失败时记录准确文件，修复后重新全量验证。
- [ ] Edge case: 渲染后 `git status --short` 不出现 `_output/` 或 `.quarto/`。

**Verification:** 静态检查通过；40 次课与 6 份补充材料全部真实渲染；`git diff --check` 通过；工作树只含预期源文件变更。

**Planning-time unknowns:** 便携 Quarto 下载是否受网络限制为 **Deferred to Planning**；若下载失败，保留静态检查证据并明确未完成的渲染验证，不伪称成功。

## 4. 质量门槛检查

- [x] 每个实施单元均有 R1–R8 的需求追踪。
- [x] 依赖关系为 Unit 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10，无循环。
- [x] 每个单元至少有 4 个测试场景，覆盖正常、空输入、错误与边界情况。
- [x] 每个单元触及不超过 8 个文件。
- [x] 每个单元引入的新抽象不超过 2 个；共享元数据与共享检查器均集中定义。
- [x] 所有规划期未知项均分类为 Deferred to Planning，无 Resolve Before Planning 阻塞项。
- [x] 实施者无需发明课程行为：课次、类型、章节、文件、固定结构、语言、代码策略和验收方式均已给定。
