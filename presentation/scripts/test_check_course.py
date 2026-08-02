#!/usr/bin/env python3
"""check_course.py 的回归测试。"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from check_course import (  # noqa: E402
    MAIN_HEADINGS,
    WORKSHOP_HEADINGS,
    WORKSHOP_NUMBERS,
    check_course,
    check_deck,
    parse_front_matter,
    split_slides,
)


def make_deck(number: int) -> str:
    workshop = number in WORKSHOP_NUMBERS
    headings = list(WORKSHOP_HEADINGS if workshop else MAIN_HEADINGS)
    while len(headings) < 18:
        headings.append(f"概念练习 {len(headings) + 1}")
    chunks = [
        "---",
        f'title: "第 {number:02d} 次中文课"',
        f"session-number: {number}",
        f'session-type: "{"工作坊" if workshop else "主课"}"',
        f"semester: {1 if number <= 20 else 2}",
        "duration: 90",
        'chapters: "Ch.1"',
        'book-pages: "1–10"',
        'pdf-pages: "21–30"',
        "---",
        "",
    ]
    for heading in headings:
        chunks.extend(
            [
                f"## {heading}",
                "",
                "中文教学正文。",
                "",
                "::: {.notes}",
                "中文讲者备注。",
                ":::",
                "",
            ]
        )
    return "\n".join(chunks)


def build_fixture(root: Path) -> None:
    sessions = root / "presentation" / "sessions"
    supplements = root / "presentation" / "supplements"
    sessions.mkdir(parents=True)
    supplements.mkdir(parents=True)
    for number in range(1, 41):
        (sessions / f"{number:02d}-fixture.qmd").write_text(
            make_deck(number), encoding="utf-8"
        )
    for number in range(1, 8):
        (supplements / f"{number:02d}-supplement.qmd").write_text(
            f'---\ntitle: "中文补充讲义 {number}"\n---\n\n中文正文。\n',
            encoding="utf-8",
        )


class CourseCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        build_fixture(self.root)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_complete_course_passes(self) -> None:
        issues = check_course(self.root)
        self.assertEqual([], [issue for issue in issues if issue.level == "error"])

    def test_missing_session_and_balance_are_reported(self) -> None:
        (self.root / "presentation/sessions/40-fixture.qmd").unlink()
        codes = {issue.code for issue in check_course(self.root)}
        self.assertIn("MISSING_SESSIONS", codes)
        self.assertIn("COURSE_BALANCE", codes)

    def test_missing_supplement_is_reported(self) -> None:
        (self.root / "presentation/supplements/07-supplement.qmd").unlink()
        codes = {issue.code for issue in check_course(self.root)}
        self.assertIn("SUPPLEMENT_COUNT", codes)

    def test_metadata_notes_and_broken_link_are_reported(self) -> None:
        target = self.root / "presentation/sessions/01-fixture.qmd"
        text = target.read_text(encoding="utf-8")
        text = text.replace("duration: 90", "duration: 60")
        text = text.replace(
            "::: {.notes}\n中文讲者备注。\n:::", ""
        )
        text += "\n[不存在的材料](missing.md)\n"
        target.write_text(text, encoding="utf-8")
        codes = {issue.code for issue in check_deck(target, self.root)}
        self.assertTrue({"DURATION", "NOTES_COVERAGE", "BROKEN_LINK"} <= codes)

    def test_code_fence_does_not_create_slide_or_link(self) -> None:
        target = self.root / "presentation/sessions/01-fixture.qmd"
        original = target.read_text(encoding="utf-8")
        _, body = parse_front_matter(original)
        original_count = len(split_slides(body))
        target.write_text(
            original + "\n~~~r\n## 伪标题\n[伪链接](missing.md)\n~~~\n",
            encoding="utf-8",
        )
        _, new_body = parse_front_matter(target.read_text(encoding="utf-8"))
        self.assertEqual(original_count, len(split_slides(new_body)))
        codes = {issue.code for issue in check_deck(target, self.root)}
        self.assertNotIn("BROKEN_LINK", codes)

    def test_overflow_and_missing_alt_are_reported(self) -> None:
        target = self.root / "presentation/sessions/01-fixture.qmd"
        target.write_text(
            target.read_text(encoding="utf-8")
            + "\n## 超长测试页\n\n"
            + "长" * 901
            + "\n\n![](figure.png)\n\n::: {.notes}\n中文备注。\n:::\n",
            encoding="utf-8",
        )
        issues = check_deck(target, self.root)
        codes = {issue.code for issue in issues}
        self.assertIn("LONG_SLIDE", codes)
        self.assertIn("MISSING_ALT", codes)


if __name__ == "__main__":
    unittest.main()
