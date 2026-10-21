# Skeleton alignment

This repository selects useful parts of [runedeck/skeleton](https://github.com/runedeck/skeleton).
The source revision is `62e1f6674ac7c1d248d71eaa2660ebda600c3ef0`.
See [third-party notices](../THIRD_PARTY.md) for attribution.

The current adaptation keeps editor defaults, a small Makefile, functional CI, and the tool README structure.
[INSTALL.md](../INSTALL.md) uses the Mintlify agent-executable structure: objective, completion criteria, checklist, steps, and execution prompt.
Optional hooks retain package validation and secret scanning.

The 2026-10-21 simplification removes mandatory review agents, prose linting, document schemas, and their tool dependencies.
Routine changes do not require a proposal or review pipeline.
Older alignment and decision records remain as history.

Copier does not manage this repository. Review future template changes and copy only the relevant parts.
No setup command installs hooks, changes signing, or modifies Little Snitch.
