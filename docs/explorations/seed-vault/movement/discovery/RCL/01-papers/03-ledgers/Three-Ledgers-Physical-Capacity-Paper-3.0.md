# The Three Ledgers of Physical Capacity

## Energy, Entropy and Exergy as a Universal Mediating Triad

### Paper 3 / 3.0 — Developed Draft

> This document is a developed working draft. Its equations, scope, provenance, maturity assignments, and novelty boundary remain subject to review.

## Central Question

> Why is energy conservation alone insufficient to describe physical transformation?

## Core Proposition

A transformation must be evaluated through three simultaneous ledgers:

1. the quantity of energy;
2. the irreversibility of its redistribution;
3. the remaining capacity to perform useful work.

| Ledger | Governing question | Fundamental behaviour |
| --- | --- | --- |
| **Energy** | How much physical capacity exists? | Conserved |
| **Entropy** | How irreversibly has that capacity been dispersed? | Generated |
| **Exergy** | How much useful work can still be extracted? | Consumed or destroyed |

The scientific heart of the triad is:

$$
\boxed{
\text{Energy is conserved}
\qquad
\text{Entropy is generated}
\qquad
\text{Exergy is destroyed}
}
$$

## Core Equations

Energy balance:

$$
\boxed{
\frac{dE}{dt}
=
P_{\mathrm{in}}-P_{\mathrm{out}}
}
$$

Entropy balance:

$$
\boxed{
\frac{dS}{dt}
=
\dot S_{\mathrm{in}}
-
\dot S_{\mathrm{out}}
+
\dot S_{\mathrm{gen}},
\qquad
\dot S_{\mathrm{gen}}\geq0
}
$$

Exergy balance in the stated reference environment:

$$
\boxed{
\frac{dB}{dt}
=
\dot B_{\mathrm{in}}
-
\dot B_{\mathrm{out}}
-
T_0\dot S_{\mathrm{gen}}
}
$$

The coupling relation is:

$$
\boxed{
B_{\mathrm{destroyed}}
=
T_0S_{\mathrm{generated}}
}
$$

## One-Sentence Claim

> Energy records what remains, entropy records what became irreversible, and exergy records what can still become purposeful action.

## Role in the Spiral

This paper introduces the triad. Papers 3.1, 3.2, and 3.3 each unfold one of its voices.

| Spiral stage | Triadic contribution |
| ---: | --- |
| **1b Substrate** | Energy establishes what can be held |
| **2 Tension** | Gradients create possible transfer |
| **3 Mediation** | Energy, entropy, and exergy evaluate the transformation |
| **5 Functions** | The five domains instantiate the three ledgers differently |
| **8 Governance** | Entropy and exergy constrain valid resonant-capacity claims |
| **13 Return** | Useful capacity returns as work, organization, or environmental dissipation |

The triad belongs at stage 3 but governs the stages that follow.

## The Triad as Three Dances

| Paper | Dance | Movement |
| --- | --- | --- |
| Energy | **Persistence dance** | storage ↔ transfer ↔ transformation |
| Entropy | **Irreversibility dance** | concentration ↔ dispersion ↔ generation |
| Exergy | **Purposeful-capacity dance** | availability ↔ work ↔ destruction |

Together:

$$
\boxed{\text{Energy}\rightarrow\text{what exists}}
$$

$$
\boxed{\text{Entropy}\rightarrow\text{what cannot be undone}}
$$

$$
\boxed{\text{Exergy}\rightarrow\text{what can still be done}}
$$

## Later Synthesis

A later second-spiral synthesis may be titled:

**Conservation, Irreversibility and Usefulness: A Three-Ledger Foundation for Resonant Physical Capacity**

It may incorporate feedback from the three dedicated papers and connect the triad formally to the five-domain maturity matrix.

## Evidence Intake 001 — Ledger Discipline

The nested capacity family is admissible only if all three ledgers refer to the same boundary, environment, and time interval. The energy ledger records storage, boundary power, conversion, and exported energy. The entropy ledger separates entropy transfer from non-negative internal production. The exergy ledger evaluates useful-work potential relative to a declared environment and records destruction as $T_0\dot S_{\mathrm{gen}}$.

The compact exergy balance is a reduced form. A complete open-system treatment may require work, heat-transfer exergy factors, material streams, kinetic, potential, and chemical exergy, and environmental-reference terms. These may be grouped into $\dot B_{\mathrm{in}}$ and $\dot B_{\mathrm{out}}$ only when explicitly defined.

The ledgers prevent three drifts: field or modal energy is not automatically exergy; attenuation is not automatically entropy generation when energy leaves through a boundary port; and resonance may increase stored energy while exergy efficiency falls because sustaining losses also increase.

## Evidence Intake 002 — Auditing the Canonical Resonator

The canonical $\mathcal I$–$\mathcal C$–$\mathcal R$ derivation is distributed across the ledgers as follows:

| Derived quantity | Energy ledger | Entropy ledger | Exergy ledger |
| --- | --- | --- | --- |
| $H=\tfrac12\mathcal I f^2+q^2/(2\mathcal C)$ | Stored recoverable Hamiltonian | No entropy meaning by itself | Exergy only if an extraction process and environment make it useful |
| $P_{\mathcal R}=\mathcal Rf^2$ | Conversion out of the selected Hamiltonian | Produces entropy only when irreversibly thermalized within the boundary | Destroys exergy by $T_0\dot S_{\mathrm{gen}}$ under the reference environment |
| Boundary radiation or transmitted power | Energy output | Entropy transfer may accompany it; not automatically generation | Exergy output must be accounted for separately |
| $Q=\omega_0H/P_{\mathrm{loss}}$ | Storage-to-loss ratio | Entropy form is conditional on the loss mechanism | Does not by itself measure exergy efficiency |

Thus the derived resonant-storage result is first an energy statement. “Accessible,” “usable,” and “sustainable” are admitted only after the entropy and exergy ledgers close over the same process.

## Evidence Intake 003 — Thermal Analogy Ledger Check

The thermal RC pair $(\Delta T,\dot Q)$ is an engineering analogy, not a power-conjugate bond. The three-ledger grammar therefore records it as follows:

| Model view | Energy ledger | Entropy ledger | Exergy ledger |
| --- | --- | --- | --- |
| Engineering RC | $\dot Q$ enters the heat balance and $C_{\mathrm{th}}\dot T$ changes internal energy | Entropy must be calculated separately | Exergy is not obtained from $\Delta T\dot Q$ |
| Energetic thermal port | $P=T\dot S_{\mathrm e}$ | $\dot S_{\mathrm e}$ is boundary entropy transfer | Relative exergy transfer is $(T-T_0)\dot S_{\mathrm e}$ under the reversible port interpretation |

This prevents a useful signal-flow analogy from silently acquiring incorrect power units or thermodynamic meaning.
