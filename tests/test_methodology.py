#!/usr/bin/env python3
"""Keep the standard, templates, prompts, and fixtures consistent. Standard library only."""
from __future__ import annotations

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def headings(text: str, level: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(rf"^{level} (.+)$", text, re.M)]


def strip_number(heading: str) -> str:
    return re.sub(r"\s*\(.*\)$", "", re.sub(r"^\d+\.\s*", "", heading))


class MethodologyTests(unittest.TestCase):
    def test_standard_and_template_use_the_same_sections(self):
        standard = headings(read("standard/SPEC-STANDARD.md").split("## SPEC.md structure")[1]
                            .split("## PROJECT-BRIEF.md structure")[0], "###")
        template = headings(read("templates/SPEC-TEMPLATE.md"), "##")
        self.assertEqual([strip_number(h) for h in standard], [strip_number(h) for h in template])

    def test_create_prompt_lists_the_standard_sections(self):
        standard = headings(read("standard/SPEC-STANDARD.md").split("## SPEC.md structure")[1]
                            .split("## PROJECT-BRIEF.md structure")[0], "###")
        prompt = read("prompts/03-create-spec.md")
        for heading in standard:
            name = strip_number(heading)
            self.assertIn(name, prompt, f"03-create-spec.md does not mention section: {name}")

    def test_brief_template_matches_the_standard(self):
        brief = headings(read("templates/PROJECT-BRIEF-TEMPLATE.md"), "##")
        self.assertEqual(brief, ["Project", "Problem", "Why this matters", "Users", "Experience", "Scope",
                                 "Not included", "Key decisions", "Deadlines", "Key risks and mitigation",
                                 "Open questions", "Success"])
        for name in brief:
            self.assertIn(name, read("standard/SPEC-STANDARD.md"))

    def test_every_prompt_uses_the_evidence_labels_or_question_classes(self):
        for name in ("01-analyze", "03-create-spec"):
            text = read(f"prompts/{name}.md")
            for label in ("Confirmed", "Inferred", "Recommended", "Open question"):
                self.assertIn(label, text, f"{name} lacks {label}")
        for label in ("Blocking", "Important", "Implementation decision"):
            self.assertIn(label, read("prompts/02-find-gaps.md"))

    def test_prompts_are_numbered_and_platform_neutral(self):
        names = sorted(p.name for p in (ROOT / "prompts").glob("*.md"))
        self.assertEqual(names, ["01-analyze.md", "02-find-gaps.md", "03-create-spec.md",
                                 "04-review-spec.md", "05-build.md"])
        for name in names:
            text = read(f"prompts/{name}").lower()
            for tool in ("claude", "chatgpt", "copilot", "openai"):
                self.assertNotIn(tool, text, f"{name} names a platform: {tool}")

    def test_build_prompt_has_the_ten_steps(self):
        steps = re.findall(r"^\d+\. ", read("prompts/05-build.md"), re.M)
        self.assertEqual(len(steps), 10)

    def test_fixtures_are_complete(self):
        folders = [p for p in (ROOT / "tests/fixtures").iterdir() if p.is_dir()]
        self.assertGreaterEqual(len(folders), 3)
        for folder in folders:
            for name in ("interview.md", "supporting-material.md", "expected-characteristics.md"):
                self.assertTrue((folder / name).is_file(), f"{folder.name} lacks {name}")

    def test_personal_information_rules_are_everywhere_they_matter(self):
        self.assertIn("personal information", read("standard/SPEC-STANDARD.md"))
        for name in ("01-analyze", "03-create-spec", "04-review-spec", "05-build"):
            self.assertIn("personal information", read(f"prompts/{name}.md"), f"{name} lacks the rule")
        self.assertIn("personal", read("templates/SPEC-TEMPLATE.md"))
        self.assertIn("Reduce personal information first", read("index.html"))

    def test_priorities_and_story_form_match_everywhere(self):
        for name in ("standard/SPEC-STANDARD.md", "templates/SPEC-TEMPLATE.md", "prompts/03-create-spec.md"):
            text = read(name)
            self.assertIn("P1", text, f"{name} lacks the P1 to P3 priorities")
            self.assertIn("would like", text, f"{name} lacks the story form")
            self.assertNotIn("must, should", text, f"{name} still uses must, should, could")

    def test_spec_and_review_prompts_ask_for_word_files(self):
        for name in ("03-create-spec", "04-review-spec"):
            self.assertIn("Word", read(f"prompts/{name}.md"), f"{name} does not ask for Word files")

    def test_interview_guide_covers_the_topics(self):
        groups = headings(read("standard/INTERVIEW-GUIDE.md"), "##")
        for topic in ("Project", "Users", "Current experience", "Future experience",
                      "Content and data", "Technology", "Access", "Constraints", "Success"):
            self.assertIn(topic, groups)


if __name__ == "__main__":
    unittest.main(verbosity=2)
