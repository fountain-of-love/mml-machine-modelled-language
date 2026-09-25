# The Worldview Layer

## A CML Experiment in Scientific Reasoning

This paper proposes a meta-level experiment for the **Common Language Model (CML)** introduced in [What MML is](../../../What.md) and developed further in the [SOS architecture](../../../sos/Architecture.md). It asks whether an explicit worldview model can become a distinct architectural layer for AI, separating durable conceptual structure from general linguistic capability and personal context.

The experiment is maintained in a **Seed Vault**, a durable knowledge base pilot whose contents are organized by CML. The names identify different architectural responsibilities: **CML is the schema; the Seed Vault is the knowledge base that applies it**. The vault name follows the analogy of the [Svalbard Global Seed Vault](https://www.seedvault.no/): it preserves compact, well-described material from which future diversity can be regenerated. Here, the preserved units are semantic seeds rather than biological seeds.

For the persistence architecture behind the Seed Vault, see [Dual-Persistence.md](../../../sos/Dual-Persistence.md). For the dual LLM/MML runtime and discovery engine that would query this structure, see [Dual-Engine.md](../../../sos/Dual-Engine.md).

The experiment uses a five-domain physical grammar covering mechanics, thermodynamics, acoustics, electromagnetics, and fluid mechanics as its first scientific demonstrator. The standalone proposal, [A Five-Domain Energy Grammar](../01-papers/00-foundation/Five-Domain-Energy-Grammar-Paper-0.md), develops its scientific foundations, novelty boundaries, hypotheses, comparison method, and evaluation programme. Its strategic aim is to illustrate the path away from ever-larger monolithic models and toward smaller generative engines connected to durable, inspectable, and evolvable worldview models.

## 1. Central Proposition

A contemporary language model performs several functions inside one dense parametric structure:

- linguistic generation;
- analogy and transposition;
- factual storage;
- conceptual organization;
- procedural reasoning;
- stylistic adaptation;
- user-specific contextualization.

The proposed architecture separates these functions across three layers:

$$
\boxed{
\text{AI capability}
=
\text{base model}
+
\text{user contextual model}
+
\text{explicit worldview model}
}
$$

Formally:

$$
\boxed{\mathcal{A} = M_{\theta} + C_u + W}
$$

where:

- $M_{\theta}$ is the general generative and transpositional model;
- $C_u$ is the active user-specific contextual model;
- $W$ is the explicit, durable worldview model represented through CML.

The central hypothesis is:

> A significant portion of what is currently stored diffusely in very large model weights can be compressed and externalized into compact, structured worldview models. This allows for smaller language models. It allows to retain or improve bounded-domain capability while reducing training cost, update cost, drift, opacity, and computational demand.

This is **architectural decomposition**, not merely conventional model compression. Adding a graph to an existing large model does not shrink its weights. The hypothesis is that future base models can be trained to rely on reliable worldview layers and therefore need not memorize every stable relation internally.

## 2. Why Test This Now?

Several research directions suggest that monolithic parametric storage is not the only route to capable AI:

- Retrieval-Augmented Generation separates parametric generation from non-parametric factual memory.[^rag]
- RETRO reported comparable performance in its evaluated settings while using substantially fewer parameters, although it depended on a very large retrieval database.[^retro]
- GraphRAG uses graph structure and hierarchical community summaries for global sense-making across large corpora.[^graphrag]
- Knowledge-editing research shows that repeatedly changing facts inside model weights can be unreliable and may degrade broader abilities.[^editing]
- TinyStories and related small-model work demonstrate that strong behavior is possible when the world, data, and task are carefully bounded.[^tinystories]

This evidence supports a direction, not the full claim:

> Better structure, external memory, curated knowledge, and task-specific distillation can sometimes substitute for scale.

The experiment shows how CML can systematize and extend that substitution.

## 3. Terminology and Repository Boundary

The project separates language, storage, indexing, and execution rather than naming all four “CML.”

| Concept | Responsibility | Repository meaning |
| --- | --- | --- |
| **CML — Common Language Model** | Defines concepts, relation types, formula roles, constraints, maturity states, provenance fields, and validation rules | The schema applied to vault contents; not the folder and not the stored knowledge itself |
| **Seed Vault** | Preserves semantic seeds, scientific papers, claims, equations, evidence, counterexamples, and competing versions | The `seed-vault/` knowledge-base folder |
| **MML — Machine Modelled Language** | Maps queries onto CML and traverses the structured knowledge and matrix/index | The deterministic query and diffusion engine |
| **LLM** | Reads sources, proposes mappings, generates explanations, and discovers candidate structures | A discovery and language engine whose output requires validation before deposit |

The relationship is:

$$
\boxed{
\text{Seed Vault contents}
\xleftarrow{\text{organized by}}
\text{CML schema}
\xleftarrow{\text{queried through}}
\text{MML}
}
$$

The Seed Vault may contain Markdown papers today and graphs, matrices, ontologies, executable constraints, and indexes later. A document belongs in the vault because it contributes knowledge or provenance. It becomes **CML-shaped knowledge** only when its concepts, relations, claims, constraints, maturity, and evidence are represented through the shared schema.

## 4. Three-Layer AI Architecture

### 4.1 Base Model

A base model (current LLMs) supplies language production, pattern recognition, analogy, transposition, synthesis, hypothesis generation, and general procedural capability.

A minimal illustration of relational transposition is:

$$
\operatorname{king}
-
\operatorname{man}
+
\operatorname{woman}
\approx
\operatorname{queen}
$$

Early embedding research demonstrated that syntactic and semantic relations appear as regular vector offsets.[^vectors] Modern language-model representations are more complex, but the example still illustrates the intended role: interpreting, traversing, combining, and expressing structures provided by the other layers.

The same transposition can be visualized as a relational square:

```text
King ───────── Queen
 │                │
 │                │
Man  ─────────    ?
```

The horizontal relation changes the masculine term into its feminine counterpart. The vertical relation moves from a royal role to the corresponding general human category. A current LLM can preserve both relations and answer the missing position with **Woman**:

```text
King ───────── Queen
 │                │
 │                │
Man  ───────── Woman
```

This is the capability the base-model layer is intended to showcase. Current LLMs are powerful transposition engines: they can recognize a relation in one part of a structure and carry it into another part, even when the surface words and domain change.

The base model should not need to memorise every current fact, domain taxonomy, formula catalogue, user preference, provenance chain, version history, institutional rule, or validated conceptual relation. Its responsibility is the general capability to interpret and transpose structures supplied through the contextual model and the Seed Vault.

### 4.2 Contextual Model

The contextual model is the active developmental layer. It contains current goals, accumulated terminology, recurring conceptual structures, user-specific distinctions, working hypotheses, unresolved tensions, active projects, provisional relations, and corrections accumulated through interaction.

This is where candidate structures emerge before they become durable CML-shaped knowledge. Consider several provisional triads. The first two rows name the shared roles: Simon Sinek’s Golden Circle moves from **Why** through **How** to **What**, while the systems-oriented vocabulary used here moves from **Kernel** through **System** to **Result**.[^golden-circle]

| Domain            | Substrate | Coordination     | Expression |
| ----------------- | --------- | ---------------- | ---------- |
| Golden Circle     | Why       | How              | What       |
| Systems theory    | Core      | System           | Result     |
| Human             | Mind      | Body             | Soul       |
| Organization      | C0O       | CO0              | CfO        |
| Computing         | Hardware  | Operating system | Software   |
| Abstract dynamics | Direction | Movement         | Form       |

Each **row** expresses a three-part organization in the vocabulary of one domain:

- **What–Why–Expressioin** distinguishes purpose, method, and observable expression in Sinek’s Golden Circle.
- **Core–System–Result** restates those roles as a systems-oriented progression from organizing seed, through mediating mechanism, to manifested outcome.
- **Body–CEO–Soul** describes a human being through embodied form, directing awareness, and animating or expressive life.
- **CFO–CEO–Soul** describes an organization through stewardship of material resources, strategic direction, and operational movement.
- **Hardware–OS–Software** describes a computing system through physical substrate, coordinating mediation, and executable expression.
- **Form–How–Movement** states the proposed archetype in domain-neutral language.

Each **column** gathers terms that occupy a comparable structural role. The first column asks **Why** and identifies a core, kernel, or form. The second asks **How** and identifies the coordinating system or direction. The third asks **What** and identifies the resulting movement or expression. Body, C0O, operating system, and form are treated as first-column bindings; Mind, CE0, operating system, and direction as second-column bindings; and Soul, CFO, software, and movement as third-column bindings. [Yes, with purpose as it's most valuable!]

These terms are not asserted to be literally equivalent. They are typed domain bindings to a reusable relational pattern. CML can store the three roles, their ordering and allowed relations once; the Seed Vault can store the domain-specific bindings, evidence, qualifications, and counterexamples. The LLM then performs the transposition between rows and can infer a missing cell from its row and column context.

This is the intended division of labour: the LLM retains general linguistic and transpositional capability, while durable conceptual topology lives explicitly in the CML-shaped Seed Vault. The system therefore need not encode every instance, mapping, and update solely inside opaque model weights.

This externalization does not eliminate human work. The present worldview has been cultivated manually “like a monk” for approximately nine months through repeated modelling, comparison, correction, and curation. For the AoE enthusiasts, Monks, we need Monks!! More than 1,000 conversations with frontier AI models, principally ChatGPT and Gemini, have been created to transpose candidate patterns across contexts, challenge inconsistencies, recover earlier distinctions, and refine the emerging structure. The project’s LinkedIn post documents an earlier stage of this sustained practice and its head start in treating context as an architecture to cultivate rather than as a disposable prompt.[^project-ace-post]

The name **Agentic Context Engineering (ACE)** refers to the formal framework introduced by Zhang et al. Their paper treats context as an evolving playbook and divides its development among generation, reflection, and curation, using structured incremental updates to preserve accumulated knowledge and resist context collapse.[^ace-paper] That paper is the conceptual research reference. The LinkedIn post serves a different purpose: it records this project’s practical history of manual context engineering, which began independently and earlier than the adoption of the ACE paper as supporting literature.

These conversations constitute developmental provenance and iterative internal validation, not independent scientific validation. A model agreeing with a pattern it helped generate is not sufficient evidence that the pattern is true. Durable deposits still require manual correction, explicit maturity labels, source verification, counterexamples, reproducible tests, and—in scientific domains—independent expert review. The Seed Vault makes that often-invisible labour inspectable instead of pretending that structure appeared automatically.

#### Exemplary Use Case: Deepening One Domain

The same grammar can be applied recursively inside a row. Instead of moving across human, organizational, computing, and abstract domains, it can deepen the human domain into candidate physiological and experiential structures:

| Human subdomain | Core                                   | System                                                      | Result                                      |
| --------------- | -------------------------------------- | ----------------------------------------------------------- | ------------------------------------------- |
| Body            | Heart                                  | Cardiovascular system                                       | Anatomy and embodied function               |
| Brain and mind  | Brain                                  | Nervous system                                              | Sensation and perception                    |
| Soul hypothesis | Unknown, or “soul” as a candidate core | Endocrine and neuroendocrine systems as candidate mediators | Emotions as candidate observable expression |

These rows do not have equal scientific maturity:

- In the **body** row, the heart and cardiovascular system illustrate a core organ acting through a distributed system to sustain embodied function. The heart is not the anatomical origin of the whole body, so “core” denotes a central functional role rather than a complete causal explanation.
- In the **brain and mind** row, the brain operates through the nervous system to support sensation and perception. The result still depends on the wider organism and environment rather than on an isolated component.
- In the **soul hypothesis** row, the endocrine–emotion connection is not merely speculative. Modern psychoneuroendocrine research studies how hormonal axes, immune signalling, neural activity, stress, mood, and emotion interact. Research on depression, including work informed by traditional Chinese medicine, explicitly models a neuroendocrine–immune network rather than treating emotion as isolated from the body.[^neuroendocrine-emotion] Traditional Chinese medicine also has a long-standing systematic vocabulary relating emotions to organs, $qì$, blood, and whole-body balance.[^tcm-emotion] These traditions and findings support investigating the **system-to-emotion** relation. They do not yet establish that the endocrine system is the mechanism of a soul, or that emotion is the scientific expression of one.

The distinction matters because traditional knowledge can preserve observations before their mechanism is legible to another scientific framework. The LinkedIn post by Wouter van Noort highlights this possibility through current research on the **interstitium** and its potential relationship to Chinese meridian traditions.[^interstitium-post] The underlying anatomical study found evidence that fluid-filled interstitial spaces continue across tissue and organ boundaries, suggesting a body-wide connective network with possible roles in signalling, cell traffic, and disease spread.[^interstitium-study] That is relevant precedent for taking an old whole-body model seriously enough to test. It is not, by itself, proof of acupuncture meridians, $qì$, an endocrine model of soul, or soul as a scientific entity.

The incomplete row immediately produces a legitimate CML research question:

> Can “soul” be translated into a scientifically operational construct, or does the apparent blank reveal a category boundary where physiological, psychological, phenomenological, and metaphysical descriptions should remain distinct?

This is precisely what a maturity-aware CML can expose. It can preserve the structural analogy, label the heart and brain mappings as simplified models, mark the soul mapping as imputed, and ask what observations would confirm, refine, or reject it. The purpose is not to let a persuasive triad manufacture a fact. It is to turn an intuition into an explicit, inspectable research hypothesis.

#### Exemplary Use Cases Across Engineering Domains

The same method has been applied beyond the human-domain example. Two open research repositories explore heat production and computer-chip design as systems problems rather than isolated engineering symptoms.

**Compost as a non-combustion heat process.** The [CTP compost thermal-process repository](https://github.com/fountain-of-love/ctp-compost-thermisch-proces) explores the proposition that useful heat does not always require burning material.[^ctp-repository] Composting still releases chemical energy through biological oxidation, but it does so through a managed decomposition process rather than a flame-based combustion process. The [Comité Jean Pain](https://comitejeanpain.be/) documents Jean Pain’s wood-composting method and describes extracting heat from the digestion process inside compost heaps, alongside compost and biogas production.[^jean-pain] In CML terms, the function **produce usable heat** is separated from the historically dominant implementation **burn fuel**:

$$
\boxed{
\text{required function: heat}
\neq
\text{required mechanism: combustion}
}
$$

**Computer chips as function-shaped systems.** The [computer-chip-design repository](https://github.com/fountain-of-love/computer-chip-design) questions a design trajectory dominated by placing more transistors into smaller areas and proposes evolving topology from functional requirements, communication paths, coherence, and physical constraints.[^chip-repository] Transistor density is not the industry’s only design objective, but it remains a powerful optimization pressure. The repository asks whether architecture should begin more explicitly with **what the system must do**, then derive the necessary topology, instead of treating density as the default proxy for progress.

Within this hypothesis, heat is read as a system signal. In a chip it arises from physical dissipation—including switching activity, leakage, resistance, interconnect, memory movement, and conversion losses—not from mechanical friction alone. “Friction” is therefore used as the broader CML role of **resistance, mismatch, or irreversible loss**. Cooling remains necessary for present hardware, but it primarily manages the resulting temperature. A deeper design programme also asks how to reduce the underlying dissipation that produces the heat:

$$
\boxed{
\text{heat}
\rightarrow
\text{observable symptom of dissipation}
\rightarrow
\text{trace the loss to its architectural source}
}
$$

Together, the compost and chip examples express the same transposition:

| Domain | Inherited mechanism | Functional reframing | Candidate alternative |
| --- | --- | --- | --- |
| Heat production | Burn material | Produce useful heat | Managed biological decomposition and heat recovery |
| Chip design | Increase density and cool the result | Satisfy computation with minimal dissipation | Function-shaped topology, communication, and coherence |
| Transportation | Refine combustion vehicles | Provide efficient mobility | Electric powertrains and an electrified energy ecosystem |

The transportation row is a strategic analogy. Elon Musk’s original Tesla master plan pursued a compelling electric car as an alternative to the established gasoline vehicle and used that first product as a step toward affordable electric mobility and a solar-electric economy.[^tesla-master-plan] Likewise, these repositories look for signals that an inherited mechanism is not the function itself. The claim is not that compost heat and alternative chip topology are already equivalent in readiness to electric vehicles. It is that CML can help separate **purpose from implementation**, reveal alternative mechanisms, and turn those analogies into explicit research programmes with measurable energy, performance, and lifecycle criteria.

The contextual model behaves as a **soft ontology** in which ontogenesis can occur:

$$
\boxed{
\text{conversation}
\rightarrow
\text{recurrence}
\rightarrow
\text{stabilized meaning}
\rightarrow
\text{candidate structure}
}
$$

This layer is the nursery in which a worldview can grow before every branch has been formally named. The exemplary use cases above show that nursery at work: analogies are proposed, transposed, corrected, maturity-labelled, and either rejected or prepared for later deposit.

### 4.3 Seed Vault: The Explicit CML-Shaped Worldview

The explicit worldview is deposited in the Seed Vault. It is persistent, structured, versioned, inspectable, independently testable, portable between models, attributable to sources, and able to represent contradiction and uncertainty.

It may use graphs, ontologies, matrices, schemas, equations, transformation rules, validity conditions, retrieval indexes, and executable constraints. Unlike an ordinary document collection, it stores relations and generative patterns—not only passages of text.

| Field | Purpose |
| --- | --- |
| Concept | Entity or principle represented |
| Functional role | Storage, effort, flow, boundary, mediation, or governance |
| Relations | Equivalent-to, transforms-into, opposes, constrains, or precedes |
| Formula archetype | General mathematical pattern |
| Domain formula | Domain-specific realization |
| Units | Dimensional constraints |
| Validity regime | Linear, near-equilibrium, lumped, or distributed |
| Maturity | Established, constitutive, reduced, extended, or imputed |
| Provenance | Evidence and source lineage |
| Counterexamples | Known failures and asymmetries |
| Drift detector | Signal that the representation is incomplete |
| Open slot | Candidate position for imputation |

This is a scientific realization of the architecture: the Seed Vault holds the knowledge, while CML supplies the shared semantic structure through which its claims, formulas, constraints, and evidence can interoperate.

## 5. Worldview Compression

### 5.1 Semantic Compression

A recurring pattern is stored once and instantiated many times. Instead of treating the following relations as wholly separate:

$$
F = bv
$$

$$
V = RI
$$

$$
\Delta p = R_a U
$$

$$
\Delta p = R_h Q
$$

$$
\Delta T = R_{\mathrm{th}}\dot{Q}
$$

the worldview stores their shared archetype:

$$
\boxed{\text{effort} = \text{resistance} \times \text{flow}}
$$

The individual equations become typed, dimensionally constrained projections of one common relation:

$$
\boxed{
\text{many surface expressions}
\rightarrow
\text{one structural pattern}
+
\text{domain bindings}
}
$$

### 5.2 Parametric Compression

If stable factual and relational knowledge is reliably externalized, a smaller base model may not need to encode all of it redundantly in its weights. The bounded-domain research target is:

$$
\boxed{M_{\mathrm{small}} + W \approx M_{\mathrm{large}}}
$$

More rigorously, define the minimum sufficient worldview as:

$$
\boxed{
W^*
=
\arg\min_W |W|
\quad
\text{subject to}
\quad
\operatorname{Perf}(M_s, C_u, W)
\geq
\operatorname{Perf}(M_L) - \varepsilon
}
$$

Here, $W^*$ is the smallest explicit worldview that lets the small model remain within tolerance $\varepsilon$ of the large model on a defined task set.

### 5.3 Update Compression

A changed fact or relation can be updated in one explicit, versioned Seed Vault record instead of retraining the base model, editing distributed weights, or duplicating the update across multiple fine-tuned models.

### 5.4 Context Compression

MML can use the CML schema and its index to retrieve the smallest relevant Seed Vault subgraph rather than inject entire documents into the context window. A query may need only the shared archetype, two domain bindings, their dimensional constraints, a relevant exception, and source references.

### 5.5 Governance Compression

Validation rules can be stored once and reused: dimensional consistency, conservation closure, entropy accounting, provenance, domain boundaries, regime validity, and contradiction handling.

## 6. Semantic Seeds

The repository name is inspired by the [Svalbard Global Seed Vault](https://www.seedvault.no/), which safeguards seed diversity for long-term conservation. The Semantic Seed Vault does not need to store every future expression; it preserves compact generative units capable of regenerating domain expressions in the right context.

$$
\boxed{
\text{semantic seed}
=
\text{pattern}
+
\text{relations}
+
\text{constraints}
+
\text{provenance}
}
$$

Examples include:

- effort multiplied by flow equals power;
- substrate multiplied by squared activation yields a capacity relation;
- resistance multiplied by squared flow yields dissipation;
- energy is conserved;
- entropy is generated;
- exergy is destroyed;
- linearity enables superposition;
- boundary mismatch produces reflection;
- a threshold changes the governing regime.

| AI layer | Seed-bank analogue |
| --- | --- |
| Base model | Germination and growth machinery |
| User contextual model | Active nursery or experimental garden |
| CML schema | Classification and preservation protocol |
| Seed Vault knowledge base | Curated seed bank |
| Scientific sources | Provenance and field records |
| LLM imputation | Recombination and candidate cultivation |
| Validation | Testing viability, fitness, and faithfulness |
| Versioning | Preserving lineages and mutations |

Like a serious conservation system, the Seed Vault must preserve variation, provenance, competing lineages, deprecated structures, local adaptations, and uncertainty rather than becoming a centralized canon. CML provides common structure without requiring one uncontested worldview.

## 7. Ontogenesis Cycle

The worldview is not designed completely in advance. It develops through human–AI interaction:

$$
\boxed{
\text{observation}
\rightarrow
\text{analogy}
\rightarrow
\text{recurrence}
\rightarrow
\text{candidate pattern}
\rightarrow
\text{formalization}
\rightarrow
\text{validation}
\rightarrow
\text{deposit}
\rightarrow
\text{reuse}
}
$$

Operationally:

1. A human introduces observations, intuitions, and distinctions.
2. The LLM searches for analogous structures.
3. Recurring relations stabilize in the contextual model.
4. Candidate nodes, relations, and equations are proposed.
5. They are checked against literature, dimensions, and counterexamples.
6. Validated structures are encoded through CML and deposited in the Seed Vault.
7. MML retrieves the relevant vault structure during later reasoning.
8. New cases expose gaps or force revision.

The update rule is:

$$
\boxed{
W_{t+1}
=
\operatorname{Validate}
\left(
W_t
+
\operatorname{Impute}(M_{\theta}, C_u, W_t)
\right)
}
$$

The essential operation is $\operatorname{Validate}$. Without it, the cycle merely crystallizes hallucinations.

## 8. The Scientific Demonstrator

The demonstrator is developed as a separate paper-like research proposal in [A Five-Domain Energy Grammar](../01-papers/00-foundation/Five-Domain-Energy-Grammar-Paper-0.md). That paper grounds the comparison in physical-system analogy, bond graphs, port-Hamiltonian systems, Onsager force–flow theory, GENERIC, exergetic modelling, and distributed port-Hamiltonian systems while isolating the proposed synthesis and its falsifiable claims.

The five-domain physical grammar tests four claims simultaneously.

### Compact Representation

A large body of scientific relationships can be represented through shared formula archetypes, five domain bindings, maturity labels, regime constraints, and cross-domain correspondences.

### Recurring Structure

Mechanics, thermodynamics, acoustics, electromagnetics, and fluid mechanics repeatedly instantiate relations involving storage, effort, flow, resistance, power, resonance, dissipation, boundaries, and regime changes.

### Assisted Discovery

The LLM assists with terminology translation, analogy search, formula alignment, abstraction matching, identification of weak cells, and candidate imputation.

### Structured Reuse

Once the grammar is explicit, the model can reason from a universal role to a domain binding rather than reconstructing every relationship from scattered prose:

$$
\boxed{
\text{worldview architecture}
\rightarrow
\text{physical worldview demonstrator}
\rightarrow
\text{evidence for worldview architecture}
}
$$

The physical model is therefore both a scientific contribution and a benchmark fixture.

## References

[^golden-circle]: Simon Sinek, “The Golden Circle,” *The Optimism Company*. <https://simonsinek.com/golden-circle>
[^ace-paper]: Qizheng Zhang et al., “Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models,” *ICLR 2026*, arXiv:2510.04618. <https://arxiv.org/abs/2510.04618>
[^project-ace-post]: Fountain of Love, “The Power of ACE — The Hidden Architecture of Intelligence,” LinkedIn, 2025. <https://www.linkedin.com/posts/fountain-of-love_agentic-context-engineering-activity-7386004122417655808-2xA0>
[^neuroendocrine-emotion]: Chan Li, Bishan Huang, and Yuan-Wei Zhang, “Chinese Herbal Medicine for the Treatment of Depression: Effects on the Neuroendocrine-Immune Network,” *Pharmaceuticals*, vol. 14, no. 1, 65, 2021. <https://doi.org/10.3390/ph14010065>
[^tcm-emotion]: Yifan Ding, Zhuxin Mao, Nan Luo, Zhihao Yang, and Jan Busschbach, “Differences and Common Ground in the Frameworks of Health-Related Quality of Life in Traditional Chinese Medicine and Modern Medicine: A Systematic Review,” *Quality of Life Research*, vol. 33, no. 7, pp. 1795–1806, 2024. <https://doi.org/10.1007/s11136-024-03669-1>
[^interstitium-post]: Wouter van Noort, “Onderzoekers ontdekken iets dat Chinese geneeskunde met de westerse kan verbinden,” LinkedIn, 2026. <https://www.linkedin.com/posts/woutervannoort_zo-dan-onderzoekers-ontdekken-iets-dat-chinese-share-7460919658364203008-Ro2O>
[^interstitium-study]: Odise Cenaj et al., “Evidence for Continuity of Interstitial Spaces across Tissue and Organ Boundaries in Humans,” *Communications Biology*, vol. 4, 436, 2021. <https://doi.org/10.1038/s42003-021-01962-0>
[^ctp-repository]: Fountain of Love, “CTP Compost Thermisch Proces,” GitHub. <https://github.com/fountain-of-love/ctp-compost-thermisch-proces>
[^jean-pain]: Comité Jean Pain, “Methoden Jean Pain.” <https://comitejeanpain.be/methoden-jean-pain-nl/>
[^chip-repository]: Fountain of Love, “Computer Chip Design,” GitHub. <https://github.com/fountain-of-love/computer-chip-design>
[^tesla-master-plan]: Elon Musk, “The Secret Tesla Motors Master Plan (Just Between You and Me),” Tesla, 2006. <https://www.tesla.com/secret-master-plan>
[^rag]: Patrick Lewis et al., “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” 2020. <https://arxiv.org/abs/2005.11401>
[^retro]: Sebastian Borgeaud et al., “Improving Language Models by Retrieving from Trillions of Tokens,” 2021. <https://arxiv.org/abs/2112.04426>
[^graphrag]: Darren Edge et al., “From Local to Global: A Graph RAG Approach to Query-Focused Summarization,” 2024. <https://arxiv.org/abs/2404.16130>
[^editing]: Peter Hase et al., “Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models,” 2023. <https://arxiv.org/abs/2305.13172>
[^tinystories]: Ronen Eldan and Yuanzhi Li, “TinyStories: How Small Can Language Models Be and Still Speak Coherent English?”, 2023. <https://arxiv.org/abs/2305.07759>
[^vectors]: Tomas Mikolov, Wen-tau Yih, and Geoffrey Zweig, “Linguistic Regularities in Continuous Space Word Representations,” 2013. <https://aclanthology.org/N13-1090/>
