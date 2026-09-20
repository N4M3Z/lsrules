## Why

Manual firewall review can confuse disabled clutter, active permissions, changing media endpoints, and unrelated shared rules.
The current package checks portable files, but it cannot justify a cleanup plan against the native rule evidence.

## What Changes

- Add an offline auditor for explicitly supplied private Little Snitch snapshots and proposed cleanup plans.
- Report disabled clutter, exact duplicates, and conservatively proven coverage as separate candidate classes.
- Assess each proposed edit with `accept`, `reject`, or `needs-evidence`, including the affected fields and evidence limits.
- Require explicit scope evidence for broader access, identity exceptions, and changes to protected workflows.
- Separate private audit details from an allowlisted public summary.
- Add synthetic adversarial cases and a Daybreak review procedure for audit decisions.

This first change produces reviewable plans and reports. It does not apply native rules, export snapshots, or restore firewall models.
It does not automate VPN activation, subscribe to blocklists, or publish a repository.

## Capabilities

### New Capabilities

- `snapshot-evidence-capture`: Bounded private snapshot input, exact rule fields, evidence provenance, and explicit unknown values.
- `cleanup-plan-audit`: Conservative candidate generation and deterministic review of proposed changes against scope constraints.
- `cleanup-audit-reporting`: Private decision reports, public summaries, and independent adversarial review evidence.

### Modified Capabilities

None. This project has no existing OpenSpec capability specifications.

## Impact

The change adds an offline Python audit module and command entrypoint, versioned input contracts, and synthetic tests.
It extends the audit skill and package checks while preserving the existing policy files and review commands.
Private evidence stays outside the repository. Existing Little Snitch settings remain outside the implementation scope.

Planning assumption: the first deliverable is the offline auditor suggested during this discussion.
The requirements and tasks remain a proposal until the user chooses implementation.
