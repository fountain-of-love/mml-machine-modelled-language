# Resonant Capacity R3 Certificates

## Purpose and status

This document freezes one analytical protocol and applies it without changing primitives to an electromagnetic reference resonator, a Helmholtz acoustic resonator, a lumped hydraulic resonator, and a second-sound mode. Its purpose is the representation theorem. Apparatus calibration and held-out empirical testing are preserved separately in [Resonant Capacity Empirical Validation Programme](../04-future-research/Resonant-Capacity-Empirical-Validation-Programme.md).

It distinguishes:

- **analytical certificate completion:** every binding, derivation, dimension, convention, derived quantity, and falsifier is specified, and the target response amplitude is not used as an input;
- **empirical certificate completion:** independently measured model inputs are inserted and the derived results pass stated tolerances against the subsequently measured response.

The electromagnetic, acoustic, hydraulic, and closed-cavity second-sound certificates are analytically complete for their declared ideal linear one-mode systems. The electromagnetic certificate includes a numerical benchmark. Laboratory replication is optional validation, not a precondition of the theorem.

## 1. Frozen certificate protocol R3-v1.0

### 1.1 Admitted parent model

Use a passive linear series one-port with accumulated-flow state $q$, flow $f=\dot q$, peak sinusoidal source effort $e_s(t)=e_0\cos\omega t$, inertance $\mathcal I>0$, compliance $\mathcal C>0$, and resistance $\mathcal R>0$:

$$
\mathcal I\dot f+\mathcal Rf+\frac q{\mathcal C}=e_s,
\qquad
\dot q=f.
$$

Its storage and dissipation functions are

$$
H(q,f)=\frac12\mathcal I f^2+\frac{q^2}{2\mathcal C},
\qquad
D=\mathcal Rf^2,
$$

and its exact instantaneous power balance is

$$
\dot H=e_sf-\mathcal Rf^2.
$$

The complex flow amplitude for a peak source amplitude $e_0$ is

$$
\hat f(\omega)
=
\frac{e_0}{\mathcal R+j\left(\omega\mathcal I-1/(\omega\mathcal C)\right)}.
$$

The declared resonance and quality factor are

$$
\omega_0=\frac1{\sqrt{\mathcal I\mathcal C}},
\qquad
Q=\frac{\omega_0\mathcal I}{\mathcal R}
=\frac1{\mathcal R}\sqrt{\frac{\mathcal I}{\mathcal C}}.
$$

### 1.2 Frozen Resonant Capacity binding

The certificate uses:

| RCL field | Frozen meaning |
| --- | --- |
| $\mathcal K_r$ | total cycle-mean energy stored in the admitted mode at $\omega_0$ |
| $\Sigma$ | flow-side inertance $\mathcal I$ |
| $\Psi$ | source-normalized baseline flow amplitude $f_0=e_0/(\omega_0\mathcal I)$ |
| $G_r$ | independently derived same-coordinate resonant gain $Q=\omega_0\mathcal I/\mathcal R$ |
| $\kappa$ | $1/2$, fixed by peak-amplitude and cycle-mean-total-energy conventions |

At resonance,

$$
f_r=\frac{e_0}{\mathcal R}=f_0Q,
\qquad
q_r=\frac{f_r}{\omega_0}.
$$

The cycle-mean inertive and compliant energies are equal:

$$
\langle H_{\mathcal I}\rangle
=\frac14\mathcal I f_r^2,
\qquad
\langle H_{\mathcal C}\rangle
=\frac1{4\mathcal C}\left(\frac{f_r}{\omega_0}\right)^2
=\frac14\mathcal I f_r^2.
$$

Therefore

$$
\boxed{
\mathcal K_r
=\langle H\rangle_{\omega_0}
=\frac12\mathcal I(f_0Q)^2
=\kappa\Sigma(\Psi G_r)^2.
}
$$

No coefficient has been fitted. The result follows from the independently specified storage functional, source convention, and transfer function.

### 1.3 Independent loss-route cross-check

With peak amplitudes,

$$
P_{\rm loss}=\frac12\mathcal Rf_r^2,
\qquad
Q=\omega_0\frac{\mathcal K_r}{P_{\rm loss}},
$$

so a second energy estimate is

$$
\boxed{
\mathcal K_r^{(P)}=\frac{Q}{\omega_0}P_{\rm in}
}
$$

at steady state, where $P_{\rm in}=P_{\rm loss}$. Empirical completion requires agreement between the amplitude/storage route and this power/loss route within a preregistered uncertainty budget.

### 1.4 Admission conditions

All must hold:

1. one mode dominates in the tested bandwidth;
2. $\mathcal I$, $\mathcal C$, and $\mathcal R$ are positive and approximately constant over that bandwidth and amplitude range;
3. source effort amplitude, source impedance, load, boundaries, and output coordinate are fixed;
4. response is steady-state sinusoidal and below nonlinear saturation;
5. peak rather than RMS amplitudes are used;
6. $\mathcal R$ includes every loss channel seen by the mode or those channels are modelled separately;
7. coefficients and normalization are obtained independently of the target resonant amplitude.

### 1.5 Mandatory rejection and failure tests

- A one-store RC or pure resistor is rejected as a resonant certificate.
- If the reactive cancellation does not occur at the predicted $\omega_0$, the certificate fails or requires an added state/operator.
- If measured $f_r$ disagrees with $e_0/\mathcal R$ beyond uncertainty, the loss/source model is incomplete.
- If amplitude- and power-route energies disagree, the storage normalization, loss partition, or one-mode assumption fails.
- Above nonlinear, multimode, hysteretic, turbulent, cavitating, breakdown, or parametric-instability onset, R3-v1.0 is out of scope.
- Away from resonance, total mean energy contains separate inertive and compliant terms; the one-term $\kappa=1/2$ certificate is not asserted.

### 1.6 Frozen C09 context-binding matrix

The twenty-row analogue inventory supplies the contextual questions. R3-v1.0 freezes the operational choices using rows 2–6, 9–10, 13, 16, 19, and 20: storage, drive, constitutive response, flow, interconnection, resonance, dissipation, boundary/load, regime, coupling, and stability. The remaining rows qualify the governing model but do not redefine gain.

Common convention for every row below:

- source: sinusoidal effort amplitude $e_0$ at the admitted one-port, held fixed while frequency is swept;
- source/load impedance: reduced into the declared total $\mathcal I$, $\mathcal C$, and $\mathcal R$, or retained as an explicitly measured external network before those totals are calculated;
- output: the common series flow $f$ at that one-port;
- observation: steady-state peak amplitude at $\omega_0$;
- baseline: $f_0=e_0/(\omega_0\mathcal I)$;
- gain: $G_r=f_r/f_0=Q=\omega_0\mathcal I/\mathcal R$;
- capacity: total cycle-mean energy of the single admitted mode;
- controlled quantity: source effort $e_0$, not response amplitude or input power.

| Domain realization | Fixed source effort $e_0$ | Output flow $f$ | Storage pair | Total loss/load binding | Boundary and coupling | Declared linear regime |
| --- | --- | --- | --- | --- | --- | --- |
| Mechanics reference | harmonic applied force $F_0$ | mass velocity $v$ | mass $m$ and compliance $1/k$ | viscous $b$ plus referred source/load damping | one translating mode between source and fixed/reference support | small displacement, linear spring/damper, single mode |
| Electromagnetics | port/source voltage $V_0$ | series current $I$ | inductance $L$ and capacitance $C$ | total series $R$, including source, ESR, wiring, and load | electrically small series loop; distributed/radiative effects excluded or referred | linear time-invariant lumped circuit below saturation/breakdown |
| Acoustics | blocked/port pressure $p_0$ | neck volume velocity $U$ | acoustic inertance $M_a$ and compliance $C_a$ | $R_a$ including thermoviscous, radiation, source, and load contributions | compact neck–cavity mode with declared radiation termination | $kL\ll1$, rigid walls, small signal, single mode |
| Hydraulics | port pressure difference $\Delta p_0$ | line volume flow $Q_h$ | line inertance $I_h$ and tangent compliance $C_h$ | tangent $R_h$ including valve, line, source/load, and leakage contributions | declared line–accumulator topology at fixed bias point | laminar/quasi-linear, no cavitation, single lumped mode |
| Thermodynamics | generalized second-sound modal effort $F_{2,0}$ derived from heater coupling | modal rate $\dot a_2$ | $M_2$ and $1/K_2$ | $R_2$ from attenuation, boundary leakage, and detector/source loading | selected second-sound cavity, eigenmode, thermal boundaries, and thermometer map | linear two-fluid mode below vortex/parametric/nonlinear thresholds |

This matrix freezes C09 for the declared R3-v1.0 representation class. A different topology or controlled variable—parallel resonator, flow source, fixed input power, transient ring-up, distributed field, or different output coordinate—is a new certificate version, not an unrecorded reinterpretation of $G_r$.

### 1.7 Frozen $\kappa$ governance and C03 certificate

R3-v1.0 does not permit a domain-specific fitted $\kappa$. It fixes

$$
\boxed{\kappa=\frac12}
$$

once, before any child binding, from two declared conventions:

1. $\Psi G_r=f_r$ is a **peak** flow amplitude;
2. $\mathcal K_r$ is **total cycle-mean modal energy at resonance**.

At resonance, equipartition of the admitted quadratic mode gives

$$
\left\langle H_{\mathcal I}\right\rangle
=\frac14\mathcal I f_r^2,
\qquad
\left\langle H_{\mathcal C}\right\rangle
=\frac14\mathcal I f_r^2,
$$

and hence $\langle H\rangle=\tfrac12\mathcal I f_r^2$. The factor is therefore derived from the energy and amplitude conventions rather than obtained from data.

#### Dependency allocation rule

| Physical dependence | Required location | Forbidden treatment |
| --- | --- | --- |
| mass, inductance, modal inertia, density, geometry-dependent storage integral | $\Sigma=\mathcal I$ | hidden in $\kappa$ |
| source coupling and sensor conversion | explicit input/observation operator | hidden in $\kappa$ |
| damping, radiation, leakage, source/load resistance | $\mathcal R$ and therefore $G_r$ | corrected by $\kappa$ |
| frequency and detuning | transfer function $G(\omega)$ | frequency-dependent $\kappa$ |
| boundary and topology | governing model and derived $\mathcal I,\mathcal C,\mathcal R$ | boundary-specific fit of $\kappa$ |
| peak/RMS or peak/mean convention | certificate version metadata | changed silently inside a domain |
| nonlinear saturation or regime transition | failure/lift model | residual multiplier in $\kappa$ |

For a distributed mode, geometry and eigenfunction normalization belong in the modal coefficient

$$
\Sigma=M_n=\int_\Omega \rho_{eff}(x)\,|\phi_n(x)|^2\,d\Omega
$$

or its domain-appropriate energy metric. If the instrument measures a local field rather than the normalized modal coordinate, the conversion is an explicit observation operator $y=C_y a_n$; it is not part of $\kappa$.

#### Per-binding demonstration

| Binding | Peak activation | Flow-side substrate | Derived capacity | $\kappa$ |
| --- | --- | --- | --- | --- |
| Mechanics | $v_r$ | $m$ | $\tfrac12mv_r^2$ at the kinetic maximum / total modal mean at resonance | $1/2$ |
| Electromagnetics | $I_r$ | $L$ | $\tfrac12LI_r^2$ total modal mean at resonance | $1/2$ |
| Acoustics | $U_r$ | $M_a$ | $\tfrac12M_aU_r^2$ total Helmholtz-mode mean at resonance | $1/2$ |
| Hydraulics | $Q_{h,r}$ | $I_h$ | $\tfrac12I_hQ_{h,r}^2$ total line–accumulator-mode mean at resonance | $1/2$ |
| Second sound | $f_{2,r}$ | $M_2$ | $\tfrac12M_2f_{2,r}^2$ total normalized-mode mean at resonance | $1/2$ |

The second-sound apparatus still requires $M_2$ and its observation map, but this uncertainty cannot change $\kappa$.

#### Audit and falsifier

Each certificate records the immutable tuple

```text
kappa = 1/2
amplitude = peak
capacity = total cycle-mean modal energy at resonance
coordinate = normalized series flow
```

The fit model contains no $\kappa$ parameter. Residual disagreement must be assigned to measurement uncertainty or to a named source, loss, boundary, multimode, nonlinear, or reduction term. If agreement can be obtained only by changing $\kappa$, the certificate fails. Alternative legitimate conventions receive a new protocol version—for example, RMS flow with total cycle-mean energy gives $\kappa=1$—and cannot be pooled with R3-v1.0 without explicit conversion.

C03 is therefore closed for R3-v1.0 at the analytical-governance level.

## 2. Electromagnetic gold-standard certificate: series RLC

### 2.1 Binding

| Parent field | Electrical binding | SI unit |
| --- | --- | --- |
| $e_s$ | source voltage $V_s$ | V |
| $f$ | current $I$ | A |
| $q$ | charge $q_e$ | C |
| $\mathcal I$ | inductance $L$ | H = V s A$^{-1}$ |
| $\mathcal C$ | capacitance $C$ | F = C V$^{-1}$ |
| $\mathcal R$ | total series resistance $R$ | $\Omega$ = V A$^{-1}$ |
| $H$ | $\tfrac12LI^2+q_e^2/(2C)$ | J |

The exact parent equation becomes

$$
L\dot I+RI+\frac{q_e}{C}=V_s,
\qquad \dot q_e=I.
$$

Thus

$$
\omega_0=\frac1{\sqrt{LC}},
\quad
Q=\frac{\omega_0L}{R},
\quad
I_0=\frac{V_0}{\omega_0L},
\quad
I_r=I_0Q=\frac{V_0}{R},
$$

and

$$
\boxed{
\mathcal K_{EM,r}=\frac12L(I_0Q)^2.
}
$$

Dimensional closure is exact: $[L I^2]=\mathrm{H\,A^2}=\mathrm J$.

### 2.2 Reproducible numerical benchmark

Freeze

$$
L=10.0\ \mathrm{mH},\quad
C=1.00\ \mathrm{\mu F},\quad
R=10.0\ \Omega,\quad
V_0=1.00\ \mathrm V\ \text{peak}.
$$

Predictions before measuring the resonant response are

$$
\omega_0=10{,}000\ \mathrm{rad\,s^{-1}},
\qquad
\nu_0=1591.55\ \mathrm{Hz},
$$

$$
Q=10.0,
\qquad
I_0=10.0\ \mathrm{mA},
\qquad
I_r=100\ \mathrm{mA}\ \text{peak},
$$

$$
\boxed{\mathcal K_{EM,r}=50.0\ \mathrm{\mu J}.}
$$

The independent loss route predicts

$$
P_{\rm in}=\frac12RI_r^2=50.0\ \mathrm{mW},
\qquad
\frac Q{\omega_0}P_{\rm in}=50.0\ \mathrm{\mu J}.
$$

This numerical equality is a benchmark calculation, not experimental confirmation. A laboratory certificate must measure actual total series resistance—including source, inductor ESR, wiring, and load—plus frequency response, phase, current, and input power with an uncertainty budget.

### 2.3 Reference verdict

`R3-ANALYTICAL-COMPLETE`; `R3-EMPIRICAL-PENDING`. This is the frozen reference certificate for the following transpositions. Standard RLC resonance and stored-energy/Q relations are documented in MIT's RLC resonator materials.

## 3. Acoustic certificate: pressure-driven Helmholtz mode

### 3.1 Binding

For a compact rigid-walled neck–cavity resonator with neck dimensions small relative to wavelength:

| Parent field | Acoustic binding | SI unit |
| --- | --- | --- |
| $e_s$ | blocked/source acoustic pressure $p_s$ | Pa |
| $f$ | neck volume velocity $U$ | m$^3$ s$^{-1}$ |
| $q$ | volume displacement $q_a$ | m$^3$ |
| $\mathcal I$ | acoustic inertance $M_a=\rho\ell_{eff}/A$ | Pa s$^2$ m$^{-3}$ |
| $\mathcal C$ | cavity compliance $C_a=V/(\rho c^2)$ | m$^3$ Pa$^{-1}$ |
| $\mathcal R$ | total acoustic resistance $R_a$ | Pa s m$^{-3}$ |

The equation and predictions are

$$
M_a\dot U+R_aU+\frac{q_a}{C_a}=p_s,
\qquad \dot q_a=U,
$$

$$
\omega_a=\frac1{\sqrt{M_aC_a}},
\quad
Q_a=\frac{\omega_aM_a}{R_a},
\quad
U_0=\frac{p_0}{\omega_aM_a},
\quad
U_r=U_0Q_a=\frac{p_0}{R_a},
$$

$$
\boxed{
\mathcal K_{A,r}=\frac12M_a(U_0Q_a)^2.
}
$$

Dimensional closure is exact: $[M_aU^2]=\mathrm{Pa\,m^3}=\mathrm J$. The acoustic inertance/compliance reduction and Helmholtz resonance follow from linearized Euler and continuity equations; thermoviscous and radiation losses are required for $R_a$ and $Q_a$.

### 3.2 Required independent measurements

Measure geometry, $\rho$, $c$, end correction, wall rigidity, source pressure at the port, and the separate radiation and thermoviscous loss contributions. Predict $\omega_a$, linewidth, $U_r$, and $\mathcal K_{A,r}$ before measuring the target response. Cross-check energy using calibrated volume velocity and using input acoustic power plus linewidth.

### 3.3 Acoustic verdict

`R3-ANALYTICAL-COMPLETE` for the compact linear one-mode model; `R3-EMPIRICAL-PENDING`. Failure is expected when higher duct/cavity modes, compliant walls, nonlinear jetting, amplitude-dependent loss, or inaccurate end correction are material.

## 4. Hydraulic certificate: pressure-driven line–accumulator mode

### 4.1 Binding

Use a liquid-filled line supplying a compliant accumulator or elastic chamber, linearized about a fixed pressure and flow operating point:

| Parent field | Hydraulic binding | SI unit |
| --- | --- | --- |
| $e_s$ | source pressure difference $\Delta p_s$ | Pa |
| $f$ | volumetric flow $Q_h$ | m$^3$ s$^{-1}$ |
| $q$ | displaced/stored volume $q_h$ | m$^3$ |
| $\mathcal I$ | hydraulic inertance $I_h=\rho\ell/A$ for the ideal line | Pa s$^2$ m$^{-3}$ |
| $\mathcal C$ | differential compliance $C_h=(dV/dp)_0$ | m$^3$ Pa$^{-1}$ |
| $\mathcal R$ | linearized total hydraulic resistance $R_h=(d\Delta p/dQ)_0$ | Pa s m$^{-3}$ |

Then

$$
I_h\dot Q_h+R_hQ_h+\frac{q_h}{C_h}=\Delta p_s,
\qquad \dot q_h=Q_h,
$$

$$
\omega_h=\frac1{\sqrt{I_hC_h}},
\quad
Q_{qual,h}=\frac{\omega_hI_h}{R_h},
\quad
Q_{h,0}=\frac{\Delta p_0}{\omega_hI_h},
\quad
Q_{h,r}=Q_{h,0}Q_{qual,h}=\frac{\Delta p_0}{R_h},
$$

$$
\boxed{
\mathcal K_{H,r}=\frac12I_h(Q_{h,0}Q_{qual,h})^2.
}
$$

The notation $Q_{qual,h}$ avoids confusing quality factor with volumetric flow. Dimensional closure again gives $[I_hQ_h^2]=\mathrm J$.

### 4.2 Required independent measurements

Infer inertance from density and effective line geometry or an independently validated impedance measurement; infer tangent compliance and resistance at the frozen bias point; include fluid compressibility, wall compliance, accumulator gas law, valve/source impedance, and leakage as applicable. Predict the resonance and response before measuring target flow. Cross-check stored energy against mean hydraulic input power and linewidth.

### 4.3 Hydraulic verdict

`R3-ANALYTICAL-COMPLETE` for the declared linear one-mode line–accumulator model; `R3-EMPIRICAL-PENDING`. Cavitation, turbulent or amplitude-dependent resistance, valve nonlinearities, distributed water-hammer modes, and state-dependent accumulator compliance are preregistered failure boundaries.

Hydraulic and acoustic certificates are closely related continuum-fluid realizations. They support representation closure but are not counted as fully independent microscopic confirmations.

## 5. Thermodynamic certificate candidate: second-sound mode

### 5.1 Binding without primitive redefinition

Project the established linear two-fluid quadratic functional onto one normalized second-sound eigenmode $a_2(t)$. Let $F_2$ be the generalized source effort conjugate to $f_2=\dot a_2$, so $F_2f_2$ is physical input power into that mode:

$$
M_2\dot f_2+R_2f_2+K_2a_2=F_2(t),
\qquad f_2=\dot a_2,
$$

$$
H_2=\frac12M_2f_2^2+\frac12K_2a_2^2,
\qquad
C_2=K_2^{-1}.
$$

The identical protocol gives

$$
\omega_2=\sqrt{\frac{K_2}{M_2}},
\quad
Q_2=\frac{\omega_2M_2}{R_2},
\quad
f_{2,0}=\frac{F_{2,0}}{\omega_2M_2},
\quad
f_{2,r}=f_{2,0}Q_2=\frac{F_{2,0}}{R_2},
$$

$$
\boxed{
\mathcal K_{T,r}=\frac12M_2(f_{2,0}Q_2)^2.
}
$$

The physical temperature or entropy-wave observable must be connected to $a_2$ by the same frozen eigenfunction normalization. Temperature amplitude cannot replace $f_2$ after the fact.

### 5.2 Selected apparatus and explicit mode projection

The frozen reference realization is a straight, closed, constant-area He-II cavity of length $D$ and area $A$, held at equilibrium temperature $T_0$, with a uniform planar heater at $x=0$ and a calibrated thermometer at $x=D$. The first longitudinal second-sound mode is used. The reference is the one-dimensional closed-cavity limit; an open finite-plate “tweezer” is a later correction case because diffraction then becomes a frequency-dependent loss and frequency-shift operator.

Let $\rho_s$ and $\rho_n$ be equilibrium superfluid and normal densities, $\rho=\rho_s+\rho_n$, $s$ the entropy per unit mass, and $c_p$ the specific heat per unit mass at constant pressure. In the ideal second-sound limit the total mass current vanishes,

$$
\rho_sv_s+\rho_nv_n=0,
$$

while the relative velocity $w=v_n-v_s$ carries the counterflow. Consequently,

$$
\frac12\rho_sv_s^2+\frac12\rho_nv_n^2
=
\frac12\frac{\rho_s\rho_n}{\rho}w^2.
$$

Define $\mu_2:=\rho_s\rho_n/\rho$ and $\chi_T:=\rho c_p/T_0$. Under the standard decoupling approximation that pressure and total-density fluctuations are negligible to first order, the small-amplitude energy density is

$$
h_2=\frac12\mu_2w^2+\frac12\chi_T(\delta T)^2,
$$

and the established second-sound speed is

$$
c_2^2=\frac{\rho_s}{\rho_n}\frac{s^2T_0}{c_p}.
$$

Choose the relative-displacement mode

$$
\xi(x,t)=a_2(t)\sin(k_nx),
\qquad
k_n=\frac{n\pi}{D},
\qquad
w=\dot\xi.
$$

The closed-end velocity condition is built into this mode. Projection gives

$$
M_{2,n}
=\mu_2A\int_0^D\sin^2(k_nx)\,dx
=\boxed{\frac{AD}{2}\frac{\rho_s\rho_n}{\rho}},
$$

$$
K_{2,n}=M_{2,n}c_2^2k_n^2,
\qquad
\boxed{\omega_{2,n}=c_2k_n=\frac{n\pi c_2}{D}},
\qquad
C_{2,n}=K_{2,n}^{-1}.
$$

This supplies the apparatus-specific $M_2$, $K_2$, normalization, boundary condition, and eigenfrequency from equilibrium material functions and geometry. No target temperature amplitude, modal rate, or fitted $\kappa$ enters the derivation.

Linear entropy balance must connect the temperature eigenfunction to this same counterflow coordinate; $\delta T$ cannot be substituted afterward as a new activation coordinate. At the driven boundary, input power is temperature effort multiplied by entropy-flow rate. Heater calibration must therefore be converted to $F_{2,0}$ through the boundary overlap of the heater entropy flux with the normalized mode.

### 5.3 Analytical source and loss roles

For the R3 amplitude result,

$$
f_{2,r}=\frac{F_{2,0}}{R_{2,n}},
\qquad
\mathcal K_{T,r}=\frac12M_{2,n}\left(\frac{F_{2,0}}{R_{2,n}}\right)^2,
$$

$F_{2,0}$ is the generalized effort obtained by projecting the boundary entropy-flux source onto the same normalized mode. $R_{2,n}>0$ is the modal dissipation coefficient in that projection. Their numerical apparatus extraction is not needed for the conditional theorem: once supplied by an admitted child model, the system derives $Q_2$, $f_{2,r}$, and $\mathcal K_{T,r}$. They may not be inferred from the target amplitude in a future empirical certificate.

### 5.4 Negative control and rejection tests

The paired Fourier node,

$$
C_{th}\dot T+\frac{T-T_\infty}{R_{th}}=P_s,
$$

has one store and a real relaxation pole. It is rejected as an R3 resonator because no independently derived complementary inertial store or nonzero natural frequency exists.

The positive second-sound record is rejected or versioned if first/second-sound mixing is appreciable, total mass current is nonzero at leading order, transducers alter the assumed boundary, ring-down is not single-exponential, adjacent modes overlap, diffraction dominates the closed-cavity loss model, or the response crosses vortex, parametric, or other nonlinear thresholds.

### 5.5 Second-sound verdict

`R3-ANALYTICAL-COMPLETE-FOR-DECLARED-CLOSED-CAVITY-MODE`; `R3-EMPIRICAL-OPTIONAL`. Ordinary Fourier RC remains the paired negative control. Second sound is thermo-fluid coupled evidence rather than a wholly independent microscopic ontology.

## 6. Cross-certificate comparison

| Certificate | $e$ | $f$ | $\mathcal I$ | $\mathcal C$ | $\mathcal R$ | Analytical status | Empirical status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Electromagnetic RLC | $V$ | $I$ | $L$ | $C$ | $R$ | Complete | Pending |
| Acoustic Helmholtz | $p$ | $U$ | $M_a$ | $C_a$ | $R_a$ | Complete in compact linear model | Pending |
| Hydraulic line–accumulator | $\Delta p$ | $Q_h$ | $I_h$ | $C_h$ | $R_h$ | Complete in linear one-mode model | Pending |
| Second sound | $F_2$ | $\dot a_2$ | $M_{2,n}=AD\rho_s\rho_n/(2\rho)$ | $1/(M_{2,n}c_2^2k_n^2)$ | $R_{2,n}>0$ from admitted modal projection | Complete for declared closed-cavity model | Optional |

All four use the same parent equation, same source-effort convention, same flow-side activation, same $G_r=Q$, same $\kappa=1/2$, same capacity convention, and same loss-route cross-check. No child redefines a primitive.

## 7. Representation-theorem result

The closed systems of equations establish a role-preserving representation theorem for the declared linear, one-mode, effort-driven, series-resonator class across the listed realizations. The Resonant Capacity expression is not rescued by arbitrary functions or fitted coefficients: it follows from the quadratic storage functional and the derived same-coordinate response.

This theorem is the analytical achievement sought by Paper 0. A new empirical invariant beyond the admitted model class is a distinct optional R4 programme, described in [Resonant Capacity Empirical Validation Programme](../04-future-research/Resonant-Capacity-Empirical-Validation-Programme.md).

## 8. Sources anchoring the constructions

- MIT OpenCourseWare, [RLC Resonators](https://www.ocw.mit.edu/courses/6-013-electromagnetics-and-applications-spring-2009/5c3f73b9b5b834d7b8c6e6082b0e9346_MIT6_013S09_lec14.pdf).
- Steven L. Garrett, [Nondissipative Lumped Elements](https://doi.org/10.1007/978-3-030-44787-8_8), deriving acoustic inertance and compliance from the compact-element approximation and showing their Helmholtz combination.
- C. Higo et al., hydraulic reduced resistance/inertia derivation and validation, [DOI 10.5739/jfps.52.16](https://doi.org/10.5739/jfps.52.16).
- M. Galal Rabie, [On the Application of Oleo-Pneumatic Accumulators for the Protection of Hydraulic Transmission Lines Against Water Hammer](https://journals.riverpublishers.com/index.php/IJFP/article/view/546), developing and comparing lumped resistance–inertia–capacitance line models with published experiments.
- H. Hu et al., [Second Sound with Ultracold Atoms: A Brief Review](https://doi.org/10.1007/s43673-022-00055-2), including the two-fluid variational formulation.
- A. Rinberg and V. Steinberg, [Parametric generation of second sound in superfluid helium](https://doi.org/10.1103/PhysRevB.64.054506).
- A. Rusaouen et al., [Second sound resonators and tweezers as vorticity or velocity probes](https://arxiv.org/abs/2301.05519), presenting and experimentally validating an open-cavity resonator model.
