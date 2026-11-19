# Opposition Two Tensions v1 — OSCARC Report

> **Alike by kind and alike by alliance are different things.**

*Deeper study for [Animal Opposition v1](opposition-matrices-v1.md).*

## Research intention

In the animal table, the dog and the mouse came out as on the same side, because both are enemies of the cat. The lion and the tiger are also alike, but for a different reason: they are the same kind of animal. We asked whether these are really two different things, and whether mixing them explains the arithmetic's mistakes.

Technically: tag each authored relation as interaction or likeness, decompose every two-hop composition into its contributing paths, and classify each conflict with governed knowledge by whether it crosses the two axes.

## Executive interpretation

Mostly yes. Of the 5 times the arithmetic contradicted the table, 4 came from mixing the two kinds of alike. For example: the dog is like the wolf, the wolf hunts sheep, so the arithmetic concluded that the dog is the sheep's enemy, while sheepdogs protect sheep. The remaining mistake is different: two hunters of the same prey are rivals, not friends, and no second scale fixes that.

4/5 conflicts cross axes (`EXPLORATORY_SIGNAL`). The axis tags were assigned after the conflicts were seen, so this is exploratory.

The rest of this report shows the evidence behind that summary in six short steps called OSCARC. It ends with the next paths worth following.

## OSCARC

OSCARC moves in a fixed order: what was seen (**O**), what was expected beforehand (**S**), how and in which order it was done (**C**), what was actually changed or applied (**A**), what came out (**R**), and the judgment that compares the outcome with the expectation (**C**). Each step starts in everyday words and then gives the technical detail.

### O — Objective observation

Almost every suggestion and every mistake of the two-step arithmetic passes through both kinds of alike at once. Only two suggestions stay within one kind: dog–mouse and cat–sheep.

5 conflicts and 13 candidates; 11 candidates draw most of their magnitude from mixed paths; single-axis candidates: dog–mouse +0.60, cat–sheep -0.30.

### S — Standard, baseline, or reference model

If there really are two tensions, the mistakes should mostly come from mixing them, and the sensible suggestions should mostly stay within one.

Classification rule, declared in code before the counts were read: `MIXED_PATH` when mixed paths supply more than half the inferred magnitude; `TARGET_ON_OTHER_AXIS` when single-axis paths land on a pair governed on the other axis; otherwise `SAME_AXIS`. The tags themselves are post hoc.

### C — Context and chronology

After the main demonstration showed the mistakes, we labelled each fact in the table as either about getting along or about being alike, and traced every two-step suggestion back through the animals it passed.

Tags live in the fixture's `dimension` field with status `EXPLORATORY_POST_HOC`. Unlisted pairs carry no tag and contribute no paths.

### A — Actions, interventions, or observed mechanisms

We did not change any numbers. We only split each two-step result into the routes that produced it, for example dog to wolf to sheep, and noted which kind of alike each step used.

For pair (i, j), each intermediate k contributes S[i,k]·S[k,j]; contributions are labelled by the axes of their two links.

### R — Result, effect, or measured outcome

Three mistakes come from chaining the two kinds of alike, one puts a getting-along guess on a pair that is really about being the same kind, and one stays within getting along.

| Pair | Inferred | Governed | Governed axis | Mixed-path share | Classification |
| --- | ---: | ---: | --- | ---: | --- |
| dog–sheep | -0.80 | +0.5 | interaction | 1.00 | `MIXED_PATH` |
| zebra–tiger | -0.80 | +0.0 | interaction | 1.00 | `MIXED_PATH` |
| wolf–sheep | +0.60 | -1.0 | interaction | 0.67 | `MIXED_PATH` |
| dog–wolf | -0.50 | +0.8 | likeness | 0.00 | `TARGET_ON_OTHER_AXIS` |
| wolf–bear | +0.50 | -0.4 | interaction | 0.00 | `SAME_AXIS` |

### C — Comparative assessment and research conclusion

The idea of two tensions is a strong lead, not yet a proven fact, because we made up the labels after seeing the mistakes. The real test is the next step.

**Conformity judgment: `EXPLORATORY_SIGNAL`.**

- `every_conflict_classified`: `True`
- `most_conflicts_cross_axes`: `True`
- `single_axis_candidates_exist`: `True`

**Evidence strength: `EXPLORATORY`.** Post hoc tags on an authored fixture.

## Next paths

Next, give the table two separate scales, filled in fresh without looking at these mistakes, and see whether the mixing mistakes disappear while the dog and mouse suggestion survives.

### Path 1 — Two axes: interaction and likeness, each in [-1, 1]

- **Hypothesis.** Two signed matrices, composed within an axis unless a declared cross-axis rule applies, remove the conflicts that come from mixing tensions without losing useful candidates.
- **Prediction (falsifiable).** The 4 cross-axis conflicts disappear; wolf–bear persists; the single-axis candidates (dog–mouse +0.60, cat–sheep -0.30) survive unchanged. Any other outcome falsifies the two-tension reading.
- **Smallest experiment.** Author both axes for the same ten animals blind to this report; build two `SignedRelationMatrix` instances; compose per axis; compare against this report.
- **Follow-up.** A persisting same-axis conflict asks for relation-specific composition rules (shared prey ⇒ competition), as in the [compiled semantic operator](../../knowledge-state-execution/semantic-operator-design.md).
- **Risk.** Axes fitted to these ten animals; without blind re-authoring the prediction is circular.

This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md) and its [reader-first layout](../../../benchmark/oscarc-reader-first-layout.md). The [machine-readable artifact](../../../../benchmark/results/opposition-two-tensions-v1.json) is authoritative.
