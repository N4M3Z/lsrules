# lsrules

Little Snitch policy references and review procedures for repository agents.
Start with [AGENTS.md](AGENTS.md) and [agent resources](.agents/README.md).
The package contains no machine backup and applies no host changes.

## OpenSpec planning

Behavior changes use the local `openspec/` root and the spec-driven workflow.
The first [proposal](openspec/changes/add-offline-cleanup-plan-audit/proposal.md) defines an offline cleanup-plan auditor.
Its [design](openspec/changes/add-offline-cleanup-plan-audit/design.md) explains evidence, scope, privacy, and verification limits.
These artifacts describe proposed behavior. The auditor is not implemented yet.

## Agent workflow

1. Use [lsrules-audit](.agents/skills/lsrules-audit/SKILL.md) for rules, profiles, disabled clutter, and changing-IP scope.
2. Use [lsrules-source-review](.agents/skills/lsrules-source-review/SKILL.md) before adopting upstream lists or tools.
3. Dispatch the [Daybreak adversary](.agents/agents/daybreak-adversary.md) to challenge the exact proposal independently.
4. Use [lsrules-release](.agents/skills/lsrules-release/SKILL.md) to prepare a checked package and complete authorized publication steps.

Source review precedes release when a change introduces an upstream source.
Skills provide procedures on demand. The rules under `.agents/rules/` provide the shared constraints.
The [Codex adapter](.codex/agents/daybreak-adversary.toml) configures the native Daybreak agent to read the canonical contract.
The Markdown contract does not dispatch itself or select a model by itself.
Check runtime evidence before claiming which model or sandbox performed a review.
Other harnesses require an explicit supported dispatch mechanism.

## Policy files

| File | Purpose |
| --- | --- |
| `rules/work-domains.json` | Domain source for a manually scoped Work rule |
| `profiles/policy.json` | Trusted, Untrusted, and Work profile designs |
| `catalog/blocklists.json` | Upstream links and selection notes |
| `rules/global-focus-disabled.lsrules` | Optional global deny example that starts disabled |
| `docs/identities.md` | Identity choices that survive application updates |
| `docs/native-workflow.md` | Native review, profile, and snapshot workflow |

## Work setup

Create Work in the native Rules window and leave it inactive during setup.
Create the social deny from `rules/work-domains.json` inside Work.
Set Any Process, Anyone, outgoing, any protocol, any port, and high priority.
Verify that the rule belongs only to Work before enabling it.
Review required application rules and the incoming boundary before activating Work in Alert mode.

Work uses its own rules and all-profile rules. It does not inherit Trusted or Untrusted.
VPN app identity does not establish which server is connected.
Use manual Work activation until the native selector proves the intended network identity.
See [profiles](https://help.obdev.at/littlesnitch6/concepts-profiles) and [networks](https://help.obdev.at/littlesnitch6/lsc-networks).

## Portable format boundary

`global-focus-disabled.lsrules` is a global example, not a Work profile installer.
Its sole rule has `disabled: true`.
The native format has no documented profile field.
The documented `.lsrules` workflow uses a remote HTTPS rule group. A local-file import workflow is not documented.
Remote groups remain global and protected.
A private GitHub repository does not provide an anonymously accessible raw subscription URL.
Do not place an access token in a rule-group URL or this package.
Use the manual Work source when only Work should block these domains.
See the [native rule format](https://help.obdev.at/littlesnitch6/adv-lsrules-file-format).

## List selection

Start with Peter Lowe for ads and tracking, plus URLhaus for malware destinations.
Verify current native catalog availability, update health, and URLhaus access requirements.
AdAway can remain a continuity choice beside Peter Lowe. Both overlap with larger general-purpose lists.
Consider StevenBlack or HaGezi Light as alternatives after false-positive review. Avoid stacking a larger list on both existing ad lists.
The catalog links upstream sources. It does not vendor or download their contents.
See [blocklists](https://help.obdev.at/littlesnitch6/concepts-blocklists) and [URLhaus access](https://urlhaus.abuse.ch/api/).

## Local checks

Use Python 3.11 or later. No package installation or external service is required.

```sh
python3 -B scripts/check.py
python3 -B scripts/test_check.py
```

The validator is offline and read-only. The regression tests use in-memory edits.
The checks cover policy safety, canonical skill structure, local references, and the allowed native adapter fields.
Frontmatter uses a restricted string-only YAML subset. The checker is not a general YAML parser.
Structural checks do not prove that prose is safe or that an agent obeys its instructions.
The Daybreak review must also assess instruction meaning and unsupported loading or enforcement claims.
A JSON check does not prove native import acceptance or effective rule precedence.
Test browsing, sign-in, mail, calls, DHCP, and VPN transitions in the selected profile.
Correlate blocked requests with native rule use before declaring enforcement verified.

See [publication status](PUBLISHING.md) before creating a repository or pushing these files.
