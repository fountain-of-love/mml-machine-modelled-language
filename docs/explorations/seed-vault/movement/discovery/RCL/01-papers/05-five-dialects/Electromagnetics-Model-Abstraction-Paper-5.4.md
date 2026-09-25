# Electromagnetics as the Model Abstraction

## How Circuits Hide Fields Without Losing Energy Logic

### Paper 5.4 — Developed Draft

**Claim maturity:** Established foundation / architectural synthesis.

## Proposition

Circuit theory succeeds as a reusable abstraction because it hides distributed fields while retaining storage, transfer, and dissipation structure.

## Core Relations

$$
V=L\dot I,
\qquad
I=C\dot V,
\qquad
V=RI.
$$

## Planned Development

- connect circuit elements to field energy and boundary assumptions;
- identify quasi-static and distributed limits;
- provide transposal, drift detector, imputation opportunity, and test.

## Assigned Scientific Concerns

This paper supplies the electromagnetic evidence for **C01, C04, C08, and C09**. It must distinguish voltage-source, current-source, and finite-source-impedance excitation; specify whether $G_r$ applies to current, voltage, charge, flux, field amplitude, or another response; and derive the associated stored-energy measure without hiding frequency or impedance factors in $\kappa$.

**Resolution evidence:** a complete RLC or field-resonator binding with independently calculated gain, a fixed energy convention, and a quasi-static-to-distributed breakdown example.

## Evidence Intake 001 — Field-Amplitude Binding

For a sinusoidal plane wave in vacuum with peak electric-field amplitude $E_0$,

$$
\langle I\rangle
=
\frac12c\varepsilon_0E_0^2,
\qquad
\langle u\rangle
=
\frac12\varepsilon_0E_0^2.
$$

If an independently characterized resonator produces an electric-field response gain $G_E$, then

$$
\langle u_r\rangle
=
\frac12\varepsilon_0(G_EE_0)^2.
$$

This is an established effort-amplitude quadratic relation. It supports the grammar's field binding but does not by itself add a new law: the scientific test remains whether the grammar predicts $G_E$, a bound, or a cross-domain normalized relation beyond the definition of amplitude gain.

Classical field amplitude and photon energy must remain distinct. At fixed frequency, $E_\gamma=h\nu$ fixes the photon energy, while increased classical intensity generally represents increased field energy or photon occupation rather than increased energy per photon.

## Evidence Intake 002 — Canonical Electrical Specialization

For a series RLC circuit,

$$
\omega_0=\frac1{\sqrt{LC}},
\qquad
Q=\frac{\omega_0L}{R}.
$$

With fixed source-voltage amplitude $V_0$, current observed at $\omega_0$, and inductive baseline $I_0=V_0/(\omega_0L)$, $G_I=Q$ and

$$
H_{L,r}=\frac12L(I_0Q)^2.
$$

This $Q^2$ energy scaling is relative to the declared inductive baseline and fixed voltage source; the input power changes with $R$. Under fixed average input power, stored energy is $(Q/\omega_0)P_{\mathrm{in}}$. Capacitor voltage, inductor voltage, current, and field amplitudes require distinct transfer functions and conventions.

## C11 Evidence Role

Electromagnetics is a candidate Tier B realization: its microscopic field mechanism differs from mechanics even though the reduced RLC equations are isomorphic. It can support robustness of the grammar's reduction, but a broader-law test must predict a field-level correction, distributed transition, bound, or failure using information not obtained by fitting the RLC response itself.

## Second-Pass Reduction Contract

The lumped circuit approximation requires electrical dimensions small enough that propagation phase, radiation, and distributed coupling are negligible or represented by explicit elements. The binding must state frequency band, electrical size, parasitic extraction, connector assumptions, and the transition criterion to transmission-line or full-wave modelling.

## Evidence Intake 014 — Gold-Standard R3-v1.0 Certificate

The series RLC circuit is the frozen reference realization. Under fixed peak source voltage, total cycle-mean modal energy at resonance, and current as the flow coordinate,

$$
I_0=\frac{V_0}{\omega_0L},
\qquad G_r=Q=\frac{\omega_0L}{R},
\qquad
\boxed{\mathcal K_{EM,r}=\frac12L(I_0Q)^2}.
$$

The coefficient $1/2$, baseline, and gain are derived before observing resonant current. The independent loss route is $\mathcal K_r=(Q/\omega_0)P_{in}$. The complete protocol, numerical benchmark, failure tests, and uncertainty requirements are in [Resonant Capacity R3 Certificates](../../02-proof/Resonant-Capacity-R3-Certificates.md). Status: `R3-ANALYTICAL-COMPLETE`; empirical replication pending.
