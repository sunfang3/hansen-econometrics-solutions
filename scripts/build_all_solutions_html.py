#!/usr/bin/env python3
"""Merge all chapter exercise solution Markdown files into one HTML with MathJax."""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
HEADER = ROOT / "scripts" / "html_header_mathjax.html"
OUT_HTML = DOCS / "Hansen_Econometrics_Exercises_Solutions.html"
TMP_MD = ROOT / "scripts" / "_combined_solutions.md"

# Ordered chapter list (skip missing)
CHAPTERS = [
    2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
    20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
]

CHAPTER_TITLES = {
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


def find_solution_md(ch: int) -> Path | None:
    d = DOCS / f"ch{ch:02d}"
    if not d.is_dir():
        return None
    # prefer standard name
    candidates = sorted(d.glob("Hansen_Ch*_Exercises_Solutions.md"))
    if not candidates:
        candidates = sorted(d.glob("*.md"))
    return candidates[0] if candidates else None


def demote_headings(text: str, by: int = 1) -> str:
    """Demote ATX headings by `by` levels so chapters sit under book title."""

    def repl(m: re.Match) -> str:
        hashes = m.group(1)
        rest = m.group(2)
        # only demote ATX headings at line start (already matched)
        new_level = min(len(hashes) + by, 6)
        return "#" * new_level + rest

    # Avoid fenced code blocks
    parts = re.split(r"(```.*?```)", text, flags=re.S)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # fenced code
            out.append(part)
        else:
            out.append(re.sub(r"^(#{1,5})(\s+.*)$", repl, part, flags=re.M))
    return "".join(out)


def strip_duplicate_top_h1(text: str) -> str:
    """Remove first H1 if present; we inject a uniform chapter H1."""
    return re.sub(r"^#\s+[^\n]+\n+", "", text.lstrip(), count=1)


def main() -> int:
    if not HEADER.is_file():
        print(f"Missing header: {HEADER}", file=sys.stderr)
        return 1

    chunks: list[str] = []
    today = date.today().isoformat()
    chunks.append(
        f"""---
title: "Bruce Hansen《Econometrics》习题解答合集"
subtitle: "Conditional Expectation → Machine Learning（各章 Exercises 逐步解答）"
author: "按 Hansen 计量经济学体系整理"
date: "{today}"
lang: zh-CN
---

本文件将仓库 `docs/chXX/` 中各章 Markdown 解答合并为一份可离线浏览的 HTML，
并启用 **MathJax 3** 渲染行内/独立数学公式（`$...$`、`$$...$$`、`\\\\(...\\\\)`、`\\\\[...\\\\]`）。

> 源文件仍以各章 `.md` / `.ipynb` 为准；本合集便于通读与检索。
"""
    )

    included = []
    missing = []
    for ch in CHAPTERS:
        path = find_solution_md(ch)
        if path is None:
            missing.append(ch)
            continue
        raw = path.read_text(encoding="utf-8")
        body = strip_duplicate_top_h1(raw)
        body = demote_headings(body, by=1)
        title = CHAPTER_TITLES.get(ch, path.stem)
        chunks.append("\n\n---\n\n")
        chunks.append(f"# 第 {ch} 章　{title}\n\n")
        chunks.append(f"<p class=\"chapter-source\"><small>来源：<code>{path.relative_to(ROOT)}</code></small></p>\n\n")
        chunks.append(body.rstrip() + "\n")
        included.append((ch, path))

    TMP_MD.write_text("".join(chunks), encoding="utf-8")
    print(f"Wrote combined markdown: {TMP_MD} ({TMP_MD.stat().st_size // 1024} KB)")
    print(f"Chapters included: {[c for c, _ in included]}")
    if missing:
        print(f"Chapters missing (skipped): {missing}")

    cmd = [
        "pandoc",
        str(TMP_MD),
        "-f",
        "markdown+tex_math_dollars+tex_math_single_backslash+pipe_tables+table_captions+yaml_metadata_block+fenced_code_attributes+link_attributes+strikeout+task_lists",
        "-t",
        "html5",
        "-s",
        "--toc",
        "--toc-depth=2",
        "--metadata",
        "toc-title=目录",
        # MathJax URL for pandoc's math spans; actual engine loaded via header
        "--mathjax",
        f"--include-in-header={HEADER}",
        "-V",
        "lang=zh-CN",
        "--standalone",
        "-o",
        str(OUT_HTML),
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

    # Ensure body has tex2jax_process class for MathJax
    html = OUT_HTML.read_text(encoding="utf-8")
    if 'class="tex2jax_process"' not in html and "<body" in html:
        html = re.sub(r"<body([^>]*)>", r'<body class="tex2jax_process"\1>', html, count=1)
        OUT_HTML.write_text(html, encoding="utf-8")

    size_mb = OUT_HTML.stat().st_size / (1024 * 1024)
    print(f"Wrote {OUT_HTML} ({size_mb:.2f} MB)")

    # cleanup temp md (keep for debug? remove to avoid clutter)
    TMP_MD.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
