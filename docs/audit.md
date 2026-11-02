# MarinOS audit and conflicts

Written before building. Records which MarinOS conventions Marin Spec follows and where the original plan changed.

## Sources read

`marin-app-template` (AGENTS.md, development guide, `marin.yml`, checks), `marin-app-shell` (components, copy helpers), `marin-ui` (components, tab sections, app nav), `marin-os` (AGENTS.md, schemas, catalog), `marin-digital-standards` (accessibility, content design, security profiles), and `marin-skills` (`marin-app-builder`, `app-maintainer`).

## Reused

- The app template, with the vendored shell 1.22.1, `security.json`, and the template checks.
- Shell-supplied About, Security, Accessibility, Tech, and Updates sections, header, and footer.
- Shell buttons (`.action-button`), the `marinCopyText` helper, and Lucide icons.
- Local Open Sans from the shell. No outside fonts or scripts.

## Conflicts with the original plan, and decisions

- **Routes.** The plan listed `/prepare` and similar routes. MarinOS apps are single pages with hash sections. The six steps (the plan had five; Review became its own step) are sections under `#start`.
- **One step at a time, still readable without JavaScript.** With JavaScript one step shows at a time. Without it every step is visible, so the instructions and prompts still work.
- **Steps in the left column.** The steps use the shell's collapsible left column (`.search-layout`), because the whole app is the workflow. A short flow inside one feature, such as the Marin Mentions report builder, keeps its steps as a row above the content.
- **"On this page."** A right-hand list built for the current step with the shell's `marinOnThisPage`, above the step on narrow screens, as the standard says.
- **No tool selector.** The plan had a Claude, ChatGPT or Copilot choice. The per-tool notes were almost identical and the choice added state, so it was removed. The prompts and the method are the same for every tool.
- **No explainer on the default view.** The "what is Marin Spec" copy and the privacy notes are in About. The first step opens with the checklist.
- **Separate pages.** The plan asked for `/accessibility`, `/security` and `/tech`. The shell provides these.
- **Copy button.** The shell requires Copy buttons to offer Text, HTML and Markdown. A prompt is one block of plain text, and the other formats would change what the user pastes. Copy prompt is a single-format button that uses `marinCopyText`. This is a deliberate exception to review with the standards owner.
- **Step buttons.** Next is the solid button with a right arrow. Previous is a quiet icon button like Copy and Download. The shell sizes declarative icons only inside quiet buttons, so the arrow on Next is sized in the app's CSS until the shell does it.
- **Button color.** Solid buttons showed Pico's stock blue, not Marin Blue. The fix is in `marin-ui` 1.33.0 and arrives with the next shell release.
- **Skill location.** Skills live in `marin-skills`, so the skill is `marin-skills/marin-spec/`, not `skills/` in this repo.
- **Prompts in the page.** There is no build step, so `scripts/sync-prompts.py` copies the prompts and interview questions into `index.html`. `--check` and the GitHub workflow keep them in sync.
- **Scrolling prompt panels.** They take keyboard focus and have names (WCAG 2.1.1). axe-core found this; it now reports nothing for the app.
- **Tests.** The starter's tests are Python. Marin Spec adds `tests/browser_spec.py` and `tests/test_methodology.py` in the same style.
- **Icon.** `route` is a Lucide icon (lucide-static 1.66.0, ISC). It is inline in the header and favicon. It is not in `marin-ui/vendor/icons/lucide/` yet, and it is not in the shell's icon set, so it cannot be added to this repo's `vendor/icons/`. Add it to `marin-ui` before registering the app in the catalog.
- **Security.** The `internal` profile fits: no sign-in, no user data, no outside services of its own.
- **Personal information.** The prompts and standard tell the AI tool not to repeat it and to label fields. The page asks people to reduce it before upload and use only an approved tool. Marin Spec cannot see files, so none of this is a guarantee.

## Open items

- Register the app in `marin-os` (`catalog.json`, the directory card, `projects.json`) once the owner approves.
- Add the `route` icon file to `marin-ui`.
- Run the workflow by hand with the fixtures in Claude, ChatGPT, and Copilot, then refine the standard and prompts. Check that each tool returns Word files when asked.
- Test with two or three staff who have not seen it, and refine the troubleshooting list from where they stall.
- Take a shell release that includes `marin-ui` 1.33.0 (Marin Blue buttons), and ask the shell to size icons on solid buttons.
- The shell's feedback component triggers an axe "region" notice. That is upstream.
- Flag `marin-skills/marin-app-builder` so a finished `SPEC.md` is a recommended input.
