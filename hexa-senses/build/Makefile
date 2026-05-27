# hexa-senses build/Makefile — verify/test/ci fan-out.

ROOT     := ..
PYTHON   ?= python3
HEXA     ?= /Users/ghost/.hx/bin/hexa
HX       ?= /Users/ghost/.hx/bin/hx

.PHONY: all verify verify-json test test-hexa selftest install-test ci everything help check clean

all: ci

verify:
	@cd $(ROOT) && $(PYTHON) verify/cli.py all

verify-json:
	@cd $(ROOT) && $(PYTHON) verify/cli.py all --json

test:
	@cd $(ROOT) && $(PYTHON) -m pytest tests/ -m auto -v

test-hexa:
	@cd $(ROOT) && $(PYTHON) -m pytest tests/ -m hexa -v

selftest:
	@cd $(ROOT) && HEXA_SENSES_ROOT=$$PWD $(HEXA) run cli/hexa-senses.hexa selftest

install-test:
	@$(HX) install $(ROOT) --entry cli/hexa-senses.hexa --as hexa-senses

ci: verify test
	@echo "  ✓ ci surface PASSED  —  hexa-senses"

everything: ci selftest
	@echo "  ✓ everything PASSED"

check:
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "MISSING: $(PYTHON)"; exit 1; }
	@$(PYTHON) --version
	@echo "OK"

clean:
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true

help:
	@echo "hexa-senses/build/Makefile targets:"
	@echo "  verify       run all verifiers"
	@echo "  verify-json  JSON output"
	@echo "  test         pytest -m auto"
	@echo "  selftest     cli/hexa-senses.hexa selftest"
	@echo "  ci           verify + test (default)"
	@echo "  everything   ci + selftest"
