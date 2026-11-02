#!/usr/bin/env python3
"""Copy the canonical prompts and interview guide into index.html.

The files in prompts/ and standard/INTERVIEW-GUIDE.md are the only source. The
page carries static copies between BEGIN/END markers so it works without
JavaScript. Use --write to refresh them and --check to fail when they differ.
Uses only the Python standard library.
"""
from __future__ import annotations

import html
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
BLOCK = re.compile(
    r"(?P<open><!-- BEGIN (?P<kind>prompt|interview)(?: (?P<name>[\w-]+))? -->)"
    r"(?P<body>.*?)"
    r"(?P<close><!-- END (?P=kind)(?: (?P=name))? -->)",
    re.S,
)


def inline(text: str) -> str:
    escaped = html.escape(text, quote=False)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def prompt_html(name: str) -> str:
    text = (ROOT / "prompts" / f"{name}.md").read_text(encoding="utf-8").rstrip("\n")
    label = re.sub(r"^\d+-", "", name).replace("-", " ")
    # The panel scrolls, so it must take keyboard focus (WCAG 2.1.1) and have a name.
    return (f'<pre class="spec-prompt__text" id="prompt-{name}" tabindex="0" role="region" '
            f'aria-label="{label} prompt text">{html.escape(text, quote=False)}</pre>')


def interview_html() -> str:
    lines = (ROOT / "standard/INTERVIEW-GUIDE.md").read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    in_list = False
    seen_first_heading = False
    for line in lines:
        if line.startswith("# "):
            continue
        if line.startswith("## "):
            if in_list:
                out.append("</ul>")
                in_list = False
            seen_first_heading = True
            out.append(f"<h4>{inline(line[3:])}</h4>")
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(line[2:])}</li>")
        elif line.strip():
            # Intro paragraphs before the first question group stay in the repo file.
            if seen_first_heading:
                if in_list:
                    out.append("</ul>")
                    in_list = False
                out.append(f"<p>{inline(line)}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def render(match: re.Match[str]) -> str:
    kind, name = match["kind"], match["name"]
    content = interview_html() if kind == "interview" else prompt_html(name)
    return f"{match['open']}\n{content}\n{match['close']}"


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) == 2 else ""
    if mode not in ("--write", "--check"):
        print("Usage: python3 scripts/sync-prompts.py --write | --check", file=sys.stderr)
        return 2
    source = INDEX.read_text(encoding="utf-8")
    if not BLOCK.search(source):
        print("ERROR: index.html has no BEGIN/END prompt blocks.", file=sys.stderr)
        return 1
    updated = BLOCK.sub(render, source)
    if mode == "--write":
        INDEX.write_text(updated, encoding="utf-8")
        print("Prompt blocks written to index.html.")
        return 0
    if updated != source:
        print("ERROR: index.html differs from prompts/ or standard/INTERVIEW-GUIDE.md. "
              "Run: python3 scripts/sync-prompts.py --write", file=sys.stderr)
        return 1
    print("Prompt blocks match the canonical files: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
