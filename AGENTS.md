# Repository guidance

This repository holds public Little Snitch policy references and offline checks.
Read [docs/reference.md](docs/reference.md) for the policy and [CONTRIBUTING.md](CONTRIBUTING.md) for changes.

Keep personal addresses, host names, account data, executable fingerprints, and backups outside public files.
Private policy belongs in the separately controlled `private/` submodule.
Credentials belong in neither repository.
Public validation and archives must exclude private payload files after verifying the submodule boundary.

Prefer targeted rules. Compare process, parent, destination, protocol, port, action, direction, and profile separately.
Preserve existing scopes and identities unless the user authorizes a change.
Preserve documented development exceptions, including the Zed Dev exception.
Never disable identity checks or allow all connections as a blanket repair.
Never weaken ChatGPT access without an explicit request.
A remote subscription is global. Do not describe it as a Work-only rule.
See [identity guidance](docs/identities.md) for signed software and unsigned helpers.

Repository maintenance does not authorize live firewall changes or network probes.
A native export records configuration. Runtime traffic records observed connections.
An Unapproved marker does not change rule matching.
Do not claim native acceptance or enforcement from repository checks alone.

Run `make validate` after changes. Keep upstream attribution and digest-bound evidence intact.
Routine changes need no proposal, mandatory review model, or prose linter.
The older records in `docs/changes/` and `docs/decisions/` remain historical references.
Use an identity from `authors.yaml` and preserve commit signing and hooks.
Obtain approval for the exact commit and push. Existing approval for that scope remains valid.
