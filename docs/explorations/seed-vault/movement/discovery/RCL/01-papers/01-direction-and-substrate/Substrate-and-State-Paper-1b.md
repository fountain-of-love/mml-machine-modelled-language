# Substrate and State

## How Physical Systems Receive, Hold and Release Energy

### Paper 1b — Developed Draft

**Claim maturity:** Established foundation / planned synthesis.

## Proposition

A physical effect requires a material, field, or state-space substrate capable of receiving, holding, and releasing energy.

## Core Formulas

$$
\boxed{E=\mathcal H(x)}
$$

$$
\boxed{
\Delta E\approx\frac12K_{\mathrm{eff}}(\Delta x)^2
}
$$

## Planned Development

- define substrate and state across the five domains;
- distinguish intrinsic, stored, and accessible capacity;
- treat $E=mc^2$ as the intrinsic neutral-gain anchor of the capacity archetype while distinguishing it from dynamic resonance;
- provide a transposal, drift detector, test, and link to Stage 2.

## Assigned Scientific Concerns

### C02 — Operational meaning of capacity

Define a typed capacity vocabulary rather than one umbrella term. At minimum, distinguish instantaneous stored energy, peak and cycle-mean stored energy, exergy relative to a specified environment, transfer or power capability, and intrinsic capacity. Every later use of $\mathcal K$ must identify one of these meanings together with its state, reference state, boundary, environment, and measurement convention.

### C07 — Rest energy as the intrinsic-capacity anchor

Evaluate $E=mc^2$ as the intrinsic, unamplified binding of the capacity archetype. Because $c$ is an invariant conversion/activation scale rather than a response amplitude, the mapping must distinguish intrinsic activation from dynamic resonant amplification. Its role is to anchor the parent capacity form, not to claim that rest energy is produced by oscillatory resonance.

### C08 — Rigorous origin of local quadratic structure

Replace the scalar heuristic with the multivariable expansion

$$
\Delta E
=
\frac12\,\delta x^{\mathsf T}H_E(x_0)\delta x
+O(\lVert\delta x\rVert^3).
$$

State the required smoothness, stationary reference state, positivity or semidefiniteness of the Hessian, constraints, zero modes, coordinate dependence, and remainder regime. Treat kinetic energy metrics separately from expansions of potential energy or availability.

**Resolution evidence:** a capacity taxonomy, a formal Hessian derivation with assumptions, and explicit examples showing which quantity each domain stores.

## Evidence Intake 001

The proposed family is now separated into four layers:

1. **intrinsic capacity:** $\mathcal K=\kappa S\Psi^2$, with $E_0=mc^2$ admitted only as the case $S=m$, $\Psi=c$, and $\kappa=1$;
2. **modal capacity:** $\mathcal K=\kappa S(\omega A)^2$ for an appropriate rate-side quadratic storage term;
3. **resonantly activated capacity:** $\mathcal K_r=\kappa S(\omega A G_r)^2$ under a specified linear response convention;
4. **bounded realized capacity:** the predicted storage constrained by source energy, material limits, boundaries, dissipation, and nonlinear response.

The first layer establishes an exact intrinsic role binding of the parent capacity archetype. It does not establish an oscillatory mechanism: the invariant speed $c$ is the activation/conversion scale, while neutral gain is $G_r=1$. The later C07 resolution retains this distinction as a permanent role-drift prohibition.

The scalar equilibrium argument is accepted as motivation, but its rigorous target remains

$$
\Delta\mathcal K
=
\frac12\delta x^{\mathsf T}H_{\mathcal K}(x_0)\delta x
+O(\lVert\delta x\rVert^3),
$$

for the appropriate potential at a stationary reference state. Near equilibrium and near resonance are independent qualifiers and must be recorded separately.

## Evidence Intake 002 — Storage Coefficients as Substrate

In the canonical linear grammar, substrate becomes precise through

$$
H(f,q)
=
\frac12\mathcal I f^2
+
\frac{q^2}{2\mathcal C}
=
\frac12\mathcal I f^2
+
\frac12\mathcal C e_{\mathcal C}^2.
$$

Thus $\mathcal I$ is the flow-side storage coefficient and $\mathcal C$ the effort-side storage coefficient. The factor $1/2$ belongs to the quadratic energy convention and should normally be represented by $\kappa=1/2$, rather than folded into the physical substrate.

Resistance is not substrate in this storage sense. It enters the dynamics and limits response by converting energy out of the selected recoverable Hamiltonian.

## Evidence Intake 003 — General Storage States

The coefficients $\mathcal I$ and $\mathcal C$ are local representations of storage functions, not the most general substrates. Under the selected port orientation,

$$
f=\partial_pH_{\mathcal I}(p),
\qquad
e=\partial_qH_{\mathcal C}(q),
\qquad
\dot p=e,
\qquad
\dot q=f.
$$

Quadratic storage follows when these Hamiltonians have locally constant positive Hessians. This connects the elementary grammar directly to C08 instead of treating scalar inertance and compliance as universally constant.

## Evidence Intake 014 — Typed Capacity Contract and C02 Closure

“Capacity” is a family label, not permission to exchange unlike observables. Every quantitative use must select one type:

| Type code | Quantity | Operational definition | Unit |
| --- | --- | --- | --- |
| `H_inst` | instantaneous recoverable stored energy | $H(x(t))$ inside a declared storage boundary | J |
| `H_peak` | peak stored energy | $\max_{t\in W}H(x(t))$ over a declared window or period | J |
| `H_mean` | cycle/time-mean stored energy | $\langle H\rangle_W=|W|^{-1}\int_WH\,dt$ | J |
| `K_mode` | selected modal energy | energy assigned to one normalized mode under a declared partition | J |
| `B` | exergy/availability | maximum useful work relative to a specified environment and constraint set | J |
| `E_intrinsic` | intrinsic energy | state property not requiring resonant activation, such as rest energy | J |
| `P_cap` | transfer or power capability | maximum admissible rate under a stated horizon and constraints | W |
| `K_realized` | bounded realized stored energy | admitted storage after source, material, boundary, loss, and nonlinear limits | J |

`P_cap` is not substituted for an energy merely because both are informally called capacity. Internal energy and exergy likewise remain distinct even though both have units of joules.

The operative R3-v1.0 definition is

$$
\boxed{
\mathcal K_r
=K_{mode,mean}(\omega_0)
=\text{total cycle-mean recoverable energy of one normalized admitted mode at resonance}.
}
$$

Its required metadata are mode/state, storage boundary, reference state, peak-amplitude convention, averaging period, source/load context, and validity regime. The domain bindings are:

| Domain | R3-v1.0 capacity |
| --- | --- |
| Mechanics | mean total kinetic-plus-elastic energy of one mode |
| Electromagnetics | mean total magnetic-plus-electric energy of one RLC mode |
| Acoustics | mean total inertive-plus-compressive energy of one Helmholtz mode |
| Hydraulics | mean total flow-inertive-plus-compliant energy of one line–accumulator mode |
| Thermodynamics | mean total energy of one normalized second-sound mode; Fourier-body exergy remains a separate `B` record and negative control |

Unqualified “capacity” may remain in titles or explanatory prose as a family name, but it cannot enter an equation, comparison, or evidence grade without a type code or explicit equivalent sentence. This satisfies C02. C02 is **closed for the paper series' current quantitative claims**; a future capacity type requires a new typed definition rather than reinterpretation of $\mathcal K_r$.

## Evidence Intake 015 — Intrinsic Rest-Energy Binding and C07 Closure

The capacity archetype admits the exact intrinsic binding

$$
\boxed{
\mathcal K
=\kappa\Sigma(\Psi G_r)^2
=1\cdot m(c\cdot1)^2
=mc^2.
}
$$

Its roles are frozen as:

| Archetype role | Relativistic binding |
| --- | --- |
| Capacity $\mathcal K$ | rest energy $E_0$ |
| Substrate $\Sigma$ | invariant mass $m$ |
| Activation scale $\Psi$ | invariant conversion scale $c$ |
| Gain $G_r$ | neutral gain $1$; no amplification required |
| Convention coefficient $\kappa$ | $1$, fixed by the exact relativistic identity |

This is the pure intrinsic member of the family: substrate already carries capacity through the universal squared conversion scale. It does not require external forcing, a cavity, a frequency match, or amplitude build-up. Dynamic resonators are activated members in which $G_r\ne1$ can amplify the relevant effort/flow coordinate.

The distinction is therefore between **intrinsic binding** and **dynamic resonant binding**, not between “binding” and “no binding.” The R3-v1.0 modal protocol retains $\kappa=1/2$ because it measures peak-activation/cycle-mean modal energy; the intrinsic relativistic certificate uses $\kappa=1$. This is a declared difference of capacity type and convention, not a fitted discrepancy.

The established relativistic derivation supplies the identity, and the grammar supplies its role-preserving placement. A classical or internal-oscillation interpretation of $c$ is not assumed in closing C07, but is retained below as H-RR with $c$ specifically typed as a generalized **rate amplitude**, not a displacement or frequency. C07 is **closed as a positive intrinsic-capacity binding with neutral gain**; the stronger origin hypothesis is governed separately by C16.

### Derivation of the neutral gain

The value $G_0=1$ is derived rather than fitted. Start from the Lorentz-invariant energy–momentum relation for a massive system,

$$
E^2=p^2c^2+m^2c^4.
$$

In its rest frame $p=0$. Selecting the positive-energy branch gives $E_0=mc^2$. Define the intrinsic multiplier occupying the squared-gain role by

$$
G_0^2:=\frac{E_0}{\kappa\Sigma\Psi^2}.
$$

Using the independently fixed intrinsic bindings $\kappa=1$, $\Sigma=m$, and $\Psi=c$,

$$
G_0^2
=\frac{mc^2}{1\cdot mc^2}
=1,
\qquad
\boxed{G_0=1}
$$

under the non-negative gain convention. Thus unity follows from the invariant rest-energy relation and the role binding.

This quotient is not offered as a new prediction of relativity; it is a consistency and uniqueness test for embedding the established identity in the capacity grammar. With $\kappa$, $\Sigma$, and $\Psi$ fixed as above, any value other than $G_0=1$ would contradict $E_0=mc^2$.

The same value is required compositionally. If gain is the norm ratio of an activation-transfer map $T$,

$$
G(T;\Psi)=\frac{\lVert T\Psi\rVert}{\lVert\Psi\rVert},
$$

then intrinsic capacity has no intervening amplification stage, so $T=T_{id}$. Since $T_{id}\Psi=\Psi$, $G(T_{id};\Psi)=1$. Unity is the neutral element required for multiplicative composition: inserting a no-change stage cannot alter capacity.

This is a representation of **no additional activation transformation**, not evidence that a physical resonator operates at rest. The derivation applies to massive systems admitting a rest frame and the positive-energy branch. Massless excitations have no rest-frame binding of this form. Moving massive states require a separately named kinematic factor and cannot be relabelled resonant gain without a further derivation. The energy–momentum invariant is standard; see the [Particle Data Group Kinematics Review](https://pdg.lbl.gov/2025/web/viewer.html?file=..%2Freviews%2Frpp2025-rev-kinematics.pdf).

## Evidence Intake 016 — Strong Relativistic Resonance Hypothesis

The programme does not exclude the stronger possibility that rest energy has an underlying coherent or resonant realization. It states it as a separate hypothesis:

> **H-RR:** A massive system possesses a Lorentz-covariant rest-frame periodic or phase-coherent degree of freedom whose independently derived generalized rate amplitude is $c$ and whose complete, non-overlapping storage functional is $mc^2$.

Quantum-relativistic phase supplies a concrete discovery route. Combining rest energy with the Planck relation gives the Compton angular frequency and reduced Compton length,

$$
\omega_C=\frac{mc^2}{\hbar},
\qquad
\bar\lambda_C=\frac{\hbar}{mc},
$$

so

$$
\boxed{\omega_C\bar\lambda_C=c}.
$$

This permits a precise candidate interpretation: if a rest-frame coordinate has characteristic amplitude $A_C=\bar\lambda_C$ and angular rate $\omega_C$, its peak generalized rate is $\omega_CA_C=c$. In that qualified sense, $c$ can occupy the **rate-amplitude** role of the capacity grammar. It is not dimensionally a displacement amplitude.

The free massive quantum phase $\exp(-i\omega_C\tau)$ and matter-wave-clock literature motivate the periodicity question; they do not by themselves demonstrate a localized classical oscillator or show that a resonator generates invariant mass. Matter-wave work explicitly relates massive-particle phase accumulation to $\omega_C=mc^2/\hbar$ ([Matter-Wave Clocks](https://opg.optica.org/abstract.cfm?uri=IQEC-2013-IC_2_5)), while the interpretation of atom interferometers as direct Compton clocks has been debated ([Wolf et al.](https://arxiv.org/abs/1012.1194)).

### Non-circular proof contract

H-RR is supported only if a model independently provides:

1. a physical state or field coordinate, not only a rewritten energy identity;
2. a Lorentz-covariant action and transformation law;
3. independently derived $A_C$, $\omega_C$, substrate metric, topology, and boundary conditions;
4. a positive storage functional whose mutually exclusive components sum to $mc^2$ without choosing a coefficient to force the result;
5. recovery of $E^2=p^2c^2+m^2c^4$ and the correct moving-state behavior;
6. an explanation of whether “resonance” means stationary phase coherence, reversible exchange between stores, an eigenmode, or driven amplification;
7. at least one discriminating consequence not obtained merely by substituting $E=mc^2$ into $E=\hbar\omega$.

A simple harmonic ansatz $x_C=\bar\lambda_C\cos\omega_C\tau$ establishes $|\dot x_C|_{max}=c$ algebraically, but a one-store/one-mode energy $\tfrac12mc^2$ does not yet recover the full rest energy. The missing factor cannot be inserted into $\kappa$ post hoc. A successful theory must derive the complementary store, additional degree of freedom, substrate normalization, or a different relativistic Hamiltonian structure that supplies the complete ledger.

### Failure criteria

The strong hypothesis fails in a proposed realization if its periodic coordinate is gauge-only or unobservable in principle, its mass is inserted as an unexplained parameter that already contains the target energy, its storage terms overlap, Lorentz invariance is broken, the construction applies only in one preferred frame, or all alleged consequences reduce identically to established dispersion and phase relations.

H-RR is therefore **included as a hypothesis-generating research branch**. It is not used to establish the already closed intrinsic binding, and it does not yet count as an R3 or R4 certificate.

The full established binding, both neutral-gain derivations, and the separate H-RR proof contract are consolidated in [Paper 1c — Einstein, Relativity, and the Intrinsic Capacity Binding](Einstein-Relativity-Capacity-Mapping-Paper-1c.md).
