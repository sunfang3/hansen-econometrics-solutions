# Hansen《Econometrics》详细中文学习笔记

`notes/` 是一套独立的中文 Quarto Book，面向已经学过本科计量、准备逐章通读 Hansen《Econometrics》的读者。现已覆盖 Chapter 1–29、Appendix A–B，并提供独立的[整书缩写与阅读记号](abbreviations.qmd)。阅读入口是 [index.qmd](index.qmd)。

## 构建与全书审计

本项目已用 Quarto 1.10.18 全量渲染。由仓库根目录运行：

~~~bash
quarto render notes
python3 notes/scripts/check_notes.py --scope all-current --rendered --global-audit
~~~

HTML 入口生成于 `notes/_output/index.html`。若只检查源文件，可省略 `--rendered`；若只检查某一阶段，可用 `--scope chapter-29`、`--scope appendices` 或 `--scope reading-aids`。

全局审计核对：

- Quarto 清单恰好包含首页、Ch.1–29、Appendix A–B 与缩写材料；
- 每章中文详细度、二级小节数、“本章路线”“本科桥接”“章末自检”达到门槛；
- 每个 Hansen 公式 `\tag{章.式}` 与 `hansen-eq-章-式` 稳定锚点一一对应、无重复且按原书顺序出现；
- 所有跨页 `.qmd` 链接、公式显示编号与目标锚点一致；
- 最终 33 个 HTML 页面及其本地页面链接、fragment id 全部存在；
- 缩写材料不占用正文编号，Ch.1–29 与 Appendix A–B 不因阅读工具而漂移。

## 编号约定

Hansen 原书编号公式写为：

~~~markdown
::: {#hansen-eq-12-29}
$$
\hat\beta_{\mathrm{2sls}}=(X'P_ZX)^{-1}X'P_ZY.
\tag{12.29}
$$
:::
~~~

正文用 `[式 (12.29)](#hansen-eq-12-29)` 引用。同一章为补齐代数步骤而增加的等式不加 `\tag`，以免伪造或挤占原书编号。

## 写作要求

- 每节说明原书位置、题意、已知条件、目标、路线、逐步推导和结论回扣；
- 不用无解释的“显然”“同理”“由定理即得”跨过关键步骤；
- 非显然记号首次出现时定义，关键矩阵说明维数；
- 将本科 OLS、IV、FE、单位根等语言连接到 Hansen 的投影、矩条件和渐近前提；
- 实证讨论说明样本、变换、滞后/趋势、cluster、检验参考分布及常见误读。
