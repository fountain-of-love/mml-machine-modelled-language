.PHONY: run run-knowledge-state experiment-3 experiment-3-1 experiment-3-2 experiment-3-3 experiment-3-4 run-elaborate run-legal trace test benchmark benchmark-check knowledge-state-benchmark knowledge-state-benchmark-check experiment-3-1-benchmark experiment-3-1-check experiment-3-2-benchmark experiment-3-2-check experiment-3-3-benchmark experiment-3-3-check experiment-3-4-benchmark experiment-3-4-check retrieval-benchmark-check update-demo

PYTHON ?= python3

run:
	$(PYTHON) -m experiments.semantic_representation.demo

run-knowledge-state:
	$(PYTHON) -m experiments.knowledge_state_execution.demo

experiment-3:
	$(PYTHON) -m experiments.combinatorial_uniqueness.demo

experiment-3-1:
	$(PYTHON) -m experiments.combinatorial_uniqueness.run_direct_intersection

experiment-3-2:
	$(PYTHON) -m experiments.combinatorial_uniqueness.run_governed_legal_qualification

experiment-3-3:
	$(PYTHON) -m experiments.combinatorial_uniqueness.run_cross_level_transition

experiment-3-4:
	$(PYTHON) -m experiments.combinatorial_uniqueness.run_compositional_generalization

run-elaborate:
	$(PYTHON) -m elaborations.mml_elaborate_corpus

run-legal:
	$(PYTHON) -m elaborations.mml_legal_usecase

trace:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m elaborations.mml_trace_demo

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.semantic_representation.benchmark --check >/dev/null
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.knowledge_state_execution.benchmark --check >/dev/null
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.direct_intersection_benchmark --check >/dev/null
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.governed_legal_qualification_benchmark --check >/dev/null
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.cross_level_transition_benchmark --check >/dev/null
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.compositional_generalization_benchmark --check >/dev/null

benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.semantic_representation.benchmark --write

benchmark-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.semantic_representation.benchmark --check

knowledge-state-benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.knowledge_state_execution.benchmark --write

knowledge-state-benchmark-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.knowledge_state_execution.benchmark --check

experiment-3-1-benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.direct_intersection_benchmark --write

experiment-3-1-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.direct_intersection_benchmark --check

experiment-3-2-benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.governed_legal_qualification_benchmark --write

experiment-3-2-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.governed_legal_qualification_benchmark --check

experiment-3-3-benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.cross_level_transition_benchmark --write

experiment-3-3-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.cross_level_transition_benchmark --check

experiment-3-4-benchmark:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.compositional_generalization_benchmark --write

experiment-3-4-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m experiments.combinatorial_uniqueness.compositional_generalization_benchmark --check

retrieval-benchmark-check:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) retrieval_benchmark.py --check

update-demo:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m elaborations.mml_update_demo
