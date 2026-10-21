# lsrules

> Little Snitch policy references: profile designs, a blocklist catalog, and a manual workflow to apply them.

The repository describes three profile designs: Trusted, Untrusted, and Work. The blocklist catalog lists source options to choose from. It is not an inventory of installed lists. Work domains are scoped by hand. An optional global deny rule is included as an example and stays disabled. You apply every change yourself in Little Snitch with the [native workflow](docs/native-workflow.md).

## Install

You need Git, Python 3.11 or later, and Make. The checks have no package dependencies.

```sh
git clone --no-recurse-submodules https://github.com/N4M3Z/lsrules.git
cd lsrules
```

The `private/` submodule points to a separate private repository and stays uninitialized. Agents can follow [INSTALL.md](INSTALL.md).

## Usage

```sh
make validate
```

This runs the Python checker and its tests offline. It changes nothing in Little Snitch.
See the [policy reference](docs/reference.md) for profile behavior, rule files, and blocklist choices.

## License

[EUPL-1.2](LICENSE). See [third-party notices](THIRD_PARTY.md).
The license does not cover external blocklist contents or private companion data.
