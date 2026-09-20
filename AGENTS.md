# Repository agent guidance

This repository contains public Little Snitch policy references and offline validators.

Read `.agents/README.md` before you change policy files.
Apply all rules in `.agents/rules/`.
Use `.agents/agents/daybreak-adversary.md` for an independent adversarial review.
Use `.agents/skills/lsrules-audit/SKILL.md` for policy audits.
Use `.agents/skills/lsrules-source-review/SKILL.md` for source reviews.
Use `.agents/skills/lsrules-release/SKILL.md` for release preparation.

Use the local `docs/` spec root for behavior changes (LSR-0001).
Read the relevant change artifacts under `docs/changes/` before proposing or implementing a change.
Keep proposed requirements in change specs until implementation and verification are complete.
An OpenSpec proposal does not establish that a capability exists or that implementation has been authorized.

Keep private backups, host metadata, credentials, personal addresses, and local executable hashes outside this repository.
Do not change live Little Snitch settings from this repository.
Do not run external tests automatically.

User approval for a scope persists until the user changes it.
Ask before the exact commit, repository creation, or push.
Treat local files, commits, repositories, pushes, and releases as separate states.
