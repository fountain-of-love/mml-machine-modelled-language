# Mechanics as the Reference Dialect

## Mass, Spring, Damper and the Architecture of Simplicity

### Paper 5.1 — Developed Draft

**Claim maturity:** Established foundation / interpretive synthesis.

## Proposition

Mechanics appears especially simple because its lumped alphabet has become the culturally canonical reference for physical-system analogy.

The sharper claim is that mechanics is not uniquely simple: mass–spring–damper notation is simply the clearest and most widely taught low-dimensional dialect.

The existence and compactness of the mechanical model are established. The comparative claim about how clearly or widely it is taught is an interpretive pedagogical hypothesis unless supported by curriculum or textbook analysis; it is not needed for the physical transposition.

## Core Relations

$$
F=m\dot v,
\qquad
F=kx,
\qquad
F=bv.
$$

## Planned Development

- bind inertance, compliance, and resistance mechanically;
- separate physical simplicity from pedagogical familiarity;
- provide transposal, drift detector, imputation opportunity, and test.

## Assigned Scientific Concerns

This paper supplies the mechanical reference binding for **C01, C04, C06, C08, and C09**. It must derive stored energy and frequency response from a stated oscillator model, define whether force, displacement, velocity, or power is controlled, derive $G_r$ from independently specified mass, stiffness, damping, forcing frequency, and boundary conditions, and distinguish kinetic from potential and total modal energy.

**Resolution evidence:** one fully specified linear test, one nonlinear or saturation breakdown case, and one result that clarifies whether the proposed relation adds predictive content beyond standard oscillator theory.

## Evidence Intake 001 — Mechanical Dual Storage

For a linear oscillator,

$$
H(x,v)=\frac12mv^2+\frac12kx^2
=\frac12mv^2+\frac{1}{2k}F_s^2,
\qquad F_s=kx.
$$

The effort-side expression uses spring force $F_s$, not an arbitrary applied force. Under $x=A\cos\omega t$, $\tfrac12m(\omega A)^2$ is peak kinetic energy and $\tfrac12kA^2$ is peak elastic energy. They are equal for a free linear normal mode with $\omega^2=k/m$; a forced off-resonance response requires both terms and its particular solution.

$G_r$ must name a transfer function such as displacement/force or velocity/force relative to a declared baseline. Holding response amplitude fixed is not the same experiment as holding source-force amplitude fixed.

## Evidence Intake 002 — Canonical Mechanical Specialization

For $m\dot v+bv+kx=F_s$ with $\dot x=v$,

$$
\omega_0=\sqrt{k/m},
\qquad
Q=\frac{m\omega_0}{b}.
$$

With fixed force amplitude $F_0$, velocity observed at $\omega_0$, and inertive baseline $v_0=F_0/(m\omega_0)$, the velocity gain is $Q$ and

$$
K_r=\frac12m(v_0Q)^2.
$$

Under fixed average mechanical input power, total stored energy instead satisfies $H=(Q/\omega_0)P_{\mathrm{in}}$ at steady state. These statements require linear viscous damping; Coulomb friction, amplitude-dependent damping, and nonlinear stiffness change the response.

## C11 Evidence Role

Mechanics is the reference realization used to construct and explain the canonical grammar. It is therefore part of the derivation set, not an out-of-sample confirmation. Its C11 role is to freeze notation, protocols, and predicted failure boundaries before the grammar is applied elsewhere.

## Evidence Intake 003 — Element Persistence and Junction Laws

For the isolated ideal inertance element, $F=0$ implies constant velocity. For the complete lossless mass–spring system, however, the state does not remain constant: energy circulates between kinetic and elastic storage. “Persistence” must therefore be stated at the element or conserved-energy level, not as a universal static-state rule.

Likewise, common-velocity force balance in a bond graph is an ideal interconnection constraint. It is related to mechanical equilibrium and action–reaction structure, but the domain-neutral 0- and 1-junction equations should not be presented as new low-dimensional versions of Newton's three laws.

## Second-Pass Reduction Contract

The mass–spring–damper model must identify whether it represents a rigid body, one structural mode, or a reduced flexible system. Its adequacy band ends when neglected modes, geometric nonlinearity, distributed inertia, contact, or non-viscous loss materially change the response. Mechanics is elementary only after this reduction has been justified.
