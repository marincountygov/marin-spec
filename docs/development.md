# Development

Marin Spec is a static MarinOS app. There is no build step, package manager, or server code. The general shell, security, and update guidance is in [marin-app-template/docs/development.md](https://github.com/marincountygov/marin-app-template/blob/main/docs/development.md). This file covers what is specific to Marin Spec.

## Run locally

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Open `http://127.0.0.1:8765/`. Do not use `file://`: the shell fetches `security.json`.

## Where things live

- `standard/` is the source of truth: the spec standard and the interview guide.
- `prompts/` holds the five prompts. They are the only copy of the prompt text.
- `templates/` holds the blank SPEC and project brief.
- `index.html` carries static copies of the prompts and interview questions between `BEGIN` and `END` markers, so the page works without JavaScript.
- `assets/app.js` handles one step at a time, the current-step marker, and Copy prompt. It holds no prompt text.

## Changing a prompt or the interview guide

1. Edit the file in `prompts/` or `standard/INTERVIEW-GUIDE.md`.
2. Run `python3 scripts/sync-prompts.py --write`.
3. Run `bash scripts/check.sh`. It fails if `index.html` differs from the canonical files.

Never edit text between the markers in `index.html` by hand.

## Changing the standard

Update `standard/SPEC-STANDARD.md` first, then `templates/SPEC-TEMPLATE.md` and `prompts/03-create-spec.md`. `tests/test_methodology.py` fails when the section lists drift apart. Update the fixtures in `tests/fixtures/` if the expected results change.

## Checks

```bash
bash scripts/check.sh
bash scripts/check.sh --browser
```

The browser option needs Playwright for Python and Chromium. It runs the starter smoke test, the Marin Spec workflow test (`tests/browser_spec.py`), and the CSP test. Automated checks are not an accessibility audit. Review keyboard use, screen reader behavior, 200% zoom, and light and dark mode by hand.

## Automatic check

`.github/workflows/check.yml` runs `bash scripts/check.sh --browser` on every push and pull request to `main`, the same way `marin-links` does. It fails when `index.html` no longer matches `prompts/` or the interview guide, so a stale page cannot be merged. It has read-only access and uses no secrets.

## Security

`security.json` uses the `internal` profile. After a reviewed change, run `python3 scripts/sync-security-meta.py --write`. Marin Spec calls no outside service of its own, so `marin.yml` declares `services: none`.

## Updating the shell

Use the shell installer from a trusted `marin-app-shell` checkout, then set `platform.shell` in `marin.yml` to the installed version. Do not edit `vendor/marinos/`.

## Deployment

GitHub Pages at `https://marincountygov.github.io/marin-spec/`. Keep `.nojekyll`.
