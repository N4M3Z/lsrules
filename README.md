# lsrules

> Little Snitch 6 policy references and offline Python validators for repository agents. The repository contains no machine backup and applies no host changes.

## Install

Use Git and Python 3.11 or later. No package installation is necessary.

```sh
git clone https://github.com/N4M3Z/lsrules.git
cd lsrules
```

A normal clone does not initialize the [private submodule](docs/private-companion.md). Do not add `--recurse-submodules`.
Setup makes no firewall changes. Little Snitch 6 is necessary only for manual host changes.
Agents can use [INSTALL.md](INSTALL.md) for a verified setup.

## Usage

Run the offline checks from the repository root:

```sh
python3 -B scripts/check.py
python3 -B scripts/test_check.py
```

Both commands exit 0 on success. They run offline and do not change repository files.
With Make installed, `make validate` runs both commands.
Read [AGENTS.md](AGENTS.md) before agent work.

## Documentation

- [Reference](docs/reference.md): package scope, agent workflow, policy files, Work setup, list selection, and check limits.
- [Native workflow](docs/native-workflow.md): manual review in Little Snitch 6.
- [Private submodule](docs/private-companion.md): the private boundary and clone behavior.
- [Publication procedure](PUBLISHING.md): approval boundaries before a push.
- [Contributing](CONTRIBUTING.md): local tooling, public-file checks, and review conventions.
- [Template alignment](docs/skeleton-alignment.md): applicable skeleton parts and their limits.

## License

This package uses [EUPL-1.2](LICENSE). See the [third-party notices](THIRD_PARTY.md).
The package license does not license external blocklist contents or private companion data.
