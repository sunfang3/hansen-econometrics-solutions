#!/usr/bin/env python3
"""核对出版版章末习题与仓库解答的题号、页码和关键修订。

默认只检查 Markdown 源文件；加入 ``--include-generated`` 可同时检查 QMD，
加入 ``--check-pdf`` 可直接从本地出版版 PDF 再核对题号集合。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FULLBOOK = ROOT / "hansen" / "manuscripts" / "Econometrics_Fullbook.pdf"


@dataclass(frozen=True)
class Chapter:
    section: str
    print_pages: str
    pdf_pages: str
    pdf_start: int
    pdf_end: int
    last_exercise: int


CHAPTERS = {
    2: Chapter("2.34", "59–61", "94–96", 94, 96, 22),
    3: Chapter("3.26", "94–97", "129–132", 129, 132, 26),
    4: Chapter("4.25", "134–138", "169–173", 169, 173, 26),
    5: Chapter("5.15", "154–158", "189–193", 189, 193, 12),
    7: Chapter("7.22", "192–198", "227–233", 227, 233, 28),
    8: Chapter("8.17", "221–224", "256–259", 256, 259, 22),
    9: Chapter("9.25", "255–261", "290–296", 290, 296, 29),
    10: Chapter("10.32", "307–314", "342–349", 342, 349, 31),
    11: Chapter("11.18", "339–340", "374–375", 374, 375, 15),
    12: Chapter("12.43", "418–423", "453–458", 453, 458, 27),
    13: Chapter("13.29", "447–454", "482–489", 482, 489, 28),
    14: Chapter("14.48", "519–523", "554–558", 554, 558, 22),
    15: Chapter("15.32", "557–560", "592–595", 592, 595, 20),
    16: Chapter("16.23", "610–612", "645–647", 645, 647, 14),
    17: Chapter("17.45", "666–668", "701–703", 701, 703, 18),
    18: Chapter("18.10", "682–686", "717–721", 717, 721, 8),
    19: Chapter("19.27", "720–722", "755–757", 755, 757, 11),
    20: Chapter("20.32", "759–762", "794–797", 794, 797, 18),
    21: Chapter("21.12", "775–778", "810–813", 810, 813, 9),
    22: Chapter("22.10", "788–789", "823–824", 823, 824, 4),
    23: Chapter("23.11", "805–806", "840–841", 840, 841, 10),
    24: Chapter("24.17", "827–828", "862–863", 862, 863, 16),
    25: Chapter("25.15", "845–846", "880–881", 880, 881, 19),
    26: Chapter("26.14", "870–871", "905–906", 905, 906, 18),
    27: Chapter("27.13", "886–888", "921–923", 921, 923, 11),
    28: Chapter("28.33", "939–940", "974–975", 974, 975, 12),
    29: Chapter("29.24", "974", "1009", 1009, 1009, 10),
}


def solution_path(chapter: int, suffix: str) -> Path:
    return DOCS / f"ch{chapter:02d}" / f"Hansen_Ch{chapter:02d}_Exercises_Solutions.{suffix}"


def heading_exercises(text: str, chapter: int) -> set[int]:
    """把 ``Exercise 8.11–8.13`` 等组合标题展开成单题集合。"""
    labels: list[str] = []
    for line in text.splitlines():
        match = re.match(
            r"^#{1,6}\s+Exercises?\s+([0-9.\s/–—-]+)",
            line,
            flags=re.IGNORECASE,
        )
        if match:
            # 只读取紧跟在 Exercise 后的题号标签，避免把标题中的式 (4.29)
            # 或 “续 3.24” 错认成另一道习题。
            labels.append(match.group(1).strip())
    headings = "\n".join(labels)
    found: set[int] = set()
    range_pattern = re.compile(
        rf"(?<!\d){chapter}\.(\d+)\s*[–—-]\s*(?:{chapter}\.)?(\d+)"
    )
    for match in range_pattern.finditer(headings):
        start, end = map(int, match.groups())
        if start <= end:
            found.update(range(start, end + 1))
    for number in re.findall(rf"(?<!\d){chapter}\.(\d+)", headings):
        found.add(int(number))
    return found


def check_solution_file(chapter: int, meta: Chapter, suffix: str) -> list[str]:
    path = solution_path(chapter, suffix)
    if not path.is_file():
        return [f"缺少文件：{path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    required_header = (
        "Econometrics_Fullbook.pdf",
        f"PDF 第 {meta.pdf_pages} 页",
        f"印刷页 {meta.print_pages}",
        f"§{meta.section} Exercises",
        f"{chapter}.1–{chapter}.{meta.last_exercise} 全部",
    )
    for fragment in required_header:
        if fragment not in text:
            errors.append(f"{path.relative_to(ROOT)} 首页缺少：{fragment}")

    expected = set(range(1, meta.last_exercise + 1))
    actual = heading_exercises(text, chapter)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing:
        errors.append(f"{path.relative_to(ROOT)} 缺少题号：{missing}")
    if extra:
        errors.append(f"{path.relative_to(ROOT)} 多出出版版题号：{extra}")
    return errors


def extract_pdf_exercises(chapters: list[int]) -> tuple[dict[int, set[int]], list[str]]:
    if not FULLBOOK.is_file():
        return {}, [f"找不到出版版 PDF：{FULLBOOK.relative_to(ROOT)}"]
    try:
        from pypdf import PdfReader
    except ImportError:
        return {}, ["--check-pdf 需要 pypdf；请先运行：python3 -m pip install pypdf"]

    reader = PdfReader(str(FULLBOOK))
    found: dict[int, set[int]] = {}
    errors: list[str] = []
    for chapter in chapters:
        meta = CHAPTERS[chapter]
        page_text = "\n".join(
            reader.pages[index].extract_text() or ""
            for index in range(meta.pdf_start - 1, meta.pdf_end)
        )
        numbers = {
            int(number)
            for number in re.findall(rf"Exercise\s*{chapter}\.(\d+)", page_text)
        }
        expected = set(range(1, meta.last_exercise + 1))
        missing = sorted(expected - numbers)
        if missing:
            errors.append(
                f"出版版 PDF Ch.{chapter} 指定页未提取到题号：{missing}"
            )
        if chapter == 12 and 28 in numbers:
            errors.append("出版版 PDF 的 Ch.12 审计异常：不应存在 Exercise 12.28")
        found[chapter] = numbers
    return found, errors


def check_special_revisions(chapters: list[int]) -> list[str]:
    errors: list[str] = []
    if 4 in chapters:
        text = solution_path(4, "md").read_text(encoding="utf-8")
        required = (
            "(4.17)(4.18)", "Theorem 4.5", "(4.29)", "(4.37)",
            "(4.38)", "(4.60)", "(4.61)", "(4.62)", "§4.14", "§4.21",
        )
        for fragment in required:
            if fragment not in text:
                errors.append(f"Ch.4 缺少出版版关键引用：{fragment}")
        if "Theorem 4.6" in text:
            errors.append("Ch.4 仍出现旧稿引用 Theorem 4.6")
    if 12 in chapters:
        md = solution_path(12, "md").read_text(encoding="utf-8")
        if re.search(r"^#{1,6}\s+Exercise 12\.28\b", md, flags=re.MULTILINE):
            errors.append("Ch.12 Markdown 仍含已从出版版删除的 Exercise 12.28")
        notebook = solution_path(12, "ipynb")
        if not notebook.is_file():
            errors.append("Ch.12 缺少 notebook")
        else:
            nb = json.loads(notebook.read_text(encoding="utf-8"))
            notebook_text = "\n".join(
                "".join(cell.get("source", [])) if isinstance(cell.get("source"), list)
                else str(cell.get("source", ""))
                for cell in nb.get("cells", [])
            )
            for label in ("12.22 AJR", "12.24 Card", "12.26 AK"):
                if label not in notebook_text:
                    errors.append(f"Ch.12 notebook 缺少出版版标签：{label}")
            for old_label in ("12.23 AJR", "12.25 Card", "12.27 AK"):
                if old_label in notebook_text:
                    errors.append(f"Ch.12 notebook 仍含旧稿标签：{old_label}")
    if 21 in chapters:
        text = solution_path(21, "md").read_text(encoding="utf-8")
        for fragment in ("59.1984", "19.6", "9.8", "29.4"):
            if fragment not in text:
                errors.append(f"Ch.21 缺少出版版带宽/阈值说明：{fragment}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--chapters", nargs="+", type=int, choices=sorted(CHAPTERS),
        help="只检查指定章节；默认检查全部有章末习题的章节",
    )
    parser.add_argument(
        "--include-generated", action="store_true", help="同时检查生成的 .qmd",
    )
    parser.add_argument(
        "--check-pdf", action="store_true", help="直接提取出版版 PDF 指定页核对题号",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    chapters = args.chapters or sorted(CHAPTERS)
    errors: list[str] = []
    for chapter in chapters:
        errors.extend(check_solution_file(chapter, CHAPTERS[chapter], "md"))
        if args.include_generated:
            errors.extend(check_solution_file(chapter, CHAPTERS[chapter], "qmd"))
    errors.extend(check_special_revisions(chapters))
    pdf_found: dict[int, set[int]] = {}
    if args.check_pdf:
        pdf_found, pdf_errors = extract_pdf_exercises(chapters)
        errors.extend(pdf_errors)

    if errors:
        print("出版版习题覆盖检查失败：", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    source = "；并已直接核对 PDF" if args.check_pdf else ""
    generated = "、QMD" if args.include_generated else ""
    pdf_count = sum(len(pdf_found.get(chapter, set())) for chapter in chapters)
    suffix = f"（PDF 提取到 {pdf_count} 个题号标签）" if args.check_pdf else ""
    print(
        f"通过：{len(chapters)} 章 Markdown{generated} 的出版版首页与题号连续覆盖无误"
        f"{source}{suffix}。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
