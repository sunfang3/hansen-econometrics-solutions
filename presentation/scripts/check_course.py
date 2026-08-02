#!/usr/bin/env python3
"""Hansen 全年 Quarto 课程的静态质量检查。"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


WORKSHOP_NUMBERS = {7, 12, 17, 20, 25, 29, 33, 40}
SESSION_PATTERN = re.compile(r"^(?P<number>\d{2})-[a-z0-9-]+\.qmd$")
CHINESE_PATTERN = re.compile(r"[\u3400-\u9fff]")
PLACEHOLDER_PATTERN = re.compile(r"\b(?:TODO|TBD)\b|待补|占位|Lorem", re.I)
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\s]+)(?:\s+['\"][^'\"]+['\"])?\)")
IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HTML_IMAGE_PATTERN = re.compile(r"<img\b(?![^>]*\balt\s*=)[^>]*>", re.I)

MAIN_HEADINGS = (
    "本次课的任务", "先修检查", "从本科语言到 Hansen 语言", "路线图",
    "推导起点：", "条件与维数核对", "常见错误：错在哪里", "课堂检查题",
    "检查题解答与诊断", "本课小结", "阅读与练习", "备查与延伸",
)

WORKSHOP_HEADINGS = (
    "本次工作坊的任务", "先修检查", "研究问题", "数据状态与复现方式",
    "样本与筛选", "变量变换", "模型与识别", "估计量", "标准误、聚类与临界值",
    "执行流程", "R 代码：数据与设定", "R 代码：估计与输出", "示例输出",
    "诊断", "敏感性分析", "常见错误：错在哪里", "课堂检查题",
    "检查题解答与诊断", "工作坊小结", "复现任务与阅读", "备查与延伸",
)


@dataclass(frozen=True)
class Issue:
    level: str
    code: str
    path: Path
    message: str
    slide: str | None = None

    def format(self, root: Path) -> str:
        try:
            shown = self.path.relative_to(root)
        except ValueError:
            shown = self.path
        location = f"{shown}"
        if self.slide:
            location += f" [{self.slide}]"
        return f"{self.level.upper()} {self.code}: {location}: {self.message}"


def strip_code_fences(text: str) -> str:
    """移除 Markdown 代码围栏内容，避免把代码中的标题/链接当正文。"""
    kept: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        marker = re.match(r"^\s*([\x60]{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)[0]
            if fence is None:
                fence = token
            elif fence == token:
                fence = None
            continue
        if fence is None:
            kept.append(line)
    return "\n".join(kept)


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return {}, text
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][A-Za-z0-9-]*):\s*(.*?)\s*$", line)
        if match:
            metadata[match.group(1)] = match.group(2).strip("\"'")
    return metadata, "\n".join(lines[end + 1 :])


def split_slides(body: str) -> list[tuple[str, str]]:
    """按代码围栏之外的二级标题切分 RevealJS 幻灯片。"""
    slides: list[tuple[str, str]] = []
    title: str | None = None
    lines: list[str] = []
    fence: str | None = None
    for line in body.splitlines():
        marker = re.match(r"^\s*([\x60]{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)[0]
            if fence is None:
                fence = token
            elif fence == token:
                fence = None
            if title is not None:
                lines.append(line)
            continue
        heading = re.match(r"^##\s+(.+?)\s*$", line) if fence is None else None
        if heading:
            if title is not None:
                slides.append((title, "\n".join(lines)))
            title = heading.group(1)
            lines = []
        elif title is not None:
            lines.append(line)
    if title is not None:
        slides.append((title, "\n".join(lines)))
    return slides


def local_link_target(source: Path, raw_target: str) -> Path | None:
    target = raw_target.split("#", 1)[0]
    if not target or re.match(r"^(?:https?://|mailto:|data:)", target):
        return None
    candidate = (source.parent / target).resolve()
    if candidate.suffix == ".html" and not candidate.exists():
        qmd = candidate.with_suffix(".qmd")
        if qmd.exists():
            return qmd
    return candidate


def check_deck(path: Path, root: Path) -> list[Issue]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(text)
    clean_body = strip_code_fences(body)

    filename_match = SESSION_PATTERN.match(path.name)
    if not filename_match:
        issues.append(Issue("error", "BAD_FILENAME", path, "文件名须为两位课次加英文 slug。"))
        return issues
    number = int(filename_match.group("number"))

    required_metadata = (
        "session-number", "session-type", "semester", "duration",
        "chapters", "book-pages", "pdf-pages",
    )
    for key in required_metadata:
        if not metadata.get(key):
            issues.append(Issue("error", "MISSING_METADATA", path, f"缺少 front matter 字段 {key}。"))

    if metadata.get("session-number") != str(number):
        issues.append(Issue("error", "SESSION_NUMBER", path, "文件名课次与 session-number 不一致。"))
    if metadata.get("duration") != "90":
        issues.append(Issue("error", "DURATION", path, "每次课 duration 必须为 90。"))
    expected_semester = "1" if number <= 20 else "2"
    if metadata.get("semester") != expected_semester:
        issues.append(Issue("error", "SEMESTER", path, f"第 {number} 次应属于第 {expected_semester} 学期。"))

    expected_type = "工作坊" if number in WORKSHOP_NUMBERS else "主课"
    if metadata.get("session-type") != expected_type:
        issues.append(Issue("error", "SESSION_TYPE", path, f"第 {number} 次应标为{expected_type}。"))
    for key in ("book-pages", "pdf-pages"):
        if metadata.get(key) and not re.search(r"\d", metadata[key]):
            issues.append(Issue("error", "PAGE_RANGE", path, f"{key} 必须包含 Hansen 页码。"))

    slides = split_slides(body)
    if len(slides) < 18:
        issues.append(Issue("error", "TOO_FEW_SLIDES", path, f"只有 {len(slides)} 个内容页，低于 18。"))
    headings = [title for title, _ in slides]
    expected_headings = WORKSHOP_HEADINGS if expected_type == "工作坊" else MAIN_HEADINGS
    for required in expected_headings:
        if not any(title == required or title.startswith(required) for title in headings):
            issues.append(Issue("error", "MISSING_SECTION", path, f"缺少教学区块“{required}”。"))

    noted = 0
    for title, slide_body in slides:
        note_match = re.search(r":::\s*\{\.notes\}\s*(.*?)\s*:::", slide_body, re.S)
        if note_match:
            noted += 1
            if not CHINESE_PATTERN.search(note_match.group(1)):
                issues.append(Issue("error", "NON_CHINESE_NOTES", path, "讲者备注缺少中文说明。", title))
        content = re.sub(r":::\s*\{\.notes\}.*?:::", "", slide_body, flags=re.S)
        chinese_count = len(CHINESE_PATTERN.findall(content))
        list_count = len(re.findall(r"^\s*(?:[-*+]|\d+\.)\s+", content, re.M))
        display_formula_count = content.count("$$") // 2
        if chinese_count > 900:
            issues.append(Issue("warning", "LONG_SLIDE", path, f"正文约 {chinese_count} 个中文字符，可能溢出。", title))
        if list_count > 10:
            issues.append(Issue("warning", "MANY_BULLETS", path, f"有 {list_count} 个列表项，可能过密。", title))
        if display_formula_count > 3:
            issues.append(Issue("warning", "MANY_FORMULAS", path, f"有 {display_formula_count} 个展示公式，可能过密。", title))

    coverage = noted / len(slides) if slides else 0
    if coverage < 0.70:
        issues.append(Issue("error", "NOTES_COVERAGE", path, f"讲者备注覆盖率 {coverage:.0%}，低于 70%。"))

    if PLACEHOLDER_PATTERN.search(clean_body):
        issues.append(Issue("error", "PLACEHOLDER", path, "正文仍含 TODO/TBD/待补等占位符。"))

    for alt, _ in IMAGE_PATTERN.findall(clean_body):
        if not alt.strip():
            issues.append(Issue("error", "MISSING_ALT", path, "Markdown 图片缺少替代文本。"))
    if HTML_IMAGE_PATTERN.search(clean_body):
        issues.append(Issue("error", "MISSING_ALT", path, "HTML 图片缺少 alt 属性。"))

    for target in LINK_PATTERN.findall(clean_body):
        candidate = local_link_target(path, target)
        if candidate is not None and not candidate.exists():
            issues.append(Issue("error", "BROKEN_LINK", path, f"本地链接不存在：{target}。"))

    for repo_path in re.findall(r"仓库\s+([A-Za-z0-9_./-]+)", clean_body):
        candidate = root / repo_path
        if not candidate.exists():
            issues.append(Issue("error", "BROKEN_SOURCE_PATH", path, f"仓库材料路径不存在：{repo_path}。"))
    return issues


def check_course(root: Path) -> list[Issue]:
    root = root.resolve()
    presentation = root / "presentation"
    sessions_dir = presentation / "sessions"
    issues: list[Issue] = []
    files = sorted(sessions_dir.glob("[0-9][0-9]-*.qmd")) if sessions_dir.exists() else []

    numbers: list[int] = []
    for path in files:
        match = SESSION_PATTERN.match(path.name)
        if match:
            numbers.append(int(match.group("number")))
        issues.extend(check_deck(path, root))

    missing = sorted(set(range(1, 41)) - set(numbers))
    duplicates = sorted(number for number in set(numbers) if numbers.count(number) > 1)
    extras = sorted(set(numbers) - set(range(1, 41)))
    if missing:
        issues.append(Issue("error", "MISSING_SESSIONS", sessions_dir, f"缺少课次：{missing}。"))
    if duplicates:
        issues.append(Issue("error", "DUPLICATE_SESSIONS", sessions_dir, f"课次重复：{duplicates}。"))
    if extras:
        issues.append(Issue("error", "EXTRA_SESSIONS", sessions_dir, f"超出 01–40：{extras}。"))

    workshop_count = sum(number in WORKSHOP_NUMBERS for number in numbers)
    main_count = len(numbers) - workshop_count
    if main_count != 32 or workshop_count != 8:
        issues.append(Issue("error", "COURSE_BALANCE", sessions_dir, f"当前为 {main_count} 主课 + {workshop_count} 工作坊，应为 32 + 8。"))

    supplements_dir = presentation / "supplements"
    supplements = sorted(supplements_dir.glob("[0-9][0-9]-*.qmd")) if supplements_dir.exists() else []
    if len(supplements) != 7:
        issues.append(Issue("error", "SUPPLEMENT_COUNT", supplements_dir, f"补充讲义为 {len(supplements)} 份，应为 7 份。"))
    for supplement in supplements:
        metadata, body = parse_front_matter(supplement.read_text(encoding="utf-8"))
        if not metadata.get("title"):
            issues.append(Issue("error", "SUPPLEMENT_TITLE", supplement, "补充讲义缺少中文标题。"))
        elif not CHINESE_PATTERN.search(metadata["title"]):
            issues.append(Issue("error", "SUPPLEMENT_LANGUAGE", supplement, "补充讲义标题不是中文。"))
        clean_supplement = strip_code_fences(body)
        if PLACEHOLDER_PATTERN.search(clean_supplement):
            issues.append(Issue("error", "PLACEHOLDER", supplement, "补充讲义仍含占位符。"))
        for alt, _ in IMAGE_PATTERN.findall(clean_supplement):
            if not alt.strip():
                issues.append(Issue("error", "MISSING_ALT", supplement, "Markdown 图片缺少替代文本。"))
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="检查 Hansen 全年 Quarto 课程。")
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[2],
        help="仓库根目录；默认由脚本位置推断。",
    )
    args = parser.parse_args(argv)
    issues = check_course(args.root)
    errors = [issue for issue in issues if issue.level == "error"]
    warnings = [issue for issue in issues if issue.level == "warning"]
    for issue in issues:
        print(issue.format(args.root.resolve()))
    if errors:
        print(f"COURSE_CHECK_FAILED: {len(errors)} 个错误，{len(warnings)} 个警告。")
        return 1
    print(f"COURSE_CHECK_OK: 40 次课（32 主课 + 8 工作坊）、7 份补充讲义；{len(warnings)} 个警告。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
