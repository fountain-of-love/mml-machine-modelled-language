# Archived v1 Retrieval Research

This note preserves the broader benchmark investigation that was removed from the active project surface. It is retained as research history, not hidden or presented as current acceptance logic.

The investigation added semantic challenge annotations, seven ranking variants, hybrid calibration, relation-weight sensitivity, staged typed-graph ablation, explanation-coverage thresholds, localized-update thresholds, and several verdicts. It improved rigor but began to redefine MML as a retrieval-ranking project. The active benchmark is therefore intentionally smaller.

## Findings retained

- The deliberately named multiplicative MML/lexical hybrid combines graph activation with lexical overlap as `mml_score × (0.2 + 0.8 × lexical_overlap)`. The focused active diagnostic now reproduces the original development observation:

  | Tier | TF-IDF nDCG@10 | MML nDCG@10 | Hybrid nDCG@10 |
  | --- | ---: | ---: | ---: |
  | Polysemy | `0.7733` | `0.7752` | `0.7911` |
  | GDPR | `0.6535` | `0.4969` | `0.7072` |

  This is a useful observation: lexical evidence and explicit semantic activation were complementary on both tiers, and the combination was especially revealing on GDPR, where MML alone trailed TF-IDF while the hybrid exceeded both. It does not establish generalization because v1 is a synthetic development fixture.

- Co-occurrence GDPR nDCG@10: `0.4969`.
- Governed aliases: `0.5295`.
- Adding `supports`: `0.5318`.
- Adding contradiction: unchanged at `0.5318`.
- Adding `requires`: `0.5351` and `+0.0023` on the selected semantic slice aggregate.
- Adding `qualifies`: `0.5403`, with no further semantic-slice gain.
- Hard-negative Top-10 intrusion worsened from `0.1667` to `0.2500`.
- The controlled GDPR relation update changed scores for 80% of candidates under the earlier `1e-4` threshold, exceeding an experimental 50% limit.
- The same update left polysemy rankings unchanged and reproduced the original snapshot and rankings exactly after rollback.
- Authored relation or alias paths appeared in 7 of 12 eligible top-three GDPR results.
- A later reciprocal-rank-fusion experiment won its declared semantic-slice selection, while the simpler multiplicative hybrid retained the stronger GDPR macro behavior. That later selection experiment should not obscure the clearer earlier `0.7072` hybrid observation above.
- Uniform relation-scale sensitivity selected `1.0` among `0.5`, `0.75`, and `1.0`.

## Why the verdict framework was retired

The `ACCEPT/REJECT`, `semantic_contribution`, `infrastructure_readiness`, and strict comparative verdicts combined useful observations with provisional thresholds. In particular, the percentage of document scores changed is not equivalent to structural update locality: one explicit, traceable edge may legitimately propagate broadly.

The findings remain useful for future work on false positives, typed relation semantics, and sensitivity. They no longer serve as the organizing definition of MML.
