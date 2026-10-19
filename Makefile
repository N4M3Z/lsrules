PYTHON ?= python3
PYTHON_FILES = scripts/check.py scripts/test_check.py
PROSE_FILES = README.md INSTALL.md CONTRIBUTING.md PUBLISHING.md THIRD_PARTY.md \
	docs/reference.md docs/cleanup-method.md docs/native-workflow.md \
	docs/identities.md docs/private-companion.md docs/skeleton-alignment.md \
	.github/PULL_REQUEST_TEMPLATE.md \
	docs/changes/align-repository-skeleton/proposal.md \
	docs/changes/align-repository-skeleton/tasks.md \
	docs/changes/align-repository-skeleton/record.md \
	docs/changes/align-repository-skeleton/specs/offline-repository-tooling/spec.md

.PHONY: help validate test lint lint-python lint-docs lint-workflows schemas quality

help:
	@echo "make validate  run the offline package checks and regression tests"
	@echo "make lint      run the installed public-file linters and schemas"
	@echo "make quality   run validation and lint checks"
	@echo "No target installs tools, activates hooks, or changes firewall settings."

validate:
	$(PYTHON) -B scripts/check.py
	$(MAKE) test

test:
	$(PYTHON) -B scripts/test_check.py

lint: lint-python lint-docs lint-workflows schemas

lint-python:
	ruff check --no-cache $(PYTHON_FILES)

lint-docs:
	vale --no-wrap $(PROSE_FILES)
	rumdl check --no-cache $(PROSE_FILES)

lint-workflows:
	actionlint .github/workflows/quality.yaml

schemas:
	mdschema --schema schemas/INSTALL.mdschema check INSTALL.md
	mdschema --schema schemas/PULL_REQUEST.mdschema check .github/PULL_REQUEST_TEMPLATE.md

quality: validate lint
