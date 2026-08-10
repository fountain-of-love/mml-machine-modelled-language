# Enigma

Enigma is the name given here to a **conceptual, context-engineered model that runs on top of OpenAI**. It is not a separately trained foundation model, a permanent ontology inside the base model, or an official OpenAI product.

It describes the working context that emerges when a general-purpose model is repeatedly supplied with a researcher's terminology, distinctions, prior formulations, frameworks, source material, and evolving conceptual relationships. In this repository, Enigma helped articulate and connect MML, SOS, the five-domain physical grammar, and their supporting research boundaries.

Its outputs remain generated language and require human judgment, source verification, testing, and governance. Account-level context is also configurable and mutable; it should not be treated as a durable knowledge graph or authoritative record. The explicit documentation and governed structures in this repository are the durable artefacts.

## Account-Level Context as an Emerging Worldview Model

Explicit conceptual nodes need not yet exist as permanent structures inside the base model itself. In the present research, they are initially approximated through the account-level context surrounding the model.

Saved memories, referenced conversation history, recurring terminology, prior formulations, user-defined frameworks, and accumulated distinctions can be selectively reintroduced into later conversations. OpenAI describes saved memories as separate from chat history and explains that relevant information from previous conversations may be added to new ones when chat-history reference is enabled. These capabilities depend on account settings, plan, and product configuration and can be managed or disabled by the user ([OpenAI: How memory works](https://help.openai.com/en/articles/8590148-memory-faq), [OpenAI: Reference saved memories](https://help.openai.com/en/articles/11146739-how-does-reference-saved-memories-work)).

This creates an intermediate layer between an unmodified general-purpose language model and a formally implemented ontology:

```text
Base model
    -> account-level contextual model
    -> explicit worldview graph
```

The account-level layer does not need to contain literal graph nodes in the technical sense. Functionally, however, it can begin to behave as a soft ontology. Recurring concepts acquire relatively stable meanings; relations between concepts are preserved across inquiries; preferred distinctions become reusable coordinates; and new observations can be interpreted in relation to an accumulating conceptual structure.

In this sense, context engineering can externally instantiate part of the worldview that the base model does not permanently contain for one particular researcher.

The five-domain physical grammar therefore serves two purposes simultaneously.

First, it provides an explicit scientific framework through which mechanics, thermodynamics, acoustics, electromagnetics, and fluid mechanics can be compared.

Second, it provides a controlled test of whether an account-level contextual model can progressively acquire and reuse a coherent worldview through repeated interaction.

The proposed developmental path is:

```text
recurring contextual patterns
    -> stable conceptual coordinates
    -> explicit schema
    -> formal knowledge graph
```

At the first stage, concepts and relations are maintained through conversational memory and contextual retrieval. At later stages, they can be externalised as typed nodes, formulas, relations, maturity labels, provenance records, and validation rules.

This makes the account not merely a storage location for previous discussions, but an experimental context-engineering environment in which a worldview is progressively articulated before being formalised.

The relevant research question is therefore not only:

> Can an LLM reason over an explicit worldview?

It is also:

> Can repeated, account-level context engineering help a human and an LLM jointly crystallise a worldview that begins as conversational structure and later becomes an explicit scientific ontology?

The [five-domain physical grammar](explorations/seed-vault/05-experiments/CML-Science-Experiment.md) provides a first controlled domain in which this development can be observed. It compares matched models from mechanics, thermodynamics, acoustics, electromagnetics, and fluid mechanics through recurring roles such as energy storage, effort, flow, resistance, power, resonance, dissipation, and system boundaries. Its scientific foundations and falsifiable comparison method are developed in [A Five-Domain Energy Grammar](explorations/seed-vault/01-papers/00-foundation/Five-Domain-Energy-Grammar-Paper-0.md).

Known formulas populate the established conceptual positions. Regime, maturity, provenance, and dimensional constraints prevent a visual analogy from being treated automatically as a valid correspondence. Structural asymmetries and rejected mappings remain visible as negative evidence, while weak or incomplete positions invite explicitly labelled candidate imputations. The resulting worldview can then be externalised and tested independently of the conversational account in which it first emerged.
