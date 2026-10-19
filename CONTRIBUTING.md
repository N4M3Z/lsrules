# Contributing

## Start

Read [INSTALL.md](INSTALL.md) and [AGENTS.md](AGENTS.md).
Use a public clone without recursive submodule initialization.
Keep private data outside the public files.
See the [private boundary](docs/private-companion.md).

## Checks

Run `make validate` with Python 3.11 or later and Make.
It runs the existing offline package validator and regression tests.
It does not install dependencies or change host settings.

Run `make lint` with Ruff, Vale, rumdl, mdschema, and actionlint already installed.
The command fails when a required tool is absent.
It uses explicit public paths and leaves the private payload untouched.
Run `make quality` to execute both groups.

The normal Vale command retains the global rule layer.
The repository also contains pinned STE and Core styles for other environments.
Use `vale --no-global` only when you need to inspect the repository layer separately.

The `.pre-commit-config.yaml` file defines optional checks for prek.
It does not activate Git hooks.
No target installs tools or changes the repository hook configuration.
The whitespace hook can modify public files when you invoke prek.
Adopted documents and their provenance remain outside those automatic edits.

## Changes

Use `docs/changes/` for behavior changes under LSR-0001.
Preserve existing rule scopes, executable identities, and private boundaries.
Do not change native Little Snitch settings as part of repository maintenance.
See the [template alignment](docs/skeleton-alignment.md) before updating shared tooling.

## Git and review

Use a feature branch and Conventional Commit subjects.
Use an identity listed in `authors.yaml`.
Keep real names, personal email addresses, and host details out of public changes.
Get the required owner approval before a commit or upload.
See [PUBLISHING.md](PUBLISHING.md) for the exact approval boundary.

Use the pull request template to record scope, tests, and release notes.
The Quality workflow runs the offline Python checks on pushes and pull requests.
It does not run the optional local linters or initialize the private submodule.
This repository does not claim that branch protection or automated review services are configured.
