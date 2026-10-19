# Repository template alignment

## Why

The repository uses the skeleton README shape but lacks its applicable maintenance tooling.
Contributors need consistent local checks without exposing private content or changing host settings.

## What Changes

- Adapt the base, Python, and tool templates from a fixed skeleton revision.
- Add explicit public-file lint targets, document schemas, contribution guidance, and local prek configuration.
- Add a read-only workflow for the existing offline package checks and regression tests.
- Preserve policy behavior, author privacy, the package license, and the private submodule boundary.

## Scope

This change adds repository tooling and narrowly required lint corrections.
It does not install tools, activate hooks, configure review services, or change firewall settings.
It does not authorize a commit or upload.

## Capabilities

### New Capabilities

- `offline-repository-tooling`: Check public repository files through explicit local targets and a restricted CI workflow.

### Modified Capabilities

None.
