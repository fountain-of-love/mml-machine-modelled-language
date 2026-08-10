# Words Carry Weight

**Machine Modelled Language: executable semantic infrastructure from public knowledge**

Machine Modelled Language (MML) is a deterministic execution engine over governed concepts, senses, aliases, and typed relations. It does not generate language or reproduce an LLM's internal mechanism. It gives explicit semantic structure a reusable, inspectable form whose statistical weights can be rebuilt from the same governed inputs.

It is the smallest visible seed of the idea: **words carry weight because they sit inside structured relationships.**

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

This repository contains a bounded Python mechanism experiment. It demonstrates representation, query activation, traceable graph diffusion, governed updates, snapshots, and rollback. It does not yet implement the proposed multi-layer MML engine or the wider Semantic Operating System (SOS).

## Start Here

The repository develops MML through three experimental stages:

- **Minimal mechanism:** establishes query-anchored activation over a small word graph.
- **Larger probe bench:** examines polysemy, concept-field combination, semantic paths, and higher-order activation.
- **Authored use case:** applies the same mechanism to a bounded GDPR evidence-ranking scenario.

Begin with [Words Carry Weight: The Essence](docs/words-carry-weight-essence.md), which explains the minimal conceptual-curation experiment and the wider dimensions required for reasoning. Continue with [What MML is and what it opens](docs/What.md), [How the experiments work](docs/How.md), and [MML in depth](docs/MML-In-Depth.md), or consult the [research contract](docs/Research-Contract.md) for the evidence boundary. The complete reading map is in [Documentation](docs/README.md).

## Executable Evidence

| Stage | Command | Demonstrates |
| --- | --- | --- |
| Minimal mechanism | `make run` | Query-anchored activation over a small word graph |
| Larger probe bench | `make run-elaborate` | Polysemy, field combination, paths, and higher-order activation |
| Authored use case | `make run-legal` | GDPR evidence ranking as a mechanism demonstration |
| Governed change | `make update-demo` | Local relation updates, consequences, and rollback |
| Retrieval diagnostic | `make benchmark-check` | Deterministic regression checks beside lexical baselines |

The corpus and probes were authored together. They demonstrate mechanics and protect regressions; they are not independent evidence of generalisation, legal validity, production readiness, or superiority over TF-IDF, BM25, RAG, or LLMs. The exact evidence boundary is defined in the [research contract](docs/Research-Contract.md).

## Science-Domain CML Feasibility Demonstration

Alongside the executable MML experiments, the repository includes a [Semantic Seed Vault](docs/explorations/seed-vault/README.md): a bounded demonstration of how a **Common Language Model (CML)** could organize scientific knowledge across a complex research domain.

The demonstration develops a five-domain energy grammar spanning mechanics, thermodynamics, acoustics, electromagnetism, and fluid mechanics. It uses shared semantic roles—such as capacity, substrate, activation, gain, storage, boundary, evidence, maturity, and failure—to compare equations without erasing their physical differences. The vault records not only papers and formulas, but also claim maturity, scientific concerns, derivations, negative mappings, provenance, competing interpretations, and optional future research.

Here, **words carry weight at the conceptual level**. CML gives terms and abstractions stable identities and structured relationships; a future compiled MML matrix could assign those relationships numerical transition weight. Combinations such as `capacity + activation + boundary` can then create a more distinctive conceptual coordinate than any broad term alone—the CML expression of [combinatorial uniqueness](docs/Combinatorial-Uniqueness.md). The current Seed Vault demonstrates the governed structure, not the executable weighting step.

This makes the Seed Vault a feasibility demonstration for several proposed CML capabilities:

- expressing one concept consistently across multiple scientific vocabularies;
- connecting reader-facing claims to equations, proof records, evidence, and scope conditions;
- distinguishing established relations, derived results, hypotheses, and superseded interpretations;
- preserving failed mappings and counterexamples instead of forcing every cell to match;
- localizing conceptual updates through explicit authorities and concern ledgers;
- maintaining a human-readable knowledge base that could later support deterministic MML traversal and governed LLM assistance.

The science corpus currently centers on the proposed Resonant Capacity representation law and its qualified mappings across five physical domains. Whether or not every scientific hypothesis survives review, the vault demonstrates the architectural feasibility of applying a common semantic schema to an evolving body of interdisciplinary research.

The Seed Vault is **not executable evidence that CML is complete or scientifically general**. Its corpus was developed as part of the same inquiry it organizes. It is therefore a structured design and governance demonstration, while the Python experiments remain the repository's executable MML evidence.

Useful entry points are the [vault manifest](docs/explorations/seed-vault/00-governance/Vault-Manifest.md), [series map](docs/explorations/seed-vault/00-governance/Series-Map.md), [claim ledger](docs/explorations/seed-vault/00-governance/Claim-Ledger.md), and [Paper 0](docs/explorations/seed-vault/01-papers/00-foundation/Five-Domain-Energy-Grammar-Paper-0.md).

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
