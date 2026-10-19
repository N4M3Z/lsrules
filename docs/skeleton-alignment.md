# Skeleton alignment

This repository adapts the base, Python, and tool templates from [runedeck/skeleton](https://github.com/runedeck/skeleton).
The source revision is `62e1f6674ac7c1d248d71eaa2660ebda600c3ef0`.
The adaptation date is 2026-10-18.
See [third-party notices](../THIRD_PARTY.md) for license and attribution.

## Applied parts

| Template part | Repository use |
| --- | --- |
| Base editor and line-ending configuration | Public text defaults, with private and adopted files excluded from normalization |
| Base Makefile | Offline validation, explicit public-file lint, schema checks, and help |
| Base prek configuration | Local checks without automatic hook activation or tool downloads |
| Base quality workflow | Public Python checks with read-only permissions and no private submodule checkout |
| Base contribution and pull request templates | Scope, privacy, validation, and release notes |
| Base installation and pull request schemas | Explicit `make schemas` checks |
| Base Vale configuration and styles | Local STE and Core snapshots, plus the normal global rule layer |
| Python lint configuration | Python 3.11 and the existing standard-library scripts |
| Tool README | Title, brief, installation, usage, and license |

## Adaptation limits

This is a selective adaptation.
Copier did not generate this repository.
There is no Copier answer file or automatic template update workflow.
Review future template changes against this source revision before copying them.

The package has no Python distribution or runtime dependencies.
Its lint configuration does not add packaging metadata or raise the Python minimum.
Long reviewed policy expressions retain their original line lengths.
The subprocess exceptions apply only to the validator's bounded local Git probes.

Vale styles are regular files copied from the committed template snapshot.
Their original comments describe how upstream generated them.
This repository does not include or invoke that generator.
Replace the snapshots only after reviewing the selected upstream revision and updating the attribution.
Do not change the privacy validator to accept unrelated digest fields.

The skeleton's installers, hook activation, signing keys, author roster, review services, and repository rulesets are not included.
Its host guard configuration and worktree cleanup commands are not included.
The existing authors file, license, agent resources, policy files, and private gitlink remain authoritative.

## Verification boundary

`make validate` uses only Python and Make.
`make lint` requires existing local tools and does not download them.
Lint targets use explicit public file lists rather than recursive repository scans.
The optional prek checks exclude the private payload and adopted evidence.
The staged secret scan still checks adopted evidence because it reads the public Git index.

The Quality workflow runs the Python validation and regression tests.
Local lint success does not establish remote CI success or native firewall enforcement.
No installation target activates hooks or changes host settings.
