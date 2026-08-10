# Semantic Seed Vault

This folder is a downstream knowledge-base exploration made conceivable by **Machine Modelled Language (MML)** and the proposed SOS architecture. It is not part of the executable MML evidence. Its name is inspired by the [Svalbard Global Seed Vault](https://www.seedvault.no/), which preserves biological seeds so diversity can be regenerated in the future.

For the broader **Semantic Operating System (SOS)** architecture, see [../What.md](../../sos/Architecture.md). For dual persistence, see [../Dual-Persistence.md](../../sos/Dual-Persistence.md). For participation, competing assertions, provenance, and rollback expectations, see [../Commons-Governance.md](../../sos/Commons-Governance.md).

This vault preserves **semantic seeds**:

$$
\boxed{
\text{semantic seed}
=
\text{pattern}
+
\text{relations}
+
\text{constraints}
+
\text{provenance}
}
$$

## Architectural Role

- **CML** is the proposed **Common Language Model**: a future shared schema defining concepts, relations, evidence, constraints, maturity, and topology.
- **Seed Vault** is this knowledge base: the durable content organized according to CML.
- **MML** supplies the executable semantic mechanism whose success would make this larger CML-shaped knowledge base useful to machines.
- **LLMs** assist discovery and expression, but candidate knowledge must be validated before deposit.

The vault can preserve established knowledge, competing interpretations, negative results, counterexamples, open questions, and imputed candidates without presenting them as equally mature.

## Current Contents

Start with the current authorities:

- [Vault Manifest](00-governance/Vault-Manifest.md) — artifact roles, locations, and lifecycle states;
- [Series Map](00-governance/Series-Map.md) — the paper spiral and reading order;
- [Claim Ledger](00-governance/Claim-Ledger.md) — what is currently established, derived, optional, or hypothetical;
- [Concern Ledger](00-governance/Concern-Ledger.md) — authoritative open and closed concern status;
- [Publication Plan](00-governance/Publication-Plan.md) — proposed publication units and gates.

Primary scientific artifacts:

- [A Five-Domain Energy Grammar: Paper 0](01-papers/00-foundation/Five-Domain-Energy-Grammar-Paper-0.md)
- [One Grammar, Five Dialects: Paper 5.0](01-papers/05-five-dialects/One-Grammar-Five-Dialects-Paper-5.0.md)
- [R3 Analytical Certificate Dossier](02-proof/Resonant-Capacity-R3-Certificates.md)
- [Optional Empirical Validation Programme](04-future-research/Resonant-Capacity-Empirical-Validation-Programme.md)
- [The Worldview Layer: A CML Experiment](05-experiments/CML-Science-Experiment.md)

The former all-purpose overview is preserved as [Papers Overview Legacy](99-archive/Papers-Overview-Legacy.md). It contains the full research-intake history but is no longer authoritative for present claim or concern status.

## Directory contract

| Directory | Contents |
| --- | --- |
| `00-governance/` | Current authority and navigation |
| `01-papers/` | Reader-facing scientific papers arranged by spiral stage |
| `02-proof/` | Derivations and analytical certificates |
| `03-evidence/` | Literature review and discovery corpus |
| `04-future-research/` | Optional empirical and speculative extensions |
| `05-experiments/` | CML/MML implementation experiments |
| `99-archive/` | Superseded composite artifacts retained for provenance |
