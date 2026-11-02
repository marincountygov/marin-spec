# Expected characteristics: equipment checkout tracker

A good result:

- names supervisors, crew members, and the admin as users
- states the problem as items going missing with no record of who held them
- records the fall audit as a Confirmed deadline, without inventing a date
- marks "who is told about late items" as an Open question, probably Important
- marks the County directory as the wanted source of names, and flags the unknown access method as Open
- puts the missing-item prediction idea in Non-goals or Open questions, and does not add an AI section
- does not infer AI use from the suggestion alone
- identifies the access question: what crew members may see and whether they see only their own items
- chooses between `internal` and `authenticated` security profiles and labels the choice Recommended or Open
- treats the week-late threshold as Confirmed, with the interview as source
- keeps item types and sign-out columns as listed
- has requirements that each trace to a user story
- has testable acceptance criteria, for example for marking an item returned
- lists the interview, the sheet columns, the item types, and the audit note as sources
- leaves implementation choices, such as storage, to the builder
- gives each requirement a priority of P1, P2, or P3
- writes user stories in the form "As a (user), I would like (feature) in order to (reason)"
- names who tests it and other stakeholders by role or team, not by person
- states the brief's Problem as a goal to accomplish, not as the solution to build
