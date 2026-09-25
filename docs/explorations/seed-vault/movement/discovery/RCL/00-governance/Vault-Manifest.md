---
artifact: governance
status: authoritative
authority: vault-structure
updated: 2026-08-10
---

# Seed Vault Manifest

## Purpose

This manifest is the authority for artifact location, role, and lifecycle status. Scientific claims are governed by [Claim Ledger](Claim-Ledger.md); concern status is governed by [Concern Ledger](Concern-Ledger.md).

## Status vocabulary

| Status | Meaning |
| --- | --- |
| `placeholder` | Scope reserved; substantive development incomplete |
| `developed-draft` | Substantial content exists; scientific/editorial review remains |
| `review-ready` | Coherent draft ready for formal review |
| `authoritative` | Current programme authority for its declared function |
| `superseded` | Retained for provenance but not current authority |
| `optional-research` | Non-blocking extension beyond the present proof claim |

## Authority rules

1. `README.md` is the entry point.
2. `00-governance/Series-Map.md` defines the paper sequence.
3. `00-governance/Claim-Ledger.md` defines current claim maturity.
4. `00-governance/Concern-Ledger.md` defines open and closed concerns.
5. `02-proof/` contains derivations supporting the representation theorem.
6. `03-evidence/` contains literature and discovery evidence, not claim authority.
7. `04-future-research/` contains work not required for the current theorem.
8. `99-archive/` preserves superseded composite documents and historical status notes.

## Artifact register

| Artifact | Type | Status | Authority |
| --- | --- | --- | --- |
| `README.md` | navigation | authoritative | vault entry point |
| `00-governance/Series-Map.md` | governance | authoritative | paper architecture |
| `00-governance/Claim-Ledger.md` | governance | authoritative | current scientific claims |
| `00-governance/Concern-Ledger.md` | governance | authoritative | concern disposition |
| `00-governance/Publication-Plan.md` | governance | developed-draft | publication sequence |
| `01-papers/00-foundation/Five-Domain-Energy-Grammar-Paper-0.md` | paper | developed-draft | foundation narrative |
| `01-papers/01-direction-and-substrate/*` | papers | developed-draft | energy, substrate, relativity |
| `01-papers/02-boundaries/*` | papers | developed-draft | inner–outer and coherence tensions |
| `01-papers/03-ledgers/*` | papers | developed-draft | energy, entropy, exergy ledgers |
| `01-papers/05-five-dialects/*` | papers | developed-draft | theorem and domain bindings |
| `01-papers/08-governance/*` | paper | developed-draft | admissibility and falsification |
| `01-papers/13-return/*` | paper | developed-draft | nonlinear and methodological return |
| `02-proof/Resonant-Capacity-R3-Certificates.md` | proof dossier | developed-draft | analytical certificates |
| `04-future-research/Resonant-Capacity-Empirical-Validation-Programme.md` | research protocol | optional-research | apparatus and R4 extension |
| `05-experiments/CML-Science-Experiment.md` | experiment | developed-draft | machine-readable worldview experiment |
| `99-archive/Papers-Overview-Legacy.md` | historical composite | superseded | provenance only |

## Migration principle

The 2026-08-10 reorganization changes location and authority, not scientific content. Historical intake notes remain available in the archived overview. Any later content extraction must preserve provenance links back to that archive.
