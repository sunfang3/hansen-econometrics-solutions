# R / Quarto toolset（分支 `r-toolset`）

将各章 **Markdown 理论解答** 与 **notebook 代码** 融合为 Quarto（`.qmd`），代码侧以 **R** 为主。

## 文件布局

```
docs/chXX/Hansen_ChXX_Exercises_Solutions.qmd   # 融合后的章节
scripts/r_companions/_common.R                  # 读数据 / OLS-HC1 等共用函数
scripts/r_companions/chXX.R                     # 章节实证 R 实现（优先）
scripts/convert_chapters_to_qmd.py              # 从 md+ipynb 重新生成 qmd
```

## 生成 / 更新 QMD

```bash
python3 scripts/convert_chapters_to_qmd.py
```

## 运行代码

```r
# 在仓库根目录
source("scripts/r_companions/_common.R")
source("scripts/r_companions/ch25.R")   # 例：probit + CPS
```

或用 Quarto（需安装 `quarto` CLI 与 R 包 `knitr`）：

```bash
cd docs/ch25
# 将 qmd 中 execute.eval 改为 true 后：
quarto render Hansen_Ch25_Exercises_Solutions.qmd --to html
```

默认 `execute: eval: false`，避免无数据时批量渲染失败。

## 安装 R 包

```r
pkgs <- c("haven","readxl","data.table","sandwich","lmtest","AER",
          "quantreg","boot","ggplot2","knitr","rmarkdown")
install.packages(setdiff(pkgs, rownames(installed.packages())))
# 扩展：vars, urca (Ch14–16); plm (Ch17); np (Ch19); mlogit (Ch26)
```

## 章节 companion 覆盖

已提供较完整 R 实现的章节：`ch04`, `ch12`, `ch16`, `ch17`, `ch19`, `ch21`, `ch23`–`ch28`。  
其余章节 qmd 含理论全文 + notebook 结构/原 Python 注释草稿，可继续往 `scripts/r_companions/` 补译。
