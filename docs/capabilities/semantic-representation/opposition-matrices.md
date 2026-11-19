# Animal Opposition — Words Carry Weight in Seven Small Steps

> **The numbers in a cell are a representational decision. They decide what the mathematics can say.**

This demonstration shows, with ten animals and one relation, how very ordinary mathematics (a lookup, a negation, a matrix product, a comparison) becomes useful once meaning is written down explicitly. It also shows how such an explicit matrix can serve as a reference for checking relations that a model has *learned*.

Run it:

```bash
make run-opposition
```

Sources: [`relation_encoding.py`](../../../src/semantic_representation/relation_encoding.py) (runtime), [`opposition/`](../../../experiments/semantic_representation/opposition/) (stages, metrics, demo), [`animal_opposition_v1.json`](../../../data/demonstration/animal_opposition_v1.json) (governed fixture with a rationale per pair). Claims below are protected by [`test_opposition_matrices.py`](../../../tests/test_opposition_matrices.py).

## Starting intuition

A weight matrix transforms a starting coordinate into an ending one. Equality and opposition can then be two functions over the *same* matrix: `W_equal = I`, `W_opposite = -I`. The demonstration takes this literally and asks which representation of "opposite" makes it work.

## The governed relation

One signed matrix `S` is the canonical form: `-1` opposite (predator and prey, rivals), `0` neutral (no relation, e.g. bears and lions never meet), `+1` alike (the diagonal, and allied or same-kind animals). The two simpler matrices are **projections** of `S`, so what they lose is visible:

| Encoding | Definition | Can say | Cannot say |
| --- | --- | --- | --- |
| Binary | `B = [S <= -0.5]` | opposite / not | alike vs never-meet (both are 0) |
| Degree | `D = (1 - S) / 2` in [0, 1] | how opposite; 0.5 = neutral | nothing more than `S`: it is a rescaling |
| Signed | `S` in [-1, 1] | opposite / neutral / alike, graded | unknown vs explicitly neutral (both are 0) |

The last limitation is real. The matrix therefore carries an `asserted` mask beside its values. Stage 4 shows why this matters.

## The seven stages

1. **Binary.** `opposite_of(cat) = one_hot(cat) @ B` returns `dog, mouse`. A matrix-vector product *is* a lookup. Five "alike" pairs and thirty-five neutral pairs are all the same 0.
2. **Degree.** The same row becomes a ranking (`mouse 1.00, dog 0.80, ...`), and choosing a threshold becomes a decision.
3. **Signed.** One matrix, opposite functions: `alike(cat)` is the positive part of `S[cat]` (lion, tiger), `opposite(cat)` is the positive part of `-S[cat]` (mouse, dog). The intuition `W_opposite = -I` holds in this space and does not in the binary one. Information per pair grows from 0.50 bits (binary) to 0.99 bits (three states) to 1.54 bits (graded values).
4. **Composition.** `S @ S` multiplies signs, so the opposite of an opposite is alike. It proposes `dog-mouse +0.60` ("the enemy of my enemy"). It also **contradicts governance five times**, e.g. dog ~ wolf and wolf ↔ sheep yields dog ↔ sheep `-0.80`, while sheepdogs guard sheep. Tiger–zebra, explicitly governed as "never meet", would be inferred opposite. Composition only produces candidates; acceptance stays a governed decision.
5. **Validate learned weights.** A toy "learned" relation is built from 24 sentences by co-occurrence: the distributional signal trained models absorb at scale, but this is not an LLM. Checked against the governed matrix, its sign agrees on only **3 of 10** governed pairs, and its alike-vs-opposite AUC is **0.28** (below chance). Predators and prey share sentences, so co-occurrence makes them look alike (lion–zebra learned `+0.23`). This is the validation pattern in miniature: an explicit reference matrix turns "the weights seem fine" into per-cell, attributable verdicts.
6. **Evaluate.** On the binary task, the degree scale at threshold 0.5 and the signed scale at threshold 0 give **identical** sensitivity (0.40), specificity (0.25), precision (0.06), and AUC (0.270). On the three-state task, accuracy is 0.78 while macro-F1 is 0.29, because every uncalibrated learned score falls inside the neutral band and "everything is neutral" wins on accuracy.
7. **Cell types.** The same values stored as bool, three-state int8, int8×127, uint8×255, one-place decimal, float16, float32, and float64. Stored as uint8 on [0, 1], neutral (0.5) and the band edges (0.25, 0.75) are not representable: **4 of 45 governed pairs change state just by being stored**. Signed int8×127 keeps all 45. Bool and three-state storage flatten the learned scores to a single value (AUC 0.5). Floats are densest near 0: float16 resolves 6e-8 around a neutral at 0, but only 1e-3 around a neutral at 0.5.

## What this says about the range question

The intuition that the signed range "gives more room" is partly right, and the demonstration separates the parts:

- **Not the range itself.** A linear rescaling with a matching threshold leaves sensitivity, specificity, precision, and AUC unchanged (stage 6). [0, 1] with 0.5 and [-1, 1] with 0 are the same information.
- **The task.** A signed scale invites a three-state task with a measurable neutral state. That adds entropy, ambiguity, and new ways to fail (stage 6's accuracy trap), so it needs per-state and macro measures.
- **The cell type.** Where neutral sits interacts with the storage type: integer grids may miss the midpoint and band edges, and floats resolve far better around 0 than around 0.5 (stage 7). This is where "unimportant" choices change results.

## Boundary

Every value and sentence is authored for teaching (`AUTHORED_ILLUSTRATION`); none is zoological authority. The learned relation is a co-occurrence toy, not a trained model, so stage 5 demonstrates the *procedure* for validating learned weights, not a finding about any LLM. Thresholds (±0.5) are declared choices.

## Observations and next paths

The generated [Animal Opposition v1 report](results/opposition-matrices-v1.md) (`make opposition-report-check`) records the measurements in plain words first and raises two signals, each studied in its own report: [cell types](results/opposition-cell-types-v1.md) and [two tensions](results/opposition-two-tensions-v1.md). The observations and the paths they open:

1. **One scale holds two tensions.** Dog–mouse is alike by *interaction* (enemy of my enemy); lion–tiger is alike by *likeness* (same kind). In an exploratory decomposition, 4 of 5 composition conflicts cross these two axes. **Next path:** a two-axis space, interaction and likeness, each in [-1, 1], with a falsifiable prediction of which conflicts disappear.
2. **Training allows testing.** A governed matrix is a test oracle. With open weights, a probed relation can be tested for sensitivity, specificity, precision, macro-F1, and AUC on held-out pairs, then fine-tuned and re-tested in a loop. **Next path:** a train–test–tune protocol that also measures what is better executed than trained.

A smaller open step remains: store the `asserted` mask as an explicit fourth state (unknown) and evaluate it separately from neutral.
