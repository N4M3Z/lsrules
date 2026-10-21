# lsrules

> Clone lsrules and run its offline checks.

I want you to set up a local lsrules checkout and run its offline checks. An existing checkout keeps its local changes, and setup installs no hooks, deploys nothing, and changes no firewall rules.

## OBJECTIVE

A local lsrules checkout passes `make validate`.

## DONE WHEN

`make validate` exits 0 in the `lsrules` directory.

## TODO

- [ ] Check Git, Make, and Python 3.11 or later
- [ ] Clone lsrules, or use the existing checkout
- [ ] Run `make validate`

## Steps

1. Check the tools. If one is missing or Python is older than 3.11, report it and stop.

```sh
git --version
make --version
python3 -c 'import sys; print(sys.version); sys.exit(sys.version_info < (3, 11))'
```

2. If `lsrules` does not exist, clone it without the private submodule. If it exists, use it as it is.

```sh
git clone --no-recurse-submodules https://github.com/N4M3Z/lsrules.git lsrules
```

3. Run the checks. They run offline. If they fail, report the output.

```sh
cd lsrules
make validate
```

EXECUTE NOW: Complete the above TODO list to achieve: a local lsrules checkout where `make validate` passes.
