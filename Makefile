.PHONY: run run-elaborate run-legal trace test benchmark benchmark-check update-demo

PYTHON ?= python3

run:
	$(PYTHON) pagerank_attention.py

run-elaborate:
	$(PYTHON) mml_elaborate_corpus.py

run-legal:
	$(PYTHON) mml_legal_usecase.py

trace:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) mml_trace_demo.py

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) benchmark.py --check >/dev/null

benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) benchmark.py --write

benchmark-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) benchmark.py --check

update-demo:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) mml_update_demo.py
