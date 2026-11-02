You are helping a County of Marin team write a build-ready specification. This is the spec step.

Write two documents from everything in this conversation: the shared material, your analysis, and my answers.

Document 1: SPEC.md

Use these sections in this order:

1. Summary (project name, problem, users, desired outcome, project owner, who tests it (UAT) and other stakeholders by role or team, specification status)
2. Platform and delivery (staff or public, security profile: internal, public-web, public-api, authenticated, or custom)
3. Goals
4. Non-goals
5. Users (if the app serves the public, start with the public need)
6. User stories, with IDs US-001, US-002, and so on, in the form "As a (user), I would like (feature) in order to (reason)", one for each user group
7. Workflows
8. Requirements, with IDs REQ-001 and so on. For each: the requirement, priority (P1 must have and critical path, P2 should have, P3 nice to have and can be deferred), evidence status, source, related user story, and acceptance criteria IDs
9. Content (pages, headings, labels, instructions, alerts, empty states, error messages)
10. Data (entities, fields with a label of public, internal, personal, or sensitive, relationships, source systems, formats, APIs, ownership, retention)
11. Integrations
12. Accessibility (target WCAG 2.2 AA; refer to the County of Marin accessibility standard instead of copying it; list only project-specific needs)
13. Security (public and private information, authentication, authorization, roles, sensitive information, how personal information is handled, external APIs, secrets, logging, dependencies; refer to the County of Marin security standard)
14. AI (include only if the finished app itself uses AI)
15. Acceptance criteria, with IDs AC-001 and so on, each testable, in the form "Given (state), when (action), then (result)"
16. Open questions, each marked Blocking, Important, or Implementation decision
17. Sources

Document 2: PROJECT-BRIEF.md

Keep it short, in active voice and plain language. Use these sections: Project, Problem, Why this matters, Users, Experience, Scope, Not included, Key decisions, Deadlines, Key risks and mitigation, Open questions, Success. Leave out Deadlines and Key risks and mitigation when there are none.

Rules:

- Mark every requirement and decision Confirmed, Inferred, Recommended, or Open question.
- Do not turn an inferred or recommended item into a confirmed requirement.
- Do not put real people's personal information in either document. Refer to people by role and make up any example data.
- Do not invent requirements. If something is unknown, put it in Open questions.
- Do not invent security requirements the project or County standards do not support.
- Every requirement must trace to a user story or a stated project need.
- Avoid vague acceptance criteria such as "search works correctly."
- Do not renumber IDs once you assign them.
- Write the Problem in the brief as the underlying goal, not the solution. Back Why this matters with evidence from the material and label it Confirmed or Inferred.

Give me both documents as separate Markdown blocks I can copy into files. If you can create Word (.docx) files, also give me one download for each document. If you cannot, say so.
