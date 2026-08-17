# Experiment 4.1 - Compiled Encyclopedic Navigation

**Status:** accumulated-capability implementation blueprint; prompt-provided seed implemented  
**Research stream:** Programme 4 - Semantic Navigation  
**Operation:** exact multidimensional retrieval and navigation over persistent governed semantic state  
**Primary claim:** the first three MML capabilities can accumulate into an inspectable navigation substrate that retrieves exact candidate regions, exposes remaining ambiguity, and recommends useful next distinctions

## Capability Chain Under Test

Experiment 4.1 executes one explicit operational chain:

```text
Semantic Representation
    governed animal identities
    recurring dimension/value coordinates
    stable compact codes
            |
            v
Knowledge State Execution
    compile once
    immutable postings
    signature equivalence classes
    content-addressed snapshots
            |
            v
Combinatorial Uniqueness
    exact coordinate intersection
    candidate-region narrowing
    unsupported-region preservation
            |
            v
Semantic Navigation
    identifiable / ambiguous / unsupported
    deterministic imputation
    remaining distinctions
    next information-gain question
    commonality
```

The experiment must record the operational identity of every layer. A local benchmark-only reimplementation does not satisfy this contract.

## Experimental World

The initial fixture is a controlled animal encyclopaedia. Animal identity is the entity being retrieved; habitat, diet, activity, and sociality form the reusable semantic basis.

```text
animal identity
    <- habitat
    <- diet
    <- activity
    <- sociality
```

Each dimension has a governed finite vocabulary whose values recur across many entities. Dimension-qualified coordinates prevent accidental collisions:

```text
habitat:woodland
diet:omnivore
activity:nocturnal
sociality:solitary
```

## Query Boundary

The engine receives governed structured coordinates. Natural-language interaction is upstream:

```text
user prompt
    -> separately evaluated semantic parser
    -> governed structured query
    -> Experiment 4.1 execution chain
```

The seed uses oracle structured queries. Parser errors must never be attributed to the navigation engine.

## Required Outcomes

1. **Exact retrieval:** every non-empty subset query returns exactly the compatible candidate region.
2. **Cardinality status:** one candidate is `IDENTIFIABLE`, several are `AMBIGUOUS`, and none is `UNSUPPORTED`.
3. **Incomplete-state diagnosis:** construction reports required semantic fields absent from governed records.
4. **Deterministic imputation:** a missing query dimension is imputed only when every candidate shares one non-missing value.
5. **Identification depth:** report the minimum available dimensions required to isolate every complete-signature equivalence class.
6. **Next question:** choose the unobserved dimension with maximum explicit partition information gain under deterministic ties, exposing prior entropy, expected posterior entropy, normalized gain, and missingness for every eligible dimension.
7. **Commonality:** return dimensions and values shared by every member of a selected set.
8. **Code equivalence:** governed labels and compact codes produce identical regions and navigation.
9. **Compiled reuse:** report compilation, warm query, flat scan, per-query reconstruction, storage, and amortization separately.

## Contribution Controls

| Treatment | Isolates |
| --- | --- |
| Unqualified/raw value sham | Whether dimension-qualified semantic representation prevents collisions and preserves explicit meaning |
| Semantic labels versus stable codes | Whether execution projection preserves represented meaning exactly |
| Flat record scan | Correctness parity and repeated work without compiled state |
| Reconstructed index per query | Knowledge State Execution contribution from persistent reuse |
| One coordinate and progressive subsets | Candidate narrowing contributed by coordinate composition |
| Redundant coordinate | Whether adding no independent information leaves the region unchanged |
| Full candidate region versus forced top-1 | Whether navigation preserves genuine ambiguity |
| Navigation ablation | What status, imputation, partitions, commonality, and next-question logic add beyond retrieval |

The current seed implements label/code, flat-scan, reconstruction, progressive subset, ambiguity, and navigation controls. The raw-value collision and explicit redundant-coordinate treatments remain required for the independently frozen version.

## Query Suite

Generate every distinct non-empty dimension subset represented by the frozen records. Add unsupported combinations composed only of individually valid values. Keep incomplete construction probes outside the canonical candidate universe.

| Query class | Expected behavior |
| --- | --- |
| Complete unique | One candidate; `IDENTIFIABLE` |
| Complete equivalence class | Complete compatible class; `AMBIGUOUS` |
| One missing | Exact region plus remaining partitions and possible imputations |
| Multiple missing | Broader exact region plus highest-information next dimension |
| Unsupported | Empty region; `UNSUPPORTED` |
| Incomplete construction record | Explicit missing-field diagnostic |

## Measurements

Report:

- exact-set accuracy, precision, recall, and Jaccard similarity;
- status and unsupported-refusal accuracy;
- deterministic-imputation precision and coverage;
- next-dimension information-gain correctness;
- commonality accuracy;
- semantic-label/code equivalence;
- complete-signature equivalence-class distribution;
- minimum identifying dimension count and unresolvable identity rate;
- representation snapshot, knowledge-state snapshot, and operator identities;
- source reads, postings writes, signature writes, coordinate lookups, postings inspected, intersections, and materializations;
- flat-scan and per-query-reconstruction work;
- stored-state size and compilation amortization; and
- wall-clock and memory measurements in the independently frozen study.

MRR and target margin are not primary metrics. An equivalence class is a correct semantic region, not a ranking failure.

## Scaling Protocol

Execute independently frozen and reviewed datasets at 100, 250, and 500 animals. Increase real near-neighbour density and expand into the governed dimension pool defined by Experiment 4.2. Report cold and warm costs separately over reuse horizons sufficient to cross or fail the measured amortization point.

The completed mechanics seed uses the default all-dimensions lens. [Experiment 4.2](dimension-contribution-experiment.md) defines explicit entropy accounting, overlapping user lenses, and dimension-contribution statistics for the larger states.

## Success Criteria

The mechanics seed conforms when:

1. all structured queries return the exact region and status;
2. all navigation diagnostics match an independent oracle;
3. label and code execution are equivalent;
4. incomplete construction records are detected;
5. all execution passes through the shared Programme 1, 2, and 3 operational contracts;
6. compiled and reconstructed execution are behaviorally equivalent; and
7. compiled warm execution uses fewer deterministic operations than flat scanning over the declared workload.

## Failure Criteria

The accumulated proposition is weakened if any upstream meaning is lost between layers, compiled state changes behavior, intersection omits compatible candidates, ambiguity is forced into one identity, navigation invents imputations, code projection drifts, or compilation fails to amortize under realistic repeated use.

## Evidence Boundary

The current animal fixture is prompt-provided and suitable only for mechanics. Experiment 4.1 does not test natural-language understanding or relational inference. Relations between dimensions or entities and derivation of facts absent from the indexed records require a separate research stream or follow-up experiment with structural holdout and equal-information controls.
