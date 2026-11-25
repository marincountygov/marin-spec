# Working on Marin Spec

## Architecture

Marin Spec is a static MarinOS app built from `marin-app-template`. It vendors a pinned Marin App Shell under `vendor/marinos/`; `platform.shell` in `marin.yml` must match `vendor/marinos/manifest.json`. Never edit `vendor/marinos/`.

It is a guide, not an AI application. It calls no AI service, uploads and stores nothing, needs no account, and has no database. `marin.yml` declares `ai: used: false` and `services: none`. Keep it that way unless the owner changes the scope.

## Source of truth

- `standard/SPEC-STANDARD.md` and `standard/INTERVIEW-GUIDE.md` define the method.
- `prompts/*.md` are the only copy of the prompts. They name no AI product and say the same thing for every tool.
- `templates/` hold the blank SPEC and project brief.
- `index.html` has generated copies between `BEGIN` and `END` markers. Change the source file, then run `python3 scripts/sync-prompts.py --write`. Never edit between the markers.
- The UI and the `marin-skills/marin-spec` skill point to the standard. Do not restate the standard in app code or the skill.

## UI rules

- The six steps (Prepare, Analyze, Resolve, Spec, Review, Build) are `section.step` elements under `#start`. They use the shell's steps layout (`nav.steps[data-steps]`; see "Steps layout" in `marin-ui/docs/components.md`): the list is the shell's collapsible left column (`.search-layout`, `data-filter-toggle` labeled "Steps", `data-filter-column-exempt="steps"` on its `aside`), and the shell shows one step at a time, writes "Completed", "Current" or "Up next" under each step, and fills `.steps-progress`, which stays the first child of `.search-results` (the narrow-screen layout needs a visible first child beside the toggle). Without JavaScript they are all visible. Do not turn them into hidden tabs, and do not write step, progress or "On this page" code in `assets/app.js` or `assets/app.css`.
- The header shows only About and Updates. The shell supplies the footer pages, including Security, Accessibility, and Tech.
- Copy prompt uses the shell's `marinCopyText`. Do not write your own copy code.
- The app stores nothing in the browser: no project content and no settings. The shell keeps its own catalog cache; that is not the app's.
- "On this page" is the right-hand column on wide screens and sits above the step on narrow ones (`.steps-body`, `[data-steps-toc]`). The shell builds it from the current step's `.step-box` headings, gives each box an id (`step-heading-words`), and rebuilds it when the step changes. A hash can name a step or a box. Do not hand-write the list.
- Each part of a step ("What you do", a prompt, "What you get back") is a `.step-box`, the shell's bordered section look, the same as the Marin Learn notes. The step heading and its one-line intro sit above the boxes.
- Use sentence case and plain language. No "view" in button or link text. No unprompted nested lists.
- Step labels read "1. Name" with no circled numbers, shapes or icons; the state is a word under each name. Completed means earlier than the current step, and nothing is saved. Previous and Next are made by the shell at the end of every step; write none. Next is the one solid button with words and a right arrow, and Previous is a quiet icon-only action button with a left arrow, like Copy and Download. The step list is a left column, not the row the Marin Mentions report builder uses, because the whole app is the workflow.

## Before finishing

Run `bash scripts/check.sh`, and `bash scripts/check.sh --browser` when Playwright and Chromium are available. State anything you did not run. After editing `security.json`, run `python3 scripts/sync-security-meta.py --write`. Do not commit, push, or register the app in `marin-os` unless asked.

## References

- `marin-app-shell`, `marin-ui`, `marin-digital-standards`, `marin-skills`, `marin-app-template`, `marin-os`
