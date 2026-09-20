---
name: lsrules-release
description: Prepare a reviewed Little Snitch repository change for publication. USE WHEN staging a shareable package, checking release readiness, or preparing an approved commit, repository creation, or push. NOT FOR live firewall cleanup or upstream list research.
compatibility: Requires Python 3.11+ for offline checks. Publication tools require separate availability and authorized scope.
---

# lsrules-release

## Prerequisites

Use the selected local package and the user's requested destination and visibility.
Read repository `AGENTS.md`, its referenced rules, and `PUBLISHING.md`.
Preserve existing approval for the exact operation and change set.

## Constraints

Keep machine backups, private inventories, addresses, credentials, usage history, and executable fingerprints outside the package.
Do not include a personalized application allow inventory in the generic package.
Do not create a repository, commit, tag, release, or push without the required exact authorization.
Do not ask again when that exact authorization already exists and the scope has not changed.
Do not install dependencies, create runtime context, or restore a firewall backup as part of publication preparation.
A private repository does not supply an anonymously accessible raw subscription endpoint.

## Instructions

1. Inspect current files and repository state without changing Git history or remote state.
2. Prepare the complete local change set before requesting publication approval.
3. Keep profile JSON declarative. Keep any portable global example disabled and explicitly global.
4. Check source licenses and access terms. Keep upstream content out when redistribution remains unverified.
5. Run the offline validator and resolve structural, domain-safety, and privacy findings.
6. Request the canonical Daybreak adversary to review the exact local files independently.
7. Resolve confirmed findings and repeat only checks affected by the changes.
8. Review the complete publication set, including hidden agent files and generated caches.
9. Remove generated caches that can embed local paths. Preserve unrelated repository work.
10. Report file scope, validation, destination, visibility, license status, and material limits in a reviewable result.
11. Ask for the exact commit, repository creation, or push only when authorization is absent.
12. If authorized, use the native supported Git or hosting workflow and verify its resulting state.
13. Report local preparation, commit, repository creation, push, and release as separate outcomes.

## Verification

Run `python3 -B scripts/check.py` from the repository root.
Confirm the Daybreak model and sandbox from runtime evidence before claiming they were used.
Confirm that local checks did not create native firewall state or upload files.
Verify remote state after an authorized publication operation. A local package is not a pushed repository.

## Troubleshooting

If the native Daybreak adapter is unavailable, report that limit and dispatch the contract through an authorized supported mechanism.
If approval review blocks an action, preserve the exact proposed scope and explain the stated reason.
If the approved change set changes, identify the new difference before requesting authorization for it.
If the user moves the package, update repository pointers without copying private evidence into the new location.

## References

Use [native rule format](https://help.obdev.at/littlesnitch6/adv-lsrules-file-format) when checking publication semantics.
Use [remote rule groups](https://help.obdev.at/littlesnitch6/lsc-rulegroups) when explaining subscription requirements.
