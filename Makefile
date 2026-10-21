PYTHON ?= python3

.PHONY: help validate test

help:
	@echo "make validate  check public policy, privacy boundaries, links, and tests"
	@echo "make test      run the regression tests"

validate:
	$(PYTHON) -B scripts/check.py
	$(MAKE) test

test:
	$(PYTHON) -B scripts/test_check.py
