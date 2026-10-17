# lsrules

> Create a local offline reference checkout of lsrules. This setup does not activate firewall rules.

I want you to create a local offline reference checkout of lsrules. Execute the steps below in order. Stop and ask the user before any action outside these steps.

## OBJECTIVE

A public lsrules checkout exists in the `lsrules` directory, the setup did not initialize the private submodule, and the offline checks pass.

## DONE WHEN

`python3 -B scripts/check.py` and `python3 -B scripts/test_check.py` both exit 0 in the `lsrules` directory, and setup did not initialize the private submodule.

## TODO

- [ ] Verify Git and Python 3.11 or later
- [ ] Clone the public repository or verify the existing checkout
- [ ] Confirm the private submodule status
- [ ] Read `AGENTS.md`
- [ ] Run the offline validator and the regression tests

## Steps

1. Verify the prerequisites. Do not install a missing tool. Report it to the user and stop.

```sh
git --version
python3 -c 'import sys; print(sys.version); sys.exit(sys.version_info < (3, 11))'
```

2. Clone the public repository into a new `lsrules` directory. The clone is the only network step.

```sh
set -eu
expected=https://github.com/N4M3Z/lsrules.git
if [ -e lsrules ]; then
    prefix=$(git -C lsrules rev-parse --show-prefix)
    if [ -n "$prefix" ]; then
        echo "lsrules is not the root of a repository" >&2
        exit 1
    fi
    origin=$(git -C lsrules remote get-url origin)
    if [ "$origin" != "$expected" ]; then
        echo "unexpected origin: $origin" >&2
        exit 1
    fi
    git -C lsrules status --short
else
    git clone --no-recurse-submodules "$expected" lsrules
fi
```

If the script stops, report the message to the user and wait for instructions.
If `lsrules` already exists, keep all local changes. Do not pull, reset, switch branches, or delete files.
Report the status output to the user.

3. Confirm the private submodule status.

```sh
cd lsrules
git submodule status -- private
```

A leading `-` means that the submodule is not initialized. The public checks accept this state.
Do not run `git submodule update`. If the owner initialized the submodule earlier, leave it unchanged.
See the [private submodule](docs/private-companion.md) boundary.

4. Read `AGENTS.md` in the repository root. Apply its rules for the rest of the session.
Keep personal rules, addresses, credentials, and machine evidence outside public files.

5. Run the offline validator and the regression tests from the repository root.

```sh
python3 -B scripts/check.py
python3 -B scripts/test_check.py
```

Both commands exit 0 on success. The test output can show a test count. Do not expect a fixed number.
If a command fails, report its output to the user. Do not edit files to make a check pass.
The [reference](docs/reference.md) lists what the checks cover and what they cannot prove.

Setup ends after these steps. Do not import rules, subscribe to lists, change profiles, or run Little Snitch commands.
Little Snitch 6 is necessary only for later manual host changes with user approval. See the [native workflow](docs/native-workflow.md).

EXECUTE NOW: Complete the above TODO list to achieve: a local offline lsrules reference checkout with passing checks without initializing the private submodule.
