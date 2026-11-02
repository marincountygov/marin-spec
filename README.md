# Marin Spec

Marin Spec helps teams turn project discovery into clear, build-ready specifications for MarinOS projects.

It provides a standard interview, reusable prompts, a specification format, and a guided workflow for using tools such as Claude, ChatGPT, and Copilot. The app is a guide. It does not call an AI service, and it never receives your files.

- **Owner:** County of Marin
- **Audience:** Staff
- **Status:** Alpha
- **Repo:** marincountygov/marin-spec

## Workflow

1. **Prepare.** Gather project material and interview the project owner.
2. **Analyze.** Your AI tool reads the material and sorts what it finds.
3. **Resolve.** You answer the questions that change what gets built.
4. **Spec.** The tool writes `SPEC.md` and `PROJECT-BRIEF.md`. You also save a Word copy for your team to review.
5. **Review.** A new conversation checks the spec for gaps and unsupported assumptions.
6. **Build.** A coding agent builds from the spec.

Every fact carries one label: Confirmed, Inferred, Recommended, or Open question. Inferred and recommended items never become requirements without a person's answer.

## Repository

```text
standard/    SPEC-STANDARD.md, INTERVIEW-GUIDE.md (source of truth)
prompts/     01-analyze, 02-find-gaps, 03-create-spec, 04-review-spec, 05-build
templates/   SPEC-TEMPLATE.md, PROJECT-BRIEF-TEMPLATE.md
tests/       checks, plus fixtures/ with example projects
scripts/     check.sh, sync-prompts.py, sync-security-meta.py
index.html   the guide
```

## Use the prompts without the app

The prompts are plain Markdown files. To use them without the app:

1. Open a new conversation in your AI tool and upload your project files.
2. Paste `prompts/01-analyze.md` and send it.
3. Continue in the same conversation with `02-find-gaps.md` and `03-create-spec.md`.
4. Review in a new conversation with `04-review-spec.md`.
5. Give `SPEC.md` and `05-build.md` to your coding agent.

## How the pieces relate

The standard is the source of truth. The prompts, the app, and the `marin-spec` skill in [marin-skills](https://github.com/marincountygov/marin-skills) all point to it. The app copies the prompts into its page with `scripts/sync-prompts.py`; the check script fails if they differ. The skill does the same workflow in an AI agent without the app.

## Develop

```bash
python3 -m http.server 8765 --bind 127.0.0.1
bash scripts/check.sh
```

See [docs/development.md](docs/development.md).

## Accessibility

The target is WCAG 2.2 AA, using the MarinOS shell and its shared components. The app has had automated checks only, not an independent review. Prompts stay on the page as plain text.

## Security and privacy

Marin Spec:

- uploads nothing
- stores nothing
- needs no account
- asks for no API key

Files you give to an AI tool follow that tool's terms and the County's rules. See `security.json` and [SECURITY.md](SECURITY.md).

## AI use

Marin Spec provides prompts for outside AI tools. It never invokes a model or sends information to an AI service. `marin.yml` declares `ai: used: false`.

## Future

A later version could call an AI service directly. It would use the same standard, prompts, evidence labels, and outputs.

## License

MIT. See [LICENSE](LICENSE).
