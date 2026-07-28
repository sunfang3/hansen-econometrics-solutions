#!/usr/bin/env python3
"""
Fuse each chapter's Markdown solutions + notebook into Quarto (.qmd) with R.

Priority for code:
1. scripts/r_companions/chXX.R if present (hand-translated R)
2. Else: notebook markdown + R chunks with original Python preserved as comments
   and a structural R draft (execute: false by default)
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
R_COMP = ROOT / "scripts" / "r_companions"

CHAPTERS = [
    2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
]

TITLES = {
    2: "Conditional Expectation and Projection",
    3: "The Algebra of Least Squares",
    4: "Least Squares Regression",
    5: "Normal Regression",
    7: "Asymptotic Theory for Least Squares",
    8: "Restricted Estimation",
    9: "Hypothesis Testing",
    10: "Resampling Methods",
    11: "Multivariate Regression",
    12: "Instrumental Variables",
    13: "Generalized Method of Moments",
    14: "Time Series",
    15: "Multivariate Time Series",
    16: "Non-Stationary Time Series",
    17: "Panel Data",
    18: "Difference in Differences",
    19: "Nonparametric Regression",
    20: "Series Regression",
    21: "Regression Discontinuity",
    22: "M-Estimators",
    23: "Nonlinear Least Squares",
    24: "Quantile Regression",
    25: "Binary Choice",
    26: "Multiple Choice",
    27: "Censoring and Selection",
    28: "Model Selection, Stein Shrinkage, and Model Averaging",
    29: "Machine Learning",
}


def yaml_header(ch: int, title: str) -> str:
    return textwrap.dedent(
        f"""\
        ---
        title: "Bruce Hansen《Econometrics》第 {ch} 章习题解答"
        subtitle: "Chapter {ch} {title}"
        author: "按 Hansen 计量经济学体系整理（R / Quarto 版）"
        date: today
        lang: zh-CN
        format:
          html:
            toc: true
            toc-depth: 3
            toc-location: left
            number-sections: true
            number-depth: 2
            html-math-method: mathjax
            theme: cosmo
            code-fold: true
            code-tools: true
        engine: knitr
        knitr:
          opts_chunk:
            comment: "#>"
            fig.path: "figures/ch{ch:02d}/"
        execute:
          eval: false
          echo: true
          warning: false
          message: false
        ---

        ::: {{.callout-note}}
        ## 说明

        - **理论：** 来自同目录 Markdown 逐步解答。
        - **代码：** Python notebook 已融合为 **R**（`scripts/r_companions/ch{ch:02d}.R` 优先；否则为带注释的翻译草稿）。
        - **数据：** `hansen/econometrics/data/`（gitignore）；渲染前请确保数据已下载。
        - 默认 `execute: eval: false`。有数据时改为 `true` 或交互运行代码块。
        - 缺包时：`install.packages(c("haven","readxl","sandwich","AER","quantreg","boot"))` 等。
        :::

        ```{{r}}
        #| label: setup
        root <- if (dir.exists("../../hansen")) "../.." else if (dir.exists("hansen")) "." else "../.."
        data_root <- file.path(root, "hansen", "econometrics", "data")
        companion_dir <- file.path(root, "scripts", "r_companions")
        if (file.exists(file.path(companion_dir, "_common.R"))) {{
          source(file.path(companion_dir, "_common.R"), local = FALSE)
        }}
        knitr::opts_chunk$set(fig.width = 7, fig.height = 4.5)
        options(stringsAsFactors = FALSE)
        ```

        """
    )


def find_md(ch: int) -> Path | None:
    d = DOCS / f"ch{ch:02d}"
    cands = sorted(d.glob("Hansen_Ch*_Exercises_Solutions.md"))
    return cands[0] if cands else None


def find_ipynb(ch: int) -> Path | None:
    d = DOCS / f"ch{ch:02d}"
    cands = sorted(d.glob("Hansen_Ch*_Exercises_Solutions.ipynb"))
    return cands[0] if cands else None


def strip_first_h1(text: str) -> str:
    return re.sub(r"^#\s+[^\n]+\n+", "", text.lstrip(), count=1)


def demote_headings(text: str, by: int = 1) -> str:
    def repl(m: re.Match) -> str:
        return "#" * min(len(m.group(1)) + by, 6) + m.group(2)

    parts = re.split(r"(```.*?```)", text, flags=re.S)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append(part)
        else:
            out.append(re.sub(r"^(#{1,5})(\s+.*)$", repl, part, flags=re.M))
    return "".join(out)


def py_as_r_comment_block(src: str) -> str:
    """Keep original Python as comments + light R idioms for readability."""
    lines = [
        "# 原 Python notebook 代码（保留备查）→ R 对照草稿",
        "# 完整可运行版本请优先使用 companion：scripts/r_companions/chXX.R",
        "",
    ]
    for line in src.splitlines():
        if re.match(r"^\s*(import|from)\s+", line):
            lines.append(f"# {line}")
            continue
        # light substitutions for readability
        t = line
        t = t.replace("True", "TRUE").replace("False", "FALSE").replace("None", "NULL")
        t = t.replace("np.", "").replace("pd.", "")
        if line.strip().startswith("#"):
            lines.append(t)
        else:
            lines.append("# PY: " + line if line.strip() else "")
    lines.append("")
    lines.append("# --- R 惯用写法提示 ---")
    lines.append("# read_dta: haven::read_dta(file.path(data_root, ...))")
    lines.append("# OLS:     qr.solve(X, y) 或 lm.fit(X, y)$coefficients")
    lines.append("# HC1 SE:  sandwich::vcovHC(lm_obj, type='HC1')")
    lines.append("# 矩阵:    crossprod(X), solve(crossprod(X), crossprod(X, y))")
    return "\n".join(lines)


def notebook_sections(nb_path: Path) -> str:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    parts = [
        "\n\n# 实证与数值代码（来自 notebook，R 版）\n\n",
    ]
    code_i = 0
    for cell in nb.get("cells", []):
        src = "".join(cell.get("source", []))
        if not src.strip():
            continue
        if cell.get("cell_type") == "markdown":
            # skip redundant title pointing only to md
            if re.search(r"理论.*见同目录", src) and len(src) < 800:
                continue
            parts.append(demote_headings(src, 1).rstrip() + "\n\n")
        elif cell.get("cell_type") == "code":
            code_i += 1
            r_body = py_as_r_comment_block(src)
            parts.append(
                f"```{{r}}\n#| label: nb-cell-{code_i:02d}\n{r_body}\n```\n\n"
            )
    return "".join(parts)


def packages_footer(ch: int) -> str:
    return textwrap.dedent(
        f"""\

        # 依赖包

        ```{{r}}
        #| label: install-pkgs
        #| eval: false
        pkgs <- c(
          "haven", "readxl", "data.table", "sandwich", "lmtest", "AER",
          "quantreg", "boot", "MASS", "Matrix", "nnet", "ggplot2", "knitr"
        )
        # 章节扩展：Ch14–16 vars/urca；Ch17 plm；Ch19 np；Ch26 mlogit
        miss <- setdiff(pkgs, rownames(installed.packages()))
        if (length(miss)) install.packages(miss, repos = "https://cloud.r-project.org")
        ```

        ---
        *第 {ch} 章 · R/Quarto · md + ipynb 融合*
        """
    )


def convert_one(ch: int) -> Path | None:
    md_path = find_md(ch)
    if not md_path:
        print(f"skip ch{ch:02d}: no md")
        return None

    title = TITLES.get(ch, "")
    theory = strip_first_h1(md_path.read_text(encoding="utf-8"))

    body = yaml_header(ch, title)
    body += "# 理论解答\n\n"
    body += theory.rstrip() + "\n"

    companion = R_COMP / f"ch{ch:02d}.R"
    nb_path = find_ipynb(ch)

    if companion.is_file():
        rel = companion.relative_to(ROOT).as_posix()
        body += "\n\n# 实证与数值代码（R companion）\n\n"
        body += f"手写/精译 R 脚本：`{rel}`。\n\n"
        body += "```{r}\n#| label: companion-main\n"
        body += f'source(file.path(root, "scripts", "r_companions", "ch{ch:02d}.R"))\n'
        body += "```\n"
        # Also include notebook markdown narrative if useful
        if nb_path:
            nb = json.loads(nb_path.read_text(encoding="utf-8"))
            md_cells = [
                "".join(c.get("source", []))
                for c in nb.get("cells", [])
                if c.get("cell_type") == "markdown"
            ]
            if len(md_cells) > 1:
                body += "\n\n## Notebook 结构说明\n\n"
                for m in md_cells[1:6]:  # a few section intros
                    if len(m) < 1200:
                        body += demote_headings(m, 2).rstrip() + "\n\n"
    elif nb_path:
        body += notebook_sections(nb_path)
    else:
        body += "\n\n::: {.callout-tip}\n本章以理论为主；无独立 notebook 或 companion。\n:::\n"

    body += packages_footer(ch)

    out = DOCS / f"ch{ch:02d}" / f"Hansen_Ch{ch:02d}_Exercises_Solutions.qmd"
    # For ch29, existing qmd is python-oriented; overwrite with R-style fusion
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)"
          f"  companion={'yes' if companion.is_file() else 'no'}"
          f"  nb={'yes' if nb_path else 'no'}")
    return out


def main() -> None:
    R_COMP.mkdir(parents=True, exist_ok=True)
    written = [convert_one(ch) for ch in CHAPTERS]
    written = [p for p in written if p]
    print(f"Done: {len(written)} qmd files on branch toolset")


if __name__ == "__main__":
    main()
