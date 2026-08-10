# Words Carry Weight

**Machine Modelled Language: executable semantic infrastructure from public knowledge**

Machine Modelled Language (MML) explores a simple proposition:

> **We don't necessarily need increasingly complicated computation. We may need a representation of meaning rich enough that powerful mathematical structures already available to us start doing useful work.**

MML compiles governed concepts, senses, semantic roles, aliases, and typed relations into deterministic weighting operators. The current Python experiment uses matrices and PageRank-style propagation; it does not generate language or reproduce an LLM's internal mechanism. It gives explicit semantic structure a reusable, inspectable form whose weights can be rebuilt from the same governed inputs.

This is the literal seed of the idea **words carry weight**: concepts become addressable coordinates, different kinds of relationship contribute different transition capacity, and a query activates a semantic field shaped by the conceptual model.

The current code compiles co-occurrence and three positive governed relation types into one normalized matrix, while treating contradiction separately. The fuller direction is a family of relation-specific matrices—synonymy, hierarchy, opposition, part/whole, causality, role correspondence, association, temporal relation, and others—from which an application constructs a task-specific semantic operator using explicit policy coefficients. Those coefficients are inspectable semantic-policy decisions, not learned black-box parameters.

The CML work makes the representation richer still. Concepts such as `capacity`, `activation`, `boundary`, `substrate`, `gain`, and `storage` can occupy comparable semantic roles across domains rather than merely being connected by an undifferentiated “related to” edge. MML is the proposed numerical execution layer over that governed structure.

Architectural misuse of LLMs contributes to:

- hallucination and convincing unsupported answers;
- semantic and behavioural drift;
- repeated power-intensive computation for known patterns;
- autonomous tool use becoming unintended external action;
- the limits of containing an entangled model with safety harnesses;
- concentration of technical and economic power;
- indiscriminate automation of complete human roles; and
- stochastic next-token prediction being used for tasks requiring exactness and reproducibility.

Hence, we propose MML. It does not independently solve security, sustainability, employment, or governance. It changes the architecture by keeping governed knowledge explicit and reserving stochastic models for discovery and language work, opening the door to more sustainable solutions.

This repository contains a bounded Python mechanism experiment. It demonstrates matrix construction, query activation, inspectable relation paths, governed updates, snapshots, and rollback. It does not yet implement relation-specific matrix composition, the proposed multi-layer MML engine, or the wider Semantic Operating System (SOS).

## Start Here

Start with the functional spine in [`activate_grounded_focus.py`](activate_grounded_focus.py) and the operational application flow in [`words_carry_weight.py`](words_carry_weight.py). Corpus grounding identifies occurrences of `bank` as governed identities such as `bank_river`; query focus narrows `bank` to the same identity; a Personalized PageRank activation strategy turns that selected identity into inspectable activation. The current experiment and benchmark are adapters over this flow, not its definition. Run the bounded demonstration through [`run_words_carry_weight.py`](run_words_carry_weight.py). The accompanying [vocabulary contract](docs/activate-grounded-focus-vocabulary.md) fixes these terms and their drift boundaries.

> **Ground the known. Focus the intended. Activate the related.**

In short: **focus is representational narrowing** (`bank -> bank_river`); **activation is the numerical distribution produced by querying that focused identity**. Attention is an inspiration-level analogy only and is not the name of an MML mechanism.

Everything else in the repository builds outward from that seed:

- **Operational flow:** `activate_grounded_focus.py` supplies the functional contracts; `words_carry_weight.py` coordinates knowledge construction and runtime activation.
- **Current demonstration:** `run_words_carry_weight.py` composes fixture loading, representation comparison, and activation-console presentation around the operational flow.
- **Mechanism elaboration:** the `elaborations/` package adds governed aliases, typed relations, provenance, paths, snapshots, updates, and rollback.
- **Authored application:** the legal demonstration applies those elaborations to bounded GDPR evidence ranking.

These later mechanisms are relevant because they test what becomes possible when the representation grows richer. They are not the definition of MML and should not obscure its originating proposition.

Begin with [Words Carry Weight: The Essence](docs/words-carry-weight-essence.md), which explains the minimal semantic-grounding and focus experiment and the wider dimensions required for reasoning. Continue with [What MML is and what it opens](docs/What.md), [How the experiments work](docs/How.md), and [MML in depth](docs/MML-In-Depth.md), or consult the [research contract](docs/Research-Contract.md) for the evidence boundary. The complete reading map is in [Documentation](docs/README.md).

## Executable Evidence

| Stage | Command | Demonstrates |
| --- | --- | --- |
| Essential seed | `make run` | Transition-model construction, semantic focus, and query-relative activation |
| Mechanism elaboration | `make run-elaborate` | Polysemy, field combination, paths, and higher-order activation |
| Authored application | `make run-legal` | GDPR evidence ranking as a mechanism demonstration |
| Governed change | `make update-demo` | Local relation updates, consequences, and rollback |
| Semantic representation benchmark | `make benchmark-check` | Whether governed identity enrichment improves semantic focus under fixed mathematics |
| Retrieval application diagnostic | `make retrieval-benchmark-check` | Legacy deterministic regression checks beside lexical baselines |

The corpus and probes were authored together. They demonstrate mechanics and protect regressions; they are not independent evidence of generalisation, legal validity, production readiness, or superiority over TF-IDF, BM25, RAG, or LLMs. The exact evidence boundary is defined in the [research contract](docs/Research-Contract.md).

## Scientific Foundation: The Semantic Seed Vault

Alongside the executable MML experiments, the repository includes a [Semantic Seed Vault](docs/explorations/seed-vault/README.md). It develops both a scientific derivation and a demonstration of how a **Common Language Model (CML)** could organize knowledge across a complex research domain.

The scientific work derives Resonant Capacity as a universal representation law for a declared class of stable quadratic two-store systems. It begins from one frozen parent system, derives

$$
\mathcal K_r=\kappa\Sigma(\Psi G_r)^2,
$$

and applies the same definitions, conventions, and admission rules to mechanics, second-sound thermodynamics, acoustics, electromagnetism, and hydraulics. The derivation fixes the coefficient from the energy convention instead of fitting it, preserves the physical role of every substituted quantity, checks dimensions and power balance, and states where the law does not apply. It establishes a bounded five-domain representation theorem; broader empirical claims outside that class remain separate work.

For scientists, the current contribution is this bounded, falsifiable cross-domain synthesis: Resonant Capacity provides one role-preserving mathematical representation for the admitted systems and makes both successful mappings and failures explicit; its exact novelty relative to the full literature remains under review.

The vault uses shared semantic roles—such as capacity, substrate, activation, gain, storage, boundary, evidence, maturity, and failure—to compare those realizations without erasing their physical differences. It records papers and formulas together with claim maturity, scientific concerns, derivations, negative mappings, provenance, competing interpretations, and possible future research.

This is a scientific foundation for **words carry weight**. CML can give scientific concepts, roles, equations, constraints, and failure conditions stable identities and typed relationships. MML can then transpose that governed scientific structure into mathematical weights and task-specific operators. Scientific discovery could potentially become directly usable in deterministic mathematical operations instead of remaining only in prose or being repeatedly reconstructed by a language model.

Combinations such as `capacity + activation + boundary` can create a more distinctive conceptual coordinate than any broad term alone—the CML expression of [combinatorial uniqueness](docs/Combinatorial-Uniqueness.md). The Seed Vault supplies the scientific and semantic structure; compiling that structure into relation-specific MML operators is the next executable step.

This makes the Seed Vault evidence for several proposed CML capabilities:

- expressing one concept consistently across multiple scientific vocabularies;
- connecting reader-facing claims to equations, proof records, evidence, and scope conditions;
- distinguishing established relations, derived results, hypotheses, and superseded interpretations;
- preserving failed mappings and counterexamples instead of forcing every cell to match;
- localizing conceptual updates through explicit authorities and concern ledgers;
- maintaining a human-readable knowledge base that could later support deterministic MML traversal and governed LLM assistance.

The scientific derivation is equation-led rather than encoded in machine-verifiable proof software. Its stated result is universal within the admitted model class, not across every physical system or regime. Experimental replication and any stronger empirical invariant outside that class remain distinct from the analytical theorem. These boundaries delimit the claim without reducing the vault to a governance demonstration.

Useful entry points are the [claim ledger](docs/explorations/seed-vault/00-governance/Claim-Ledger.md), [analytical derivation](docs/explorations/seed-vault/02-proof/Resonant-Capacity-R3-Certificates.md), [Paper 0](docs/explorations/seed-vault/01-papers/00-foundation/Five-Domain-Energy-Grammar-Paper-0.md), [vault manifest](docs/explorations/seed-vault/00-governance/Vault-Manifest.md), and [series map](docs/explorations/seed-vault/00-governance/Series-Map.md).

## Direction

MML is the implemented concept-execution component. SOS is the proposed modular stack that could combine governed concept routing, document authority, lexical retrieval, and constrained language rendering. The [four-tier pipeline](docs/sos/Four-Tier-Modular-Pipeline.md) describes that collaboration without treating the current prototype as the completed architecture.

## The Spark

Two people feel like natural ignition points for this idea.

[Oleg Lavrovsky](https://datalets.ch/) brings the other half: Swiss open-data craft, Wikidata practice, civic tooling, hackathon culture, and the patient work of making public knowledge usable by people and machines.

[Andrej Karpathy](https://github.com/karpathy), through [minGPT](https://github.com/karpathy/minGPT), makes the neural side small enough to understand. That matters because MML does not reject LLMs; it needs a clear, inspectable neural workbench for discovery, syntax, and generation.

Put those two instincts together—small intelligible models and living public knowledge—and the MML idea starts to crackle. [Apertus](https://apertvs.ai/), from the Swiss AI Initiative, then feels like the institutional runway: sovereign AI discipline, open methods, reproducibility, and European seriousness around governance.

## Closing Vision

MML points towards a complementary European sovereign AI path: transparent knowledge structures, inspectable graph dynamics, potentially lower-energy computation, and controllable semantic foundations working alongside language models rather than pretending to replace all of their capabilities.

We also believe that no single person should be allowed to hold this much power, money, and technology in a centralised form, as the world increasingly reflects today. For that reason, this work is paired with a legal container: a non-profit operating model, refined by lessons learned from OpenAI and documented at [fountain-of-love/operating-model](https://github.com/fountain-of-love/operating-model).

In the spirit of [First Follower: Leadership Lessons from Dancing Guy](https://www.youtube.com/watch?v=fW8amMCVAJQ), we prefer to be the first follower rather than the first mover. The goal is not to centralise a new movement around one actor, but to help legitimise and strengthen a direction that others can join, inspect, and carry forward.

There is also a second meaning: first followers get to observe, learn, and move with more care. By studying where earlier systems struggled—technically and institutionally—we can avoid repeating preventable mistakes around concentration of power, governance, sustainability, and trust.

Use and redistribution are governed by [LICENSE.md](LICENSE.md). The licence text is authoritative.

## Easter Egg: Drift by Design

There is a rat race towards power, money, and technology. So this repository carries a small Easter egg: a deliberate drift, a few small imperfections, in analogy to how Leonardo da Vinci's notebooks also contained oddities, reversals, and human traces.

Anyone who hands the idea blindly to an AI system and starts building without thinking may launch a rocket in a slightly wrong direction. Two degrees off course at the start looks harmless; over distance, it becomes massive deviation.

That is part of the point. The current LLM race demonstrates the danger of accelerating before understanding: building ever-larger systems, even approaching nuclear-scale energy demands, while a more elegant division of labour may be available through structured, inspectable MMLs. The Easter egg is a reminder that intelligence is not speed. It is orientation.

This is a philosophical and editorial reminder—not permission for hidden defects, benchmark bypasses, or undocumented behaviour. Executable claims remain subject to tests, integrity checks, and the [research contract](docs/Research-Contract.md).

A lesson that might account for an EU bank as well. ;-)

This README was generated with [Enigma](docs/enigma.md), a conceptual context-engineered model that runs on top of OpenAI.
