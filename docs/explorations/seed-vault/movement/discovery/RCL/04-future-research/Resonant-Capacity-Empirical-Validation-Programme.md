# Resonant Capacity Empirical Validation Programme

## Optional R4 and apparatus-level extension

### Status

Deferred experimental programme. This document preserves the apparatus, calibration, uncertainty, and held-out-test work that is not required to prove the analytical representation theorem in Paper 0.

## 1. Separation from the analytical proof

Paper 0 proves a conditional representation theorem from closed systems of equations. That proof requires governing dynamics, positive quadratic storage, frozen role bindings, a derived same-coordinate gain, dimensional closure, and explicit exclusions. It does not require construction or retrospective reconstruction of a particular laboratory apparatus.

This document asks the stronger optional questions:

1. Do apparatus-level measurements agree with the analytical child models within declared uncertainty?
2. Does the grammar derive a held-out invariant, correction, exclusion, missing operator, or failure boundary not already guaranteed by class membership and the standard child model?

The first is empirical validation of the representation. The second is the R4 route toward a broader empirical-law claim.

## 2. General apparatus certificate

An empirical certificate should freeze before target measurement:

- realization and geometry;
- equilibrium state and material functions;
- source and detector locations;
- effort, flow, and power-conjugacy convention;
- mode normalization and storage coefficients;
- source-to-mode and mode-to-detector transfer operators;
- independent damping or linewidth route;
- target observable and uncertainty model;
- linearity, modal-isolation, boundary, and saturation limits;
- rejection criteria.

The target steady resonant amplitude may validate the derivation but may not be used to determine the source overlap, damping, gain, or $\kappa$ that generates it.

## 3. Second-sound apparatus programme

### 3.1 Reference realization

Use a straight, closed, constant-area He-II cavity of length $D$ and area $A$, held at equilibrium temperature $T_0$, with a planar heater at $x=0$ and calibrated thermometer at $x=D$. The closed one-dimensional cavity is the reference realization. Finite open plates are a correction case because diffraction introduces frequency-dependent leakage and resonance shifts.

For $\rho=\rho_s+\rho_n$, zero leading-order mass current gives

$$
\rho_sv_s+\rho_nv_n=0,
$$

and relative counterflow $w=v_n-v_s$ has kinetic density

$$
\frac12\rho_sv_s^2+\frac12\rho_nv_n^2
=
\frac12\frac{\rho_s\rho_n}{\rho}w^2.
$$

Under the standard second-sound decoupling approximation,

$$
h_2
=
\frac12\frac{\rho_s\rho_n}{\rho}w^2
+
\frac12\frac{\rho c_p}{T_0}(\delta T)^2,
$$

$$
c_2^2
=
\frac{\rho_s}{\rho_n}\frac{s^2T_0}{c_p}.
$$

For

$$
\xi(x,t)=a_2(t)\sin(k_nx),
\qquad
k_n=\frac{n\pi}{D},
$$

the analytical coefficients are

$$
M_{2,n}=\frac{AD}{2}\frac{\rho_s\rho_n}{\rho},
\qquad
K_{2,n}=M_{2,n}c_2^2k_n^2,
\qquad
\omega_{2,n}=c_2k_n.
$$

### 3.2 Source, loss, and detector requirements

For

$$
f_{2,r}=\frac{F_{2,0}}{R_{2,n}},
\qquad
\mathcal K_{T,r}
=
\frac12M_{2,n}\left(\frac{F_{2,0}}{R_{2,n}}\right)^2,
$$

the experiment requires:

1. electrical heater calibration;
2. heat/entropy-flux conversion and heater-to-mode overlap;
3. independent damping from ring-down or a separate small-signal linewidth run;
4. thermometer transfer function derived from the same entropy-balance eigenmode;
5. boundary leakage and modal-contamination accounting;
6. a declared ceiling below vortex, parametric, and nonlinear thresholds.

For amplitude ring-down $a_2\propto e^{-t/\tau_A}$,

$$
R_{2,n}=\frac{2M_{2,n}}{\tau_A}.
$$

A simultaneous fit of loss and amplitude to the target resonance peak is not an independent route.

### 3.3 Open-cavity correction case

Woillez, Valentin, and Roche model finite-plate second-sound resonators in which diffraction, misalignment, and throughflow affect the spectrum. Their reported $L=1\,\mathrm{mm}$, $D\approx1.435\,\mathrm{mm}$ example demonstrates resonance shifts and geometry-dependent loss. Their local peak representation contains fitted amplitude and loss parameters, so it is evidence for the missing boundary/loss operators but is not by itself an independent target-capacity certificate.

This makes the open cavity a strong prospective R4 case: derive the direction and scale of the correction from geometry before inspecting a held-out spectrum, then test frequency shift, gain reduction, or admission failure.

### 3.4 Negative control and rejection

The ordinary Fourier node

$$
C_{th}\dot T+\frac{T-T_\infty}{R_{th}}=P_s
$$

is the required negative control. It has one store and a real relaxation pole, so it is not admitted as a resonant-capacity mode.

Reject or version the positive certificate if first/second-sound mixing is appreciable, total mass current is nonzero at leading order, transducers alter the assumed boundary, ring-down is not single exponential, adjacent modes overlap, diffraction invalidates the closed-cavity model, or vortices and nonlinear processes appear.

## 4. Candidate held-out R4 tests

The most promising first test is the finite-open-cavity correction:

1. freeze the closed-cavity theorem record;
2. derive the additional diffraction/boundary operator from independently measured geometry;
3. preregister the predicted direction and tolerance for resonance shift or gain loss;
4. test against a held-out mode or device;
5. compare against the null model consisting of the standard child wave equation plus conventional diffraction theory.

Success beyond that null could support a broader law-level claim. Failure leaves the analytical representation theorem intact and localizes the missing operator or scope boundary.

## 5. Sources

- E. Woillez, J. Valentin, and P.-E. Roche, [Second sound resonators and tweezers as vorticity or velocity probes](https://arxiv.org/abs/2301.05519).
- H. Hu et al., [Second Sound with Ultracold Atoms: A Brief Review](https://doi.org/10.1007/s43673-022-00055-2).
- A. Rinberg and V. Steinberg, [Parametric generation of second sound in superfluid helium](https://doi.org/10.1103/PhysRevB.64.054506).
