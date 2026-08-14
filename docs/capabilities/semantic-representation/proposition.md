# The Representational Leverage Proposition

The Representational Leverage Proposition is the architectural mechanism within MML's first capability, [Semantic Representation](README.md): making task-relevant meaning explicit, addressable, and governed may enable fixed ordinary mathematics to produce more useful and attributable semantic behavior.

The intended shift is from:

> “More useful behavior requires more complicated computation.”

to:

> “Some useful behavior becomes available when the representation exposes the distinction the computation needs.”

An execution method cannot reliably act on a semantic distinction that its input state does not represent. A surface identity such as `bank` merges several meanings into one coordinate; governed identities such as `bank_river` and `bank_financial` make those meanings separately addressable. The mathematical operator may remain unchanged while its executable semantic state becomes more precise.

The proposition is not that every richer representation is better. Added structure creates leverage only when it is relevant to the task, correctly governed, and executable by the fixed operator. Irrelevant relations, decorative labels, duplicated edges, or answer-bearing shortcuts add complexity without establishing a semantic mechanism.

The mechanism therefore depends on explicit controls:

- hold source observations, task, operator, and numerical settings fixed;
- vary one task-relevant semantic distinction;
- separate representation changes from query transformations;
- compare against relabelling, sham, and matched-topology controls; and
- remove the distinction again through ablation.

This is a research proposition, not a universal law that representation always dominates algorithm design. Experiments must show that the relevant distinction produces a preregistered useful change, that irrelevant enrichments do not reproduce it, and that the benefit remains material relative to construction and governance cost.

The systematic test is defined by [Experiment 1 — Represent the Meaning. Change the Field.](experiment.md). The current human-readable development evidence is reported in [Semantic Representation Benchmark v1](results/v1.md).
