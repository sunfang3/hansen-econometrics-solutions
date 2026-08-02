#!/usr/bin/env python3
"""检查 Hansen 中文学习笔记的结构、详细度和原书公式锚点。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / "notes"
EXPECTED = {
    "ch01.qmd": (10, "1", 1200),
    "ch02.qmd": (34, "2", 5000),
    "ch03.qmd": (26, "3", 4500),
    "ch04.qmd": (27, "4", 4500),
    "ch05.qmd": (15, "5", 2800),
    "ch06.qmd": (10, "6", 2200),
    "ch07.qmd": (22, "7", 3800),
    "ch08.qmd": (17, "8", 3300),
    "appendix-a.qmd": (23, "A", 3500),
    "appendix-b.qmd": (5, "B", 2200),
}
SCOPES = {
    "appendices": {"appendix-a.qmd", "appendix-b.qmd"},
    "chapters-1-2": {"ch01.qmd", "ch02.qmd"},
    "chapters-3-4": {"ch03.qmd", "ch04.qmd"},
    "chapters-5-6": {"ch05.qmd", "ch06.qmd"},
    "chapters-7-8": {"ch07.qmd", "ch08.qmd"},
    "chapters": {name for name in EXPECTED if name.startswith("ch")},
    "foundation": {
        "appendix-a.qmd",
        "appendix-b.qmd",
        *(f"ch{i:02d}.qmd" for i in range(1, 7)),
    },
    "all-current": set(EXPECTED),
}
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD)\b|待补|占位|Lorem", re.I)
CHINESE = re.compile(r"[\u3400-\u9fff]")
TAG = re.compile(r"\\tag\{([1-9]\d*|[AB])\.(\d+)\}")
ANCHOR = re.compile(r"\{#hansen-eq-([1-9]\d*|[ab])-(\d+)\}")
FENCED_ANCHOR = re.compile(
    r"^::: \{#hansen-eq-([1-9]\d*|[ab])-(\d+)\}\s*$", re.M
)
REFERENCE = re.compile(r"\[式 \(([1-9]\d*|[AB])\.(\d+)\)\]\(([^)]+)\)")


def error(path: Path, code: str, message: str) -> str:
    return f"ERROR {code}: {path.relative_to(ROOT)}: {message}"


def check_file(path: Path, minimum_sections: int, prefix: str, minimum_chinese: int) -> list[str]:
    issues: list[str] = []
    if not path.exists():
        return [error(path, "MISSING_FILE", "章节文件不存在。")]
    text = path.read_text(encoding="utf-8")
    if PLACEHOLDER.search(text):
        issues.append(error(path, "PLACEHOLDER", "含未完成占位符。"))
    sections = re.findall(r"^##\s+", text, re.M)
    if len(sections) < minimum_sections:
        issues.append(error(path, "SECTION_COUNT", f"二级小节 {len(sections)}，至少应为 {minimum_sections}。"))
    chinese_count = len(CHINESE.findall(text))
    if chinese_count < minimum_chinese:
        issues.append(error(path, "DETAIL_LEVEL", f"中文字符约 {chinese_count}，低于详细笔记门槛 {minimum_chinese}。"))
    for required in ("本章路线", "本科桥接", "章末自检"):
        if required not in text:
            issues.append(error(path, "MISSING_BLOCK", f"缺少“{required}”。"))

    tags = TAG.findall(text)
    anchors = ANCHOR.findall(text)
    fenced_anchors = FENCED_ANCHOR.findall(text)
    if sorted(anchors) != sorted(fenced_anchors):
        issues.append(error(path, "ANCHOR_BLOCK", "公式锚点必须放在 fenced div 起始行，不能写在公式末尾。"))
    normalized_anchors = [(a.upper(), b) for a, b in anchors]
    if sorted(tags) != sorted(normalized_anchors):
        issues.append(error(path, "FORMULA_PAIR", "原书公式 tag 与稳定 anchor 不是一一对应。"))
    wrong_prefix = [f"{a}.{b}" for a, b in tags if a != prefix]
    if wrong_prefix:
        issues.append(error(path, "FORMULA_CHAPTER", f"公式前缀不属于本章：{wrong_prefix}。"))
    numbers = [int(b) for _, b in tags]
    if numbers != sorted(numbers):
        issues.append(error(path, "FORMULA_ORDER", "原书公式编号未按递增顺序出现。"))

    anchors_set = {f"#hansen-eq-{a.lower()}-{b}" for a, b in tags}
    for a, b, target in REFERENCE.findall(text):
        expected_target = f"#hansen-eq-{a.lower()}-{b}"
        if target.startswith("#") and target not in anchors_set:
            issues.append(error(path, "BROKEN_FORMULA_REF", f"式 ({a}.{b}) 的本章锚点不存在：{target}。"))
        if target.startswith("#") and target != expected_target:
            issues.append(error(path, "FORMULA_REF_MISMATCH", f"式 ({a}.{b}) 指向 {target}。"))
    return issues


def check_rendered_file(path: Path, prefix: str) -> list[str]:
    issues: list[str] = []
    output = NOTES / "_output" / f"{path.stem}.html"
    if not output.exists():
        return [error(path, "MISSING_RENDER", f"渲染产物不存在：{output.relative_to(ROOT)}。")]
    source = path.read_text(encoding="utf-8")
    html = output.read_text(encoding="utf-8")
    for chapter, number in ANCHOR.findall(source):
        anchor_id = f"hansen-eq-{chapter.lower()}-{number}"
        if f'id="{anchor_id}"' not in html:
            issues.append(error(path, "MISSING_RENDERED_ANCHOR", f"HTML 中没有公式锚点 {anchor_id}。"))
    if f'data-number="{prefix}.1"' not in html:
        issues.append(error(path, "CHAPTER_NUMBER", f"渲染后首节没有沿用原书编号 {prefix}.1。"))
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scope",
        choices=SCOPES,
        default="all-current",
        help="选择章节批次、基础阶段、当前全部章节或附录（默认：当前全部）。",
    )
    parser.add_argument(
        "--rendered",
        action="store_true",
        help="同时检查 _output 中的公式锚点与章节编号；应先运行 quarto render notes。",
    )
    args = parser.parse_args()
    issues: list[str] = []
    for name, requirements in EXPECTED.items():
        if name not in SCOPES[args.scope]:
            continue
        path = NOTES / name
        issues.extend(check_file(path, *requirements))
        if args.rendered and path.exists():
            issues.extend(check_rendered_file(path, requirements[1]))
    for message in issues:
        print(message)
    if issues:
        print(f"NOTES_CHECK_FAILED: {len(issues)} 个错误。")
        return 1
    print(f"NOTES_CHECK_OK: {args.scope} 达到结构、详细度和公式编号门槛。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
