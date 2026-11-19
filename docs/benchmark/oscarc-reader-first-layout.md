# OSCARC Reader-First Layout

Layout version: `OSCARC-reader-first-v1`. It extends the [OSCARC methodology](oscarc-methodology.md) (`OSCARC-v1`) with how a report is written and arranged; the six OSCARC steps and their judgments are unchanged.

New reports use this layout. Existing reports keep the v1 layout until they are next regenerated. The methodology document itself is unchanged on purpose: six benchmarks record its hash as provenance, so editing it would make their evidence stale.

## Why

A report has two audiences: the researcher who needs the evidence, and anyone else who needs to understand what was found. A useful test is whether someone working at a supermarket checkout could follow the first paragraph of every section. Review of generated reports also showed that readers lose their way when technical material arrives without guidance, and when a second question's tables appear in the middle of the first question's results.

## Principles

1. **Plain words first.** Every section opens with one paragraph a reader outside the field can follow, built on one running example. The animal reports use cat and mouse as enemies, lion and tiger as alike, and bear and lion as animals that never meet. That paragraph contains no code, identifiers, tables, or formulas.
2. **Then the technical detail.** Thresholds, identifiers, tables, and verdict codes follow the plain paragraph. They are never removed for readability.
3. **Guide the reader.** After the executive interpretation, one short bridge paragraph says what follows. The OSCARC section opens with one paragraph explaining the six steps, and each step is a subsection.
4. **One report, one claim.** When a result section starts to grow tables for a second question, stop and make it a *signal*. The parent report explains the signal in one plain paragraph and links to a deeper-study report; the deeper report links back.

## Template

The executable form is [`src/helpers/oscarc_report.py`](../../src/helpers/oscarc_report.py). It renders the fixed layout and guidance paragraphs, and refuses a section whose plain paragraph is missing or contains code-like notation. Programmes own every word of content.

```markdown
# [Study] — OSCARC Report
> **[One-sentence tagline]**
*Deeper study for [parent report].*            (deeper-study reports only)

## Research intention        plain paragraph, then technical detail
## Executive interpretation  plain paragraph, then technical detail
[bridge: what follows — six OSCARC steps, any signals, next paths]

## OSCARC
[one paragraph explaining O, S, C, A, R, C]
### O — Objective observation                          plain, then technical
### S — Standard, baseline, or reference model         plain, then technical
### C — Context and chronology                         plain, then technical
### A — Actions, interventions, or observed mechanisms plain, then technical
### R — Result, effect, or measured outcome            plain, then technical
### C — Comparative assessment and research conclusion plain, then verdict, criteria, evidence strength

## Signals for deeper study                            (when present)
### Signal N — [title]       plain paragraph, then link to its own report

## Next paths                plain paragraph, then hypotheses, predictions, protocols, risks
[methodology and machine-readable artifact links]
```

The [Animal Opposition v1 report](../capabilities/semantic-representation/results/opposition-matrices-v1.md) and its two deeper-study reports are the reference example.

## Lessons learned

These rules come from review of generated reports:

1. **Generate every number and count in prose,** including the plain paragraphs. A hand-written plain example ("the lion and the tiger stop being alike") was false; the computed list named different pairs.
2. **Check plain examples against the data before publishing.** Simplifying must not change the claim.
3. **Preserve unfavourable results in the main text.** When a control explains the effect (a parse-once cache matching compiled reuse), say so where the effect is claimed.
4. **Label post hoc analysis `EXPLORATORY`,** and turn it into a falsifiable prediction for the next path rather than a conclusion.
5. **Separate review observations from measurements.** An idea raised while reading results is recorded as a signal or an observation, and tested before it becomes a finding.
6. **Say what a change of scale does and does not change.** A linear rescaling with matching thresholds leaves retrieval measures unchanged; the task definition and the storage type may not.
7. **Methodology documents are provenance.** Benchmarks hash the methodology they were written under. Extend it in a new versioned document, or regenerate and review every dependent artifact deliberately.
