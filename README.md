# Hansen Econometrics Solutions

Bruce E. Hansen《Econometrics》习题解答（按 Hansen 体系完整解题）。题号、页码和交叉引用以 Princeton University Press 2022 年出版版 `hansen/manuscripts/Econometrics_Fullbook.pdf` 为准。

## 章节进度

| 章节 | 内容与出版版题号 | 出版版 PDF 页 | 格式 |
|------|------------------|--------------|------|
| Ch.2 | Conditional Expectation and Projection（2.1–2.22） | 94–96 | `.md` / `.qmd` / `.ipynb` |
| Ch.3 | The Algebra of Least Squares（3.1–3.26） | 129–132 | `.md` / `.qmd` / `.ipynb` |
| Ch.4 | Least Squares Regression（4.1–4.26） | 169–173 | `.md` / `.qmd` / `.ipynb` |
| Ch.5 | Normal Regression（5.1–5.12） | 189–193 | `.md` / `.qmd` / `.ipynb` |
| Ch.7 | Asymptotic Theory for Least Squares（7.1–7.28） | 227–233 | `.md` / `.qmd` / `.ipynb` |
| Ch.8 | Restricted Estimation（8.1–8.22） | 256–259 | `.md` / `.qmd` / `.ipynb` |
| Ch.9 | Hypothesis Testing（9.1–9.29） | 290–296 | `.md` / `.qmd` / `.ipynb` |
| Ch.10 | Resampling Methods（10.1–10.31） | 342–349 | `.md` / `.qmd` / `.ipynb` |
| Ch.11 | Multivariate Regression（11.1–11.15） | 374–375 | `.md` / `.qmd` / `.ipynb` |
| Ch.12 | Instrumental Variables（12.1–12.27） | 453–458 | `.md` / `.qmd` / `.ipynb` |
| Ch.13 | Generalized Method of Moments（13.1–13.28） | 482–489 | `.md` / `.qmd` / `.ipynb` |
| Ch.14 | Time Series（14.1–14.22） | 554–558 | `.md` / `.qmd` / `.ipynb` |
| Ch.15 | Multivariate Time Series（15.1–15.20） | 592–595 | `.md` / `.qmd` / `.ipynb` |
| Ch.16 | Non-Stationary Time Series（16.1–16.14） | 645–647 | `.md` / `.qmd` / `.ipynb` |
| Ch.17 | Panel Data（17.1–17.18） | 701–703 | `.md` / `.qmd` / `.ipynb` |
| Ch.18 | Difference in Differences（18.1–18.8） | 717–721 | `.md` / `.qmd` / `.ipynb` |
| Ch.19 | Nonparametric Regression（19.1–19.11） | 755–757 | `.md` / `.qmd` / `.ipynb` |
| Ch.20 | Series Regression（20.1–20.18） | 794–797 | `.md` / `.qmd` / `.ipynb` |
| Ch.21 | Regression Discontinuity（21.1–21.9） | 810–813 | `.md` / `.qmd` / `.ipynb` |
| Ch.22 | M-Estimators（22.1–22.4） | 823–824 | `.md` / `.qmd` / `.ipynb` |
| Ch.23 | Nonlinear Least Squares（23.1–23.10） | 840–841 | `.md` / `.qmd` / `.ipynb` |
| Ch.24 | Quantile Regression（24.1–24.16） | 862–863 | `.md` / `.qmd` / `.ipynb` |
| Ch.25 | Binary Choice（25.1–25.19） | 880–881 | `.md` / `.qmd` / `.ipynb` |
| Ch.26 | Multiple Choice（26.1–26.18） | 905–906 | `.md` / `.qmd` / `.ipynb` |
| Ch.27 | Censoring and Selection（27.1–27.11） | 921–923 | `.md` / `.qmd` / `.ipynb` |
| Ch.28 | Model Selection, Stein Shrinkage, Model Averaging（28.1–28.12） | 974–975 | `.md` / `.qmd` / `.ipynb` |
| Ch.29 | Machine Learning（29.1–29.10） | 1009 | `.md` / `.qmd` |

解答位于 `docs/chXX/`。Chapter 1 与 Chapter 6 没有章末 Exercises；其余 27 章共 **486 道**出版版习题全部覆盖。逐章差异和页码映射见 [`docs/PUBLISHED_EXERCISES_AUDIT.md`](docs/PUBLISHED_EXERCISES_AUDIT.md)。

直接从本地出版版 PDF 核对题号，并检查 Markdown/QMD 连续覆盖：

```bash
python3 scripts/check_published_exercises.py --include-generated --check-pdf
```

## 全年中文 Quarto 课程

`presentation/` 提供一套从本科计量平缓过渡到 Hansen 全书的研究生课程：

- 40 次课，每次 90 分钟：32 次主课 + 8 次工作坊；
- 覆盖 Ch.1–29 与 Appendix A–B；
- 7 份中文补充讲义，包括矩阵、概率、渐近、记号、复现、练习导航和[全书缩写总表](presentation/supplements/07-abbreviations-glossary.qmd)；
- 每页课堂演示均有中文讲者备注，工作坊含固定种子的代码和数值结果。

课程入口为 [presentation/index.qmd](presentation/index.qmd)，全年安排见 [presentation/syllabus.qmd](presentation/syllabus.qmd)。一键检查并渲染：

~~~bash
presentation/scripts/render.sh
~~~

详细构建、讲者视图、PDF 和数据说明见 [presentation/README.md](presentation/README.md)。

## Hansen 全书详细中文学习笔记

`notes/` 提供沿 Hansen 原书顺序编排的 Quarto Book，面向从本科计量过渡到研究生计量的读者：

- 覆盖 Chapter 1–29 与 Appendix A–B；
- 逐节写明对象、条件、路线、矩阵维数、推导和常见误读；
- 保留 Hansen 原公式编号并提供稳定的跨页锚点；
- 附有[整书缩写与阅读记号](notes/abbreviations.qmd)，整理英文全称、中文释义和同形缩写辨析。

入口与构建说明见 [notes/index.qmd](notes/index.qmd) 和 [notes/README.md](notes/README.md)。完整检查命令：

~~~bash
quarto render notes
python3 notes/scripts/check_notes.py --scope all-current --rendered --global-audit
~~~

## 习题解答的 R / Quarto 版

各章 **Markdown 理论 + notebook 代码** 已融合为 Quarto：

- `docs/chXX/Hansen_ChXX_Exercises_Solutions.qmd`
- R 实证：`scripts/r_companions/`（见 `docs/R_TOOLSET.md`）
- 重新生成：`python3 scripts/convert_chapters_to_qmd.py`

## 合集 HTML

全部章节习题解答已合并为单一 HTML（含 **MathJax 3** 公式渲染）：

- [`docs/Hansen_Econometrics_Exercises_Solutions.html`](docs/Hansen_Econometrics_Exercises_Solutions.html)

重新生成：

```bash
python3 scripts/build_all_solutions_html.py
```


## 数据

教材数据请从 Hansen 官网下载：

- https://users.ssc.wisc.edu/~bhansen/econometrics/

常用子集：`cps09mar`、`Invest1993`、`Nerlove1963`、`MRW1992`、`DDK2011`、`AJR2001`、`Card1995`、`AK1991`、`FRED-QD`、`FRED-MD`、`Kilian2009`、`AB1991`、`CK1994`、`DS2004`、`BMN2016`、`RR2010`、`CHJ2004`、`AL1999`、`LM2007`、`PSS2017`、`Koppelman`。

Notebook 中数据路径指向本地 `hansen/econometrics/data/...`（该目录被 `.gitignore` 忽略，需自行下载）。

## 运行

```bash
jupyter notebook docs/ch09/Hansen_Ch09_Exercises_Solutions.ipynb
```

## 许可说明

习题来自 Hansen 公开讲义/教材；解答仅供学习参考。正式出版教材版权归 Princeton University Press / 作者所有。
