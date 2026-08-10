# A Five-Domain Energy Grammar

## The Provisional Resonant Capacity Law Across Five Physical Domains

### Paper 0 — Research Proposal

Repository context: this paper is part of the [Semantic Seed Vault](../../README.md), a knowledge-base pilot for the broader [Semantic Operating System architecture](../../../../sos/Architecture.md). It can be read independently as a scientific proposal; the Common Language Model and MML references are optional architectural extensions, not prerequisites for the paper's core claim.

## Abstract

Mechanics, thermodynamics, acoustics, electromagnetics, and fluid mechanics are commonly taught and modelled through distinct vocabularies, even though energy-based modelling traditions have long demonstrated structural correspondences among physical domains. Bond graphs express cross-domain power exchange through conjugate effort and flow variables; port-Hamiltonian systems provide a domain-neutral account of storage, interconnection, ports, and dissipation; nonequilibrium thermodynamics contributes force–flow relations and entropy production; and exergetic extensions connect useful work capacity to the first and second laws. These foundations are substantial but distributed across separate literatures and often applied at incompatible abstraction levels.

This paper proposes a five-domain energy grammar across mechanics, thermodynamics, acoustics, electromagnetics, and fluid mechanics at deliberately matched levels of abstraction. Its provisional synthesis is the Resonant Capacity Law,

$$
\boxed{
\text{Capacity}
=
\text{Substrate}
\times
(\text{Activation}\times\text{Resonant gain})^2
}
$$

which proposes that accessible capacity grows quadratically with coherent activation of a receiving substrate, subject to domain-specific conversion, boundary conditions, dissipation, saturation, and regime limits. The proposal is motivated by recurring substrate-times-squared-activation capacity forms across the five domains; it does not treat formal similarity as proof of a universal physical law.

The Resonant Capacity Law is explicitly classified as imputed and falsifiable. Qualified relations, formula-maturity labels, abstraction and regime metadata, drift detection, constrained imputation, and Energy–Entropy–Exergy checks form its scientific control layer. They distinguish established domain formulas from the proposed synthesis and test whether the grammar improves explanatory compression, cross-domain transposition, gap detection, and disciplined hypothesis generation. A broader unified research programme may emerge from this work, but it is a downstream consequence rather than the paper's primary contribution.

**Keywords:** Resonant Capacity Law; energy grammar; coherent activation; multiphysics modelling; bond graphs; port-Hamiltonian systems; nonequilibrium thermodynamics; exergy; cross-domain transposition

## 1. Research Position

The existence of shared mathematical structures across physical systems is well established. The proposed contribution lies in how those structures are expressed, qualified, compared, and used:

> **Effort–flow relations, domain-neutral energy structures, and the individual capacity formulas are established prior art. The candidate new synthesis is the Resonant Capacity Law as a five-domain grammar, together with the controls required to bind, compare, test, and potentially reject it across domains.**

The reviewer-facing boundary is therefore explicit:

> **This work does not propose an alternative to bond graphs or port-Hamiltonian systems. It uses them as physical foundations and adds an epistemically explicit layer for disciplined comparison across domains.**

The grammar asks:

> Does $\mathcal K_r=\kappa\Sigma(\Psi G_r)^2$ express a meaningful substrate–activation–resonance structure across five foundational physical domains, and can the grammar show precisely where that structure holds, changes form, or fails?

The current analytical answer is affirmative over a declared class: stable linear one-mode systems with complementary positive quadratic storage, a role-preserving reduction to the frozen parent dynamics, and a same-coordinate gain derived under an explicit source and boundary protocol. Within that scope, Resonant Capacity is claimed as a **universal representation law**, not merely a visual analogy. The stronger statement that it is a new empirical invariant outside the represented class remains optional future work, while the exact novelty of the five-domain formulation remains subject to the systematic review obligation C10.

The physical interpretation is nested. Complementary modal stores operate within an inner system, while activation and gain arise through an energetic relation with a relevant outer system across a declared boundary. Both belong to the energy ledger:

$$
H_{\mathrm{extended}}
=
H_{\mathrm{inner}}
+H_{\mathrm{coupling}}
+H_{\mathrm{outer}}.
$$

This partition must avoid double counting. The two modal stores are not automatically identical to “inner” and “outer”; rather, they form the receiving mode inside the larger system–environment relation developed in Paper 2.1.

The five selected domains are:

1. mechanics;
2. thermodynamics;
3. acoustics;
4. electromagnetics;
5. fluid mechanics.

The comparison deliberately begins at a matched elementary or lumped level. Distributed fields, nonlinearities, memory, turbulence, and far-from-equilibrium behavior are reintroduced only after the common elementary structure is made explicit.

Mechanics is not assumed to be uniquely simple. It is a familiar reference dialect because mass–spring–damper models are widely taught. Thermal RC networks, lumped acoustic elements, RLC circuits, and hydraulic inertance–compliance–resistance models provide corresponding low-dimensional descriptions. The comparison must nevertheless distinguish a shared role vocabulary from one particular series topology and preserve the thermodynamic distinction between engineering heat-rate analogies and true temperature–entropy-flow power bonds.

The paper's claim can be falsified without accepting any wider programme: if the Resonant Capacity Law lacks coherent domain bindings, fails dimensional or regime tests, or provides no explanatory or predictive advantage over simpler analogy tables, the grammar has not demonstrated its central added value.

## 2. Scientific Foundations

This chapter establishes the scientific basis from which the five-domain grammar is constructed. Its purpose is neither to provide an exhaustive history of energy-based modelling nor to present eight independent theories as competing explanations. Each subsection supplies a specific part of the grammar and constrains what the proposal may legitimately claim as new.

The chapter follows a deliberate progression. It begins with historical cross-domain analogy, then introduces the power-conjugate language and its mathematical system formulation. It next examines acoustics as a mature example of domain transposition, adds thermodynamic treatment of irreversible processes and open systems, incorporates exergy as the measure of useful work relative to an environment, and finally restores the distributed-field complexity suppressed by the initial lumped comparison.

| Foundation | Function within the grammar |
| --- | --- |
| Historical physical-system analogies | Establish prior art for comparing domains and define the novelty boundary |
| Bond graphs | Supply power-conjugate effort–flow variables and cross-domain element roles |
| Port-Hamiltonian systems | Formalize storage, interconnection, ports, and dissipation |
| Electro-mechano-acoustic modelling | Demonstrate mature transposition and the need for physical role correspondence |
| Onsager relations | Introduce irreversible force–flow coupling, entropy production, and near-equilibrium limits |
| GENERIC and open-system thermodynamics | Separate reversible and irreversible evolution and make boundaries explicit |
| Exergetic port-Hamiltonian systems | Connect energy, entropy, useful work, and environmental reference states |
| Distributed port-Hamiltonian systems | Extend the grammar from lumped elements to fields and boundary flows |

Together, these foundations provide three things: an established common language of energy exchange, constraints that prevent superficial analogy, and a path from elementary comparison back to physically complete models. Chapter 3 then identifies what remains uncombined in the literature, and Chapter 4 defines the proposed grammar built from this foundation.

### 2.1 Historical Physical-System Analogies

Schönfeld’s 1954 study, *Analogy of Hydraulic, Mechanical, Acoustic and Electric Systems*, is the closest historical predecessor identified in the present literature review. It treats hydraulics as distinct from mechanics and interprets acoustics through mixed mechanical–hydraulic structure while comparing resistance, inertance, and storage across domains.[^schonfeld]

That work establishes a strong boundary for novelty. The present grammar extends the comparison by introducing thermodynamics as an equal fifth domain and by adding maturity labels, abstraction-drift checks, gap-oriented analysis, and the Energy–Entropy–Exergy triad.

**Contribution to the grammar.** Historical analogy supplies the comparative precedent and the initial cross-domain element vocabulary. It also imposes a novelty constraint: the grammar may claim a new organization and qualification of correspondences, but not the discovery of the correspondences themselves.

### 2.2 Bond Graphs and Power-Conjugate Variables

Bond-graph theory provides the nearest established grammar. Its literature explicitly treats electrical, mechanical, hydraulic, acoustic, thermodynamic, and other systems through domain-neutral power bonds and ideal storage, dissipation, source, transduction, and junction roles.[^broenink] Different physical domains exchange power through conjugate effort and flow variables:

$$
\boxed{P = e f}
$$

Representative domain bindings include:

$$
P_{\mathrm{mechanical}} = Fv
$$

For a reversible thermal port, temperature and entropy-transfer rate form the corresponding conjugate pair:

$$
P_{\mathrm{thermal,rev}}
=
T\dot S_{\mathrm{e}}
=
\dot Q_{\mathrm{rev}}
$$

where $\dot S_{\mathrm{e}}$ denotes entropy exchanged through the system boundary, not entropy produced internally. For an irreversible process, the entropy balance must additionally retain $\dot S_{\mathrm{gen}}\geq0$; consequently, $\dot Q=T\dot S$ is not admitted as an unconditional thermodynamic identity.

$$
P_{\mathrm{acoustic}} = pU
$$

$$
P_{\mathrm{electrical}} = VI
$$

$$
P_{\mathrm{hydraulic}} = \Delta p\,Q
$$

Maschke and van der Schaft formalized port-controlled Hamiltonian systems from generalized bond-graph network representations. Their formulation connects network topology, stored energy, environmental ports, and conjugate variables across physical domains.[^maschke]

Accordingly, this paper does **not** claim to discover effort multiplied by flow as a common physical language. It uses the established tradition as the foundation for a controlled five-domain comparison.

**Contribution to the grammar.** Bond graphs supply its minimal common syntax: effort, flow, power, storage, resistance, source, and interconnection roles. The grammar retains $P=ef$ as a central invariant while requiring every domain-specific binding to carry its units, sign convention, boundary, and validity regime.

### 2.3 Port-Hamiltonian Systems

Port-Hamiltonian theory supplies a rigorous mathematical backbone for multiphysics systems. In a representative finite-dimensional form:

$$
\dot{x}
=
\left[J(x)-R(x)\right]\nabla H(x)
+
G(x)u
$$

$$
y = G(x)^{\mathsf{T}}\nabla H(x)
$$

where $H$ is a storage function, $J=-J^{\mathsf{T}}$ represents power-conserving interconnection, $R=R^{\mathsf{T}}\succeq0$ represents dissipation, and $(u,y)$ form a port pair. The framework makes energy storage, interconnection, input–output exchange, and dissipation explicit without tying them to one physical domain.[^overview]

This structure anchors three of the proposed grammar’s central roles:

- **storage**, represented by $H$;
- **circulation or interconnection**, represented by $J$;
- **dissipation**, represented by $R$.

**Contribution to the grammar.** Port-Hamiltonian systems turn the role vocabulary into a system-level structural model. They provide the distinction among stored energy, power-conserving interconnection, dissipative behavior, and environmental ports that the grammar uses to classify relations and test whether a proposed mapping preserves system function rather than equation shape alone.

### 2.4 Electro-Mechano-Acoustic Modelling

Acoustics already has a mature cross-domain modelling tradition. Busch-Vishniac and Paynter applied lumped bond-graph methods to sound and vibration systems.[^sound] Bertuccio later examined the physical origin of electro-mechano-acoustic analogy, reinforcing a methodological requirement crucial to this programme: equation-shape similarity is insufficient unless mapped variables play corresponding physical roles.[^bertuccio]

The criterion for a valid transposition is therefore:

$$
\boxed{
\text{formal similarity}
+
\text{role correspondence}
+
\text{dimensional validity}
+
\text{regime compatibility}
}
$$

**Contribution to the grammar.** Electro-mechano-acoustic modelling supplies a worked precedent for transposition and motivates the grammar's admissibility rule. A candidate mapping must preserve physical role, dimensions, and regime—not merely reproduce a familiar algebraic form.

### 2.5 Onsager Force–Flow Relations

Near equilibrium, irreversible thermodynamics represents generalized flows $J_i$ as linear responses to thermodynamic forces $X_j$:

$$
J_i = \sum_j L_{ij}X_j
$$

or in matrix form:

$$
\mathbf{J}=\mathbf{L}\mathbf{X}
$$

with entropy production:

$$
\sigma = \sum_i J_iX_i = \mathbf{J}^{\mathsf{T}}\mathbf{X} \geq 0
$$

Onsager’s reciprocal relations provide the classical basis for this near-equilibrium structure under their stated microscopic conditions.[^onsager1][^onsager2] They support both cross-domain force–flow comparison and an important boundary: elegant linear transposition is most defensible near equilibrium, while coefficients may become nonlinear, state-dependent, or nonlocal farther from equilibrium.

**Contribution to the grammar.** Onsager theory adds irreversible force–flow relations, coupled transport, and non-negative entropy production. It requires validity regime to be part of every qualified relation and prevents a near-equilibrium linear correspondence from being silently generalized to nonlinear or far-from-equilibrium behavior.

### 2.6 GENERIC and Open-System Thermodynamics

The GENERIC framework separates reversible and irreversible time evolution through energy and entropy structures. A schematic form is:

$$
\dot{x}
=
L(x)\nabla E(x)
+
M(x)\nabla S(x)
$$

where the antisymmetric operator $L$ generates reversible dynamics and the symmetric positive-semidefinite operator $M$ generates irreversible dynamics. Öttinger’s open-system extension distinguishes bulk, boundary, and environmental exchange contributions.[^ottinger]

This is directly relevant to the grammar’s treatment of:

- reversible storage and circulation;
- irreversible entropy generation;
- system boundaries;
- environmental exchange;
- transitions from closed to open descriptions.

**Contribution to the grammar.** GENERIC supplies an explicit separation between reversible and irreversible operators, while its open-system extension makes the system boundary a first-class grammatical qualifier. This supports the grammar's boundary and operator-drift checks and prevents bulk dynamics, boundary transfer, and environmental exchange from being conflated.

### 2.7 Exergetic Port-Hamiltonian Systems

Exergetic port-Hamiltonian research argues that, in thermodynamically extended formulations, the Hamiltonian is appropriately interpreted as exergy: useful work capacity relative to an environment. It connects port-Hamiltonian modelling to GENERIC while encoding the first and second laws structurally.[^ephs]

Later work develops a compositional modelling language in which systems exchange exergy and thermodynamic consistency follows from the structure of primitive subsystems and their composition.[^ephs-language]

This provides direct prior art for using Energy, Entropy, and Exergy together. The triad’s quantities are not proposed as discoveries. The proposed contribution is their systematic use as semantic and thermodynamic checks inside the five-domain grammar.

**Contribution to the grammar.** Exergetic port-Hamiltonian systems ground the Energy–Entropy–Exergy triad and its dependence on an environmental reference state. They give the grammar a way to distinguish conserved energy from irreversible degradation and useful work capacity, so an energetically closed mapping is not automatically treated as thermodynamically complete.

### 2.8 Distributed Port-Hamiltonian Systems

Low-dimensional models risk obscuring the field nature of acoustics, electromagnetics, and fluid mechanics. Distributed port-Hamiltonian theory answers this concern by extending energy-based modelling to continua and partial differential equations while retaining boundary power flows and physical structure.[^distributed]

The intended progression is therefore:

$$
\boxed{
\text{element}
\rightarrow
\text{lumped network}
\rightarrow
\text{distributed field}
\rightarrow
\text{nonlinear regime}
}
$$

Simplification is a controlled starting point, not a denial of complexity.

**Contribution to the grammar.** Distributed port-Hamiltonian theory supplies the lifting path from elementary and lumped relations to fields, spatial operators, and boundary power flows. It grounds the abstraction ladder and operator-drift check: a lumped correspondence may be retained as a reduction, but it cannot stand in for its distributed counterpart without an explicit reduction or lifting relation.

## 3. Gap in the Literature

This chapter identifies the precise opening left by the scientific foundations reviewed in Chapter 2. Its intention is not to manufacture novelty by treating established ideas as absent. It separates three questions: what prior work already establishes, what remains fragmented or implicit, and what synthesis this paper therefore has grounds to propose.

The chapter is the argumentative hinge of the paper. Chapter 2 establishes that the physical and mathematical ingredients are credible prior art; Chapter 3 shows that they have not yet been assembled into the qualified comparative instrument defined in Chapter 4.

### 3.1 What the Existing Foundations Already Cover

The reviewed traditions already provide cross-domain analogies, effort–flow variables, energy-based system structures, irreversible force–flow relations, entropy production, exergy, open-system formulations, and distributed-field extensions. These are not gaps, and the paper does not claim them as discoveries.

Their coverage is nevertheless distributed across different literatures, terminologies, abstraction levels, and modelling purposes. A relation that is foundational in one tradition may appear as a constitutive assumption, reduced model, or implicit analogy in another. Existing frameworks also differ in how explicitly they record validity regimes, environmental boundaries, negative mappings, and provenance.

**Contribution to Chapter 3's intention.** This subsection fixes the baseline against which novelty must be judged. It prevents the proposed grammar from gaining apparent originality by renaming established physical structures and confines the gap analysis to missing integration, qualification, and comparative method.

### 3.2 The Unresolved Comparative Gap

This preliminary, non-exhaustive literature review did not identify one publication combining all of the following:

1. mechanics, thermodynamics, acoustics, electromagnetics, and fluid mechanics as five equal comparative columns;
2. a deliberately matched low-dimensional abstraction level;
3. a shared formula-maturity matrix;
4. explicit separation of foundational, constitutive, reduced, extended, and imputable relations;
5. drift detection through missing operators or mismatched abstraction levels;
6. Energy–Entropy–Exergy as the active mediating triad;
7. a provisional substrate–activation–coherence synthesis expressed as the Resonant Capacity Law;
8. a single inspectable record format that carries relation, meaning, evidence, limits, and status together.

The gap is therefore not the absence of cross-domain energy formalisms. It is the absence of a controlled five-domain synthesis of substrate, activation, resonance or coherence gain, and accessible capacity, together with a comparative method that makes semantic role, epistemic maturity, abstraction, regime, boundary, admissibility, and provenance simultaneously inspectable.

**Contribution to Chapter 3's intention.** This subsection defines the missing capability the paper addresses. Each listed feature becomes a requirement for the grammar in Chapter 4 and, later, an object of evaluation rather than an unsupported novelty assertion.

### 3.3 Scope of the Proposed Synthesis

The novelty claim is a **provisional cross-domain capacity law supported by a comparative and epistemic grammar**, subject to a systematic review before publication. It is not a claim that the constituent physical structures or square-law formulas are unknown. The synthesis proposes a shared resonant-capacity form, organizes established relations around it, and preserves failed mappings and structural absences as evidence.

This scope also identifies what is not required for the paper's central claim. CML encoding and the wider unified research programme are downstream possibilities. Resonant Capacity is not in that list: it is the central hypothesis the grammar exists to express and test.

**Contribution to Chapter 3's intention.** This subsection converts the observed gap into a bounded novelty claim. It protects the proposal from both overclaiming and dilution by separating the grammar itself from consequences and optional extensions.

### 3.4 Bounded and Testable Grammar Requirements

Chapter 3 transforms the foundations review into a design obligation. Because prior work already supplies the physics, the proposed contribution must be demonstrated in the grammar's organization, qualifications, operations, and comparative performance. The chapter therefore establishes the following dependency:

$$
\boxed{
\text{established foundations}
\rightarrow
\text{unresolved comparative gap}
\rightarrow
\text{bounded grammar requirements}
\rightarrow
\text{testable added value}
}
$$

Chapter 4 answers this obligation by stating the provisional Resonant Capacity Law, binding it to the five domains, and defining the qualification, maturity, and thermodynamic controls required to test it responsibly.

## 4. Proposed Five-Domain Grammar

This chapter states the paper's central proposal. The grammar aligns mechanics, thermodynamics, acoustics, electromagnetics, and fluid mechanics at a common abstraction level and seeks the energetic structure recurring across them. Its essence is the provisional **Resonant Capacity Law**. The qualified-relation schema, maturity labels, thermodynamic checks, drift detection, and imputation rules do not constitute the essence of the grammar; they determine how its central law may be interpreted, tested, bounded, and revised without being mistaken for established physics.

### 4.1 Common Energetic Pattern

Across the five domains, energy is:

1. stored in a substrate or compliant/inertial structure;
2. activated through an effort, flow, or displacement from equilibrium;
3. amplified in accessible effect through a defined resonant response or another separately qualified coherence or coupling mechanism;
4. degraded through resistance, attenuation, loss of phase coherence, or entropy generation, without assuming these are physically identical;
5. limited by boundary conditions and the regime in which the model applies.

The familiar power relation $P=ef$ describes the instantaneous transfer of energy. The proposed grammar extends the comparison from transfer to **accessible capacity**: how much domain-specific capacity becomes available when a substrate is coherently activated.

**Function within the grammar.** This pattern supplies the shared sentence structure from which the Resonant Capacity Law is formed: substrate, activation, coherence gain, conversion, and limiting conditions.

#### 4.1.1 Operational Contract for a Matched Lumped Comparison

“The same lumped level” is not established by calling five equations zero-dimensional. Two records are compared at matched resolution only when each declares the same modelling commitments:

| Contract field | Required declaration |
| --- | --- |
| System boundary | What is inside the model, what is environmental, and which ports cross the boundary |
| Retained states | The finite set of storage variables or modes retained |
| Eliminated structure | Spatial modes, delays, boundary layers, memory, fluctuations, or couplings removed by reduction |
| Power variables | The conjugate effort and flow variables where an energetic port is claimed |
| Storage | The energy or availability functional and its reference state |
| Constitutive elements | Inertive, compliant, resistive, source, transformer, gyrator, or other closures used |
| Interconnection topology | How elements are connected; a shared role vocabulary does not imply a shared series equation |
| Input and output | Source type, measured response, observation point, and amplitude convention |
| Operating regime | Linearity, passivity, locality, time invariance, near-equilibrium assumptions, and admissible amplitude/frequency range |
| Adequacy criterion | A scale-separation or error condition justifying the lumped reduction—for example wavelength large relative to device dimensions or internal equilibration fast relative to forcing |
| Breakdown lift | The first omitted state, operator, boundary effect, or nonlinearity expected when the criterion fails |

Only records satisfying this contract may be placed in one comparative row. A thermal engineering RC model may be dynamically comparable to another first-order network without thereby making $(\Delta T,\dot Q)$ a power-conjugate bond; its energetic thermal variables and availability reference must be recorded separately.

This contract makes the comparison falsifiable. A mapping fails when it requires incompatible boundaries, retained states, energetic meanings, topologies, or validity regimes, even if the displayed differential equations have the same algebraic shape.

#### 4.1.2 What Complete Archetype Coverage Would Establish

If every equation in a prespecified corpus can be derived as a role-preserving specialization of one archetype under the contract above, the result establishes a **representation theorem for that declared model class**. This is stronger than visual analogy: it proves closure of the corpus under an explicit common grammar and identifies each domain equation as a specialization, degeneration, reduction, or lift of the parent form.

The strength of that result depends on the archetype's constraint. A parent expression with unrestricted functions, operators, or fitted coefficients can reproduce almost any equation and is therefore weak evidence. A scientifically substantive archetype must:

1. use fixed physical roles and dimensional rules;
2. restrict admissible storage, interconnection, dissipation, and boundary structures;
3. derive the child equations without post hoc redefinition of its primitives;
4. identify equations or mappings that are inadmissible;
5. predict which term, state, or operator appears when a declared reduction fails.

Accordingly, exhaustive successful mapping can prove structural universality over the stated class. It becomes a broader empirical law of nature only if the same fixed archetype also supplies content not guaranteed by class membership—for example an independently testable invariant, bound, correction, exclusion, or failure threshold in a held-out realization.

#### 4.1.3 Admissibility Framework for the One Candidate Formula

The programme has one candidate universal formula: the Resonant Capacity Law,

$$
\boxed{
\mathcal K_r=\kappa\Sigma(\Psi G_r)^2
}
$$

or

$$
\boxed{
\text{Capacity}
=
\text{Substrate}
\times
(\text{Activation}\times\text{Resonant gain})^2.
}
$$

The typed open dissipative Hamiltonian system below is **not** a competing universal formula. It is an established structural framework used to decide whether a proposed domain binding of the Resonant Capacity Law preserves storage, power, dissipation, and boundary meaning:

$$
\boxed{
\dot x=[J(x)-R(x)]\nabla H(x)+B(x)u,
\qquad
y=B(x)^{\mathsf T}\nabla H(x)
}
$$

subject to

$$
J=-J^{\mathsf T},
\qquad
R=R^{\mathsf T}\succeq0.
$$

These restrictions imply the non-negotiable balance

$$
\boxed{
\dot H=u^{\mathsf T}y-
\nabla H^{\mathsf T}R\nabla H
\le u^{\mathsf T}y.
}
$$

Here $x$ is a declared state, $H$ is a physically derived energy or availability functional, $J$ is the power-preserving interconnection structure, $R$ is the dissipative structure, and $(u,y)$ is a power-conjugate boundary or source port. For distributed systems, gradients become variational derivatives and $J$, $R$, and $B$ become differential or integral operators with domains and boundary traces specified explicitly.

This admissibility framework is constraining rather than merely accommodating:

- the reversible part cannot create or destroy $H$ because $J$ is skew-adjoint;
- the dissipative part cannot increase $H$ in an unforced passive system because $R$ is positive semidefinite;
- interconnection must preserve port power;
- storage and port variables must be dimensionally and physically typed;
- boundary power must close the balance;
- the child equation must be derived by a stated state choice and reduction, not fitted by assigning an arbitrary residual to $J$, $R$, or $H$.

The thermodynamic binding requires an energy–entropy or exergy-consistent extension. If $H$ denotes exergy relative to a declared environment, irreversible evolution may satisfy the same dissipation inequality while total energy conservation and non-negative entropy production remain separately auditable. A GENERIC-style energy–entropy structure is an admissible parent where one Hamiltonian alone cannot encode both laws without ambiguity.

This framework does not make every known physical equation a Resonant Capacity binding. A proposed binding fails when no physically justified state and storage functional yield the required storage coefficient and capacity measure; when the selected activation is not the corresponding energetic coordinate; when $G_r$ is not an independently defined dimensionless transfer gain; when ports do not close the balance; or when the system has no resonant regime at the declared scale. Such exclusions give the candidate law content.

The Hamiltonian framework derives and audits the ingredients; the Resonant Capacity Law is the proposed cross-domain compression of their resonantly activated quadratic-capacity specialization. It applies when $H$ has the relevant locally quadratic storage coordinate and the declared dynamics produce a resonant transfer gain. Intermediate balance, propagation, boundary, superposition, and stability equations support or delimit that binding; they are not claimed to be algebraic instances of the capacity formula itself.

#### 4.1.4 Gate-Level Derivation Chain

The gate-level evidence supplies a derivation environment rather than additional candidate universal formulas:

$$
E=H(x)
\rightarrow
e,f,\;P=ef
\rightarrow
\text{interconnection and balance}
\rightarrow
\text{coupled storage and loss}
\rightarrow
G_r
\rightarrow
\mathcal K_r=\kappa\Sigma(\Psi G_r)^2.
$$

The chain is admissible only with the following distinctions:

- $E=H(x)$ defines storage, while $\dot E=P_{in}-P_{out}$ is a balance law;
- generalized effort is not universally a negative potential gradient, because nonconservative and induced efforts exist;
- junction constraints preserve power but are not identical to local conservation or static force balance;
- $M\ddot q+R\dot q+Kq=u$ describes a declared second-order linear topology, while $M=0$ is a relaxation branch rather than an oscillator;
- a dimensionless drive/opposition ratio is a regime-analysis template, not one universal threshold law.

#### 4.1.5 Transformation Accounting Without Double Counting

A transformation ledger may use directed port powers

$$
\dot E_i=\sum_{j\ne i}P_{j\to i}-\sum_{j\ne i}P_{i\to j}+P_i^{ext},
$$

but only after the $E_i$ form a mutually exclusive partition. The five pedagogical domains do not automatically supply such a partition: acoustic energy is commonly selected mechanical energy of a compressible medium; hydraulic energy is fluid mechanical energy at another resolution; and Joule or viscous “loss” becomes internal energy when the receiving store remains inside the boundary.

Consequently $E_m+E_{th}+E_a+E_{em}+E_f$ is not asserted as a universal conserved sum. Each example must define exclusive carriers or modes, prevent double counting, and include all relevant stores and boundary transfers. The grammar compares domain dialects; it does not presume five additive kinds of energy.

#### 4.1.6 Second-Pass Binding Result

At the matched lumped level, the new information supplies the following direct specializations of the candidate formula:

$$
\begin{aligned}
\mathcal K_{m,r}&=\frac12m(G_vv_0)^2,
&\mathcal K_{a,r}&=\frac12M_a(G_UU_0)^2,\\
\mathcal K_{em,r}&=\frac12L(G_II_0)^2,
&\mathcal K_{h,r}&=\frac12I_h(G_QQ_0)^2,
\end{aligned}
$$

with dual compliant forms obtained only by pairing the corresponding effort with its compliance. In each displayed flow-side form,

$$
\kappa=\frac12,
\qquad
\Sigma\in\{m,M_a,L,I_h\},
\qquad
\Psi\in\{v_0,U_0,I_0,Q_0\},
$$

and $G_r$ is the transfer gain of that same response variable under a declared protocol. These are genuine child formulas, but they share the conventional linear quadratic-storage construction.

Ordinary thermal RC does not provide the fifth specialization. Its internal-energy change $\Delta U=C_{th}\Delta T$ is linear for constant heat capacity and its one-store dynamics relax rather than resonate. The quadratic thermal candidate is instead the near-environment exergy

$$
B_T\simeq\frac{C_{th}}{2T_0}(\Delta T)^2,
$$

which binds to Resonant Capacity only if a separate physical model predicts a dimensionless gain of the same temperature-deviation coordinate. Setting an inertance coefficient to zero does not turn relaxation into resonance and does not justify assigning $G_r$.

This earlier four-plus-one result is completed by the closed-cavity second-sound projection, which supplies a defensible thermodynamic resonant mode without changing capacity, activation, or gain. Fourier RC remains the asymmetric negative control. Together the admitted systems establish the five-domain representation theorem over the declared linear one-mode class.

#### 4.1.7 Academic Engine

The comparative method is operationalized as a thirteen-slot academic engine. Each domain–slot cell combines an exact formula, scientific role, equation type, maturity, units, abstraction, regime, boundary/topology, provenance, drift detector, imputation question, falsifier, independence tier, and explicit relevance to the five Resonant Capacity terms.

The engine does not assume that every slot is physically present or equally mature. Its admissible outputs include established, restricted, analogue-only, absent/degenerate, unresolved, and rejected mappings. This preserves negative evidence and prevents the visual completion of a $13\times5$ matrix from being treated as proof.

The Fibonacci gates organize navigation through the engine. Neither gate membership nor numerical position contributes evidential weight to the candidate law unless a separate preregistered quantitative prediction depends on it.

The engine separates four axes that must not be compressed into one maturity label: equation type, epistemic status, mapping verdict, and evidence role. A constitutive law can be well established yet map inadmissibly to a given slot; an analogue can be pedagogically useful yet provide no evidence for Resonant Capacity; an absent cell can be a correct negative result.

A formula record enters the comparative matrix only after typed-variable, dimensional, role, energetic, boundary, regime, provenance, and falsifiability checks. Resonant Capacity membership is a second decision requiring derived quadratic capacity, coordinate-consistent activation and gain, independently determined $G_r$, an evidenced resonant regime, and frozen $\kappa$.

To prevent circularity, records used to define the grammar are marked as construction cases. A frozen engine version is then applied to separate calibration and held-out sets. Changes to primitives or admission rules invalidate the held-out status of affected records. The grammar can therefore be proved over a declared corpus without treating its construction examples as independent discoveries.

#### 4.1.8 Fibonacci Gate Projection

The thirteen-slot engine and the Fibonacci gate sequence serve different functions. The thirteen slots provide the scientific audit path. The sequence

$$
1,1,2,3,5,8,13
$$

provides an optional navigational projection: storage, persistence, drive, interaction, circulation, rhythm, and regime. It does not mathematically generate the thirteen slots, and its numbers do not enter the Resonant Capacity Law.

The gate projection may reveal useful clustering, but scientific claims are invariant under removal of the Fibonacci labels unless a separate preregistered test demonstrates added explanatory or predictive value. This gives the scaffold its own falsifier: if a simpler non-Fibonacci organization performs equally well, Fibonacci alignment remains editorial rather than physical.

Empty or weak cells are interpreted through the engine's admissibility rules. A gap is imputed only when physical theory expects a role and the role is neither already known under different terminology nor excluded at the declared scale. Cross-domain symmetry alone is insufficient.

The deeper object beneath the presentation is a typed network of scientific relations, not a mandatory linear progression. The thirteen-step sequence is one traversal; Fibonacci gates are a projection over it. Paper 0 therefore does not claim that Fibonacci alignment is presently physical or predictive.

Its organizational value has the null that an unlabelled engine, conventional taxonomy, or permuted grouping performs equally well. Resonant Capacity stands or falls on its bindings regardless of that comparison.

#### 4.1.9 Basic-Law Reader View

A plain-language basic-law table may sit above the academic engine as a pedagogical façade. Its purpose is to help readers ask about storage, drive, exchange, conservation, dissipation, deformation, resistance, propagation, resonance, boundaries, and regime validity using familiar examples.

This façade is not evidence that the examples instantiate one law family. Every cell must link to qualified engine records, and the underlying record—not the simplified wording—determines scientific status and Resonant Capacity relevance. The façade contributes directly to documentation and accessibility, but contributes to the representation theorem only after its examples pass the engine's membership protocol.

The strongest accepted elementary transposition is

$$
e_R=\mathcal Rf,
\qquad
P_D=\mathcal Rf^2,
$$

for a passive linear resistive element. General impedance, thermal engineering analogies, nonlinear friction, and distributed transport require their own qualifications and cannot be collapsed into the scalar resistor without loss of physical role.

#### 4.1.10 Supporting Evidence and Claim Boundary

Established literature supports the grammar's construction. Port-Hamiltonian systems on open graphs combine storage, dissipation, effort/flow relations, interconnection, and boundary power.[^ph-graphs] Acoustic inertance and compliance follow from linearized Euler and continuity equations when elements are small relative to wavelength; their coupling gives a Helmholtz resonator, while quality factor requires loss and radiation modelling.[^swift-lumped] Hydraulic research derives and tests reduced resistance/inertia models and shows why steady pipe coefficients can fail for complex viscous passages.[^higo-hydraulic]

Thermodynamic evidence supports the programme's asymmetry. Temperature and entropy flow form the energetic thermal power pair,[^thoma-thermal] while exergetic port-Hamiltonian formulations encode first- and second-law structure.[^ephs] A distributed Navier–Stokes–Fourier EPHS model separates kinetic/internal storage from conduction and viscous mechanisms, supporting explicit partition and boundary accounting.[^ephs-nsf]

None of these sources proposes or tests $\mathcal K_r=\kappa\Sigma(\Psi G_r)^2$. They establish the parent grammar, child-model ingredients, and exclusions. Novelty and proof must reside in the fixed synthesis, complete bindings, and any held-out increment—not in effort–flow networks, acoustic analogy, or exergy modelling themselves.

#### 4.1.11 Constructive Thermal Completion Candidate

The thermal column need not end with Fourier relaxation. Second sound provides an established thermodynamic wave in which entropy/temperature disturbances propagate through out-of-phase normal and superfluid motion. Two-fluid theory supplies a quadratic variational functional, cavity experiments supply resonances and linewidths, and parametric studies supply amplification and nonlinear failure thresholds.[^second-sound-review][^second-sound-resonator][^second-sound-parametric]

Projecting a normalized second-sound mode onto $a_2(t)$ gives the candidate child form

$$
H_2=\frac12M_2\dot a_2^2+\frac12K_2a_2^2,
\qquad
\mathcal K_{T,r}=\frac12M_2(\dot a_{2,0}G_2)^2.
$$

This preserves the Resonant Capacity roles without calling ordinary thermal relaxation resonance. The Fourier RC case remains the negative control; the second-sound cavity becomes the positive thermodynamic construction. A complete certificate still requires independent derivation of mode normalization, coefficients, coupling, gain, loss, and boundaries and an experimental comparison using separate amplitude and power-loss energy estimates.

#### 4.1.12 Constructive proof target

The strengthened target is now an explicit conditional theorem rather than a search for visual resemblance:

> For every admitted small-amplitude resonant mode in the frozen five-domain corpus, if (i) the mode has an independently derived positive quadratic storage functional, (ii) the activation coordinate is one of that functional's conjugate effort/flow coordinates, and (iii) resonant gain is the transfer ratio of that same coordinate under a frozen source, output, boundary, and normalization convention, then its resonantly accessible modal capacity has the role-preserving form
> $$
> \mathcal K_r=\kappa\Sigma(\Psi G_r)^2.
> $$

This statement is restrictive. It admits linear mechanical, acoustic, electromagnetic, hydraulic, and second-sound modes when their certificates are complete. It rejects ordinary Fourier RC relaxation as a resonant member; non-quadratic, multimode, nonlinear, hysteretic, turbulent, shock, and regime-changing cases are outside the theorem unless an explicit reduction produces the required positive quadratic mode. No primitive may be redefined between children, and $\kappa$ may encode only a declared peak, mean, geometric, distributed, or normalization convention—not a fitted residual.

The proof is analytical. It derives $\Sigma$, $\kappa$, $G_r$, response amplitude, and capacity from closed governing, constitutive, source, and boundary equations; declares $\Psi$; demonstrates dimensional closure; and records admission and rejection conditions. No measured target amplitude is required. The same parent system generates the five child bindings by frozen role-preserving substitution, establishing the representation theorem. Apparatus replication and held-out empirical-law tests are optional extensions maintained in [Resonant Capacity Empirical Validation Programme](../../04-future-research/Resonant-Capacity-Empirical-Validation-Programme.md), not prerequisites of Paper 0's theorem.

#### 4.1.13 Operator-completeness audit

The discovery corpus adds a thirteen-question audit around each candidate child model: conservation/balance, storage, drive, constitutive response, flux, equilibrium, propagation, resonance, dissipation, boundary, superposition, nonlinearity, and regime scaling. The audit does not replace the Resonant Capacity Law and does not assert that every row is present in every realization. Its function is to expose missing conditions that could make an apparent binding circular or false.

For a Resonant Capacity certificate, the minimum connected subgraph is:

$$
\text{balance}
\rightarrow
\text{storage functional}
\rightarrow
\text{constitutive/interconnection structure}
\rightarrow
\text{modal dynamics}
\rightarrow
\text{gain and dissipation}
\rightarrow
\text{boundary and regime limits}.
$$

The certificate fails if it has energy without a balance ledger, gain without a declared input/output transfer function, resonance without complementary reversible storage, lossless amplification without a source and dissipation account, or a result applied outside its dimensionless validity regime. This converts the thirteen-slot matrix from an analogy display into a proof-completeness instrument.

The corpus also identifies an optional route beyond the representation theorem. Dimensionless groups derived from competing terms can define held-out admission, saturation, or failure boundaries. If the same role-preserving construction derives such a boundary more specifically than the null child descriptions, that would support a stronger R4 empirical-law claim. It is not required for C11 closure at the representation-theorem level, and the dimensionless group must be derived rather than invented after observing the transition.

#### 4.1.14 Cross-domain analogue layer

The broader twenty-family inventory is retained as a discovery layer behind the compressed thirteen-slot engine. Compression is many-to-many: reciprocal exchange becomes interconnection metadata; limiting speed qualifies propagation; geometric dilution depends on conservation and geometry; irreversibility joins the Energy–Entropy–Exergy ledger; variational structure records derivational provenance; and field–medium coupling qualifies constitutive and boundary records. No scientific category is deleted merely to preserve a thirteen-row display.

The analogue layer makes three distinct claims:

1. the five domains repeatedly require comparable modelling questions;
2. answers to those questions may occupy corresponding effort–flow, balance, storage, boundary, or regime roles;
3. a role correspondence becomes a Resonant Capacity specialization only after the complete membership certificate passes.

Thus “potential difference creates flow,” “medium determines response,” “resistance limits transfer,” and “boundaries transform disturbances” are useful search heuristics. They are not unconditional laws. Conservative-force gradients, Fourier transport, inertial pressure-gradient dynamics, Ohmic conduction, and hydraulic resistance differ in operator order, reversibility, locality, and constitutive assumptions. The engine preserves those distinctions while testing whether they participate in the same higher-level capacity construction.

The final master table should therefore expose both layers: the readable law-family analogue and the authoritative qualified record. Each displayed cell links to its governing equation, role, dimensions, conditions, provenance, drift detector, correction, and Resonant Capacity relevance. This realizes the requested cross-domain mapping without allowing the façade to overrule the physics.

#### 4.1.15 Typed correspondence rather than analogy by resemblance

A cross-domain edge is assigned exactly one primary correspondence type:

| Type | Meaning | Evidential use |
| --- | --- | --- |
| `Identity` | Same physical quantity and law under notation or coordinate change | One realization, not independent confirmation |
| `Isomorphism` | Invertible structure-preserving map over the declared model and regime | Strong representation-theorem support |
| `Reduction/Lift` | Many-to-one elimination or reconstruction with an adequacy and error contract | Conditional support at the reduced resolution |
| `Role homology` | Different mechanisms occupy the same qualified grammar role | Discovery and translation; certificate still required |
| `Phenomenological similarity` | Similar observed behavior without a preserved governing structure | Hypothesis generation only |
| `Metaphor` | Semantic resemblance without physical operationalization | Exposition only |
| `Rejected/none` | Required invariants fail or the role is physically absent | Negative evidence and scope definition |

For a proposed transposition $T:D_i\rightarrow D_j$, the engine evaluates a preservation vector

$$
\Pi(T)=
(u,p,b,h,o,c,\partial,r),
$$

where the entries record preservation of units/dimensions $u$, power pairing $p$, balance structure $b$, storage or Hamiltonian structure $h$, operator order $o$, causal/input–output structure $c$, boundary/topology $\partial$, and validity regime $r$. Each entry is `preserved`, `transformed with a declared map`, `lost`, or `not applicable`. An isomorphism cannot contain an undeclared loss. A role homology may contain losses, but those losses prevent it from serving as a derivation.

The mapping is directional. A distributed acoustic field may reduce to a lumped inertance–compliance network, but the lumped network does not uniquely reconstruct the field. Similarly, an electrical circuit and a mechanical oscillator may be isomorphic at the state-equation level while differing in constitutive origin and evidential independence. This prevents symmetry of notation from being mistaken for symmetry of physical explanation.

#### 4.1.16 Compression-loss audit

The twenty-to-thirteen transformation is stored as a versioned crosswalk rather than performed implicitly. For every merged family the audit records:

1. source and destination record identifiers;
2. whether the merge is an alias, subtype, qualifier, or genuine aggregation;
3. information suppressed in the reader-facing table;
4. a retrieval test showing that the suppressed relation can be recovered;
5. a collision test showing that non-equivalent mechanisms remain distinguishable;
6. the effect of the merge on Resonant Capacity admission.

Compression succeeds when it shortens the representation while preserving correct classification, rejection, and reconstruction of held-out records. It fails when, for example, equilibrium is confused with a standing-wave solution, resistance with impedance, relaxation with resonance, dissipation with irreversibility, or nonlinear response with instability. This supplies a measurable rather than aesthetic meaning of grammatical compression.

#### 4.1.17 Cross-domain falsification tests

The analogue map makes prospective tests possible:

- **unit/power test:** reject a mapping whose purported effort–flow pair does not yield the declared power or whose substrate–activation product does not yield capacity;
- **operator-order test:** reject a constitutive identity that maps a gradient law to an inertial time-derivative law without an explicit state transformation;
- **energy-sign test:** reject a storage binding whose quadratic form is not positive on the admitted stable modes;
- **boundary test:** change load or interface conditions and test the predicted transformation of $G_r$ and loss;
- **regime test:** cross a preregistered dimensionless boundary and test the predicted failure or correction;
- **negative-role test:** verify that Fourier RC relaxation, a pure resistor, and other one-store or dissipative systems are not falsely classified as resonant capacity modes;
- **round-trip test:** where an isomorphism is claimed, map a child model to the archetype and back and recover its equations and declared constraints without fitted residue.

Passing these tests would support a restrictive grammar. Failure localizes whether the problem lies in the domain binding, the compression ontology, or the proposed parent law.

#### 4.1.18 Gold-standard certificate execution

The proposed protocol has now been executed analytically in [Resonant Capacity R3 Certificates](../../02-proof/Resonant-Capacity-R3-Certificates.md). One series effort-driven parent model and one convention set are frozen across the realizations:

$$
\Psi=\frac{e_0}{\omega_0\mathcal I},
\qquad
G_r=Q=\frac{\omega_0\mathcal I}{\mathcal R},
\qquad
\mathcal K_r=\frac12\mathcal I(\Psi G_r)^2.
$$

The RLC reference includes a numerical benchmark. Acoustic and hydraulic certificates use identical definitions with pressure and volume velocity/flow. Second sound uses a mode-projected generalized effort and modal rate; its closed-cavity equations derive modal inertia, stiffness, and eigenfrequency from geometry and equilibrium two-fluid functions.

The analytical execution establishes the representation theorem without freely fitted functions, measured target-amplitude input, or child-specific primitive redefinition. Apparatus-level agreement between amplitude/storage and power/loss routes remains valuable validation, but belongs to the optional empirical programme rather than the theorem's proof burden.

#### 4.1.19 Context binding and C09 closure

The cross-domain analogue table supplies the semantic context, especially storage, drive, constitutive response, transport/flow, reciprocal coupling, resonance, dissipation, boundary, scaling, field–medium coupling, and instability. The R3-v1.0 context matrix converts those roles into fixed operational choices for mechanics, electromagnetics, acoustics, hydraulics, and second sound.

Across all five, the controlled quantity is peak sinusoidal source effort at the admitted one-port; the output is common series flow; the response is steady-state at the derived resonance; the baseline is $e_0/(\omega_0\mathcal I)$; gain is $Q$; capacity is total cycle-mean modal energy; and source/load effects are included in or explicitly connected to the declared total inertance, compliance, and resistance. The domain table then fixes the physical meaning, location, boundary, loss, and validity regime of each term.

C09 is closed for this declared context. Context dependence is preserved through versioning: a flow-driven, parallel, fixed-power, transient, distributed, or different-output experiment requires a new certificate identifier and cannot be pooled with R3-v1.0 without a derived conversion.

#### 4.1.20 $\kappa$ allocation and C03 closure

For R3-v1.0, $\kappa$ is not a domain-dependent normalization reservoir. It is fixed globally to $1/2$ by the use of peak activation and total cycle-mean modal energy at resonance. All five bindings demonstrate the same equipartition derivation.

Geometry and modal normalization belong in $\Sigma$; source and detector coupling belong in explicit operators; resistance, damping, radiation, and leakage belong in $\mathcal R$ and $G_r$; frequency and detuning belong in the transfer function; and boundaries belong in the governing topology and its reduced coefficients. Nonlinearity or saturation cannot be repaired with $\kappa$ and instead marks failure of R3-v1.0.

The coefficient is removed from all fitting procedures. A residual that can be eliminated only by altering $\kappa$ rejects the certificate. Different legitimate energy or amplitude conventions require a new version with an exact conversion. C03 is closed for the declared analytical protocol.

### 4.2 Semantic Seeds as Grammar Primitives

A semantic seed is not merely a fact. It is a compact generative unit:

$$
\boxed{
\text{Semantic seed}
=
\text{Pattern}
+
\text{Relations}
+
\text{Constraints}
+
\text{Provenance}
}
$$

Representative seeds include:

- effort $\times$ flow $=$ power;
- substrate $\times$ squared activation $=$ capacity;
- resistance $\times$ flow$^2$ $=$ dissipation;
- energy is conserved;
- entropy is generated;
- exergy is destroyed;
- linearity enables superposition;
- boundary mismatch produces reflection;
- a threshold changes the governing regime.

From such seeds, many domain-specific expressions can be regenerated. Regeneration does not mean unconstrained symbolic substitution: every expression inherits the seed's physical roles and must acquire domain bindings, units, boundary conditions, validity regime, maturity, and provenance. For example, resistance times flow squared represents dissipated power for the appropriate linear resistive constitutive relation, not an unconditional law for every dissipative system.

The Resonant Capacity Law combines several seeds: stored capacity has a substrate, stable capacity is locally quadratic in activation, resonance changes activation amplitude, and dissipation and regime boundaries limit the resulting gain.

**Function within the grammar.** Semantic seeds provide the grammar's compact generative vocabulary. They explain how a small set of physically constrained patterns can regenerate many domain expressions while preserving the evidence and limits needed to distinguish valid transposition from analogy by appearance.

### 4.3 Provisional Resonant Capacity Law

The grammar's provisional synthesis is:

$$
\boxed{
\mathcal K_r=\kappa\Sigma(\Psi G_r)^2
}
$$

Equivalently, in the grammar's physical terms:

$$
\boxed{
\text{Capacity}
=
\text{Substrate}
\times
(\text{Activation}\times\text{Resonant gain})^2
}
$$

where:

- $\mathcal K_r$ is, in R3-v1.0, the total cycle-mean recoverable energy of one normalized admitted mode at resonance;
- $\Sigma$ is the receiving substrate or storage coefficient;
- $\Psi$ is the relevant generalized activation; it becomes a bond-graph flow only in a flow-side binding;
- $G_r$ is a resonant response gain defined by an input, output, baseline, frequency, damping, and boundary;
- $\kappa=1/2$ in R3-v1.0, fixed globally by the peak-activation and cycle-mean-total-modal-energy conventions; it is not a domain fit parameter.

Here $\Sigma$ is a named substrate quantity, not a summation operator. The law proposes that the selected modal energy grows quadratically with coherent activation, subject to boundary conditions, dissipation, saturation, and regime limits. The square applies to the combined activation term $fG_r$; it does not by itself establish that every physical resonance produces unbounded quadratic growth. In each domain, $\Sigma$, $f$, and $G_r$ require operational definitions and dimensional closure, while the frozen $\kappa$ convention remains unchanged.

At Paper 0 stage, this law has maturity **I — Imputed**. It is the grammar's central hypothesis, not an established conservation law. Its centrality determines what the research proposal investigates; its provisional status determines how cautiously the paper may assert it.

**Function within the grammar.** The law is the proposed cross-domain invariant around which established capacity formulas are aligned, asymmetries are exposed, and new candidate bindings are generated.

### 4.4 What May Be Emerging

The proposed law can be read at three nested levels. The narrowest is a standard normal-mode energy relation. A broader level groups several substrate-times-squared-activation formulas into one quadratic-capacity family. The most general candidate principle connects that quadratic structure to stable equilibrium and treats resonance as a measurable amplitude gain. These levels should not be assigned equal maturity: the harmonic derivation is established within its regime, whereas its elevation to a universal five-domain principle remains imputed.

#### 4.4.1 The Resonant Capacity Law as a Normal-Mode Energy Law

For a harmonic mode with displacement-like coordinate

$$
a(t)=A G_r\cos(\omega t),
$$

the corresponding rate or flow amplitude is

$$
f_{\max}=\omega A G_r.
$$

If $\Sigma_{\mathrm{eff}}$ is the effective flow-side storage coefficient, the peak flow-side energy is

$$
\mathcal K_f
=
\frac{1}{2}\Sigma_{\mathrm{eff}}
(\omega A G_r)^2.
$$

This has exactly the proposed form

$$
\text{capacity}
=
\text{substrate}
\times
(\text{flow}\times\text{resonant gain})^2,
$$

with the unamplified rate amplitude $\omega A$ playing the role of $f$, $G_r$ the amplitude gain, and $\kappa=1/2$ for peak energy under this convention. For a sinusoidal time average, normalization, or another energy convention, the coefficient changes accordingly.

This gives the flow-side quadratic term an established physical basis for suitable linear harmonic modes. It does not make the cross-domain synthesis independently predictive, prove that every binding is a normal mode, or establish that one definition of $G_r$ transfers unchanged among domains.

For the canonical linear series topology,

$$
\mathcal I\dot f+\mathcal Rf+\frac q{\mathcal C}=e_s,
\qquad \dot q=f,
$$

the element laws determine

$$
\omega_0=\frac1{\sqrt{\mathcal I\mathcal C}},
\qquad
Q=\frac{\omega_0\mathcal I}{\mathcal R}
=\frac1{\mathcal R}\sqrt{\frac{\mathcal I}{\mathcal C}}.
$$

For a fixed sinusoidal source-effort amplitude $e_0$, flow observed at $\omega_0$, and inertive baseline $f_0=e_0/(\omega_0\mathcal I)$, the flow gain is $G_f=Q$. Hence

$$
H_{\mathcal I,r}
=\frac12\mathcal I(f_0Q)^2
=\frac{\mathcal I^2}{2\mathcal C\mathcal R^2}f_0^2.
$$

This is a rigorous specialization of the proposed grammar, not a topology-independent law. The equality $G_f=Q$ changes with the selected source, output, and baseline. Under fixed average input power at steady state, the same quality-factor definition instead yields

$$
H_{\mathrm{stored}}=\frac{Q}{\omega_0}P_{\mathrm{in}},
$$

so the stored energy scales linearly rather than quadratically with $Q$.

Both parameter statements require a declared intervention. In the fixed source-effort experiment, $f_0=e_0/(\omega_0\mathcal I)$ depends on $\mathcal I$ and $\mathcal C$. Consequently,

$$
\frac{\mathcal I^2}{2\mathcal C\mathcal R^2}f_0^2
=
\frac{\mathcal I e_0^2}{2\mathcal R^2},
$$

so the expanded baseline formula must not be interpreted as a causal parameter ranking under fixed $e_0$. Likewise, $H=(Q/\omega_0)P_{\mathrm{in}}$ is proportional to $Q$ only when $P_{\mathrm{in}}$ and $\omega_0$ are controlled.

**Contribution to the synthesis.** The normal-mode derivation shows that the squared resonant gain is not merely an observed algebraic resemblance. Within linear harmonic dynamics, it follows directly from differentiating an amplified amplitude and substituting the resulting flow amplitude into a quadratic storage law.

#### 4.4.2 A Broader Quadratic-Capacity Family

The overarching family may be written as

$$
\boxed{
\mathcal K=\kappa\Sigma\Psi^2
}
$$

where $\Psi$ is the characteristic activation appropriate to the system:

| System | Substrate $\Sigma$ | Activation $\Psi$ |
| --- | --- | --- |
| Relativistic rest energy | Mass $m$ | Invariant conversion scale $c$ |
| Mechanical mode | Effective mass | $\omega A G_r$ |
| Acoustic mode | Acoustic inertance | Volume-velocity amplitude |
| Electromagnetic resonator | Inductance or field susceptibility | Current or field amplitude |
| Hydraulic mode | Hydraulic inertance | Flow amplitude |
| Thermal effort mode | $C_{\mathrm{th}}/T_0$ | Temperature displacement $\Delta T$ |
| Thermal flow mode | Candidate thermal-flux inertance | Entropy-flow amplitude |

Outside R3-v1.0, $\kappa$ may label an explicitly versioned energy/amplitude convention or a different algebraic family member. Within R3-v1.0 it is fixed to $1/2$ and cannot encode physical realization, geometry, loss, coupling, or missing physics.

Relativistic rest energy is the intrinsic, neutral-gain binding of the capacity archetype:

$$
E_0
=mc^2
=1\cdot m(c\cdot1)^2.
$$

Mass is the substrate, $c$ is the invariant activation/conversion scale, $G_r=1$ is the neutral no-amplification state, and $\kappa=1$ belongs to the intrinsic-energy convention. This makes $E=mc^2$ the pure intrinsic member of the capacity family. It does not make $c$ a classical amplitude or claim that rest energy arises through oscillatory resonance.

Neutral gain is derived rather than fitted. The relativistic invariant

$$
E^2=p^2c^2+m^2c^4
$$

gives $E_0=mc^2$ at $p=0$. Therefore

$$
G_0^2
:=\frac{E_0}{\kappa\Sigma\Psi^2}
=\frac{mc^2}{1\cdot mc^2}
=1,
\qquad
\boxed{G_0=1}.
$$

Equivalently, the intrinsic case contains the identity activation-transfer map, whose dimensionless norm gain is unity. The notation denotes the neutral element of the multiplicative capacity grammar, not an operating resonator. This binding applies to massive systems with a rest frame; massless propagation and moving-state kinematic factors require different qualified records.

The stronger physical interpretation is retained as **H-RR, the Strong Relativistic Resonance Hypothesis**, rather than excluded. The Compton scales obey

$$
\omega_C=\frac{mc^2}{\hbar},
\qquad
\bar\lambda_C=\frac{\hbar}{mc},
\qquad
\boxed{\omega_C\bar\lambda_C=c}.
$$

Thus $c$ can be investigated as the peak generalized rate associated with a characteristic Compton-scale coordinate. H-RR asks whether a Lorentz-covariant periodic or phase-coherent degree of freedom physically realizes this rate and whether its independently derived, non-overlapping storage ledger yields the full $mc^2$. A harmonic rewrite alone is insufficient: with the naive scalar normalization it produces a $\tfrac12mc^2$ store, so the complementary storage, degree of freedom, or relativistic Hamiltonian structure must be derived rather than hidden in $\kappa$.

The hypothesis must recover relativistic dispersion and moving-state behavior, define what resonance means, and produce a discriminating consequence beyond combining $E=mc^2$ with $E=\hbar\omega$. Until then it is a core hypothesis-generating extension, not evidence used to prove the intrinsic binding or R3-v1.0. The dedicated relativity certificate and hypothesis boundary are developed in [Paper 1c — Einstein, Relativity, and the Intrinsic Capacity Binding](../01-direction-and-substrate/Einstein-Relativity-Capacity-Mapping-Paper-1c.md).

**Contribution to the synthesis.** The quadratic family separates the general substrate-times-squared-scale grammar from its specifically resonant realization. This prevents resonance from being projected onto every square-law formula while retaining a common mathematical classification.

#### 4.4.3 Stable Equilibrium as the Origin of the Quadratic Form

Near a stable equilibrium, a smooth capacity or potential function may be expanded about its equilibrium state. The first-order term vanishes at the stationary point, leaving the positive second-order term as the leading contribution:

$$
\Delta\mathcal K
\sim
\frac{1}{2}
(\text{effective substrate})
(\text{activation})^2.
$$

This local structure may explain why kinetic energy, spring energy, capacitor energy, inductor energy, acoustic energy, and many wave intensities are quadratic, and why thermal exergy becomes quadratic near equilibrium. The deeper shared pattern is therefore not resonance alone:

$$
\boxed{
\text{stable substrate}
+
\text{small coherent displacement}
\Longrightarrow
\text{quadratic accessible capacity}
}
$$

Under a fixed and declared linear source protocol, let $G_r$ denote the independently determined response-amplitude ratio relative to a fixed baseline. Because the selected capacity term is quadratic in that response amplitude, the corresponding capacity ratio is

$$
\frac{\mathcal K_r}{\mathcal K_0}=G_r^2,
$$

provided the substrate, frequency, energy convention, and baseline are held fixed and nonlinear saturation, parameter drift, and additional dissipation have not begun. This ratio is a consistency consequence of quadratic storage, not by itself a new prediction; predictive content requires $G_r$ or an additional bound to be determined independently.

The cleanest candidate form of the universal Resonant Capacity Principle is consequently

$$
\boxed{
\mathcal K_r
=
\kappa\Sigma(\omega A G_r)^2
}
$$

with $E=mc^2$ retained as the intrinsic neutral-gain binding of the same capacity archetype, while the modal certificates describe dynamically amplified members.

**Contribution to the synthesis.** The equilibrium argument identifies a possible reason the quadratic grammar recurs, while the gain relation isolates the specifically resonant and experimentally falsifiable claim. It therefore separates the origin of quadratic capacity from the additional effect of resonance.

### 4.5 Five-Domain Bindings

The initial low-dimensional comparison is:

| Domain | Substrate or storage term | Activation variable | Representative established capacity |
| --- | --- | --- | --- |
| Mechanics | Mass or compliance | Velocity or force | $\frac12mv^2$; $\frac{F^2}{2k}$ |
| Thermodynamics | Thermal capacity relative to $T_0$ | Temperature difference | $\frac{C_{\mathrm{th}}}{2T_0}(\Delta T)^2$ in the stated near-equilibrium availability approximation |
| Acoustics | Acoustic inertance or compliance | Volume velocity or pressure | $\frac12M_aU^2$; $\frac12C_ap^2$ |
| Electromagnetics | Inductance or capacitance | Current or voltage | $\frac12LI^2$; $\frac12CV^2$ |
| Fluid mechanics | Hydraulic inertance or compliance | Volume flow or pressure | $\frac12I_hQ^2$; $\frac12C_h(\Delta p)^2$ |

These formulas do not by themselves prove a new universal empirical invariant. Combined with the closed systems-of-equations derivation and frozen operational contract, however, they establish a representation theorem for the declared model class. The proposed $G_r$ term is bound to the same activation coordinate and derived from each admitted child system rather than inferred from resemblance.

Meaningful asymmetries are retained. For example, the thermodynamic expression depends explicitly on the environmental reference temperature $T_0$, while irreversible entropy production constrains accessible work. Such differences qualify the grammar rather than count as defects to be erased.

**Function within the grammar.** The bindings give the Resonant Capacity Law empirical and theoretical contact points. They identify which parts of the synthesis echo established formulas, which require domain-specific interpretation, and where the proposed coherence term introduces genuinely new work.

### 4.6 Qualification and Scientific Control

Every binding of the Resonant Capacity Law is recorded as a qualified relation:

$$
\mathcal{R}=(q,r,d,v,u,s,a,g,b,m,p)
$$

where $q$ is the mathematical relation, $r$ is physical role, $d$ is domain, $v$ is the variable binding, $u$ is dimensional information, $s$ is sign convention, $a$ is abstraction level, $g$ is validity regime, $b$ is the system boundary, $m$ is maturity, and $p$ is provenance.

The Energy–Entropy–Exergy triad adds three checks:

- **Energy** asks whether the capacity and transfer balances close.
- **Entropy** asks whether irreversible production is represented and non-negative.
- **Exergy** asks what useful capacity exists relative to an environment.

Relations are classified as foundational, constitutive, reduced, extended, imputed, or structurally absent. The grammar compares only compatible abstraction levels and retains rejected mappings as negative evidence.

**Function within the grammar.** Qualification is the law's scientific control layer. It prevents the central synthesis from acquiring authority through pattern recognition alone and makes every proposed binding dimensionally testable, regime-bound, provenance-aware, and falsifiable.

### 4.7 Added Value of the Grammar

The five-domain grammar serves as both a compact scientific worldview and a test environment:

- established formulas populate corresponding substrate–activation–capacity positions;
- the Resonant Capacity Law makes the proposed unifying structure explicit;
- meaningful asymmetries reveal domain limits and missing qualifications;
- incomplete positions become candidates for disciplined theoretical, empirical, or LLM-assisted imputation;
- maturity and drift controls separate established formulas from the proposed law and its candidate extensions;
- failed bindings remain informative rather than being hidden to preserve symmetry.

Its primary added value is therefore not metadata around known formulas. It is a falsifiable cross-domain synthesis that proposes where to look, while carrying the controls required to show where the synthesis holds, changes form, or fails.

**Function within the grammar.** This subsection converts the Resonant Capacity Law into an evaluation obligation. The grammar succeeds only if the law and its domain bindings improve explanatory compression, guide valid transposition or prediction, and expose informative failures more effectively than conventional analogy tables.

## 5. Drift Detection

Drift occurs when an apparently matching cell violates one or more comparison constraints. Each candidate transposition is checked against:

1. **role drift** — variables occupy different physical roles;
2. **dimensional drift** — units do not map coherently;
3. **abstraction drift** — models occupy incompatible levels;
4. **regime drift** — validity conditions differ materially;
5. **boundary drift** — system/environment partitions differ;
6. **maturity drift** — conjecture is compared as if it were established law;
7. **operator drift** — the mapped equation lacks a required derivative, integral, tensor, or nonlocal operator.

Represent a candidate mapping from domain $a$ to domain $b$ as $\mathcal{T}_{a\rightarrow b}$. It is admissible only if:

$$
\operatorname{Admissible}(\mathcal{T}_{a\rightarrow b})
=
R\land D\land A\land V\land B\land M\land O
$$

where $R$, $D$, $A$, $V$, $B$, $M$, and $O$ denote role, dimensional, abstraction, validity, boundary, maturity, and operator compatibility.

Failure is informative. A failed mapping may reveal a legitimate asymmetry, a missing operator, or a research gap rather than an error to be patched by analogy.

## 6. Constrained Imputation

Blank matrix cells are classified before candidate generation:

- **unknown but expected**;
- **absent by physical structure**;
- **hidden at another abstraction level**;
- **known under different terminology**;
- **candidate for empirical or theoretical research**.

An imputed relation must include:

| Requirement | Question |
| --- | --- |
| Source pattern | Which established row or transformation suggested it? |
| Variable binding | What does every symbol mean physically? |
| Units | Is the expression dimensionally valid? |
| Regime | Under what assumptions could it hold? |
| Boundary | What system and environment are assumed? |
| Conservation | Does the energy balance close? |
| Entropy | Is entropy production non-negative where required? |
| Falsification | What observation would reject it? |
| Maturity | Is it labelled explicitly as imputed? |

No candidate becomes part of the established grammar through structural elegance alone.

## 7. Conclusion

Existing work in bond graphs, port-Hamiltonian systems, nonequilibrium thermodynamics, GENERIC, and exergetic modelling establishes that physical domains can share energy-based structures without becoming physically identical. Building on that foundation, this paper proposes a five-domain grammar organized around the provisional Resonant Capacity Law:

$$
\boxed{
\mathcal K_r=\kappa\Sigma(\Psi G_r)^2
}
$$

or, in the grammar's physical terms:

$$
\boxed{
\text{Capacity}
=
\text{Substrate}
\times
(\text{Activation}\times\text{Resonant gain})^2
}
$$

The law expresses a recurring structure in which a substrate is activated through a generalized variable and its selected typed capacity measure is shaped by a defined resonant gain. Other coherence or coupling mechanisms require separate factors. Mechanics, second-sound thermodynamics, acoustics, electromagnetics, and fluid mechanics provide role-preserving bindings at a matched elementary or lumped level. Their closed systems of equations establish universality over the admitted quadratic two-store class; they do not establish applicability to every physical system or regime. In R3-v1.0, $\Psi$ and $G_r$ acquire operational, dimensional, and domain-specific meanings while $\kappa=1/2$ remains globally frozen by convention.

The grammar's qualification, maturity, drift, Energy–Entropy–Exergy, and imputation controls keep that distinction visible. Their purpose is to show where the law is derived, where it requires additional assumptions, and where it fails. The paper's contribution is therefore a bounded and falsifiable universal representation law together with the comparative grammar needed to apply and delimit it. Its inner–outer interpretation locates modal storage within the larger energetic relation through which a system is activated by, and returns energy to, its surroundings.

## 8. Potential Future Work

The immediate next step is to present the representation theorem compactly: state the admitted parent system, prove the Resonant Capacity form, list the five frozen substitutions, and publish counterexamples that fail admission. The proof dossier should remain equation-led and should not expand into apparatus metrology.

A second step is to complete the remaining grammar concerns concerning domain partition, multivariable equilibrium, literature novelty, operator-role separation, corpus circularity, Fibonacci increment, and correspondence typing. These determine how strongly the theorem can be interpreted and communicated.

Apparatus replication, uncertainty analysis, and held-out prediction are retained as optional work in [Resonant Capacity Empirical Validation Programme](../../04-future-research/Resonant-Capacity-Empirical-Validation-Programme.md). Success there could support a stronger empirical-law claim; absence of that work does not weaken the derived representation theorem or the hypothesis-generating comparative grammar.

The thermodynamic binding requires particular care. Future work should derive the near-equilibrium availability expression relative to $T_0$, retain entropy generation explicitly, and test whether coherent activation has a defensible thermodynamic interpretation rather than being imported by analogy.

The grammar should then be extended from elementary and lumped models to distributed fields, nonlinear regimes, memory, turbulence, shocks, hysteresis, and phase change. Reduction and lifting operators must remain explicit so that success at one abstraction level is not treated as proof at another.

Only after the physical bindings have been examined should optional machine-readable encoding, LLM-assisted imputation, alternative orderings, or a wider unified research programme be pursued. Those directions may amplify the grammar's usefulness, but they should follow evidence for the Resonant Capacity Law rather than substitute for it.

## References

[^schonfeld]: J. C. Schönfeld, “Analogy of Hydraulic, Mechanical, Acoustic and Electric Systems,” *Applied Scientific Research, Section B*, vol. 3, pp. 417–450, 1954. <https://doi.org/10.1007/BF02919918>

[^maschke]: H. M. Maschke and A. J. van der Schaft, “Port-Controlled Hamiltonian Systems: Modelling Origins and Systemtheoretic Properties,” *IFAC Symposium on Nonlinear Control Systems Design*, 1992. <https://ris.utwente.nl/ws/files/215811066/Maschke1992port_controlled.pdf>

[^broenink]: J. F. Broenink, “Bond Graphs: A Unifying Framework for Modelling of Physical Systems,” in *Foundations of Multi-Paradigm Modelling for Cyber-Physical Systems*, pp. 15–45, 2020. <https://doi.org/10.1007/978-3-030-43946-0_2>

[^overview]: A. J. van der Schaft and D. Jeltsema, “Port-Hamiltonian Systems Theory: An Introductory Overview,” *Foundations and Trends in Systems and Control*, vol. 1, nos. 2–3, pp. 173–378, 2014. <https://doi.org/10.1561/2600000002>

[^sound]: I. J. Busch-Vishniac and H. M. Paynter, “Bond Graph Models of Sound and Vibration Systems,” *Journal of the Acoustical Society of America*, vol. 85, no. 4, pp. 1750–1758, 1989. <https://doi.org/10.1121/1.397971>

[^bertuccio]: G. Bertuccio, “On the Physical Origin of the Electro-Mechano-Acoustical Analogy,” *Journal of the Acoustical Society of America*, vol. 151, no. 3, p. 2066, 2022. <https://doi.org/10.1121/10.0009803>

[^onsager1]: L. Onsager, “Reciprocal Relations in Irreversible Processes. I,” *Physical Review*, vol. 37, pp. 405–426, 1931. <https://doi.org/10.1103/PhysRev.37.405>

[^onsager2]: L. Onsager, “Reciprocal Relations in Irreversible Processes. II,” *Physical Review*, vol. 38, pp. 2265–2279, 1931. <https://doi.org/10.1103/PhysRev.38.2265>

[^ottinger]: H. C. Öttinger, “Nonequilibrium Thermodynamics for Open Systems,” *Physical Review E*, vol. 73, 036126, 2006. <https://doi.org/10.1103/PhysRevE.73.036126>

[^ephs]: M. Lohmayer, P. Kotyczka, and S. Leyendecker, “Exergetic Port-Hamiltonian Systems: Modelling Basics,” 2020. <https://arxiv.org/abs/2008.04091>

[^ephs-language]: M. Lohmayer, O. Lynch, and S. Leyendecker, “Exergetic Port-Hamiltonian Systems Modeling Language,” 2024. <https://arxiv.org/abs/2402.17640>

[^distributed]: A. Rashad, F. Califano, A. J. van der Schaft, and S. Stramigioli, “Twenty Years of Distributed Port-Hamiltonian Systems: A Literature Review,” *IMA Journal of Mathematical Control and Information*, vol. 37, no. 4, pp. 1400–1422, 2020. <https://doi.org/10.1093/imamci/dnaa018>

[^ph-graphs]: A. J. van der Schaft and B. M. Maschke, “Port-Hamiltonian Systems on Graphs,” 2011. <https://arxiv.org/abs/1107.2006>

[^swift-lumped]: G. W. Swift, “Nondissipative Lumped Elements,” <https://doi.org/10.1007/978-3-030-44787-8_8>.

[^higo-hydraulic]: H. Higo, F. Shimizu, and K. Tanaka, “Derivation of a Lumped Parameter System Model of a Flow Passage Simultaneously Modeling Resistance and Inertia and Verification in Basic Flow Passages,” 2021. <https://doi.org/10.5739/jfps.52.16>

[^thoma-thermal]: J. U. Thoma, “Bond Graphs for Thermal Energy Transport and Entropy Flow,” *Journal of the Franklin Institute*, vol. 292, no. 2, pp. 109–120, 1971. <https://doi.org/10.1016/0016-0032(71)90198-0>

[^ephs-nsf]: M. Lohmayer and S. Leyendecker, “Exergetic Port-Hamiltonian Systems: Navier-Stokes-Fourier Fluid,” 2022. <https://arxiv.org/abs/2204.05135>

[^second-sound-review]: H. Hu, E. Taylor, X.-J. Liu, S. Stringari, and A. Griffin, “Second Sound with Ultracold Atoms: A Brief Review,” <https://doi.org/10.1007/s43673-022-00055-2>.

[^second-sound-resonator]: “Analysis of a Second-Sound Resonator for Velocity and Viscosity Measurements in Liquid Helium II,” *Physica B+C*, vol. 104, pp. 285–302, 1981. <https://doi.org/10.1016/0378-4363(81)90175-3>

[^second-sound-parametric]: D. Rinberg and V. Steinberg, “Parametric Generation of Second Sound in Superfluid Helium: Linear Stability and Nonlinear Dynamics,” *Physical Review B*, vol. 64, 054506, 2001. <https://doi.org/10.1103/PhysRevB.64.054506>
