# Contributing

Keep changes small and preserve rule scopes, identities, and private data boundaries.
Read [AGENTS.md](AGENTS.md) and the [policy reference](docs/reference.md) before changing rules.

Run the offline checks with Python 3.11 or later:

```sh
make validate
```

The Quality workflow runs the same checks without access to the private submodule.
The optional prek configuration runs validation and a staged secret scan.
Setup does not install hooks or tools. Existing signing and hook requirements still apply.

Use an identity listed in `authors.yaml` and a Conventional Commit subject.
Obtain approval for the exact commit and push, as described in [PUBLISHING.md](PUBLISHING.md).
Routine changes need no proposal, automated review service, or prose linter.
