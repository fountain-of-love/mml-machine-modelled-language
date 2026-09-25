---
artifact: concept-seed
status: candidate
updated: 2026-08-28
wikidata_id: Q80006
concept_uri: https://www.wikidata.org/entity/Q80006
wikipedia_anchor: https://en.wikipedia.org/wiki/Computer_programming
---

# Computer Programming

## Identity

- Canonical label: `computer_programming`
- Local id: `form.computer_programming`
- Status: `candidate`

## Human Introduction

Computer programming is the practice of turning an intended task into precise instructions a computer can execute. A person may want to sort records, display a page, automate a workflow, simulate a system, or process sensor data, but the machine cannot act on that intention until the task is expressed in an executable form.

In ordinary use, people often treat programming as "writing code," and that is close enough for first orientation. But the concept is slightly richer than typing syntax. Programming usually includes translating a problem into steps, choosing representations, expressing control flow, testing behavior, fixing faults, and revising the program as the problem changes.

This concept matters in the current repository because it is one of the clearest bridges between human semantic intent and machine-operational execution. It sits under the broader computing umbrella, touches algorithm, data structure, and software engineering, and becomes a useful anchor for later MML-oriented distinctions between meaning, representation, and execution.

## Definition

Computer programming is the computing practice of designing, expressing, testing, and maintaining executable instructions so that a computational system performs a declared task or class of tasks.

## Operational View

- Parent branch: `form`
- Immediate parent concepts:
  - `form.computer_science`
  - `form.computing`
- Typical child concepts:
  - `form.programming_language`
  - `form.compiler`
  - `form.debugging`
  - `form.script`
  - `form.source_code`
- Adjacent concepts:
  - `form.algorithm`
  - `form.data_structure`
  - `form.software_engineering`
  - `form.information_technology`
- Typical relations:
  - `(form.computer_programming, within, form.computer_science)`
  - `(form.computer_programming, uses, form.algorithm)`
  - `(form.computer_programming, uses, form.data_structure)`
  - `(form.computer_programming, adjacent_to, form.software_engineering)`

## Process Shape

Computer programming should be navigable as a process graph, not only as a topic. A simple path is:

```text
problem framing
  -> algorithm design
  -> source code authoring
  -> testing
  -> debugging
  -> source code revision
```

This path is intentionally cyclic. Debugging does not merely happen after programming; it can feed revised code back into testing, maintenance, and new problem framing.

Process tuple hints:

```text
(form.computer_programming, has_stage, form.problem_framing)
(form.problem_framing, precedes, form.algorithm_design)
(form.algorithm_design, precedes, form.source_code_authoring)
(form.source_code_authoring, produces, form.source_code)
(form.source_code, input_to, form.testing)
(form.testing, precedes, form.debugging)
(form.debugging, revised_into, form.source_code)
```

## LLM Synthesis

Across model-style explanations, the stable common core is that computer programming means expressing problem-solving steps in a form a computer can execute. The strongest beginner-friendly explanations emphasize instructions, examples, variables, loops, functions, and the path from problem to code to test and debugging.

One useful distinction surfaced especially clearly in the user-provided ChatGPT-style explanation: programming is often taught as writing a recipe for the machine, which helps orientation, but the ontology should keep that metaphor subordinate to the more exact idea of executable representation. The main remaining ambiguity is boundary: programming overlaps strongly with software engineering, but software engineering is broader in lifecycle and system coordination than programming alone.

## Boundary

Included:

- writing executable instructions
- coding and implementation practice
- program construction and revision
- operational bridge between design and execution
- expressing algorithms in executable form
- testing and debugging as part of making code operative

Excluded:

- computer science as a whole
- every lifecycle activity in software engineering
- hardware design without executable program logic
- abstract algorithm study without implementation context
- product management or requirements work apart from code expression
- infrastructure administration apart from program creation or modification

## Aliases

- programming
- coding
- program construction

## Representation Hints

- Tuple hints:
  - `(form.computer_programming, within, form.computer_science)`
  - `(form.computer_programming, within, form.computing)`
  - `(form.computer_programming, uses, form.algorithm)`
  - `(form.computer_programming, uses, form.data_structure)`
  - `(form.computer_programming, adjacent_to, form.software_engineering)`
  - `(form.computer_programming, has_stage, form.problem_framing)`
  - `(form.source_code, input_to, form.testing)`
  - `(form.debugging, revised_into, form.source_code)`
- Linked-data hints:
  - `rdf:type`
  - `skos:broader`
  - `skos:related`
- Retrieval phrases:
  - writing code
  - executable instructions
  - coding practice
  - implementing algorithms
  - debugging and testing code

## Provenance

- Form Computing Foundations Concept Ledger
- Wikidata `computer programming` (`Q80006`)
- English Wikipedia `Computer programming`
- User-provided ChatGPT-style explanatory sample on 2026-08-28

## Source Packet

- Wikidata item: `Q80006`
- Concept URI: `https://www.wikidata.org/entity/Q80006`
- Wikipedia anchor: `https://en.wikipedia.org/wiki/Computer_programming`
- Inventory seed: `Science-and-Technology-Wikipedia-Inventory-Seed`
- Ledger rows:
  - `Form-Computing-Foundations-Concept-Ledger`
  - `Form-Computing-Relation-Ledger`
- External ontology or schema references:
  - Wikidata statement model
  - RDF triple pattern
  - SKOS broader/related reading
- LLM synthesis inputs:
  - user-provided ChatGPT-style explanation focused on instructions, examples, control flow, and the problem-to-code process
  - local project synthesis shaped by current computing ledgers and seed-governance rules

## Open Questions

- Should programming remain a child of computer science, or later sit between computer science and software engineering?
- How should programming language, paradigm, and software development relate to this concept?
- Which child concepts should be seeded next to make this concept operational for navigation: `programming_language`, `source_code`, `debugging`, or `compiler`?
