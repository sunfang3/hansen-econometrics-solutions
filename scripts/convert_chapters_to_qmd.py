#!/usr/bin/env python3
"""
Fuse each chapter's Markdown solutions + R companion (+ notebook narrative)
into a single Quarto .qmd with knitr / MathJax.

Every chapter gets:
  1. YAML (R/knitr, MathJax, toc)
  2. Full theory from Hansen_ChXX_Exercises_Solutions.md
  3. Inlined R code from scripts/r_companions/chXX.R (or auto draft)
  4. Optional notebook markdown section headers
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

        - **理论：** 同目录 Markdown 逐步解答全文嵌入。
        - **代码：** R 实现（`scripts/r_companions/ch{ch:02d}.R`）**内联**于下文；数据在 `hansen/econometrics/data/`。
        - 默认 `execute: eval: false`。有数据/包时改为 `true`，或在 R 中 `source()` companion。
        - 装包示例：`install.packages(c("haven","readxl","sandwich","AER","quantreg","boot","knitr"))`
        :::

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


def load_companion_r(ch: int) -> str:
    p = R_COMP / f"ch{ch:02d}.R"
    if not p.is_file():
        return (
            f"# (no companion scripts/r_companions/ch{ch:02d}.R yet)\n"
            f"message('Chapter {ch}: theory-only or pending R port')\n"
        )
    text = p.read_text(encoding="utf-8")
    # Drop recursive source of _common — qmd setup sources it once
    text = re.sub(
        r"^## bootstrap\nlocal\(\{[\s\S]*?\}\)\n*",
        "# helpers: see setup chunk (source _common.R)\n",
        text,
        count=1,
    )
    text = re.sub(
        r"^source\(file\.path\([^\n]+_common\.R[^\n]+\)\s*\n",
        "# helpers: see setup chunk\n",
        text,
        count=1,
        flags=re.M,
    )
    return text.rstrip() + "\n"


def notebook_md_excerpt(nb_path: Path, max_cells: int = 8) -> str:
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    parts: list[str] = []
    n = 0
    for cell in nb.get("cells", []):
        if cell.get("cell_type") != "markdown":
            continue
        src = "".join(cell.get("source", [])).strip()
        if not src or len(src) > 1500:
            continue
        if re.search(r"理论.*见同目录|Hansen_Ch\d+_Exercises_Solutions\.md", src):
            continue
        if src.startswith("# Hansen") and n == 0:
            continue
        parts.append(demote_headings(src, 1).rstrip())
        n += 1
        if n >= max_cells:
            break
    if not parts:
        return ""
    return "\n\n## Notebook 导读\n\n" + "\n\n".join(parts) + "\n"


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
        # 扩展：vars/urca (Ch14–16), plm (Ch17), np (Ch19), mlogit (Ch26)
        miss <- setdiff(pkgs, rownames(installed.packages()))
        if (length(miss)) {{
          install.packages(miss, repos = "https://cloud.r-project.org")
        }}
        ```

        ---

        *第 {ch} 章 · R/Quarto · 理论 Markdown + R companion 融合*  
        *重新生成：`python3 scripts/convert_chapters_to_qmd.py`*
        """
    )


def convert_one(ch: int) -> Path | None:
    md_path = find_md(ch)
    if not md_path:
        print(f"skip ch{ch:02d}: no md")
        return None

    title = TITLES.get(ch, "")
    theory = strip_first_h1(md_path.read_text(encoding="utf-8"))
    r_code = load_companion_r(ch)
    nb_path = find_ipynb(ch)

    body = yaml_header(ch, title)
    body += textwrap.dedent(
        f"""\
        ```{{r}}
        #| label: setup
        #| include: true
        root <- if (dir.exists("../../hansen")) {{
          "../.."
        }} else if (dir.exists("hansen")) {{
          "."
        }} else {{
          "../.."
        }}
        data_root <- file.path(root, "hansen", "econometrics", "data")
        companion_dir <- file.path(root, "scripts", "r_companions")
        if (file.exists(file.path(companion_dir, "_common.R"))) {{
          source(file.path(companion_dir, "_common.R"), local = FALSE)
        }}
        if (requireNamespace("knitr", quietly = TRUE)) {{
          knitr::opts_chunk$set(fig.width = 7, fig.height = 4.5)
        }}
        options(stringsAsFactors = FALSE)
        ```

        # 理论解答

        """
    )
    body += theory.rstrip() + "\n"
    body += "\n\n# 实证与数值代码（R）\n\n"
    body += f"以下代码来自 `scripts/r_companions/ch{ch:02d}.R`（与 Python notebook 对应）。\n\n"
    body += "```{r}\n#| label: companion\n"
    body += r_code
    if not r_code.endswith("\n"):
        body += "\n"
    body += "```\n"

    if nb_path:
        body += notebook_md_excerpt(nb_path)

    body += packages_footer(ch)

    out = DOCS / f"ch{ch:02d}" / f"Hansen_Ch{ch:02d}_Exercises_Solutions.qmd"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size // 1024} KB)")
    return out


def main() -> None:
    written = []
    for ch in CHAPTERS:
        p = convert_one(ch)
        if p:
            written.append(p)
    print(f"Done: {len(written)} qmd files")
    missing = [f"ch{ch:02d}" for ch in CHAPTERS if not (R_COMP / f"ch{ch:02d}.R").is_file()]
    if missing:
        print("Missing companions:", missing)
    else:
        print("All chapters have R companions.")


if __name__ == "__main__":
    main()
