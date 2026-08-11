.PHONY: run run-knowledge-state experiment-3-1 run-elaborate run-legal trace test benchmark benchmark-check knowledge-state-benchmark knowledge-state-benchmark-check experiment-3-1-benchmark experiment-3-1-check retrieval-benchmark-check update-demo

PYTHON ?= python3

run:
	$(PYTHON) run_words_carry_weight.py

run-knowledge-state:
	$(PYTHON) run_knowledge_is_state.py

experiment-3-1:
	$(PYTHON) run_experiment_3_1.py

run-elaborate:
	$(PYTHON) -m elaborations.mml_elaborate_corpus

run-legal:
	$(PYTHON) -m elaborations.mml_legal_usecase

trace:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m elaborations.mml_trace_demo

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) benchmark.py --check >/dev/null
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) knowledge_state_experiment.py --check >/dev/null
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) direct_combinatorial_intersection_experiment.py --check >/dev/null

benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) benchmark.py --write

benchmark-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) benchmark.py --check

knowledge-state-benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) knowledge_state_experiment.py --write

knowledge-state-benchmark-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) knowledge_state_experiment.py --check

experiment-3-1-benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) direct_combinatorial_intersection_experiment.py --write

experiment-3-1-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) direct_combinatorial_intersection_experiment.py --check

retrieval-benchmark-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) retrieval_benchmark.py --check

update-demo:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m elaborations.mml_update_demo
