#!/usr/bin/env python3
"""Marin Spec workflow checks over local HTTP: steps, Copy prompt,
reflow, and no-JavaScript access. Reuses the starter smoke test's server and helpers."""
from __future__ import annotations

from pathlib import Path
import shutil
import sys

from browser_smoke import configure, ready, require, serve, no_overflow

ROOT = Path(__file__).resolve().parents[1]
PROMPTS = sorted((ROOT / "prompts").glob("*.md"))
STEPS = ["prepare", "analyze", "resolve", "spec", "review", "build"]


def current_steps(page) -> list[str]:
    return page.eval_on_selector_all(".spec-steps a[aria-current='step']", "els => els.map(e => e.getAttribute('href'))")


def run() -> None:
    from playwright.sync_api import sync_playwright

    with serve() as base_url, sync_playwright() as pw:
        executable = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
        options = {"headless": True, "args": ["--no-sandbox", "--disable-dev-shm-usage"]}
        if executable:
            options["executable_path"] = executable
        browser = pw.chromium.launch(**options)
        try:
            context = browser.new_context(viewport={"width": 1280, "height": 900})
            context.grant_permissions(["clipboard-read", "clipboard-write"], origin=base_url.rsplit("/", 2)[0])
            problems, _ = configure(context, base_url)
            page = context.new_page()
            page.goto(base_url, wait_until="networkidle")
            ready(page)

            # Steps: six links in order, one marked current, and it follows the address.
            require(page.locator(".spec-steps ol > li").count() == 6, "Expected six steps")
            require(page.locator(".spec-steps a").all_text_contents() == ["1. Prepare", "2. Analyze", "3. Resolve", "4. Spec", "5. Review", "6. Build"],
                    "Step names or order differ")
            require(current_steps(page) == ["#prepare"], "Prepare should start as the current step")
            page.locator(".spec-steps a[href='#resolve']").click()
            page.wait_for_function("() => document.querySelector(\"a[aria-current='step']\")?.getAttribute('href') === '#resolve'")
            require(current_steps(page) == ["#resolve"], "Exactly one step should be current")
            visible = [s for s in STEPS if page.locator(f"#{s}").is_visible()]
            require(visible == ["resolve"], f"Only the chosen step should show, got {visible}")
            require(page.locator("#resolve > h2").evaluate("el => el === document.activeElement"),
                    "Focus should move to the step heading")
            page.locator("#resolve [data-next-step]").click()
            page.wait_for_function("() => document.querySelector(\"a[aria-current='step']\")?.getAttribute('href') === '#spec'")
            require(page.locator("#resolve [data-next-step]").evaluate("el => el.classList.contains('primary')"),
                    "Next should be the solid main-action button")
            require(page.locator("#spec").is_visible() and not page.locator("#resolve").is_visible(), "Next did not change the step")
            previous = page.locator("#spec [data-prev-step]")
            require(previous.evaluate("el => el.classList.contains('action-button') && !el.classList.contains('primary') && el.textContent.trim() === '' && !!el.querySelector('svg')"),
                    "Previous should be a quiet icon-only action button with an arrow")
            require(previous.get_attribute("aria-label") == "Previous: resolve", "Previous should name the step")
            require(page.locator("#prepare [data-prev-step]").count() == 0, "The first step has no Previous")
            require(page.locator("#build [data-next-step]").count() == 0, "The last step has no Next")
            previous.click()
            require(page.locator("#resolve").is_visible(), "Previous did not go back")
            page.locator("#resolve [data-next-step]").click()
            page.go_back()
            page.wait_for_function("() => document.querySelector(\"a[aria-current='step']\")?.getAttribute('href') === '#resolve'")
            require(page.locator("#resolve").is_visible(), "Back did not return to the previous step")
            side, results = page.locator(".search-side").bounding_box(), page.locator(".search-results").bounding_box()
            require(side["x"] < results["x"], "The steps should sit in a left column")
            require(page.locator(".spec-steps ol").evaluate("el => getComputedStyle(el).display") == "block",
                    "Steps should be stacked")
            require(page.locator(".spec-steps a").all_text_contents() == ["1. Prepare", "2. Analyze", "3. Resolve", "4. Spec", "5. Review", "6. Build"],
                    "Step labels should read '1. Name'")
            require(page.locator("input[type='radio'], [data-platform]").count() == 0, "The tool selector should be gone")
            keys = page.evaluate("() => Object.keys(window.localStorage)")
            require(not [k for k in keys if not k.startswith("marinos-")], f"The app should store nothing itself, found {keys}")

            # The steps column collapses and reopens.
            toggle = page.locator(".filter-toggle")
            require(toggle.get_attribute("aria-label") == "Steps", "The toggle should be named Steps")
            require(toggle.get_attribute("aria-expanded") == "true", "The column should start open on wide screens")
            toggle.click()
            require(toggle.get_attribute("aria-expanded") == "false" and page.locator("#steps-panel").is_hidden(),
                    "The column did not collapse")
            require(page.locator(".search-results").bounding_box()["width"] > results["width"], "Content should widen")
            require(page.locator(".spec-progress").inner_text() == "Step 3 of 6: Resolve",
                    "The current step should show while the column is collapsed")
            require(page.locator(".spec-progress").is_visible(), "The current step line should be visible when collapsed")
            page.locator("#resolve [data-next-step]").click()
            require(page.locator(".spec-progress").inner_text() == "Step 4 of 6: Spec", "The step line should follow Next")
            page.locator("#spec [data-prev-step]").click()
            toggle.click()
            require(page.locator("#steps-panel").is_visible(), "The column did not reopen")

            # "On this page": the current step's boxes, rebuilt per step, linking to boxes that stay on their step.
            page.locator(".spec-steps a[href='#prepare']").click()
            require(page.locator(".spec-toc li a").all_text_contents()[:2] == ["Gather these", "Reduce personal information first"],
                    "On this page should list the Prepare boxes")
            toc_box, main_box = page.locator(".spec-toc").bounding_box(), page.locator(".spec-main").bounding_box()
            require(toc_box["x"] > main_box["x"] + main_box["width"] - 1, "On this page should be a right-hand column")
            page.locator(".spec-toc a", has_text="Interview your project owner").click()
            page.wait_for_timeout(300)
            require(page.locator(".spec-toc").is_visible() and page.locator(".spec-toc").bounding_box()["y"] >= 0,
                    "On this page should stay in view while you read")
            page.locator(".spec-steps a[href='#spec']").click()
            require("Spec prompt" in page.locator(".spec-toc li a").all_text_contents(), "On this page should list the Spec boxes")
            page.locator(".spec-toc a", has_text="Save a copy for review").click()
            page.wait_for_function("() => document.querySelector('.spec-toc a[aria-current=\"location\"]') !== null")
            require(page.locator("#spec").is_visible() and page.locator("a[aria-current='step']").get_attribute("href") == "#spec",
                    "A link in On this page should keep the step")
            require(page.locator("#spec-save-a-copy-for-review").is_visible(), "The box should be on screen")

            # Every step ends with a "You're ready when" box, and the troubleshooting link reaches About.
            for step in STEPS:
                require(page.locator(f"#{step} .spec-box h3", has_text="You're ready when").count() == 1, f"{step} lacks a ready check")
            page.locator(".spec-steps a[href='#spec']").click()
            require(page.locator("#spec .spec-box h3", has_text="Save a copy for review").count() == 1, "Spec needs the save-for-review box")
            require("Word" in page.locator("#spec").inner_text(), "Spec should mention a Word copy")
            page.locator(".spec-steps a[href='#analyze']").click()
            page.get_by_role("link", name="If something goes wrong").click()
            page.wait_for_function("() => !document.getElementById('about').hidden")
            require("Continue" in page.locator("#about").inner_text(), "About should list what to do when something goes wrong")
            page.go_back()
            page.wait_for_function("() => !document.getElementById('start').hidden")

            # The scrolling prompt panels take keyboard focus and have names.
            for prompt in PROMPTS:
                panel = page.locator(f"#prompt-{prompt.stem}")
                require(panel.get_attribute("tabindex") == "0" and bool(panel.get_attribute("aria-label")),
                        f"{prompt.name} panel needs tabindex and a name")

            # Copy prompt: every prompt copies exactly its canonical file and reports it.
            step_of = {"01": "analyze", "02": "resolve", "03": "spec", "04": "review", "05": "build"}
            for prompt in PROMPTS:
                page.locator(f".spec-steps a[href='#{step_of[prompt.stem[:2]]}']").click()
                button = page.locator(f"[data-copy-prompt='prompt-{prompt.stem}']")
                require(button.is_visible(), f"No Copy prompt button for {prompt.name}")
                button.click()
                status = button.locator("xpath=ancestor::div[contains(@class,'spec-prompt')]//*[@role='status']")
                status.wait_for(state="visible")
                require("Copied" in status.inner_text(), f"No copied message for {prompt.name}")
                copied = page.evaluate("() => navigator.clipboard.readText()")
                require(copied.strip() == prompt.read_text().strip(), f"Clipboard differs from {prompt.name}")
            require(not problems, f"Browser errors: {problems}")
            context.close()

            # Reflow at the narrowest supported width.
            narrow = browser.new_context(viewport={"width": 320, "height": 800})
            narrow_problems, _ = configure(narrow, base_url)
            small = narrow.new_page()
            small.goto(base_url, wait_until="networkidle")
            ready(small)
            small_toggle = small.locator(".filter-toggle")
            require(small_toggle.is_visible() and small.locator("#steps-panel").is_hidden(),
                    "The steps column should start closed on narrow screens")
            require(small.locator(".spec-progress").is_visible(), "The current step should show on narrow screens")
            for step in STEPS:
                no_overflow(small)
                if step != STEPS[-1]:
                    small.locator(f"#{step} [data-next-step]").click()
            toc_small, main_small = small.locator(".spec-toc").bounding_box(), small.locator(".spec-main").bounding_box()
            require(toc_small["y"] < main_small["y"], "On this page should sit above the step on narrow screens")
            small_toggle.click()
            require(small.locator("#steps-panel").is_visible(), "The steps column did not open")
            no_overflow(small)
            require(not narrow_problems, f"Narrow browser errors: {narrow_problems}")
            narrow.close()

            # No JavaScript: every prompt and the interview questions are on the page.
            plain = browser.new_context(java_script_enabled=False)
            nojs = plain.new_page()
            nojs.goto(base_url, wait_until="networkidle")
            for prompt in PROMPTS:
                require(nojs.locator(f"#prompt-{prompt.stem}").inner_text().strip() == prompt.read_text().strip(),
                        f"{prompt.name} is not readable without JavaScript")
            require(nojs.locator(".spec-interview li").count() >= 20, "Interview questions missing without JavaScript")
            require(all(nojs.locator(f"#{step}").is_visible() for step in STEPS), "A step is hidden without JavaScript")
            require(nojs.locator(".spec-toc").count() == 0, "On this page needs JavaScript and should not appear without it")
            require(nojs.locator("[data-copy-prompt]:visible, [data-next-step]:visible, [data-prev-step]:visible").count() == 0,
                    "Copy, Previous and Next buttons should stay hidden without JavaScript")
            plain.close()
        finally:
            browser.close()


if __name__ == "__main__":
    try:
        run()
        print("Marin Spec browser workflow: PASS")
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
