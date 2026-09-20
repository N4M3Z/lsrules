---
name: lsrules-audit
description: Audit Little Snitch rules and profiles with native evidence. USE WHEN reviewing approved, unapproved, disabled, redundant, or changing-IP rules and profile behavior. NOT FOR researching upstream lists or creating commits, repositories, or pushes.
compatibility: Requires Python 3.11+ for offline checks. Native inspection requires an authorized macOS session.
---

# lsrules-audit

## Prerequisites

Use the requested scope, existing private evidence, and current native observations.
Read repository `AGENTS.md` and the referenced rules before starting.
Keep machine exports and identity fingerprints outside the repository.

## Constraints

Review annotations separately from traffic matching.
Do not treat an inactive profile as a disabled rule.
Preserve explicit denies, required ChatGPT transports, and stable vendor Code IDs.
Preserve user-created scopes unless the authorized cleanup explicitly changes them.
A helper identity exception must preserve the signed parent and its recorded connection scope.
Do not translate reverse DNS, recent use, or a valid signature into durable endpoint ownership.
Do not load dynamic context, install tools, or run network probes automatically.
Do not restore a complete backup to perform a narrow edit.

## Instructions

1. State whether the task requests inspection, a reviewed proposal, or authorized native changes.
2. Reuse a suitable existing backup. Verify its checksum and distinguish later GUI changes.
3. Do not repeat export or restore cycles when the available evidence answers the question.
4. Inspect approved, unapproved, protected, and disabled rules within the requested scope.
5. Record process, via helper, identity, action, direction, destination, protocol, ports, profile, and enabled state.
6. Verify covering rules before calling an allowance redundant. Preserve process and via distinctions.
7. Review disabled clutter separately. Retain useful containment and remove obsolete entries only within the authorized scope.
8. Classify IP scopes as protocol constants, verified service ranges, private bindings, or temporary session endpoints.
9. Replace temporary addresses only when current primary evidence supports a stable destination and required transport.
10. Check all-profile inheritance and native precedence before proposing profile restrictions or copying application rules.
11. Keep Work application access usable. A restriction-only profile is not a complete application baseline.
12. Select the main Rules app for authorized GUI work. Read fresh accessibility state after each mutation.
13. Treat native editor summaries as evidence. A displayed but uncommitted field does not prove a saved rule.
14. Use the Daybreak contract for an independent review of the exact proposal and its strongest counterargument.
15. Report applied changes, observed GUI state, exported state, runtime checks, and remaining uncertainty separately.

## Verification

Run `python3 -B scripts/check.py` from the repository root for offline artifact checks.
Confirm that deliberate denies and required ChatGPT scopes remain intact.
Use authorized representative workflows and native rule correlation when runtime evidence is needed.
Do not call a successful connection proof of executable integrity or every firewall decision.
Report current counts with their source. Label inferred native counts as inferred.

## Troubleshooting

If the Rules window is unavailable, reacquire the main app and current accessibility state before retrying.
If native input fails, use a bounded retry and report the limit. Do not open unrelated apps as a workaround.
If the user stops exports, retain the existing backup and report later GUI evidence separately.
If a CLI updates frequently, prefer its verified vendor Code ID or the user's documented helper exception.

## References

Use [rule semantics](https://help.obdev.at/littlesnitch6/concepts-rules) when evaluating matches and annotations.
Use [profiles](https://help.obdev.at/littlesnitch6/concepts-profiles) when evaluating inherited and local policy.
Use [code identity](https://help.obdev.at/littlesnitch6/adv-code-identity) when reviewing a process or helper.
