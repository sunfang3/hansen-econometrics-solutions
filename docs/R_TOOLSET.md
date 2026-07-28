# R / Quarto toolset（分支 `r-toolset`）

将各章 **Markdown 理论解答** 与 **R 实证代码** 融合为 Quarto（`.qmd`）。

## 布局

```
docs/chXX/Hansen_ChXX_Exercises_Solutions.qmd   # 理论 + 内联 R
scripts/r_companions/_common.R                  # 数据路径 / OLS-HC1
scripts/r_companions/chXX.R                     # 各章 R 实现（全部 27 章）
scripts/convert_chapters_to_qmd.py              # 重新生成全部 qmd
docs/R_TOOLSET.md                               # 本说明
```

## 重新生成 QMD

在仓库根目录：

```bash
python3 scripts/convert_chapters_to_qmd.py
```

每章 qmd 包含：

1. YAML（knitr、MathJax、TOC、`execute: eval: false`）
2. **理论解答**全文（来自 `.md`）
3. **R companion 代码内联**（来自 `scripts/r_companions/chXX.R`）
4. 装包提示

## 运行 R 代码

```r
# 仓库根目录
source("scripts/r_companions/_common.R")
source("scripts/r_companions/ch02.R")   # 模拟 / 无需外部数据
source("scripts/r_companions/ch25.R")   # 需 haven + cps09mar 数据
```

或用 Quarto（需 `quarto` CLI + `knitr`）：

```bash
cd docs/ch02
# 将 qmd 顶部 execute.eval 改为 true 后：
quarto render Hansen_Ch02_Exercises_Solutions.qmd --to html
```

## 安装 R 包

```r
# 建议使用用户库
dir.create(Sys.getenv("R_LIBS_USER"), recursive = TRUE, showWarnings = FALSE)
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))

pkgs <- c(
  "haven", "readxl", "data.table", "sandwich", "lmtest", "AER",
  "quantreg", "boot", "ggplot2", "knitr", "rmarkdown"
)
install.packages(setdiff(pkgs, rownames(installed.packages())),
                 repos = "https://cloud.r-project.org")

# 扩展
# install.packages(c("vars","urca","plm","np","mlogit","glmnet"))
```

## 章节 companion 一览

| 类型 | 章节 | 说明 |
|------|------|------|
| 模拟 / 基础 | 02,03,05,07–11,13–15,18,20,22,29 | 纯 base R，无需外部数据即可跑 |
| 实证 / 数据 | 04,12,16,17,19,21,23–28 | 读 Hansen 数据或专用算法（probit/Tobit/RDD/模型选择等） |

数据目录：`hansen/econometrics/data/`（gitignore，需自行下载）。

## 从 Python notebook 继续精译

复杂 notebook（如 Ch.17 AB/BB GMM、Ch.26 nested/mixed logit）companion 为工具骨架或核心复现；可对照 `docs/chXX/*.ipynb` 继续补全 `scripts/r_companions/chXX.R`，再运行转换脚本刷新 qmd。
