#!/usr/bin/env python3
"""检查 Hansen 中文学习笔记的结构、详细度和原书公式锚点。"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
NOTES = ROOT / "notes"
READING_AID = "abbreviations.qmd"
BOOK_SOURCES = [
    "index.qmd",
    READING_AID,
    *(f"ch{i:02d}.qmd" for i in range(1, 30)),
    "appendix-a.qmd",
    "appendix-b.qmd",
]
EXPECTED = {
    "ch01.qmd": (10, "1", 1200),
    "ch02.qmd": (34, "2", 5000),
    "ch03.qmd": (26, "3", 4500),
    "ch04.qmd": (27, "4", 4500),
    "ch05.qmd": (15, "5", 2800),
    "ch06.qmd": (10, "6", 2200),
    "ch07.qmd": (22, "7", 3800),
    "ch08.qmd": (17, "8", 3300),
    "ch09.qmd": (24, "9", 4000),
    "ch10.qmd": (32, "10", 4500),
    "ch11.qmd": (18, "11", 3200),
    "ch12.qmd": (43, "12", 4800),
    "ch13.qmd": (29, "13", 4500),
    "ch14.qmd": (48, "14", 5200),
    "ch15.qmd": (32, "15", 3000),
    "ch16.qmd": (23, "16", 4000),
    "ch17.qmd": (45, "17", 3500),
    "ch18.qmd": (10, "18", 1700),
    "ch19.qmd": (27, "19", 3500),
    "ch20.qmd": (32, "20", 4500),
    "ch21.qmd": (12, "21", 2700),
    "ch22.qmd": (10, "22", 2200),
    "ch23.qmd": (11, "23", 2300),
    "ch24.qmd": (17, "24", 2200),
    "ch25.qmd": (15, "25", 2250),
    "ch26.qmd": (14, "26", 4200),
    "ch27.qmd": (13, "27", 4200),
    "ch28.qmd": (33, "28", 7800),
    "ch29.qmd": (24, "29", 7200),
    "appendix-a.qmd": (23, "A", 3500),
    "appendix-b.qmd": (5, "B", 2200),
}
SCOPES = {
    "appendices": {"appendix-a.qmd", "appendix-b.qmd"},
    "chapters-1-2": {"ch01.qmd", "ch02.qmd"},
    "chapters-3-4": {"ch03.qmd", "ch04.qmd"},
    "chapters-5-6": {"ch05.qmd", "ch06.qmd"},
    "chapters-7-8": {"ch07.qmd", "ch08.qmd"},
    "chapters-9-10": {"ch09.qmd", "ch10.qmd"},
    "chapters-11-13": {"ch11.qmd", "ch12.qmd", "ch13.qmd"},
    "chapter-14": {"ch14.qmd"},
    "chapters-15-16": {"ch15.qmd", "ch16.qmd"},
    "chapter-17": {"ch17.qmd"},
    "chapter-18": {"ch18.qmd"},
    "chapter-19": {"ch19.qmd"},
    "chapter-20": {"ch20.qmd"},
    "chapter-21": {"ch21.qmd"},
    "chapter-22": {"ch22.qmd"},
    "chapter-23": {"ch23.qmd"},
    "chapter-24": {"ch24.qmd"},
    "chapter-25": {"ch25.qmd"},
    "chapter-26": {"ch26.qmd"},
    "chapter-27": {"ch27.qmd"},
    "chapter-28": {"ch28.qmd"},
    "chapter-29": {"ch29.qmd"},
    "reading-aids": {READING_AID},
    "chapters-14-18": {*(f"ch{i:02d}.qmd" for i in range(14, 19))},
    "chapters": {name for name in EXPECTED if name.startswith("ch")},
    "foundation": {
        "appendix-a.qmd",
        "appendix-b.qmd",
        *(f"ch{i:02d}.qmd" for i in range(1, 7)),
    },
    "all-current": {*EXPECTED, READING_AID},
}
PLACEHOLDER = re.compile(r"\b(?:TODO|TBD)\b|待补|占位|Lorem", re.I)
CHINESE = re.compile(r"[\u3400-\u9fff]")
TAG = re.compile(r"\\tag\{([1-9]\d*|[AB])\.(\d+)\}")
ANCHOR = re.compile(r"\{#hansen-eq-([1-9]\d*|[ab])-(\d+)\}")
FENCED_ANCHOR = re.compile(
    r"^::: \{#hansen-eq-([1-9]\d*|[ab])-(\d+)\}\s*$", re.M
)
REFERENCE = re.compile(r"\[式 \(([1-9]\d*|[AB])\.(\d+)\)\]\(([^)]+)\)")
QMD_LINK = re.compile(r"\((ch\d{2}|appendix-[ab])\.qmd(?:#[^)]+)?\)")
LOCAL_QMD_LINK = re.compile(r"\]\(([^)]+\.qmd(?:#[^)]+)?)\)")


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
    if len(tags) != len(set(tags)) or len(anchors) != len(set(anchors)):
        issues.append(error(path, "DUPLICATE_FORMULA", "同一原书公式编号或稳定锚点在本页重复出现。"))
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


def check_reading_aid(path: Path) -> list[str]:
    """检查独立缩写材料的覆盖面、中文详细度与章节链接。"""
    issues: list[str] = []
    if not path.exists():
        return [error(path, "MISSING_FILE", "缩写阅读材料不存在。")]
    text = path.read_text(encoding="utf-8")
    if PLACEHOLDER.search(text):
        issues.append(error(path, "PLACEHOLDER", "含未完成占位符。"))
    chinese_count = len(CHINESE.findall(text))
    if chinese_count < 6000:
        issues.append(error(path, "DETAIL_LEVEL", f"中文字符约 {chinese_count}，低于缩写材料门槛 6000。"))
    sections = len(re.findall(r"^##\s+", text, re.M))
    if sections < 12:
        issues.append(error(path, "SECTION_COUNT", f"二级小节 {sections}，至少应为 12。"))
    table_rows = [
        line for line in text.splitlines()
        if line.startswith("|")
        and not re.match(r"^\|\s*(?:---|缩写|写法|记号)", line)
    ]
    if len(table_rows) < 150:
        issues.append(error(path, "GLOSSARY_COVERAGE", f"有效表格行约 {len(table_rows)}，低于整书覆盖门槛 150。"))
    for required in ("英文全称", "中文释义", "同形缩写速查", "按字母快速定位", "阅读自检"):
        if required not in text:
            issues.append(error(path, "MISSING_BLOCK", f"缺少“{required}”。"))
    for stem in QMD_LINK.findall(text):
        target = NOTES / f"{stem}.qmd"
        if not target.exists():
            issues.append(error(path, "BROKEN_SOURCE_LINK", f"章节链接目标不存在：{target.name}。"))
    return issues


def check_rendered_reading_aid(path: Path) -> list[str]:
    output = NOTES / "_output" / f"{path.stem}.html"
    if not output.exists():
        return [error(path, "MISSING_RENDER", f"渲染产物不存在：{output.relative_to(ROOT)}。")]
    html = output.read_text(encoding="utf-8")
    issues: list[str] = []
    for anchor in ("怎样使用这份材料", "同形缩写速查", "阅读自检"):
        if anchor not in html:
            issues.append(error(path, "MISSING_RENDERED_SECTION", f"HTML 中缺少“{anchor}”。"))
    return issues


class LinkCollector(HTMLParser):
    """收集渲染 HTML 中的元素 id 与超链接。"""

    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "a" and values.get("href"):
            self.hrefs.append(values["href"] or "")


def check_book_manifest() -> list[str]:
    """核对 Quarto 清单恰好含首页、Ch.1--29、附录与缩写材料。"""
    config = NOTES / "_quarto.yml"
    text = config.read_text(encoding="utf-8")
    listed = re.findall(r"^\s+-\s+([^\s]+\.qmd)\s*$", text, re.M)
    if listed != BOOK_SOURCES:
        return [
            error(
                config,
                "BOOK_MANIFEST",
                f"Quarto 页面顺序不完整或有漂移。应为 {BOOK_SOURCES}，实际为 {listed}。",
            )
        ]
    return []


def check_global_source_links() -> list[str]:
    """核对跨页 qmd 链接及公式显示编号与目标锚点。"""
    issues: list[str] = []
    for name in BOOK_SOURCES:
        source = NOTES / name
        if not source.exists():
            issues.append(error(source, "MISSING_FILE", "Quarto 清单中的源文件不存在。"))
            continue
        text = source.read_text(encoding="utf-8")
        for raw_target in LOCAL_QMD_LINK.findall(text):
            path_part, _, fragment = raw_target.partition("#")
            target = source.parent / path_part
            if not target.exists():
                issues.append(error(source, "BROKEN_SOURCE_LINK", f"链接目标不存在：{raw_target}。"))
                continue
            if fragment and fragment.startswith("hansen-eq-"):
                target_text = target.read_text(encoding="utf-8")
                if f"{{#{fragment}}}" not in target_text:
                    issues.append(error(source, "BROKEN_SOURCE_ANCHOR", f"公式锚点不存在：{raw_target}。"))

        for chapter, number, raw_target in REFERENCE.findall(text):
            path_part, marker, fragment = raw_target.partition("#")
            expected = f"hansen-eq-{chapter.lower()}-{number}"
            if not marker or fragment != expected:
                issues.append(
                    error(
                        source,
                        "FORMULA_REF_MISMATCH",
                        f"式 ({chapter}.{number}) 应指向 #{expected}，实际为 {raw_target}。",
                    )
                )
                continue
            target = source if not path_part else source.parent / path_part
            if not target.exists() or f"{{#{expected}}}" not in target.read_text(encoding="utf-8"):
                issues.append(error(source, "BROKEN_FORMULA_REF", f"式 ({chapter}.{number}) 的目标不存在：{raw_target}。"))
    return issues


def check_rendered_book() -> list[str]:
    """遍历全部 book HTML，核对页面清单、本地页面链接和 fragment id。"""
    output = NOTES / "_output"
    issues: list[str] = []
    expected = {f"{Path(name).stem}.html" for name in BOOK_SOURCES}
    actual = {path.name for path in output.glob("*.html")}
    if actual != expected:
        issues.append(
            error(
                NOTES / "_quarto.yml",
                "RENDERED_MANIFEST",
                f"HTML 页面集合不符；缺少 {sorted(expected - actual)}，多出 {sorted(actual - expected)}。",
            )
        )

    parsed: dict[Path, LinkCollector] = {}
    for name in expected & actual:
        path = output / name
        collector = LinkCollector()
        collector.feed(path.read_text(encoding="utf-8"))
        parsed[path.resolve()] = collector

    output_root = output.resolve()
    for source_path, collector in parsed.items():
        for href in collector.hrefs:
            split = urlsplit(href)
            if split.scheme or split.netloc:
                continue
            link_path = unquote(split.path)
            fragment = unquote(split.fragment)
            if link_path and not link_path.endswith(".html"):
                continue
            target = source_path if not link_path else (source_path.parent / link_path).resolve()
            if output_root not in target.parents and target != output_root:
                issues.append(error(source_path, "LINK_OUTSIDE_BOOK", f"本地 HTML 链接越出 book 输出目录：{href}。"))
                continue
            if not target.exists():
                issues.append(error(source_path, "BROKEN_HTML_LINK", f"HTML 页面链接不存在：{href}。"))
                continue
            if fragment:
                target_collector = parsed.get(target)
                if target_collector is None:
                    target_collector = LinkCollector()
                    target_collector.feed(target.read_text(encoding="utf-8"))
                    parsed[target] = target_collector
                if fragment not in target_collector.ids:
                    issues.append(error(source_path, "BROKEN_HTML_ANCHOR", f"HTML fragment 不存在：{href}。"))

    abbreviation_html = output / "abbreviations.html"
    if abbreviation_html.exists() and re.search(
        r"<h[1-6][^>]*data-number=", abbreviation_html.read_text(encoding="utf-8")
    ):
        issues.append(error(NOTES / READING_AID, "READING_AID_NUMBERED", "缩写材料的标题或小节不应占用正文或附录编号。"))
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
    parser.add_argument(
        "--global-audit",
        action="store_true",
        help="核对完整 Quarto 清单、跨页源链接与全部 HTML fragment；通常与 --rendered 合用。",
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
    if READING_AID in SCOPES[args.scope]:
        reading_aid = NOTES / READING_AID
        issues.extend(check_reading_aid(reading_aid))
        if args.rendered and reading_aid.exists():
            issues.extend(check_rendered_reading_aid(reading_aid))
    if args.global_audit:
        issues.extend(check_book_manifest())
        issues.extend(check_global_source_links())
        if args.rendered:
            issues.extend(check_rendered_book())
    for message in issues:
        print(message)
    if issues:
        print(f"NOTES_CHECK_FAILED: {len(issues)} 个错误。")
        return 1
    suffix = "，并通过全书清单与链接审计" if args.global_audit else ""
    print(f"NOTES_CHECK_OK: {args.scope} 达到结构、详细度和公式编号门槛{suffix}。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
