# Experiment 4.2 - Semantic Navigation Strategy Comparison

## Result

Judgment: `UNIFORM_STRATEGY_EXPERIMENT_CONFORMANT`.

Every strategy started from the same 60-animal compiled state and was evaluated against the same 48 complete-signature equivalence classes under a uniform candidate prior. Random selection used 32 deterministic replicates.

## Open-Lens Comparison

| Strategy | Resolve target class | Questions | Residual entropy | Reduction/question | Ambiguous | Selected regret |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `information_gain` | 100.0% | 2.750 | 0.233 | 23.262 | 20.8% | 0.000 |
| `fixed_dimension_order` | 100.0% | 2.938 | 0.233 | 22.245 | 20.8% | 0.120 |
| `highest_cardinality_dimension` | 100.0% | 2.750 | 0.233 | 23.262 | 20.8% | 0.006 |
| `highest_coverage_dimension` | 100.0% | 2.938 | 0.233 | 22.245 | 20.8% | 0.120 |
| `random_eligible_dimension` | 100.0% | 3.087 | 0.233 | 20.962 | 20.8% | 0.355 |

Every treatment uses the same MML representation, compiled state, exact retrieval, ambiguity, and refusal contracts; only the injected next-question strategy changes.

The best other strategy by mean questions was `highest_cardinality_dimension`. Information gain minus that strategy was `0.000` questions and `0.000` residual-entropy bits.

Because every foundational record is complete, all dimensions have equal coverage. The highest-coverage strategy therefore falls back to frozen basis order and is behaviorally equivalent to fixed order in this treatment; coverage sensitivity remains for the partial-state expansion.

## Lens Results

| Lens | Strategy | Resolve target class | Questions | Residual entropy | Lens regret | Lens exhausted |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `ecological` | `information_gain` | 43.8% | 2.396 | 1.047 | 0.152 | 56.2% |
| `ecological` | `fixed_dimension_order` | 43.8% | 2.375 | 1.047 | 0.130 | 56.2% |
| `ecological` | `highest_cardinality_dimension` | 43.8% | 2.375 | 1.047 | 0.130 | 56.2% |
| `ecological` | `highest_coverage_dimension` | 43.8% | 2.375 | 1.047 | 0.130 | 56.2% |
| `ecological` | `random_eligible_dimension` | 43.8% | 2.677 | 1.047 | 0.073 | 56.2% |
| `behavioral` | `information_gain` | 12.5% | 1.750 | 2.332 | 0.574 | 87.5% |
| `behavioral` | `fixed_dimension_order` | 12.5% | 2.000 | 2.332 | 0.392 | 87.5% |
| `behavioral` | `highest_cardinality_dimension` | 12.5% | 1.750 | 2.332 | 0.574 | 87.5% |
| `behavioral` | `highest_coverage_dimension` | 12.5% | 2.000 | 2.332 | 0.392 | 87.5% |
| `behavioral` | `random_eligible_dimension` | 12.5% | 1.906 | 2.332 | 0.460 | 87.5% |

## Refusal And Ambiguity

All 3 unsupported combinations remained `UNSUPPORTED` (100.0%). Valid target trajectories never became unsupported. Terminal ambiguity represents genuine complete-signature equivalence classes or a lens that cannot express the remaining distinction; it is not forced into top-1 identification.

## Interpretation Boundary

This is a strategy ablation within one shared MML substrate: governed representation, compiled state, exact candidate composition, ambiguity, and refusal are common to every treatment. It does not compare MML with a non-MML system, learned priors, natural-language generation, an LLM strategy, or the partial multi-valued Canidae source state.

Non-uniform `IG(d | C, P)`, LLM-selected questions, comparisons with non-MML systems, and the partial multi-valued Canidae field are separately identified follow-on treatments.
