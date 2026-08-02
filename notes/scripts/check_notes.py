#!/usr/bin/env python3
"""检查 Hansen 中文学习笔记的结构、详细度和原书公式锚点。"""

from __future__ import annotations

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
    "appendix-a.qmd": (23, "A", 3500),
    "appendix-b.qmd": (5, "B", 2200),
}
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD)\b|待补|占位|Lorem", re.I)
CHINESE = re.compile(r"[\u3400-\u9fff]")
TAG = re.compile(r"\\tag\{([1-9]\d*|[AB])\.(\d+)\}")
ANCHOR = re.compile(r"\{#hansen-eq-([1-9]\d*|[ab])-(\d+)\}")
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


def main() -> int:
    issues: list[str] = []
    for name, requirements in EXPECTED.items():
        issues.extend(check_file(NOTES / name, *requirements))
    for message in issues:
        print(message)
    if issues:
        print(f"NOTES_CHECK_FAILED: {len(issues)} 个错误。")
        return 1
    print("NOTES_CHECK_OK: Ch.1–6 与 Appendix A–B 达到结构、详细度和公式编号门槛。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
