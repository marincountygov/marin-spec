# Marin Spec standard

This is the source of truth for what a Marin Spec contains and how it is checked. The prompts, the `marin-spec` skill, and the Marin Spec app all point here. None of them restate it.

A Marin Spec is a build-ready description of a project. A coding agent can build from it without guessing the project's goals.

## Outputs

A Marin Spec run produces two files. Keep `SPEC.md` for the coding agent, and also save a copy in a format your team can read and comment on, such as a Word document, so the spec is documented for review:

- `SPEC.md`, the full build specification. Use `templates/SPEC-TEMPLATE.md`.
- `PROJECT-BRIEF.md`, a short plain-language summary for people. Use `templates/PROJECT-BRIEF-TEMPLATE.md`.

## Evidence rules

Every fact, requirement, and decision in a spec carries one of four statuses.

- **Confirmed.** The project material says so directly.
- **Inferred.** The material reasonably implies it but does not say it.
- **Recommended.** The author or a MarinOS standard suggests it.
- **Open question.** A decision is still needed.

Rules:

1. Never turn an inferred or recommended item into a confirmed one without a person's answer.
2. Cite a source for every confirmed item when one exists.
3. Keep open questions visible. Do not hide uncertainty by inventing a requirement.
4. Do not infer that the built app uses AI just because AI helped build it.
5. Do not put real personal information about individuals in a spec or brief. Refer to people by role and make up any example data.

## Question classes

When gaps are found, sort each one:

- **Blocking.** The project cannot reasonably proceed without an answer.
- **Important.** The project can proceed, but the team should decide.
- **Implementation decision.** A developer or coding agent can reasonably decide while building.

Do not ask project owners technical questions that belong in the third class. The goal is to gather enough information to build confidently, not to document every choice.

## Stable IDs

Use these ID formats. Never renumber an ID after it appears in a draft. Retire it instead.

- `US-001` for user stories
- `REQ-001` for requirements
- `AC-001` for acceptance criteria

## SPEC.md structure

Use these sections in this order. Leave out a section only where this standard says it is conditional.

### 1. Summary

Project name, problem, users, desired outcome, project owner, who tests it before it goes live (UAT), other stakeholders, and specification status (draft, in review, approved). Name testers and stakeholders by role or team, not by person.

### 2. Platform and delivery

Say who the app is for (staff or public). Name the security profile from `marin-digital-standards/security/profiles.md`: `internal`, `public-web`, `public-api`, `authenticated`, or `custom`. Mark each answer with an evidence status.

### 3. Goals

What the project should accomplish.

### 4. Non-goals

What the project will not address. This section is required. Coding agents use it to avoid scope creep.

### 5. Users

Primary, secondary, internal, and administrator users. Include only the categories that apply. Describe what each group needs, not an elaborate persona. If the app serves the public, start with the public need.

### 6. User stories

Each story has an ID and follows the form "As a (user), I would like (feature) in order to (reason)." Write one story for each user group the project serves.

### 7. Workflows

The major user flows, in implementation-neutral terms. For example: Search, Results, Project, Status.

### 8. Requirements

Each requirement has:

- an ID
- the requirement itself
- priority: P1 (must have, critical path), P2 (should have, the best experience), or P3 (nice to have, can be deferred if it is too complicated)
- evidence status
- source, when one exists
- the related user story
- acceptance criteria IDs

Every requirement must trace to a user story or a stated project need. If it does not, it is a candidate for removal.

### 9. Content

Pages, headings, labels, instructions, alerts, empty states, and error messages. Apply the Marin content standards in `marin-digital-standards/content-design`.

### 10. Data

Entities, fields, relationships, source systems, formats, APIs, schemas, ownership, and retention. Label each field public, internal, personal, or sensitive. Prefer established standards such as Schema.org and SchemaGov where they fit.

### 11. Integrations

Every system the project depends on or talks to, and what flows each way.

### 12. Accessibility

The target is WCAG 2.2 AA. Reference the Marin accessibility standard in `marin-digital-standards/accessibility`. Do not copy it. List only project-specific accessibility needs, such as a map, a chart, or a complex form.

### 13. Security

Say what is public and what is private. Cover authentication, authorization, roles, sensitive information, external APIs, secrets, logging, and dependencies. For each personal-data field, say who can see it, how long it is kept, and whether it is shown. Reference `marin-digital-standards/security`. Do not invent security requirements that neither the project nor a Marin standard supports.

### 14. AI (conditional)

Include this section only when the built app uses AI. Cover purpose, service or model where known, inputs, outputs, data sent to AI, human review, failure behavior, and fallback behavior.

### 15. Acceptance criteria

Each criterion has an ID and can be tested. Prefer the form "Given (state), when (action), then (result)."

Weak: "Search works correctly."

Strong: "Given a user enters a valid address, when matching projects exist, the system shows the matching projects."

### 16. Open questions

Unresolved decisions, each with its question class and an owner when known.

### 17. Sources

Every document, link, and conversation used to write the spec.

## PROJECT-BRIEF.md structure

The brief is short. Use active voice and plain language. Sections: Project, Problem, Why this matters, Users, Experience, Scope, Not included, Key decisions, Deadlines, Key risks and mitigation, Open questions, and Success.

Write the Problem as the underlying goal, not the solution. Weak: "We want to add a search box." Strong: "Residents cannot find the permit status they need, so they call staff. We want them to find it themselves."

Back Why this matters with evidence, such as survey results, usage data, or a policy or leadership driver, and label each point Confirmed or Inferred. Deadlines and Key risks and mitigation are optional. Leave them out when there are none.

## Review criteria

A spec is ready for a coding agent when a review finds none of these:

- unsupported assumptions
- missing user needs
- missing requirements
- conflicting requirements
- vague requirements
- vague acceptance criteria
- requirements with no clear user or project need
- unresolved blocking decisions
- accessibility gaps
- security gaps
- real personal information about individuals
- personal-data fields with no decision on access, retention, or display
- data gaps
- integration gaps
- scope creep
- duplicated requirements

Review first lists material issues. It does not rewrite the spec until a person has resolved them.

## Building from a spec

For a MarinOS app, the coding agent starts from `marin-app-template` and follows `marin-skills/marin-app-builder`. The spec says what to build. MarinOS standards and the template decide how it looks and behaves, unless the spec records a justified exception.
