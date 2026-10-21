# Private companion

[`N4M3Z/lsrules-private`](https://github.com/N4M3Z/lsrules-private) holds personal policy and scoped review records.
It is the optional `private/` submodule of this public repository.
The parent exposes its URL and selected commit. GitHub access controls protect its contents.
The public EUPL license does not license private companion data.

## Use

Public clones and checks work without private access:

```sh
git clone --no-recurse-submodules https://github.com/N4M3Z/lsrules.git
```

An owner with private access can initialize the companion from the public checkout:

```sh
git submodule update --init -- private
```

Use existing Git authentication. Never add credentials to the submodule URL.
The private repository has its own README and installation guide.

## Data boundary

Keep reusable policy and procedures in the public parent.
Keep approved personal rules and scoped review records in the private repository.
Keep native backups and detailed machine evidence local. Store credentials in neither repository.
The private policy is a reference, not a native backup or import file.

The public validator verifies the submodule declaration and local metadata before excluding its contents.
It rejects unexpected URLs, paths, symlinks, and ordinary directories presented as submodules.
An absent checkout validates the declaration only. Verify the child commit separately before publication.
Push an approved private update before updating the public pointer. See [publishing](../PUBLISHING.md).
