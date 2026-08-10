# Thermodynamics as the Asymmetric Dialect

## Exergy, Relaxation and the Candidate Missing Inertance

### Paper 5.2 — Developed Draft

**Claim maturity:** Established diffusive model / candidate extension.

## Proposition

Ordinary thermal RC models form a primarily diffusive branch. In a power-conjugate temperature–entropy-flow formulation they do not normally contain the complementary passive inertive store of the canonical resonator; extended heat-flux theories may introduce an inertance-like state under additional assumptions.

## Core Formulas

$$
C_{\mathrm{th}}\dot T+\frac{T-T_0}{R_{\mathrm{th}}}=P_s
$$

$$
\boxed{
B_T\approx\frac{C_{\mathrm{th}}}{2T_0}(\Delta T)^2
}
$$

## Planned Development

- distinguish energy, entropy, and exergy bindings;
- derive the near-equilibrium availability approximation;
- evaluate finite heat-flux relaxation as candidate inertance;
- state drift detectors, tests, and invalid transposals.

## Assigned Scientific Concerns

### C05 — Thermodynamics as an asymmetric or negative binding

Derive the constant-heat-capacity availability relation before taking its near-equilibrium limit, for example

$$
B_T
=
C_{\mathrm{th}}
\left[
(T-T_0)-T_0\ln\!\left(\frac{T}{T_0}\right)
\right]
\approx
\frac{C_{\mathrm{th}}}{2T_0}(\Delta T)^2.
$$

Keep internal energy, entropy production, and exergy distinct. Classical Fourier conduction must not be labelled resonant. A resonant binding requires a stated oscillatory theory and regime—such as a supported heat-flux relaxation, second-sound, or thermoacoustic model—with independently defined input and response gain. If no defensible binding results, retain thermodynamics as explicit negative evidence.

This paper also provides the thermal evidence required by **C02, C04, C08, and C09**.

**Resolution evidence:** an exact derivation and assumptions, a justified oscillatory model or documented structural absence, entropy-production closure, and a falsifiable experiment or simulation protocol.

## Evidence Intake 001 — Exact Effort Form and Candidate Flow Form

For a uniform body with approximately constant heat capacity, no phase change, and environment temperature $T_0$, the effort-side physical exergy is

$$
B_T
=
C_{\mathrm{th}}
\left[
(T-T_0)-T_0\ln\!\left(\frac{T}{T_0}\right)
\right].
$$

For $T=T_0+\Delta T$ with $|\Delta T|\ll T_0$,

$$
B_T
=
\frac{C_{\mathrm{th}}}{2T_0}(\Delta T)^2
+O\!\left(\frac{|\Delta T|^3}{T_0^2}\right).
$$

This closes the derivational part of C05 for the thermal effort form, while leaving environmental assumptions and entropy generation explicit. A gain $G_T$ may be applied to a temperature response only after a source, baseline, transfer function, and oscillatory thermal model have been specified.

For a lumped Maxwell–Cattaneo relaxation model,

$$
\tau_q\frac{d\dot Q}{dt}+\dot Q=\frac{\Delta T}{R_{\mathrm{th}}},
$$

and, near $T_0$ with $f_T=\dot S\approx\dot Q/T_0$,

$$
\Delta T=L_T\dot f_T+R_Sf_T,
\qquad
L_T=\tau_qR_{\mathrm{th}}T_0,
\qquad
R_S=R_{\mathrm{th}}T_0.
$$

This establishes an inertance-like **constitutive form**, not yet an established stored-exergy term. The candidate

$$
B_{T,f}^{\mathrm{candidate}}
=
\frac12L_T\dot S^2
=
\frac{\tau_qR_{\mathrm{th}}}{2T_0}\dot Q^2
$$

must be derived from a thermodynamically consistent extended entropy, free-energy, exergy, or passivity balance before being promoted. Dimensional closure alone is insufficient. Its Fourier limit $\tau_q\to0$ is a useful degeneracy test, but not proof of the storage interpretation.

**Updated maturity:** exact effort-side exergy — established under stated assumptions; Maxwell–Cattaneo relaxation — established model class; flow-side exergy storage and universal interpretation — imputed.

## Evidence Intake 002 — Why Ordinary Thermal Dynamics Is a Boundary Case

The ordinary lumped model

$$
C_{\mathrm{th}}\dot T+\frac{T-T_\infty}{R_{\mathrm{th}}}=P_s
$$

has one state-storage term and one dissipative transfer term. Its homogeneous response is first-order relaxation, not passive oscillation, and it has no canonical counterpart to

$$
\omega_0=\frac1{\sqrt{\mathcal I\mathcal C}}.
$$

Therefore no $G_T=Q$ substitution is admissible for this ordinary model. A periodic temperature transfer function can attenuate and phase-shift forcing but has no resonant peak. Thermal resonance requires added coupled states or a supported hyperbolic, thermoelastic, thermoacoustic, phase-change, or feedback mechanism.

The near-equilibrium quadratic expression belongs to exergy, not internal energy:

$$
\Delta U=C_{\mathrm{th}}\Delta T,
\qquad
B_T\approx\frac{C_{\mathrm{th}}}{2T_0}(\Delta T)^2.
$$

Thus thermodynamics remains a scientifically useful asymmetric and potentially negative binding for the ordinary passive grammar.

## C11 Evidence Role

Ordinary lumped thermodynamics is the programme's strongest negative control: the grammar should predict relaxation and the structural absence of passive $\mathcal I$–$\mathcal C$ resonance rather than force a filled cell. If a Maxwell–Cattaneo, second-sound, thermoelastic, or thermoacoustic realization is later tested, it becomes a separate model with additional states and must not be used retroactively to claim that ordinary Fourier thermodynamics was resonant.

A successful prediction of this absence and of the operator needed to leave the Fourier limit would support the grammar's diagnostic value. It would not alone establish a universal resonant law.

## Evidence Intake 003 — Thermal RC and Energetic Variables

The established thermal RC model is

$$
C_{\mathrm{th}}\dot T
=P_s-\frac{T-T_\infty}{R_{\mathrm{th}}},
\qquad
\tau=R_{\mathrm{th}}C_{\mathrm{th}}.
$$

For constant coefficients and zero source after $t=0$,

$$
T(t)-T_\infty
=
[T(0)-T_\infty]e^{-t/\tau}.
$$

Here $P_s$ and the resistance flow are heat rates in an engineering balance. This model is valid, but its temperature–heat-rate analogy is not a power bond.

For energetic bond graphs,

$$
e_T=T,
\qquad
f_T=\dot S_{\mathrm e},
\qquad
P=T\dot S_{\mathrm e}.
$$

Near $T_0$, the linearized storage and resistance relations become

$$
\dot S\approx\frac{C_{\mathrm{th}}}{T_0}\dot T,
\qquad
\Delta T\approx R_{\mathrm{th}}T_0\dot S.
$$

Therefore $C_{\mathrm{th}}$ is the engineering heat-rate/temperature storage coefficient, while $C_{\mathrm{th}}/T_0$ is the near-environment effort-side exergy compliance for the conjugate pair $(\Delta T,\dot S)$.

The formal equation

$$
I_{\mathrm{th}}\ddot q+R_{\mathrm{th}}\dot q+q/C_{\mathrm{th}}=\Delta T_s
$$

is not admitted merely by analogy. It requires a declared state $q$, conjugate variables, topology, dimensions, and a thermodynamically consistent storage functional. Maxwell–Cattaneo supplies heat-flux relaxation, but the corresponding domain-neutral $I$-element interpretation remains a candidate.

## Second-Pass Robustness — Passive RC Networks

Adding ordinary thermal capacitances creates a higher-order RC network but not automatically an oscillator. For a reciprocal passive linear conduction network,

$$
\mathbf C\dot{\boldsymbol\theta}
=-\mathbf G\boldsymbol\theta,
$$

with $\mathbf C\succ0$ and symmetric $\mathbf G\succeq0$, the dynamics are similar to

$$
-\mathbf C^{-1/2}\mathbf G\mathbf C^{-1/2},
$$

whose eigenvalues are real and non-positive. Its modes relax without passive oscillation. Complex or oscillatory thermal behavior requires delayed flux, non-reciprocal transport, feedback, coupling to another storage domain, or another additional state structure.

For a single isothermal lump, internal conduction must equilibrate much faster than boundary heat transfer; a small Biot number is a common adequacy criterion. When that approximation fails, the usual remedy is a validated multi-node or distributed thermal model, not an assumed passive thermal inertance.

## Evidence Intake 010 — Source Support for the Asymmetry

Thoma identifies absolute temperature and entropy flow as the thermal power pair and distinguishes entropy flow in conduction from entropy convection: [DOI 10.1016/0016-0032(71)90198-0](https://doi.org/10.1016/0016-0032(71)90198-0). Lohmayer, Kotyczka, and Leyendecker interpret dissipative port-Hamiltonian storage exergetically and encode first- and second-law restrictions structurally: [Exergetic Port-Hamiltonian Systems](https://arxiv.org/abs/2008.04091).

These sources support the two-dialect correction, exergy ledger, and refusal to treat $(\Delta T,\dot Q)$ as a physical power bond. They do not establish a passive thermal resonator or $G_r$; thermodynamics remains an asymmetric/negative-control result unless independently supported oscillatory dynamics are added.

## Evidence Intake 011 — Positive Resonant Branch Through Second Sound

The independently supported oscillatory dynamics now have a concrete candidate: second sound. In superfluids, the normal component carries entropy while the superfluid component does not; their out-of-phase motion supports a temperature/entropy wave. The two-fluid variational formulation contains quadratic kinetic terms in the two displacement fields and quadratic thermodynamic terms in density and entropy fluctuations: [Second sound with ultracold atoms](https://doi.org/10.1007/s43673-022-00055-2).

Second-sound cavity resonance is not merely hypothetical. Resonance curves have been used to infer velocity and viscosity in helium II ([resonator analysis](https://doi.org/10.1016/0378-4363(81)90175-3)), and parametric cavity experiments report predicted thresholds, strong amplification, geometry dependence, attenuation, and nonlinear saturation ([Rinberg & Steinberg](https://doi.org/10.1103/PhysRevB.64.054506)).

### Two-case thermal design

| Thermal case | Role |
| --- | --- |
| Passive reciprocal Fourier RC network | Negative control: quadratic exergy may exist locally, but no passive resonant gain |
| Linear second-sound cavity below nonlinear threshold | Positive candidate: paired reversible stores, temperature/entropy wave, resonance, damping, and measurable gain |

### Modal binding to derive

Project the established two-fluid quadratic functional onto one normalized second-sound mode:

$$
H_2=\frac12M_2\dot a_2^2+\frac12K_2a_2^2.
$$

For a flow-side test,

$$
\mathcal K_{T,r}=\frac12M_2(\dot a_{2,0}G_2)^2.
$$

$M_2$, the mode normalization, source coupling, attenuation, and $G_2$ must be derived independently from two-fluid properties, geometry, boundaries, and linewidth. Temperature amplitude may be used only after its mapping to $a_2$ and the corresponding effort-side compliance are derived.

This is a genuine thermodynamic-mode candidate, but its fluid/acoustic embodiment must be declared under C06. It can complete the five-dialect representation theorem without being counted as a wholly independent fifth microscopic confirmation.

## Evidence Intake 014 — Frozen Second-Sound Transposition

R3-v1.0 applies without redefining a primitive after projecting one two-fluid eigenmode onto $a_2$ and defining its conjugate source effort $F_2$ so that $F_2\dot a_2$ is modal input power:

$$
f_{2,0}=\frac{F_{2,0}}{\omega_2M_2},
\qquad
G_r=Q_2=\frac{\omega_2M_2}{R_2},
\qquad
\boxed{\mathcal K_{T,r}=\frac12M_2(f_{2,0}Q_2)^2}.
$$

The protocol is complete, but the certificate is not yet analytically complete for a physical apparatus: eigenfunction normalization, $M_2$, $K_2$, heater coupling, $R_2$, thermometer mapping, and boundary leakage must be extracted independently for one selected cavity. See [Resonant Capacity R3 Certificates](../../02-proof/Resonant-Capacity-R3-Certificates.md). Fourier RC remains the negative control.

## C05 Resolution

C05 required either a justified oscillatory thermal model or an explicit negative/asymmetric result while preserving thermodynamic distinctions. Both branches are now supplied:

1. the exact constant-heat-capacity exergy and its near-environment quadratic limit are derived with environment and approximation stated;
2. internal energy, exergy, entropy production, and engineering heat-rate storage remain distinct;
3. ordinary passive Fourier RC is a one-store relaxation and remains the negative control;
4. second sound supplies a supported positive oscillatory branch with paired quadratic modal storage, damping, resonance, and the frozen R3-v1.0 protocol;
5. passage from Fourier conduction to second sound requires additional two-fluid states and cannot be achieved by relabelling relaxation time as gain;
6. amplitude, linewidth, power, boundary, and nonlinear-threshold checks make the positive branch falsifiable.

The remaining apparatus-specific extraction of $M_2$, $K_2$, $R_2$, source coupling, and observation mapping is a certificate-completion obligation under C04, not an unresolved ambiguity about the admissible thermodynamic branches. C05 is **closed at the model-selection and thermodynamic-consistency level**.
