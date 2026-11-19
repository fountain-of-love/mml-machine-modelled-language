# Opposition Cell Types v1 — OSCARC Report

> **A number can only mean what its storage can hold.**

*Deeper study for [Animal Opposition v1](opposition-matrices-v1.md).*

## Research intention

Every number in the animal table has to be stored somehow. Think of a supermarket till that only accepts whole euros: a price of fifty cents becomes either nothing or one euro. We asked whether the way we store the cat, dog, lion and tiger numbers can change what the table says.

Technically: store the same governed and learned relation values in nine cell types, on their natural scale (signed [-1, 1] or degree [0, 1]), read them back on the signed scale, and measure what each type preserves.

## Executive interpretation

Yes, it can. Stored as whole numbers from 0 to 255 on a 0-to-1 scale, the middle value that means never meet cannot be stored exactly, and four pairs change their meaning just by being saved: cat–lion, cat–tiger, dog–sheep and sheep–bear. Stored the other way, with never meet at zero, every pair keeps its meaning.

uint8 on the degree scale kept 41/45 governed states; signed int8×127 kept 45/45 (`MECHANISM_CONFORMANT`).

The rest of this report shows the evidence behind that summary in six short steps called OSCARC. It ends with the next paths worth following.

## OSCARC

OSCARC moves in a fixed order: what was seen (**O**), what was expected beforehand (**S**), how and in which order it was done (**C**), what was actually changed or applied (**A**), what came out (**R**), and the judgment that compares the outcome with the expectation (**C**). Each step starts in everyday words and then gives the technical detail.

### O — Objective observation

Some ways of storing numbers keep every pair's meaning. Others lose a few pairs, and the coarsest ones squash the learned version into a single value, so nothing useful is left.

Nine cell types were applied to 45 distinct pairs. Kept states ranged from 40 to 45; the learned relation kept between 1 and 45 distinct values.

### S — Standard, baseline, or reference model

We expected that storage could quietly change meaning, that the whole-number-from-0-to-255 version would be the riskiest, and that very coarse storage would wipe out the learned version's detail.

The expectations are the four conformity criteria under the final step. The float-density criterion follows from IEEE 754 and is included as a check of the measurement, not a finding.

### C — Context and chronology

We took the finished animal table and the learned version, saved each in nine different ways, and read them back.

Types: bool, int8 three states, int8×127, uint8×255, one-place decimal, float16 (both scales), float32, float64. The three-state classes use the ±0.5 band of the main report.

### A — Actions, interventions, or observed mechanisms

Nothing about the animals was changed, only the way the numbers were written down. Each version was stored in its own natural range and converted back, so any difference comes from the storage alone.

`stored_as_signed()` applies a type on its own scale and maps the result back; `neutral_is_exact()` checks whether 0 (or 0.5 on the degree scale) survives storage.

### R — Result, effect, or measured outcome

Here is what each way of storing kept. Most kept everything. The 0-to-255 version on the 0-to-1 scale lost the pairs sitting exactly on the line between alike and never meet. The two coarsest versions kept the table's meaning but erased all detail of the learned version.

| Type | Scale | Levels | Neutral exact | Resolution at neutral | Governed states kept | Learned AUC |
| --- | --- | ---: | --- | ---: | ---: | ---: |
| bool: opposite or not | signed | 2 | False | n/a | 40/45 | 0.500 |
| int8: three states | signed | 3 | True | 1.0e+00 | 45/45 | 0.500 |
| int8: x127 | signed | 255 | True | 7.9e-03 | 45/45 | 0.268 |
| uint8: x255 | degree | 256 | False | 7.8e-03 | 41/45 | 0.273 |
| decimal: 1 place | degree | 11 | True | 2.0e-01 | 45/45 | 0.278 |
| float16 | degree | 15,361 | True | 9.8e-04 | 45/45 | 0.270 |
| float16 | signed | 30,721 | True | 6.0e-08 | 45/45 | 0.270 |
| float32 | signed | 2,130,706,433 | True | 1.4e-45 | 45/45 | 0.270 |
| float64 | signed | 9,214,364,837,600,034,817 | True | 4.9e-324 | 45/45 | 0.270 |

The uint8 failures are the band edges: degree 0.25 and 0.75 are not multiples of 1/255. Floats are densest near zero: float16 resolves 6.0e-08 around a neutral at 0, but 9.8e-04 around a neutral at 0.5.

### C — Comparative assessment and research conclusion

Storage is not a detail. Putting never meet at zero, on a scale from minus one to plus one, kept every meaning in every way of storing we tried. Putting it in the middle of a 0-to-1 scale did not.

**Conformity judgment: `MECHANISM_CONFORMANT`.**

- `unit_scale_uint8_changes_governed_states`: `True`
- `signed_int8_keeps_every_governed_state`: `True`
- `coarse_types_flatten_learned_scores`: `True`
- `float_resolves_finer_around_zero_than_half`: `True`

**Evidence strength: `ILLUSTRATIVE`.** One authored table; the effect is arithmetic and will recur wherever a band edge or neutral point is not representable.

## Next paths

Next, check the same thing on numbers that matter more: the stored weights of a real AI, which are often squeezed into small whole numbers to save memory, and the tables MML itself compiles.

- Apply the type study to compiled MML operators before choosing their storage dtype.
- Repeat it for the 8-bit and 4-bit quantisation schemes used for open model weights, as part of Path 2 in the [main report](opposition-matrices-v1.md).

This report follows the [OSCARC methodology](../../../benchmark/oscarc-methodology.md) and its [reader-first layout](../../../benchmark/oscarc-reader-first-layout.md). The [machine-readable artifact](../../../../benchmark/results/opposition-cell-types-v1.json) is authoritative.
