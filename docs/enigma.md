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

## Memory as a Combinatorial Uniqueness Playground

Enigma's account-level context has served as an informal playground for **[combinatorial uniqueness](Combinatorial-Uniqueness.md)**. Recurring conceptual coordinates are not introduced as isolated keywords. They are related across questions: MML with governed execution, CML with conceptual identity, SOS with architectural separation, and the five-domain grammar with cross-domain comparison and drift controls.

During this work, the researcher observed responses that felt faster, became longer and more complete when depth was useful, adhered more closely to the intended conceptual distinctions, and required fewer corrective turns. The working interpretation is that reusable conceptual combinations reduce the need to reconstruct intent from scratch. If the context already preserves several independent coordinates, their intersection can constrain the active meaning more precisely than one broad instruction.

These are **anecdotal observations, not established measurements**. Account-level retrieval is not fully controlled or exposed, model and product versions can change, and response latency depends on infrastructure as well as conceptual fit. Longer output is also not automatically more token-efficient. The relevant efficiency measure is supported, task-relevant content per input and output token, together with the number of repair turns—not output length alone.

The hypothesis to test is:

> Conceptually modelled context based on sufficiently independent, related coordinates reduces semantic search and reconstruction inside a bounded task, producing more accurate and stable responses with fewer unsupported claims and less corrective interaction than either no context or an equally sized unstructured context.

In practical terms, this predicts less drift and hallucination, but it does not claim to eliminate either.

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

## A Local Ollama Experiment

A local model makes the hypothesis testable without relying on opaque account-memory selection. [Qwen3-8B](https://qwenlm.github.io/blog/qwen3/) is an appropriate bounded example because it is an open-weight 8-billion-parameter model and is available through Ollama as `qwen3:8b`. The experiment simulates memory by supplying controlled context packets; it does not claim that Ollama implements OpenAI account memory.

### 1. Freeze the environment

Record:

- Ollama version;
- exact model name and digest;
- quantisation;
- hardware and available memory;
- context-window and generation limits;
- temperature, seed, and thinking mode;
- system prompt and prompt template; and
- every input, output, timing record, and evaluator decision.

Pull the model once and run all conditions locally:

```bash
ollama pull qwen3:8b
```

Ollama supports a fixed generation seed through runtime options. Use the same seed and `temperature: 0` for the primary deterministic comparison. Run a separate multi-seed track when measuring stochastic stability.

### 2. Build one source set and four context conditions

Start from one frozen set of facts and definitions. Derive context packets with comparable token budgets:

| Condition | Context supplied | Purpose |
| --- | --- | --- |
| **A — none** | Task only | Measures the local model without external worldview context |
| **B — flat** | The same facts as an unstructured memory summary | Controls for additional information and prompt length |
| **C — conceptual** | Stable concept identifiers, typed distinctions, relations, exclusions, and provenance | Tests context engineering based on combinatorial uniqueness |
| **D — ablated** | Condition C with one coordinate removed, relations shuffled, or labels made ambiguous | Tests whether structure—not formatting alone—causes the effect |

For the combinatorial component, include single-coordinate, pair, and triple variants. For example:

```text
attention
attention + systems theory
attention + systems theory + ranking
```

The expected result is not that more terms always help. It is that a relevant, sufficiently independent combination improves the intended intersection, while an irrelevant or shuffled combination should not.

### 3. Use held-out tasks

Prepare at least 30–50 prompts that were not used to write the context packets. The five-domain grammar provides a bounded source domain with known formulas, explicit maturity labels, negative mappings, and provenance. Include:

- direct factual questions;
- ambiguous terminology requiring sense selection;
- cross-domain comparisons;
- questions whose answer requires two or three conceptual coordinates;
- hard negatives where a plausible analogy must be rejected;
- insufficient-evidence cases where the model should abstain; and
- paraphrased versions of the same intent for drift measurement.

Freeze an answer key and evidence packet before running the model. Human assessors should be blind to the context condition when scoring outputs.

### 4. Execute a randomised crossover

Run every task under all four conditions in random order. Start with warmed model state so model-loading time does not contaminate inference latency. Use fresh conversational state for each trial and prohibit tools or network access.

An Ollama `/api/generate` request can keep the primary comparison repeatable:

```json
{
  "model": "qwen3:8b",
  "system": "<condition-specific context packet>",
  "prompt": "<held-out task>",
  "stream": false,
  "options": {
    "temperature": 0,
    "seed": 42,
    "num_predict": 1024
  }
}
```

Repeat the deterministic run to detect execution variance. Then repeat with several declared seeds at a low non-zero temperature to measure whether conceptual context reduces output variance rather than merely fixing one decode.

### 5. Measure separate outcomes

Do not collapse all observations into one quality score.

| Dimension | Suggested measure |
| --- | --- |
| **Accuracy** | Blind rubric score against the frozen answer key |
| **Hallucination** | Unsupported atomic claims divided by all atomic claims |
| **Drift** | Contradictions or rubric variance across paraphrases and seeds |
| **Completeness** | Required supported points present |
| **Sense control** | Correct interpretation and exclusion of prohibited senses |
| **Latency** | Prompt-evaluation time, generation time, and total warmed latency |
| **Output length** | Generated token count, reported independently |
| **Token efficiency** | Supported required claims per total input and output token |
| **Repair cost** | Corrective turns and tokens needed to reach an acceptable answer |
| **Energy proxy** | Wall time, tokens processed, throughput, and optional device power measurement |

The Ollama response exposes timing and token-count fields that can support the latency and throughput analysis. Hardware power measurement, if available, should remain a separate observation rather than being inferred from token count alone.

### 6. Decide what would count as evidence

Pre-register thresholds before inspecting results. The hypothesis receives support only if conceptual context outperforms both the no-context and equal-information flat-context conditions on held-out quality and unsupported-claim measures. Condition D should degrade predictably; otherwise the apparent benefit may come from extra tokens, formatting, or evaluator preference rather than conceptual relationships.

A credible result would show some combination of:

- higher blind accuracy and completeness;
- lower unsupported-claim rate;
- lower variance across paraphrases and seeds;
- fewer corrective turns; and
- better supported-claim yield per token or unit of measured compute.

Faster responses and longer responses are separate hypotheses. A structured prompt can improve generation focus while increasing prompt-evaluation cost, and a longer answer can be more useful while consuming more tokens. The experiment should report those trade-offs rather than defining every increase as an efficiency gain.

A null or negative result is informative. It may show that the model already infers the structure, that the context packet is poorly designed, that the concepts are not sufficiently independent, or that context overhead exceeds its benefit. That is precisely why the account-level observation should be externalised into a controlled local experiment.

For the current Ollama request contract and generation options, see the official [Generate API](https://docs.ollama.com/api/generate) and [Modelfile parameter reference](https://docs.ollama.com/modelfile).
