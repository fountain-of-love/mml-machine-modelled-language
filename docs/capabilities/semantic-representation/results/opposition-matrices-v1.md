# Animal Opposition v1 — OSCARC Report

> **The numbers in a cell are a representational decision. They decide what the mathematics can say.**

## Research intention

Some animals are enemies, like a cat and a mouse. Some are alike, like a lion and a tiger. Some never meet at all, like a bear and a lion. We wrote facts like these down as a table, one number for every pair of animals, and asked two questions. If the facts are written down clearly, can a computer answer simple questions with nothing more than school arithmetic? And can the same table be used to check what a computer has picked up on its own by reading sentences?

Technically: show with one governed relation how ordinary mathematics (lookup, negation, matrix product, comparison) becomes useful once meaning is explicit; how encoding, range, and cell type change what can be expressed and measured; and how an explicit matrix can act as a test oracle for a learned relation. Walkthrough: [Animal Opposition](../opposition-matrices.md), run with `make run-opposition`.

## Executive interpretation

The simple questions work. Ask the table for the cat's enemies and it says mouse and dog; ask who is like the cat and it says lion and tiger. The arithmetic can also suggest new ideas: the dog and the mouse share an enemy, the cat, so perhaps they are on the same side. But it sometimes suggests nonsense too, so a person still has to decide. The computer that learned from sentences got 7 of 10 checked pairs wrong. For example, it thought the lion and the zebra were alike, simply because they show up in the same stories. The table caught that.

All declared mechanism checks held (`MECHANISM_CONFORMANT`). The fixture is an authored illustration over 10 animals, so this is a teaching result about mechanisms, not evidence about animals or any trained model. Two signals emerged and have their own reports: storage type changes meaning, and one scale holds two tensions.

The rest of this report shows the evidence behind that summary in six short steps called OSCARC. After that, two signals point to deeper studies in separate reports. It ends with the next paths worth following.

## OSCARC

OSCARC moves in a fixed order: what was seen (**O**), what was expected beforehand (**S**), how and in which order it was done (**C**), what was actually changed or applied (**A**), what came out (**R**), and the judgment that compares the outcome with the expectation (**C**). Each step starts in everyday words and then gives the technical detail.

### O — Objective observation

Written as plain yes or no, the table only knows that the cat and the mouse are enemies. It cannot say that the lion and the tiger are alike, or that the bear and the lion never meet: both are just no. Written with numbers from minus one to plus one, it can say all three.

Over 45 distinct pairs, the binary projection kept 5 opposite pairs and merged 5 alike pairs with 35 neutral ones. Information per pair: 0.50 bits (binary), 0.99 bits (three states), 1.54 bits (graded). Two-hop composition produced 13 candidates (the 3 strongest are listed in the JSON) and 5 conflicts with governed pairs. The toy learned relation agreed in sign with 3 of 10 governed pairs. No interpretation is made here.

### S — Standard, baseline, or reference model

Before looking at the results we wrote down what should happen, like a checklist. The simpler tables should forget things on purpose. One table should answer both who is the cat's enemy and who is like the cat. Guesses made by arithmetic must stay guesses. Changing the scale from 0 to 1 into minus one to plus one should not, by itself, change any score.

The reference is the governed signed matrix in [`animal_opposition_v1.json`](../../../../data/demonstration/animal_opposition_v1.json), with a rationale per pair and a mask separating stated neutrality from unstated pairs. The declared mechanism expectations are the conformity criteria listed under the final step.

### C — Context and chronology

We started with one table of numbers. From it we made the simpler yes-or-no and 0-to-1 versions. Then we asked questions about the cat, combined facts in two steps, and finally checked a version learned from 24 short sentences against the table.

```text
governed signed matrix S -> binary B and degree D projections
  -> lookup, polarity, and S @ S composition
  -> toy learned relation from 24 sentences -> per-cell validation and IR measures
```

Values and sentences are authored for teaching; thresholds of ±0.5 are declared choices.

### A — Actions, interventions, or observed mechanisms

Flipping the sign of a number turns alike into enemy. So the same table answers both questions: read it as it is to find who is like the cat, read it flipped to find the cat's enemies. Combining two steps works like the saying the enemy of my enemy is my friend.

Binary and degree matrices are computed from `S`, never authored separately. Composition multiplies signs, so the opposite of an opposite becomes alike; results stay `CANDIDATE_NOT_GOVERNED`. The learned relation is the cosine of mean-centred co-occurrence vectors: a stand-in for trained weights, not an LLM.

### R — Result, effect, or measured outcome

The 0-to-1 scale and the minus-one-to-plus-one scale gave exactly the same scores for the learned version, so the range alone changed nothing. What did matter was the question we asked. Once never meet became its own answer, the learned version looked good on simple accuracy, because it called every pair never meet, while it actually found none of the enemies or look-alikes.

| Treatment | Sensitivity | Specificity | Precision | AUC |
| --- | ---: | ---: | ---: | ---: |
| Degree scale, >= 0.5 | 0.40 | 0.25 | 0.06 | 0.270 |
| Signed scale, <= 0 | 0.40 | 0.25 | 0.06 | 0.270 |

Three-state task: accuracy 0.78, macro-F1 0.29; 45/45 learned values lie in the neutral band. Alike-versus-opposite AUC of the learned relation: 0.28.

### C — Comparative assessment and research conclusion

Everything behaved as expected for a demonstration. But we made up the animals' numbers ourselves, so this shows how the method works. It does not prove anything about real animals or about real artificial intelligence.

**Conformity judgment: `MECHANISM_CONFORMANT`.**

- `projections_lose_declared_distinctions`: `True`
- `entropy_grows_binary_to_signed`: `True`
- `one_matrix_answers_both_polarities`: `True`
- `composition_only_proposes`: `True`
- `linear_rescaling_preserves_measures`: `True`
- `learned_relation_checked_per_cell`: `True`

**Evidence strength: `ILLUSTRATIVE`.** Values and sentences are authored and the learned relation is a toy, so the report establishes mechanisms and next questions only.

## Signals for deeper study

Some findings deserve a closer look than one section can give. Each signal below is explained briefly here and studied in its own report.

### Signal 1 — The storage type changes meaning

How a number is stored matters, like a till that only takes whole euros. Our table puts never meet exactly in the middle. Saved as whole numbers from 0 to 255, that middle cannot be stored, and four pairs quietly change their meaning.

Deeper study: [Opposition Cell Types v1](opposition-cell-types-v1.md).

### Signal 2 — One scale holds two tensions

Alike means two different things here. The dog and the mouse are on the same side because they share an enemy, the cat. The lion and the tiger are alike because they are the same kind of animal. When the arithmetic mixes these two, it makes most of its mistakes: 4 of 5.

Deeper study: [Opposition Two Tensions v1](opposition-two-tensions-v1.md).

## Next paths

Two next steps follow. First, give the table two separate scales: one for how two animals get along, one for how similar they are. Second, use the table as an exam for a real AI whose inside we can look at, retrain it until it passes, and keep checking that it learned rather than memorised the answers.

### Path 1 — Two axes: interaction and likeness

Separate interaction from likeness, each in [-1, 1], and compose within an axis. The falsifiable prediction and protocol are in the [two-tensions report](opposition-two-tensions-v1.md).

### Path 2 — Train, test, tune: governed matrices as tests for open weights

- **Hypothesis.** A governed relation matrix can act as a test suite for a model with open weights, and a fine-tune-and-retest loop can raise held-out test scores without regressing unrelated behaviour.
- **Protocol.** (1) Split governed pairs into training and held-out sets, by pair and by animal. (2) Probe an open model for the relation (embedding probe, or scored prompts with token log-probabilities) and freeze the probe. (3) Write tests with declared thresholds for sensitivity, specificity, precision, macro-F1, and AUC on held-out pairs, per axis after Path 1. (4) Fine-tune on training pairs only. (5) Re-test held-out pairs plus a regression suite. (6) Loop with a declared stopping rule and a fixed budget.
- **What it measures for MML.** How much governed knowledge must be trained in versus executed explicitly. This is the Research Contract's conversion question: what still fails after tuning is worth keeping as a governed operator.
- **Risks.** Testing on trained pairs measures memorisation; a probe can pass while behaviour does not change; optimising for the tests can game them; the model's compute and licence terms must be recorded.

Suggested order: Path 1 first. It needs no model or compute, and Path 2's tests are cleaner per axis.

This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md) and its [reader-first layout](../../../benchmark/oscarc-reader-first-layout.md). The [machine-readable artifact](../../../../benchmark/results/opposition-matrices-v1.json) is authoritative.
