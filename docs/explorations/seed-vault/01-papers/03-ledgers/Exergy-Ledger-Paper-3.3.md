# The Exergy Ledger

## Useful Capacity, Environmental Reference and the Limits of Transformation

### Paper 3.3 — Developed Draft

> This document is a developed working draft. Its equations, scope, provenance, maturity assignments, and novelty boundary remain subject to review.

## Central Question

> How much of conserved energy can still produce an organized effect?

## Core Proposition

Exergy measures useful physical capacity relative to a specified environment. Unlike energy, it is destroyed by irreversibility.

## Core Formulas

$$
\boxed{
B_{\mathrm{destroyed}}
=
T_0S_{\mathrm{generated}}
}
$$

A general balance in the stated reference environment is:

$$
\boxed{
\dot B
=
\dot B_{\mathrm{in}}
-
\dot B_{\mathrm{out}}
-
T_0\dot S_{\mathrm{gen}}
}
$$

Near thermal equilibrium:

$$
\boxed{
B_T
\approx
\frac{C_{\mathrm{th}}}{2T_0}
(\Delta T)^2
}
$$

This expression places thermal useful capacity inside the same local quadratic family as mechanical, acoustic, and electromagnetic storage.

## One-Sentence Claim

> Exergy is not energy itself, but energy's remaining ability to become directed action within a particular environment.

## Drift Detector

> Is useful capacity being inferred from energy quantity alone, without considering entropy generation or the reference environment?

## Connection to Resonant Capacity

A governed version of the Resonant Capacity Law is provisionally:

$$
\boxed{
B_r
=
\kappa\Sigma(\Psi G_r)^2
-
T_0\Delta S_{\mathrm{gen}}
}
$$

More generally:

$$
\boxed{
B_{\mathrm{realized}}
=
B_{\mathrm{activated}}
-
B_{\mathrm{destroyed}}
}
$$

where

$$
B_{\mathrm{destroyed}}
=
T_0\Delta S_{\mathrm{gen}}.
$$

This turns the Resonant Capacity Principle from an amplification formula into a candidate available-capacity formula.

The reduced subtraction is not a universal constitutive law. It is valid only when supplied or initial exergy, accumulation, useful output, exported exergy, and destruction are evaluated over the same process boundary and interval.

## Dance

**Purposeful-capacity dance:** availability ↔ work ↔ destruction.

## Evidence Intake 001 — Exact Thermal Exergy and Resonant Accounting

For a uniform body of approximately constant heat capacity, with no phase change and environment $T_0$,

$$
B_T
=
C_{\mathrm{th}}
\left[(T-T_0)-T_0\ln\!\left(\frac{T}{T_0}\right)\right].
$$

Its local expansion is

$$
B_T
=
\frac{C_{\mathrm{th}}}{2T_0}(\Delta T)^2
+O\!\left(\frac{|\Delta T|^3}{T_0^2}\right).
$$

A temperature-response gain may be inserted only after an oscillatory model defines that response. Outside the local regime, the exact logarithmic expression replaces the quadratic approximation. The candidate heat-flux-memory term in Paper 5.2 remains imputed until derived from a consistent nonequilibrium potential or passivity balance.

For a resonant process, the conceptual balance is

$$
\Delta B_{\mathrm{system}}
=B_{\mathrm{in}}-B_{\mathrm{useful\ out}}-B_{\mathrm{other\ out}}-T_0S_{\mathrm{gen}},
$$

with signs and stream terms adapted to the boundary. Resonance changes state trajectories and transfer rates; it does not create exergy.

## Evidence Intake 002 — Stored Energy versus Recoverable Capacity

The canonical $\mathcal I$–$\mathcal C$–$\mathcal R$ derivation first predicts stored Hamiltonian energy. Calling that quantity accessible or usable requires an extraction process and environment. Stored energy may be highly recoverable in an ideal mechanical, acoustic, electrical, or hydraulic model, but recoverability is not guaranteed by amplitude alone.

The qualified grammar therefore separates

$$
\text{quadratic storage: energy present in the selected mode}
$$

from

$$
\text{exergy: maximum useful work relative to an environment}.
$$

Resistance affects both resonant response and exergy destruction. A high-$Q$ state can contain more stored energy under one source protocol without implying greater overall exergy efficiency.
