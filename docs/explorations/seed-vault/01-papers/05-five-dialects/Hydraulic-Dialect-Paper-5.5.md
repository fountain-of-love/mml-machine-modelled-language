# The Hydraulic Dialect

## Inertance, Compliance and Resistance Before Turbulence

### Paper 5.5 — Developed Draft

**Claim maturity:** Established lumped model / bounded synthesis.

## Proposition

Fluid systems admit a compact lumped grammar before geometry, free surfaces, nonlinear advection, separation, and turbulence require additional structure.

## Core Relations

$$
\Delta p=I_h\dot Q,
\qquad
Q=C_h\dot p,
\qquad
\Delta p=R_hQ.
$$

## Planned Development

- bind hydraulic inertance, compliance, and resistance;
- identify the exact breakdown path toward nonlinear and distributed flow;
- provide transposal, drift detector, imputation opportunity, and test.

## Assigned Scientific Concerns

This paper supplies the hydraulic evidence for **C01, C04, C06, C08, and C09**. It must distinguish pressure-source from flow-source excitation, include source and load impedance, identify whether compressibility, free-surface elevation, or vessel compliance stores the relevant energy, and state the laminar, linear, and lumped assumptions.

It must explicitly compare its physical ancestry and mathematical overlap with acoustics and mechanics so that common structure is not misreported as independent confirmation.

**Resolution evidence:** a complete hydraulic resonator binding, an independently predicted gain, and a nonlinear advection, separation, cavitation, water-hammer, or turbulence case that rejects the reduced relation.

## Evidence Intake 001 — Hydraulic Dual Storage

Within a declared lumped, linear, compliant model,

$$
H_h=\frac12I_hQ^2+\frac12C_h(\Delta p)^2.
$$

The compliance term must identify its physical store—fluid compressibility, vessel elasticity, accumulator gas, or free-surface gravity—and its reference state. Pressure and flow gains depend on whether the source is pressure-like, flow-like, or has finite impedance.

Water hammer can supply an oscillatory test while exposing the lift to distributed wave propagation. Turbulent pressure loss is not generally a linear $R_hQ$ law, and cavitation changes boundary and constitutive structure.

## Evidence Intake 002 — Canonical Hydraulic Specialization

For a linear series hydraulic inertance–resistance–compliance model,

$$
\omega_0=\frac1{\sqrt{I_hC_h}},
\qquad
Q_h=\frac{\omega_0I_h}{R_h}.
$$

With fixed source-pressure amplitude, volume flow observed at $\omega_0$, and inertive baseline $Q_0=\Delta p_0/(\omega_0I_h)$, the canonical flow gain is $Q_h$ and $H_{I,r}=\tfrac12I_h(Q_0Q_h)^2$.

This result is not evidence independent of mechanics or acoustics merely because the symbols differ. It is a hydraulic realization of the same linear network structure and must be classified accordingly under C06.

## C11 Evidence Role

Hydraulics is provisionally Tier A or B depending on the tested mechanism. A rigid-column/elastic-vessel lumped model mainly demonstrates the same continuum-mechanical reduction. A stronger test must predict, before calibration, where compressibility, water hammer, cavitation, nonlinear resistance, or fluid–structure interaction adds an operator, state, or bound absent from the canonical grammar.

## Evidence Intake 003 — Elementary Hydraulic Parameters

For a uniform pipe segment in the plug-flow inertance approximation,

$$
I_h=\frac{\rho\ell}{A}.
$$

For a compliant store and fully developed laminar flow in a circular pipe,

$$
C_h=\frac{dV}{dp},
\qquad
R_h=\frac{8\mu\ell}{\pi r^4}.
$$

The resulting linear relations are

$$
\Delta p=I_h\dot Q,
\qquad
Q=C_h\dot p,
\qquad
\Delta p=R_hQ.
$$

Each coefficient is regime- and geometry-dependent. Entrance effects, velocity profiles, fluid compressibility, wall elasticity, gravity, nonlinear loss, cavitation, and turbulence determine whether the lumped parameters remain valid.

## Second-Pass Reduction Contract

The hydraulic lumped approximation must compare element transit and wave times with the system timescale, state the assumed velocity profile and Reynolds regime, and identify whether compressibility and wall elasticity are neglected or represented as compliance. Failure routes include distributed water hammer, unsteady friction, fluid–structure interaction, separation, cavitation, and turbulence.

## Evidence Intake 010 — Source-Supported Resistance/Inertia Reduction

Higo, Shimizu, and Tanaka derive and verify a lumped flow-passage model combining resistance and inertia and show why a steady laminar pipe resistance can fail for complex viscous passages: [DOI 10.5739/jfps.52.16](https://doi.org/10.5739/jfps.52.16).

This strengthens the hydraulic reduction and its failure boundary. It does not supply compliance, a complete resonant topology, or independent law-level evidence. Those remain required for a full R3 certificate.

## Evidence Intake 014 — R3-v1.0 Hydraulic Certificate

The missing topology is fixed as a pressure-driven line–accumulator mode linearized at a declared bias point. With $I_h$, tangent compliance $C_h$, and tangent total resistance $R_h$ independently obtained,

$$
Q_{h,0}=\frac{\Delta p_0}{\omega_hI_h},
\qquad
G_r=Q_{qual,h}=\frac{\omega_hI_h}{R_h},
\qquad
\boxed{\mathcal K_{H,r}=\frac12I_h(Q_{h,0}Q_{qual,h})^2}.
$$

The energy is cross-checked from $(Q_{qual,h}/\omega_h)P_{in}$. Cavitation, nonlinear/turbulent resistance, distributed water hammer, and state-dependent compliance are explicit rejection or lift conditions. See [Resonant Capacity R3 Certificates](../../02-proof/Resonant-Capacity-R3-Certificates.md). Status: analytically complete for the declared linear one-mode model; empirical certificate pending.
