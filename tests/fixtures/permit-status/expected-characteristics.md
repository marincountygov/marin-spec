# Expected characteristics: permit status lookup

A good result:

- names residents, contractors, and front-desk staff as users
- states the problem as repeated status calls that take staff time
- marks the half-as-many-calls target as Confirmed, with the interview as source
- marks the inspector's name as an Open question or Inferred, not Confirmed
- marks "permits are public records" as Inferred or Open, and does not state it as a legal fact
- treats hiding the applicant phone number as Recommended or Open, not Confirmed
- identifies the missing access question: who may see which fields
- records that Permit Tracker has no API and a nightly CSV is the data source
- supports search by address, since callers rarely have a permit number
- does not add editing features, which the owner ruled out (Non-goals)
- does not invent a sign-in requirement
- picks a security profile, probably `public-web`, and labels it Recommended
- has no AI section, because the app does not use AI
- has testable acceptance criteria in given/when/then form
- lists the interview, the sample columns, the status values, and the call log as sources
- keeps the status values in Data or Content exactly as listed
- gives each requirement a priority of P1, P2, or P3
- writes user stories in the form "As a (user), I would like (feature) in order to (reason)"
- names who tests it and other stakeholders by role or team, not by person
- states the brief's Problem as a goal to accomplish, not as the solution to build
