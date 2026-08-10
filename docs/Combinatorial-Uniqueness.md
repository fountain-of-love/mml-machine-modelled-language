# Combinatorial Uniqueness

**Combinatorial uniqueness** is the operational name used in this project for a simple but powerful retrieval principle:

> Several individually broad, sufficiently independent conceptual constraints can form a narrow and highly distinctive intersection.

The phrase does not claim that MML invented conjunction, faceted search, product-of-experts inference, query composition, or vector intersection. It names how MML applies that family of ideas to governed, addressable concepts and typed relationships.

## Core Intuition

A single broad term usually has high recall and low precision:

- `attention` may refer to cognition, ADHD, economics, organisations, transformers, or user-interface design;
- `systems theory` spans engineering, biology, sociology, management, and cybernetics; and
- `ranking` appears in information retrieval, decision theory, sport, optimisation, and institutional priority-setting.

Taken separately, each concept activates a large field. Together, they express a more specific intent:

```text
attention
    + systems theory
    + ranking
    -> how complex macro-systems allocate focus and sequence priority
```

The combination is distinctive because each term constrains a different dimension of the intended region. `Attention` supplies the scarce resource, `systems theory` supplies the scale and relational frame, and `ranking` supplies ordering or allocation. A candidate supported by all three is more informative than one that happens to be strongly associated with only one.

## What “Orthogonal” Means Here

“Orthogonal” is used operationally, not as an unmeasured claim that two embedding vectors have a dot product of zero. The concepts should be **sufficiently independent constraints**:

- each removes plausible results admitted by the others;
- none is merely a synonym or predictable restatement of another;
- their conjunction retains relevant candidates rather than collapsing to nothing; and
- the combination expresses an intent that the individual terms do not.

This independence must be examined against the actual corpus and representation. It can be estimated through overlap, mutual information, ablation, or changes in hard-negative intrusion, but it should not be assumed from wording alone.

## How Retrieval Mechanisms Express the Idea

The same intuition appears differently across systems.

### Boolean and lexical retrieval

An inverted index can calculate a literal set intersection:

$$
S = S_{\mathrm{attention}} \cap S_{\mathrm{systems\ theory}} \cap S_{\mathrm{ranking}}
$$

This can sharply reduce the candidate set when documents contain all required terms. It can also miss relevant documents that express one concept with different vocabulary.

A relational database can perform the same logic when concepts have already been represented as explicit rows, tags, or relations. Relational databases do not inherently provide semantic vector search; the quality of the intersection depends on the schema and data entered.

### Dense-vector retrieval

Dense retrieval may encode related wording near one another geometrically. A composed query can sometimes retrieve material spanning several domains, but this is not automatically a literal intersection. Results depend on the embedding model, query construction, similarity function, index, and whether composition occurs before retrieval or through later score fusion.

Broad terms may improve cross-domain recall, but they can also pull a composed vector towards a generic midpoint that matches none of the intended constraints precisely. Claims about a particular search engine's embedding or ranking behaviour require direct evidence; this repository does not assume how Google Scholar internally ranks results.

### MML activation

MML gives each governed query concept its own propagated activation field. For concept fields $f_1, \ldots, f_k$, the shared combination step uses a geometric mean:

$$
C(x)
=
\frac{
\left(\prod_{i=1}^{k} \max(f_i(x), \epsilon)\right)^{1/k}
}{
\sum_y \left(\prod_{i=1}^{k} \max(f_i(y), \epsilon)\right)^{1/k}
}
$$

A candidate cannot dominate merely because one broad field assigns it a very high score. Weak support from another field suppresses the product. This behaves like a soft intersection over graph activation rather than an arithmetic average of query meanings. The larger probe bench normalises this combination directly; `GraphModel` first corrects it for background hub frequency and then normalises the final field.

The executable implementation is visible in [`GraphModel.activation`](../mml_graph.py) and the larger probe bench in [`query_anchored_diffusion`](../mml_elaborate_corpus.py). The regression test explicitly verifies that multi-token activation is not the additive average of individual fields.

## Why the Broad Combination Can Be Useful

### High intent at the intersection

Broad concepts preserve multiple vocabularies at the edges of a query, while their conjunction narrows the centre. In a suitable corpus, this can reduce noise substantially without requiring one brittle, discipline-specific phrase.

The size of that reduction is empirical. A claim that millions of results become hundreds—or that one paper obtains the highest rank—must be measured for a named search system, corpus, date, and query formulation.

### Cross-domain discovery

Concept-level combinations can connect work written in different disciplinary dialects. Political science may discuss attention allocation in institutions, computer science may discuss ranking and attention mechanisms, and economics may discuss scarce attention. A governed conceptual query can preserve those bridges while still requiring shared structural support.

This benefit depends on aliases, ontology coverage, corpus diversity, and relation quality. Broad terminology alone does not guarantee useful interdisciplinary discovery.

### Explicit conceptual alignment

In a future CML-shaped knowledge base, the query terms would not remain ambiguous strings. They would map to ranked concept candidates, typed relations, exclusions, and provenance. MML could then execute their intersection over stable semantic identities rather than relying entirely on latent geometric proximity.

This is where combinatorial uniqueness connects CML and MML:

```text
CML: governed conceptual coordinates and typed relationships
    +
MML: independent activation fields and soft intersection
    =
inspectable combinatorial retrieval
```

## Failure Modes

The strategy can fail when:

- concepts are correlated rather than independently constraining;
- a term maps to the wrong sense;
- the required concept or alias is absent from the governed vocabulary;
- propagation makes every field too broad;
- the intersection is so strict that it suppresses relevant candidates;
- one field contains only tiny numerical support everywhere;
- authored relations encode the expected answer into the graph;
- the corpus and evaluation queries were curated together; or
- a compelling intersection is mistaken for proof of causality or reasoning.

Literal identifiers and original query terms should therefore be preserved beside concept routing. Lexical retrieval and concept activation should be evaluated independently and in combination.

## How to Test It

A defensible experiment should compare:

1. each single concept;
2. every concept pair;
3. the full three-concept combination;
4. Boolean lexical conjunction;
5. TF-IDF or BM25;
6. additive activation;
7. geometric-mean MML activation;
8. an available dense-retrieval baseline; and
9. lexical–MML fusion.

Use held-out documents, queries, and judgments. Report recall, precision, MRR, nDCG, zero-overlap recovery, hard-negative intrusion, and the number of candidates retained at each stage. Ablate aliases, typed relations, and each query concept so the contribution of curation and combination remains visible.

The central test is not whether three terms always beat one. It is:

> Does independently propagated, governed concept combination retrieve the intended intersection more accurately and inspectably than the relevant lexical, additive, and dense baselines, at an acceptable construction and execution cost?

That is a falsifiable mechanism claim. Academic visibility, search-engine ranking, and universal cross-domain discovery remain possible consequences to measure, not properties established by the current prototype.
