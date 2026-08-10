.PHONY: run run-elaborate run-legal trace test benchmark benchmark-check retrieval-benchmark-check update-demo

PYTHON ?= python3

run:
	$(PYTHON) run_words_carry_weight.py

run-elaborate:
	$(PYTHON) -m elaborations.mml_elaborate_corpus

run-legal:
	$(PYTHON) -m elaborations.mml_legal_usecase

trace:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m elaborations.mml_trace_demo

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) benchmark.py --check >/dev/null

benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) benchmark.py --write

benchmark-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) benchmark.py --check

retrieval-benchmark-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) retrieval_benchmark.py --check

update-demo:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m elaborations.mml_update_demo
