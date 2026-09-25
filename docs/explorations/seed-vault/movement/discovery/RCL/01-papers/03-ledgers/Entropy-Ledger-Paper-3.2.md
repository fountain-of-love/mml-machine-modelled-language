# The Entropy Ledger

## Irreversibility, Dispersion and the Direction of Physical Change

### Paper 3.2 — Developed Draft

> This document is a developed working draft. Its equations, scope, provenance, maturity assignments, and novelty boundary remain subject to review.

## Central Question

> If energy is conserved, why can transformations not simply be reversed?

## Core Proposition

Entropy generation measures the irreversible dispersal of organized physical capacity, even while total energy remains conserved.

## Core Formulas

$$
\boxed{
\dot S_{\mathrm{gen}}\geq0
}
$$

For a lumped linear dissipative element at temperature $T$:

$$
\boxed{
\dot S_{\mathrm{gen}}
=
\frac{\mathcal Rf^2}{T}
}
$$

## Five-Domain Transposal

| Domain | Dissipation | Entropy-generation approximation |
| --- | --- | --- |
| Mechanics | $bv^2$ | $bv^2/T$ |
| Thermodynamics | Heat conduction and mixing | $\mathbf q\cdot\nabla(1/T)$ |
| Acoustics | $R_aU^2$ | $R_aU^2/T$ |
| Electromagnetics | $I^2R$ | $I^2R/T$ |
| Fluid mechanics | $R_hQ^2$ or viscous loss | $R_hQ^2/T$ |

## One-Sentence Claim

> Entropy is the physical memory of what cannot be perfectly rewound.

## Drift Detector

> Does the model contain resistance, attenuation, viscosity, or friction without an entropy consequence?

## Connection to Resonance

For a resonator:

$$
\boxed{
Q
\approx
2\pi
\frac{E_{\mathrm{stored}}}
{T_0\Delta S_{\mathrm{gen,cycle}}}
}
$$

High resonance quality means substantial stored energy relative to entropy generated per cycle.

This entropy form is conditional. The conventional definition is

$$
Q
=
2\pi
\frac{E_{\mathrm{stored}}}{\Delta E_{\mathrm{lost,cycle}}}.
$$

Replacing lost energy by $T_0\Delta S_{\mathrm{gen,cycle}}$ requires thermalization within the declared environment. Radiation, transmitted sound, exported fluid power, and other boundary outputs are not automatically entropy generation.

## Dance

**Irreversibility dance:** concentration ↔ dispersion ↔ generation.

## Evidence Intake 001 — Entropy Constraints

Near equilibrium, entropy production is commonly quadratic in thermodynamic forces or flows under linear constitutive laws. This resembles quadratic storage algebraically but has a different role: it is a non-negative rate of irreversible production, not stored capacity.

For the Maxwell–Cattaneo branch, finite flux relaxation alone does not establish a positive storage function. A proposed heat-flux quadratic term must be derived with an extended entropy, free-energy, exergy, or passivity functional and shown to preserve non-negative total entropy production.

Every apparent loss will be classified as reversible boundary export, irreversible internal conversion, entropy transfer, internal entropy generation, or unresolved loss caused by an incomplete boundary.

## Evidence Intake 002 — Resistance, Quality Factor, and Entropy

For the canonical linear series resonator,

$$
P_{\mathcal R}=\mathcal Rf^2,
\qquad
Q=\frac{\omega_0\mathcal I}{\mathcal R}
=\omega_0\frac{H_{\mathrm{stored}}}{P_{\mathrm{loss}}}.
$$

The first equality is a constitutive dissipation rate for the selected recoverable model. The corresponding entropy-production rate is $P_{\mathcal R}/T$ only when that lost work is thermalized at a sufficiently well-defined temperature $T$ within the chosen boundary.

Decreasing $\mathcal R$ increases $Q$, but it does not imply zero total entropy generation for a driven experiment: under fixed source effort, the response and supplied power also increase. Entropy and exergy conclusions therefore require the source protocol and integration interval, not $Q$ alone.
