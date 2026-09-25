# The Energy Ledger

## Persistence, Transfer and Transformation Across Physical Domains

### Paper 3.1 — Developed Draft

> This document is a developed working draft. Its equations, scope, provenance, maturity assignments, and novelty boundary remain subject to review.

## Central Question

> How can one conserved quantity appear as motion, heat, sound, fields, and fluid flow?

## Core Proposition

Energy is the conserved quantitative substrate of transformation, while its carrier and form may change continuously.

## Core Formulas

$$
\boxed{
\dot E
=
P_{\mathrm{in}}-P_{\mathrm{out}}
}
$$

For interconnected domains:

$$
\boxed{
\dot E_i
=
\sum_{j\neq i}P_{j\rightarrow i}
-
\sum_{j\neq i}P_{i\rightarrow j}
+
P_i^{\mathrm{external}}
}
$$

## Five-Domain Transposal

| Domain | Representative energy |
| --- | --- |
| Mechanics | $\frac12mv^2+\frac12kx^2$ |
| Thermodynamics | $U(T,V,N)$ |
| Acoustics | $\frac12M_aU^2+\frac{q_a^2}{2C_a}$ |
| Electromagnetics | $\frac12LI^2+\frac12CV^2$ |
| Fluid mechanics | $\frac12I_hQ^2+\frac{q_h^2}{2C_h}+mgh$ |

## One-Sentence Claim

> Energy does not disappear when a process becomes noisy, warm, or turbulent; it changes carrier, scale, and accessibility.

## Drift Detector

> Has every apparent loss been assigned to another energy store, output path, or boundary transfer?

## Connection to Resonant Capacity

$$
\boxed{
\mathcal K_r
=
\kappa\Sigma(\Psi G_r)^2
}
$$

This paper establishes the quantity being stored and transformed, but not yet its recoverability.

## Dance

**Persistence dance:** storage ↔ transfer ↔ transformation.

## Evidence Intake 001 — Energy Meaning of the Quadratic Family

$\mathcal K=\kappa S\Psi^2$ is accepted here only as a classification of particular energy terms, never as the general energy balance. Each example must state whether it is instantaneous, peak, cycle-mean, modal, distributed, or intrinsic.

For $a(t)=A\cos\omega t$, the rate-side peak kinetic term is

$$
K_{\mathrm{peak}}=\frac12S_f(\omega A)^2.
$$

This is not automatically total stored energy for a forced off-resonance system. Potential or field-side terms must be included, and peak, mean, and total conventions must not be mixed.

For a vacuum plane wave with peak electric field $E_0$, $\langle u\rangle=\tfrac12\varepsilon_0E_0^2$ includes equal cycle-mean electric and magnetic contributions. At fixed frequency, amplitude changes field energy or occupation, while photon energy remains $h\nu$. Rest energy $mc^2$ is the intrinsic neutral-gain capacity binding $1\cdot m(c\cdot1)^2$; it is not an oscillatory amplification term.

## Evidence Intake 002 — Dynamic Stored-Capacity Balance

For a recoverable storage function $H$ connected to external ports and a resistive conversion path,

$$
\dot H=P_{\mathrm{in}}-P_{\mathrm{out}}-P_{\mathrm{loss}}.
$$

Here $P_{\mathrm{loss}}$ leaves the selected recoverable Hamiltonian but remains energy in the complete first-law boundary, commonly as internal energy. Calling this “sustainable capacity” requires a declared store and time horizon; capacity itself is not a conserved substance.

At periodic steady state, $\langle\dot H\rangle=0$. If there is no other net output, $P_{\mathrm{in}}=P_{\mathrm{loss}}$ and

$$
H_{\mathrm{stored}}=\frac{Q}{\omega_0}P_{\mathrm{in}}.
$$

This fixed-power relation and the fixed-source-effort $Q^2$ response describe different experiments, not competing laws.

## Evidence Intake 006 — Cross-Domain Transfer Ledger

A transformation network may use

$$
\dot E_i=\sum_{j\ne i}P_{j\to i}-\sum_{j\ne i}P_{i\to j}+P_i^{ext},
$$

with internal transfers cancelling pairwise under one sign convention. This proof requires non-overlapping ledger accounts. Domain labels do not guarantee that condition: acoustic energy may already be included in fluid or mechanical energy; hydraulic energy is fluid mechanical energy at another resolution; and dissipated mechanical or electromagnetic energy becomes internal energy only if the receiving store lies inside the boundary.

The ledger therefore distinguishes:

1. **carrier or modal partition** — mutually exclusive stored-energy accounts;
2. **domain dialect** — alternative variables describing a process;
3. **conversion edge** — physical transfer between distinct accounts;
4. **reclassification** — a change of description that transfers no energy.

Only mutually exclusive accounts and physical conversion edges enter the conservation sum.
