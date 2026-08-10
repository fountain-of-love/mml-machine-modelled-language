# Recovering Acoustic Elegance

## Pressure, Volume Velocity and the Lumped Sound Element

### Paper 5.3 — Developed Draft

**Claim maturity:** Established lumped model / pedagogical synthesis.

## Proposition

Acoustic complexity often results from comparing distributed acoustic fields with lumped elements in other domains; at equal resolution, acoustics has an equally compact grammar.

## Core Relations

$$
\Delta p=M_a\dot U,
\qquad
U=C_a\dot p,
\qquad
\Delta p=R_aU.
$$

## Planned Development

- bind acoustic inertance, compliance, and resistance;
- state wavelength and geometry limits;
- provide cross-domain transposal, drift detector, and test.

## Assigned Scientific Concerns

This paper supplies the acoustic evidence for **C01, C04, C06, C08, and C09**. It must distinguish pressure-controlled from volume-velocity-controlled excitation, declare source and radiation impedances, define the measurement location and steady-state or transient convention, and derive peak, mean, and total acoustic energy consistently.

It must also state whether the example is independent evidence or a continuum-mechanical realization closely related to the hydraulic and mechanical bindings.

**Resolution evidence:** a complete lumped resonator binding, an independently predicted gain and bandwidth, and a distributed or radiation-loss case that marks the lumped model's failure boundary.

## Evidence Intake 001 — Acoustic Dual Storage

For a lumped linear acoustic element,

$$
H_a=\frac12M_aU^2+\frac12C_ap^2,
$$

with reference pressure and coordinate convention stated. The first term is inertive flow-side storage and the second compliant effort-side storage. Peak and cycle-mean values differ by sinusoidal normalization.

Pressure gain and volume-velocity gain generally differ because source impedance, load impedance, geometry, losses, and observation position differ. Radiation carries energy across a boundary and is not automatically entropy generation inside the resonator. Absorption and viscothermal loss require separate treatment. A 432/440 Hz comparison is admissible only after natural frequency, bandwidth, quality factor, and protocol are specified.

## Evidence Intake 002 — Canonical Acoustic Specialization

For a series lumped acoustic resonator,

$$
\omega_0=\frac1{\sqrt{M_aC_a}},
\qquad
Q=\frac{\omega_0M_a}{R_a}.
$$

With fixed source-pressure amplitude, volume velocity observed at $\omega_0$, and inertive baseline $U_0=p_0/(\omega_0M_a)$, the canonical gain is $G_U=Q$ and $H_{M,r}=\tfrac12M_a(U_0Q)^2$. Pressure across the compliance has a different transfer function even when its resonant magnitude also contains a $Q$ factor.

The result applies only while the lumped wavelength, linear acoustics, and loss model remain valid. Radiation and distributed modes change the topology and energy balance.

## C11 Evidence Role

The lumped acoustic realization is mathematically isomorphic to the canonical network and physically descends from continuum mechanics. It validates transposition and reduction, but it is not automatically independent evidence. A stronger C11 test would preregister a correction or breakdown caused by radiation, viscothermal boundary layers, or distributed modes and verify it without refitting the core grammar.

## Evidence Intake 003 — Elementary Acoustic Parameters

For a short uniform duct used as a lumped inertance and a small compressible cavity used as a compliance,

$$
M_a=\frac{\rho\ell}{A},
\qquad
C_a=\frac{V}{\rho c^2},
$$

under the stated uniform-flow, small-signal, and wavelength assumptions. The canonical equations are

$$
\Delta p=M_a\dot U,
\qquad
U=C_a\dot p,
\qquad
\Delta p=R_aU.
$$

These relations justify an elementary acoustic presentation. They do not replace the wave equation; they are reductions whose validity depends on geometry, mode shape, end corrections, radiation loading, and viscothermal loss.

## Second-Pass Reduction Contract

The acoustic lumped approximation requires a long-wavelength or compact-element regime, commonly expressed as $kL\ll1$ for characteristic size $L$. Each binding must state the frequency band, retained mode, end correction, radiation impedance, and comparison with a distributed or measured response. “Acoustic elegance” is a controlled reduction, not absence of field structure.

## Evidence Intake 010 — Source-Supported Reduction

Swift derives acoustic compliance from linearized continuity and inertance from linearized Euler dynamics for elements small relative to wavelength; their combination produces a Helmholtz resonator, while loss and radiation are required for quality factor: [Nondissipative Lumped Elements](https://doi.org/10.1007/978-3-030-44787-8_8).

This supports the reduction map, storage roles, natural frequency, and breakdown lift. It does not complete Resonant Capacity membership: the energy convention, transfer function, baseline, independently predicted $G_r$, and $\kappa$ still require one frozen certificate and a held-out comparison.

## Evidence Intake 014 — R3-v1.0 Acoustic Certificate

The frozen protocol supplies the previously missing fields. For a pressure-driven compact Helmholtz mode,

$$
U_0=\frac{p_0}{\omega_aM_a},
\qquad
G_r=Q_a=\frac{\omega_aM_a}{R_a},
\qquad
\boxed{\mathcal K_{A,r}=\frac12M_a(U_0Q_a)^2}.
$$

Capacity is total cycle-mean modal energy at resonance, peak amplitudes are used, and $R_a$ must include independently inferred thermoviscous and radiation losses. The amplitude route is cross-checked by $(Q_a/\omega_a)P_{in}$. See [Resonant Capacity R3 Certificates](../../02-proof/Resonant-Capacity-R3-Certificates.md). Status: analytically complete for the declared compact linear one-mode model; empirical certificate pending.
